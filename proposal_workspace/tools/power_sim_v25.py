"""Version 25: a finite-population check of the principal decision with construction that depends on difficulty
(round-15 point R15.3; iteration-3 meta-review item 2).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v25.py [vlist]
Unlike power_sim_v8.py, which redraws every protocol and function in every simulated study, this script first builds
one fully enumerated frame of M = 200 protocols and keeps it fixed:
- V counts per protocol come from a list (default: list 2 of evidence/frame_inventory/README.md, uncapped values are
  not available there, so the capped list is used; replace it with the audited counts of evidence/frame_audit/ when
  they exist); N counts are uniform on 30..120;
- every function has fixed latent effects: a protocol effect (sd 0.5), a protocol-by-author effect (sd 0.5), a
  function effect shared by authors (sd 1.5; correlation 0.3 with the historical code, share 0.5 for agents);
- the historical implementation of each function is fixed as vulnerable or not; each agent configuration has a fixed
  vulnerability probability per function;
- each function is buildable or not under the fixed construction allowance, decided once: buildable with probability
  expit(b - kappa * difficulty), where difficulty = lam * (shared function effect) + noise, so that with lam > 0 harder
  functions are both more often vulnerable and less often built. b is set so that the target yield holds.
The target (the constructible domain) is computed exactly on the frame: the security part is
sum_s share_s * (mean over buildable functions in s of agent vulnerability probability * agent recall
                  - historical vulnerable indicator * historical recall), with share_s the stratum's share of buildable
functions. Each simulated study samples 20 protocols without replacement, up to 2 V and 6 N functions per protocol,
drops unbuilt functions, runs two attempts per configuration, applies detection (recall by author and stratum),
compilation 0.9 and functional success 0.8 for agents, and estimates the security part with the weighted ratio
estimator and a delete-one-protocol jackknife. Decision: Holm at 0.035 across the two configurations (the level of
power_results_v24.txt). Reported: the frame's true security part, the mean estimate, coverage of the 95% interval with
multiplier 1.2, and the minimum configuration power. 300 studies per scenario.
"""
import sys
import numpy as np
from scipy import stats
import power_sim_v8 as v8
from power_sim_v21 import LIST2

expit = v8.expit
M, P, VCAP, NPER, K = 200, 20, 2, 6, 2
RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}


def make_frame(rng, vlist, aV, aN, hV, hN, lam, yield_, kappa=1.0):
    NV = rng.choice(np.array(vlist), M); NN = rng.integers(30, 121, M)
    sd_tot = np.sqrt(0.5**2 + 1.5**2 + 0.5**2)
    bA = {s: [v8.calib(a, sd_tot) for a in rates] for s, rates in (("V", aV), ("N", aN))}
    bH = {"V": v8.calib(hV, np.hypot(0.5, 1.5)), "N": v8.calib(hN, np.hypot(0.5, 1.5))}
    up, upa = rng.normal(0, 0.5, M), rng.normal(0, 0.5, M)
    fr = []
    for p in range(M):
        for s, n in (("V", NV[p]), ("N", NN[p])):
            if n == 0:
                continue
            sh = rng.normal(0, 1.5, n)
            hum = 0.3 * sh + np.sqrt(1 - 0.09) * rng.normal(0, 1.5, n)
            yh = rng.random(n) < expit(bH[s] + up[p] + hum)
            pa = np.array([expit(b + up[p] + upa[p] + np.sqrt(0.5) * sh + np.sqrt(0.5) * rng.normal(0, 1.5, n)) for b in bA[s]])
            diff = lam * sh / 1.5 + np.sqrt(max(1 - lam**2, 0)) * rng.normal(0, 1, n)
            fr.append(dict(p=p, s=s, n=n, yh=yh, pa=pa, diff=diff))
    alld = np.concatenate([f["diff"] for f in fr])
    lo, hi = -20.0, 20.0
    for _ in range(100):                              # intercept giving the target build yield over the frame
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if expit(mid - kappa * alld).mean() > yield_ else (mid, hi)
    for f in fr:
        f["built"] = rng.random(f["n"]) < expit((lo + hi) / 2 - kappa * f["diff"])
    return NV, NN, fr


