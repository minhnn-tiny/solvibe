"""RQ1 calibration of the jackknife-t test, version 6 (answers Peer B's remaining concern in round 4).

Run: uv run --offline --with numpy --with statsmodels python tools/power_sim_v6.py
Same data model and estimator as tools/power_sim_v5.py (unequal frames, inclusion weights, six
configurations, protocols as primary sampling units), with only the delete-one-protocol jackknife and a
t(P - 1) reference.

Step 1, calibration (seed A): over a preregistered set of null scenarios, find the largest nominal
level alpha* (grid 0.050 down to 0.010) at which Holm's family-wise error is at most 0.05 in every
scenario, and the smallest interval multiplier c* (times the t(P - 1) 97.5% quantile) at which every
configuration's pointwise coverage is at least 0.95 in every scenario. The null set has two kinds:
equal rates in both strata, and offsetting nulls, where agents avoid human bugs in group V and add bugs
in group N in amounts that cancel at the expected frame share of group V.
Step 2, validation (seed B, independent draws): family-wise error and coverage at alpha* and c*, with
Monte Carlo 95% intervals.
Step 3, power at alpha* for the effect scenarios (seed B).
"""
import numpy as np
from scipy import stats

expit = lambda x: 1 / (1 + np.exp(-x))
GX, GW = np.polynomial.hermite_e.hermegauss(60)
GW = GW / GW.sum()
EPI = 4 / 79            # expected frame share of group V: E[2 + Poisson(2)] / (that + E[U(30, 120)])


def calibrate(p, sd):
    lo, hi = -25.0, 25.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if (GW * expit(mid + sd * GX)).sum() < p else (lo, mid)
    return (lo + hi) / 2


def holm_reject(p, alpha):
    rej = np.zeros(len(p), bool)
    for rank, i in enumerate(np.argsort(p)):
        if p[i] <= alpha / (len(p) - rank):
            rej[i] = True
        else:
            break
    return rej


def simulate(rng, P, aV, aN, hV, hN, sdp, sdf, rho, gamma, sims, k=3):
    """Returns per study: estimates d0 (sims x C), jackknife SEs, true differences (sims x C)."""
    C = len(aV)
    sd = np.hypot(sdp, sdf)
    bV = np.array([calibrate(a, sd) for a in aV]); bN = np.array([calibrate(a, sd) for a in aN])
    bHV, bHN = calibrate(hV, sd), calibrate(hN, sd)
    D0, SE, TRUE = np.zeros((sims, C)), np.zeros((sims, C)), np.zeros((sims, C))
    for s in range(sims):
        NV = 2 + rng.poisson(2, P); NN = rng.integers(30, 121, P)
        nv = np.minimum(2, NV); nn = np.full(P, 8)
        pi = NV.sum() / (NV + NN).sum()
        TRUE[s] = pi * (np.array(aV) - hV) + (1 - pi) * (np.array(aN) - hN)
        up = rng.normal(0, sdp, P)
        SV = np.zeros((C, P)); SN = np.zeros((C, P)); WV = np.zeros(P); WN = np.zeros(P)
        for p in range(P):
            for n, N, b, bh, S, W in ((nv[p], NV[p], bV, bHV, SV, WV), (nn[p], NN[p], bN, bHN, SN, WN)):
                shared = rng.normal(0, sdf, n)
                agent = np.sqrt(gamma) * shared + np.sqrt(1 - gamma) * rng.normal(0, sdf, (C, n))
                human = rho * shared + np.sqrt(1 - rho**2) * rng.normal(0, sdf, n)
                ya = rng.binomial(k, expit(b[:, None] + up[p] + agent)) / k
                yh = rng.binomial(1, expit(bh + up[p] + human))
                w = N / n
                S[:, p] = w * (ya - yh).sum(1); W[p] = w * n
        def est(mult):
            v = (SV * mult[..., None, :]).sum(-1) / (WV * mult).sum(-1)[..., None]
            m = (SN * mult[..., None, :]).sum(-1) / (WN * mult).sum(-1)[..., None]
            return pi * v + (1 - pi) * m
        D0[s] = est(np.ones(P))
        jk = est(1.0 - np.eye(P))
        SE[s] = np.sqrt((P - 1) / P * ((jk - jk.mean(0)) ** 2).sum(0))
    return D0, SE, TRUE


def grid():
    hN = 0.02
    for P in (25, 30):
        for hV in (1.0, 0.9):
            for rho, gamma in ((0.3, 1.0), (0.6, 0.5)):
                for sdp, sdf in ((0.5, 1.5), (1.0, 2.0)):
                    yield P, hV, hN, rho, gamma, sdp, sdf


def null_scenarios(hV, hN):
    off_aV = hV - 0.4
    off_aN = hN + EPI * 0.4 / (1 - EPI)        # cancels at the expected frame share
    return {"equal": ([hV] * 6, [hN] * 6),
            "offsetting": ([off_aV] * 6, [off_aN] * 6),
            "mixed": ([hV] * 3 + [off_aV] * 3, [hN] * 3 + [off_aN] * 3)}


