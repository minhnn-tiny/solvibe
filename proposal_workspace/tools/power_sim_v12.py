"""Version 12: allocation for the design comparison (V-only estimate minus weighted estimate) as a
co-primary estimand, answering iteration-2 reviews R1 (W1, W8), R2 (W4), R4 (W1) and R5 (W1).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v12.py
Data model: power_sim_v8.py with parts=True. New: p_nov, the share of sampled protocols with no V function
(a frame built from contest listings can contain them), and max_v, the cap on V functions per protocol.
For each allocation (protocols P, cap max_v, share p_nov): the interval multiplier for the design difference
is chosen on one stream (smallest multiplier on a grid with coverage >= 0.95 in every scenario) and checked
on an independent stream; then the validation stream gives the mean calibrated half-width and, by size of
the true design difference, the minimum configuration-specific rate at which the calibrated interval
excludes zero. 12 scenarios (agents' V rate 0.6 or 0.9; three recall patterns; null or added N rate) as in
power_sim_v11.py, 400 studies per scenario and stream.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8

RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}
SCEN = [(aV, rc, hN, add) for aV in (0.6, 0.9) for rc in RECALLS.values() for hN, add in ((0.02, None), (0.05, 0.10))]
GROUPS = [("0.39 to 0.57", 0.385, 9), ("about 0.33", 0.3, 0.385), ("0.17 to 0.27", 0.15, 0.3), ("0.10 to 0.15", 0.08, 0.15), ("below 0.07", 0, 0.08)]


def stream(rng, P, max_v, p_nov, n=400):
    return [v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, n, rng, "D", parts=True, max_v=max_v, p_nov=p_nov)[6:]
            for aV, rc, hN, add in SCEN]


if __name__ == "__main__":
    cs = np.round(np.arange(1.0, 1.81, 0.02), 2)
    print("P max_v p_nov | mean V functions | multiplier | validation worst coverage | mean calibrated half-width | power by |true design difference|")
    for P in (15, 20, 25):
        q = stats.t.ppf(0.975, P - 1)
        for max_v in (2, 4, 6):
            for p_nov in (0.0, 0.3):
                seed = 1200 + 100 * P + 10 * max_v + int(10 * p_nov)
                cal, val = stream(np.random.default_rng(seed), P, max_v, p_nov), stream(np.random.default_rng(seed + 5), P, max_v, p_nov)
                cover = lambda data, c: min(((dd - c * q * sed <= td) & (td <= dd + c * q * sed)).mean(0).min() for dd, sed, td in data)
                c = min([c for c in cs if cover(cal, c) >= 0.95], default=None)
                if c is None:
                    print(f"{P} {max_v} {p_nov}: no multiplier up to {cs[-1]} reaches 0.95 coverage"); continue
                cv = cover(val, c)
                hw = np.mean([(c * q * sed).mean() for dd, sed, td in val])
                nv = (1 - p_nov) * np.minimum(max_v, 2 + np.random.default_rng(1).poisson(2, 100000)).mean() * P
                pw = {}
                for dd, sed, td in val:
                    size = abs(td.mean())
                    g = next(name for name, lo, hi in GROUPS if lo <= size < hi)
                    r = (np.abs(dd) / sed > c * q).mean(0).min()
                    pw.setdefault(g, []).append(r)
                cells = "; ".join(f"{g}: {min(v):.2f}-{max(v):.2f}" for g, _, _ in GROUPS for k, v in pw.items() if k == g)
                print(f"{P} {max_v} {p_nov} | {nv:.0f} | {c} | {cv:.3f} (+/-{1.96 * np.sqrt(cv * (1 - cv) / 400):.3f}) | {hw:.3f} | {cells}", flush=True)
