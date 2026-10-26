"""Precision and power for the reduced core study (iteration 1 meta-review, items 1, 2, 5, 6).

Run: uv run --offline --with numpy --with statsmodels python tools/power_sim_v8.py
Design: P protocols, up to 2 group V and 8 group N functions each (unequal frames, inclusion weights),
two primary configurations (vendor-supported agents), three attempts each, one human version per function.
Each attempt has three outcomes: compiles (C), passes the legitimate-behaviour suite (L), and has a true
High/Medium vulnerability (V). The observed vulnerability is V times detection by the common procedure,
which is run on both authors without the audit report. Detection probability can differ by author and
stratum (recall s). Endpoints: K = C * V_detected and D = C * L * V_detected.
Effects: protocol effect shared by everyone, a protocol-by-author effect, function effects shared across
configurations (share gamma) and correlated with the human (rho).
Inference: weighted estimator, delete-one-protocol jackknife, t(P - 1); Holm over the two configurations
at a level calibrated on null scenarios in this script (largest alpha on a grid with worst family-wise
error <= 0.05); 95% interval width; and a two one-sided tests (TOST) equivalence test against a smallest
difference of interest of 0.05 at 0.05.
"""
import numpy as np
from scipy import stats

expit = lambda x: 1 / (1 + np.exp(-x))
GX, GW = np.polynomial.hermite_e.hermegauss(60)
GW = GW / GW.sum()


def calib(p, sd):
    lo, hi = -25.0, 25.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if (GW * expit(mid + sd * GX)).sum() < p else (lo, mid)
    return (lo + hi) / 2


def holm(p, a):
    r = np.zeros(len(p), bool)
    for k, i in enumerate(np.argsort(p)):
        if p[i] <= a / (len(p) - k):
            r[i] = True
        else:
            break
    return r


