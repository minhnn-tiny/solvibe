"""Version 44: an explicit confirmation-and-review state machine for the fixed reserves (round-27 points R27.1 to R27.5).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v44.py
Base: power_sim_v42.py (frames of 230 protocols less three development protocols, three frame groups, frozen estimator
with the empty-stratum rule and rates bounded by 0 and 1, jackknife over every sampled protocol, Holm 0.03, multiplier
1.175, reading of the upper limit at Holm 0.01). State machine, applied to each source (main study, development):
 1. Registration. Only implementations with known working status 1 (agents: compiled and passing ordinary checks;
    historical: passing ordinary checks) register a bundle: their first three candidates in frozen order. A known
    non-working implementation keeps (W, D) = (0, 0); its candidates are closed without confirmation (R27.1).
 2. Candidates. A working implementation with a detected flaw has k_pos candidates (1 or 3) with the confirming candidate at
    a uniform position; a working implementation without one has Binomial(3, R / 3) rejected candidates, with R = 3/13, the
    higher pilot rate, fixed for the scenario and independent of the sample (R27.3).
 3. Confirmation order and admission. Bundles are processed in a random order. A bundle starts only if the reserve holds
    1.0 hour for each of its candidates; otherwise processing stops, and every candidate of this and every later bundle is
    "unfinished: reserve".
 4. Within a bundle, candidates are processed in order. A rejected candidate is "rejected". The first candidate whose PoV
    executes and whose body-only correction blocks it is "student-confirmed"; the bundle stops there, and later candidates
    are "not needed". Time used: 0.5 or 1.0 hour per candidate, or 1.0 for the confirming and 0.5 for rejected candidates.
    Reserved but unused time returns to the reserve when the bundle ends.
 5. Review. Student-confirmed packages are reviewed in a random order, 0.5 hours per package per adjudicator, up to the
    review reserve; a package beyond it is "unfinished: review". The simulation assumes that the student confirms only
    true flaws and that completed reviews confirm them (stated simplification; adjudicator inability is the separate
    package mechanism).
 6. Outcome. Positive if a package is confirmed; unresolved (with W = 1 known) if no package is confirmed and a candidate is
    "unfinished"; otherwise not confirmed. Unknown-working-status mechanisms (independent, task, protocol, difficulty) and
    the package mechanism are combined with this outcome as in V42.
 7. Warning (R27.5). Per author, the denominator is candidate records with an assessment status (rejected,
    student-confirmed, unfinished), excluding "not needed" and closed candidates of non-working implementations; the
    numerator is records "unfinished: reserve", packages "unfinished: review", packages unresolved by the package mechanism,
    and records of implementations whose outcome an unknown-working-status mechanism makes unresolved. Fires when the
    one-sided 95% Clopper-Pearson lower limit exceeds 0.05 for a configuration or 0.2 for historical code. An author with
    no record is unassessable; development samples with nothing built are counted as unassessable, not dropped.
Reserves: main 177.7 confirmation hours and 178 review packages; development 24.2 hours and 25 packages.
Scenarios: positive bundle 1 or 3 x time mode 0.5, 1.0 or adverse: 6 (R = 3/13 only; 8/64 gives less demand).
Checks: every V42 condition (exact null, both partial nulls, +0.025, the three margin conditions, +0.10, +0.15, negative).
For every scenario: the V42 region corners of each mechanism. For the binding scenario (three-candidate bundles at 0.5 hour
each: with the fixed rejected rate it is, with one-candidate adverse time, the passing scenario with most demand,
per power_results_v44_demand.txt): the full V42 grids (76 ordered vectors for four mechanisms,
64 per-package vectors). 4,000 studies per frame and condition (seed 4401), 4,000 development samples per frame. (A first run with 2,000 is kept as power_results_v44_2000.txt; its Bonferroni bounds were too wide to certify the limits.)
Outputs: power_results_v44.txt, power_results_v44_vectors.csv.
"""
import csv
import itertools
import multiprocessing as mp
import os
import numpy as np
from scipy import stats
import power_sim_v30 as v30
import power_sim_v42 as v42

