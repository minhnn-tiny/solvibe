"""Version 24: the principal decision of proposal_v16 on the security part (round-15 point R15.2).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v24.py
Design: the chosen allocation (20 protocols, up to 2 V and 6 N functions, simple random sampling, two attempts), V counts
from list 2 of evidence/frame_inventory/README.md. Estimand: the security part of RQ1b, the difference in detected
vulnerability among implementations that compile and pass the functional checks, standardized by stratum shares
(power_sim_v8.py output indices 12 to 14). Data are generated with the security part set EXACTLY to a target in every
study (power_sim_v8.py option add=("sec_target", T)).
Decision: for each configuration, the t(P-1) test on the bound on the claimed side (lower bound for "agents worse",
upper bound for "agents better"; with no unresolved results both bounds equal the estimate), Holm across the two
configurations. A family error is any claim for a configuration whose true security part is zero, or with the wrong sign.
Calibration (stream A): the largest Holm level on a grid with worst family-wise error <= 0.05 over exact security nulls
without unresolved results. Validation (stream B): exact nulls with unresolved shares 0, 0.005 and 0.013 in both authors;
a partial null (configuration 1 at 0, configuration 2 at +0.10); and power at exactly +0.05, +0.10 and +0.15, with
unresolved shares 0 and 0.013. Every scenario is reported separately (12 scenarios: agents' V rate 0.6 or 0.9, three recall
patterns, historical N rate 0.05 or 0.10; a rate of 0.02 makes the exact security null infeasible). 300 studies per scenario.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8
from power_sim_v21 import LIST2, RECALLS

P, VCAP, NPER = 20, 2, 6
LO, HI = ((0, 1), (0, 1)), ((1, 0), (1, 0))
BASE = [(aV, rc, hN) for aV in (0.6, 0.9) for rc in RECALLS.values() for hN in (0.05, 0.10)]   # hN 0.02 cannot hold an exact security null when agents have higher recall


def pair(seed, aV, rc, hN, target, u):
    kw = dict(parts=True, max_v=VCAP, k=2, nv_dist=LIST2, n_per=NPER, sec=True, unres=u if any(u) else None)
    lo = v8.run(P, ([aV] * 2, ("sec_target", target), 0.9, hN), rc, 300, np.random.default_rng(seed), "D", unres_val=LO, **kw)
    hi = v8.run(P, ([aV] * 2, ("sec_target", target), 0.9, hN), rc, 300, np.random.default_rng(seed), "D", unres_val=HI, **kw)
    return (lo[12], lo[13], lo[14]), (hi[12], hi[13])


def decide(lo, hi, a):
    (dl, sl, tr), (dh, sh) = lo, hi
    pl, ph = 2 * stats.t.sf(np.abs(dl) / sl, P - 1), 2 * stats.t.sf(np.abs(dh) / sh, P - 1)
    p = np.where(dl > 0, pl, np.where(dh < 0, ph, 1.0))
    sign = np.where(dl > 0, 1, np.where(dh < 0, -1, 0))
    return np.array([v8.holm(x, a) for x in p]), sign, tr


def fam_err(lo, hi, a):
    rej, sign, tr = decide(lo, hi, a)
    return (rej & ((np.abs(tr) < 1e-9) | (np.sign(tr) != sign))).any(1).mean()


if __name__ == "__main__":
    alphas = [0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02]
    seedA, seedB = np.random.default_rng(2401), np.random.default_rng(2402)
    cal = [pair(seedA.integers(2**62), *b, 0.0, (0, 0)) for b in BASE]
    a_star = max([a for a in alphas if max(fam_err(lo, hi, a) for lo, hi in cal) <= 0.05], default=0.02)
    print(f"Holm level {a_star} (calibrated on exact security nulls, no unresolved results)", flush=True)
    for u in ((0, 0), (0.005, 0.005), (0.013, 0.013)):
        errs = [fam_err(*pair(seedB.integers(2**62), *b, 0.0, u), a_star) for b in BASE]
        print(f"  exact null, unresolved {u}: family-wise error by scenario " + ", ".join(f"{e:.3f}" for e in errs) + f"; worst {max(errs):.3f}", flush=True)
    errs = [fam_err(*pair(seedB.integers(2**62), *b, np.array([0.0, 0.10]), (0, 0)), a_star) for b in BASE]
    print("  partial null (configuration 1 at 0, configuration 2 at +0.10): family-wise error by scenario " + ", ".join(f"{e:.3f}" for e in errs) + f"; worst {max(errs):.3f}", flush=True)
    for target in (0.05, 0.10, 0.15):
        for u in ((0, 0), (0.013, 0.013)):
            pw = []
            for b in BASE:
                rej, sign, tr = decide(*pair(seedB.integers(2**62), *b, target, u), a_star)
                assert np.allclose(tr, target)
                pw.append((rej & (sign > 0)).mean(0).min())
            print(f"  exact +{target:.2f}, unresolved {u}: minimum configuration power by scenario " + ", ".join(f"{x:.2f}" for x in pw) + f"; lowest {min(pw):.2f}, median {np.median(pw):.2f}", flush=True)
