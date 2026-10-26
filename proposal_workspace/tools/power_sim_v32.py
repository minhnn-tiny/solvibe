"""Version 32: round-19 structural fix (Loop 1 points R18.1 and R18.2).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v32.py
Two changes to power_sim_v31.py:
1. Rule for strata with no detected flaw (R18.1). When an author has no detected flaw in a stratum, the delete-one-protocol
   jackknife gives that rate a standard error of zero. The interval then adds, on the side that rate pushes, the stratum
   share times the exact one-sided 97.5% upper limit for a rate with zero events, 1 - 0.025^(1/n), where n is the number of
   resolved working implementations of that author in that stratum. Historical zero widens the lower end; agent zero widens
   the upper end of that configuration. The decision rule (Holm on the claimed-side bound) is unchanged.
2. Design screening (R18.2). The same ~900-hour budget is spent in different ways. Cost per protocol at the middle rates of
   power_sim_v22.py: setup 9 + f x 2.25 build + f x (1 + 2K) x 0.328 campaigns + V cap x 1.875 audit-assisted work,
   f = V cap + N take, K = attempts per configuration. Each design is screened on its own stream (1,000 studies per frame
   and condition): the Holm level is the largest grid value whose Bonferroni-adjusted Clopper-Pearson error bound is at most
   0.05 over all null conditions; then the +0.15 power lower bound at unresolved 0.013 (both authors and each author alone).
   The development record stays at 3 cases x 8 functions x 5 implementations = 120 outcomes in every design, so 0.013
   (zero unresolved outcomes in 120, upper 80% limit) is the best attainable readiness setting.
3. Full calibration (2,000 studies) and fresh validation (4,000 studies) on every condition, as in v31, for the (up to) three
   designs with the highest screening power bound among those at least 0.60. Unresolved settings include 0.0075, the upper 80% limit for zero in 216 outcomes.
Per-frame validation results go to power_results_v32_frames.csv.
"""
import csv
import multiprocessing as mp
import numpy as np
from scipy import stats
import power_sim_v29 as v29
import power_sim_v30 as v30

DESIGNS = [(20, 2, 6, 2), (23, 2, 6, 1), (23, 1, 6, 2), (24, 2, 4, 2), (27, 2, 4, 1), (26, 1, 6, 1), (29, 1, 4, 2), (33, 1, 4, 1)]
U_SET = [0.0, 0.005, 0.0075, 0.013, (0.0075, 0.0), (0.0, 0.0075), (0.013, 0.0), (0.0, 0.013)]
NULLS = [("exact null", 0.0, u) for u in U_SET] + [("partial null (0, +0.10)", (0.0, 0.10), 0.0)]
SCREEN = NULLS + [("exact +0.15", 0.15, u) for u in (0.013, (0.013, 0.0), (0.0, 0.013))]
CONDS = NULLS + [("exact +0.15", 0.15, u) for u in U_SET] + [("exact +0.10", 0.10, 0.0), ("exact +0.10", 0.10, 0.013), ("negative", "neg", 0.0), ("negative", "neg", 0.013)]


def cost(P, vcap, nper, k):
    f = vcap + nper
    return P * (9 + f * 2.25 + f * (1 + 2 * k) * 0.328 + vcap * 1.875)


def init(design):
    v29.P, v29.VCAP, v29.NPER, v29.K = design
    v30.init()


