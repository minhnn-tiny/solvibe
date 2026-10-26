"""Version 35: author-specific unresolved rates and four missingness mechanisms for the frozen V33 procedure
(proposal_v21 section 6.3, "Required simulation before launch"; Peer B's round-20 simulation list, items 1 to 6).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v35.py
Design: 22 protocols, up to one V and six N functions, two attempts per configuration; the 24 frames of power_sim_v29.py
(seed 2901); procedure frozen from power_results_v33.txt: Holm level 0.03, interval multiplier 1.175, with the widening
terms of power_sim_v32.py. No recalibration.
Unresolved rates (u_A1, u_A2, u_H): all vectors on {0, 0.005, 0.0075, 0.013}^3 plus u_H in {0.02, 0.03, 0.065} with agent
rates in {0, 0.0075}^2. The two configurations are generated identically, so only u_A1 <= u_A2 is simulated (both partial-null
assignments are run, which covers the swapped vectors): 49 vectors.
Mechanisms (each implementation is unresolved when a uniform draw falls below its threshold):
  1 independent: one draw per implementation; threshold = the author's rate;
  2 task: one draw per function, shared by the historical implementation and all agent attempts; threshold = each author's rate;
  3 protocol: one draw per protocol, shared by all its implementations; threshold = each author's rate;
  4 difficulty: one draw per implementation; threshold expit(b_a + s_f), s_f = 0.6 x (shared function effect) / 1.5 +
    0.8 x N(0, 1) fixed per function, b_a set by bisection so that the mean threshold over the frame's built functions
    equals the author's rate. Higher s_f means more often vulnerable and more often unresolved.
Common random numbers: each simulated study is drawn once; every mechanism and rate vector thresholds the same draws.
Conditions: exact global null, partial nulls (0, +0.10) and (+0.10, 0), exact +0.10, exact +0.15, and the negative target
max(-0.05, half the lowest attainable contrast). 4,000 fresh studies per frame and condition (seed 3901).
Checks, per mechanism (Bonferroni over the checks of that mechanism, one-sided Clopper-Pearson, family confidence 0.95):
family-wise error at the three null conditions (upper bound <= 0.05), marginal coverage in all six conditions (lower bound
>= 0.95), correct-direction power at +0.15 (lower bound >= 0.60). An interval is undefined when any of the six quantities
that form it (both bounds, both standard errors, both widening terms) is nonfinite (point 1: corrected diagnostic; the
v33 definition, which checked four quantities, is reported beside it). Undefined intervals count as coverage failures.
Operating regions: a vector passes when all three checks pass at it; the downward-closed passing set keeps a vector only if
every tested vector no larger in any coordinate also passes; its maximal vectors are reported.
Monitoring: unweighted and inverse-inclusion-weighted observed unresolved shares by author, from the exact-null condition.
RQ1a (mechanism 1): G = (1 - share of V) x (V difference - N difference), adverse bounds, delete-one-protocol jackknife,
interval multiplier 1.175; marginal coverage, undefined share and mean half-width.
Outputs: power_results_v35.txt and power_results_v35_vectors.csv (one row per mechanism, vector and condition, worst over
frames).
"""
import csv
import itertools
import multiprocessing as mp
import numpy as np
from scipy import stats
import power_sim_v29 as v29
import power_sim_v30 as v30
import power_sim_v32 as v32

DESIGN, A_STAR, C_STAR, N_STUDIES, SEED = (22, 1, 6, 2), 0.03, 1.175, 4000, 3901
BASE = [0.0, 0.005, 0.0075, 0.013]
VECS = [(a1, a2, h) for a1, a2 in itertools.combinations_with_replacement(BASE, 2) for h in BASE] + \
       [(a1, a2, h) for a1, a2 in itertools.combinations_with_replacement([0.0, 0.0075], 2) for h in (0.02, 0.03, 0.065)]
