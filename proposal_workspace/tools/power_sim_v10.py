"""Version 10: answers Peer B's round-7 points R7.1 to R7.3.

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v10.py [a|b|c]

Part A (R7.2), RQ1 core, endpoint D, 15 and 20 protocols, model of power_sim_v8.py:
- Calibration stream: the Holm level on exact nulls; the interval multiplier on exact nulls; the equivalence
  multiplier on data GENERATED with a true difference of exactly +0.05 and exactly -0.05 in every study
  (no location shift). The equivalence decision is a family decision: equivalence is claimed for each
  configuration whose two one-sided tests both pass; family false equivalence = any claim at a boundary.
- Independent validation stream: family-wise error (nulls), worst coverage (nulls and alternatives),
  family false equivalence at both boundaries, then power, interval half-width and equivalence power of
  the SELECTED procedure (calibrated level and multipliers) for alternatives and the exact null.
Part B (R7.3), paper 2: one common outcome in every arm, retention or reproduction of the attributable
  vulnerability. Ordinary wrong assertions may still change vulnerability retention (general test
  obedience); security-related ones may change it more. The tested quantity is the probability-scale
  three-way contrast (security interaction minus ordinary interaction, both on vulnerability retention),
  estimated per function and tested by a t-test across protocol means. Zero-contrast scenarios include
  equal nonzero interactions. Effect-based allocation: functions needed for power 0.80 at a security-
  specific contrast of 1.0 and of 1.5 on the logit scale.
Part C (R7.1), seeded validation precision: half-width of the 95% interval for the paired recall difference
  (agent-implementation seed detected minus human-implementation seed detected), by number of matched
  pairs, discordance rate and a design effect for clustering by protocol.
"""
import sys
import numpy as np
from scipy import stats
import power_sim_v8 as v8

RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}


def holm(p, a):
    return v8.holm(p, a)


def part_a():
    alphas = [0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02]
    cs = np.round(np.arange(1.0, 1.81, 0.02), 2)
    for P in (15, 20):
        q975, q95 = stats.t.ppf(0.975, P - 1), stats.t.ppf(0.95, P - 1)
        def gen(rng, target, n):
            """Null and upper boundary: agents' group V rate 0.6, human group N rate 0.02 or 0.05.
            Lower boundary (-0.05): reachable only if agents avoid more human bugs and humans have more
            group N flaws, so agents' group V rate 0.2 and human group N rate 0.12 or 0.15."""
            out = []
            aV, hNs = ((0.2, (0.12, 0.15)) if target < 0 else (0.6, (0.02, 0.05)))
            for rc in RECALLS.values():
                for hN in hNs:
                    add = None if target == 0 else ("target", target)
                    out.append(v8.run(P, ([aV] * 2, add, 0.9, hN), rc, n, rng, "D"))
            return out
        rngA, rngB = np.random.default_rng(9009 + P), np.random.default_rng(9109 + P)
        calN, calHi, calLo = gen(rngA, 0, 600), gen(rngA, 0.05, 600), gen(rngA, -0.05, 600)
        def fwer(data, a):
            return max(np.mean([holm(x, a).any() for x in 2 * stats.t.sf(np.abs(d) / se, P - 1)]) for d, se, tr in data)
        def cover(data, c):
            return min((((d - c * q975 * se) <= tr) & (tr <= d + c * q975 * se)).mean(0).min() for d, se, tr in data)
        def fam_false_eq(data, c):
            return max(((d - c * q95 * se > -0.05) & (d + c * q95 * se < 0.05)).any(1).mean() for d, se, tr in data)
        def eq_power(data, c):
            return min(((d - c * q95 * se > -0.05) & (d + c * q95 * se < 0.05)).mean(0).min() for d, se, tr in data)
        a_star = max([a for a in alphas if fwer(calN, a) <= 0.05], default=0.02)
        c_ci = min([c for c in cs if cover(calN + calHi + calLo, c) >= 0.95], default=cs[-1])
        c_eq = min([c for c in cs if max(fam_false_eq(calHi, c), fam_false_eq(calLo, c)) <= 0.05], default=cs[-1])
        valN, valHi, valLo = gen(rngB, 0, 600), gen(rngB, 0.05, 600), gen(rngB, -0.05, 600)
        n = 600; mc = lambda x: 1.96 * np.sqrt(x * (1 - x) / n)
        fw, cv = fwer(valN, a_star), cover(valN + valHi + valLo, c_ci)
        fe = max(fam_false_eq(valHi, c_eq), fam_false_eq(valLo, c_eq))
        ep = eq_power(valN, c_eq)
        print(f"Part A, P={P}: calibrated (seed {9009 + P}): Holm level {a_star}, interval multiplier {c_ci}, family equivalence multiplier {c_eq}")
        print(f"  validation (seed {9109 + P}, 6 scenarios x 600 studies per condition): worst FWER {fw:.3f} (+/-{mc(fw):.3f});"
              f" worst coverage at 0 and at +/-0.05 {cv:.3f} (+/-{mc(cv):.3f}); worst family false equivalence at +/-0.05 {fe:.3f} (+/-{mc(fe):.3f});"
              f" equivalence power at a true difference of 0, worst scenario {ep:.2f}")
        # power and widths of the selected procedure for alternatives
        rngC = np.random.default_rng(9209 + P)
        rows = []
        for rname, rc in RECALLS.items():
            for hN, add in ((0.02, 0.05), (0.02, 0.10), (0.05, 0.10)):
                d0, se, tr = v8.run(P, ([0.6] * 2, [add] * 2, 0.9, hN), rc, 400, rngC, "D")
                p = 2 * stats.t.sf(np.abs(d0) / se, P - 1)
                pw = np.array([holm(x, a_star) for x in p]).mean(0).min()
                rows.append((rname, hN, add, tr.mean(), pw, (c_ci * q975 * se).mean()))
        for r in rows:
            print(f"  selected procedure: recall {r[0]:13s} hN {r[1]:.2f} added N rate {r[2]:+.2f}: true difference {r[3]:+.3f},"
                  f" minimum configuration power {r[4]:.2f}, mean 95% half-width {r[5]:.3f}")


