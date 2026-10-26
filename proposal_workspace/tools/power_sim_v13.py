"""Version 13: power of the RQ1 directional claim under the adverse-bound rule for unresolved security
results (iteration-2 review R3, weakness 1).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v13.py
Data model: power_sim_v8.py with unres=(uA, uH): each working agent attempt has probability uA, and each
historical implementation probability uH, of an unresolved security result. For a claim that agents are
worse (positive difference), the adverse bound sets unresolved agent results to "not vulnerable" and
unresolved historical results to "vulnerable"; the selected 15- and 20-protocol procedures (Holm levels
0.04 and 0.035 from power_results_v10_a.txt) are applied to that bound. Counts only rejections with a
positive estimate. 400 studies per row. The true difference column is the difference without unresolved results.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8

RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}
LEVEL = {15: 0.04, 20: 0.035}

if __name__ == "__main__":
    rng = np.random.default_rng(1313)
    for P in (15, 20):
        for u in ((0, 0), (0.005, 0.005), (0.01, 0.01), (0.02, 0.02), (0.05, 0.05), (0.02, 0.0), (0.0, 0.02)):
            pw, tr_all = [], []
            for rname, rc in RECALLS.items():
                for hN, add in ((0.02, 0.10), (0.05, 0.10)):
                    d0, se, tr = v8.run(P, ([0.6] * 2, [add] * 2, 0.9, hN), rc, 400, rng, "D", unres=u if any(u) else None)
                    p = 2 * stats.t.sf(np.abs(d0) / se, P - 1)
                    rej = np.array([v8.holm(x, LEVEL[P]) for x in p]) & (d0 > 0)
                    pw.append(rej.mean(0).min()); tr_all.append(tr.mean())
            print(f"P={P} unresolved share agents {u[0]}, historical {u[1]}: true differences {min(tr_all):+.3f} to {max(tr_all):+.3f};"
                  f" minimum configuration power {min(pw):.2f} to {max(pw):.2f}", flush=True)
