"""Version 37: V35 without the configuration-swap shortcut, with the region rule validated inside the same generator
(round-21 points R21.1 to R21.3).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v37.py
Changes from power_sim_v35.py:
1. R21.1: every ordered agent-rate assignment is simulated: (u_A1, u_A2, u_H) on {0, 0.005, 0.0075, 0.013}^3 plus u_H in
   {0.02, 0.03, 0.065} with (u_A1, u_A2) in {0, 0.0075}^2: 76 vectors. The two configurations have separate fixed latent
   effects in each frame, so no swap is assumed. Bonferroni counts per mechanism: 3 x 76 x 24 error, 6 x 76 x 24 x 2 coverage,
   76 x 24 x 2 power checks. The operating region is the downward-closed set (over tested vectors) of vectors passing all
   three checks under all four mechanisms.
2. R21.2: the rule for evidence of leaving the region is computed on every simulated main study, under each mechanism and
   vector, from the same sampled functions and unresolved draws as the inference. For each author: x = protocols with at
   least one unresolved outcome of that author, n = protocols with at least one outcome of that author, m = the largest
   number of that author's outcomes in one protocol; limit = (one-sided 95% Clopper-Pearson lower limit for x of n) / m.
   The rule fires when the vector of the three limits is not inside the region. Each limit is stored by the smallest grid
   value at or above it (grid 0, 0.005, 0.0075, 0.013, 0.02, 0.03, 0.065, above); because region corners are grid values,
   this gives the same decision for any region on the grid.
   Development: 4,000 extra samples of three protocols per frame, drawn by the same randomized systematic sampling with
   inclusion probabilities proportional to N summing to 3, one V and six N functions, two attempts; the same rule.
3. R21.3: in the same development samples, the share of construction failures; a check fires when the one-sided 95%
   Clopper-Pearson upper limit for the pooled construction yield (built over sampled functions) is below 0.7.
Everything else (frozen procedure Holm 0.03 and multiplier 1.175, 24 frames, mechanisms, conditions, 4,000 studies per frame
and condition, corrected undefined diagnostic, RQ1a) is as in power_sim_v35.py. Seed 3701.
Outputs: power_results_v37.txt and power_results_v37_vectors.csv.
"""
import csv
import itertools
import multiprocessing as mp
import numpy as np
from scipy import stats
import power_sim_v29 as v29
import power_sim_v30 as v30
import power_sim_v35 as v35

BASE = v35.BASE
VECS = [v for v in itertools.product(BASE, BASE, BASE)] + [(a1, a2, h) for a1 in (0.0, 0.0075) for a2 in (0.0, 0.0075) for h in (0.02, 0.03, 0.065)]
v35.VECS, v35.NV = VECS, len(VECS)
NV, NM, CONDS, MECHS = len(VECS), len(v35.MECHS), v35.CONDS, v35.MECHS
GRID = np.array([0.0, 0.005, 0.0075, 0.013, 0.02, 0.03, 0.065])
N_STUDIES, N_DEV, SEED = 4000, 4000, 3701
_cache = {}
_masks = v35.masks
v35.masks = lambda cat, bmap: _cache["m"]          # v35.evaluate reuses the masks computed here


def init():
    v35.init()
    for _, _, fr in v30.FRAMES:
        fr.pi3 = v29.incl_probs(fr.NN.astype(float), 3)


