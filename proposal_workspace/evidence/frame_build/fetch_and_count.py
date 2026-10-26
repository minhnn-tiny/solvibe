#!/usr/bin/env python3
"""Step 2 of the frame build (network, read-only): fetch the Solidity files of each audit's linked repositories and
count eligible functions, the first-stage size measure of the development and main draws (proposal section 5.1).

Usage (from the repository root):
  python3.12 -I proposal_workspace/evidence/frame_build/fetch_and_count.py --clones <empty folder> [--jobs 8]
For every audit in frame_list.csv with a linked repository, and for each of its listed "owner/repo@ref" entries:
- a new empty folder; `git init`; `git fetch --depth 1 --filter=blob:none https://github.com/owner/repo <ref>` (no
  credentials, GIT_TERMINAL_PROMPT=0, so a private repository fails instead of prompting); a sparse checkout of *.sol
  files only. If the ref cannot be fetched, the default branch is used and this is recorded. Nothing in a clone is run.
- scope: the Code4rena `scope.txt` when present; otherwise the files listed in the README's scope section ("Audit
  scope" in Sherlock repositories, "Scope" or "Files in scope" in Code4rena repositories, up to any "out of scope"
  heading); otherwise every .sol file except test, mock, script, library and
  dependency folders (test, tests, mock, mocks, script, scripts, lib, node_modules, forge-std, dependencies, certora,
  echidna, out, cache) and files ending in .t.sol or .s.sol. This automated scope is a size measure only; sampled
  protocols get the exact scope by hand (proposal section 8).
- if one of an audit's repositories has an explicit scope (scope.txt or README), repositories without one are ignored.
- eligible functions: the counting rule of ../frame_audit/count_functions.py, imported unchanged.
Writes next to this script: frame_counts.csv (one row per audit: status, repositories used, ref used, scope source,
files, functions with a body, eligible functions, parse failures) and protocol_frame.csv (protocol_id, n_eligible) for
audits with at least one eligible function, the input of dev_case/draw_protocols.py.
"""
import argparse, csv, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parent / "frame_audit"))
from count_functions import count

SKIP = re.compile(r"(^|/)(test|tests|mock|mocks|script|scripts|lib|node_modules|forge-std|dependencies|certora|echidna|out|cache)/|\.t\.sol$|\.s\.sol$", re.I)
ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="/usr/bin/false")


def git(args, cwd, timeout=600):
    return subprocess.run(["git", "-c", "advice.detachedHead=false", "-c", "core.hooksPath=/dev/null"] + args, cwd=cwd, env=ENV,
                          capture_output=True, text=True, timeout=timeout)


def readme_scope(text):
    """.sol paths listed in a README scope section ("Audit scope", "Scope" or "Files in scope"), stopping at an
    "out of scope" heading or the next top-level heading. Handles relative links, GitHub blob links and backticked paths."""
    m = re.search(r"^(#+)\s*(audit scope|scope|files in scope)\b[^\n]*$(.*?)(?=^#+\s*[^\n]*out of scope|^#\s|\Z)", text, re.M | re.S | re.I)
    if not m:
        return []
    paths = []
    for p in re.findall(r"([\w\-./@]+\.sol)\b", m.group(3)):
        if "/blob/" in p:
            p = p.split("/blob/", 1)[1].split("/", 1)[-1]
        p = p.lstrip("./")
        if p not in paths:
            paths.append(p)
    return paths


def fetch(owner, repo, ref, dest):
    dest.mkdir(parents=True)
    git(["init", "-q"], dest)
    git(["remote", "add", "origin", f"https://github.com/{owner}/{repo}.git"], dest)
    git(["sparse-checkout", "set", "--no-cone", "*.sol"], dest)
    used = ref
    r = git(["fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", ref], dest)
    if r.returncode != 0:
        used = "default branch"
        r = git(["fetch", "-q", "--depth", "1", "--filter=blob:none", "origin", "HEAD"], dest)
        if r.returncode != 0:
            return None, (r.stderr.strip().splitlines() or ["fetch failed"])[-1][:160]
    r = git(["checkout", "-q", "FETCH_HEAD"], dest)
    if r.returncode != 0:
        return None, (r.stderr.strip().splitlines() or ["checkout failed"])[-1][:160]
    return used, None


