"""Power simulation, version 4. Addresses Peer B's round-2 audit of v2 and v3.

Run: uv run --with numpy --with statsmodels python tools/power_sim_v4.py [rq1|rq2]
(statsmodels is only used for its scipy dependency: scipy.optimize and scipy.stats.)

RQ1 (endpoint K, confirmed vulnerable compiled output per scheduled attempt)
- Six configurations. Function effects are partly shared across configurations (share gamma) and
  correlated with the human outcome (rho). Protocol effects are shared by everyone.
- Intercepts are calibrated by quadrature so each MARGINAL rate equals its target; the calibration is
  checked independently by a large Monte Carlo sample.
- The human rate in group V is a scenario parameter (hV), not fixed at 1.
- Uncertainty: protocols are the primary sampling units. The bootstrap resamples protocols only
  (ultimate-cluster variance), drawing P - 1 of P with replacement and rescaling as Rao and Wu do
  (equivalent here, with equal weights, to a factor sqrt(P / (P - 1)) on the bootstrap deviations).
  Functions within a drawn protocol are kept as they are, so within-protocol variation is not counted
  twice. Basic interval and centered two-sided p-value, as in proposal v3, section 6.3.
- Reported: rejection rates with Monte Carlo 95% intervals, family-wise error under partial nulls,
  coverage of the 95% interval for the pooled difference, and bias.
RQ2 (within-function 2 x 2: tests assert the bug or not, x execution of the repository suite or not)
- Model: logistic with a random intercept per function, fitted by maximum likelihood with
  Gauss-Hermite quadrature (30 nodes). Data are generated with protocol AND function effects, so the
  fitted model is deliberately simpler than the truth; the null check shows whether the test still
  holds its level.
- Test: likelihood-ratio test of the interaction against chi-square(1). The null rejection rate is
  reported for every allocation; a parametric bootstrap per data set is too slow here, so the
  chi-square calibration is checked by simulation instead.
- Natural and injected strata are separate. The primary family is Holm over the two injected-stratum
  interactions (writing and repair); the natural stratum is reported with its own power.
Fit failures are counted and reported; they stay in the denominator as non-rejections.
"""
import sys
import numpy as np
from scipy import optimize, stats

rng = np.random.default_rng(20261021)
expit = lambda x: 1 / (1 + np.exp(-x))
GX, GW = np.polynomial.hermite_e.hermegauss(60)
GW = GW / GW.sum()


def calibrate(p, sd):
    lo, hi = -25.0, 25.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if (GW * expit(mid + sd * GX)).sum() < p else (lo, mid)
    return (lo + hi) / 2


def mc_ci(x, n):
    h = 1.96 * np.sqrt(max(x * (1 - x), 1e-9) / n)
    return f"{x:.2f} [{max(0, x - h):.2f}, {min(1, x + h):.2f}]"


def holm(p, alpha=0.05):
    rej = np.zeros(len(p), bool)
    for rank, i in enumerate(np.argsort(p)):
        if p[i] <= alpha / (len(p) - rank):
            rej[i] = True
        else:
            break
    return rej