def draw(rng, fr, recall, P, pi):
    """v35.draw with the protocol count and inclusion probabilities as arguments; also returns sampled and built counts."""
    VCAP, NPER, K = v29.VCAP, v29.NPER, v29.K
    sAV, sAN, sHV, sHN = recall
    sel = v29.sys_pps(rng, pi)
    assert len(set(sel.tolist())) == P
    rows, n_samp, n_built = [], 0, 0
    for j, p in enumerate(sel):
        hh = 1.0 / pi[p]
        for st, s in enumerate(("V", "N")):
            d = fr.f.get((p, s))
            if d is None:
                continue
            n = d["yh"].size; cap = VCAP if st == 0 else NPER
            idx = np.arange(n) if n <= cap else rng.choice(n, cap, replace=False)
            w = hh * n / idx.size
            n_samp += idx.size
            idx = idx[d["built"][idx]]
            n_built += idx.size
            if idx.size == 0:
                continue
            sA, sH = (sAV, sHV) if st == 0 else (sAN, sHN)
            hy = d["yh"][idx] & (rng.random(idx.size) < sH)
            pa = fr.pa(s, d)[:, idx]
            work = (rng.random((2, K, idx.size)) < 0.9) & (rng.random((2, K, idx.size)) < 0.8)
            ay = work & (rng.random((2, K, idx.size)) < pa[:, None, :]) & (rng.random((2, K, idx.size)) < sA)
            rows.append(dict(st=np.full(idx.size, st), j=np.full(idx.size, j), w=np.full(idx.size, w), hy=hy, aw=work, ay=ay, score=d["score"][idx]))
    if not rows:
        return None, n_samp, n_built
    cat = {k: np.concatenate([r[k] for r in rows], axis=-1) for k in rows[0]}
    nf = cat["hy"].size
    cat["Uh"] = rng.random(nf); cat["Ua"] = rng.random((2, K, nf)); cat["Ut"] = rng.random(nf); cat["Up"] = rng.random(P)[cat["j"]]
    return cat, n_samp, n_built


def rule_levels(cat, hu, au, P):
    """Combined grid level (0..511) of the three authors' lower limits, for every mechanism and vector."""
    J = np.zeros((cat["j"].size, P)); J[np.arange(cat["j"].size), cat["j"]] = 1.0
    out_h = J.sum(0)                                                  # historical outcomes per protocol
    unres = [au[:, 0].sum(1).astype(float) @ J, au[:, 1].sum(1).astype(float) @ J, hu.astype(float) @ J]   # (MV, P) each: A1, A2, H
    outs = [v29.K * out_h, v29.K * out_h, out_h]
    lev = []
    for u_p, o in zip(unres, outs):
        has = o > 0
        n, m = has.sum(), o.max()
        x = ((u_p > 0) & has).sum(-1)
        lo = np.where(x > 0, stats.beta.ppf(0.05, np.maximum(x, 1), n - x + 1), 0.0) / m
        lev.append(np.searchsorted(GRID, lo - 1e-12, side="left"))
    return lev[0] * 64 + lev[1] * 8 + lev[2]                         # order: A1, A2, H


def evaluate(cat, bmap):
    m = _masks(cat, bmap); _cache["m"] = m
    return v35.evaluate(cat, bmap) + (rule_levels(cat, m[0], m[1], v29.P),)


