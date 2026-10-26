#!/usr/bin/env python3
"""Count, per protocol audit, the distinct functions linked by High and Medium findings.

Reads the downloaded Solodit findings and the Tier 1 Solidity files (read-only) and writes one CSV row
per protocol audit. Prints the tables used in README.md. Standard library only.

Usage: python3 -I proposal_workspace/evidence/frame_inventory/frame_inventory.py [--out per_protocol_audit.csv]
"""
import argparse, csv, json, random, re, statistics, sys
from collections import Counter, defaultdict
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT / "data_collection"
sys.dont_write_bytecode = True  # do not leave a cache next to the imported script
sys.path.insert(0, str(ROOT / "scripts"))
from filter_tier1_after_cutoff import linked_month  # same date-from-links rule as tier1_master.csv

KEEP_RATE = 17 / 34  # one-function fixes among the 34 pilot findings with an identified fix
SEED, REPS, CAP = 20261022, 20000, 6
WELL_MAPPED = 0.8  # an audit is "well mapped" when at least this share of its H/M findings is mapped
# A GitHub link to a .sol file, optionally followed by ?plain=1 and a line anchor #L<n>.
LINK = re.compile(r"https://github\.com/([\w.-]+)/([\w.-]+)/blob/([\w.-]+)/([\w\-./]+?\.sol)"
                  r"(?:\?plain=1)?(?:#\s*L(\d+))?")
TEST_PATH = re.compile(r"(^|/)(test|tests|testing)/|\.t\.sol$|\.s\.sol$", re.I)
DECL = re.compile(r"^[ \t]*(?:(function)\s+(\w+)|(function)\s*\(|(modifier)\s+(\w+)|(constructor)\s*\(|"
                  r"(fallback)\s*\(|(receive)\s*\()", re.M)


def audit_key(f):
    """One key per audit report or contest."""
    if f["contest_id"]:
        return f"{f['firm_name']} | contest {f['contest_id']}"
    if f["kind"] == "GIT":  # Immunefi boosts: links are per finding, the protocol name is per boost
        return f"{f['firm_name']} | {f['protocol_name']}"
    for k in ("pdf_link", "source_link", "contest_link"):
        if f[k]:
            return f"{f['firm_name']} | {f[k].split('#')[0].rstrip('/')}"
    return f"{f['firm_name']} | {f['protocol_name']}"


def blank_comments_and_strings(src):
    """Replace comments and string literals with spaces, keeping newlines so line numbers stay put."""
    out, i, n = list(src), 0, len(src)
    while i < n:
        c, nxt = src[i], src[i + 1] if i + 1 < n else ""
        if c == "/" and nxt in "/*":
            end = src.find("\n", i) if nxt == "/" else src.find("*/", i + 2)
            end = n if end == -1 else end + (0 if nxt == "/" else 2)
        elif c in "\"'":
            end = i + 1
            while end < n and src[end] != c and src[end] != "\n":
                end += 2 if src[end] == "\\" else 1
            end = min(end + 1, n)
        else:
            i += 1
            continue
        for j in range(i, end):
            if out[j] != "\n":
                out[j] = " "
        i = end
    return "".join(out)


def function_spans(src):
    """[(name, first_line, last_line)] for every function, modifier, constructor, fallback, receive
    with a body. A span starts at the comment or blank lines directly above the declaration, so a link to
    a function's NatSpec maps to that function. Returns None when the braces do not balance."""
    text = blank_comments_and_strings(src)
    blank = [not ln.strip() for ln in text.split("\n")]
    match, stack = {}, []
    for i, c in enumerate(text):
        if c == "{":
            stack.append(i)
        elif c == "}":
            if not stack:
                return None
            match[stack.pop()] = i
    if stack:
        return None
    line_at = lambda pos: text.count("\n", 0, pos) + 1  # noqa: E731
    spans, header_end = [], -1
    for m in DECL.finditer(text):
        if m.start() < header_end:  # a function type inside the previous header's parameter list
            continue
        kind = next(g for g in m.groups() if g in ("function", "modifier", "constructor", "fallback", "receive"))
        name = m.group(2) or m.group(5) or ("fallback" if kind == "function" else kind)  # function() = old fallback
        brace, semi = text.find("{", m.end()), text.find(";", m.end())
        if brace == -1 or (semi != -1 and semi < brace):
            continue  # declaration without a body (interface, abstract, function-type variable)
        header_end = brace
        start = line_at(m.start())
        while start > 1 and blank[start - 2]:
            start -= 1
        spans.append((name, start, line_at(match[brace])))
    return spans


