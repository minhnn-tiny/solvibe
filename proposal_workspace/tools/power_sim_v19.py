"""Version 19: the RQ1a criterion of proposal_v13 section 6.4 on the full interval that encloses both
identification bounds, for the fixed allocation (20 protocols, up to 6 V and 8 N functions, two attempts),
with unresolved results (round-12 concern of Peer B: V18 checked one bound only).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v19.py
For each simulated study the design difference G is computed twice on the same data: at its lower bound
(V: unresolved agent results not vulnerable, historical vulnerable; N: the reverse) and at its upper bound
(V: agent vulnerable, historical not; N: the reverse). Full interval = [G_lo - c q se_lo, G_hi + c q se_hi], with
the multiplier c chosen on a separate stream without unresolved results (smallest with coverage >= 0.95 in every
configuration and scenario). Reported for unresolved shares 0, 0.005, 0.01, 0.02 and 0.05 in both authors:
the largest mean half-width of the full interval over configurations and scenarios; the worst coverage of the true
design difference; and, for scenarios with a true difference of -0.30 or below, the lowest configuration rate at
which the full interval lies wholly below -0.10. Frames: the earlier V assumption (2 + Poisson(2)) and the counted
spread [9, 2, 2, 0, 1, 1, 1, 1, 0, 0]. 12 scenarios as in power_sim_v11.py; 400 studies per scenario.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8

RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}
SCEN = [(aV, rc, hN, add) for aV in (0.6, 0.9) for rc in RECALLS.values() for hN, add in ((0.02, None), (0.05, 0.10))]
COUNTED = [9, 2, 2, 0, 1, 1, 1, 1, 0, 0]
GLO, GHI = ((0, 1), (1, 0)), ((1, 0), (0, 1))
P, CAP, K = 20, 6, 2


def runs(rng, dist, u, vals):
    seed = rng.integers(2**63, size=len(SCEN))
    return [v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, 400, np.random.default_rng(s), "D", parts=True,
                   max_v=CAP, k=K, nv_dist=dist, unres=u if any(u) else None, unres_val=vals)[6:]
            for s, (aV, rc, hN, add) in zip(seed, SCEN)]


if __name__ == "__main__":
    cs = np.round(np.arange(1.0, 1.81, 0.02), 2)
    q = stats.t.ppf(0.975, P - 1)
    for name, dist, seed in (("earlier V assumption", None, 2001), ("counted spread", COUNTED, 2002)):
        cal = runs(np.random.default_rng(seed), dist, (0, 0), GLO)
        cover = lambda data, c: min(((dd - c * q * sed <= td) & (td <= dd + c * q * sed)).mean(0).min() for dd, sed, td in data)
        c = min([c for c in cs if cover(cal, c) >= 0.95], default=None)
        print(f"{name}, 20 protocols, V cap 6, two attempts: multiplier {c} (calibration stream, no unresolved results)", flush=True)
        for u in ((0, 0), (0.005, 0.005), (0.01, 0.01), (0.02, 0.02), (0.05, 0.05)):
            r = np.random.default_rng(seed + 10)                 # same studies for every u and both bounds
            lo, hi = runs(r, dist, u, GLO), runs(np.random.default_rng(seed + 10), dist, u, GHI)
            hw, cov, ex = [], [], []
            for (gl, sl, td), (gh, sh, _) in zip(lo, hi):
                a, b = gl - c * q * sl, gh + c * q * sh
                hw.append(((b - a) / 2).mean(0).max()); cov.append(((a <= td) & (td <= b)).mean(0).min())
                if td.mean() <= -0.30:
                    ex.append((round(float(td.mean()), 2), (b < -0.10).mean(0).min()))
            print(f"  unresolved {u}: largest mean full-interval half-width {max(hw):.3f}; worst coverage {min(cov):.3f}; excludes -0.10: "
                  + "; ".join(f"true {t:+.2f}: {e:.2f}" for t, e in sorted(ex)), flush=True)