def study(rng, fr, recall, u):
    """power_sim_v29.study plus the zero-event widening terms zL (historical) and zU (agents), per configuration."""
    P, VCAP, NPER, K = v29.P, v29.VCAP, v29.NPER, v29.K
    sAV, sAN, sHV, sHN = recall
    u_a, u_h = (u, u) if np.isscalar(u) else u
    draws = v29.sys_pps(rng, fr.pi)
    assert len(set(draws.tolist())) == P
    A = np.zeros((2, 2, 3, P)); H = np.zeros((2, 3, P)); B = np.zeros((2, P))
    he = np.zeros(2); hn = np.zeros(2); ae = np.zeros((2, 2)); an = np.zeros((2, 2))
    for j, p in enumerate(draws):
        hh = 1.0 / fr.pi[p]
        for st, s in enumerate(("V", "N")):
            d = fr.f.get((p, s))
            if d is None:
                continue
            n = d["yh"].size; cap = VCAP if st == 0 else NPER
            idx = np.arange(n) if n <= cap else rng.choice(n, cap, replace=False)
            w = hh * n / idx.size
            idx = idx[d["built"][idx]]
            B[st, j] = w * idx.size
            if idx.size == 0:
                continue
            sA, sH = (sAV, sHV) if st == 0 else (sAN, sHN)
            hy = d["yh"][idx] & (rng.random(idx.size) < sH)
            hu = rng.random(idx.size) < u_h
            H[st, :, j] = w * np.array([(hy & ~hu).sum(), (~hu).sum(), hu.sum()])
            he[st] += (hy & ~hu).sum(); hn[st] += (~hu).sum()
            pa = fr.pa(s, d)[:, idx]
            for c in range(2):
                work = (rng.random((K, idx.size)) < 0.9) & (rng.random((K, idx.size)) < 0.8)
                y = work & (rng.random((K, idx.size)) < pa[c]) & (rng.random((K, idx.size)) < sA)
                au = rng.random((K, idx.size)) < u_a
                A[st, c, :, j] = w * np.array([(y & ~au).sum(), (work & ~au).sum(), au.sum()])
                ae[st, c] += (y & ~au).sum(); an[st, c] += (work & ~au).sum()

    def bounds(m):
        shr_v = (B[0] * m).sum(-1); shr = (shr_v / (shr_v + (B[1] * m).sum(-1)))[..., None]
        out = []
        for st in (0, 1):
            Ay, Aw, Au = [(A[st, :, i] * m[..., None, :]).sum(-1) for i in range(3)]
            Hy, Hw, Hu = [((H[st, i] * m).sum(-1))[..., None] for i in range(3)]
            out.append((Ay / (Aw + Au) - (Hy + Hu) / (Hw + Hu), (Ay + Au) / (Aw + Au) - Hy / (Hw + Hu)))
        return shr * out[0][0] + (1 - shr) * out[1][0], shr * out[0][1] + (1 - shr) * out[1][1], shr
    with np.errstate(invalid="ignore", divide="ignore"):
        L0, U0, shr = bounds(np.ones(P)); Lj, Uj, _ = bounds(1.0 - np.eye(P))
        seL = np.sqrt((P - 1) / P * ((Lj - np.nanmean(Lj, 0)) ** 2).sum(0))
        seU = np.sqrt((P - 1) / P * ((Uj - np.nanmean(Uj, 0)) ** 2).sum(0))
        ucl = lambda n: np.where(n > 0, 1 - 0.025 ** (1 / np.maximum(n, 1)), np.nan)
        share = np.array([shr[0], 1 - shr[0]])
        zL = np.full(2, sum(share[st] * ucl(hn[st]) for st in (0, 1) if he[st] == 0))
        zU = np.array([sum(share[st] * ucl(an[st, c]) for st in (0, 1) if ae[st, c] == 0) for c in range(2)])
    return L0, seL, U0, seU, zL, zU


def job(args):
    seed, fi, ci, conds, n = args
    name, rc, fr = v30.FRAMES[fi]
    cond, target, u = conds[ci]
    if target == "neg":
        target = np.maximum(-0.05, 0.5 * fr.truth(rc, np.full(2, -15.0)))
    tr = fr.set_target(rc, target)
    rng = np.random.default_rng([seed, fi, ci])
    res = [study(rng, fr, rc, u) for _ in range(n)]
    return fi, ci, tr, np.array([[r[i] for r in res] for i in range(6)])     # shape (6, n, 2)


def cover(R, tr, c):
    L, sL, U, sU, zL, zU = R
    q = stats.t.ppf(0.975, v29.P - 1)
    with np.errstate(invalid="ignore"):
        hit = (L - c * q * sL - zL <= tr) & (tr <= U + c * q * sU + zU)    # NaN compares False: undefined counts as a miss
    return hit.mean(0), hit.all(1).mean(), (~np.isfinite(R[:4]).all(0)).any(1).mean()


_decide = v30.decide
v30.cover = cover                                       # v30.check looks both up at call time
v30.decide = lambda R, tr, a: _decide(R[:4], tr, a)     # the decision ignores the zero-event terms


def run(pool, seed, conds, n):
    jobs = [(seed, fi, ci, conds, n) for fi in range(len(v30.FRAMES)) for ci in range(len(conds))]
    return {(fi, ci): (tr, R) for fi, ci, tr, R in pool.imap_unordered(job, jobs)}


def holm_level(out, conds, n):
    return next((a for a in v30.ALPHAS if v30.check(out, conds, n, a, v30.CS[-1])[0]["err"] <= 0.05), None)


