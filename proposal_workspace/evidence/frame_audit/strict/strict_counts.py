#!/usr/bin/env python3
"""Strict V and N counts for the 25 audits of the frame audit. Standard library only. No network.

Reads the frame audit files one folder up (per_audit.csv, per_finding.csv, scope_files.csv), the hand re-read of
fix scope in this folder (fix_reread.csv), and the cloned repositories in --work/<slug>/repo. It runs nothing from
the repositories. It writes per_function_strict.csv and per_audit_strict.csv in this folder and prints the tables.

Usage:
    python3 -I strict_counts.py --work <frame audit work folder>
    python3 -I strict_counts.py --selftest

Rules, as in the proposal:
  - A function is identified by its full path, its contract (or library), its name and its parameter types.
  - Eligibility is the counting rule of ../count_functions.py, applied to V and N alike.
  - Strict V: the function is a root cause of a High or Medium finding, it is eligible, and the developers' fix,
    read as a diff, changes only that function's body. fix_reread.csv records the reading.
  - Strict V upper bound: strict V plus the same test applied to the finding's recommendation.
  - Strict N: eligible functions minus every function linked to any High or Medium finding.
"""
import argparse, csv, re, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True  # leave the folder above unchanged
sys.path.insert(0, str(HERE.parent))
import count_functions as cf  # noqa: E402  the original counting rule, reused unchanged

CONTAINER = re.compile(r"(?<![\w.])(?:abstract\s+)?(contract|library|interface)\s+(\w+)[^;{]*\{")
LOCATION = {"memory", "storage", "calldata", "indexed"}
KEEP_LAST = {"payable", "external", "internal", "public", "private", "view", "pure", "returns"}
ALIAS = {"uint": "uint256", "int": "int256", "byte": "bytes1", "ufixed": "ufixed128x18", "fixed": "fixed128x18"}


def split_top(s):
    """Split on commas that are not inside brackets."""
    out, depth, cur = [], 0, ""
    for c in s:
        depth += {"(": 1, "[": 1, ")": -1, "]": -1}.get(c, 0)
        if c == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += c
    return out + [cur] if cur.strip() else out


def param_type(p):
    """'uint256[] memory amounts' -> 'uint256[]'; 'address payable to' -> 'address payable'."""
    p = re.sub(r"\s+([\[\]().,])", r"\1", " ".join(p.split()))
    p = re.sub(r"([\[(.,])\s+", r"\1", p)
    toks = [t for t in p.split(" ") if t not in LOCATION]
    if len(toks) > 1 and re.fullmatch(r"[A-Za-z_$][\w$]*", toks[-1]) and toks[-1] not in KEEP_LAST:
        toks = toks[:-1]  # drop the parameter name
    return re.sub(r"\b(u?int|byte|u?fixed)\b(?![\dx])", lambda m: ALIAS[m.group(1)], " ".join(toks))


def params_of(header):
    start = header.find("(")
    depth = 0
    for i in range(start, len(header)):
        depth += {"(": 1, ")": -1}.get(header[i], 0)
        if depth == 0:
            return ",".join(param_type(p) for p in split_top(header[start + 1:i]))
    return ""


def parse(src):
    """[(container, container_kind, name, kind, types, header, body)], same functions as cf.functions()."""
    text = cf.blank_comments_and_strings(src)
    match, stack = {}, []
    for i, c in enumerate(text):
        if c == "{":
            stack.append(i)
        elif c == "}":
            match[stack.pop()] = i
    boxes = []
    for m in CONTAINER.finditer(text):
        b = m.end() - 1
        boxes.append((b, match[b], m.group(2), m.group(1)))
    out, header_end = [], -1
    for m in cf.DECL.finditer(text):  # same loop as cf.functions, keeping the position
        if m.start() < header_end:
            continue
        kind = next(g for g in m.groups() if g in ("function", "constructor", "fallback", "receive"))
        name = m.group(2) or ("fallback" if kind == "function" else kind)
        brace, semi = text.find("{", m.end()), text.find(";", m.end())
        if brace == -1 or (semi != -1 and semi < brace):
            continue
        header_end = brace
        inside = [x for x in boxes if x[0] < m.start() < x[1]]
        box = max(inside, key=lambda x: x[0]) if inside else (0, 0, "(file level)", "file")
        header = text[m.start():brace]
        out.append((box[2], box[3], name, kind, params_of(header), header, text[brace + 1:match[brace]]))
    return out


