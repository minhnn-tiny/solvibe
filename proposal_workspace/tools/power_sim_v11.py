"""Version 11: precision of the sampling-design comparison in section 6.4 (V-only estimate minus the
weighted estimate), which proposal_v9 names as the main justification of the core study.

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v11.py
Data model: power_sim_v8.py with parts=True (endpoint D, two configurations, three attempts, up to 2 V and
8 N functions per protocol, compilation, functional success, detection by author and stratum, protocol-by-author
effect). Human V-stratum vulnerability rate 0.9 as in v8. For each configuration the V-only estimate is the
weighted V-stratum difference; the design difference is V-only minus weighted, (1 - pi)(v - w), with a
delete-one-protocol jackknife and t(P - 1), uncorrected 95% intervals and a two-sided test at 0.05.
Scenarios vary agents' V rate (0.6, 0.9), recall, the human N rate and the added N rate.
Second block (argument "v4"): up to 4 V functions per protocol instead of 2, 15 protocols.
Third block (argument "calib"): interval multiplier for the design difference, chosen on one stream (smallest
multiplier with coverage >= 0.95 in every scenario) and checked on an independent stream, 600 studies per scenario.
"""
import sys
import numpy as np
from scipy import stats
import power_sim_v8 as v8

C_DESIGN = {15: 1.16, 20: 1.14}     # calibrated multipliers from power_results_v11_calib.txt (2 V per protocol)
RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}

def calib():
    cs = np.round(np.arange(1.0, 1.61, 0.02), 2)
    for P in (15, 20):
        q = stats.t.ppf(0.975, P - 1)
        def stream(rng):
            out = []
            for aV in (0.6, 0.9):
                for rc in RECALLS.values():
                    for hN, add in ((0.02, None), (0.05, 0.10)):
                        out.append(v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, 600, rng, "D", parts=True)[6:])
            return out
        def cover(data, c):
            return min(((dd - c * q * sed <= td) & (td <= dd + c * q * sed)).mean(0).min() for dd, sed, td in data)
        cal, val = stream(np.random.default_rng(1121 + P)), stream(np.random.default_rng(1131 + P))
        c = min([c for c in cs if cover(cal, c) >= 0.95], default=None)
        cv = cover(val, c) if c else float("nan")
        hw = np.mean([(c * q * sed).mean() for dd, sed, td in val]) if c else float("nan")
        print(f"P={P}: uncalibrated worst coverage {cover(cal, 1.0):.3f}; multiplier {c}; validation worst coverage {cv:.3f}"
              f" (+/-{1.96 * np.sqrt(cv * (1 - cv) / 600):.3f}); mean calibrated half-width {hw:.3f}")


if __name__ == "__main__" and sys.argv[1:] == ["calib"]:
    calib()
elif __name__ == "__main__":
    rng = np.random.default_rng(1111)
    print("Design difference = V-only estimate minus weighted estimate, endpoint D, 400 studies per row")
    v4 = len(sys.argv) > 1 and sys.argv[1] == "v4"
    if v4:
        rng = np.random.default_rng(1112)
        print("Up to 4 V functions per protocol (instead of 2)")
    for P in ((15,) if v4 else (15, 20)):
        q = stats.t.ppf(0.975, P - 1)
        for aV in (0.6, 0.9):
            for rname, rc in RECALLS.items():
                for hN, add in ((0.02, None), (0.05, 0.10)):
                    r = v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, 400, rng, "D", parts=True, max_v=4 if v4 else 2)
                    dv, sev, tv, dd, sed, td = r[3:]
                    rej = (2 * stats.t.sf(np.abs(dd) / sed, P - 1) < 0.05).mean(0).min()
                    rej_c = (np.abs(dd) / sed > C_DESIGN[P] * q).mean(0).min()
                    cov = ((dd - q * sed <= td) & (td <= dd + q * sed)).mean(0).min()
                    covv = ((dv - q * sev <= tv) & (tv <= dv + q * sev)).mean(0).min()
                    print(f"P={P} aV {aV} recall {rname:13s} hN {hN:.2f} added N {'null' if add is None else f'{add:+.2f}'}:"
                          f" true V-only {tv.mean():+.3f}, true design difference {td.mean():+.3f};"
                          f" power {rej:.2f} (calibrated multiplier {C_DESIGN[P]}: {rej_c:.2f}), coverage {cov:.3f} (V-only {covv:.3f}), mean half-width {(q * sed).mean():.3f}")
