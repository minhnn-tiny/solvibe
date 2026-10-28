#!/usr/bin/env python3
"""Summarise a tier 1 collection built by filter_tier1_after_cutoff.py into one JSON file for charts and the README.

Reads the master CSV (one row per tier 1 finding), the lower-tier CSV, and batch 5's report and duplicate logs.
Usage: python3 scripts/collection_stats.py [--name 2025-08-01_to_2026-10-27]
Writes data_collection/tier1_<name>/stats.json.
"""
import argparse, collections, csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data_collection"


def rows(path):
    return list(csv.DictReader(open(path, encoding="utf-8"))) if Path(path).exists() else []


def count(items, key):
    return dict(collections.Counter(key(i) for i in items).most_common())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="2025-08-01_to_2026-10-27")
    a = ap.parse_args()
    master, lower = rows(ROOT / f"tier1_master_{a.name}.csv"), rows(ROOT / f"lower_tier_{a.name}.csv")
    reports, dups = rows(ROOT / "batch_5_reports.csv"), rows(ROOT / "batch_5_duplicates.csv")
    extraction = json.loads((ROOT / "batch_5_extracted_contracts/extraction_stats.json").read_text())
    selected = [r for r in master if r["status"] == "selected"]
    in_range = [r for r in master if r["exclusion_reason"] in ("", "insufficient")
                and r["date"] and r["date"] >= a.name[:7] and r["date"] <= a.name[-10:]]
    source = lambda r: "new firm reports (batch 5)" if r["batch"] == "batch_5" else "Solodit download (batches 1-4)"
    stats = dict(
        name=a.name,
        selected=len(selected),
        selected_by_source=count(selected, source),
        selected_by_month=count(sorted(selected, key=lambda r: r["date"]), lambda r: r["date"][:7]),
        selected_by_month_and_source=count(selected, lambda r: f"{r['date'][:7]}|{source(r)}"),
        selected_by_firm=count(selected, lambda r: r["firm"]),
        selected_by_impact=count(selected, lambda r: r["impact"]),
        selected_by_scsvs=count(selected, lambda r: f"{r['scsvs']} {r['scsvs_name']}".strip() or "none"),
        selected_by_mando=count(selected, lambda r: r["mando"] or "none"),
        selected_by_date_source=count(selected, lambda r: r["date_source"]),
        selected_by_validator=count(selected, lambda r: r["validator_model"]),
        tier1_in_range_insufficient=len([r for r in in_range if r["exclusion_reason"] == "insufficient"]),
        insufficient_by_check=count([c for r in in_range for c in r["failed_checks"].split(";") if c], lambda c: c),
        lower_tier=len(lower), lower_tier_by_tier=count(lower, lambda r: r["tier"]),
        lower_tier_by_source=count(lower, source), lower_tier_by_month=count(sorted(lower, key=lambda r: r["date"]),
                                                                              lambda r: r["date"][:7]),
        batch5=dict(
            reports=len(reports), reports_by_source=count(reports, lambda r: f"{r['source']}/{r['format']}"),
            high_medium=sum(int(r["high_medium"]) for r in reports),
            solidity_high_medium=sum(int(r["solidity_high_medium"]) for r in reports),
            reports_with_solidity_findings=sum(int(r["solidity_high_medium"]) > 0 for r in reports),
            duplicates=len(dups), duplicates_by_where=count(dups, lambda r: r["where"]),
            duplicates_by_firm=count(dups, lambda r: r["firm"]),
            extraction=dict(processed=extraction.get("total_processed"), by_tier=extraction.get("by_tier"),
                            failed=extraction.get("failed"), failure_reasons=extraction.get("failure_reasons"))),
    )
    out = ROOT / f"tier1_{a.name}/stats.json"
    out.write_text(json.dumps(stats, indent=1, ensure_ascii=False))
    print(json.dumps({k: stats[k] for k in ("selected", "selected_by_source", "lower_tier")}), "->", out)


if __name__ == "__main__":
    main()
