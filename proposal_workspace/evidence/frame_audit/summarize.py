#!/usr/bin/env python3
"""Merge the per-audit work files into the two deliverable CSVs and print the README tables.
Standard library only. Uses no network.

Reads, for each processed audit, <work>/<slug>/findings_classified.csv, audit_meta.csv, functions.csv,
scope.txt and findings.md. Writes per_audit.csv, per_finding.csv, functions_in_scope.csv and scope_files.csv
next to this script. Needs Python 3.8 or later.
Usage:
    python3 -I proposal_workspace/evidence/frame_audit/summarize.py --work <folder>
"""
import argparse, csv, re, statistics
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = 25
CLASSES = {"one function body", "several function bodies", "signature, storage or new declaration", "undetermined"}
EVIDENCE = {"observed fix", "from recommendation", "none"}
# Audits drawn but not processed, in draw order, with the reason. Each was replaced by the next audit in the order.
REPLACED = {
    "cantina-berachain_clique_january2025": "Private Cantina review. The report names the repository "
        "(clique-bera-contracts) but not its owner. No public copy was found; the one guessed location needs a login.",
    "cantina-eggs_february2025": "Private Cantina review. The report names the repository (eggs) but not its owner. "
        "No public copy was found.",
    "cantina-optimism_february2025": "Private Cantina review of the optimism monorepo at one commit. The report does "
        "not say which part of the monorepo was reviewed, so the scope cannot be identified.",
    "sherlock-1140": "Ethereum client code (Go, Rust, TypeScript), not Solidity. Outside the frame.",
    "sherlock-1073": "The Sherlock contest repository needs a login. The findings link no public sponsor repository.",
    "sherlock-1176": "The Sherlock contest repository needs a login. The public sponsor repository is a large "
        "monorepo, and the scope list (which packages and files) is not public.",
    "cantina-honeyjar_february2025": "Private Cantina review. A public repository with the same name exists, but "
        "neither the reviewed commit nor the fix commits are in it.",
    "cantina-pinto_february2025": "Private Cantina review. The public repository's history starts after the review, "
        "so the reviewed commit is not in it.",
}

# Merge-time corrections that make one rule hold across all audits: a fix that edits a function's header
# (adds a modifier, changes a base-constructor argument) is not a body change. Other sessions already
# classed such fixes this way (TermMax 54905, Kinetiq 58557, Blackhole 58342).
OVERRIDES = {
    ("code4rena-526", "63709"): "The recommendation adds a modifier to the header, so it is not a body change.",
    ("code4rena-487", "50064"): "The recommendation changes a base-constructor argument in the header, so it is "
                                "not a body change.",
}