def enclosing(spans, line):
    """Outermost span containing the line (outermost, so a Yul function maps to its Solidity function)."""
    hits = [s for s in spans if s[1] <= line <= s[2]]
    return min(hits, key=lambda s: s[1])[0] if hits else None


def load():
    findings = []
    for path in sorted((DATA / "downloaded_findings").glob("batch_*_solodit_findings.json")):
        findings += json.loads(path.read_text())
    tier1 = {}  # (owner, repo, ref, path) -> local .sol file; any finding's Tier 1 copy of that file
    for meta_path in sorted(DATA.glob("batch_*_extracted_contracts/tier_1_complete/*.json")):
        m = LINK.match(json.loads(meta_path.read_text()).get("source_url") or "")
        if m and meta_path.with_suffix(".sol").exists():
            tier1.setdefault(m.groups()[:4], meta_path.with_suffix(".sol"))
    return findings, tier1


def map_finding(f, tier1, span_cache):
    """Status of one finding and the function keys it links to (first line link, and all line links)."""
    links = [m.groups() for m in LINK.finditer(f["content"]) if not TEST_PATH.search(m.group(4))]
    line_links = [g for g in links if g[4]]
    if not links:
        return "no_sol_link", None, set()
    if not line_links:
        return "no_line_link", None, set()
    first, every, statuses = None, set(), []
    for owner, repo, ref, path, line in line_links:
        sol = tier1.get((owner, repo, ref, path))
        if sol is None:
            statuses.append("no_tier1_file")
            continue
        if sol not in span_cache:
            span_cache[sol] = function_spans(sol.read_text(errors="replace"))
        spans = span_cache[sol]
        if spans is None:
            statuses.append("parse_failure")
            continue
        name = enclosing(spans, int(line))
        if name is None:
            statuses.append("line_outside_function")
            continue
        key = f"{Path(path).name}::{name}"
        every.add(key)
        first = first or key
    if first:
        return "mapped", first, every
    for s in ("parse_failure", "line_outside_function", "no_tier1_file"):  # report the most informative reason
        if s in statuses:
            return s, None, set()




# Text check only (not used for counting): the first function named in backticks in the title or description,
# written as `Name::fn`, `Name.fn(` or `fn(`. Used to test whether text names could replace line links.
CODE_SPAN, COLON_NAME = re.compile(r"`([^`\n]{1,160})`"), re.compile(r"\b\w+::([A-Za-z_]\w*)")
CALL_NAME = re.compile(r"\b([A-Za-z_]\w*)\s*\(")
NOT_TARGET = set("require revert assert keccak256 abi encode encodePacked decode transfer transferFrom safeTransfer "
                 "safeTransferFrom approve safeApprove balanceOf totalSupply call delegatecall staticcall send "
                 "uint256 uint address bytes32 bytes int256 uint128 uint8 type emit new mulDiv max min".split())
TAIL = re.compile(r"\n#+\s*(?:Recommend|Mitigation|Proof of Concept|PoC)|\*\*(?:Recommend|Proof of Concept)")


def text_function_name(f):
    for src in (f["title"], TAIL.split(f["content"])[0]):
        for span in CODE_SPAN.findall(src):
            for name in COLON_NAME.findall(span) + CALL_NAME.findall(span):
                if name not in NOT_TARGET:
                    return name
    return None


def simulate(counts, rate, rng):
    """Average share of audits with min(CAP, kept) = 0..CAP when each of n items is kept with `rate`."""
    tally = Counter()
    for _ in range(REPS):
        for n in counts:
            tally[min(CAP, sum(rng.random() < rate for _ in range(n)))] += 1
    return [tally[k] / (REPS * len(counts)) for k in range(CAP + 1)]


def exact(counts, rate):
    """Exact version of simulate(), used as a check."""
    out = [0.0] * (CAP + 1)
    for n in counts:
        for k in range(n + 1):
            out[min(CAP, k)] += comb(n, k) * rate ** k * (1 - rate) ** (n - k) / len(counts)
    return out


