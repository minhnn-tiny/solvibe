#!/usr/bin/env python3
"""Check of the automated size measure: for audits that are both in the frame count (frame_counts.csv) and in the
25-audit hand count (../frame_audit/strict/per_audit_strict.csv), compare the automated eligible-function count with the
hand count's eligible functions and strict N. Prints each pair, the ratio, and Spearman's rank correlation.
Usage (from the repository root): python3.12 -I proposal_workspace/evidence/frame_build/compare_with_audit.py
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent


def ranks(x):
    order = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    n = len(a); ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    va = sum((x - ma) ** 2 for x in ra) ** 0.5; vb = sum((y - mb) ** 2 for y in rb) ** 0.5
    return cov / (va * vb)


def main():
    auto = {r["slug"]: r for r in csv.DictReader(open(HERE / "frame_counts.csv"))}
    hand = {r["slug"]: r for r in csv.DictReader(open(HERE.parent / "frame_audit" / "strict" / "per_audit_strict.csv"))}
    pairs = []
    for s, h in sorted(hand.items()):
        a = auto.get(s)
        if a and a["status"] == "counted":
            pairs.append((s, int(a["eligible"]), int(h["eligible_functions"]), int(h["strict_n"]), a["scope_source"]))
    print(f"audits in both: {len(pairs)} of {len(hand)} hand-counted")
    for s, ae, he, hn, src in pairs:
        print(f"  {s}: automated eligible {ae} ({src}); hand eligible {he}; strict N {hn}; ratio automated / strict N {ae / max(hn, 1):.2f}")
    if len(pairs) >= 3:
        ae = [p[1] for p in pairs]; hn = [p[3] for p in pairs]
        rat = sorted(a / max(h, 1) for a, h in zip(ae, hn))
        print(f"Spearman correlation, automated eligible vs strict N: {spearman(ae, hn):.3f}; ratio median {rat[len(rat) // 2]:.2f}, range {rat[0]:.2f} to {rat[-1]:.2f}")


if __name__ == "__main__":
    main()