def contrast_power(nf, npr, d_sec, d_ord, rng, sims=1000, k=3, slope_sd=0.75):
    prot = np.arange(nf) % npr
    rej = 0
    for _ in range(sims):
        u = rng.normal(0, 1.5, nf) + rng.normal(0, 0.5, npr)[prot]
        est = np.zeros(nf)
        for sign, inter in ((1, d_sec), (-1, d_ord)):
            it = inter + rng.normal(0, slope_sd, nf)
            m = {}
            for t in (0, 1):            # assertion wrong (1) or correct (0)
                for x in (0, 1):        # execution of repository tests permitted
                    eta = -0.85 + u + 0.5 * t - 0.5 * x + it * t * x
                    m[t, x] = rng.binomial(k, 1 / (1 + np.exp(-eta))) / k     # vulnerability retained
            est += sign * ((m[1, 1] - m[1, 0]) - (m[0, 1] - m[0, 0]))
        pm = np.array([est[prot == j].mean() for j in range(npr)])
        t = pm.mean() / (pm.std(ddof=1) / np.sqrt(npr))
        rej += 2 * stats.t.sf(abs(t), npr - 1) < 0.05
    return rej / sims


def part_b():
    rng = np.random.default_rng(9309)
    print("Part B, paper 2: outcome in every arm = vulnerability retained or reproduced; probability-scale three-way contrast;")
    print("  t-test across 20 protocol means, alpha 0.05, function-specific interactions (sd 0.75), 1,000 studies per row")
    for nf in (40, 80, 120, 160):
        for d_sec, d_ord in ((0.0, 0.0), (1.0, 1.0), (1.5, 1.5), (1.0, 0.0), (1.5, 0.5), (1.5, 0.0), (2.0, 1.0)):
            print(f"  functions {nf:3d}: security interaction {d_sec}, ordinary interaction {d_ord}: rejection rate {contrast_power(nf, 20, d_sec, d_ord, rng):.3f}")


def part_c():
    print("Part C, seeded validation: 95% half-width of the paired recall difference = 1.96 * sqrt(deff * (delta - d^2) / n)")
    print("  n matched pairs (one seed in the human implementation, the same seed in an agent implementation of the same function)")
    print("  delta = probability that exactly one of the pair is detected; d = true recall difference (0.1); deff = 1.5 for clustering")
    for delta in (0.2, 0.3, 0.4):
        cells = []
        for n in (60, 120, 240, 480):
            hw = 1.96 * np.sqrt(1.5 * (delta - 0.1 ** 2) / n)
            cells.append(f"n={n}: {hw:.3f}")
        print(f"  delta {delta}: " + ", ".join(cells))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "abc"
    if "c" in which: part_c()
    if "b" in which: part_b()
    if "a" in which: part_a()
