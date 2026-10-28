#!/usr/bin/env python3
"""Find a publication date for old Solodit findings whose links carry no date (see filter_tier1_after_cutoff.py).

Only findings Solodit added from id 61000 on (mid 2025) are dated; lower ids were added before 2025-08 and
cannot fall in the later date range. The date is when the report first appeared in public:
- GitHub-hosted reports: the first commit that added the report file (or the audit's folder), read from a
  history-only clone, so no GitHub API quota is used.
- blog.openzeppelin.com posts: the page's datePublished.
Quantstamp certificate pages load their content with JavaScript, so those findings stay undated.

Usage: python3 -I scripts/date_undated_findings.py [--min-id 61000]
Writes data_collection/undated_finding_dates.csv (id, firm, report, date, date_source).
"""
import argparse, csv, json, re, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I leaves the script folder off the path
from filter_tier1_after_cutoff import linked_month

ROOT = Path(__file__).resolve().parent.parent
DL = ROOT / "data_collection/downloaded_findings"
CLONES = DL / "batch_5_raw/dating"
FOLDER_REPOS = ("immunefi-team/Past-Audit-Competitions", "mixbytes/audits_public")  # one folder per audit


def report_of(f):
    return re.sub(r"#.*", "", f.get("source_link") or f.get("github_link") or f.get("pdf_link") or f.get("contest_link") or "")


def github_date(repo, path):
    clone = CLONES / repo.replace("/", "_")
    if not clone.exists():
        subprocess.run(["git", "clone", "-q", "--filter=blob:none", "--no-checkout", f"https://github.com/{repo}.git",
                        str(clone)], check=True)
    if repo in FOLDER_REPOS:
        path = path.rsplit("/", 1)[0]
    log = subprocess.run(["git", "-C", str(clone), "log", "--format=%cs", "--", path], capture_output=True, text=True,
                         check=True).stdout.split()
    return min(log) if log else None


def web_date(url):
    if "blog.openzeppelin.com" not in url:
        return None
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    m = re.search(r'"datePublished":"(\d{4}-\d\d-\d\d)', html)
    return m and m[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-id", type=int, default=61000)
    a = ap.parse_args()
    findings = [f for b in sorted(DL.glob("batch_*_solodit_findings.json")) for f in json.loads(b.read_text())]
    undated = [f for f in findings if linked_month(f)[0] is None and int(f["id"]) >= a.min_id]
    dates = {}
    for report in sorted({report_of(f) for f in undated}):
        m = re.match(r"https://github\.com/([^/]+/[^/]+)/blob/[^/]+/(.+)", report)
        if m:
            dates[report] = (github_date(m[1], urllib.parse.unquote(m[2])), "first git commit of the report")
        else:
            dates[report] = (web_date(report), "blog datePublished")
        print(f"{dates[report][0] or 'undated':10} {report[:110]}", file=sys.stderr)
    rows = [dict(id=f["id"], firm=f["firm_name"], report=report_of(f), date=dates[report_of(f)][0] or "",
                 date_source=dates[report_of(f)][1] if dates[report_of(f)][0] else "none found") for f in undated]
    out = ROOT / "data_collection/undated_finding_dates.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(json.dumps(dict(undated=len(rows), dated=sum(bool(r["date"]) for r in rows),
                          in_2025_08_or_later=sum(r["date"] >= "2025-08" for r in rows if r["date"]), out=str(out))))


if __name__ == "__main__":
    main()
