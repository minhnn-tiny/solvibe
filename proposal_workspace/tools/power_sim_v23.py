"""Version 23: the chosen allocation (20 protocols, up to 2 V and 6 N functions, simple random sampling, two
attempts; measured frame, list 2) with RQ1b calibrated: Holm level chosen on exact nulls of a calibration stream
(largest on a grid with worst family-wise error <= 0.05) and checked on an independent stream; interval multiplier
chosen as in power_sim_v22.py; power of the selected procedure for added N rates 0.05, 0.10, 0.15. Also the RQ1b
security part (vulnerability among working implementations; power_sim_v8.py output indices 12 to 14): calibrated
multiplier, largest mean half-width and the rate at which the interval excludes zero, by true value.
Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v23.py
300 studies per scenario; scenarios as in power_sim_v22.py.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8
from power_sim_v21 import LIST2, RECALLS

P, VCAP, NPER = 20, 2, 6
ADDS = (None, 0.05, 0.10, 0.15)
SCEN = [(aV, rc, hN, add) for aV in (0.6, 0.9) for rc in RECALLS.values() for hN in (0.02, 0.05) for add in ADDS]


def runs(seed):
    seeds = np.random.default_rng(seed).integers(2**63, size=len(SCEN))
    return [v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, 300, np.random.default_rng(s), "D", parts=True,
                   max_v=VCAP, k=2, nv_dist=LIST2, n_per=NPER, sec=True) for s, (aV, rc, hN, add) in zip(seeds, SCEN)]


if __name__ == "__main__":
    q = stats.t.ppf(0.975, P - 1)
    cal, val = runs(2701), runs(2702)
    alphas = [0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02]
    fw = lambda data, a: max(np.array([v8.holm(x, a) for x in 2 * stats.t.sf(np.abs(r[0]) / r[1], P - 1)]).any(1).mean() for r, sc in zip(data, SCEN) if sc[3] is None)
    a_star = max([a for a in alphas if fw(cal, a) <= 0.05], default=0.02)
    print(f"RQ1b Holm level {a_star} (calibration); validation worst family-wise error {fw(val, a_star):.3f}")
    by = {}
    for r, sc in zip(val, SCEN):
        if sc[3] is None: continue
        rej = np.array([v8.holm(x, a_star) for x in 2 * stats.t.sf(np.abs(r[0]) / r[1], P - 1)]) & (r[0] > 0)
        by.setdefault(sc[3], []).append((r[2].mean(), rej.mean(0).min()))
    for a, v in sorted(by.items()):
        print(f"  added {a}: true {min(x for x, _ in v):+.3f} to {max(x for x, _ in v):+.3f}: minimum configuration power {min(p for _, p in v):.2f} to {max(p for _, p in v):.2f}")
    cs = np.round(np.arange(1.0, 1.81, 0.02), 2)
    for key, idx in (("RQ1b on D", 0), ("RQ1b security part", 12)):
        pick = lambda data: [(r[idx], r[idx + 1], r[idx + 2]) for r in data]
        cover = lambda data, c: min(((d - c * q * se <= t) & (t <= d + c * q * se)).mean(0).min() for d, se, t in data)
        c = min([c for c in cs if cover(pick(cal), c) >= 0.95], default=cs[-1])
        vd = pick(val)
        hw = max((c * q * se).mean(0).max() for d, se, t in vd)
        ex = sorted({round(float(t.mean()), 3): (np.sign(d) == np.sign(t.mean())) & (np.abs(d) > c * q * se) for d, se, t in vd if abs(t.mean()) > 0.01}.items())
        print(f"{key}: multiplier {c}, largest mean half-width {hw:.3f}, worst coverage {cover(vd, c):.3f}; interval excludes zero (correct side), by true value: "
              + "; ".join(f"{t:+.3f}: {e.mean(0).min():.2f}" for t, e in ex))