def fwer_and_cov(D0, SE, TRUE, P, alpha, c):
    p = 2 * stats.t.sf(np.abs(D0) / SE, P - 1)
    fw = np.mean([holm_reject(pi_, alpha).any() for pi_ in p])
    q = c * stats.t.ppf(0.975, P - 1)
    cov = ((D0 - q * SE <= TRUE) & (TRUE <= D0 + q * SE)).mean(0)
    return fw, cov


def mc(x, n):
    h = 1.96 * np.sqrt(max(x * (1 - x), 1e-9) / n)
    return f"{x:.3f} [{max(0, x - h):.3f}, {min(1, x + h):.3f}]"


if __name__ == "__main__":
    alphas = np.round(np.arange(0.050, 0.009, -0.005), 3)
    mults = np.round(np.arange(1.00, 1.31, 0.02), 2)
    rngA, rngB = np.random.default_rng(1001), np.random.default_rng(2002)
    nsim = 1000
    # Step 1: calibration on seed A
    worst_fw = {a: 0.0 for a in alphas}; worst_cov = {c: 1.0 for c in mults}
    for P, hV, hN, rho, gamma, sdp, sdf in grid():
        for name, (aV, aN) in null_scenarios(hV, hN).items():
            D0, SE, TRUE = simulate(rngA, P, aV, aN, hV, hN, sdp, sdf, rho, gamma, nsim)
            for a in alphas:
                worst_fw[a] = max(worst_fw[a], fwer_and_cov(D0, SE, TRUE, P, a, 1.0)[0])
            for c in mults:
                worst_cov[c] = min(worst_cov[c], fwer_and_cov(D0, SE, TRUE, P, 0.05, c)[1].min())
    a_star = max([a for a in alphas if worst_fw[a] <= 0.05], default=alphas[-1])
    c_star = min([c for c in mults if worst_cov[c] >= 0.95], default=mults[-1])
    print("Step 1 (calibration, seed A, 1000 studies per scenario, 48 null scenarios):")
    print("  worst family-wise error by nominal alpha:", {float(a): round(worst_fw[a], 3) for a in alphas})
    print("  worst pointwise coverage by multiplier:", {float(c): round(worst_cov[c], 3) for c in mults})
    print(f"  chosen alpha* = {a_star}, interval multiplier c* = {c_star}")
    # Step 2: validation on seed B
    print("Step 2 (validation, seed B, independent draws, 1000 studies per scenario):")
    vfw, vcov = [], []
    for P, hV, hN, rho, gamma, sdp, sdf in grid():
        for name, (aV, aN) in null_scenarios(hV, hN).items():
            D0, SE, TRUE = simulate(rngB, P, aV, aN, hV, hN, sdp, sdf, rho, gamma, nsim)
            fw, cov = fwer_and_cov(D0, SE, TRUE, P, a_star, c_star)
            vfw.append(fw); vcov.append(cov.min())
    print(f"  family-wise error at alpha*: max {mc(max(vfw), nsim)}, mean {np.mean(vfw):.3f}")
    print(f"  pointwise coverage at c*: min {mc(min(vcov), nsim)}, mean {np.mean(vcov):.3f}")
    # Step 3: power at alpha* on seed B
    print("Step 3 (power at alpha*, seed B, 400 studies per scenario; minimum over affected configurations):")
    rows = []
    for P, hV, hN, rho, gamma, sdp, sdf in grid():
        for name, aNe in (("larger effect, half null", hN + 0.13), ("smaller effect, all six", hN + 0.06), ("middle effect, all six", hN + 0.09)):
            if name.startswith("larger"):
                aV, aN = [hV] * 3 + [0.6] * 3, [hN] * 3 + [aNe] * 3
            else:
                aV, aN = [0.6] * 6, [aNe] * 6
            D0, SE, TRUE = simulate(rngB, P, aV, aN, hV, hN, sdp, sdf, rho, gamma, 400)
            p = 2 * stats.t.sf(np.abs(D0) / SE, P - 1)
            rej = np.array([holm_reject(pi_, a_star) for pi_ in p]).mean(0)
            aff = TRUE.mean(0) != 0
            rows.append((name, P, TRUE.mean(0)[aff].mean(), rej[aff].min()))
    for name in ("larger effect, half null", "middle effect, all six", "smaller effect, all six"):
        for P in (25, 30):
            sel = [r for r in rows if r[0] == name and r[1] == P]
            print(f"  {name:26s} P={P}: true difference {min(r[2] for r in sel):+.3f} to {max(r[2] for r in sel):+.3f}; "
                  f"minimum configuration power {min(r[3] for r in sel):.2f} to {max(r[3] for r in sel):.2f}")
