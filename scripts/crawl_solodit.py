#!/usr/bin/env python3
"""Crawl all Solodit findings reported after a cutoff date (default: GPT-5.4 cutoff 2025-08-31).

Usage:  python3 scripts/crawl_solodit.py [--after 2025-08-31] [--out data/solodit_after_2025-08-31.jsonl]
Key:    SOLODIT_API_KEY from env or ./.env
API:    POST https://solodit.cyfrin.io/api/v1/solodit/findings  (20 req/min, pageSize<=100)
"""
import argparse, json, os, sys, time, urllib.error, urllib.request
from pathlib import Path

API = "https://solodit.cyfrin.io/api/v1/solodit/findings"


def load_key():
    if os.environ.get("SOLODIT_API_KEY"):
        return os.environ["SOLODIT_API_KEY"]
    env = Path(__file__).resolve().parent.parent / ".env"
    for line in env.read_text().splitlines() if env.exists() else []:
        k, _, v = line.partition("=")
        if k.strip() == "SOLODIT_API_KEY":
            return v.strip().strip('"\'')
    sys.exit("SOLODIT_API_KEY not set (env or .env)")


def fetch(key, page, after):
    body = {"page": page, "pageSize": 100, "filters": {
        "reported": {"value": "after"}, "reportedAfter": after,
        "sortField": "Recency", "sortDirection": "Asc"}}  # Asc: new findings append at the end, pages stay stable
    req = urllib.request.Request(API, json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "X-Cyfrin-API-Key": key,
                                          "User-Agent": "secure-solvibe-crawler"})
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                rem, reset = r.headers.get("x-ratelimit-remaining"), r.headers.get("x-ratelimit-reset")
                data = json.load(r)
            if rem is not None and int(rem) <= 1 and reset:  # pre-emptively wait for the window to reset
                time.sleep(max(0, int(reset) - time.time()) + 1)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 401:
                sys.exit("401: invalid SOLODIT_API_KEY")
            if e.code == 429 or e.code >= 500:
                reset = e.headers.get("x-ratelimit-reset")
                wait = max(1, int(reset) - time.time() + 1) if reset else 2 ** attempt * 5
                print(f"  HTTP {e.code}, sleeping {wait:.0f}s", file=sys.stderr)
                time.sleep(wait)
                continue
            sys.exit(f"HTTP {e.code}: {e.read()[:300]!r}")
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"  network error {e}, retrying", file=sys.stderr)
            time.sleep(2 ** attempt * 5)
    sys.exit(f"giving up on page {page}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--after", default="2025-08-31")
    ap.add_argument("--out")
    a = ap.parse_args()
    out = Path(a.out or f"data/solodit_after_{a.after}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    key, seen, page, total_pages, dropped = load_key(), set(), 1, 1, 0
    tmp = out.with_suffix(".part")
    with tmp.open("w") as f:
        while page <= total_pages:
            d = fetch(key, page, a.after)
            m = d["metadata"]
            total_pages = m["totalPages"]
            for x in d["findings"]:
                if not (x.get("report_date") or "")[:10] > a.after:  # strict: report_date after cutoff; drops undated
                    dropped += 1
                    continue
                if x["id"] not in seen:
                    seen.add(x["id"])
                    f.write(json.dumps(x, ensure_ascii=False) + "\n")
            print(f"page {page}/{total_pages}  saved={len(seen)}/{m['totalResults']}", file=sys.stderr)
            page += 1
    tmp.replace(out)
    dates = sorted(json.loads(l).get("report_date") or "" for l in out.open())
    dates = [x for x in dates if x]
    print(f"dropped {dropped} findings with report_date <= {a.after} or missing")
    print(f"done: {len(seen)} findings -> {out}  (report_date {dates[0] if dates else '?'} .. {dates[-1] if dates else '?'})")


if __name__ == "__main__":
    main()
