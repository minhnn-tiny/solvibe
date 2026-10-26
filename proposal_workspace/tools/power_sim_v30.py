"""Version 30: calibration with Monte Carlo confidence bounds and a separate, fresh validation (round-18 Major point, C6;
proposal_v19 section 6.3 "Required calibration correction").

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v30.py
Same 24 frames, sampling design, estimator and decision as power_sim_v29.py (frames are built from seed 2901 exactly as in
v29). What changes:
- Calibration stream (seed 3001, 2,000 studies per frame and condition) covers every retained condition used for the
  requirements: exact nulls with unresolved shares (0, 0), (0.005, 0.005), (0.013, 0.013), (0.013, 0), (0, 0.013), the
  partial null (0, +0.10), and exact +0.15 at the same five unresolved settings.
- Selection uses one-sided Clopper-Pearson bounds with a Bonferroni adjustment over the checks of each kind:
  Holm level = the largest grid value whose family-wise error upper bound is at most 0.05 in every null check;
  interval multiplier = the smallest grid value whose coverage lower bound is at least 0.95 in every check (per
  configuration, unconditional: an undefined interval counts as not covering). There is no fallback: if no grid value
  passes, the script prints that calibration failed and stops.
- Power requirement (proposal_v19): correct directional power at exactly +0.15 of at least 0.60 for each configuration in
  every retained scenario, shown by the Bonferroni-adjusted Clopper-Pearson lower bound.
- Validation stream (seed 3002, 4,000 studies per frame and condition) is drawn after the procedure is frozen; it repeats
  the calibration conditions and adds exact +0.10 and a feasible negative alternative (both at unresolved 0 and 0.013).
  The negative target is max(-0.05, half the lowest attainable contrast of the frame); the lowest attainable contrast is
  the frame's contrast when both agent configurations have N-stratum vulnerability near zero.
- Every frame-and-condition result is saved to power_results_v30_frames.csv.
"""
import csv
import multiprocessing as mp
import numpy as np
from scipy import stats
import power_sim_v8 as v8
import power_sim_v29 as v29

ALPHAS = np.round(np.arange(0.05, 0.0099, -0.0025), 4)
CS = np.round(np.arange(1.0, 2.001, 0.025), 3)
U_SET = [0.0, 0.005, 0.013, (0.013, 0.0), (0.0, 0.013)]
CAL_CONDS = [("exact null", 0.0, u) for u in U_SET] + [("partial null (0, +0.10)", (0.0, 0.10), 0.0)] + [("exact +0.15", 0.15, u) for u in U_SET]
VAL_CONDS = CAL_CONDS + [("exact +0.10", 0.10, 0.0), ("exact +0.10", 0.10, 0.013), ("negative", "neg", 0.0), ("negative", "neg", 0.013)]
FRAMES = None


def build_frames():
    rng = np.random.default_rng(2901)
    out = []
    for vname, vlist in (("upper", v29.V_REC), ("observed", v29.V_OBS)):
        for rname, rc in v29.RECALLS.items():
            for hN in (0.05, 0.10):
                for link, yld in ((0.0, 0.9), (0.6, 0.7)):
                    out.append((f"{vname}, recall {rname}, hN {hN}, link {link}, yield {yld}", rc, v29.Frame(rng, vlist, hN, link, yld)))
    return out


def init():
    global FRAMES
    FRAMES = build_frames()


def job(args):
    seed, fi, ci, conds, n = args
    name, rc, fr = FRAMES[fi]
    cond, target, u = conds[ci]
    if target == "neg":
        tmin = fr.truth(rc, np.full(2, -15.0))
        target = np.maximum(-0.05, 0.5 * tmin)
    tr = fr.set_target(rc, target)
    rng = np.random.default_rng([seed, fi, ci])
    res = [v29.study(rng, fr, rc, u) for _ in range(n)]
    return fi, ci, tr, np.array([[r[i] for r in res] for i in range(4)])   # shape (4, n, 2)


