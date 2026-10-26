"""Power simulation, version 5. Fixes the issues Peer B found in v4 (round 3, R2 and R5).

Run: uv run --offline --with numpy --with statsmodels python tools/power_sim_v5.py [rq1|rq2]
(statsmodels only provides scipy here.)

RQ1, the declared procedure (proposal section 6.3):
- Unequal protocols: each has a group V frame of 2 + Poisson(2) functions and a group N frame of
  30 to 120 functions; up to 2 V (census if fewer) and 8 N functions are sampled per protocol.
  Function weight = frame size / sample size within its protocol and stratum. pi is the frame share
  of group V. Estimator: sum over strata of pi_s times the weighted mean of (agent mean - human).
- Bootstrap: protocols are the primary sampling units. Each replicate draws P - 1 protocols with
  replacement and recomputes the weighted estimator with the drawn multiplicities (Rao-Wu with
  m = P - 1; for this ratio estimator the P/(P-1) weight factor cancels, so no further scaling).
  Functions inside a drawn protocol are kept, which treats protocols as ultimate clusters.
- Two tests are compared for every configuration: (a) basic bootstrap interval and centered
  p-value; (b) bootstrap standard error with a t reference on P - 1 degrees of freedom. Holm across
  the six configurations for each.
- Reported per configuration: power, coverage of the 95% interval, and family-wise error, all with
  Monte Carlo 95% intervals.
RQ2, the declared model (proposal section 6.4):
- 40 functions in 20 protocols. The writing and the repair outcomes of a function share its protocol
  and function effects. Each outcome has 4 cells x 3 attempts.
- Model: logistic with random intercepts for protocol and for function (nested), fitted by maximum
  likelihood with nested Gauss-Hermite quadrature (12 x 12 nodes). Test: likelihood-ratio test of
  the interaction against chi-square(1).
- Convergence: a fit counts only if the optimizer reports success, the gradient norm is below
  1e-3, and the likelihood-ratio statistic is not negative (a negative one triggers a refit of the
  full model from the reduced estimates). Failed fits are counted and stay in the denominator.
- Family: Holm over the writing and repair interactions, with all-null, partial-null and
  alternative rows.
"""
import sys
import numpy as np
from scipy import optimize, stats

rng = np.random.default_rng(20261022)
expit = lambda x: 1 / (1 + np.exp(-x))
GX, GW = np.polynomial.hermite_e.hermegauss(60)
GW = GW / GW.sum()


def calibrate(p, sd):
    lo, hi = -25.0, 25.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if (GW * expit(mid + sd * GX)).sum() < p else (lo, mid)
    return (lo + hi) / 2


def ci(x, n):
    h = 1.96 * np.sqrt(max(x * (1 - x), 1e-9) / n)
    return f"{x:.2f} [{max(0, x - h):.2f},{min(1, x + h):.2f}]"


def holm(p, alpha=0.05):
    rej = np.zeros(len(p), bool)
    for rank, i in enumerate(np.argsort(p)):
        if p[i] <= alpha / (len(p) - rank):
            rej[i] = True
        else:
            break
    return rej


