"""Version 15: cheaper ways to make the design comparison precise (iteration-2 meta-review items 1, 13 and
disagreement 6), with V counts per protocol shaped like the measured frame.

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v15.py
Data model: power_sim_v8.py with parts=True and three options: nv_dist (V counts per protocol drawn from a list),
n_sub (N functions built only in the first n_sub protocols; the other protocols contribute V functions only), and
k (attempts per configuration).
V-count lists:
- "counted": [9, 2, 2, 0, 1, 1, 1, 1, 0, 0], the distinct single-function V functions per protocol among the 43
  pilot findings with history (evidence/frame_count/README.md). This undercounts a full audit, because the 43 are
  a filtered subset of each protocol's findings; it is the pessimistic case.
- "v8": 2 + Poisson(2), the earlier assumption.
For each allocation: interval multiplier for the design difference chosen on one stream and checked on another
(as in power_sim_v12.py), mean calibrated half-width, rates of excluding zero by size of the true design
difference, and the mean raw half-width of the RQ1 weighted difference (t quantile, no multiplier).
Counts: mean V functions, N functions, and discovery campaigns F + F x 2 x k.
12 scenarios as in power_sim_v11.py, 400 studies per scenario and stream.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8

RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}
SCEN = [(aV, rc, hN, add) for aV in (0.6, 0.9) for rc in RECALLS.values() for hN, add in ((0.02, None), (0.05, 0.10))]
GROUPS = [("0.39 to 0.57", 0.385, 9), ("about 0.33", 0.3, 0.385), ("0.17 to 0.27", 0.15, 0.3), ("0.10 to 0.15", 0.08, 0.15), ("below 0.07", 0, 0.08)]
COUNTED = [9, 2, 2, 0, 1, 1, 1, 1, 0, 0]
ALLOC = [  # (protocols, cap on V per protocol, attempts, protocols with N functions)
    (15, 4, 3, None), (20, 6, 2, None), (25, 6, 2, None), (30, 6, 2, 20), (40, 6, 2, 20)]


def stream(rng, P, cap, k, n_sub, dist):
    return [v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, 400, rng, "D", parts=True,
                   max_v=cap, k=k, n_sub=n_sub, nv_dist=dist) for aV, rc, hN, add in SCEN]


if __name__ == "__main__":
    cs = np.round(np.arange(1.0, 1.81, 0.02), 2)
    print("V counts | P cap attempts N-protocols | V fns, N fns, campaigns | multiplier | validation worst coverage | calibrated half-width | RQ1 raw half-width | rate of excluding zero by |true design difference|")
    for dname, dist in (("counted", COUNTED), ("v8", None)):
        for P, cap, k, n_sub in ALLOC:
            q = stats.t.ppf(0.975, P - 1)
            seed = 1500 + P * 10 + cap + k + (0 if n_sub is None else n_sub) + (0 if dist is None else 7)
            cal, val = stream(np.random.default_rng(seed), P, cap, k, n_sub, dist), stream(np.random.default_rng(seed + 3), P, cap, k, n_sub, dist)
            dd_cal = [r[6:] for r in cal]; dd_val = [r[6:] for r in val]
            cover = lambda data, c: min(((dd - c * q * sed <= td) & (td <= dd + c * q * sed)).mean(0).min() for dd, sed, td in data)
            c = min([c for c in cs if cover(dd_cal, c) >= 0.95], default=None)
            if c is None:
                print(f"{dname} | {P} {cap} {k} {n_sub}: no multiplier up to {cs[-1]} reaches 0.95"); continue
            cv = cover(dd_val, c)
            hw = np.mean([(c * q * sed).mean() for dd, sed, td in dd_val])
            rq1 = np.mean([(q * r[1]).mean() for r in val])
            draw = np.random.default_rng(2).choice(COUNTED, 200000) if dist is not None else 2 + np.random.default_rng(2).poisson(2, 200000)
            nV = np.minimum(cap, draw).mean() * P
            nN = 8 * (P if n_sub is None else n_sub)
            camp = (nV + nN) * (1 + 2 * k)
            pw = {}
            for dd, sed, td in dd_val:
                g = next(name for name, lo, hi in GROUPS if lo <= abs(td.mean()) < hi)
                pw.setdefault(g, []).append((np.abs(dd) / sed > c * q).mean(0).min())
            cells = "; ".join(f"{g}: {min(pw[g]):.2f}-{max(pw[g]):.2f}" for g, _, _ in GROUPS if g in pw)
            print(f"{dname} | {P} {cap} {k} {n_sub or P} | {nV:.0f}, {nN}, {camp:.0f} | {c} | {cv:.3f} (+/-{1.96 * np.sqrt(cv * (1 - cv) / 400):.3f}) | {hw:.3f} | {rq1:.3f} | {cells}", flush=True)
