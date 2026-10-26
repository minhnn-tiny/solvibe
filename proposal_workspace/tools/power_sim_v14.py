"""Version 14: paper 2 with a matched outcome (iteration-2 reviews R1 W4, R3 W2, R4 W2, R5 W5).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v14.py
Design: each function has two assertion types. For each type k, the outcome is whether the final code keeps the
behaviour that the type's wrong assertion endorses: the vulnerability for security assertions, the wrong ordinary
output for ordinary assertions. Both types get matched contrary evidence (a shown failing PoV, or a shown failing
check derived from the specification). Arms: wrong assertion present (t) x execution of repository tests (x).
Logit model per type: b_k + u + 0.5 t - 0.5 x + I_k t x, with function effects u (sd 1.5) shared by both types,
protocol effects (sd 0.5), function-specific interactions (sd 0.75) and three attempts per cell.
Generic test obedience means I_security = I_ordinary (null). A security-specific effect means I_security > I_ordinary.
The baseline b_k may differ by type, because the wrong ordinary output and the vulnerability need not be equally
common without any wrong assertion.
Two tests across 20 protocol means, alpha 0.05, 1,000 studies per row:
- probability scale: theta = I_sec - I_ord estimated from cell proportions per function (as in v10);
- logit scale: per protocol, the interaction of empirical log-odds (0.5 added to each cell count) for each type,
  then the difference between types, t-test across protocols.
"""
import numpy as np
from scipy import stats

expit = lambda x: 1 / (1 + np.exp(-x))


def sim(nf, npr, b_sec, b_ord, i_sec, i_ord, rng, sims=1000, k=3, slope_sd=0.75):
    prot = np.arange(nf) % npr
    rej_p = rej_l = 0
    for _ in range(sims):
        u = rng.normal(0, 1.5, nf) + rng.normal(0, 0.5, npr)[prot]
        est_p = np.zeros(nf); lo = np.zeros(npr)
        for sign, b, inter in ((1, b_sec, i_sec), (-1, b_ord, i_ord)):
            it = inter + rng.normal(0, slope_sd, nf)
            m = {}; cnt = {}
            for t in (0, 1):
                for x in (0, 1):
                    y = rng.binomial(k, expit(b + u + 0.5 * t - 0.5 * x + it * t * x))
                    m[t, x] = y / k
                    cnt[t, x] = np.array([y[prot == j].sum() for j in range(npr)]), np.bincount(prot, minlength=npr) * k
            est_p += sign * ((m[1, 1] - m[1, 0]) - (m[0, 1] - m[0, 0]))
            lg = {key: np.log((c + 0.5) / (n - c + 0.5)) for key, (c, n) in cnt.items()}
            lo += sign * ((lg[1, 1] - lg[1, 0]) - (lg[0, 1] - lg[0, 0]))
        pm = np.array([est_p[prot == j].mean() for j in range(npr)])
        for arr, which in ((pm, "p"), (lo, "l")):
            t = arr.mean() / (arr.std(ddof=1) / np.sqrt(npr))
            r = 2 * stats.t.sf(abs(t), npr - 1) < 0.05
            if which == "p": rej_p += r
            else: rej_l += r
    return rej_p / sims, rej_l / sims


if __name__ == "__main__":
    rng = np.random.default_rng(1414)
    print("functions, baselines (security, ordinary), interactions (security, ordinary): rejection rate, probability scale | logit scale")
    for nf in (80, 160):
        for b_ord in (-0.85, -2.0, 0.5):
            for i_sec, i_ord in ((0.0, 0.0), (1.0, 1.0), (1.5, 1.5), (1.0, 0.0), (1.5, 0.5), (2.0, 1.0)):
                rp, rl = sim(nf, 20, -0.85, b_ord, i_sec, i_ord, rng)
                print(f"{nf:3d} functions, baselines (-0.85, {b_ord:+.2f}), interactions ({i_sec}, {i_ord}): {rp:.3f} | {rl:.3f}", flush=True)
