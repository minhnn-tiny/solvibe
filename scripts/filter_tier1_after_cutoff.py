#!/usr/bin/env python3
"""Copy tier_1 findings reported after the GPT-5.4 / GPT-5.4 mini cutoff (2025-08-31) into one flat dir,
and write a master CSV with one row per tier_1 finding (selected and excluded) for analysis.

The downloaded findings have an empty `report_date` ({}), so the date comes from the finding's links:
contest repo / report / PDF names such as `code-423n4/2025-10-...`, `security-review_2025-11-03.md`,
`...-Review-November-2025.pdf`. A finding is kept only if its latest linked month is >= 2025-09
(month granularity is exact here because the cutoff is the last day of a month).
Findings without any date in their links are excluded.

"Sufficient information" = the tier_1 artifact is a complete, well-formed contract (pragma, contract,
function, balanced braces), has extracted problem code, and the LLM validation found the report
consistent with the code. The finding's markdown report is copied alongside.

Usage: python3 scripts/filter_tier1_after_cutoff.py [--min-month 2025-09] [--out data_collection/tier1_after_2025-08-31]
                                                     [--master data_collection/tier1_master.csv]
"""
import argparse, csv, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data_collection"
LINK_FIELDS = ("contest_link", "github_link", "source_link", "pdf_link")
MONTHS = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
NUMERIC = re.compile(r"(?<!\d)(20[12]\d)[-_/](0?[1-9]|1[0-2])(?!\d)")  # 2025-09, 2023-8, 2025_11
NAMED = re.compile(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[-_ ]?(?:%20)?(20[12]\d)(?!\d)", re.I)
CHECKS = ("is_complete", "has_pragma", "has_contract", "has_function", "balanced_braces")
SOURCE_URL = re.compile(r"https://github\.com/([^/]+/[^/]+)/blob/([^/]+)/")


def linked_month(finding):
    """(year*100+month, link) for the latest month mentioned in the finding's links, or (None, "")."""
    best = (None, "")
    for link in (str(finding.get(k) or "") for k in LINK_FIELDS):
        found = [int(y) * 100 + int(m) for y, m in NUMERIC.findall(link)]
        found += [int(y) * 100 + MONTHS[m[:3].lower()] for m, y in NAMED.findall(link)]
        if found and (best[0] is None or max(found) > best[0]):
            best = (max(found), link)
    return best


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
    ap.add_argument("--min-month", default="2025-09")
    ap.add_argument("--out", default=str(ROOT / "tier1_after_2025-08-31"))
    ap.add_argument("--master", default=str(ROOT / "tier1_master.csv"))
    a = ap.parse_args()
    min_month = int(a.min_month.replace("-", ""))
    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    findings, md, rank = {}, {}, {}
    for batch in sorted((ROOT / "downloaded_findings").glob("batch_*_solodit_findings.json")):
        data = json.loads(batch.read_text())
        for f in data if isinstance(data, list) else data["findings"]:
            fid = str(f["id"])
            findings[fid], md[fid] = f, batch.with_suffix("") / f"{fid}.md"
            rank[fid] = len(rank) + 1  # download order, roughly newest first

    rows, manifest = [], []
    for meta_path in sorted(ROOT.glob("batch_*_extracted_contracts/tier_1_complete/*.json")):
        meta = json.loads(meta_path.read_text())
        fid = str(meta["id"])
        f = findings.get(fid, {})
        month, date_link = linked_month(f)
        failed = failed_checks(meta)
        reason = "insufficient" if failed else "undated" if month is None else "before_cutoff" if month < min_month else ""
        month_str = f"{month // 100}-{month % 100:02d}" if month else ""
        v = meta.get("validation") or {}
        scsvs, mando = v.get("scsvs_classification") or {}, v.get("mando_classification") or {}
        src = SOURCE_URL.match(meta.get("source_url") or "")
        rows.append(dict(
            id=fid, batch=meta_path.parts[-3].removesuffix("_extracted_contracts"),
            status="excluded" if reason else "selected", exclusion_reason=reason, failed_checks=";".join(failed),
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
        manifest.append(dict(id=fid, linked_month=month_str, firm=f["firm_name"], protocol=f["protocol_name"],
                             impact=f["impact"], title=f["title"], links=[f[k] for k in LINK_FIELDS if f.get(k)],
                             files=[sol.name]))

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    rows.sort(key=lambda r: (r["status"] != "selected", r["exclusion_reason"], r["linked_month"] or "0", int(r["id"])))
    with open(a.master, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    counts = {}
    for r in rows:
        k = r["exclusion_reason"] or "selected"
        counts[k] = counts.get(k, 0) + 1
    print(json.dumps(dict(tier1_findings=len(rows), **counts, master=a.master), indent=2))


if __name__ == "__main__":
    main()
