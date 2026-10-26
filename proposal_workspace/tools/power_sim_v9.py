"""Validation of the core-study inference, and power for paper 2's matched contrast (version 9).

Run: uv run --offline --with numpy --with statsmodels python tools/power_sim_v9.py
Answers Peer B's round-6 concerns about v8: (1) the calibrated level is checked on an independent random
stream; (2) the 95% interval's coverage is checked; (3) equivalence is checked at the margin boundaries,
where the false-equivalence rate must stay at or below 0.05; (4) paper 2's revised contrast gets its own
power analysis.

Part A reuses the data model of tools/power_sim_v8.py (endpoint D, two configurations, three attempts, up to
2 V and 8 N functions per protocol, compilation and functional outcomes, recall by author and stratum,
protocol-by-author effect, exact offsetting nulls). Calibration: seed 6006; validation: seed 7007.
Part B, paper 2: each function has four arms crossed with two assertion types (security-related wrong
assertion, matched wrong assertion about ordinary behaviour); outcome "keeps or writes the vulnerable or wrong
behaviour". Contrast of interest: the tests-x-execution interaction for security assertions minus the same
interaction for ordinary assertions (a three-way contrast), estimated per function and tested with a
protocol-clustered t-test; function-level treatment effects vary (random slopes).
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8


def part_a():
    """Calibrate on one stream, validate on another: the Holm level, the interval multiplier c_ci (smallest
    with coverage >= 0.95 in every scenario), and the equivalence multiplier c_eq (smallest with
    false-equivalence <= 0.05 at both margin boundaries in every scenario). Boundaries use a location shift
    of the null estimates by +/-0.05 (an approximation that keeps the null's noise)."""
    alphas = [0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02]
    cs = np.round(np.arange(1.0, 1.61, 0.02), 2)
    recalls = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}
    for P in (15, 20):
        rngA, rngB = np.random.default_rng(6006 + P), np.random.default_rng(7007 + P)
        q975 = stats.t.ppf(0.975, P - 1); q95 = stats.t.ppf(0.95, P - 1)
        def stream(rng, n):
            out = []
            for rc in recalls.values():
                for hN in (0.02, 0.05):
                    out.append(v8.run(P, ([0.6] * 2, None, 0.9, hN), rc, n, rng, "D"))
            return out
        cal, val = stream(rngA, 600), stream(rngB, 600)
        def fwer(data, a):
            return max(np.mean([v8.holm(x, a).any() for x in 2 * stats.t.sf(np.abs(d) / se, P - 1)]) for d, se, tr in data)
        def cover(data, c):
            return min((((d - c * q975 * se) <= tr) & (tr <= d + c * q975 * se)).mean(0).min() for d, se, tr in data)
        def false_eq(data, c):
            return max(max(((d + sh - c * q95 * se > -0.05) & (d + sh + c * q95 * se < 0.05)).mean(0).max() for sh in (0.05, -0.05)) for d, se, tr in data)
        def eq_power(data, c):
            return min(((d - c * q95 * se > -0.05) & (d + c * q95 * se < 0.05)).mean(0).min() for d, se, tr in data)
        a_star = max([a for a in alphas if fwer(cal, a) <= 0.05], default=0.02)
        c_ci = min([c for c in cs if cover(cal, c) >= 0.95], default=cs[-1])
        c_eq = min([c for c in cs if false_eq(cal, c) <= 0.05], default=cs[-1])
        n = 600; mc = lambda x: 1.96 * np.sqrt(x * (1 - x) / n)
        print(f"Part A, P={P}: calibrated on seed {6006 + P}: alpha* = {a_star}, interval multiplier c_ci = {c_ci}, equivalence multiplier c_eq = {c_eq}")
        f, cv, fe, ep = fwer(val, a_star), cover(val, c_ci), false_eq(val, c_eq), eq_power(val, c_eq)
        print(f"  validation on seed {7007 + P} (6 null scenarios x 600 studies): max FWER {f:.3f} (+/-{mc(f):.3f}); min coverage {cv:.3f} (+/-{mc(cv):.3f});"
              f" max false-equivalence at +/-0.05 {fe:.3f} (+/-{mc(fe):.3f}); equivalence shown under the exact null in at least {ep:.2f} of studies")


def part_b(nf, nprot, k=3, d_sec=1.5, d_ord=0.0, slope_sd=0.75, sims=1000, rng=None):
    """Three-way contrast: (interaction for security assertions) - (interaction for ordinary assertions)."""
    rej = 0
    prot = np.arange(nf) % nprot
    for _ in range(sims):
        u = rng.normal(0, 1.5, nf) + rng.normal(0, 0.5, nprot)[prot]
        est = np.zeros(nf)
        for kind, inter in ((1, d_sec), (0, d_ord)):
            it = inter + rng.normal(0, slope_sd, nf)               # function-specific interaction
            m = {}
            for t in (0, 1):
                for x in (0, 1):
                    eta = -0.85 + u + 0.5 * t - 0.5 * x + it * t * x + rng.normal(0, slope_sd, nf) * t
                    m[t, x] = rng.binomial(k, 1 / (1 + np.exp(-eta))) / k
            did = (m[1, 1] - m[1, 0]) - (m[0, 1] - m[0, 0])
            est += did if kind == 1 else -did
        # protocol-clustered: average within protocols, t-test across protocols
        pm = np.array([est[prot == j].mean() for j in range(nprot)])
        t = pm.mean() / (pm.std(ddof=1) / np.sqrt(nprot))
        rej += 2 * stats.t.sf(abs(t), nprot - 1) < 0.05
    return rej / sims


if __name__ == "__main__":
    part_a()
    rng = np.random.default_rng(8008)
    print("Part B (paper 2): three-way contrast, protocol-clustered t-test, alpha 0.05, function slopes sd 0.75")
    for nf, npr in ((40, 20), (60, 20), (80, 20)):
        for d_sec, d_ord in ((0.0, 0.0), (1.5, 0.0), (1.5, 0.75), (2.0, 0.5)):
            print(f"  functions {nf}, protocols {npr}, security interaction {d_sec}, ordinary interaction {d_ord}:"
                  f" rejection rate {part_b(nf, npr, d_sec=d_sec, d_ord=d_ord, rng=rng):.3f}")
