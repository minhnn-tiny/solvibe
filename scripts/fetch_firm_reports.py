#!/usr/bin/env python3
"""Download audit reports dated in a range straight from the firms' public sources (Solodit API replacement).

Sources: Cyfrin/cyfrin-audit-reports, pashov/audits, trailofbits/publications, sherlock-protocol/sherlock-reports,
solodit/solodit_content (GitHub), and code4rena.com/reports/<contest> pages listed in the Code4rena sitemap.
The date comes from the file name (Code4rena: the contest month in the URL, as filter_tier1_after_cutoff.py does).
When a report exists as both .md and .pdf, only the .md is kept.

Usage: python3 -I scripts/fetch_firm_reports.py [--start 2025-08-01] [--end 2026-10-27]
                                                [--out data_collection/downloaded_findings/batch_5_raw]
Writes <out>/listings/ (raw listings), <out>/<source>/<file> and <out>/reports.json (one entry per report).
"""
import argparse, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GITHUB = {  # source -> (repo, branch, folders to take reports from, firm name as Solodit spells it)
    "cyfrin": ("Cyfrin/cyfrin-audit-reports", "main", ("reports/", "reports_md/"), "Cyfrin"),
    "pashov": ("pashov/audits", "master", ("team/", "agentic/"), "Pashov Audit Group"),
    "trailofbits": ("trailofbits/publications", "master", ("reviews/",), "TrailOfBits"),
    "sherlock": ("sherlock-protocol/sherlock-reports", "main", ("audits/",), "Sherlock"),
    "solodit_content": ("solodit/solodit_content", "main", ("reports/",), None),  # firm = folder name
}
DATE = re.compile(r"(20\d\d)[-_.](0[1-9]|1[0-2])(?:[-_.](0[1-9]|[12]\d|3[01]))?(?!\d)")


def get(url, path=None):
    req = urllib.request.Request(url, headers={"User-Agent": "solvibe-research-crawler"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            if path:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            return data
        except Exception as e:  # network or 5xx: back off; 404 is final
            if getattr(e, "code", None) == 404:
                raise
            print(f"  retry {attempt + 1} {url}: {e}", file=sys.stderr)
            time.sleep(5 * 2 ** attempt)
    sys.exit(f"giving up on {url}")


def file_date(name):
    """'YYYY-MM-DD' or 'YYYY-MM' from a file name, or None."""
    m = DATE.search(name)
    return m and f"{m[1]}-{m[2]}" + (f"-{m[3]}" if m[3] else "")


def in_range(date, start, end):
    return bool(date) and start[:len(date)] <= date <= end  # month-only dates compare on the month


def github_reports(source, start, end, listings):
    repo, branch, folders, firm = GITHUB[source]
    cache = listings / f"tree_{repo.replace('/', '_')}.json"
    tree = json.loads(cache.read_bytes() if cache.exists() else
                      get(f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1", cache))
    assert not tree["truncated"], f"{repo}: tree listing truncated"
    paths = [e["path"] for e in tree["tree"] if e["type"] == "blob" and e["path"].startswith(folders)
             and e["path"].lower().endswith((".md", ".pdf")) and "readme" not in e["path"].lower()]
    md_stems = {Path(p).stem for p in paths if p.endswith(".md")}
    out = []
    for p in paths:
        date = file_date(Path(p).name)
        if not in_range(date, start, end) or (p.endswith(".pdf") and Path(p).stem in md_stems):
            continue
        out.append(dict(source=source, firm=firm or p.split("/")[1], date=date, path=p, format=p.rsplit(".", 1)[1],
                        url=f"https://github.com/{repo}/blob/{branch}/{urllib.parse.quote(p)}",
                        raw_url=f"https://raw.githubusercontent.com/{repo}/{branch}/{urllib.parse.quote(p)}"))
    return out


def code4rena_reports(start, end, listings):
    cache = listings / "code4rena_sitemap.xml"
    xml = (cache.read_bytes() if cache.exists() else get("https://code4rena.com/sitemap.xml", cache)).decode()
    out = []
    for url in sorted(set(re.findall(r"<loc>(https://code4rena\.com/reports/([^<]+))</loc>", xml))):
        date = file_date(url[1])
        if in_range(date and date[:7], start, end):
            out.append(dict(source="code4rena", firm="Code4rena", date=date[:7], path=f"{url[1]}.html", format="html",
                            url=url[0], raw_url=url[0]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2025-08-01")
    ap.add_argument("--end", default="2026-10-27")
    ap.add_argument("--out", default=str(ROOT / "data_collection/downloaded_findings/batch_5_raw"))
    a = ap.parse_args()
    out, listings = Path(a.out), Path(a.out) / "listings"
    reports = code4rena_reports(a.start, a.end, listings)
    for source in GITHUB:
        reports += github_reports(source, a.start, a.end, listings)
    for i, r in enumerate(reports, 1):
        local = out / r["source"] / r["path"]
        r["local_path"] = str(local.relative_to(ROOT))
        if local.exists() and local.stat().st_size:
            continue
        print(f"[{i}/{len(reports)}] {r['url']}", file=sys.stderr)
        get(r["raw_url"], local)
        time.sleep(1.5 if r["source"] == "code4rena" else 0.3)
    (out / "reports.json").write_text(json.dumps(reports, indent=1, ensure_ascii=False))
    counts = {}
    for r in reports:
        counts[f"{r['source']}/{r['format']}"] = counts.get(f"{r['source']}/{r['format']}", 0) + 1
    print(json.dumps(dict(reports=len(reports), **dict(sorted(counts.items())), index=str(out / "reports.json")), indent=1))


if __name__ == "__main__":
    main()
