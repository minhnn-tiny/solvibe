#!/usr/bin/env python3
"""Step 3 of the frame build (no network): apply the repository rule, merge duplicate audits, group audits of the same
project into one sampling unit, and record the exact snapshots counted (round-29 points R29.1, R29.2, R29.3, R29.5).

Usage (from the repository root):
  python3.12 -I proposal_workspace/evidence/frame_build/frame_units.py --clones <folder used by fetch_and_count.py>
Reads frame_list.csv and frame_counts.csv (steps 1 and 2), the inventory months (../frame_inventory/per_protocol_audit.csv),
the 25-audit hand count and ../../dev_case/drawn_protocols.csv. Uses the existing clones only; nothing in them is run.
Rules:
- Repository rule. A linked repository counts as an audit's code only if it belongs to the contest organisation
  (code-423n4 or sherlock-audit) and the year-month prefix of its name is within one month of the audit's month. Other
  linked repositories (dependencies, the project's own repository, another contest's repository) are ignored. An audit with
  no such repository has no identified audited code; one whose such repositories all failed to fetch is not accessible.
- Scope and eligible functions: as in fetch_and_count.py (scope.txt, then the README scope section, then every .sol file
  outside test, mock, script and library folders), applied to the counted repositories only.
- Duplicates. Audits whose counted repositories and commits are identical are one audit; the lowest-numbered record is kept.
- Project. Audits whose inventory protocol names share the first word (ignoring "The", "Audit" and "Protocol"; the first six
  letters compared) form one sampling unit. The 25 resulting groups were checked by hand on 2026-10-26.
- Development. Units that contain a drawn development audit are removed from the main frame.
Writes next to this script: frame_audits.csv (one row per audit: status, reason, counted repositories, scope source,
eligible functions, duplicate and project), frame_snapshots.csv (one row per counted repository: resolved commit, SHA-256 of
the scope file, number of in-scope files, SHA-256 of their sorted path and blob list, eligible functions) and
protocol_units.csv (unit_id, n_eligible, members, development) and main_frame.csv (protocol_id, n_eligible: the units
without a development audit), the input of the main draw with ../../dev_case/draw_protocols.py.
"""
import argparse, collections, csv, hashlib, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
from fetch_and_count import SKIP, readme_scope, count

ORGS = ("code-423n4", "sherlock-audit")
STOP = {"the", "audit", "protocol"}


def month(s):
    return int(s[:4]) * 12 + int(s[5:7])


def git(args, cwd):
    return subprocess.run(["git", "-c", "core.hooksPath=/dev/null"] + args, cwd=cwd, capture_output=True, text=True).stdout


def qualifies(entry, audit_month):
    owner, rest = entry.split("/", 1)
    m = re.match(r"(\d{4}-\d{2})-", rest)
    return owner in ORGS and m is not None and abs(month(audit_month) - month(m.group(1))) <= 1


def project_key(protocol):
    w = [t for t in (re.sub(r"[^a-z0-9]", "", x.lower()) for x in protocol.split()) if t and t not in STOP]
    return w[0][:6] if w else protocol


