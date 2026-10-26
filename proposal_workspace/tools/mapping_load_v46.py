"""Exact-mapping load under project units (round-30 point R30.1): how many member audits the 22 sampled units of the
corrected main frame contain, from the inclusion probabilities and 20,000 randomized systematic draws (seed 1).

Run (from proposal_workspace/tools): uv run --offline --with numpy python mapping_load_v46.py
Input: ../evidence/frame_build/protocol_units.csv (development units removed). Output: mapping_load_v46.txt.
"""
import csv
import numpy as np
import power_sim_v29 as v29

rows = [r for r in csv.DictReader(open("../evidence/frame_build/protocol_units.csv")) if r["development"] == "0"]
size = np.array([int(r["n_eligible"]) for r in rows], float)
na = np.array([len(r["members"].split()) for r in rows])
pi = v29.incl_probs(size, 22)
rng = np.random.default_rng(1)
tot = np.array([na[v29.sys_pps(rng, pi)].sum() for _ in range(20000)])
lines = [f"main frame: {len(rows)} units, {na.sum()} audits, {(na > 1).sum()} units with several audits",
         f"expected member audits in 22 sampled units: {(pi * na).sum():.1f}; expected sampled units with several audits: {(pi * (na > 1)).sum():.1f}",
         f"member audits in 20,000 draws: median {np.median(tot):.0f}, 95th percentile {np.percentile(tot, 95):.0f}, maximum {tot.max()}"]
for h in (2, 4):
    lines.append(f"mapping hours at {h} h per audit, with the 3 development audits: median {(np.median(tot) + 3) * h:.0f}, 95th percentile {(np.percentile(tot, 95) + 3) * h:.0f}")
open("mapping_load_v46.txt", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
