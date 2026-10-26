"""Simulated power for the proposal's two main analyses.

Run: uv run --with numpy python tools/power_sim.py
RQ1: the weighted agent-minus-human difference D = pi*(aV-1) + (1-pi)*(aN-hN), estimated from a
stratified sample of functions within protocols, with a protocol-level jackknife standard error.
RQ2: a within-function 2x2 (fault-enforcing tests present or corrected, x execution off or on),
testing the interaction on function-level means.
All rates are on the logit scale with random effects for protocol and function, so runs of one
function are correlated (the pilot's intraclass correlation was 0.69 on 8 tasks).
"""
import numpy as np

rng = np.random.default_rng(20261021)
expit = lambda x: 1 / (1 + np.exp(-x))
logit = lambda p: np.log(p / (1 - p))


def sim_rq1(n_prot, nv_per, nn_per, k, pi, aV, aN, hN, sd_prot, sd_fun, alpha, reps=2000):
    """Power of a two-sided test of D = 0 for one agent configuration."""
    hits, ests = 0, []
    for _ in range(reps):
        dv, dn, dh = [], [], []
        for _p in range(n_prot):
            up = rng.normal(0, sd_prot)
            # agent: k runs per function; human: one version per group N function
            fv = expit(logit(aV) + up + rng.normal(0, sd_fun, nv_per))
            fn = expit(logit(aN) + up + rng.normal(0, sd_fun, nn_per))
            dv.append(rng.binomial(k, fv) / k)
            dn.append(rng.binomial(k, fn) / k)
            dh.append(rng.binomial(1, expit(logit(hN) + up), nn_per))
        dv, dn, dh = map(np.array, (dv, dn, dh))

        def est(mask):
            return pi * (dv[mask].mean() - 1) + (1 - pi) * (dn[mask].mean() - dh[mask].mean())

        full = np.ones(n_prot, bool)
        d = est(full)
        jack = np.array([est(np.arange(n_prot) != i) for i in range(n_prot)])
        se = np.sqrt((n_prot - 1) / n_prot * ((jack - jack.mean()) ** 2).sum())
        z = abs(d) / se if se > 0 else 0
        from math import erf, sqrt
        p = 2 * (1 - 0.5 * (1 + erf(z / sqrt(2))))
        hits += p < alpha
        ests.append(d)
    true = pi * (aV - 1) + (1 - pi) * (aN - hN)
    return hits / reps, true, float(np.mean(ests))


def sim_rq2(n_fun, k, base, eff_tests, eff_exec, eff_inter, sd_fun, alpha, reps=2000):
    """Power for the interaction in a within-function 2x2 with k runs per cell."""
    from math import erf, sqrt
    hits = 0
    for _ in range(reps):
        u = rng.normal(0, sd_fun, n_fun)
        cell = {}
        for t in (0, 1):          # 1 = fault-enforcing tests present
            for e in (0, 1):      # 1 = agent can execute tests
                eta = logit(base) + u + eff_tests * t + eff_exec * e + eff_inter * t * e
                cell[t, e] = rng.binomial(k, expit(eta)) / k
        dd = (cell[1, 1] - cell[1, 0]) - (cell[0, 1] - cell[0, 0])   # per-function interaction
        z = abs(dd.mean()) / (dd.std(ddof=1) / np.sqrt(n_fun))
        hits += 2 * (1 - 0.5 * (1 + erf(z / sqrt(2)))) < alpha
    return hits / reps


if __name__ == "__main__":
    assert abs(expit(logit(0.3)) - 0.3) < 1e-12
    # Holm across six configurations: the strictest step tests at 0.05 / 6.
    a6 = 0.05 / 6
    print("RQ1: power for one configuration at alpha = 0.05/6 (Holm, worst step)")
    print("protocols nV/prot nN/prot  aN   hN   sd_prot sd_fun   true D   power")
    for n_prot, nv, nn in ((25, 2, 4), (30, 2, 4), (40, 2, 4)):
        for aN, hN in ((0.10, 0.02), (0.15, 0.02), (0.15, 0.05)):
            for sd_prot, sd_fun in ((0.5, 1.5), (1.0, 2.0)):
                pw, true, _ = sim_rq1(n_prot, nv, nn, 3, 0.10, 0.6, aN, hN, sd_prot, sd_fun, a6, reps=600)
                print(f"{n_prot:9d} {nv:6d} {nn:7d}  {aN:.2f} {hN:.2f}   {sd_prot:.1f}     {sd_fun:.1f}   {true:+.3f}   {pw:.2f}")
    print()
    print("RQ2: power for the tests-x-execution interaction, alpha = 0.05, 3 runs per cell")
    print("functions  base  interaction(logit)  power")
    for n_fun in (10, 15, 20, 30):
        for inter in (1.0, 1.5, 2.0):
            pw = sim_rq2(n_fun, 3, 0.3, 0.5, -0.5, inter, 1.5, 0.05, reps=1000)
            print(f"{n_fun:9d}  0.30  {inter:18.1f}  {pw:.2f}")