def scope_of(dest):
    sol = [str(p.relative_to(dest)) for p in dest.rglob("*.sol") if ".git/" not in str(p)]
    sf, rd = dest / "scope.txt", dest / "README.md"
    if sf.exists():
        listed = [ln.strip().lstrip("./") for ln in sf.read_text(errors="replace").splitlines() if ln.strip().endswith(".sol")]
        return "scope.txt", [p for p in listed if (dest / p).is_file()], sf
    listed = [p for p in (readme_scope(rd.read_text(errors="replace")) if rd.exists() else []) if (dest / p).is_file()]
    if listed:
        return "README scope", listed, rd
    return "automatic", [p for p in sol if not SKIP.search(p)], None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clones", required=True)
    a = ap.parse_args()
    months = {r["audit_key"]: r["month"] for r in csv.DictReader(open(HERE.parent / "frame_inventory" / "per_protocol_audit.csv"))}
    old = {r["slug"]: r for r in csv.DictReader(open(HERE / "frame_counts.csv"))}
    dev = {r["protocol_id"] for r in csv.DictReader(open(WS / "dev_case" / "drawn_protocols.csv"))}
    audits, snaps = [], []
    for r in csv.DictReader(open(HERE / "frame_list.csv")):
        out = dict(slug=r["slug"], firm=r["firm"], protocol=r["protocol"], year=r["year"], month=months.get(r["audit_key"], ""),
                   status="", reason="", repos="", scope_source="", files=0, eligible=0, duplicate_of="", project=project_key(r["protocol"]))
        entries = r["repos"].split()
        if not entries:
            out.update(status="excluded", reason="no linked repository"); audits.append(out); continue
        keep = [(i, e) for i, e in enumerate(entries) if out["month"] and qualifies(e, out["month"])]
        if not keep:
            out.update(status="excluded", reason="audited code not identified: no linked contest repository from the audit's month"); audits.append(out); continue
        per = []
        for i, e in keep:
            dest = Path(a.clones) / f"{r['slug']}-{i}"
            if not (dest / ".git").exists() or not git(["rev-parse", "--verify", "-q", "HEAD"], dest).strip():
                continue
            src, scope, sfile = scope_of(dest)
            per.append((i, e, dest, src, scope, sfile))
        if not per:
            out.update(status="excluded", reason="contest repository not accessible"); audits.append(out); continue
        if any(p[3] != "automatic" for p in per):
            per = [p for p in per if p[3] != "automatic"]
        total, nfiles, srcs, used = 0, 0, [], []
        for i, e, dest, src, scope, sfile in per:
            rows, _ = count(dest, scope)
            elig = sum(x["eligible"] for x in rows)
            commit = git(["rev-parse", "HEAD"], dest).strip()
            listing = git(["ls-files", "-s", "--"] + sorted(scope), dest) if scope else ""
            snaps.append(dict(slug=r["slug"], repository=e.rsplit("@", 1)[0], linked_ref=e.rsplit("@", 1)[1], commit=commit, scope_source=src,
                              scope_file_sha256=hashlib.sha256(sfile.read_bytes()).hexdigest() if sfile else "", files=len(scope),
                              files_sha256=hashlib.sha256(listing.encode()).hexdigest(), eligible=elig))
            total += elig; nfiles += len(scope); srcs.append(src); used.append(f"{e.rsplit('@', 1)[0]}@{commit}")
        out.update(repos=" ".join(used), scope_source="+".join(sorted(set(srcs))), files=nfiles, eligible=total)
        out.update(status="counted" if total > 0 else "excluded", reason="" if total > 0 else "no Solidity code in scope at the linked version")
        audits.append(out)
    seen = {}
    for o in audits:
        if o["status"] == "counted":
            k = tuple(sorted(o["repos"].split()))
            if k in seen:
                o.update(status="duplicate", duplicate_of=seen[k])
            else:
                seen[k] = o["slug"]
    units = collections.defaultdict(list)
    for o in audits:
        if o["status"] == "counted":
            units[o["project"]].append(o)
    fields = list(audits[0])
    with open(HERE / "frame_audits.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(audits)
    with open(HERE / "frame_snapshots.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(snaps[0])); w.writeheader(); w.writerows(snaps)
    with open(HERE / "protocol_units.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["unit_id", "n_eligible", "members", "development"])
        for k in sorted(units):
            ms = units[k]
            w.writerow([f"project-{k}", sum(m["eligible"] for m in ms), " ".join(f"{m['slug']}:{m['eligible']}" for m in ms), int(any(m["slug"] in dev for m in ms))])
    with open(HERE / "main_frame.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["protocol_id", "n_eligible"])
        for k in sorted(units):
            if not any(m["slug"] in dev for m in units[k]):
                w.writerow([f"project-{k}", sum(m["eligible"] for m in units[k])])
    st = collections.Counter((o["status"], o["reason"]) for o in audits)
    for k, v in sorted(st.items()):
        print(f"{v:4d}  {k[0]}  {k[1]}")
    counted = [o for o in audits if o["status"] == "counted"]
    print("counted audits:", len(counted), "| eligible functions:", sum(o["eligible"] for o in counted),
          "| by firm:", dict(collections.Counter(o["firm"] for o in counted)), "| by year:", dict(collections.Counter(o["year"] for o in counted)))
    print("scope source (mutually exclusive):", dict(collections.Counter(o["scope_source"] for o in counted)))
    multi = {k: v for k, v in units.items() if len(v) > 1}
    print("units:", len(units), "| units with several audits:", len(multi), "| development units:", sorted(k for k, v in units.items() if any(m["slug"] in dev for m in v)))
    print("main frame units:", sum(1 for v in units.values() if not any(m["slug"] in dev for m in v)),
          "| eligible functions:", sum(sum(m["eligible"] for m in v) for v in units.values() if not any(m["slug"] in dev for m in v)))
    changed = [(o["slug"], old[o["slug"]]["status"], old[o["slug"]]["eligible"], o["status"], o["eligible"]) for o in audits
               if (old[o["slug"]]["status"] == "counted") != (o["status"] == "counted") or (o["status"] == "counted" and int(old[o["slug"]]["eligible"]) != o["eligible"])]
    print("audits whose status or count changed from frame_counts.csv:")
    for c in changed:
        print("  ", c)
    hand = {h["slug"]: h for h in csv.DictReader(open(HERE.parent / "frame_audit" / "strict" / "per_audit_strict.csv"))}
    pairs = [(o["slug"], o["eligible"], int(hand[o["slug"]]["eligible_functions"])) for o in counted if o["slug"] in hand]
    print(f"hand-counted audits in the frame: {len(pairs)}; equal to the hand eligible count: {sum(x == y for _, x, y in pairs)}")


if __name__ == "__main__":
    main()