# ---------------------------------------------------------------- RQ1
def rq1(P, nv, nn, k, pi, aV, aN, hV, hN, sdp, sdf, rho, gamma, sims=400, boots=999):
    C = len(aV)
    sd = np.hypot(sdp, sdf)
    bV = np.array([calibrate(a, sd) for a in aV])
    bN = np.array([calibrate(a, sd) for a in aN])
    bHV, bHN = calibrate(hV, sd), calibrate(hN, sd)
    true_c = pi * (np.array(aV) - hV) + (1 - pi) * (np.array(aN) - hN)
    true_pool = true_c.mean()
    scale = np.sqrt(P / (P - 1))
    rej_c = np.zeros(C)
    fwer = cover = pooled_rej = 0
    bias = []
    for _ in range(sims):
        up = rng.normal(0, sdp, (P, 1))
        def fun(n):
            shared = rng.normal(0, sdf, (P, n))
            own = rng.normal(0, sdf, (C, P, n))
            human = rho * shared + np.sqrt(1 - rho**2) * rng.normal(0, sdf, (P, n))
            agent = np.sqrt(gamma) * shared[None] + np.sqrt(1 - gamma) * own
            return agent, human
        av, hv = fun(nv)
        an, hn = fun(nn)
        yv = rng.binomial(k, expit(bV[:, None, None] + up[None] + av)) / k     # C x P x nv
        yn = rng.binomial(k, expit(bN[:, None, None] + up[None] + an)) / k
        yhv = rng.binomial(1, expit(bHV + up + hv))
        yhn = rng.binomial(1, expit(bHN + up + hn))
        # per-protocol contributions (equal weights): difference per protocol and configuration
        dp = pi * (yv.mean(2) - yhv.mean(1)) + (1 - pi) * (yn.mean(2) - yhn.mean(1))   # C x P
        d0 = dp.mean(1)
        idx = rng.integers(0, P, (boots, P - 1))
        db = dp[:, idx].mean(2)                         # C x boots
        e = (db - d0[:, None]) * scale
        p = (1 + (np.abs(e) >= np.abs(d0)[:, None]).sum(1)) / (boots + 1)
        r = holm(p)
        rej_c += r
        fwer += r[true_c == 0].any()
        ep = e.mean(0)
        dpool = d0.mean()
        pooled_rej += (1 + (np.abs(ep) >= abs(dpool)).sum()) / (boots + 1) < 0.05
        lo, hi = dpool - np.quantile(ep, 0.975), dpool - np.quantile(ep, 0.025)
        cover += lo <= true_pool <= hi
        bias.append(dpool - true_pool)
    return true_c, rej_c / sims, pooled_rej / sims, fwer / sims, cover / sims, float(np.mean(bias)), sims


def run_rq1():
    # independent check of the calibration with a large Monte Carlo sample
    z = rng.normal(0, 1, 2_000_000)
    for p, sd in ((0.15, np.hypot(0.5, 1.5)), (0.02, np.hypot(1.0, 2.0))):
        mc = expit(calibrate(p, sd) + sd * z).mean()
        assert abs(mc - p) < 0.002, (p, sd, mc)
    pi, hN = 0.10, 0.02
    print("RQ1. 6 configurations, 3 attempts, nV = 2 per protocol. Rejection rates with Monte Carlo 95% intervals.")
    print("P  nN  hV   rho gamma sd(p,f)  scenario             per-config Holm power (mean over configs)   pooled power        FWER  coverage  bias")
    for P, nn in ((25, 8), (30, 8), (30, 12)):
        for hV in (1.0, 0.9):
            nullN = hN + pi * (hV - 0.6) / (1 - pi)
            scen = {"all null": [nullN] * 6, "all +0.077-ish": [nullN + 0.0855] * 6,
                    "half null": [nullN] * 3 + [nullN + 0.0855] * 3}
            for rho, gamma in ((0.3, 1.0), (0.6, 0.5)):
                for sdp, sdf in ((0.5, 1.5), (1.0, 2.0)):
                    for name, aN in scen.items():
                        t, rc, pr, fw, cov, b, n = rq1(P, 2, nn, 3, pi, [0.6] * 6, aN, hV, hN, sdp, sdf, rho, gamma)
                        print(f"{P:2d} {nn:3d} {hV:.1f}  {rho:.1f}  {gamma:.1f}  ({sdp},{sdf})  {name:16s} "
                              f"true {t.mean():+.3f}  {mc_ci(rc[t != 0].mean() if (t != 0).any() else 0.0, n):18s}  "
                              f"{mc_ci(pr, n):18s}  {fw:.2f}  {cov:.2f}  {b:+.4f}")


# ---------------------------------------------------------------- RQ2
GHX, GHW = np.polynomial.hermite_e.hermegauss(30)
GHW = GHW / GHW.sum()