# ------------------------------------------------------------------ RQ1
def rq1(P, k, aV, aN, hV, hN, sdp, sdf, rho, gamma, sims=400, boots=999):
    C = len(aV)
    sd = np.hypot(sdp, sdf)
    bV = np.array([calibrate(a, sd) for a in aV]); bN = np.array([calibrate(a, sd) for a in aN])
    bHV, bHN = calibrate(hV, sd), calibrate(hN, sd)
    res = {m: {"rej": np.zeros(C), "cov": np.zeros(C), "fw": 0} for m in ("basic", "t", "jk")}
    res["true"] = np.zeros(C)
    null = (np.abs(np.array(aV) - hV) < 1e-12) & (np.abs(np.array(aN) - hN) < 1e-12)
    for _ in range(sims):
        NV = 2 + rng.poisson(2, P); NN = rng.integers(30, 121, P)
        nv = np.minimum(2, NV); nn = np.full(P, 8)
        pi = NV.sum() / (NV + NN).sum()
        true = pi * (np.array(aV) - hV) + (1 - pi) * (np.array(aN) - hN)
        up = rng.normal(0, sdp, P)
        # per-protocol weighted sums: S_s[c, p] = sum_i w_i (agent - human), W_s[p] = sum_i w_i
        SV = np.zeros((C, P)); SN = np.zeros((C, P)); WV = np.zeros(P); WN = np.zeros(P)
        for p in range(P):
            for n, N, b, bh, S, W in ((nv[p], NV[p], bV, bHV, SV, WV), (nn[p], NN[p], bN, bHN, SN, WN)):
                shared = rng.normal(0, sdf, n)
                own = rng.normal(0, sdf, (C, n))
                agent = np.sqrt(gamma) * shared + np.sqrt(1 - gamma) * own
                human = rho * shared + np.sqrt(1 - rho**2) * rng.normal(0, sdf, n)
                ya = rng.binomial(k, expit(b[:, None] + up[p] + agent)) / k
                yh = rng.binomial(1, expit(bh + up[p] + human))
                w = N / n
                S[:, p] = w * (ya - yh).sum(1); W[p] = w * n
        def est(mult):            # mult: (..., P) multiplicities
            v = (SV * mult[..., None, :]).sum(-1) / (WV * mult).sum(-1)[..., None]
            m = (SN * mult[..., None, :]).sum(-1) / (WN * mult).sum(-1)[..., None]
            return pi * v + (1 - pi) * m
        d0 = est(np.ones(P))                                   # C
        draws = rng.integers(0, P, (boots, P - 1))
        mult = np.zeros((boots, P)); np.add.at(mult, (np.arange(boots)[:, None], draws), 1)
        db = est(mult)                                         # boots x C
        e = db - d0
        # (a) basic bootstrap
        p_basic = (1 + (np.abs(e) >= np.abs(d0)).sum(0)) / (boots + 1)
        lo_b, hi_b = d0 - np.quantile(e, 0.975, 0), d0 - np.quantile(e, 0.025, 0)
        # (b) bootstrap standard error with t reference on P - 1 degrees of freedom
        se = db.std(0, ddof=1)
        p_t = 2 * stats.t.sf(np.abs(d0) / se, P - 1)
        q = stats.t.ppf(0.975, P - 1)
        lo_t, hi_t = d0 - q * se, d0 + q * se
        # (c) delete-one-protocol jackknife standard error with t reference on P - 1 degrees of freedom
        jk = est(1.0 - np.eye(P))                              # P x C
        se_j = np.sqrt((P - 1) / P * ((jk - jk.mean(0)) ** 2).sum(0))
        p_j = 2 * stats.t.sf(np.abs(d0) / se_j, P - 1)
        lo_j, hi_j = d0 - q * se_j, d0 + q * se_j
        res["true"] += true
        for name, pv, lo, hi in (("basic", p_basic, lo_b, hi_b), ("t", p_t, lo_t, hi_t), ("jk", p_j, lo_j, hi_j)):
            r = holm(pv)
            res[name]["rej"] += r
            res[name]["cov"] += (lo <= true) & (true <= hi)
            res[name]["fw"] += r[null].any()
    return res, sims


def run_rq1():
    z = rng.normal(0, 1, 2_000_000)
    for p, sd in ((0.15, np.hypot(0.5, 1.5)), (0.02, np.hypot(1.0, 2.0)), (0.9, np.hypot(1.0, 2.0))):
        assert abs(expit(calibrate(p, sd) + sd * z).mean() - p) < 0.002
    hN = 0.02
    print("RQ1 (declared procedure). 6 configurations, 3 attempts; up to 2 V and 8 N functions per protocol; unequal frames.")
    print("Null configurations equal the human in both strata (aV = hV, aN = hN). Effect configurations: aV = 0.6 with hV,")
    print("and aN = hN + 0.13 (added vulnerabilities outweigh avoided ones). Each cell: rejection or coverage [MC 95%], 400 studies.")
    for P in (25, 30):
        for hV in (1.0, 0.9):
            eff_aV = 0.6
            scen = {"all null": ([hV] * 6, [hN] * 6),
                    "half null": ([hV] * 3 + [eff_aV] * 3, [hN] * 3 + [hN + 0.13] * 3),
                    "all effect": ([eff_aV] * 6, [hN + 0.13] * 6),
                    "small effect": ([eff_aV] * 6, [hN + 0.06] * 6)}
            for rho, gamma in ((0.3, 1.0), (0.6, 0.5)):
                for sdp, sdf in ((0.5, 1.5), (1.0, 2.0)):
                    for name, (aV, aN) in scen.items():
                        res, n = rq1(P, 3, aV, aN, hV, hN, sdp, sdf, rho, gamma)
                        for m in ("basic", "t", "jk"):
                            rr = res[m]["rej"] / n; cv = res[m]["cov"] / n; fw = res[m]["fw"] / n
                            print(f"P={P} hV={hV} rho={rho} gamma={gamma} sd=({sdp},{sdf}) {name:10s} {m:5s} true D {res['true'].max() / n:+.3f} "
                                  f"power/rej per config: {' '.join(f'{x:.2f}' for x in rr)} | "
                                  f"min power {ci(rr[3:].min() if name == 'half null' else rr.min(), n)} | "
                                  f"coverage min {ci(cv.min(), n)} | FWER {ci(fw, n)}")


# ------------------------------------------------------------------ RQ2
Q = 12
HX, HW = np.polynomial.hermite_e.hermegauss(Q)
LW = np.log(HW / HW.sum())