K, P = v42.K, v42.P
R_REJ = 3 / 13
SCEN = list(itertools.product((1, 3), ("0.5", "1.0", "adverse")))
BIND = SCEN.index((3, "0.5"))
CORNERS = [("none", None)] + [(m, v) for m in ("independent", "task", "protocol", "difficulty") for v in ((0.0075, 0.0075, 0.0075), (0.013, 0.013, 0.005))] + [("package", (0.05, 0.05, 0.2))]
NS, NC = len(SCEN), len(CORNERS)
NFULL = int(v42.OFF[-1])
MVT = NS * NC + NFULL
CONDS, NULLC, POW15, READERR = v42.CONDS, v42.NULLC, v42.POW15, v42.READERR
RES_MAIN, RES_DEV = (177.7, 178), (24.2, 25)
N_STUDIES, N_DEV = 4000, 4000
LIMITS = np.array([0.05, 0.05, 0.2])
_full_masks = v42.masks
_CACHE = {}
v42.masks = lambda cat, bmap: _CACHE["m"]
v42.pkg_counts = lambda cat, hu, au: (None, None)


def init():
    v42.init(dict(sizes=(230,), zero_share=True, n_studies=N_STUDIES, rd_levels=[0.01], vacuous=True, groups=None, n_dev=N_DEV))


def corner_masks(cat, bmap):
    nf = cat["hy"].size
    hs, as_ = [], []
    for mech, vec in CORNERS:
        if mech == "none":
            hs.append(np.zeros(nf, bool)); as_.append(np.zeros((2, K, nf), bool)); continue
        uA, uH = np.array(vec[:2])[:, None, None], vec[2]
        if mech == "independent":
            h, a = cat["Uh"] < uH, cat["Ua"] < uA
        elif mech == "task":
            h, a = cat["Ut"] < uH, np.broadcast_to(cat["Ut"] < uA, (2, K, nf))
        elif mech == "protocol":
            h, a = cat["Up"] < uH, np.broadcast_to(cat["Up"] < uA, (2, K, nf))
        elif mech == "difficulty":
            bA = np.array([bmap[x] for x in vec[:2]])[:, None, None]
            with np.errstate(over="ignore"):
                h = cat["Uh"] < v42.expit(bmap[uH] + cat["score"]); a = cat["Ua"] < v42.expit(bA + cat["score"][None, None])
        else:
            h, a = cat["hy"] & (cat["Uh"] < uH), cat["ay"] & (cat["Ua"] < uA)
        hs.append(h); as_.append(np.asarray(a))
    return np.array(hs), np.array(as_)


def machine(rng, pos, work, reserve, k_pos, mode):
    """State machine over implementations. Returns per implementation: unresolved-by-reserve, and record counts."""
    M = pos.size
    k = np.where(work, np.where(pos, k_pos, rng.binomial(3, R_REJ / 3, M)), 0)
    jpos = rng.integers(1, k_pos + 1, M)
    c_rej, c_conf = {"0.5": (0.5, 0.5), "1.0": (1.0, 1.0), "adverse": (0.5, 1.0)}[mode]
    cost = np.where(pos, (jpos - 1) * c_rej + c_conf, k * c_rej)
    assessed = np.where(pos, jpos, k)                                     # records with an assessment status if processed
    idx = np.flatnonzero(k > 0)
    order = idx[rng.permutation(idx.size)]
    before = np.concatenate([[0.0], np.cumsum(cost[order])[:-1]])
    stop = reserve[0] - before < k[order] * 1.0
    first = int(np.argmax(stop)) if stop.any() else order.size
    unf = np.zeros(M, bool); unf[order[first:]] = True
    pk = order[:first][pos[order[:first]]]
    pk = pk[rng.permutation(pk.size)]
    unrev = np.zeros(M, bool); unrev[pk[int(reserve[1]):]] = True
    rec = np.where(unf, k, assessed)                                      # denominator records per implementation
    rec_unf = np.where(unf, k, 0) + unrev                                 # unfinished records per implementation
    return unf | unrev, rec, rec_unf, bool(stop.any()), pk.size > reserve[1]