def nll(theta, X, y, g, nf):
    beta, sig = theta[:-1], np.exp(theta[-1])
    eta = (X @ beta)[:, None] + sig * GHX[None, :]               # obs x nodes
    ll_obs = y[:, None] * eta - np.logaddexp(0, eta)
    ll_fun = np.zeros((nf, len(GHX)))
    np.add.at(ll_fun, g, ll_obs)
    m = ll_fun.max(1, keepdims=True)
    return -(m[:, 0] + np.log((np.exp(ll_fun - m) * GHW).sum(1))).sum()


def lrt(X, y, g, nf):
    try:
        full = optimize.minimize(nll, np.zeros(X.shape[1] + 1), args=(X, y, g, nf), method="BFGS")
        red = optimize.minimize(nll, np.zeros(X.shape[1]), args=(X[:, :-1], y, g, nf), method="BFGS")
        if not (np.isfinite(full.fun) and np.isfinite(red.fun)):
            return None
        return stats.chi2.sf(max(0.0, 2 * (red.fun - full.fun)), 1)
    except Exception:
        return None


def rq2_data(nf, nprot, k, base, e_t, e_x, inter, sdp, sdf):
    prot = np.arange(nf) % nprot
    up = rng.normal(0, sdp, nprot)[prot]
    uf = rng.normal(0, sdf, nf)
    rows, y, g = [], [], []
    for f in range(nf):
        for t in (0, 1):
            for x in (0, 1):
                eta = base + e_t * t + e_x * x + inter * t * x + up[f] + uf[f]
                for _ in range(k):
                    rows.append((1, t, x, t * x)); y.append(rng.random() < expit(eta)); g.append(f)
    return np.array(rows, float), np.array(y, float), np.array(g)


def rq2(nf, nprot, inter, sims=300, k=3, base=-0.85, e_t=0.5, e_x=-0.5, sdp=0.5, sdf=1.5):
    rej = fails = 0
    for _ in range(sims):
        X, y, g = rq2_data(nf, nprot, k, base, e_t, e_x, inter, sdp, sdf)
        p = lrt(X, y, g, nf)
        if p is None:
            fails += 1
        else:
            rej += p < 0.05
    return rej / sims, fails, sims


def rq2_family(nf, nprot, inter_w, inter_r, sims=200, k=3):
    """Holm over the two injected-stratum interactions (writing, repair), as the primary family."""
    hits = np.zeros(2); fails = 0
    for _ in range(sims):
        ps = []
        for inter in (inter_w, inter_r):
            X, y, g = rq2_data(nf, nprot, k, -0.85, 0.5, -0.5, inter, 0.5, 1.5)
            p = lrt(X, y, g, nf)
            fails += p is None
            ps.append(1.0 if p is None else p)
        hits += holm(np.array(ps))
    return hits / sims, fails, sims


def run_rq2():
    print("RQ2. Random-intercept logistic model by quadrature; likelihood-ratio test of the interaction, alpha 0.05.")
    print("Data have protocol (sd 0.5) and function (sd 1.5) effects; 3 attempts per cell.")
    print("functions protocols interaction  rejection rate [MC 95%]   fit failures")
    for nf, nprot in ((10, 5), (20, 10), (30, 15), (40, 20)):
        for inter in (0.0, 1.0, 1.5, 2.0):
            r, f, n = rq2(nf, nprot, inter)
            print(f"{nf:9d} {nprot:9d} {inter:11.1f}  {mc_ci(r, n):24s} {f}/{n}")
    print()
    print("Primary family: Holm over writing and repair interactions, injected stratum.")
    print("functions  interaction(write, repair)  power write  power repair  fit failures")
    for nf in (30, 40):
        for iw, ir in ((1.5, 1.5), (2.0, 1.0), (0.0, 1.5)):
            h, f, n = rq2_family(nf, nf // 2, iw, ir)
            print(f"{nf:9d}  ({iw}, {ir}){'':16s}  {mc_ci(h[0], n):18s} {mc_ci(h[1], n):18s} {f}/{2*n}")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("rq1", "both"):
        run_rq1()
    if which in ("rq2", "both"):
        run_rq2()