MECHS = ["independent", "task", "protocol", "difficulty"]
CONDS = [("exact null", 0.0), ("partial null (0, +0.10)", (0.0, 0.10)), ("partial null (+0.10, 0)", (0.10, 0.0)),
         ("exact +0.10", 0.10), ("exact +0.15", 0.15), ("negative", "neg")]
BINS = np.arange(0, 0.2001, 0.0025)
NV, NM = len(VECS), len(MECHS)
expit = v29.expit
_SCORE = {}


def init(design=DESIGN):
    v32.init(design)
    rng = np.random.default_rng(3999)
    for fi, (_, _, fr) in enumerate(v30.FRAMES):
        for key in sorted(fr.f):
            d = fr.f[key]
            d["score"] = 0.6 * d["sh"] / 1.5 + 0.8 * rng.normal(0, 1, d["sh"].size)
        built = np.concatenate([d["score"][d["built"]] for d in fr.f.values()])
        _SCORE[fi] = {u: calib(built, u) for u in sorted({x for v in VECS for x in v})}


def calib(score, u):
    if u == 0:
        return -np.inf
    lo, hi = -30.0, 30.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if expit(mid + score).mean() < u else (lo, mid)
    return (lo + hi) / 2


def draw(rng, fr, recall):
    """One study's sample and outcomes before any unresolved status: per-function arrays."""
    P, VCAP, NPER, K = v29.P, v29.VCAP, v29.NPER, v29.K
    sAV, sAN, sHV, sHN = recall
    sel = v29.sys_pps(rng, fr.pi)
    assert len(set(sel.tolist())) == P
    rows = []
    for j, p in enumerate(sel):
        hh = 1.0 / fr.pi[p]
        for st, s in enumerate(("V", "N")):
            d = fr.f.get((p, s))
            if d is None:
                continue
            n = d["yh"].size; cap = VCAP if st == 0 else NPER
            idx = np.arange(n) if n <= cap else rng.choice(n, cap, replace=False)
            w = hh * n / idx.size
            idx = idx[d["built"][idx]]
            if idx.size == 0:
                continue
            sA, sH = (sAV, sHV) if st == 0 else (sAN, sHN)
            hy = d["yh"][idx] & (rng.random(idx.size) < sH)
            pa = fr.pa(s, d)[:, idx]
            work = (rng.random((2, K, idx.size)) < 0.9) & (rng.random((2, K, idx.size)) < 0.8)
            ay = work & (rng.random((2, K, idx.size)) < pa[:, None, :]) & (rng.random((2, K, idx.size)) < sA)
            rows.append(dict(st=np.full(idx.size, st), j=np.full(idx.size, j), w=np.full(idx.size, w), hy=hy, aw=work, ay=ay, score=d["score"][idx]))
    cat = {k: np.concatenate([r[k] for r in rows], axis=-1) for k in rows[0]}
    nf = cat["hy"].size
    cat["Uh"] = rng.random(nf); cat["Ua"] = rng.random((2, K, nf)); cat["Ut"] = rng.random(nf); cat["Up"] = rng.random(P)[cat["j"]]
    return cat


def masks(cat, bmap):
    """Unresolved masks for every mechanism and vector: hu (MV, nf), au (MV, 2, K, nf)."""
    u = np.array(VECS)                                      # (NV, 3): u_A1, u_A2, u_H
    tA, tH = u[:, :2, None, None], u[:, 2, None]
    hu = [cat["Uh"][None] < tH, cat["Ut"][None] < tH, cat["Up"][None] < tH]
    shp = (len(VECS), 2) + cat["Ua"].shape[1:]
    au = [cat["Ua"][None] < tA, np.broadcast_to(cat["Ut"] < tA, shp), np.broadcast_to(cat["Up"] < tA, shp)]
    bH = np.array([bmap[x] for x in u[:, 2]]); bA = np.array([[bmap[x] for x in r] for r in u[:, :2]])
    with np.errstate(over="ignore"):
        pH = expit(bH[:, None] + cat["score"][None]); pA = expit(bA[:, :, None] + cat["score"][None, None])
    hu.append(cat["Uh"][None] < pH); au.append(cat["Ua"][None] < pA[:, :, None, :])
    return np.concatenate(hu), np.concatenate(au)