def build(rng, cat, bmap, reserve, full):
    hy, ay, hw, aw = cat["hy"], cat["ay"], cat["hw"], cat["aw"]
    nf = hy.size
    pos = np.concatenate([hy, ay.ravel()]); work = np.concatenate([hw, aw.ravel()])
    author = np.concatenate([np.full(nf, 2), np.repeat([0, 1], K * nf)])
    ch, ca = corner_masks(cat, bmap)
    cflat = np.concatenate([ch, ca.reshape(NC, -1)], 1)
    HU, AU, X, N, FL = [], [], [], [], []
    keep = None
    for si, (k_pos, mode) in enumerate(SCEN):
        ex, rec, rec_unf, st_c, st_r = machine(rng, pos, work, reserve, k_pos, mode)
        comb = cflat | ex[None]
        HU.append(comb[:, :nf]); AU.append(comb[:, nf:].reshape(NC, 2, K, nf))
        mech_rec = np.where(~ex & cflat, np.where(pos, 1, rec), 0)        # records left unresolved by an added mechanism
        x = rec_unf[None] + mech_rec
        X.append(np.stack([(x * (author == a)).sum(1) for a in (0, 1, 2)], 1))
        N.append(np.array([rec[author == a].sum() for a in (0, 1, 2)]))
        FL.append((st_c, st_r))
        if si == BIND:
            keep = ex
    if full:
        fh, fa = _full_masks(cat, bmap)
        HU.append(fh | keep[:nf][None]); AU.append(fa | keep[nf:].reshape(2, K, nf)[None])
    return np.concatenate(HU), np.concatenate(AU), np.array(X), np.array(N), np.array(FL)


def warn(X, N):
    Nb = np.broadcast_to(N[:, :, None, :], X.shape)
    with np.errstate(invalid="ignore", divide="ignore"):
        lo = np.where(X > 0, stats.beta.ppf(0.05, np.maximum(X, 1), np.maximum(Nb - X + 1, 1)), 0.0)
    fire = ((lo > LIMITS) & (Nb > 0)).any(-1)
    return fire.sum(0), (N == 0).any(-1).sum(0)


def job(args):
    fi, ci = args
    size, group, name, rc, spec = v42.FRAMES[fi]
    fr = v42.Frame(*spec)
    cond, target = CONDS[ci]
    if target == "neg":
        target = np.maximum(-0.05, 0.5 * fr.truth(rc, np.full(2, -15.0)))
    tr = fr.set_target(rc, np.array(target, float))
    rng = np.random.default_rng([4401, fi, ci])
    outs, Xs, Ns, FLs, unres = [], [], [], [], []
    for _ in range(N_STUDIES):
        cat = v42.draw(rng, fr, rc)
        hu, au, X, N, FL = build(rng, cat, fr.bmap, RES_MAIN, True)
        _CACHE["m"] = (hu, au)
        outs.append(v42.evaluate(cat, fr.bmap)[:7]); Xs.append(X); Ns.append(N); FLs.append(FL)
        unres.append(np.stack([au[:, 0].mean((-1, -2)), au[:, 1].mean((-1, -2)), hu.mean(-1)], 1)[: NS * NC])
    L, sL, U, sU, zL, zU = (np.array([o[i] for o in outs]) for i in range(6))
    dfb = (np.array([o[6] for o in outs]) - 1.0)[:, None, None]
    with np.errstate(invalid="ignore", divide="ignore"):
        q = stats.t.ppf(0.975, dfb)
        pl, pu = 2 * stats.t.sf(np.abs(L) / sL, dfb), 2 * stats.t.sf(np.abs(U) / sU, dfb)
        sign = np.where(L > 0, 1, np.where(U < 0, -1, 0))
        p = np.nan_to_num(np.where(L > 0, pl, np.where(U < 0, pu, 1.0)), nan=1.0)
        rej = v42.holm2(p, v42.A_STAR)
        null = np.abs(tr) < 1e-9
        err = (rej & (null | (np.sign(tr) != sign))).any(-1).sum(0)
        pw = (rej & (sign == np.sign(tr)) & ~null).sum(0)
        hit = (L - v42.C_STAR * q * sL - zL <= tr) & (tr <= U + v42.C_STAR * q * sU + zU)
        undef = (~(np.isfinite(L) & np.isfinite(sL) & np.isfinite(U) & np.isfinite(sU) & np.isfinite(zL) & np.isfinite(zU))).any(-1).sum(0)
        pr = np.nan_to_num(stats.t.cdf((U + zU - v42.MARGIN) / sU, dfb), nan=1.0)
        rd = v42.holm2(pr, 0.01)
        rd_err = (rd & (tr >= v42.MARGIN - 1e-9)).any(-1).sum(0)
    fire, unass = warn(np.array(Xs), np.array(Ns))
    r = dict(err=err, pw=pw, cov=hit.sum(0), undef=undef, rd_err=rd_err, fire=fire, unass=unass, flags=np.array(FLs).sum(0), unres=np.mean(unres, 0))
    if ci == 0:
        dX, dN, empty = [], [], 0
        for _ in range(N_DEV):
            cat = v42.draw(rng, fr, rc, 3, fr.pi3)
            if cat is None:
                empty += 1; continue
            _, _, X, N, _ = build(rng, cat, fr.bmap, RES_DEV, False)
            dX.append(X); dN.append(N)
        dfire, dun = warn(np.array(dX), np.array(dN))
        r["dev"] = dict(fire=dfire, unass=dun + empty, n=N_DEV)
    return fi, ci, r


