"""Version 22: allocations aimed at RQ1b (the agent-minus-historical difference over the eligible population), with
the design comparison (RQ1a) kept as a secondary estimate; measured V-count frame (list 2 of
evidence/frame_inventory/README.md, mean 2.15). Answers iteration-3 meta-review items 1, 5 and 6 after power_sim_v21.py
showed that no affordable allocation meets the RQ1a criterion.

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v22.py
Cost: as power_sim_v21.py, except that audit-informed V work after the primary lock is done for a random half of the
V functions (it serves only secondary analyses), so it costs half per V slot. Protocol sampling is simple random
(SRS) or, where marked, with probability proportional to V count + 1 (PPS, power_sim_v8.py option pps).
Precision: interval multipliers for RQ1b and RQ1a on D chosen on a calibration stream (smallest with coverage >= 0.95
in every configuration and scenario), then on an independent stream: largest mean half-width, worst coverage; RQ1b:
minimum configuration power (Holm at 0.05, correct sign) for added N rates 0.05, 0.10 and 0.15; RQ1a: lowest
configuration rate of lying wholly below -0.10 by true value. Scenarios: agents' V rate 0.6 or 0.9, three recall
patterns, historical N rate 0.02 or 0.05; nulls and the three added N rates. Two attempts. 300 studies per scenario.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8
from power_sim_v21 import LIST2, RECALLS

RATES = {"low": (6, 1.5, 0.1, 8 / 64, 0.5, 1.25), "middle": (9, 2.25, 0.15, 0.178, 1.0, 1.875), "high": (12, 3, 0.2, 3 / 13, 1.5, 2.5)}
ALLOC = [(20, 2, 6, False), (17, 2, 8, False), (23, 1, 6, False), (24, 2, 4, False), (18, 4, 4, True)]
ADDS = (None, 0.05, 0.10, 0.15)
SCEN = [(aV, rc, hN, add) for aV in (0.6, 0.9) for rc in RECALLS.values() for hN in (0.02, 0.05) for add in ADDS]


def cost(vcap, nper, r):
    setup, build, op, cand, conf, sec = r
    f = vcap + nper
    return setup + f * build + f * 5 * (op + cand * conf) + vcap * sec


def runs(seed, P, vcap, nper, pps):
    seeds = np.random.default_rng(seed).integers(2**63, size=len(SCEN))
    return [v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, 300, np.random.default_rng(s), "D", parts=True,
                   max_v=vcap, k=2, nv_dist=LIST2, n_per=nper, pps=pps) for s, (aV, rc, hN, add) in zip(seeds, SCEN)]


if __name__ == "__main__":
    print("Cost: hours reserved per protocol for the maximum allocation (audit-informed V work for half of V functions)")
    for P, vcap, nper, pps in ALLOC:
        print(f"  P={P}, V cap {vcap}, N {nper}{' PPS' if pps else ''}: " + "; ".join(f"{k} {cost(vcap, nper, r):.1f} h (fits {int(900 // cost(vcap, nper, r))})" for k, r in RATES.items())
              + f"; P x middle = {P * cost(vcap, nper, RATES['middle']):.0f} h", flush=True)
    cs = np.round(np.arange(1.0, 1.81, 0.02), 2)
    for i, (P, vcap, nper, pps) in enumerate(ALLOC):
        q = stats.t.ppf(0.975, P - 1)
        cal, val = runs(2600 + 2 * i, P, vcap, nper, pps), runs(2601 + 2 * i, P, vcap, nper, pps)
        out = [f"  P={P}, V cap {vcap}, N {nper}{' PPS' if pps else ''}:"]
        for key, idx in (("RQ1b", 0), ("RQ1a on D", 6)):
            pick = lambda data: [(r[idx], r[idx + 1], r[idx + 2]) for r in data]
            cover = lambda data, c: min(((d - c * q * se <= t) & (t <= d + c * q * se)).mean(0).min() for d, se, t in data)
            c = min([c for c in cs if cover(pick(cal), c) >= 0.95], default=cs[-1])
            vd = pick(val)
            hw = max((c * q * se).mean(0).max() for d, se, t in vd)
            cv = cover(vd, c)
            if key == "RQ1b":
                fw = max(np.array([v8.holm(x, 0.05) for x in 2 * stats.t.sf(np.abs(d) / se, P - 1)]).any(1).mean() for (d, se, t), sc in zip(vd, SCEN) if sc[3] is None)
                byadd = {}
                for (d, se, t), sc in zip(vd, SCEN):
                    if sc[3] is None: continue
                    rej = np.array([v8.holm(x, 0.05) for x in 2 * stats.t.sf(np.abs(d) / se, P - 1)]) & (d > 0)
                    byadd.setdefault(sc[3], []).append((t.mean(), rej.mean(0).min()))
                cells = "; ".join(f"added {a}: true {min(x for x, _ in v):+.3f} to {max(x for x, _ in v):+.3f}, power {min(p for _, p in v):.2f}-{max(p for _, p in v):.2f}" for a, v in sorted(byadd.items()))
                out.append(f"    RQ1b: multiplier {c}, largest mean half-width {hw:.3f}, worst coverage {cv:.3f}, worst null family-wise error {fw:.3f}; {cells}")
            else:
                rates = sorted({round(float(t.mean()), 2): (d + c * q * se < -0.10).mean(0).min() for (d, se, t) in vd if t.mean() < -0.15}.items())
                out.append(f"    RQ1a on D: multiplier {c}, largest mean half-width {hw:.3f}, worst coverage {cv:.3f}; wholly below -0.10 by true value " + "; ".join(f"{t:+.2f}: {e:.2f}" for t, e in rates))
        print("\n".join(out), flush=True)