def evaluate(cat, bmap):
    P, K = v29.P, v29.K
    G = np.zeros((cat["hy"].size, 2 * P)); G[np.arange(cat["hy"].size), cat["st"] * P + cat["j"]] = 1.0
    hu, au = masks(cat, bmap)
    w, hy, aw, ay = cat["w"], cat["hy"], cat["aw"], cat["ay"]
    S = lambda x: (x * w) @ G                                # weighted sums by (stratum, protocol)
    Hy, Hw, Hu = S(hy & ~hu), S(~hu), S(hu)                  # (MV, 2P)
    Ay, Aw, Au = [S(x).sum(2) for x in (ay & ~au, aw & ~au, au)]   # (MV, 2, 2P) after summing attempts
    B = w @ G
    rs = lambda x: x.reshape(x.shape[:-1] + (2, P))
    Hy, Hw, Hu, Ay, Aw, Au, B = map(rs, (Hy, Hw, Hu, Ay, Aw, Au, B))
    cnt = lambda x: (x.astype(float) @ G).reshape(x.shape[:-1] + (2, P)).sum(-1)
    he, hn = cnt(hy & ~hu), cnt(~hu)                         # (MV, 2)
    ae, an = cnt(ay & ~au).sum(2), cnt(aw & ~au).sum(2)      # (MV, 2c, 2)

    def bounds(m):                                           # m: (R, P)
        Bm = B @ m.T; shr = Bm[0] / (Bm[0] + Bm[1])          # (R,)
        h = [x @ m.T for x in (Hy, Hw, Hu)]                  # (MV, 2, R)
        a = [x @ m.T for x in (Ay, Aw, Au)]                  # (MV, 2c, 2, R)
        vlo = a[0] / (a[1] + a[2]); vhi = (a[0] + a[2]) / (a[1] + a[2])
        hlo = (h[0] / (h[1] + h[2]))[:, None]; hhi = ((h[0] + h[2]) / (h[1] + h[2]))[:, None]
        dlo, dhi = vlo - hhi, vhi - hlo                      # (MV, 2c, 2st, R)
        L = shr * dlo[:, :, 0] + (1 - shr) * dlo[:, :, 1]; U = shr * dhi[:, :, 0] + (1 - shr) * dhi[:, :, 1]
        GL = (1 - shr) * (dlo[:, :, 0] - dhi[:, :, 1]); GU = (1 - shr) * (dhi[:, :, 0] - dlo[:, :, 1])
        return L, U, GL, GU, shr
    with np.errstate(invalid="ignore", divide="ignore"):
        L0, U0, GL0, GU0, shr0 = bounds(np.ones((1, P)))
        Lj, Uj, GLj, GUj, _ = bounds(1.0 - np.eye(P))
        se = lambda x: np.sqrt((P - 1) / P * ((x - np.nanmean(x, -1, keepdims=True)) ** 2).sum(-1))
        share = np.array([shr0[0], 1 - shr0[0]])
        ucl = np.where(hn > 0, 1 - 0.025 ** (1 / np.maximum(hn, 1)), np.nan)
        zL = np.where(he == 0, share * ucl, 0.0).sum(-1)                         # (MV,)
        ucla = np.where(an > 0, 1 - 0.025 ** (1 / np.maximum(an, 1)), np.nan)
        zU = np.where(ae == 0, share * ucla, 0.0).sum(-1)                        # (MV, 2c)
        nf = hy.size
        mon = np.stack([hu.mean(-1), au[:, 0].mean((-1, -2)), au[:, 1].mean((-1, -2)),
                        (hu * w).sum(-1) / w.sum(), (au[:, 0] * w).sum((-1, -2)) / (K * w.sum()), (au[:, 1] * w).sum((-1, -2)) / (K * w.sum())], 1)
    return (L0[..., 0], se(Lj), U0[..., 0], se(Uj), np.broadcast_to(zL[:, None], (len(zL), 2)), zU,
            GL0[:NV, :, 0], se(GLj[:NV]), GU0[:NV, :, 0], se(GUj[:NV]), mon)