if __name__ == "__main__":
    print("Screening (1,000 studies per frame and condition; 24 frames; Holm level from the null conditions; +0.15 power bound at unresolved 0.013)", flush=True)
    passed = []
    for k, d in enumerate(DESIGNS):
        tag = f"{d[0]} protocols, V cap {d[1]}, N take {d[2]}, {d[3]} attempt(s) per configuration ({cost(*d):.0f} h at middle rates)"
        init(d)
        with mp.Pool(8, initializer=init, initargs=(d,)) as pool:
            out = run(pool, 3301 + k, SCREEN, 1000)
        a = holm_level(out, SCREEN, 1000)
        if a is None:
            print(f"  {tag}: no Holm level passes", flush=True); continue
        w, rows, m = v30.check(out, SCREEN, 1000, a, v30.CS[-1])
        pts = [rows[key][2].min() for key in rows if SCREEN[key[1]][0] == "exact +0.15"]
        print(f"  {tag}: Holm level {a}; +0.15 power at unresolved 0.013: lowest point estimate {min(pts):.3f}, lower bound {w['pw']:.3f}", flush=True)
        if w["pw"] >= 0.60:
            passed.append((w["pw"], k, d, tag))
    passed = [x[1:] for x in sorted(passed, reverse=True)[:3]]      # full runs for the three best screened designs
    fh = open("power_results_v32_frames.csv", "w", newline="")
    wr = csv.writer(fh)
    wr.writerow(["design", "frame", "condition", "unresolved", "target_c1", "target_c2", "studies", "familywise_error", "power_c1", "power_c2", "coverage_c1", "coverage_c2", "simultaneous_coverage", "undefined_share"])
    for k, d, tag in passed:
        init(d)
        names = [f[0] for f in v30.FRAMES]
        with mp.Pool(8, initializer=init, initargs=(d,)) as pool:
            cal = run(pool, 3401 + k, CONDS, 2000)
            a_star = holm_level(cal, CONDS, 2000)
            c_star = next((c for c in v30.CS if v30.check(cal, CONDS, 2000, v30.ALPHAS[0], c)[0]["cov"] >= 0.95), None)
            if a_star is None or c_star is None:
                print(f"  {tag}: calibration failed (Holm level {a_star}, multiplier {c_star})", flush=True); continue
            w, _, m = v30.check(cal, CONDS, 2000, a_star, c_star)
            print(f"  {tag}: selected Holm level {a_star}, multiplier {c_star}; calibration bounds: error {w['err']:.4f}, coverage {w['cov']:.4f}, +0.15 power {w['pw']:.3f}", flush=True)
            val = run(pool, 3501 + k, CONDS, 4000)
        w, rows, m = v30.check(val, CONDS, 4000, a_star, c_star)
        print(f"  {tag}, validation (fresh draws, procedure frozen):")
        print(f"    worst family-wise error upper bound {w['err']:.4f} over {m[0]} null checks (<= 0.05): {'pass' if w['err'] <= 0.05 else 'FAIL'}")
        print(f"    worst marginal coverage lower bound {w['cov']:.4f} over {m[1]} checks (>= 0.95): {'pass' if w['cov'] >= 0.95 else 'FAIL'}")
        print(f"    worst +0.15 power lower bound {w['pw']:.3f} over {m[2]} checks, all unresolved settings (>= 0.60): {'pass' if w['pw'] >= 0.60 else 'FAIL'}")
        for ci, (cond, target, u) in enumerate(CONDS):
            ks = [key for key in rows if key[1] == ci]
            e = max(rows[key][1] for key in ks); cv = min(rows[key][3].min() for key in ks); sim = min(rows[key][4] for key in ks); und = max(rows[key][5] for key in ks)
            line = f"    {cond}, unresolved {u}: worst error {e:.3f}; lowest marginal coverage {cv:.3f}; lowest simultaneous coverage {sim:.3f}; undefined share up to {und:.4f}"
            pws = np.array([rows[key][2].min() for key in ks if np.all(np.abs(rows[key][0]) > 1e-9)])
            if pws.size:
                line += f"; minimum configuration power lowest {pws.min():.3f}, quartiles {np.percentile(pws, 25):.2f} / {np.median(pws):.2f} / {np.percentile(pws, 75):.2f}"
            print(line, flush=True)
        for (fi, ci), (tr, e, pw, cv, sim, und) in sorted(rows.items()):
            cond, _, u = CONDS[ci]
            wr.writerow([tag, names[fi], cond, u, f"{tr[0]:.4f}", f"{tr[1]:.4f}", 4000, f"{e:.4f}", f"{pw[0]:.4f}", f"{pw[1]:.4f}", f"{cv[0]:.4f}", f"{cv[1]:.4f}", f"{sim:.4f}", f"{und:.4f}"])
        fh.flush()
    fh.close()
    print("done")