def one(row, clones):
    out = dict(audit_key=row["audit_key"], slug=row["slug"], firm=row["firm"], year=row["year"], status="", repos="", refs_used="",
               scope_source="", files=0, functions=0, eligible=0, parse_failures=0, note="")
    entries = row["repos"].split()
    if not entries:
        out["status"] = "no linked repository"
        return out
    total_rows, notes, refs, sources, nfiles, nfail, per_repo = [], [], [], [], 0, 0, []
    for i, e in enumerate(entries):
        owner_repo, ref = e.rsplit("@", 1)
        owner, repo = owner_repo.split("/", 1)
        dest = Path(clones) / f"{row['slug']}-{i}"
        try:
            used, err = fetch(owner, repo, ref, dest)
        except subprocess.TimeoutExpired:
            used, err = None, "timeout"
        if err:
            notes.append(f"{owner_repo}: {err}")
            continue
        refs.append(f"{owner_repo}@{used}")
        sol = [str(p.relative_to(dest)) for p in dest.rglob("*.sol") if ".git/" not in str(p)]
        scope_file, readme = dest / "scope.txt", dest / "README.md"
        git(["sparse-checkout", "add", "scope.txt", "README.md"], dest)
        listed_readme = readme_scope(readme.read_text(errors="replace")) if readme.exists() else []
        if scope_file.exists():
            listed = [ln.strip().lstrip("./") for ln in scope_file.read_text(errors="replace").splitlines() if ln.strip().endswith(".sol")]
            scope = [p for p in listed if (dest / p).is_file()]
            sources.append("scope.txt")
        elif [p for p in listed_readme if (dest / p).is_file()]:
            scope = [p for p in listed_readme if (dest / p).is_file()]
            sources.append("README scope")
        else:
            scope = [p for p in sol if not SKIP.search(p)]
            sources.append("automatic")
        per_repo.append((sources[-1], dest, scope))
    if any(src != "automatic" for src, _, _ in per_repo):          # an explicit scope in one repository: drop automatic ones
        dropped = sum(src == "automatic" for src, _, _ in per_repo)
        per_repo = [x for x in per_repo if x[0] != "automatic"]
        sources = [x[0] for x in per_repo]
        if dropped:
            notes.append(f"{dropped} repository without an explicit scope ignored")
    for src, dest, scope in per_repo:
        rows, failures = count(dest, scope)
        total_rows += rows; nfiles += len(scope); nfail += len(failures)
    out.update(repos=" ".join(entries), refs_used=" ".join(refs), scope_source="+".join(sources), files=nfiles,
               functions=len(total_rows), eligible=sum(r["eligible"] for r in total_rows), parse_failures=nfail, note="; ".join(notes))
    out["status"] = "counted" if refs and out["eligible"] > 0 else ("no eligible function in scope" if refs else "repository not accessible")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clones", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    Path(a.clones).mkdir(parents=True, exist_ok=True)
    assert not any(Path(a.clones).iterdir()), "--clones must be an empty folder"
    rows = list(csv.DictReader(open(HERE / "frame_list.csv")))
    with ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda r: one(r, a.clones), rows))
    fields = list(res[0])
    with open(HERE / "frame_counts.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(res)
    counted = [r for r in res if r["status"] == "counted"]
    with open(HERE / "protocol_frame.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["protocol_id", "n_eligible"])
        for r in counted:
            w.writerow([r["slug"], r["eligible"]])
    from collections import Counter
    print("status:", dict(Counter(r["status"] for r in res)))
    print("counted audits:", len(counted), "| eligible functions: total", sum(r["eligible"] for r in counted),
          "| scope.txt used:", sum("scope.txt" in r["scope_source"] for r in counted), "| README scope used:", sum("README" in r["scope_source"] for r in counted))


if __name__ == "__main__":
    main()