def read_csv(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def selftest():
    src = """
    library L { function f(uint a) internal pure returns (uint) { return a; } }
    contract A { function f(uint256 a, address payable b) external { x = a; }
                 function f(bytes calldata d, uint[] memory xs) external { x = 1; } uint x; }
    abstract contract B is A { function g(function (uint) external cb) internal { cb(1); }
                               constructor() { } receive() external payable { } }
    function free(uint a) pure returns (uint) { return a + 1; }"""
    got = [(c, n, t) for c, ck, n, k, t, h, b in parse(src)]
    assert got == [("L", "f", "uint256"), ("A", "f", "uint256,address payable"), ("A", "f", "bytes,uint256[]"),
                   ("B", "g", "function(uint256) external"), ("B", "constructor", ""), ("B", "receive", ""),
                   ("(file level)", "free", "uint256")], got
    assert [x[2] for x in parse(src)] == [x[0] for x in cf.functions(src)]
    print("selftest ok")


def identities(work, scope_rows, old_fns):
    """Re-parse every in-scope file. Checks that the function list and eligibility match the original count."""
    rows = []
    for slug, paths in scope_rows.items():
        for path in paths:
            fns = parse((work / slug / "repo" / path).read_text(errors="replace"))
            for cont, ckind, name, kind, types, header, body in fns:
                ok, why, vp, st, br = cf.classify(header, body)
                rows.append(dict(slug=slug, path=path, contract=cont, contract_kind=ckind,
                                 function_key="{}::{}".format(Path(path).name, name), name=name, kind=kind,
                                 param_types=types, identity="{}::{}.{}({})".format(path, cont, name, types),
                                 view_or_pure=vp, statements=st, branch=br, eligible=ok, reason=why,
                                 # view or pure functions only: a non-view function with assembly still writes state
                                 eligible_without_assembly_rule=ok if not vp else
                                 cf.classify(header, body.replace("assembly", "_"))[0]))
    old = [(r["slug"], r["path"], r["function"], r["eligible"]) for r in old_fns]
    new = [(r["slug"], r["path"], r["function_key"], str(r["eligible"])) for r in rows]
    assert old == new, "re-parse differs from functions_in_scope.csv"
    return rows


# Names that stand for two or more functions, resolved by reading the finding. Values are Contract.name(types).
ROOT_RESOLVE = {
    ("code4rena-507", "58351", "Governor.sol::_castVote"):  # line link L534-L554 is the five-parameter overload
        ["L2Governor._castVote(uint256,address,uint8,string,bytes)"],
    ("sherlock-991", "58593", "GatewaySend.sol::depositAndCall"):  # link names the first; both use raw transferFrom
        ["GatewaySend.depositAndCall(address,uint256,bytes,address,address,uint32,bytes)",
         "GatewaySend.depositAndCall(address,uint256,address,uint32,bytes)"],
    ("sherlock-1001", "62485", "AbstractYieldStrategy.sol::price"): ["AbstractYieldStrategy.price()"],  # L118-L120
    ("sherlock-1001", "62515", "CurveConvex2Token.sol::TOKENS"):  # link is L162; the vault's copy is identical
        ["CurveConvexLib.TOKENS()", "CurveConvex2Token.TOKENS()"],
    ("sherlock-1001", "62516", "CurveConvex2Token.sol::constructor"):  # the note names the CurveConvexLib constructor
        ["CurveConvexLib.constructor(address,address,address,uint8,DeploymentParams)"],
    ("code4rena-502", "58559", "StakingManager.sol::processL1Operations"):  # line link L627-L666
        ["StakingManager.processL1Operations(uint256)"],
    ("code4rena-489", "65100", "LibStaking.sol::confirmChange"): ["LibStaking.confirmChange(uint64)"],  # L584
}
REREAD_CHANGES = {"none", "new error or event", "import", "new or removed function", "header of the changed function",
                  "other declaration", "storage layout"}


def dist(values, top=6):
    c = Counter(min(v, top) for v in values)
    return [c.get(i, 0) for i in range(top + 1)]


def quart(values):
    q = statistics.quantiles(values, n=4, method="inclusive")
    return min(values), q[0], statistics.median(values), q[2], max(values), statistics.mean(values)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    work = Path(a.work)
    audits = [r for r in read_csv(HERE.parent / "per_audit.csv") if r["status"] == "processed"]
    scope = defaultdict(list)
    for r in read_csv(HERE.parent / "scope_files.csv"):
        scope[r["slug"]].append(r["path"])
    fns = identities(work, {x["slug"]: scope[x["slug"]] for x in audits},
                     read_csv(HERE.parent / "functions_in_scope.csv"))
    assert len({(r["slug"], r["identity"]) for r in fns}) == len(fns), "two functions share one identity"
    fn = {(r["slug"], r["identity"]): r for r in fns}
    by_old = defaultdict(list)
    for r in fns:
        by_old[(r["slug"], r["function_key"])].append(r["identity"])

    def resolve(slug, fid, key):
        ids = by_old.get((slug, key), [])
        if len(ids) > 1:
            want = ROOT_RESOLVE[(slug, fid, key)]
            ids = [i for i in ids if i.split("::", 1)[1] in want]
            assert len(ids) == len(want), (slug, fid, key)
        return ids

    findings = read_csv(HERE.parent / "per_finding.csv")
    reread = {(r["slug"], r["finding_id"]): r for r in read_csv(HERE / "fix_reread.csv")}
    one_body = {(r["slug"], r["finding_id"]) for r in findings if r["fix_class"] == "one function body"}
    assert set(reread) == one_body, set(reread) ^ one_body
    for f in findings:
        k = (f["slug"], f["finding_id"])
        f["roots"] = [i for key in f["root_cause_functions"].split(";") if "::" in key
                      for i in resolve(f["slug"], f["finding_id"], key.strip())]
        f["linked"] = set(f["roots"])
        f["strict"], f["why_not"] = "", []
        if k not in reread:
            continue
        r = reread[k]
        assert r["evidence"] == f["fix_evidence"], k
        changes = {c.strip() for c in r["outside_body_changes"].split(";")}
        assert changes <= REREAD_CHANGES and r["strict_one_body"] in ("yes", "no"), k
        target = r["target_identity"].strip()
        others = [i for key in r["other_bodies_changed"].split(";") if "::" in key
                  for i in by_old.get((f["slug"], key.strip()), [])]
        f["linked"] |= set(others) | ({target} if (f["slug"], target) in fn else set())
        if r["fix_read_now"] == "no":
            f["why_not"].append("fix diff not readable")
        f["why_not"] += sorted(changes - {"none"})
        if others or (r["other_bodies_changed"].strip() not in ("", "none")):
            f["why_not"].append("another function body changed")
        if r["strict_one_body"] == "yes" and f["why_not"]:
            raise AssertionError(("re-read says yes but lists a change", k))
        if r["strict_one_body"] == "no" and not f["why_not"]:
            f["why_not"].append("re-read: not a one-body change (see note)")
        if (f["slug"], target) not in fn:
            f["why_not"].append("changed function not in scope")
        else:
            if target not in f["roots"]:
                f["why_not"].append("changed function is not a root cause")
            if not fn[(f["slug"], target)]["eligible"]:
                f["why_not"].append("changed function not eligible")
        if not f["why_not"]:
            f["strict"] = target

    for r in fns:
        r.update(name_shared=len(by_old[(r["slug"], r["function_key"])]) > 1, linked_findings="",
                 strict_v_observed_findings="", strict_v_recommendation_findings="")
    for f in findings:
        for i in sorted(f["linked"]):
            row = fn[(f["slug"], i)]
            row["linked_findings"] = ";".join(filter(None, [row["linked_findings"], f["finding_id"]]))
        if f["strict"]:
            col = ("strict_v_observed_findings" if f["fix_evidence"] == "observed fix"
                   else "strict_v_recommendation_findings")
            row = fn[(f["slug"], f["strict"])]
            row[col] = ";".join(filter(None, [row[col], f["finding_id"]]))
    for r in fns:
        r["in_strict_n"] = r["eligible"] and not r["linked_findings"]

    out = []
    for x in audits:
        slug = x["slug"]
        rows = [r for r in fns if r["slug"] == slug]
        fs = [f for f in findings if f["slug"] == slug]
        groups = [ids for (s, _), ids in by_old.items() if s == slug and len(ids) > 1]
        v_obs = {f["strict"] for f in fs if f["strict"] and f["fix_evidence"] == "observed fix"}
        v_all = {f["strict"] for f in fs if f["strict"]}
        not_read = [f for f in fs if f["fix_evidence"] != "observed fix" or
                    reread.get((slug, f["finding_id"]), {}).get("fix_read_now") == "no"]
        out.append(dict(
            rank=x["rank"], slug=slug, protocol={"Audit 507": "Blackhole"}.get(x["protocol"], x["protocol"]),
            hm_findings=len(fs),
            functions_with_body=len(rows), name_collisions=len(groups),
            functions_sharing_a_name=sum(len(g) for g in groups),
            eligible_functions=sum(r["eligible"] for r in rows),
            linked_eligible_functions=sum(r["eligible"] and bool(r["linked_findings"]) for r in rows),
            strict_n=sum(r["in_strict_n"] for r in rows),
            strict_n_without_assembly_rule=sum(r["in_strict_n"] and r["eligible_without_assembly_rule"] for r in rows),
            original_n=int(x["n_functions"]), findings_fix_not_read=len(not_read),
            findings_fix_not_read_fixed_status=sum(f["sponsor_status"] == "fixed" for f in not_read),
            findings_one_body_observed=sum(f["fix_evidence"] == "observed fix" and (slug, f["finding_id"]) in reread
                                           for f in fs),
            findings_strict_observed=sum(bool(f["strict"]) and f["fix_evidence"] == "observed fix" for f in fs),
            findings_strict_recommendation=sum(bool(f["strict"]) and f["fix_evidence"] != "observed fix" for f in fs),
            strict_v_observed=len(v_obs), strict_v_upper_bound=len(v_all),
            original_v_observed=int(x["v_functions_observed"]),
            original_v_incl_recommendation=int(x["v_functions_incl_recommendation"])))

    for name, rows in (("per_function_strict.csv", fns), ("per_audit_strict.csv", out)):
        with open(HERE / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    report(out, findings, reread, fns, by_old)


def report(out, findings, reread, fns, by_old):
    tot = lambda k: sum(a[k] for a in out)  # noqa: E731
    print("| Rank | Audit | H/M findings | Fix not read | V observed (orig.) | Strict V observed | "
          "V incl. rec. (orig.) | Strict V upper bound | N (orig.) | Strict N | Collisions resolved |")
    print("|" + "---|" * 11)
    keys = ("hm_findings", "findings_fix_not_read", "original_v_observed", "strict_v_observed",
            "original_v_incl_recommendation", "strict_v_upper_bound", "original_n", "strict_n", "name_collisions")
    for a in out:
        print("| {} | {} | {} |".format(a["rank"], a["protocol"], " | ".join(str(a[k]) for k in keys)))
    print("| | **Total** | " + " | ".join("**{}**".format(tot(k)) for k in keys) + " |")
    print("\n| Strict V per audit | 0 | 1 | 2 | 3 | 4 | 5 | 6 or more | Mean | Median | Total |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for label, k in (("Observed fixes", "strict_v_observed"), ("Upper bound (observed plus recommendation)",
                                                              "strict_v_upper_bound")):
        v = [a[k] for a in out]
        print("| {} | {} | {:.2f} | {:g} | {} |".format(label, " | ".join(map(str, dist(v))), statistics.mean(v),
                                                      statistics.median(v), sum(v)))
        print("    mean when capped at 6: {:.2f}; per finding: {:.3f}; sorted: {}".format(
            statistics.mean(min(x, 6) for x in v), sum(v) / tot("hm_findings"), sorted(v)))
    print("\n| Count per audit | Min | First quartile | Median | Third quartile | Max | Mean | Total |")
    print("|---|---|---|---|---|---|---|---|")
    for label, k in (("Strict N", "strict_n"), ("Strict N without the assembly rule", "strict_n_without_assembly_rule"),
                     ("Original N", "original_n"), ("Eligible functions", "eligible_functions")):
        v = [a[k] for a in out]
        print("| {} | {} | {:g} | {:g} | {:g} | {} | {:.1f} | {} |".format(label, *quart(v), sum(v)))
    groups = [(s, ids) for (s, _), ids in by_old.items() if len(ids) > 1]
    kinds = Counter()
    for s, ids in groups:
        paths = {i.split("::", 1)[0] for i in ids}
        conts = {i.split("::", 1)[1].split(".")[0] for i in ids}
        kinds["same file name in different folders" if len(paths) > 1 else
              "same name in different contracts of one file" if len(conts) > 1 else "overloads in one contract"] += 1
    print("\nname collisions:", len(groups), "functions in them:", sum(len(i) for _, i in groups), dict(kinds))
    elig_groups = [ids for s, ids in groups if sum(r["eligible"] for r in fns if r["slug"] == s
                                                     and r["identity"] in ids) > 1]
    print("collisions with 2+ eligible functions:", len(elig_groups))
    print("linked names that collide:", len(ROOT_RESOLVE))
    rows = [f for f in findings if (f["slug"], f["finding_id"]) in reread]
    for ev in ("observed fix", "from recommendation"):
        sub = [f for f in rows if f["fix_evidence"] == ev]
        why = Counter(w for f in sub for w in f["why_not"])
        print("\n{}: one-body findings {}, strict {}, excluded {}".format(
            ev, len(sub), sum(bool(f["strict"]) for f in sub), sum(not f["strict"] for f in sub)))
        for w, n in why.most_common():
            print("  {}: {}  [{}]".format(w, n, ", ".join(f["finding_id"] for f in sub if w in f["why_not"])))
        only = Counter(f["why_not"][0] for f in sub if len(f["why_not"]) == 1)
        print("  excluded for one reason only:", dict(only))
    nr = [a["findings_fix_not_read"] for a in out]
    print("\nfindings with no fix read: {} (sponsor status fixed: {})".format(
        sum(nr), sum(a["findings_fix_not_read_fixed_status"] for a in out)))
    print("\nstrict V observed:", [a["strict_v_observed"] for a in out])
    print("strict V upper bound:", [a["strict_v_upper_bound"] for a in out])
    print("strict N:", [a["strict_n"] for a in out])
    print("collisions resolved:", [a["name_collisions"] for a in out])


if __name__ == "__main__":
    sys.exit(main())