def histogram(values):
    h = Counter(min(v, CAP) for v in values)
    return [h[k] for k in range(CAP + 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "per_protocol_audit.csv"))
    a = ap.parse_args()

    # Self-check of the function finder on a small contract.
    demo = ('contract A {\n modifier m() { _; }\n // function fake() {\n'
            ' function f(function(uint) external g) external m {\n  string memory s = "}";\n'
            '  assembly { function y() {} }\n }\n function i() external;\n receive() external payable {}\n}\n')
    spans = function_spans(demo)
    assert [s[0] for s in spans] == ["m", "f", "receive"], spans
    assert enclosing(spans, 6) == "f" and enclosing(spans, 8) is None and enclosing(spans, 9) == "receive"
    assert enclosing(spans, 3) == "f"  # comment line directly above f

    findings, tier1 = load()
    assert len({f["id"] for f in findings}) == len(findings), "duplicate finding ids"
    span_cache, audits = {}, defaultdict(list)
    for f in findings:
        status, first, every = map_finding(f, tier1, span_cache)
        f.update(_status=status, _first=first, _every=every, _month=linked_month(f)[0])
        audits[audit_key(f)].append(f)

    rows = []
    for key, fs in audits.items():
        months = [f["_month"] for f in fs if f["_month"]]
        st = Counter(f["_status"] for f in fs)
        first_funcs = {f["_first"] for f in fs if f["_first"]}
        rows.append(dict(
            audit_key=key, firm=fs[0]["firm_name"],
            protocol=Counter(f["protocol_name"] for f in fs).most_common(1)[0][0],
            year=max(months) // 100 if months else "",
            month=f"{max(months) // 100}-{max(months) % 100:02d}" if months else "",
            hm_findings=len(fs), high=sum(f["impact"] == "HIGH" for f in fs),
            medium=sum(f["impact"] == "MEDIUM" for f in fs),
            solidity_signal=any(".sol" in f["content"] or "```solidity" in f["content"] for f in fs),
            mapped=st["mapped"], unmapped=len(fs) - st["mapped"],
            share_unmapped=round((len(fs) - st["mapped"]) / len(fs), 3),
            well_mapped=st["mapped"] >= WELL_MAPPED * len(fs),
            distinct_functions=len(first_funcs),
            distinct_functions_all_links=len(set().union(*(f["_every"] for f in fs))),
            findings_linking_several_functions=sum(len(f["_every"]) > 1 for f in fs),
            **{f"unmapped_{s}": st[s] for s in ("no_sol_link", "no_line_link", "no_tier1_file",
                                                  "line_outside_function", "parse_failure")},
            functions=";".join(sorted(first_funcs))))
    rows.sort(key=lambda r: (str(r["year"]), r["firm"], r["audit_key"]))

    well = [r for r in rows if r["well_mapped"]]
    per_finding = sum(r["distinct_functions"] for r in well) / sum(r["mapped"] for r in well)
    rng = random.Random(SEED)
    for r in rows:  # one fixed-seed draw per audit, ready to use as a sampling vector
        r["adjusted_draw"] = min(CAP, sum(rng.random() < KEEP_RATE for _ in range(r["distinct_functions"])))
        r["model_draw"] = min(CAP, sum(rng.random() < per_finding * KEEP_RATE for _ in range(r["hm_findings"])))
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # ---- printed tables -------------------------------------------------------------------------
    p = print
    st = Counter(f["_status"] for f in findings)
    mapped = [f for f in findings if f["_status"] == "mapped"]
    p(f"findings {len(findings)}  impacts {dict(Counter(f['impact'] for f in findings))}")
    p(f"Tier 1 files indexed by (owner, repo, ref, path): {len(tier1)}; files parsed {len(span_cache)}, "
      f"parse failures {sum(v is None for v in span_cache.values())}")
    p("finding status:", dict(st.most_common()))
    p(f"mapped findings whose function name appears in the title or text: "
      f"{sum(f['_first'].split('::')[1] in f['title'] + f['content'] for f in mapped)} of {len(mapped)}")
    both = [(f["_first"].split("::")[1], t) for f in mapped if (t := text_function_name(f))]
    p(f"text-name check: {len(both)} mapped findings also name a function in backticks; "
      f"same function as the line link in {sum(x == y for x, y in both)}")
    p(f"\nprotocol audits {len(rows)}; with a Solidity signal {sum(r['solidity_signal'] for r in rows)}; "
      f"well mapped (>= {WELL_MAPPED:.0%} of H/M findings mapped) {len(well)}")
    p("\naudits by firm (all | Solidity signal | well mapped | 2025+ | 2025+ well mapped):")
    new = lambda r: r["year"] != "" and r["year"] >= 2025  # noqa: E731
    for firm, n in Counter(r["firm"] for r in rows).most_common():
        fr = [r for r in rows if r["firm"] == firm]
        p(f"  {firm}: {n} | {sum(r['solidity_signal'] for r in fr)} | {sum(r['well_mapped'] for r in fr)} | "
          f"{sum(new(r) for r in fr)} | {sum(new(r) and r['well_mapped'] for r in fr)}")
    p("\naudits by year (all | Solidity signal | well mapped):")
    for y in sorted({str(r["year"]) for r in rows}):
        yr = [r for r in rows if str(r["year"]) == y]
        p(f"  {y or 'undated'}: {len(yr)} | {sum(r['solidity_signal'] for r in yr)} | {sum(r['well_mapped'] for r in yr)}")

    groups = {
        "all audits": rows,
        "Solidity signal": [r for r in rows if r["solidity_signal"]],
        "well mapped": well,
        "2025+": [r for r in rows if new(r)],
        "2025+ Solidity signal": [r for r in rows if new(r) and r["solidity_signal"]],
        "2025+ well mapped": [r for r in well if new(r)],
    }
    p("\ndistinct linked functions per audit (first line link): audits with 0,1,2,3,4,5,6+")
    for name, g in groups.items():
        v, va = [r["distinct_functions"] for r in g], [r["distinct_functions_all_links"] for r in g]
        hm, un = sum(r["hm_findings"] for r in g), sum(r["unmapped"] for r in g)
        p(f"  {name}: n={len(g)} {histogram(v)} mean={statistics.mean(v):.2f} median={statistics.median(v)} "
          f"| all links: {histogram(va)} mean={statistics.mean(va):.2f} median={statistics.median(va)} "
          f"| H/M {hm}, unmapped {un} ({un / hm:.1%}), H/M per audit mean {hm / len(g):.1f} "
          f"median {statistics.median(r['hm_findings'] for r in g)}")

    p(f"\ndistinct functions per mapped finding in well-mapped audits: {per_finding:.3f}; by mapped findings per audit:")
    for lo, hi in ((1, 1), (2, 3), (4, 6), (7, 10), (11, 20), (21, 10 ** 6)):
        b = [r for r in well if lo <= r["mapped"] <= hi]
        if b:
            p(f"  {lo}-{hi if hi < 10 ** 6 else ''}: audits {len(b)}, "
              f"{sum(r['distinct_functions'] for r in b) / sum(r['mapped'] for r in b):.3f}")

    def show(label, g, field, rate):
        v = [r[field] for r in g]
        sim, ex = simulate(v, rate, random.Random(SEED)), exact(v, rate)
        assert all(abs(s - e) < 0.01 for s, e in zip(sim, ex)), (sim, ex)
        p(f"  {label}: n={len(g)} share 0..6 = {[round(s, 3) for s in sim]} "
          f"expected audits = {[round(s * len(g), 1) for s in sim]} mean={sum(k * s for k, s in enumerate(sim)):.2f} "
          f"median={next(k for k in range(CAP + 1) if sum(sim[:k + 1]) >= 0.5)}")

    p(f"\n(a) direct: each linked function kept with {KEEP_RATE:.2f}, cap {CAP}, {REPS} replicates, seed {SEED}")
    for name, g in groups.items():
        show(name, g, "distinct_functions", KEEP_RATE)
    p(f"\n(b) model: each H/M finding gives a kept function with {per_finding:.3f} x {KEEP_RATE:.2f} "
      f"= {per_finding * KEEP_RATE:.3f}, cap {CAP}")
    for name in ("Solidity signal", "2025+ Solidity signal"):
        show(name, groups[name], "hm_findings", per_finding * KEEP_RATE)

    for name, field in (("2025+ Solidity signal", "distinct_functions"), ("2025+ Solidity signal", "adjusted_draw"),
                        ("2025+ well mapped", "distinct_functions"), ("2025+ well mapped", "adjusted_draw"),
                        ("2025+ Solidity signal", "model_draw")):
        p(f"\n{name}, {field}:", [r[field] for r in groups[name]])
    p(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