def region(passv, vecs):
    ok = {v: all(passv[w] for w in vecs if all(a <= b + 1e-12 for a, b in zip(w, v))) for v in vecs}
    dc = [v for v in vecs if ok[v]]
    return dc, [v for v in dc if not any(w != v and all(a >= b - 1e-12 for a, b in zip(w, v)) for w in dc)]


if __name__ == "__main__":
    init()
    nfr = len(v42.FRAMES)
    res = {}
    with mp.Pool(8, initializer=init) as pool:
        for fi, ci, r in pool.imap_unordered(job, [(fi, ci) for fi in range(nfr) for ci in range(len(CONDS))], chunksize=1):
            res[fi, ci] = r
    import pickle
    pickle.dump(res, open(os.path.join(os.environ["CLAUDE_JOB_DIR"], "tmp", "power_results_v44_raw.pkl") if os.environ.get("CLAUDE_JOB_DIR") else "power_results_v44_raw.pkl", "wb"))
    n = N_STUDIES
    lines = [f"V44: state machine for fixed reserves; rejected-candidate rate {R_REJ:.4f} fixed per scenario; {nfr} frames of 230; frozen estimator; {n} studies per frame and condition; reserves main {RES_MAIN}, development {RES_DEV}"]
    rows = []

    def checks(k, m_err, m_cov, m_pw, m_rd):
        eub = max(v30.ucb(int(res[fi, ci]["err"][k]), n, m_err) for fi in range(nfr) for ci in NULLC)
        clb = min(v30.lcb(int(x), n, m_cov) for fi in range(nfr) for ci in range(len(CONDS)) for x in res[fi, ci]["cov"][k])
        plb = min(v30.lcb(int(x), n, m_pw) for fi in range(nfr) for x in res[fi, POW15]["pw"][k])
        pmin = min(x / n for fi in range(nfr) for x in res[fi, POW15]["pw"][k])
        rub = max(v30.ucb(int(res[fi, ci]["rd_err"][k]), n, m_rd) for fi in range(nfr) for ci in READERR)
        und = max(res[fi, ci]["undef"][k] for fi in range(nfr) for ci in range(len(CONDS))) / n
        return eub, clb, pmin, plb, rub, und

    m = (3 * NC * nfr, len(CONDS) * NC * nfr * 2, NC * nfr * 2, len(READERR) * NC * nfr)
    lines.append(f"Region corners, every scenario (Bonferroni per scenario over {m[0]} error, {m[1]} coverage, {m[2]} power and {m[3]} reading checks)")
    for si, (k_pos, mode) in enumerate(SCEN):
        fl0 = sum(res[fi, 0]["flags"][si] for fi in range(nfr)) / (n * nfr); fl15 = sum(res[fi, POW15]["flags"][si] for fi in range(nfr)) / (n * nfr)
        un = sum(res[fi, 0]["dev"]["unass"][si] for fi in range(nfr)) / (N_DEV * nfr)
        lines.append(f"\npositive bundle {k_pos}, time {mode}: confirmation reserve ran out in {fl0[0]:.3f} (null) / {fl15[0]:.3f} (+0.15); review reserve in {fl0[1]:.3f} / {fl15[1]:.3f}; development warning unassessable {un:.3f}")
        for c, (mech, vec) in enumerate(CORNERS):
            k = si * NC + c
            eub, clb, pmin, plb, rub, und = checks(k, *m)
            ok = eub <= 0.05 and clb >= 0.95 and plb >= 0.60 and rub <= 0.05
            u15 = np.mean([res[fi, POW15]["unres"][k] for fi in range(nfr)], 0)
            fm = sum(res[fi, ci]["fire"][si, c] for fi in range(nfr) for ci in range(len(CONDS))) / (n * nfr * len(CONDS))
            fm15 = sum(res[fi, POW15]["fire"][si, c] for fi in range(nfr)) / (n * nfr)
            dv = sum(res[fi, 0]["dev"]["fire"][si, c] for fi in range(nfr)) / (N_DEV * nfr)
            lines.append(f"  {mech} {vec if vec else ''}: error {eub:.4f}; coverage {clb:.4f}; reading {rub:.4f}; +0.15 power {pmin:.3f}/{plb:.3f}{'' if ok else ' FAIL'}; undefined {und:.4f}; "
                         f"unresolved at +0.15 (A1, A2, H) {u15[0]:.3f}/{u15[1]:.3f}/{u15[2]:.3f}; warning main {fm:.3f} (+0.15 {fm15:.3f}), development {dv:.3f}")
            rows.append(["corner", k_pos, mode, mech, vec, f"{eub:.4f}", f"{clb:.4f}", f"{rub:.4f}", f"{pmin:.4f}", f"{plb:.4f}", f"{und:.5f}", int(ok)])
    lines.append(f"\nFull grids for the binding scenario (positive bundle {SCEN[BIND][0]}, time {SCEN[BIND][1]}); Bonferroni per mechanism")
    base = NS * NC
    for mi, (mech, vecs) in enumerate(v42.MECHS):
        nv = len(vecs)
        mm = (3 * nv * nfr, len(CONDS) * nv * nfr * 2, nv * nfr * 2, len(READERR) * nv * nfr)
        passv, worst = {}, []
        for vi, vec in enumerate(vecs):
            k = base + int(v42.OFF[mi]) + vi
            eub, clb, pmin, plb, rub, und = checks(k, *mm)
            passv[vec] = eub <= 0.05 and clb >= 0.95 and plb >= 0.60 and rub <= 0.05
            worst.append((eub, clb, rub, und))
            rows.append(["full", SCEN[BIND][0], SCEN[BIND][1], mech, vec, f"{eub:.4f}", f"{clb:.4f}", f"{rub:.4f}", f"{pmin:.4f}", f"{plb:.4f}", f"{und:.5f}", int(passv[vec])])
        dc, maxi = region(passv, vecs)
        lines.append(f"  {mech}: worst error {max(w[0] for w in worst):.4f}; worst coverage {min(w[1] for w in worst):.4f}; worst reading {max(w[2] for w in worst):.4f}; worst undefined {max(w[3] for w in worst):.4f}; "
                     f"passing {sum(passv.values())} of {nv}; maximal: " + "; ".join(map(str, maxi)))
    lines.append("done")
    open("power_results_v44.txt", "w").write("\n".join(lines) + "\n")
    with open("power_results_v44_vectors.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["part", "positive_bundle", "time_mode", "mechanism", "vector", "error_upper_bound", "coverage_lower_bound", "reading_error_upper_bound", "lowest_power_015", "power_lower_bound_015", "worst_undefined_share", "passes"])
        wr.writerows(rows)
    print("\n".join(lines))