def study(rng, P, aV, add, hV, hN, recall, sdp=0.5, sdf=1.5, sdpa=0.5, rho=0.3, gamma=0.5,
          compile_p=0.9, legit_p=0.8, k=3, endpoint="D", parts=False, max_v=2, p_nov=0.0, unres=None, nv_dist=None, n_sub=None, unres_val=((0, 1), (0, 1)), p_build=None, n_per=8, sec=False, pps=False, frame_pairs=None, pps_n=False):
    """aV: agents' true vulnerability rate in group V (per configuration). add: the added detected-endpoint
    rate in group N relative to the human (per configuration), or None for an exact offsetting null, in
    which group N is set from this study's frame share so that the true difference is exactly zero.
    Returns estimates, jackknife SEs and the true differences of the detected endpoint."""
    C = len(aV)
    sd = np.sqrt(sdp**2 + sdf**2 + sdpa**2)
    sAV, sAN, sHV, sHN = recall
    fac = compile_p * (legit_p if endpoint == "D" else 1.0)      # agents: compiles (and passes) given vulnerable
    NV = 2 + rng.poisson(2, P); NN = rng.integers(30, 121, P)
    if p_nov:                                              # p_nov: share of protocols with no V function (v12); no draw when 0, so earlier results reproduce
        NV = np.where(rng.random(P) < p_nov, 0, NV)
    pwt = np.ones(P)
    if frame_pairs is not None:                            # v26: (V, N) counts per protocol drawn together from an audited list
        fp = np.array(frame_pairs)
        if pps_n:                                          # v27: protocols drawn in proportion to N count, with weights
            pick = rng.choice(len(fp), P, p=fp[:, 1] / fp[:, 1].sum())
        else:
            pick = rng.integers(0, len(fp), P)
        NV, NN = fp[pick, 0], fp[pick, 1]
        if pps_n:
            pwt = fp[:, 1].mean() / NN
    if nv_dist is not None and pps:                        # v22: protocols drawn with probability proportional to (V count + 1), with weights
        vals = np.array(nv_dist); pr = (vals + 1.0) / (vals + 1.0).sum()
        NV = rng.choice(vals, P, p=pr); pwt = 1.0 / (NV + 1.0)
    elif nv_dist is not None:                              # v15: V counts per protocol drawn from a given list
        NV = rng.choice(np.array(nv_dist), P)
    nv = np.minimum(max_v, NV); nn = np.full(P, n_per)
    if n_sub is not None:                                  # v15: N functions built only in the first n_sub protocols
        nn[n_sub:] = 0
    pi = NV.sum() / (NV + NN).sum()
    if pps:                                                # v22: known frame share from the population distribution (mean N count 75)
        pi = np.mean(nv_dist) / (np.mean(nv_dist) + 75.0)
    if frame_pairs is not None and pps_n:                  # v27: known frame share of the audited list
        fpa = np.array(frame_pairs); pi = fpa[:, 0].sum() / fpa.sum()
    dV = np.array([a * fac * sAV - hV * sHV for a in aV])
    if add is None:
        dN = -pi * dV / (1 - pi)
    elif isinstance(add, tuple) and add[0] == "target":
        dN = (add[1] - pi * dV) / (1 - pi)          # true difference exactly add[1] in this study
    elif isinstance(add, tuple) and add[0] == "sec_target":   # v24: security-part difference (among working) exactly add[1]
        dVs = np.array([a * sAV for a in aV]) - hV * sHV
        aNs = (hN * sHN + (add[1] - pi * dVs) / (1 - pi)) / sAN
        dN = aNs * fac * sAN - hN * sHN
    else:
        dN = np.array(add, float)
    aN = (hN * sHN + dN) / (fac * sAN)
    assert np.all((aN > 0) & (aN < 1)), aN
    true = pi * dV + (1 - pi) * dN
    if p_build is not None:                              # v20: target is the constructible domain; building independent of outcomes
        pic = pi * p_build[0] / (pi * p_build[0] + (1 - pi) * p_build[1])
        true_dom, gdiff_dom = pic * dV + (1 - pic) * dN, (1 - pic) * (dV - dN)
    if add is None:
        assert np.all(np.abs(true) < 1e-12)
    if isinstance(add, tuple) and add[0] == "target":
        assert np.all(np.abs(true - add[1]) < 1e-12)
    bV = [calib(a, sd) for a in aV]; bN = [calib(a, sd) for a in aN]
    bHV, bHN = calib(hV, np.hypot(sdp, sdf)), calib(hN, np.hypot(sdp, sdf))
    SV = np.zeros((C, P)); SN = np.zeros((C, P)); WV = np.zeros(P); WN = np.zeros(P)
    AY = np.zeros((2, C, P)); AW = np.zeros((2, C, P)); HY = np.zeros((2, P)); HW = np.zeros((2, P))   # v21: security part
    up = rng.normal(0, sdp, P)
    for p in range(P):
        upa = rng.normal(0, sdpa)                        # protocol-by-author effect (agents vs human)
        for st, (n, N, b, bh, sA, sH, S, W) in enumerate(((nv[p], NV[p], bV, bHV, sAV, sHV, SV, WV),
                                                         (nn[p], NN[p], bN, bHN, sAN, sHN, SN, WN))):
            shared = rng.normal(0, sdf, n)
            hum_fx = rho * shared + np.sqrt(1 - rho**2) * rng.normal(0, sdf, n)
            yh = (rng.random(n) < expit(bh + up[p] + hum_fx)) & (rng.random(n) < sH)   # human: compiles, legit
            if unres:                                        # v13: unresolved results set to bound values; unres_val[stratum] = (agent value, historical value)
                uh = rng.random(n) < unres[1]                # default: historical set to vulnerable, agent to not vulnerable
                yh = (yh | uh) if unres_val[st][1] else (yh & ~uh)
            built = (rng.random(n) < p_build[st]) if p_build is not None else np.ones(n, bool)   # v20: task built within its own allowance
            for c in range(C):
                fx = np.sqrt(gamma) * shared + np.sqrt(1 - gamma) * rng.normal(0, sdf, n)
                pv = expit(b[c] + up[p] + upa + fx)
                vul = rng.random((k, n)) < pv
                det = rng.random((k, n)) < sA
                comp = rng.random((k, n)) < compile_p
                leg = rng.random((k, n)) < legit_p
                y = comp & vul & det & (leg if endpoint == "D" else True)
                if unres:
                    ua = comp & (leg if endpoint == "D" else True) & (rng.random((k, n)) < unres[0])
                    y = (y | ua) if unres_val[st][0] else (y & ~ua)
                S[c, p] = pwt[p] * (N / n) * ((y.mean(0) - yh) * built).sum() if n else 0.0
                if sec and n:                            # v21: detected-vulnerable and working agent attempts, weighted
                    work = comp & (leg if endpoint == "D" else True)
                    AY[st, c, p] = pwt[p] * (N / n) * ((y & work).sum(0) * built).sum(); AW[st, c, p] = pwt[p] * (N / n) * (work.sum(0) * built).sum()
            W[p] = pwt[p] * (((N / n) * built.sum() if p_build is not None else N) if n else 0)
            if sec and n:
                HY[st, p] = pwt[p] * (N / n) * (yh * built).sum(); HW[st, p] = pwt[p] * (N / n) * built.sum()
    def est(m, part="all"):
        v = (SV * m[..., None, :]).sum(-1) / (WV * m).sum(-1)[..., None]
        w = (SN * m[..., None, :]).sum(-1) / (WN * m).sum(-1)[..., None]
        sh = pi
        if p_build is not None:                          # v20: constructible stratum shares estimated in every replicate
            sv, sn = (WV * m).sum(-1)[..., None], (WN * m).sum(-1)[..., None]
            sh = sv / (sv + sn)
        return {"all": sh * v + (1 - sh) * w, "V": v, "diff": (1 - sh) * (v - w)}[part]
    def est_sec(m, part="diff"):                         # v21: design difference (v23: or overall difference) among working implementations
        dlt = []
        for st in (0, 1):
            va = (AY[st] * m[..., None, :]).sum(-1) / (AW[st] * m[..., None, :]).sum(-1)
            vh = ((HY[st] * m).sum(-1) / (HW[st] * m).sum(-1))[..., None]
            dlt.append(va - vh)
        sh = pi
        if p_build is not None:
            sv, sn = (WV * m).sum(-1)[..., None], (WN * m).sum(-1)[..., None]
            sh = sv / (sv + sn)
        return (1 - sh) * (dlt[0] - dlt[1]) if part == "diff" else sh * dlt[0] + (1 - sh) * dlt[1]
    def jack(part):
        if part in ("sec", "secall"):
            pp = "diff" if part == "sec" else "all"
            jk = est_sec(1.0 - np.eye(P), pp)
            return est_sec(np.ones(P), pp), np.sqrt((P - 1) / P * ((jk - jk.mean(0)) ** 2).sum(0))
        jk = est(1.0 - np.eye(P), part)
        return est(np.ones(P), part), np.sqrt((P - 1) / P * ((jk - jk.mean(0)) ** 2).sum(0))
    d0, se = jack("all")
    if p_build is not None:
        true, dg = true_dom, gdiff_dom
    else:
        dg = (1 - pi) * (dV - dN)
    if not parts:
        return d0, se, true
    # parts (power_sim_v11.py): V-only estimate and V-only minus weighted, with their true values
    out = (d0, se, true, *jack("V"), dV, *jack("diff"), dg)
    if sec:                                              # v21: true security-part design difference
        sh_t = pic if p_build is not None else pi
        tsec = (1 - sh_t) * ((np.array(aV) * sAV - hV * sHV) - (aN * sAN - hN * sHN))
        out = out + (*jack("sec"), tsec)
        dva, dna = np.array(aV) * sAV - hV * sHV, aN * sAN - hN * sHN
        out = out + (*jack("secall"), sh_t * dva + (1 - sh_t) * dna)   # v23: overall security-part difference (indices 12-14)
    return out


