"""Version 18: the RQ1a precision criterion evaluated per configuration and per scenario, with exclusion of the
meaningful difference 0.10 and with bounds for unresolved results (round-11 points R11.5 and R11.6).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v18.py
Data model: power_sim_v8.py with parts=True, two attempts. Allocations: (a) earlier V assumption, 15 protocols with
N functions, cap 4; (b) earlier assumption, 20 protocols, cap 6; (c) counted V spread, 40 protocols of which 20
with N functions, cap 6. For each allocation the interval multiplier for the design difference is chosen on stream A
(no unresolved results; smallest multiplier on a grid with coverage >= 0.95 for every configuration and scenario).
On stream B, for unresolved shares 0, 0.01 and 0.05 (both authors), the design difference is computed at its bound
toward zero for a negative difference: in V, unresolved agent results set to vulnerable and historical to not
vulnerable; in N, the reverse. Reported:
- the largest mean calibrated half-width over configurations and scenarios (not an average across them);
- for each scenario whose true design difference is negative and at least 0.30 in size, the lowest configuration
  rate at which the calibrated interval of the bound lies wholly below -0.10, i.e. excludes the meaningful difference.
12 scenarios as in power_sim_v11.py; 400 studies per scenario and stream.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8

RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}
SCEN = [(aV, rc, hN, add) for aV in (0.6, 0.9) for rc in RECALLS.values() for hN, add in ((0.02, None), (0.05, 0.10))]
COUNTED = [9, 2, 2, 0, 1, 1, 1, 1, 0, 0]
ALLOC = [("earlier assumption, 15 protocols, cap 4", 15, 4, None, None), ("earlier assumption, 20 protocols, cap 6", 20, 6, None, None),
         ("counted spread, 40 protocols (20 with N), cap 6", 40, 6, 20, COUNTED)]
TOWARD0 = ((1, 0), (0, 1))


def stream(rng, P, cap, n_sub, dist, u):
    return [v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, 400, rng, "D", parts=True, max_v=cap, k=2,
                   n_sub=n_sub, nv_dist=dist, unres=u if any(u) else None, unres_val=TOWARD0)[6:] for aV, rc, hN, add in SCEN]


if __name__ == "__main__":
    cs = np.round(np.arange(1.0, 1.81, 0.02), 2)
    for name, P, cap, n_sub, dist in ALLOC:
        q = stats.t.ppf(0.975, P - 1)
        seed = 1900 + P + cap
        cal = stream(np.random.default_rng(seed), P, cap, n_sub, dist, (0, 0))
        cover = lambda data, c: min(((dd - c * q * sed <= td) & (td <= dd + c * q * sed)).mean(0).min() for dd, sed, td in data)
        c = min([c for c in cs if cover(cal, c) >= 0.95], default=None)
        print(f"{name}: multiplier {c} (stream A)", flush=True)
        for u in ((0, 0), (0.01, 0.01), (0.05, 0.05)):
            val = stream(np.random.default_rng(seed + 1), P, cap, n_sub, dist, u)
            hw = max((c * q * sed).mean(0).max() for dd, sed, td in val)
            rates = []
            for dd, sed, td in val:
                t = td.mean()
                if t <= -0.30:
                    rates.append((t, ((dd + c * q * sed) < -0.10).mean(0).min()))
            cv = cover(val, c) if not any(u) else float("nan")
            print(f"  unresolved {u}: largest mean calibrated half-width over configurations and scenarios {hw:.3f}; "
                  + (f"validation worst coverage {cv:.3f}; " if not any(u) else "")
                  + "excludes -0.10: " + "; ".join(f"true {t:+.2f}: {r:.2f}" for t, r in sorted(rates)), flush=True)
