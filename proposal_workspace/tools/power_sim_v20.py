"""Version 20: the fixed allocation under construction selection (round-13 point R13.1).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v20.py
Design: each sampled function has its own fixed construction allowance; its task is built with probability
p_build[V] or p_build[N], independently of outcomes and of other functions (power_sim_v8.py option p_build). The
target is the constructible domain. Estimation is domain-weighted: stratum means over built functions with
inclusion weights, and constructible stratum shares estimated from the weighted built counts in every jackknife
replicate. Fixed allocation: 20 protocols, up to 6 V and 8 N functions, two attempts, earlier V assumption.
For each build scenario:
- RQ1a: multiplier for the design difference chosen on a stream without unresolved results; then, on an
  independent stream with unresolved shares 0 and 0.005 in both authors, the full interval enclosing both bounds
  (as in power_sim_v19.py): largest mean half-width over configurations and scenarios, worst coverage of the
  domain's true design difference, and the lowest configuration rate of lying wholly below -0.10 near -0.33;
- RQ1b: worst family-wise error under exact frame nulls is not defined for the domain, so the script reports
  coverage of the domain's true author difference by the plain t-interval, the mean raw half-width, and the
  minimum configuration power of Holm at level 0.05 (the two-attempt level of power_results_v17.txt) for the
  larger alternatives (added N rate +0.10).
12 scenarios as in power_sim_v11.py for RQ1a; 6 for RQ1b; 400 studies per scenario.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8

RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}
SCEN = [(aV, rc, hN, add) for aV in (0.6, 0.9) for rc in RECALLS.values() for hN, add in ((0.02, None), (0.05, 0.10))]
GLO, GHI = ((0, 1), (1, 0)), ((1, 0), (0, 1))
P, CAP, K = 20, 6, 2
BUILD = [None, (0.9, 0.9), (0.7, 0.9), (0.9, 0.7), (0.6, 0.6)]


def runs(seed, pb, u, vals, scen=SCEN, parts=True):
    seeds = np.random.default_rng(seed).integers(2**63, size=len(scen))
    return [v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, 400, np.random.default_rng(s), "D", parts=parts,
                   max_v=CAP, k=K, unres=u if any(u) else None, unres_val=vals, p_build=pb)
            for s, (aV, rc, hN, add) in zip(seeds, scen)]


if __name__ == "__main__":
    cs = np.round(np.arange(1.0, 1.81, 0.02), 2)
    q = stats.t.ppf(0.975, P - 1)
    for i, pb in enumerate(BUILD):
        name = "all tasks built" if pb is None else f"build probability V {pb[0]}, N {pb[1]}"
        cal = [r[6:] for r in runs(2100 + i, pb, (0, 0), GLO)]
        cover = lambda data, c: min(((dd - c * q * sed <= td) & (td <= dd + c * q * sed)).mean(0).min() for dd, sed, td in data)
        c = min([c for c in cs if cover(cal, c) >= 0.95], default=None)
        print(f"{name}: RQ1a multiplier {c}", flush=True)
        for u in ((0, 0), (0.005, 0.005)):
            lo, hi = runs(2200 + i, pb, u, GLO), runs(2200 + i, pb, u, GHI)
            hw, cov, ex = [], [], []
            for a_, b_ in zip(lo, hi):
                (gl, sl, td), (gh, sh, _) = a_[6:], b_[6:]
                a, b = gl - c * q * sl, gh + c * q * sh
                hw.append(((b - a) / 2).mean(0).max()); cov.append(((a <= td) & (td <= b)).mean(0).min())
                if td.mean() <= -0.30:
                    ex.append((round(float(td.mean()), 2), (b < -0.10).mean(0).min()))
            print(f"  RQ1a, unresolved {u}: largest mean full-interval half-width {max(hw):.3f}; worst coverage {min(cov):.3f}; excludes -0.10: "
                  + "; ".join(f"true {t:+.2f}: {e:.2f}" for t, e in sorted(ex)), flush=True)
        alt = [(0.6, rc, hN, 0.10) for rc in RECALLS.values() for hN in (0.02, 0.05)]
        res = runs(2300 + i, pb, (0, 0), GLO, scen=alt, parts=False)
        pw = [np.array([v8.holm(x, 0.05) for x in 2 * stats.t.sf(np.abs(d) / se, P - 1)]).mean(0).min() for d, se, tr in res]
        cv = [((d - q * se <= tr) & (tr <= d + q * se)).mean(0).min() for d, se, tr in res]
        hwb = [(q * se).mean() for d, se, tr in res]
        trs = [tr.mean() for d, se, tr in res]
        print(f"  RQ1b, larger alternatives (domain true {min(trs):+.3f} to {max(trs):+.3f}): minimum configuration power {min(pw):.2f} to {max(pw):.2f};"
              f" worst coverage of plain t-interval {min(cv):.3f}; mean raw half-width {min(hwb):.3f} to {max(hwb):.3f}", flush=True)
