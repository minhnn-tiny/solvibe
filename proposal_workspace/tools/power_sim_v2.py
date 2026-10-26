"""Power simulation for the proposal, version 2. It replaces tools/power_sim.py, whose "true" difference
used conditional rather than marginal rates (Peer B, round 1, point N1).

Run: uv run --with numpy --with statsmodels python tools/power_sim_v2.py
RQ1: agent-minus-human difference D = pi*(aV - hV) + (1-pi)*(aN - hN) with hV = 1.
  Intercepts are calibrated so that the MARGINAL rates (averaged over protocol and function random
  effects) equal aV, aN and hN. Test: two-stage cluster bootstrap (protocols, then functions within
  them), percentile interval at level 1 - 0.05/6 (Holm's strictest step for six configurations).
RQ2: within-function 2x2 (fault-enforcing tests present or corrected, x test execution off or on).
  Test: logistic regression with the four cells and their interaction, standard errors clustered by
  function, Wald test of the interaction at alpha = 0.05. Effects are on the logit scale, conditional
  on the function.
Both report the rejection rate under the null, to check the tests keep their level.
"""
import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(20261021)
expit = lambda x: 1 / (1 + np.exp(-x))
GH_X, GH_W = np.polynomial.hermite_e.hermegauss(60)   # nodes for E[f(Z)], Z ~ N(0, 1)
GH_W = GH_W / GH_W.sum()


def calibrate(marginal, sd):
    """Intercept b with E[expit(b + sd * Z)] = marginal."""
    lo, hi = -20.0, 20.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if (GH_W * expit(mid + sd * GH_X)).sum() < marginal:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def rq1(P, nv, nn, k, pi, aV, aN, hN, sdp, sdf, level, sims=400, boots=1000):
    sd = np.hypot(sdp, sdf)
    bV, bN, bH = calibrate(aV, sd), calibrate(aN, sd), calibrate(hN, sdp)
    rej = 0
    for _ in range(sims):
        up = rng.normal(0, sdp, (P, 1))
        yv = rng.binomial(k, expit(bV + up + rng.normal(0, sdf, (P, nv)))) / k
        yn = rng.binomial(k, expit(bN + up + rng.normal(0, sdf, (P, nn)))) / k
        yh = rng.binomial(1, expit(bH + up + np.zeros((P, nn))))
        # two-stage bootstrap: protocols with replacement, then functions within each drawn protocol
        pidx = rng.integers(0, P, (boots, P))
        fv = rng.integers(0, nv, (boots, P, nv))
        fn = rng.integers(0, nn, (boots, P, nn))
        mv = yv[pidx[..., None], fv].mean(axis=(1, 2))
        mn = yn[pidx[..., None], fn].mean(axis=(1, 2))
        mh = yh[pidx[..., None], fn].mean(axis=(1, 2))
        d = pi * (mv - 1) + (1 - pi) * (mn - mh)
        lo, hi = np.quantile(d, [(1 - level) / 2, 1 - (1 - level) / 2])
        rej += (lo > 0) or (hi < 0)
    return rej / sims, pi * (aV - 1) + (1 - pi) * (aN - hN)


def rq2(nf, k, base, e_tests, e_exec, inter, sdf, alpha=0.05, sims=400):
    rej = 0
    cells = [(t, e) for t in (0, 1) for e in (0, 1)]
    X = np.array([[1, t, e, t * e] for t, e in cells for _ in range(k)] * nf, float)
    groups = np.repeat(np.arange(nf), 4 * k)
    for _ in range(sims):
        u = np.repeat(rng.normal(0, sdf, nf), 4 * k)
        eta = base + X[:, 1] * e_tests + X[:, 2] * e_exec + X[:, 3] * inter + u
        y = rng.binomial(1, expit(eta))
        try:
            fit = sm.GLM(y, X, family=sm.families.Binomial()).fit(cov_type="cluster", cov_kwds={"groups": groups})
            rej += fit.pvalues[3] < alpha
        except Exception:
            pass   # separation in a tiny sample: count as no rejection
    return rej / sims


if __name__ == "__main__":
    assert abs((GH_W * expit(calibrate(0.15, 2.0) + 2.0 * GH_X)).sum() - 0.15) < 1e-6
    level = 1 - 0.05 / 6
    pi, aV, hN = 0.10, 0.6, 0.02
    null_aN = hN + pi * (1 - aV) / (1 - pi)          # makes D = 0
    print("RQ1: marginal rates; bootstrap interval at 1 - 0.05/6; 2 group V and 4 group N functions per protocol; 3 runs")
    print("protocols  aN     hN    true D   sd(prot,fun)  rejection rate")
    for P in (25, 30, 40):
        for aN, h in ((null_aN, hN), (0.10, 0.02), (0.15, 0.02), (0.15, 0.05)):
            for sdp, sdf in ((0.5, 1.5), (1.0, 2.0)):
                r, d = rq1(P, 2, 4, 3, pi, aV, aN, h, sdp, sdf, level)
                print(f"{P:9d}  {aN:.3f}  {h:.2f}  {d:+.3f}   ({sdp},{sdf})      {r:.2f}")
    print()
    print("RQ2: interaction of tests present x test execution, logistic, cluster-robust by function, alpha 0.05, 3 runs per cell")
    print("functions  interaction(logit)  rejection rate")
    for nf in (20, 30, 40):
        for inter in (0.0, 1.0, 1.5, 2.0):
            print(f"{nf:9d}  {inter:18.1f}  {rq2(nf, 3, -0.85, 0.5, -0.5, inter, 1.5):.2f}")
