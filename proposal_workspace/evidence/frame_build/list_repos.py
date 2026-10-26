#!/usr/bin/env python3
"""Step 1 of the frame build (no network): list the 2024 and 2025 Code4rena, Sherlock and Cantina audits with Solidity
code from the per-protocol inventory, and, for each, the GitHub repositories and refs that its findings link to.

Usage (from the repository root): python3 -I proposal_workspace/evidence/frame_build/list_repos.py
Reads: proposal_workspace/evidence/frame_inventory/per_protocol_audit.csv and data_collection/downloaded_findings/.
Writes: frame_list.csv next to this script. One row per audit: audit_key, slug, firm, protocol, year, hm_findings, and
`repos`: up to three "owner/repo@ref" entries, each holding at least 25% of the audit's .sol links (most linked first).
Pilot protocols stay in the frame (proposal section 8: exposure changes who does the work, not which protocols are in it).
"""
import collections, csv, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent / "frame_inventory"))
sys.path.insert(0, str(HERE.parent / "frame_audit"))
from frame_inventory import audit_key, LINK  # same audit grouping and link pattern as the inventory
from draw_sample import slug

FIRMS = {"Code4rena", "Sherlock", "Cantina"}


def main():
    rows = [r for r in csv.DictReader(open(HERE.parent / "frame_inventory" / "per_protocol_audit.csv"))
            if r["firm"] in FIRMS and r["year"] in ("2024", "2025") and r["solidity_signal"] == "True"]
    keys = {r["audit_key"] for r in rows}
    links = collections.defaultdict(collections.Counter)
    for p in sorted((ROOT / "data_collection" / "downloaded_findings").glob("batch_*_solodit_findings.json")):
        for f in json.loads(p.read_text()):
            k = audit_key(f)
            if k in keys:
                for m in LINK.finditer(f.get("content") or ""):
                    owner, repo, ref = m.group(1), m.group(2), m.group(3)
                    links[k][(owner, repo, ref)] += 1
    with open(HERE / "frame_list.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["audit_key", "slug", "firm", "protocol", "year", "hm_findings", "repos"])
        for r in sorted(rows, key=lambda r: r["audit_key"]):
            c = links[r["audit_key"]]
            total = sum(c.values())
            by_repo = collections.Counter()
            for (o, rp, ref), n in c.items():
                by_repo[(o, rp)] += n
            chosen = []
            for (o, rp), n in by_repo.most_common(3):
                if total and n / total >= 0.25:
                    ref = max(((rf, m) for (oo, rr, rf), m in c.items() if (oo, rr) == (o, rp)), key=lambda x: x[1])[0]
                    chosen.append(f"{o}/{rp}@{ref}")
            w.writerow([r["audit_key"], slug(r["audit_key"]), r["firm"], r["protocol"], r["year"], r["hm_findings"], " ".join(chosen)])
    n_with = sum(1 for _ in csv.DictReader(open(HERE / "frame_list.csv")) if _["repos"])
    print(f"audits in the 2024-2025 frame: {len(rows)}; with at least one linked repository: {n_with}")


if __name__ == "__main__":
    main()