def run(P, scen, recall, nsim, rng, endpoint, parts=False, max_v=2, p_nov=0.0, unres=None, **kw):
    out = [study(rng, P, *scen, recall, endpoint=endpoint, parts=parts, max_v=max_v, p_nov=p_nov, unres=unres, **kw) for _ in range(nsim)]
    return tuple(np.array([o[i] for o in out]) for i in range(len(out[0])))     # each nsim x C


if __name__ == "__main__":
    rng = np.random.default_rng(5005)
    alphas = [0.05, 0.04, 0.03, 0.025, 0.02, 0.015, 0.01]
    recalls = {"equal recall 0.7": (0.7, 0.7, 0.7, 0.7),
               "agent recall 0.8, human 0.5": (0.8, 0.8, 0.5, 0.5),
               "agent recall 0.5, human 0.8": (0.5, 0.5, 0.8, 0.8)}
    print("Core study: 2 configurations, 3 attempts, up to 2 V and 8 N functions per protocol.")
    print("Agents compile with p 0.9 and pass the legitimate suite with p 0.8; human code always does.")
    print("Effects: protocol sd 0.5, function sd 1.5, protocol-by-author sd 0.5; 400 studies per row.")
    for endpoint in ("D", "K"):
        for P in (12, 15, 20):
            worst = {a: 0.0 for a in alphas}
            for rname, rc in recalls.items():
                for hN in (0.02, 0.05):
                    d0, se, tr = run(P, ([0.6] * 2, None, 0.9, hN), rc, 400, rng, endpoint)
                    p = 2 * stats.t.sf(np.abs(d0) / se, P - 1)
                    for a in alphas:
                        worst[a] = max(worst[a], np.mean([holm(x, a).any() for x in p]))
            a_star = max([a for a in alphas if worst[a] <= 0.05], default=0.01)
            print(f"\nEndpoint {endpoint}, P={P}: worst family-wise error over exact offsetting nulls by alpha: "
                  f"{ {a: round(w, 3) for a, w in worst.items()} }; calibrated alpha* = {a_star}")
            for rname, rc in recalls.items():
                for hN, add in ((0.02, 0.05), (0.02, 0.10), (0.05, 0.10)):
                    d0, se, tr = run(P, ([0.6] * 2, [add] * 2, 0.9, hN), rc, 400, rng, endpoint)
                    p = 2 * stats.t.sf(np.abs(d0) / se, P - 1)
                    powr = np.array([holm(x, a_star) for x in p]).mean(0).min()
                    half = (stats.t.ppf(0.975, P - 1) * se).mean()
                    print(f"  {rname:28s} hN={hN:.2f} added N rate {add:+.2f}: true difference {tr.mean():+.3f}, "
                          f"minimum configuration power {powr:.2f}, mean 95% half-width {half:.3f}")
                d0, se, tr = run(P, ([0.6] * 2, None, 0.9, 0.02), rc, 400, rng, endpoint)
                q = stats.t.ppf(0.95, P - 1)
                eq = ((d0 - q * se > -0.05) & (d0 + q * se < 0.05)).mean(0).min()
                print(f"  {rname:28s} exact null: equivalence (two one-sided tests, margin 0.05) shown in {eq:.2f} of studies")
