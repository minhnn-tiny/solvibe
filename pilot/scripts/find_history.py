#!/usr/bin/env python3
"""Find the commit that introduced each pilot finding's vulnerable lines (an SZZ-style search with git blame).

For each selected finding:
  1. Take the audited file from the snapshot repository (the Code4rena contest repo, or the project repo itself).
  2. Find the same file content in the project's own history (exact git blob match, else the closest version).
  3. Run `git blame` on the lines the report links to. The commit that last changed most of those lines is the
     candidate bug-introducing commit (VIC); its first parent is the PVIC.
  4. List later commits that touched the file, as fix candidates for manual review.

Writes pilot/tasks/<id>/history.json and pilot/results/history_search.csv.
Usage: python3 pilot/scripts/find_history.py
"""
import csv, json, re, subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPOS, TASKS, RESULTS = ROOT / "pilot/repos", ROOT / "pilot/tasks", ROOT / "pilot/results"
DATASET = ROOT / "data_collection/tier1_after_2025-08-31"

# Code4rena contest repo -> sponsor's public repository (found with GitHub code search, see process log step 3).
SPONSOR = {
    "code-423n4/2025-12-panoptic": "panoptic-labs/panoptic-v2-core",
    "code-423n4/2025-11-megapot": "coordinationlabs/megapot-v2-public",
    "code-423n4/2025-11-merkl": "AngleProtocol/merkl-contracts",
    "code-423n4/2025-10-sequence": "0xsequence/wallet-contracts-v3",
    "code-423n4/2025-11-ekubo": "EkuboProtocol/evm-contracts",
    "code-423n4/2025-10-hybra-finance": None,
    "code-423n4/2025-11-brix-money": None,
    "code-423n4/2025-11-sukukfi": None,
}
# Findings whose tier-1 file is third-party library code, not the audited protocol (dataset report, caveat 2).
LIBRARY_FILE = {"62808", "62812", "62819", "62820", "63336", "63922", "64108", "64400", "65379"}


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[:300]}")
    return r.stdout


def clone(full_name):
    dest = REPOS / full_name.replace("/", "__")
    if not dest.exists():
        subprocess.run(["git", "clone", "-q", f"https://github.com/{full_name}.git", str(dest)], check=True)
    return dest


def find_audited_commit(hist, blob, content, path):
    """Commit in `hist` whose tree holds this exact blob, with its path; else the closest version of the same file name.

    Returns (commit, path in hist, number of changed lines versus the snapshot)."""
    for c in git(hist, "log", "--all", "--format=%H", f"--find-object={blob}").split():
        for line in git(hist, "ls-tree", "-r", c).splitlines():
            if line.split()[2] == blob:
                return c, line.split("\t", 1)[1], 0
    # No exact copy: store the snapshot content in the history repo so git can diff against it.
    subprocess.run(["git", "-C", str(hist), "hash-object", "-w", "--stdin"], input=content, text=True, check=True,
                   capture_output=True)
    name, best = Path(path).name, None
    for c in git(hist, "log", "--all", "--format=%H", "--", f"*{name}").split()[:300]:  # ponytail: 300 newest commits
        for line in git(hist, "ls-tree", "-r", c).splitlines():
            p = line.split("\t", 1)[1]
            if Path(p).name != name:
                continue
            nums = [int(x) for x in git(hist, "diff", "--numstat", f"{c}:{p}", blob, check=False).split()[:2] if x.isdigit()]
            if nums and (best is None or sum(nums) < best[2]):
                best = (c, p, sum(nums))
    return best or (None, None, None)


def blame(hist, commit, path, ranges):
    counts, info = Counter(), {}
    for a, b in ranges:
        out = git(hist, "blame", "-w", "-M", "-C", "--line-porcelain", "-L", f"{a},{b}", commit, "--", path, check=False)
        cur = None
        for line in out.splitlines():
            if re.match(r"^[0-9a-f]{40} ", line):
                cur = line.split()[0]
                counts[cur] += 1
            elif cur and line.startswith("author-time "):
                info.setdefault(cur, {})["date"] = int(line.split()[1])
            elif cur and line.startswith("summary "):
                info.setdefault(cur, {})["summary"] = line[8:]
    return counts, info