def nll(theta, X, y, fun, prot, nf, npr):
    beta = theta[:4] if X.shape[1] == 4 else theta[:3]
    sp, sf = np.exp(theta[-2]), np.exp(theta[-1])
    eta = (X @ beta)[:, None, None] + sp * HX[None, :, None] + sf * HX[None, None, :]   # obs x Qp x Qf
    ll = y[:, None, None] * eta - np.logaddexp(0, eta)
    lf = np.zeros((nf, Q, Q)); np.add.at(lf, fun, ll)                  # function x Qp x Qf
    lf = np.logaddexp.reduce(lf + LW[None, None, :], axis=2)           # integrate function effect
    lp = np.zeros((npr, Q)); np.add.at(lp, prot, lf)                   # protocol x Qp
    return -np.logaddexp.reduce(lp + LW[None, :], axis=1).sum()


def fit(X, y, fun, prot, nf, npr, start):
    """L-BFGS-B with log standard deviations bounded to [-7, 3], so a variance at the boundary
    (a protocol effect of about zero) is a valid estimate, not a failure. Converged means the optimizer
    reports success and every free coordinate has a gradient below 1e-3; one restart from a
    perturbed start is allowed."""
    bounds = [(None, None)] * (len(start) - 2) + [(-7, 3), (-7, 3)]
    for attempt in range(2):
        x0 = start if attempt == 0 else start + rng.normal(0, 0.3, len(start))
        r = optimize.minimize(nll, x0, args=(X, y, fun, prot, nf, npr), method="L-BFGS-B", bounds=bounds,
                              options={"maxiter": 1000, "ftol": 1e-12, "gtol": 1e-6})
        g = np.asarray(r.jac)
        free = np.array([not (b[0] is not None and (abs(v - b[0]) < 1e-6 or abs(v - b[1]) < 1e-6)) for v, b in zip(r.x, bounds)])
        ok = r.success and np.all(np.abs(g[free]) < 1e-3)
        if ok:
            return r, True
    return r, False


def lrt(X, y, fun, prot, nf, npr):
    red, ok_r = fit(X[:, :3], y, fun, prot, nf, npr, np.r_[np.zeros(3), np.log(0.5), np.log(1.0)])
    full, ok_f = fit(X, y, fun, prot, nf, npr, np.r_[red.x[:3], 0.0, red.x[3:]])
    stat = 2 * (red.fun - full.fun)
    if stat < -1e-4:
        full, ok_f = fit(X, y, fun, prot, nf, npr, np.r_[red.x[:3], 0.0, red.x[3:]] + 1e-3)
        stat = 2 * (red.fun - full.fun)
    if not (ok_r and ok_f) or stat < -1e-4:
        return None
    return stats.chi2.sf(max(stat, 0.0), 1)


def rq2_dataset(nf, npr, k, inter_w, inter_r, sdp=0.5, sdf=1.5):
    prot = np.arange(nf) % npr
    up = rng.normal(0, sdp, npr)[prot]; uf = rng.normal(0, sdf, nf)
    out = []
    for base, inter in ((-0.85, inter_w), (-0.3, inter_r)):      # writing, repair share up and uf
        rows, y, fun = [], [], []
        for f in range(nf):
            for t in (0, 1):
                for x in (0, 1):
                    eta = base + 0.5 * t - 0.5 * x + inter * t * x + up[f] + uf[f]
                    for _ in range(k):
                        rows.append((1, t, x, t * x)); y.append(rng.random() < expit(eta)); fun.append(f)
        fun = np.array(fun)
        out.append((np.array(rows, float), np.array(y, float), fun, prot))   # prot: protocol of each function
    return out


def rq2_family(nf, npr, inter_w, inter_r, sims=300, k=3):
    hits = np.zeros(2); fails = 0; fw = 0
    for _ in range(sims):
        ps = []
        for X, y, fun, pr in rq2_dataset(nf, npr, k, inter_w, inter_r):
            p = lrt(X, y, fun, pr, nf, npr)
            fails += p is None
            ps.append(1.0 if p is None else p)
        r = holm(np.array(ps))
        hits += r
        fw += (r & (np.array([inter_w, inter_r]) == 0)).any()
    return hits / sims, fw / sims, fails, 2 * sims


def run_rq2():
    print("RQ2 (declared model). Random intercepts for protocol and function, nested quadrature; LRT vs chi-square(1);")
    print("writing and repair share effects; Holm over the two. Checked convergence; failures stay as non-rejections.")
    print("functions protocols (writing, repair) | rejection writing | rejection repair | FWER | failed fits")
    for nf, npr in ((40, 20), (20, 10), (10, 5)):
        for iw, ir in ((0.0, 0.0), (0.0, 1.5), (1.0, 1.0), (1.5, 1.5), (2.0, 1.0)):
            if nf < 40 and (iw, ir) not in ((0.0, 0.0), (1.5, 1.5)):
                continue
            h, fw, f, n = rq2_family(nf, npr, iw, ir)
            print(f"{nf:9d} {npr:9d} ({iw}, {ir})  | {ci(h[0], n // 2)} | {ci(h[1], n // 2)} | {ci(fw, n // 2)} | {f}/{n}")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("rq1", "both"):
        run_rq1()
    if which in ("rq2", "both"):
        run_rq2()
