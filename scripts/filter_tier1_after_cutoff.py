#!/usr/bin/env python3
"""Copy tier_1 findings dated inside a range (default: after the GPT-5.4 / GPT-5.4 mini cutoff 2025-08-31)
into one flat dir, and write a master CSV with one row per tier_1 finding (selected and excluded) for analysis.

Findings come from every batch: batches 1-4 (Solodit API) and batch 5 (firm reports, split_firm_reports.py).
The date of a finding, in this order:
1. batch 5: `report_date`, from the report file name (Code4rena: the contest month in the report URL);
2. Solodit findings have an empty `report_date` ({}), so the latest month named in their links: contest repo /
   report / PDF names such as `code-423n4/2025-10-...`, `security-review_2025-11-03.md`, `...-November-2025.pdf`;
3. links without a date: data_collection/undated_finding_dates.csv (date_undated_findings.py).
Month-only dates are compared on the month; ranges start on the first of a month, so this is exact.
Findings without any date are excluded.

"Sufficient information" = the tier_1 artifact is a complete, well-formed contract (pragma, contract,
function, balanced braces), has extracted problem code, and the validation (OpenAI for batches 1-4, a Claude
review for batch 5) found the report consistent with the code. The finding's markdown report is copied alongside.

Usage: python3 scripts/filter_tier1_after_cutoff.py [--start 2025-09-01] [--end 9999-12-31]
           [--out data_collection/tier1_after_2025-08-31] [--master data_collection/tier1_master.csv]
           [--lower data_collection/lower_tier.csv]   # also list tier 2/3 findings in the range
"""
import argparse, csv, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data_collection"
LINK_FIELDS = ("contest_link", "github_link", "source_link", "pdf_link")
MONTHS = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
NUMERIC = re.compile(r"(?<!\d)(20[12]\d)[-_/](0?[1-9]|1[0-2])(?!\d)")  # 2025-09, 2023-8, 2025_11
NAMED = re.compile(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[-_ ]?(?:%20)?(20[12]\d)(?!\d)", re.I)
CHECKS = ("is_complete", "has_pragma", "has_contract", "has_function", "balanced_braces")
SOURCE_URL = re.compile(r"https://github\.com/([^/]+/[^/]+)/(?:blob|tree)/([^/]+)/")


def linked_month(finding):
    """(year*100+month, link) for the latest month mentioned in the finding's links, or (None, "")."""
    best = (None, "")
    for link in (str(finding.get(k) or "") for k in LINK_FIELDS):
        found = [int(y) * 100 + int(m) for y, m in NUMERIC.findall(link)]
        found += [int(y) * 100 + MONTHS[m[:3].lower()] for m, y in NAMED.findall(link)]
        if found and (best[0] is None or max(found) > best[0]):
            best = (max(found), link)
    return best


def finding_date(finding, extra):
    """(date 'YYYY-MM' or 'YYYY-MM-DD', where it came from) or (None, ''). extra: id -> date for undated links."""
    if isinstance(finding.get("report_date"), str) and finding["report_date"]:
        how = "contest month in report URL" if finding.get("source") == "code4rena" else "report file name"
        return finding["report_date"], how
    month, _ = linked_month(finding)
    if month:
        return f"{month // 100}-{month % 100:02d}", "month in link"
    if extra.get(str(finding["id"])):
        return extra[str(finding["id"])], "first publication of the report"
    return None, ""


def in_range(date, start, end):
    return start[:len(date)] <= date <= end  # a month-only date is compared on the month


def failed_checks(meta):
    """Names of the sufficiency checks this tier_1 artifact fails (empty = sufficient)."""
    failed = [k for k in CHECKS if meta.get(k) is not True]
    if (meta.get("problem_code") or {}).get("has_problem_code") is not True:
        failed.append("has_problem_code")
    if ((meta.get("validation") or {}).get("content_code_consistency") or {}).get("consistent") is not True:
        failed.append("consistent")
    return failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2025-09-01")
    ap.add_argument("--end", default="9999-12-31")
    ap.add_argument("--out", default=str(ROOT / "tier1_after_2025-08-31"))
    ap.add_argument("--master", default=str(ROOT / "tier1_master.csv"))
    ap.add_argument("--lower", help="also write a CSV of the tier 2/3 findings in the range, kept for later review")
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    findings, md, rank = {}, {}, {}
    for batch in sorted((ROOT / "downloaded_findings").glob("batch_*_findings.json")):  # Solodit + firm reports
        data = json.loads(batch.read_text())
        for f in data if isinstance(data, list) else data["findings"]:
            fid = str(f["id"])
            findings[fid], md[fid] = f, batch.with_suffix("") / f"{fid}.md"
            rank[fid] = len(rank) + 1  # download order, roughly newest first
    dates_csv = ROOT / "undated_finding_dates.csv"
    extra = {r["id"]: r["date"] for r in csv.DictReader(open(dates_csv))} if dates_csv.exists() else {}

    rows, manifest, lower = [], [], []
    for meta_path in sorted(ROOT.glob("batch_*_extracted_contracts/tier_*/*.json")):
        meta = json.loads(meta_path.read_text())
        fid = str(meta["id"])
        f = findings.get(fid, {})
        date, date_source = finding_date(f, extra) if f else (None, "")
        out_of_range = ("undated" if date is None else "" if in_range(date, a.start, a.end)
                        else "before_cutoff" if date < a.start[:len(date)] else "after_end")
        batch = meta_path.parts[-3].removesuffix("_extracted_contracts")
        if meta_path.parent.name != "tier_1_complete":
            if not out_of_range:
                lower.append(dict(id=fid, batch=batch, tier=meta.get("tier", ""), date=date, date_source=date_source,
                                  firm=f.get("firm_name", ""), protocol=f.get("protocol_name", ""),
                                  impact=f.get("impact", ""), title=f.get("title") or meta.get("vulnerability_title", ""),
                                  num_lines=meta.get("num_lines", ""),
                                  has_problem_code=(meta.get("problem_code") or {}).get("has_problem_code"),
                                  sol_file=str(meta_path.with_suffix(".sol").relative_to(ROOT)),
                                  report_md=str(md[fid].relative_to(ROOT)) if fid in md else ""))
            continue
        month, date_link = linked_month(f)
        failed = failed_checks(meta)
        reason = "insufficient" if failed else out_of_range
        month_str = f"{month // 100}-{month % 100:02d}" if month else ""
        v = meta.get("validation") or {}
        scsvs, mando = v.get("scsvs_classification") or {}, v.get("mando_classification") or {}
        src = SOURCE_URL.match(meta.get("source_url") or "")
        rows.append(dict(
            id=fid, batch=batch,
            status="excluded" if reason else "selected", exclusion_reason=reason, failed_checks=";".join(failed),
            date=date or "", date_source=date_source,
            linked_month=month_str, date_source_link=date_link, download_rank=rank.get(fid, ""),
            firm=f.get("firm_name", ""), protocol=f.get("protocol_name", ""), impact=f.get("impact", ""),
            title=f.get("title") or meta.get("vulnerability_title", ""), sol_file=meta_path.with_suffix(".sol").name,
            num_lines=meta.get("num_lines", ""), source_repo=src[1] if src else "", source_ref=src[2] if src else "",
            source_url=meta.get("source_url", ""),
            has_recommendation=(meta.get("recommendation") or {}).get("has_recommendation"),
            has_poc=(meta.get("poc") or {}).get("has_poc"), fix_code_source=v.get("fix_code_source", ""),
            scsvs=scsvs.get("primary_category", ""), scsvs_name=scsvs.get("primary_category_name", ""),
            mando=mando.get("primary_category", ""), mando_applicable=mando.get("mando_applicable", ""),
            consistency_confidence=(v.get("content_code_consistency") or {}).get("confidence", ""),
            validator_model=v.get("model", "")))
        if reason:
            continue
        sol = meta_path.with_suffix(".sol")
        assert not (out / sol.name).exists(), f"filename clash: {sol.name}"
        shutil.copy2(sol, out / sol.name)
        shutil.copy2(meta_path, out / meta_path.name)
        if md[fid].exists():
            shutil.copy2(md[fid], out / md[fid].name)
        manifest.append(dict(id=fid, date=date, linked_month=month_str, firm=f["firm_name"], protocol=f["protocol_name"],
                             impact=f["impact"], title=f["title"], links=[f[k] for k in LINK_FIELDS if f.get(k)],
                             files=[sol.name]))

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    by_id = lambda r: (r["id"].isdigit(), int(r["id"]) if r["id"].isdigit() else r["id"])  # Solodit ids are numbers
    rows.sort(key=lambda r: (r["status"] != "selected", r["exclusion_reason"], r["date"] or "0", by_id(r)))
    lower.sort(key=lambda r: (r["date"], by_id(r)))
    for path, table in ((a.master, rows), (a.lower, lower)):
        if path and table:
            with open(path, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=list(table[0]))
                w.writeheader()
                w.writerows(table)

    counts = {}
    for r in rows:
        k = r["exclusion_reason"] or "selected"
        counts[k] = counts.get(k, 0) + 1
    print(json.dumps(dict(tier1_findings=len(rows), **counts, master=a.master,
                          lower_tier_in_range=len(lower) if a.lower else None), indent=2))


if __name__ == "__main__":
    main()
