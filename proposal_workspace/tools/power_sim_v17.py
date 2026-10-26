"""Version 17: calibration and validation of the final RQ1b decision under the adverse-bound rule
(round-11 point R11.4; iteration-2 meta-review item 9).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v17.py
Design: power_sim_v8.py, endpoint D, two configurations, TWO attempts (k=2), up to 2 V and 8 N functions per protocol,
15 or 20 protocols. Unresolved security results: each working agent attempt with probability uA, each historical
implementation with probability uH.
Decision for each configuration: a claim that agents are worse uses the lower bound (unresolved agent results set to
not vulnerable, historical to vulnerable); a claim that agents are better uses the upper bound (the reverse). The
configuration's p-value is the two-sided t(P-1) p-value of whichever bound lies on the claimed side of zero (1 if
neither does). Holm over the two configurations. A family error is any claim in the wrong direction or any claim
for a configuration whose true difference is zero.
Calibration (stream A, exact offsetting nulls, no unresolved results): the largest Holm level on a grid with worst
family-wise error <= 0.05. Validation (stream B): family-wise error under nulls with unresolved shares 0, 0.05, 0.10,
and under partial nulls (configuration 1 null, configuration 2 at +0.08) with 0 and 0.05; then power for
positive alternatives (agents worse, true +0.069 to +0.090) and negative alternatives (agents better, true -0.05)
across a grid of unresolved shares by author. 6 scenarios (three recall patterns x two historical N rates),
600 studies per null scenario, 400 per alternative.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8

RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}
LO, HI = ((0, 1), (0, 1)), ((1, 0), (1, 0))


def both(rng, P, scen, rc, n, u):
    """Return (estimates, SEs) at the lower and upper bound, and the true difference, for the same simulated studies."""
    seed = rng.integers(2**63)
    lo = v8.run(P, scen, rc, n, np.random.default_rng(seed), "D", k=2, unres=u if any(u) else None, unres_val=LO)
    hi = v8.run(P, scen, rc, n, np.random.default_rng(seed), "D", k=2, unres=u if any(u) else None, unres_val=HI)
    return lo, hi


def decide(lo, hi, P, a):
    (dl, sl, tr), (dh, sh, _) = lo, hi
    pl, ph = 2 * stats.t.sf(np.abs(dl) / sl, P - 1), 2 * stats.t.sf(np.abs(dh) / sh, P - 1)
    p = np.where(dl > 0, pl, np.where(dh < 0, ph, 1.0))
    sign = np.where(dl > 0, 1, np.where(dh < 0, -1, 0))
    rej = np.array([v8.holm(x, a) for x in p])
    return rej, sign, tr


def fam_error(lo, hi, P, a):
    rej, sign, tr = decide(lo, hi, P, a)
    wrong = rej & ((np.abs(tr) < 1e-9) | (np.sign(tr) != sign))
    return wrong.any(1).mean()


if __name__ == "__main__":
    alphas = [0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02]
    for P in (15, 20):
        rA, rB = np.random.default_rng(1717 + P), np.random.default_rng(1817 + P)
        nulls = lambda rng, u, n: [both(rng, P, ([0.6] * 2, None, 0.9, hN), rc, n, u) for rc in RECALLS.values() for hN in (0.02, 0.05)]
        cal = nulls(rA, (0, 0), 600)
        a_star = max([a for a in alphas if max(fam_error(lo, hi, P, a) for lo, hi in cal) <= 0.05], default=0.02)
        print(f"P={P}, two attempts: calibrated Holm level {a_star} (stream A, exact nulls, no unresolved results)", flush=True)
        for u in ((0, 0), (0.05, 0.05), (0.10, 0.10)):
            fw = max(fam_error(lo, hi, P, a_star) for lo, hi in nulls(rB, u, 600))
            print(f"  validation null, unresolved ({u[0]}, {u[1]}): worst family-wise error {fw:.3f} (+/-{1.96 * np.sqrt(fw * (1 - fw) / 600):.3f})", flush=True)
        for u in ((0, 0), (0.05, 0.05)):
            part = [both(rB, P, ([0.6] * 2, ("target", np.array([0.0, 0.08])), 0.9, hN), rc, 400, u) for rc in RECALLS.values() for hN in (0.02, 0.05)]
            fw = max(fam_error(lo, hi, P, a_star) for lo, hi in part)
            print(f"  validation partial null (configuration 1 null, configuration 2 +0.08), unresolved ({u[0]}, {u[1]}): worst family-wise error {fw:.3f}", flush=True)
        grid = ((0, 0), (0.005, 0.005), (0.01, 0.01), (0.02, 0.02), (0.05, 0.05), (0.10, 0.10), (0.02, 0), (0, 0.02), (0.10, 0), (0, 0.10))
        for u in grid:
            pos, neg, tp, tn = [], [], [], []
            for rc in RECALLS.values():
                for hN in (0.02, 0.05):
                    lo, hi = both(rB, P, ([0.6] * 2, [0.10] * 2, 0.9, hN), rc, 400, u)
                    rej, sign, tr = decide(lo, hi, P, a_star)
                    pos.append((rej & (sign > 0)).mean(0).min()); tp.append(tr.mean())
                for hN in (0.12, 0.15):
                    lo, hi = both(rB, P, ([0.2] * 2, ("target", -0.05), 0.9, hN), rc, 400, u)
                    rej, sign, tr = decide(lo, hi, P, a_star)
                    neg.append((rej & (sign < 0)).mean(0).min()); tn.append(tr.mean())
            print(f"  unresolved (agents {u[0]}, historical {u[1]}): agents worse, true {min(tp):+.3f} to {max(tp):+.3f}: minimum configuration power {min(pos):.2f} to {max(pos):.2f};"
                  f" agents better, true {min(tn):+.3f}: {min(neg):.2f} to {max(neg):.2f}", flush=True)
