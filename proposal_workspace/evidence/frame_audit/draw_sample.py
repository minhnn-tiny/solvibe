#!/usr/bin/env python3
"""Draw the random order of 2025+ Code4rena, Sherlock and Cantina audits, and dump each audit's
High and Medium findings to a work folder for reading. Standard library only. Uses no network.

Writes sample_order.csv next to this script. Writes one findings.md per audit under --work
(finder names removed). Usage:
    python3 -I proposal_workspace/evidence/frame_audit/draw_sample.py --work <folder> [--dump N]
"""
import argparse, csv, json, random, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent / "frame_inventory"))
from frame_inventory import audit_key  # same audit grouping as the modelled inventory

SEED = 20261022
FIRMS = {"Code4rena", "Sherlock", "Cantina"}
PILOT = {"Licredity", "Sorella L2 Angstrom", "Ammplify", "Sequence", "Wannabet", "Panoptic", "Ekubo",
         "Merkl", "stETH by EaseDeFi", "YuzuUSD", "Megapot"}


def slug(key):
    firm, rest = key.split(" | ", 1)
    if rest.startswith("contest "):
        return "{}-{}".format(firm.lower(), rest.split()[1])
    return "{}-{}".format(firm.lower(), Path(rest).stem.replace("cantina_", ""))


def eligible():
    rows = csv.DictReader(open(HERE.parent / "frame_inventory" / "per_protocol_audit.csv"))
    keep = [r for r in rows if r["firm"] in FIRMS and r["year"] and int(r["year"]) >= 2025
            and r["protocol"] not in PILOT]
    return sorted(keep, key=lambda r: r["audit_key"])


def scrub(text):
    """Remove finder names: Sherlock 'Found by' blocks and Code4rena 'Submitted by' lines."""
    text = re.sub(r"## Found by\s*\n[^\n]*\n", "## Found by\n[removed]\n", text)
    return re.sub(r"(?im)^.*\b(submitted by|found by|reported by)\b.*$", "[finder line removed]", text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--dump", type=int, default=40, help="dump findings for the first N audits in order")
    a = ap.parse_args()
    el = eligible()
    order = random.Random(SEED).sample(el, len(el))
    with open(HERE / "sample_order.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "audit_key", "slug", "firm", "protocol", "year_month", "hm_findings"])
        for i, r in enumerate(order, 1):
            w.writerow([i, r["audit_key"], slug(r["audit_key"]), r["firm"], r["protocol"], r["month"],
                        r["hm_findings"]])
    print("eligible audits:", len(el))
    wanted = {r["audit_key"]: slug(r["audit_key"]) for r in order[:a.dump]}
    findings = {}
    for p in sorted((ROOT / "data_collection" / "downloaded_findings").glob("batch_*_solodit_findings.json")):
        for f in json.loads(p.read_text()):
            k = audit_key(f)
            if k in wanted:
                findings.setdefault(k, {})[f["id"]] = f  # dedupe by id
    for k, s in wanted.items():
        out = Path(a.work) / s
        out.mkdir(parents=True, exist_ok=True)
        fs = sorted(findings.get(k, {}).values(), key=lambda f: (f["impact"], f["title"]))
        parts = ["# {} ({})\n".format(k, len(fs))]
        for f in fs:
            parts.append("\n\n========== FINDING {} | {} | {}\nlinks: {} {} {}\n\n{}".format(
                f["id"], f["impact"], f["title"], f["github_link"] or "", f["source_link"] or "",
                f["pdf_link"] or "", scrub(f["content"] or "")))
        (out / "findings.md").write_text("".join(parts))
        print(s, len(fs))


if __name__ == "__main__":
    main()