def truth(fr, recall):
    sAV, sAN, sHV, sHN = recall
    out, cnt = {}, {}
    for s, sA, sH in (("V", sAV, sHV), ("N", sAN, sHN)):
        pa = np.concatenate([f["pa"][:, f["built"]] for f in fr if f["s"] == s], axis=1)
        yh = np.concatenate([f["yh"][f["built"]] for f in fr if f["s"] == s])
        out[s] = pa.mean(1) * sA - yh.mean() * sH
        cnt[s] = yh.size
    sh = cnt["V"] / (cnt["V"] + cnt["N"])
    return sh * out["V"] + (1 - sh) * out["N"]


def study(rng, fr, recall):
    sAV, sAN, sHV, sHN = recall
    prot = rng.choice(M, P, replace=False)
    AY = np.zeros((2, 2, P)); AW = np.zeros((2, 2, P)); HY = np.zeros((2, P)); HW = np.zeros((2, P))
    byp = {}
    for f in fr:
        byp.setdefault(f["p"], []).append(f)
    for j, p in enumerate(prot):
        for f in byp.get(p, []):
            st = 0 if f["s"] == "V" else 1
            cap = VCAP if st == 0 else NPER
            idx = np.arange(f["n"]) if f["n"] <= cap else rng.choice(f["n"], cap, replace=False)
            idx = idx[f["built"][idx]]
            if idx.size == 0:
                continue
            w = f["n"] / min(f["n"], cap)
            sA, sH = (sAV, sHV) if st == 0 else (sAN, sHN)
            yh = f["yh"][idx] & (rng.random(idx.size) < sH)
            HY[st, j] += w * yh.sum(); HW[st, j] += w * idx.size
            for c in range(2):
                vul = rng.random((K, idx.size)) < f["pa"][c, idx]
                work = (rng.random((K, idx.size)) < 0.9) & (rng.random((K, idx.size)) < 0.8)
                det = rng.random((K, idx.size)) < sA
                AY[st, c, j] += w * (vul & det & work).sum(); AW[st, c, j] += w * work.sum()
    def est(m):
        d = []
        for st in (0, 1):
            va = (AY[st] * m[..., None, :]).sum(-1) / (AW[st] * m[..., None, :]).sum(-1)
            vh = ((HY[st] * m).sum(-1) / (HW[st] * m).sum(-1))[..., None]
            d.append(va - vh)
        sv, sn = (HW[0] * m).sum(-1)[..., None], (HW[1] * m).sum(-1)[..., None]
        sh = sv / (sv + sn)
        return sh * d[0] + (1 - sh) * d[1]
    with np.errstate(invalid="ignore", divide="ignore"):
        d0 = est(np.ones(P)); jk = est(1.0 - np.eye(P))
    se = np.sqrt((P - 1) / P * ((jk - np.nanmean(jk, 0)) ** 2).sum(0))
    return d0, se


if __name__ == "__main__":
    vlist = LIST2
    q = stats.t.ppf(0.975, P - 1)
    print(f"Finite frame of {M} protocols; V counts from list 2 (mean {np.mean(LIST2):.2f}); 20 protocols sampled; Holm 0.035; multiplier 1.2")
    rng = np.random.default_rng(2501)
    for lam, yld in ((0.0, 0.9), (0.0, 0.7), (0.6, 0.9), (0.6, 0.7)):
        for aN in (0.04, 0.17, 0.24):
            for rname, rc in RECALLS.items():
                NV, NN, fr = make_frame(rng, vlist, (0.6, 0.6), (aN, aN), 0.9, 0.05, lam, yld)
                tr = truth(fr, rc)
                res = [study(rng, fr, rc) for _ in range(300)]
                d = np.array([r[0] for r in res]); se = np.array([r[1] for r in res])
                ok = np.isfinite(d).all(1) & np.isfinite(se).all(1)
                d, se = d[ok], se[ok]
                cov = ((d - 1.2 * q * se <= tr) & (tr <= d + 1.2 * q * se)).mean(0).min()
                p = 2 * stats.t.sf(np.abs(d) / se, P - 1)
                rej = np.array([v8.holm(x, 0.035) for x in p]) & (np.sign(d) == np.sign(tr))
                print(f"  difficulty link {lam}, build yield {yld}, agent N rate {aN}, recall {rname}: frame truth {tr.mean():+.3f};"
                      f" mean estimate {d.mean():+.3f}; coverage {cov:.3f}; minimum configuration rate of a correct claim {rej.mean(0).min():.2f}; usable studies {ok.mean():.2f}", flush=True)