def job(args):
    fi, ci = args
    name, rc, fr = v30.FRAMES[fi]
    cond, target = CONDS[ci]
    if target == "neg":
        target = np.maximum(-0.05, 0.5 * fr.truth(rc, np.full(2, -15.0)))
    tr = fr.set_target(rc, target)
    gtr = v35.rq1a_truth(fr, rc)
    rng = np.random.default_rng([SEED, fi, ci])
    out = [evaluate(draw(rng, fr, rc, v29.P, fr.pi)[0], v35._SCORE[fi]) for _ in range(N_STUDIES)]
    L, sL, U, sU, zL, zU, GL, sGL, GU, sGU, mon, lev = (np.array([o[i] for o in out]) for i in range(12))
    q = stats.t.ppf(0.975, v29.P - 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        pl, pu = 2 * stats.t.sf(np.abs(L) / sL, v29.P - 1), 2 * stats.t.sf(np.abs(U) / sU, v29.P - 1)
        sign = np.where(L > 0, 1, np.where(U < 0, -1, 0))
        p = np.nan_to_num(np.where(L > 0, pl, np.where(U < 0, pu, 1.0)), nan=1.0)
        o = np.argsort(p, -1, kind="stable"); ps = np.take_along_axis(p, o, -1)
        r1 = ps[..., 0] <= v35.A_STAR / 2; r2 = r1 & (ps[..., 1] <= v35.A_STAR)
        rej = np.zeros_like(p, bool); np.put_along_axis(rej, o, np.stack([r1, r2], -1), -1)
        null = np.abs(tr) < 1e-9
        err = (rej & (null | (np.sign(tr) != sign))).any(-1).sum(0)
        pw = (rej & (sign == np.sign(tr)) & ~null).sum(0)
        hit = (L - v35.C_STAR * q * sL - zL <= tr) & (tr <= U + v35.C_STAR * q * sU + zU)
        undef = (~(np.isfinite(L) & np.isfinite(sL) & np.isfinite(U) & np.isfinite(sU) & np.isfinite(zL) & np.isfinite(zU))).any(-1).sum(0)
        ghit = (GL - v35.C_STAR * q * sGL <= gtr) & (gtr <= GU + v35.C_STAR * q * sGU)
        gfin = np.isfinite(GL) & np.isfinite(GU) & np.isfinite(sGL) & np.isfinite(sGU)
        ghw = np.where(gfin, ((GU + v35.C_STAR * q * sGU) - (GL - v35.C_STAR * q * sGL)) / 2, np.nan)
    hist = np.zeros((lev.shape[1], 512), np.int64)
    np.add.at(hist, (np.broadcast_to(np.arange(lev.shape[1]), lev.shape), lev), 1)
    r = dict(err=err, pw=pw, cov=hit.sum(0), undef=undef, gcov=ghit.sum(0), ghw=np.nanmean(ghw, 0), rule=hist)
    if ci == 0:                                                       # development samples, drawn once per frame
        dh = np.zeros((lev.shape[1], 512), np.int64); cfire = 0; yields = []; empty = 0
        for _ in range(N_DEV):
            cat, ns, nb = draw(rng, fr, rc, 3, fr.pi3)
            yields.append(nb / ns)
            cfire += nb < ns and stats.beta.ppf(0.95, nb + 1, ns - nb) < 0.7
            if cat is None:
                empty += 1; continue
            hu, au = _masks(cat, v35._SCORE[fi])
            dh[np.arange(lev.shape[1]), rule_levels(cat, hu, au, 3)] += 1
        r.update(dev_rule=dh, dev_cfire=cfire, dev_yield=np.mean(yields), dev_empty=empty)
    return fi, ci, tr, gtr, r


def inside(combo, maxi):
    la1, la2, lh = combo // 64, (combo // 8) % 8, combo % 8
    idx = {x: i for i, x in enumerate(GRID)}
    return any(la1 <= idx[a] and la2 <= idx[b] and lh <= idx[c] for a, b, c in maxi)


def region(passv):
    ok = {v: all(passv[w] for w in VECS if all(a <= b + 1e-12 for a, b in zip(w, v))) for v in VECS}
    dc = [v for v in VECS if ok[v]]
    return dc, [v for v in dc if not any(w != v and all(a >= b - 1e-12 for a, b in zip(w, v)) for w in dc)]


if __name__ == "__main__":
    init()
    names = [f[0] for f in v30.FRAMES]
    res = {}
    with mp.Pool(8, initializer=init) as pool:
        for fi, ci, tr, gtr, r in pool.imap_unordered(job, [(fi, ci) for fi in range(24) for ci in range(len(CONDS))]):
            res[fi, ci] = (tr, gtr, r)
    n = N_STUDIES
    m_err, m_cov, m_pw = 3 * NV * 24, len(CONDS) * NV * 24 * 2, NV * 24 * 2
    lines = [f"Frozen V33 procedure (Holm {v35.A_STAR}, multiplier {v35.C_STAR}) for 22 x (1, 6), two attempts; {n} studies per frame and condition; "
             f"{NV} ordered rate vectors x {NM} mechanisms; Bonferroni per mechanism over {m_err} error, {m_cov} coverage and {m_pw} power checks"]
    passes, worst, rows = {}, {}, []
    for mi, mech in enumerate(MECHS):
        passes[mech] = {}
        for vi, vec in enumerate(VECS):
            k = mi * NV + vi
            eub = max(v30.ucb(int(res[fi, ci][2]["err"][k]), n, m_err) for fi in range(24) for ci in (0, 1, 2))
            clb = min(v30.lcb(int(x), n, m_cov) for fi in range(24) for ci in range(len(CONDS)) for x in res[fi, ci][2]["cov"][k])
            plb = min(v30.lcb(int(x), n, m_pw) for fi in range(24) for x in res[fi, 4][2]["pw"][k])
            pmin = min(x / n for fi in range(24) for x in res[fi, 4][2]["pw"][k])
            und = max(res[fi, ci][2]["undef"][k] for fi in range(24) for ci in range(len(CONDS))) / n
            passes[mech][vec] = eub <= 0.05 and clb >= 0.95 and plb >= 0.60
            worst[mech, vec] = (eub, clb, plb, pmin, und)
            rows.append([mech, *vec, f"{eub:.4f}", f"{clb:.4f}", f"{pmin:.4f}", f"{plb:.4f}", f"{und:.5f}", int(passes[mech][vec])])
        dc, maxi = region(passes[mech])
        lines.append(f"\nMechanism: {mech}: {sum(passes[mech].values())} of {NV} vectors pass all three checks; downward-closed set {len(dc)} vectors; maximal: " + "; ".join(map(str, maxi)))
        lines.append(f"  worst error upper bound {max(worst[mech, v][0] for v in VECS):.4f}; worst coverage lower bound {min(worst[mech, v][1] for v in VECS):.4f}; worst undefined share {max(worst[mech, v][4] for v in VECS):.5f}")
    allpass = {v: all(passes[m][v] for m in MECHS) for v in VECS}
    dc, MAXI = region(allpass)
    lines.append(f"\nRegion passing under all four mechanisms: {len(dc)} vectors; maximal vectors (u_A1, u_A2, u_H): " + "; ".join(map(str, MAXI)))
    lines.append("\n+0.15 power, lowest point estimate / Bonferroni lower bound, by vector (columns: independent, task, protocol, difficulty); '*' fails a check")
    for vec in VECS:
        cells = []
        for mech in MECHS:
            eub, clb, plb, pmin, und = worst[mech, vec]
            cells.append(f"{pmin:.3f}/{plb:.3f}{'' if passes[mech][vec] else '*'}")
        lines.append(f"  {vec}: " + "  ".join(cells))
    lines.append("\nRule for evidence of leaving the region (frozen region above): share of studies in which it fires")
    for label, key, tot in (("main study, 22 protocols", "rule", n), ("development, 3 protocols", "dev_rule", N_DEV)):
        lines.append(f"  {label}:")
        for mi, mech in enumerate(MECHS):
            fire = {}
            for vi, vec in enumerate(VECS):
                k = mi * NV + vi
                cis = range(len(CONDS)) if key == "rule" else [0]
                h = sum(res[fi, ci][2][key][k] for fi in range(24) for ci in cis)
                fire[vec] = sum(h[c] for c in range(512) if not inside(c, MAXI)) / h.sum()
            ins = [fire[v] for v in VECS if v in dc]; outs = {v: fire[v] for v in VECS if v not in dc}
            sel = [(0.0, 0.0, 0.013), (0.0, 0.0, 0.02), (0.0, 0.0, 0.03), (0.0, 0.0, 0.065), (0.0075, 0.0075, 0.065), (0.013, 0.013, 0.013)]
            lines.append(f"    {mech}: inside the region, at most {max(ins):.3f}; outside: " + "; ".join(f"{v} {outs[v]:.3f}" for v in sel if v in outs))
    for yl in (0.9, 0.7):
        fis = [fi for fi in range(24) if f"yield {yl}" in names[fi]]
        cf = sum(res[fi, 0][2]["dev_cfire"] for fi in fis) / (N_DEV * len(fis))
        my = np.mean([res[fi, 0][2]["dev_yield"] for fi in fis])
        emp = sum(res[fi, 0][2]["dev_empty"] for fi in fis)
        lines.append(f"Development construction check (upper 95% limit of pooled yield below 0.7), frames with target yield {yl}: fires in {cf:.3f} of samples; mean development yield {my:.3f}; samples with nothing built {emp}")
    lines.append("\nRQ1a (independent mechanism, multiplier 1.175, not calibrated for RQ1a), by condition over frames and vectors")
    for ci, (cond, _) in enumerate(CONDS):
        cv = min(res[fi, ci][2]["gcov"][:NV].min() for fi in range(24)) / n
        hw = max(np.nanmax(res[fi, ci][2]["ghw"][:NV]) for fi in range(24))
        hw0 = max(np.nanmax(res[fi, ci][2]["ghw"][VECS.index((0.0, 0.0, 0.0))]) for fi in range(24))
        lines.append(f"  {cond}: lowest coverage {cv:.3f}; largest mean half-width {hw:.3f} (no unresolved outcome: {hw0:.3f})")
    lines.append("done")
    open("power_results_v37.txt", "w").write("\n".join(lines) + "\n")
    with open("power_results_v37_vectors.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["mechanism", "u_A1", "u_A2", "u_H", "error_upper_bound", "coverage_lower_bound", "lowest_power_015", "power_lower_bound_015", "worst_undefined_share", "passes"])
        wr.writerows(rows)
    print("\n".join(lines))