def pvals(R):
    L, sL, U, sU = R
    with np.errstate(invalid="ignore", divide="ignore"):
        pl, pu = 2 * stats.t.sf(np.abs(L) / sL, v29.P - 1), 2 * stats.t.sf(np.abs(U) / sU, v29.P - 1)
    sign = np.where(L > 0, 1, np.where(U < 0, -1, 0))
    p = np.nan_to_num(np.where(L > 0, pl, np.where(U < 0, pu, 1.0)), nan=1.0)
    return p, sign


def holm2(p, a):
    """Holm across the two configurations, vectorized over studies (same decisions as power_sim_v8.holm)."""
    o = np.argsort(p, axis=1, kind="stable"); ps = np.take_along_axis(p, o, 1)
    r1 = ps[:, 0] <= a / 2; r2 = r1 & (ps[:, 1] <= a)
    rej = np.zeros_like(p, dtype=bool); np.put_along_axis(rej, o, np.stack([r1, r2], 1), 1)
    return rej


def decide(R, tr, a):
    p, sign = pvals(R)
    rej = holm2(p, a)
    null = np.abs(tr) < 1e-9
    err = (rej & (null | (np.sign(tr) != sign))).any(1)
    pw = (rej & (sign == np.sign(tr)) & ~null).mean(0)
    return err.mean(), pw


def cover(R, tr, c):
    L, sL, U, sU = R
    q = stats.t.ppf(0.975, v29.P - 1)
    with np.errstate(invalid="ignore"):
        hit = (L - c * q * sL <= tr) & (tr <= U + c * q * sU)          # NaN compares False: undefined counts as a miss
    return hit.mean(0), hit.all(1).mean(), (~np.isfinite(R).all(0)).any(1).mean()


def ucb(k, n, m):          # one-sided Clopper-Pearson upper bound, Bonferroni over m checks, family confidence 0.95
    return 1.0 if k == n else stats.beta.ppf(1 - 0.05 / m, k + 1, n - k)


def lcb(k, n, m):
    return 0.0 if k == 0 else stats.beta.ppf(0.05 / m, k, n - k + 1)


def run(pool, seed, conds, n):
    jobs = [(seed, fi, ci, conds, n) for fi in range(len(FRAMES)) for ci in range(len(conds))]
    return {(fi, ci): (tr, R) for fi, ci, tr, R in pool.imap_unordered(job, jobs)}


def check(out, conds, n, a, c):
    """Worst Bonferroni-adjusted bounds for the three requirements, and the per-check rows."""
    nulls = [k for k in out if conds[k[1]][0] != "exact +0.15" and np.any(np.abs(out[k][0]) < 1e-9)]
    pos15 = [k for k in out if conds[k[1]][0] == "exact +0.15"]
    m_err, m_cov, m_pw = len(nulls), 2 * len(out), 2 * len(pos15)
    rows, worst = {}, dict(err=0.0, cov=1.0, pw=1.0)
    for k, (tr, R) in out.items():
        e, pw = decide(R, tr, a); cv, sim, und = cover(R, tr, c)
        rows[k] = (tr, e, pw, cv, sim, und)
        if k in nulls:
            worst["err"] = max(worst["err"], ucb(round(e * n), n, m_err))
        worst["cov"] = min(worst["cov"], min(lcb(round(x * n), n, m_cov) for x in cv))
        if k in pos15:
            worst["pw"] = min(worst["pw"], min(lcb(round(x * n), n, m_pw) for x in pw))
    return worst, rows, (m_err, m_cov, m_pw)


