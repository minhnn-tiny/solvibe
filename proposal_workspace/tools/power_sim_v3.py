"""Power simulation, version 3: six agent configurations, paired bootstrap, Holm on actual p-values.

Run: uv run --with numpy python tools/power_sim_v3.py
Endpoint K (confirmed vulnerable compiled output per scheduled attempt). Each configuration c has its
own marginal rates aV_c and aN_c; protocol and function effects are shared by all configurations and,
with correlation rho on the latent scale, by the human outcome. Intercepts are calibrated so the
MARGINAL rates equal the stated values (Gauss-Hermite quadrature), and the reported true difference
is computed from those marginal rates.
Inference follows the plan: one two-stage bootstrap (protocols, then functions within protocols,
the same draw for the human and every configuration, attempts kept with their function), a
centered two-sided bootstrap p-value per configuration, and Holm's procedure across the six. The
pooled test (average of the six configurations) uses the same bootstrap draws.
Equal-size protocols and equal inclusion probabilities are assumed here; the month-2 rerun uses the
measured frame sizes and weights.
"""
import numpy as np

rng = np.random.default_rng(20261021)
expit = lambda x: 1 / (1 + np.exp(-x))
GX, GW = np.polynomial.hermite_e.hermegauss(60)
GW = GW / GW.sum()


def calibrate(p, sd):
    lo, hi = -25.0, 25.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if (GW * expit(mid + sd * GX)).sum() < p else (lo, mid)
    return (lo + hi) / 2


def holm(pvals, alpha=0.05):
    order = np.argsort(pvals)
    rej = np.zeros(len(pvals), bool)
    for rank, i in enumerate(order):
        if pvals[i] <= alpha / (len(pvals) - rank):
            rej[i] = True
        else:
            break
    return rej


def simulate(P, nv, nn, k, pi, aV, aN, hN, sdp, sdf, rho, sims=300, boots=1000):
    C = len(aV)
    sd = np.hypot(sdp, sdf)
    bV = np.array([calibrate(a, sd) for a in aV])
    bN = np.array([calibrate(a, sd) for a in aN])
    bH = calibrate(hN, sd)
    true = pi * (np.array(aV) - 1) + (1 - pi) * (np.array(aN) - hN)
    holm_rej = np.zeros(C)
    pooled_rej = 0
    fwer_hits = 0
    for _ in range(sims):
        up = rng.normal(0, sdp, (P, 1))
        fv = rng.normal(0, sdf, (P, nv))
        fn = rng.normal(0, sdf, (P, nn))
        # human group N outcome shares the function effect with correlation rho
        eh = rho * fn + np.sqrt(1 - rho**2) * rng.normal(0, sdf, (P, nn))
        yh = rng.binomial(1, expit(bH + up + eh))
        yv = np.stack([rng.binomial(k, expit(bV[c] + up + fv)) / k for c in range(C)])   # C x P x nv
        yn = np.stack([rng.binomial(k, expit(bN[c] + up + fn)) / k for c in range(C)])
        def est(iv, inn, pidx):
            mv = yv[:, pidx[..., None], iv].mean(axis=(-1, -2))
            mn = yn[:, pidx[..., None], inn].mean(axis=(-1, -2))
            mh = yh[pidx[..., None], inn].mean(axis=(-1, -2))
            return pi * (mv - 1) + (1 - pi) * (mn - mh)        # one value per configuration
        base_p = np.arange(P)[None, :]
        d0 = est(np.arange(nv)[None, None, :].repeat(P, 1), np.arange(nn)[None, None, :].repeat(P, 1), base_p)[:, 0]
        pidx = rng.integers(0, P, (boots, P))
        iv = rng.integers(0, nv, (boots, P, nv))
        inn = rng.integers(0, nn, (boots, P, nn))
        db = est(iv, inn, pidx)                                  # C x boots
        e = db - d0[:, None]
        p = (1 + (np.abs(e) >= np.abs(d0)[:, None]).sum(1)) / (boots + 1)
        r = holm(p)
        holm_rej += r
        fwer_hits += r[true == 0].any() if (true == 0).any() else 0
        pooled_e = e.mean(0)
        pooled_rej += (1 + (np.abs(pooled_e) >= abs(d0.mean())).sum()) / (boots + 1) < 0.05
    return true, holm_rej / sims, pooled_rej / sims, fwer_hits / sims


if __name__ == "__main__":
    assert abs((GW * expit(calibrate(0.2, 1.8) + 1.8 * GX)).sum() - 0.2) < 1e-9
    pi, hN = 0.10, 0.02
    aV = [0.6] * 6
    null_aN = hN + pi * (1 - 0.6) / (1 - pi)
    scenarios = {
        "all null": [null_aN] * 6,
        "all +0.077": [0.15] * 6,
        "mixed (3 null, 3 +0.077)": [null_aN] * 3 + [0.15] * 3,
        "spread (0.08..0.20)": [0.08, 0.10, 0.12, 0.15, 0.18, 0.20],
    }
    print("P   nV nN  scenario                    true D by configuration              Holm power by configuration         pooled  FWER")
    for P, nv, nn in ((25, 2, 4), (25, 2, 8), (30, 2, 8)):
        for name, aN in scenarios.items():
            for sdp, sdf, rho in ((0.5, 1.5, 0.3), (1.0, 2.0, 0.3)):
                true, hr, pr, fw = simulate(P, nv, nn, 3, pi, aV, aN, hN, sdp, sdf, rho)
                print(f"{P:2d} {nv:3d} {nn:2d}  {name:26s} ({sdp},{sdf}) "
                      f"{' '.join(f'{t:+.3f}' for t in true)}  {' '.join(f'{x:.2f}' for x in hr)}  {pr:.2f}  {fw:.2f}")
