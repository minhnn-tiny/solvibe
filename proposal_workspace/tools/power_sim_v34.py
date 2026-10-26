"""Version 34: power and error of the frozen V33 procedure (22 x (1, 6), two attempts, Holm 0.03, multiplier 1.175) when
historical outcomes are unresolved more often than agent outcomes (round-19 check of the pooled unresolved limit).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v34.py
Why: development has one historical outcome for every eight agent outcomes, so a limit pooled over authors does not bound
the historical share; with no unresolved outcome in 24 historical outcomes the upper 80% limit is 1 - 0.2^(1/24) = 0.065.
Conditions (unresolved share: agents, historical): exact null and exact +0.15 at (0, 0.02), (0, 0.03), (0, 0.065),
(0.0075, 0.02), (0.0075, 0.065). 2,000 studies per frame and condition, fresh seed; same 24 frames; no recalibration.
Reported: worst family-wise error, lowest coverage, lowest minimum-configuration power and its Bonferroni-adjusted lower bound
(over the 2 x 24 x 5 power checks of this run).
"""
import multiprocessing as mp
import numpy as np
import power_sim_v30 as v30
import power_sim_v32 as v32

DESIGN, A, C = (22, 1, 6, 2), 0.03, 1.175
US = [(0.0, 0.02), (0.0, 0.03), (0.0, 0.065), (0.0075, 0.02), (0.0075, 0.065)]
CONDS = [("exact null", 0.0, u) for u in US] + [("exact +0.15", 0.15, u) for u in US]

if __name__ == "__main__":
    v32.init(DESIGN)
    with mp.Pool(8, initializer=v32.init, initargs=(DESIGN,)) as pool:
        out = v32.run(pool, 3801, CONDS, 2000)
    m_pw = 2 * 24 * len(US)
    print(f"Frozen V33 procedure for 22 x (1, 6): Holm level {A}, multiplier {C}; 2,000 studies per frame and condition")
    for ci, (cond, target, u) in enumerate(CONDS):
        ks = [k for k in out if k[1] == ci]
        res = [(v30.decide(out[k][1], out[k][0], A), v30.cover(out[k][1], out[k][0], C)) for k in ks]
        e = max(r[0][0] for r in res); cv = min(r[1][0].min() for r in res)
        line = f"  {cond}, unresolved {u}: worst error {e:.3f}; lowest marginal coverage {cv:.3f}"
        if cond == "exact +0.15":
            pw = [x for r in res for x in r[0][1]]
            lb = min(v30.lcb(round(x * 2000), 2000, m_pw) for x in pw)
            line += f"; lowest power {min(pw):.3f}, quartiles {np.percentile(pw, 25):.2f} / {np.median(pw):.2f} / {np.percentile(pw, 75):.2f}; lower bound {lb:.3f}"
        print(line, flush=True)
    print("done")