def read_csv(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def dist(values, top=6):
    c = Counter(min(v, top) for v in values)
    return [c.get(i, 0) for i in range(top + 1)]


def quart(values):
    q = statistics.quantiles(values, n=4, method="inclusive")
    return min(values), q[0], statistics.median(values), q[2], max(values), statistics.mean(values)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    work = Path(ap.parse_args().work)
    order = read_csv(HERE / "sample_order.csv")
    inv = {r["audit_key"]: r for r in read_csv(HERE.parent / "frame_inventory" / "per_protocol_audit.csv")}
    audits, findings, fn_rows, scope_rows, done = [], [], [], [], 0
    for o in order:
        if done == TARGET:
            break
        slug, base = o["slug"], {k: o[k] for k in ("rank", "slug", "audit_key", "firm", "protocol", "year_month")}
        if slug in REPLACED:
            audits.append(dict(base, status="replaced", reason=REPLACED[slug], hm_findings=o["hm_findings"]))
            continue
        d = work / slug
        rows = read_csv(d / "findings_classified.csv")
        meta = read_csv(d / "audit_meta.csv")[0]
        fns = read_csv(d / "functions.csv")
        ids = re.findall(r"^========== FINDING (\S+) \|", (d / "findings.md").read_text(), re.M)
        for r in rows:
            why = OVERRIDES.get((slug, r["finding_id"]))
            if why:
                r.update(fix_class="signature, storage or new declaration", v_function="",
                         note=r["note"] + " Reclassified at merge: " + why)
        got = [r["finding_id"] for r in rows]
        assert sorted(got) == sorted(ids), (slug, set(ids) ^ set(got))
        for r in rows:
            assert r["fix_class"] in CLASSES and r["fix_evidence"] in EVIDENCE, (slug, r["finding_id"])
            assert (r["fix_class"] == "one function body") == bool(r["v_function"].strip()), (slug, r["finding_id"])
            assert (r["fix_class"] == "undetermined") == (r["fix_evidence"] == "none"), (slug, r["finding_id"])
        keys = lambda r: [k.strip() for k in r["root_cause_functions"].split(";") if "::" in k]  # noqa: E731
        mapped = [r for r in rows if keys(r)]
        root = {k for r in mapped for k in keys(r)}
        v_obs = {r["v_function"].strip() for r in rows if r["fix_evidence"] == "observed fix" and r["v_function"]}
        v_all = {r["v_function"].strip() for r in rows if r["v_function"]}
        eligible = [f for f in fns if f["eligible"] == "True"]
        eligible_keys = {f["function"] for f in eligible}
        linked = (root | v_all) & eligible_keys
        cls = Counter(r["fix_class"] for r in rows)
        audits.append(dict(
            base, status="processed", reason="", hm_findings=len(rows), repo_url=meta["repo_url"],
            commit=meta["commit"], scope_source=meta["scope_source"], scope_files=meta["scope_files"],
            mapped_findings=len(mapped), distinct_root_cause_functions=len(root),
            v_functions_observed=len(v_obs), v_functions_incl_recommendation=len(v_all),
            v_functions_not_eligible_in_scope=len(v_all - eligible_keys),
            findings_one_body_observed=sum(r["fix_class"] == "one function body" and r["fix_evidence"] ==
                                           "observed fix" for r in rows),
            findings_one_body_recommendation=sum(r["fix_class"] == "one function body" and r["fix_evidence"] ==
                                                 "from recommendation" for r in rows),
            findings_several_bodies=cls["several function bodies"],
            findings_signature_storage_declaration=cls["signature, storage or new declaration"],
            findings_undetermined=cls["undetermined"],
            findings_with_observed_fix=sum(r["fix_evidence"] == "observed fix" for r in rows),
            functions_with_body=len(fns), eligible_functions=len(eligible), v_linked_eligible=len(linked),
            n_functions=len(eligible) - len(linked), parse_failures=meta["parse_failures"],
            modelled_linked_functions=inv[o["audit_key"]]["distinct_functions"]))
        for r in rows:  # one sponsor repo sits under a personal account; name it by role, not by owner
            r["fix_reference"] = r["fix_reference"].replace(
                "https://github.com/Skyewwww/omni-chain-contracts", "DODO sponsor repo (linked in the findings)")
            findings.append(dict(rank=o["rank"], **r))
        for f in fns:
            fn_rows.append(dict(slug=slug, **f))
        for ln in open(d / "scope.txt"):
            if ln.strip() and not ln.startswith("#"):
                scope_rows.append({"slug": slug, "repo_url": meta["repo_url"], "commit": meta["commit"],
                                   "path": ln.strip()})
        done += 1

    cols = list(audits[-1])
    with open(HERE / "per_audit.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, restval="")
        w.writeheader()
        w.writerows(audits)
    for name, rows in (("per_finding.csv", findings), ("functions_in_scope.csv", fn_rows),
                       ("scope_files.csv", scope_rows)):
        with open(HERE / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    p = [a for a in audits if a["status"] == "processed"]
    print("drawn: {}  processed: {}  replaced: {}".format(len(audits), len(p), len(audits) - len(p)))
    vo = [a["v_functions_observed"] for a in p]
    va = [a["v_functions_incl_recommendation"] for a in p]
    n = [a["n_functions"] for a in p]
    print("\n| V count | 0 | 1 | 2 | 3 | 4 | 5 | 6+ | Mean | Median | Zero share |\n|---|---|---|---|---|---|---|---|---|---|---|")
    for label, v in (("Observed fixes only", vo), ("Including from recommendation", va)):
        print("| {} | {} | {:.2f} | {} | {}/{} ({:.0%}) |".format(label, " | ".join(map(str, dist(v))),
              statistics.mean(v), statistics.median(v), v.count(0), len(v), v.count(0) / len(v)))
    print("\nUncapped V, sorted (incl. recommendation):", sorted(va))
    print("Mean when capped at 6: observed {:.2f}, incl. recommendation {:.2f}".format(
        statistics.mean(min(x, 6) for x in vo), statistics.mean(min(x, 6) for x in va)))
    nf = sum(a["hm_findings"] for a in p)
    print("V functions per H/M finding: observed {}/{} = {:.3f}, incl. recommendation {}/{} = {:.3f}".format(
        sum(vo), nf, sum(vo) / nf, sum(va), nf, sum(va) / nf))
    blind = [a for a in p if a["findings_with_observed_fix"] == 0]
    print("audits with no fix diff read: {} -> {}; their V incl. rec: {}".format(
        len(blind), [a["slug"] for a in blind], [a["v_functions_incl_recommendation"] for a in blind]))
    seen = [a for a in p if a["findings_with_observed_fix"] > 0]
    print("audits with at least one fix diff read: {}; V observed: {}; mean {:.2f}; zeros {}".format(
        len(seen), [a["v_functions_observed"] for a in seen],
        statistics.mean(a["v_functions_observed"] for a in seen), sum(a["v_functions_observed"] == 0 for a in seen)))
    und = [a["findings_undetermined"] / a["hm_findings"] for a in p]
    print("undetermined share per audit: median {:.2f}, max {:.2f}".format(statistics.median(und), max(und)))
    print("\n| Count | Min | Q1 | Median | Q3 | Max | Mean |\n|---|---|---|---|---|---|---|")
    for label, v in (("Eligible in-scope functions", [a["eligible_functions"] for a in p]), ("N functions", n),
                     ("Functions with a body", [a["functions_with_body"] for a in p])):
        print("| {} | {} | {:g} | {:g} | {:g} | {} | {:.1f} |".format(label, *quart(v)))
    bins = [(0, 49), (50, 99), (100, 199), (200, 399), (400, 10 ** 9)]
    print("\nN bins:", [(lo, hi, sum(lo <= x <= hi for x in n)) for lo, hi in bins])
    tot = Counter(r["fix_class"] for r in findings)
    ev = Counter((r["fix_class"], r["fix_evidence"]) for r in findings)
    print("\nFindings: {}  by class: {}".format(len(findings), dict(tot)))
    print("by class and evidence:", dict(ev))
    for e in ("observed fix", "from recommendation"):
        k = [ev[(c, e)] for c in ("one function body", "several function bodies",
                                  "signature, storage or new declaration")]
        print("  {}: one body {} of {} classified = {:.0%}".format(e, k[0], sum(k), k[0] / sum(k)))
    k = sum(ev[("one function body", e)] for e in ("observed fix", "from recommendation"))
    print("  both: one body {} of {} classified = {:.0%}".format(k, len(findings) - tot["undetermined"],
                                                                 k / (len(findings) - tot["undetermined"])))
    print("undetermined share: {}/{} = {:.1%}".format(tot["undetermined"], len(findings),
                                                       tot["undetermined"] / len(findings)))
    print("mapped findings: {}/{}".format(sum(a["mapped_findings"] for a in p), len(findings)))
    print("sponsor status:", dict(Counter(r["sponsor_status"] for r in findings)))
    print("scope source:", dict(Counter(a["scope_source"] for a in p)))
    print("V functions not eligible or not in scope:", sum(a["v_functions_not_eligible_in_scope"] for a in p))
    print("parse failures:", [(a["slug"], a["parse_failures"]) for a in p if a["parse_failures"] not in ("0", "")])
    print("\n| Rank | Audit | H/M findings | Mapped | Root-cause functions | Findings with fix diff read | "
          "V (observed) | V (incl. recommendation) | Undetermined | Eligible functions | N |")
    print("|" + "---|" * 11)
    for a in p:
        where = a["audit_key"].split(" | ")[1] if a["firm"] != "Cantina" else (
            "competition" if "competition" in a["slug"] else "private review")
        name = {"Audit 507": "Blackhole"}.get(a["protocol"], a["protocol"])  # the inventory has no name for 507
        print("| {} | {} {}, {} ({}) | {} |".format(
            a["rank"], a["firm"], where, name, a["year_month"], " | ".join(str(a[k]) for k in (
                "hm_findings", "mapped_findings", "distinct_root_cause_functions", "findings_with_observed_fix",
                "v_functions_observed", "v_functions_incl_recommendation", "findings_undetermined",
                "eligible_functions", "n_functions"))))
    print("| | **Total** | " + " | ".join("**{}**".format(sum(a[k] for a in p)) for k in (
        "hm_findings", "mapped_findings", "distinct_root_cause_functions", "findings_with_observed_fix",
        "v_functions_observed", "v_functions_incl_recommendation", "findings_undetermined",
        "eligible_functions", "n_functions")) + " |")
    print("\nV list (incl. recommendation):", va)
    print("V list (observed only):", vo)
    print("N list:", n)


if __name__ == "__main__":
    main()