def job(args):
    fi, ci = args
    name, rc, fr = v30.FRAMES[fi]
    cond, target = CONDS[ci]
    if target == "neg":
        target = np.maximum(-0.05, 0.5 * fr.truth(rc, np.full(2, -15.0)))
    tr = fr.set_target(rc, target)
    gtr = rq1a_truth(fr, rc)
    rng = np.random.default_rng([SEED, fi, ci])
    out = [evaluate(draw(rng, fr, rc), _SCORE[fi]) for _ in range(N_STUDIES)]
    L, sL, U, sU, zL, zU, GL, sGL, GU, sGU, mon = (np.array([o[i] for o in out]) for i in range(11))   # (n, MV, 2) etc.
    q = stats.t.ppf(0.975, v29.P - 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        pl, pu = 2 * stats.t.sf(np.abs(L) / sL, v29.P - 1), 2 * stats.t.sf(np.abs(U) / sU, v29.P - 1)
        sign = np.where(L > 0, 1, np.where(U < 0, -1, 0))
        p = np.nan_to_num(np.where(L > 0, pl, np.where(U < 0, pu, 1.0)), nan=1.0)
        o = np.argsort(p, -1, kind="stable"); ps = np.take_along_axis(p, o, -1)
        r1 = ps[..., 0] <= A_STAR / 2; r2 = r1 & (ps[..., 1] <= A_STAR)
        rej = np.zeros_like(p, bool); np.put_along_axis(rej, o, np.stack([r1, r2], -1), -1)
        null = np.abs(tr) < 1e-9
        err = (rej & (null | (np.sign(tr) != sign))).any(-1).sum(0)                  # (MV,)
        pw = (rej & (sign == np.sign(tr)) & ~null).sum(0)                             # (MV, 2)
        hit = (L - C_STAR * q * sL - zL <= tr) & (tr <= U + C_STAR * q * sU + zU)
        undef_new = (~(np.isfinite(L) & np.isfinite(sL) & np.isfinite(U) & np.isfinite(sU) & np.isfinite(zL) & np.isfinite(zU))).any(-1).sum(0)
        undef_old = (~(np.isfinite(L) & np.isfinite(sL) & np.isfinite(U) & np.isfinite(sU))).any(-1).sum(0)
        ghit = (GL - C_STAR * q * sGL <= gtr) & (gtr <= GU + C_STAR * q * sGU)
        gfin = np.isfinite(GL) & np.isfinite(GU) & np.isfinite(sGL) & np.isfinite(sGU)
        ghw = np.where(gfin, ((GU + C_STAR * q * sGU) - (GL - C_STAR * q * sGL)) / 2, np.nan)
    hist = np.array([[np.histogram(np.clip(mon[:, m, k], 0, 0.19999), BINS)[0] for k in range(6)] for m in range(mon.shape[1])])
    return fi, ci, tr, gtr, dict(err=err, pw=pw, cov=hit.sum(0), sim=hit.all(-1).sum(0), undef_new=undef_new, undef_old=undef_old,
                                 gcov=ghit.sum(0), gundef=(~gfin).any(-1).sum(0), ghw=np.nanmean(ghw, 0), hist=hist, mon_mean=mon.mean(0))


def rq1a_truth(fr, recall):
    sAV, sAN, sHV, sHN = recall
    out, cnt = {}, {}
    for s, sA, sH in (("V", sAV, sHV), ("N", sAN, sHN)):
        ds = [d for (p, ss), d in fr.f.items() if ss == s]
        pa = np.concatenate([fr.pa(s, d)[:, d["built"]] for d in ds], axis=1)
        yh = np.concatenate([d["yh"][d["built"]] for d in ds])
        out[s] = pa.mean(1) * sA - yh.mean() * sH; cnt[s] = yh.size
    shr = cnt["V"] / (cnt["V"] + cnt["N"])
    return (1 - shr) * (out["V"] - out["N"])


if __name__ == "__main__":
    init()
    names = [f[0] for f in v30.FRAMES]
    jobs = [(fi, ci) for fi in range(len(names)) for ci in range(len(CONDS))]
    res = {}
    with mp.Pool(8, initializer=init) as pool:
        for fi, ci, tr, gtr, r in pool.imap_unordered(job, jobs):
            res[fi, ci] = (tr, gtr, r)
    n = N_STUDIES
    nullc = [0, 1, 2]
    m_err, m_cov, m_pw = len(nullc) * NV * 24, len(CONDS) * NV * 24 * 2, NV * 24 * 2
    lines = [f"Frozen V33 procedure (Holm {A_STAR}, multiplier {C_STAR}) for 22 x (1, 6), two attempts; {n} studies per frame and condition; "
             f"{NV} rate vectors x {NM} mechanisms; Bonferroni per mechanism over {m_err} error, {m_cov} coverage and {m_pw} power checks"]
    rowsout = []
    regions = {}
    for mi, mech in enumerate(MECHS):
        sl = slice(mi * NV, (mi + 1) * NV)
        passv = np.ones(NV, bool); worst = {}
        for vi, vec in enumerate(VECS):
            k = mi * NV + vi
            eub = max(v30.ucb(int(res[fi, ci][2]["err"][k]), n, m_err) for fi in range(24) for ci in nullc)
            clb = min(v30.lcb(int(x), n, m_cov) for fi in range(24) for ci in range(len(CONDS)) for x in res[fi, ci][2]["cov"][k])
            plb = min(v30.lcb(int(x), n, m_pw) for fi in range(24) for x in res[fi, 4][2]["pw"][k])
            pmin = min(x / n for fi in range(24) for x in res[fi, 4][2]["pw"][k])
            passv[vi] = eub <= 0.05 and clb >= 0.95 and plb >= 0.60
            worst[vec] = (eub, clb, plb, pmin)
            for ci, (cond, _) in enumerate(CONDS):
                e = max(res[fi, ci][2]["err"][k] for fi in range(24)) / n
                cv = min(res[fi, ci][2]["cov"][k].min() for fi in range(24)) / n
                sim = min(res[fi, ci][2]["sim"][k] for fi in range(24)) / n
                un = max(res[fi, ci][2]["undef_new"][k] for fi in range(24)) / n
                uo = max(res[fi, ci][2]["undef_old"][k] for fi in range(24)) / n
                pw = min(res[fi, ci][2]["pw"][k].min() for fi in range(24)) / n
                rowsout.append([mech, *vec, cond, f"{e:.4f}", f"{cv:.4f}", f"{sim:.4f}", f"{pw:.4f}", f"{uo:.5f}", f"{un:.5f}"])
        tested = np.array(VECS)
        full = lambda v: [tuple(v), (v[1], v[0], v[2])]
        ok = {}
        for vi, vec in enumerate(VECS):
            below = [wi for wi, w in enumerate(VECS) if any(np.all(np.array(x) <= np.array(vec) + 1e-12) for x in full(w))]
            ok[vec] = all(passv[wi] for wi in below)
        dc = [v for v in VECS if ok[v]]
        maxi = [v for v in dc if not any(w != v and all(a >= b - 1e-12 for a, b in zip(w, v)) for w in dc)]
        regions[mech] = maxi
        lines.append(f"\nMechanism: {mech}")
        lines.append(f"  vectors passing all three checks: {int(passv.sum())} of {NV}; downward-closed passing set: {len(dc)} vectors")
        lines.append("  maximal vectors of the downward-closed set (u_A1, u_A2, u_H): " + "; ".join(f"({a}, {b}, {c})" for a, b, c in maxi))
        e_all = max(w[0] for w in worst.values()); c_all = min(w[1] for w in worst.values())
        lines.append(f"  over all {NV} vectors: worst error upper bound {e_all:.4f}; worst coverage lower bound {c_all:.4f}")
        lines.append("  +0.15 power by vector, lowest point estimate / lower bound (fails marked *):")
        for vec in VECS:
            eub, clb, plb, pmin = worst[vec]
            lines.append(f"    ({vec[0]}, {vec[1]}, {vec[2]}): {pmin:.3f} / {plb:.3f}{' *' if plb < 0.60 else ''}{'  [error or coverage FAIL]' if eub > 0.05 or clb < 0.95 else ''}")
        un_old = max(res[fi, ci][2]["undef_old"][mi * NV:(mi + 1) * NV].max() for fi in range(24) for ci in range(len(CONDS))) / n
        un_new = max(res[fi, ci][2]["undef_new"][mi * NV:(mi + 1) * NV].max() for fi in range(24) for ci in range(len(CONDS))) / n
        lines.append(f"  undefined-interval share, worst over frames, conditions and vectors: {un_old:.5f} (four quantities, V33 definition), {un_new:.5f} (all six quantities)")
    # monitoring (exact null, pooled over frames)
    lines.append("\nMonitoring, exact null, all frames pooled: observed unresolved share, mean and 95th percentile (unweighted | inverse-inclusion weighted)")
    auth = ["historical", "configuration 1", "configuration 2"]
    for mi, mech in enumerate(MECHS):
        for vec in [(0.0, 0.0, 0.0), (0.0075, 0.0075, 0.0075), (0.013, 0.013, 0.013), (0.0, 0.0, 0.02), (0.0, 0.0, 0.065)]:
            k = mi * NV + VECS.index(vec)
            H = sum(res[fi, 0][2]["hist"][k] for fi in range(24))                 # (6, bins)
            mm = np.mean([res[fi, 0][2]["mon_mean"][k] for fi in range(24)], 0)
            p95 = [BINS[np.searchsorted(np.cumsum(h) / h.sum(), 0.95) + 1] for h in H]
            order = [0, 1, 2]
            lines.append(f"  {mech}, {vec}: " + "; ".join(f"{auth[a]} {mm[a]:.4f}/{p95[a]:.4f} | {mm[a + 3]:.4f}/{p95[a + 3]:.4f}" for a in order))
    # RQ1a
    lines.append("\nRQ1a (independent mechanism, multiplier 1.175, not calibrated for RQ1a): lowest marginal coverage, largest undefined share, largest mean half-width, by condition over frames and vectors")
    for ci, (cond, _) in enumerate(CONDS):
        cv = min(res[fi, ci][2]["gcov"][:NV].min() for fi in range(24)) / n
        un = max(res[fi, ci][2]["gundef"][:NV].max() for fi in range(24)) / n
        hw = max(np.nanmax(res[fi, ci][2]["ghw"][:NV]) for fi in range(24))
        hw0 = max(np.nanmax(res[fi, ci][2]["ghw"][VECS.index((0.0, 0.0, 0.0))]) for fi in range(24))
        lines.append(f"  {cond}: coverage {cv:.3f}; undefined {un:.4f}; mean half-width up to {hw:.3f} (at no unresolved outcome: {hw0:.3f})")
    lines.append("done")
    open("power_results_v35.txt", "w").write("\n".join(lines) + "\n")
    with open("power_results_v35_vectors.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["mechanism", "u_A1", "u_A2", "u_H", "condition", "worst_familywise_error", "lowest_marginal_coverage", "lowest_simultaneous_coverage", "lowest_power", "undefined_share_v33_definition", "undefined_share_all_six"])
        wr.writerows(rowsout)
    print("\n".join(lines))
