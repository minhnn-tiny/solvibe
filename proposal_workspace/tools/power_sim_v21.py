"""Version 21: a table of candidate allocations for the iteration-3 meta-review (items 1, 2, 3, 5, 6).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v21.py
Part 1 (cost): for each allocation (protocols P, cap on V functions per protocol, N functions per protocol), the
student hours reserved for the maximum allocation of one protocol, at the low, middle and high assumed rates, with
one common construction allowance for V and N (labels are sealed during construction):
  setup + (Vcap + Nper) * build + (Vcap + Nper) * 5 * (operation + candidates * confirmation) + Vcap * secondary
with two attempts per configuration (5 discovery campaigns per function: the historical one and four agent ones).
Rates (low / middle / high): setup 6 / 9 / 12; build 1.5 / 2.25 / 3; operation 0.1 / 0.15 / 0.2 per campaign;
candidates 8/64 / 0.178 / 3/13 per campaign; confirmation 0.5 / 1.0 / 1.5 per candidate; audit-informed V work after
the primary lock 2.5 / 3.75 / 5 per V function. The processing budget is 900 student hours (months 3 to 9 less seeds).
Part 2 (precision): for each allocation and two V-count lists from evidence/frame_inventory/README.md (list 2: 2025+
audits with Solidity code, built from High/Medium counts, mean 2.15; list 1: 2025+ audits with at least 80% of
findings mapped, mean 3.19), on a calibration stream an interval multiplier for each of RQ1a on D, RQ1a on the
security part (vulnerability among working implementations) and RQ1b (smallest with coverage >= 0.95 in every
configuration and scenario); then on an independent stream: the largest mean calibrated half-width over
configurations and scenarios, worst coverage, and, for each scenario, the lowest configuration rate at which the
interval lies wholly beyond 0.10 on the side of the true value (RQ1a) or excludes zero (RQ1b, Holm at 0.05).
No unresolved outcomes; all tasks built. 12 scenarios as in power_sim_v11.py; 400 studies per scenario and stream.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8

LIST2 = [4, 0, 0, 2, 2, 1, 1, 6, 5, 3, 2, 0, 2, 1, 0, 4, 0, 1, 0, 1, 4, 2, 1, 1, 6, 6, 3, 1, 2, 3, 6, 0, 6, 4, 1, 1, 2, 2, 2, 6, 4, 1, 1, 6, 6, 1, 6, 0, 1, 1, 2, 0, 0, 2, 5, 1, 0, 2, 0, 1, 3, 0, 6, 2, 6, 6, 2, 2, 0, 2, 0, 0, 0, 1, 0, 1, 2, 2, 0, 0, 1, 6, 3, 6, 4, 1, 0, 0, 2, 1, 1, 1, 0, 0, 1, 2, 2, 3, 0, 1, 3, 2, 1, 0, 3, 1, 0, 1, 1, 1, 2, 3, 2, 0, 5, 4, 2, 4, 2, 3, 2, 4, 1, 0, 1, 1, 2, 5, 4, 1, 1, 0, 6, 4, 1, 4, 4, 1, 2, 1, 5, 6, 5, 2, 2, 0, 2, 0, 0, 6, 1, 1, 0, 1, 5, 0, 1, 2, 0, 0, 0, 6, 1, 2, 2, 0, 3, 1, 0, 2, 0, 0, 2, 2, 4, 4, 5, 6, 3, 6, 0, 6, 1, 6, 1, 0, 6, 1, 2, 2, 0, 4, 2, 0, 6, 2, 1, 6, 2, 5, 3, 6, 6, 0, 2, 5, 3, 5, 0, 0, 3, 6, 1, 0, 6, 6, 6, 5, 0, 0, 0, 1, 0, 0, 0, 2, 2, 1, 0, 1, 1, 1, 2, 4, 1, 0, 3, 5, 0, 3, 0, 0, 0, 5, 0, 6, 0, 2, 1, 6, 3, 1, 0]
LIST1 = [1, 1, 6, 6, 2, 1, 3, 5, 6, 0, 6, 3, 3, 5, 3, 3, 4, 1, 2, 1, 5, 0, 3, 0, 0, 1, 6, 6, 2, 1, 1, 3, 2, 6, 4, 6, 2, 6, 6, 4, 3, 5]
RATES = {"low": (6, 1.5, 0.1, 8 / 64, 0.5, 2.5), "middle": (9, 2.25, 0.15, 0.178, 1.0, 3.75), "high": (12, 3, 0.2, 3 / 13, 1.5, 5)}
ALLOC = [(20, 6, 8), (16, 4, 4), (19, 4, 2), (22, 2, 4), (24, 3, 2)]
RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}
SCEN = [(aV, rc, hN, add) for aV in (0.6, 0.9) for rc in RECALLS.values() for hN, add in ((0.02, None), (0.05, 0.10))]


def cost(vcap, nper, r):
    setup, build, op, cand, conf, sec = r
    f = vcap + nper
    return setup + f * build + f * 5 * (op + cand * conf) + vcap * sec


def runs(seed, P, vcap, nper, dist):
    seeds = np.random.default_rng(seed).integers(2**63, size=len(SCEN))
    return [v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, 400, np.random.default_rng(s), "D", parts=True,
                   max_v=vcap, k=2, nv_dist=dist, n_per=nper, sec=True) for s, (aV, rc, hN, add) in zip(seeds, SCEN)]


if __name__ == "__main__":
    print("Part 1: hours reserved per protocol for the maximum allocation, and protocols that fit 900 hours")
    for P, vcap, nper in ALLOC:
        cells = []
        for name, r in RATES.items():
            h = cost(vcap, nper, r)
            cells.append(f"{name} {h:.1f} h (fits {int(900 // h)} protocols)")
        print(f"  P={P}, V cap {vcap}, N {nper}: " + "; ".join(cells) + f"; needed at middle rates for P={P}: {P * cost(vcap, nper, RATES['middle']):.0f} h", flush=True)
    print("Part 2: precision")
    cs = np.round(np.arange(1.0, 1.81, 0.02), 2)
    for lname, dist in (("list 2 (mean 2.15)", LIST2), ("list 1 (mean 3.19)", LIST1)):
        for i, (P, vcap, nper) in enumerate(ALLOC):
            q = stats.t.ppf(0.975, P - 1)
            seed = 2400 + 10 * i + (0 if dist is LIST2 else 5)
            cal, val = runs(seed, P, vcap, nper, dist), runs(seed + 1, P, vcap, nper, dist)
            res = []
            for key, idx in (("RQ1a on D", 6), ("RQ1a security part", 9), ("RQ1b", 0)):
                pick = lambda data: [(r[idx], r[idx + 1], r[idx + 2]) for r in data]
                cover = lambda data, c: min(((d - c * q * se <= t) & (t <= d + c * q * se)).mean(0).min() for d, se, t in data)
                c = min([c for c in cs if cover(pick(cal), c) >= 0.95], default=cs[-1])
                vd = pick(val)
                hw = max((c * q * se).mean(0).max() for d, se, t in vd)
                cv = cover(vd, c)
                rates = []
                for d, se, t in vd:
                    tt = t.mean()
                    if key == "RQ1b":
                        if abs(tt) < 1e-9:
                            continue
                        rej = np.array([v8.holm(x, 0.05) for x in 2 * stats.t.sf(np.abs(d) / se, P - 1)]) & (np.sign(d) == np.sign(tt))
                        rates.append((round(float(tt), 3), rej.mean(0).min()))
                    else:
                        beyond = (d + c * q * se < -0.10) if tt < 0 else (d - c * q * se > 0.10)
                        rates.append((round(float(tt), 2), beyond.mean(0).min()))
                rr = "; ".join(f"{t:+.2f}: {e:.2f}" for t, e in sorted(rates))
                res.append(f"    {key}: multiplier {c}, largest mean half-width {hw:.3f}, worst coverage {cv:.3f}; " + ("power by true difference " if key == "RQ1b" else "beyond 0.10 by true value ") + rr)
            print(f"  {lname}, P={P}, V cap {vcap}, N {nper}:\n" + "\n".join(res), flush=True)