if __name__ == "__main__":
    init()
    names = [f[0] for f in FRAMES]
    with mp.Pool(8, initializer=init) as pool:
        n_cal, n_val = 2000, 4000
        cal = run(pool, 3001, CAL_CONDS, n_cal)
        print(f"Calibration: {len(FRAMES)} frames x {len(CAL_CONDS)} conditions x {n_cal} studies; Bonferroni-adjusted one-sided Clopper-Pearson bounds, family confidence 0.95", flush=True)
        a_star = c_star = None
        for a in ALPHAS:
            w, _, m = check(cal, CAL_CONDS, n_cal, a, CS[-1])
            print(f"  Holm level {a}: worst error upper bound {w['err']:.4f} ({m[0]} null checks); worst +0.15 power lower bound {w['pw']:.3f} ({m[2]} checks)", flush=True)
            if a_star is None and w["err"] <= 0.05:
                a_star = a
        for c in CS:
            w, _, m = check(cal, CAL_CONDS, n_cal, ALPHAS[0], c)
            if w["cov"] >= 0.95:
                c_star = c; break
        if a_star is None or c_star is None:
            print(f"Calibration failed: Holm level {a_star}, multiplier {c_star}; no inferential procedure is selected.")
            raise SystemExit(1)
        w, _, m = check(cal, CAL_CONDS, n_cal, a_star, c_star)
        print(f"Selected: Holm level {a_star}; interval multiplier {c_star}. Calibration bounds: error {w['err']:.4f}, coverage {w['cov']:.4f} ({m[1]} checks), +0.15 power {w['pw']:.3f}", flush=True)
        val = run(pool, 3002, VAL_CONDS, n_val)
    w, rows, m = check(val, VAL_CONDS, n_val, a_star, c_star)
    print(f"Validation (fresh draws, procedure frozen): {len(FRAMES)} frames x {len(VAL_CONDS)} conditions x {n_val} studies")
    print(f"  worst family-wise error upper bound {w['err']:.4f} over {m[0]} null checks (requirement <= 0.05): {'pass' if w['err'] <= 0.05 else 'FAIL'}")
    print(f"  worst marginal coverage lower bound {w['cov']:.4f} over {m[1]} checks (requirement >= 0.95): {'pass' if w['cov'] >= 0.95 else 'FAIL'}")
    print(f"  worst +0.15 power lower bound {w['pw']:.3f} over {m[2]} checks (requirement >= 0.60): {'pass' if w['pw'] >= 0.60 else 'FAIL'}")
    for ci, (cond, target, u) in enumerate(VAL_CONDS):
        ks = [k for k in rows if k[1] == ci]
        e = max(rows[k][1] for k in ks); cv = min(rows[k][3].min() for k in ks); sim = min(rows[k][4] for k in ks); und = max(rows[k][5] for k in ks)
        line = f"  {cond}, unresolved {u}: worst error {e:.3f}; lowest marginal coverage {cv:.3f}; lowest simultaneous coverage {sim:.3f}; undefined share up to {und:.4f}"
        pws = np.array([rows[k][2].min() for k in ks if np.all(np.abs(rows[k][0]) > 1e-9)])
        if pws.size:
            line += f"; minimum configuration power lowest {pws.min():.3f}, quartiles {np.percentile(pws, 25):.2f} / {np.median(pws):.2f} / {np.percentile(pws, 75):.2f}"
        if target == "neg":
            t = np.array([rows[k][0] for k in ks])
            line += f"; targets {t.min():+.3f} to {t.max():+.3f} (target reached -0.05 in {int((t <= -0.05 + 1e-6).all(1).sum())} of {len(ks)} frames)"
        print(line)
    with open("power_results_v30_frames.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["frame", "condition", "unresolved", "target_c1", "target_c2", "studies", "familywise_error", "power_c1", "power_c2", "coverage_c1", "coverage_c2", "simultaneous_coverage", "undefined_share"])
        for (fi, ci), (tr, e, pw, cv, sim, und) in sorted(rows.items()):
            cond, _, u = VAL_CONDS[ci]
            wr.writerow([names[fi], cond, u, f"{tr[0]:.4f}", f"{tr[1]:.4f}", n_val, f"{e:.4f}", f"{pw[0]:.4f}", f"{pw[1]:.4f}", f"{cv[0]:.4f}", f"{cv[1]:.4f}", f"{sim:.4f}", f"{und:.4f}"])
    print("done")