def main():
    TASKS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows = [r for r in csv.DictReader(open(ROOT / "data_collection/tier1_master.csv")) if r["status"] == "selected"]
    out = []
    for r in rows:
        fid = r["id"]
        meta = json.loads((DATASET / r["sol_file"].replace(".sol", ".json")).read_text())
        m = re.match(r"https://github\.com/([^/]+/[^/]+)/blob/([^/]+)/([^#]+)", r["source_url"])
        snap_repo, snap_ref, path = m[1], m[2], m[3]
        ranges = meta.get("referenced_lines") or []
        h = dict(id=fid, protocol=r["protocol"], firm=r["firm"], snapshot_repo=snap_repo, snapshot_ref=snap_ref,
                 file=path, referenced_lines=ranges,
                 functions=[s.get("function_name") for s in (meta.get("problem_code") or {}).get("snippets") or []])
        if fid in LIBRARY_FILE:
            h.update(method="not searched", reason="tier-1 file is third-party library code; the bug is in protocol code we do not have")
        else:
            hist_name = SPONSOR.get(snap_repo, snap_repo) if snap_repo.startswith("code-423n4/") else snap_repo
            h["history_repo"] = hist_name
            if not hist_name:
                h.update(method="fallback", reason="no public sponsor repository found")
            else:
                try:
                    snap = clone(snap_repo)
                    ref = git(snap, "rev-parse", snap_ref if snap_ref != "main" else "HEAD").strip()
                    blob = git(snap, "rev-parse", f"{ref}:{path}").strip()
                    hist = clone(hist_name)
                    commit, hpath, diff_lines = find_audited_commit(hist, blob, git(snap, "show", f"{ref}:{path}"), path)
                    h.update(snapshot_commit=ref, snapshot_blob=blob, audited_commit=commit, history_path=hpath,
                             lines_differing_from_snapshot=diff_lines)
                    if not commit:
                        h.update(method="fallback", reason="audited file not found in the sponsor history")
                    elif not ranges:
                        h.update(method="fallback", reason="report links no line numbers to blame")
                    else:
                        counts, info = blame(hist, commit, hpath, ranges)
                        cands = [dict(commit=c, lines=n, date=info.get(c, {}).get("date"),
                                      summary=info.get(c, {}).get("summary")) for c, n in counts.most_common()]
                        vic = cands[0]["commit"] if cands else None
                        parents = git(hist, "rev-list", "--parents", "-n", "1", vic).split()[1:] if vic else []
                        later = git(hist, "log", "--format=%H %ad %s", "--date=short", f"{commit}..", "--", hpath, check=False)
                        h.update(method="history" if vic and parents and diff_lines == 0 else "history (approximate)" if vic and parents else "fallback",
                                 reason="" if vic and parents else "blame gave no usable commit or the commit has no parent",
                                 vic=vic, pvic=parents[0] if parents else None, blame_candidates=cands,
                                 vic_is_root=bool(vic) and not parents,
                                 fix_candidates=later.splitlines()[:15])
                except Exception as e:  # keep going; the failure is recorded for the log
                    h.update(method="fallback", reason=f"error: {e}")
        d = TASKS / fid
        d.mkdir(exist_ok=True)
        (d / "history.json").write_text(json.dumps(h, indent=2))
        out.append(dict(id=fid, protocol=r["protocol"], firm=r["firm"], method=h["method"], reason=h.get("reason", ""),
                        history_repo=h.get("history_repo") or "", vic=(h.get("vic") or "")[:10],
                        blame_commits=len(h.get("blame_candidates") or []),
                        lines_differing=h.get("lines_differing_from_snapshot", "")))
        print(fid, h["method"], h.get("reason", "")[:80], flush=True)
    with open(RESULTS / "history_search.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    main()
