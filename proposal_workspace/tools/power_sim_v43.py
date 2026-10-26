"""Version 43: the fixed-reserve stopping rule of proposal_v27 section 5.7 and its observable package warning (round-26
simulation request S1).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v43.py
Base: power_sim_v42.py (frames of 230 protocols less three development protocols, three frame groups, frozen estimator
with the empty-stratum rule and rates bounded by 0 and 1, Holm 0.03, multiplier 1.175). Added:
- Candidate bundles. An implementation with a detected flaw (a positive) registers k_pos candidates (1 or 3); the
  confirming candidate is at a uniform position among them. An implementation without a detected flaw registers
  Binomial(3, p) rejected candidates, with p set in each sample so that the expected candidates per implementation equal
  the target rate R (8/64 or 3/13, the pilot rates). If positives alone exceed R, p = 0 and the sample is counted as
  infeasible for that R (positives are never removed).
- Confirmation reserve. Main study 770 x 3/13 x 1.0 = 177.7 hours; development 105 x 3/13 x 1.0 = 24.2 hours. Bundles are
  processed in a random order. Before a bundle starts, the reserve must hold its full cap (k x 1.0 hours); otherwise
  processing stops and every later bundle is unfinished. Actual time used: cost mode "0.5" (every candidate 0.5 h), "1.0"
  (every candidate 1.0 h) or "adverse" (the confirming candidate 1.0 h, rejected ones 0.5 h). A positive bundle stops at its
  confirming candidate. Unused reserved time returns to the reserve.
- Review reserve. Main study 178 packages, development 25. Each processed positive gives one package; packages are reviewed
  in a random order; packages beyond the reserve are unfinished.
- Outcomes. An unfinished bundle or an unreviewed package makes that implementation's security outcome unresolved (its
  working status stays known). This is combined (logical or) with each V42 mechanism at its region corners: independent,
  task, protocol and difficulty at (0.0075, 0.0075, 0.0075) and (0.013, 0.013, 0.005); package at (0.05, 0.05, 0.2); and no
  added mechanism (exhaustion alone).
- Observable package warning. Per author, n = registered candidate records (within the three-candidate limit), x = records
  left unfinished (records of unfinished bundles, unreviewed packages, and records of implementations unresolved by the
  added mechanism). Fires when the one-sided 95% Clopper-Pearson lower limit for x of n exceeds 0.05 for a configuration or
  0.2 for historical code; an author with no record is unassessable.
Scenarios: k_pos in {1, 3} x R in {8/64, 3/13} x cost mode in {0.5, 1.0, adverse}: 12. Conditions: exact null, both partial
nulls (0, +0.10) and (+0.10, 0), exact +0.15. 4,000 studies per frame and condition (seed 4301); 4,000 development samples
of three protocols per frame at the exact null. Bonferroni per scenario over that scenario's checks.
Outputs: power_results_v43.txt and power_results_v43_scenarios.csv.
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
SCEN = list(itertools.product((1, 3), (8 / 64, 3 / 13), ("0.5", "1.0", "adverse")))
COMBOS = [("none", None)] + [(m, v) for m in ("independent", "task", "protocol", "difficulty") for v in ((0.0075, 0.0075, 0.0075), (0.013, 0.013, 0.005))] + [("package", (0.05, 0.05, 0.2))]
NS, NC = len(SCEN), len(COMBOS)
CONDS = [("exact null", (0.0, 0.0)), ("partial null (0, +0.10)", (0.0, 0.10)), ("partial null (+0.10, 0)", (0.10, 0.0)), ("exact +0.15", (0.15, 0.15))]
RES_MAIN, RES_DEV = (177.7, 178), (24.2, 25)
N_STUDIES, N_DEV = 4000, 4000
LIMITS = np.array([0.05, 0.05, 0.2])
_CACHE = {}
v42.masks = lambda cat, bmap: _CACHE["m"]                      # v42.evaluate reads the combined masks prepared here
v42.pkg_counts = lambda cat, hu, au: (None, None)


def init():
    v42.init(dict(sizes=(230,), zero_share=True, n_studies=N_STUDIES, rd_levels=[0.01], vacuous=True, groups=None, n_dev=N_DEV))


def mech_masks(cat, bmap):
    """Masks for the 10 combinations: hu (NC, nf), au (NC, 2, K, nf)."""
    nf = cat["hy"].size
    hs, as_ = [], []
    for mech, vec in COMBOS:
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
            bH = bmap[uH]; bA = np.array([bmap[x] for x in vec[:2]])[:, None, None]
            with np.errstate(over="ignore"):
                h = cat["Uh"] < v42.expit(bH + cat["score"]); a = cat["Ua"] < v42.expit(bA + cat["score"][None, None])
        else:
            h, a = cat["hy"] & (cat["Uh"] < uH), cat["ay"] & (cat["Ua"] < uA)
        hs.append(h); as_.append(np.asarray(a))
    return np.array(hs), np.array(as_)


def exhaust(rng, pos, reserve, k_pos, R, mode):
    """pos: (M,) positives over all implementations. Returns k, unfinished-bundle mask, unreviewed-package mask, flags."""
    M = pos.size
    npos = pos.sum(); nneg = M - npos
    p = (R * M - k_pos * npos) / (3 * nneg) if nneg else 0.0
    infeasible = p < 0
    p = min(max(p, 0.0), 1.0)
    k = np.where(pos, k_pos, rng.binomial(3, p, M))
    jpos = rng.integers(1, k_pos + 1, M)                                   # position of the confirming candidate
    c_rej, c_conf = {"0.5": (0.5, 0.5), "1.0": (1.0, 1.0), "adverse": (0.5, 1.0)}[mode]
    cost = np.where(pos, (jpos - 1) * c_rej + c_conf, k * c_rej)
    idx = np.flatnonzero(k > 0)
    order = idx[rng.permutation(idx.size)]
    before = np.concatenate([[0.0], np.cumsum(cost[order])[:-1]])
    stop = reserve[0] - before < k[order] * 1.0
    first = np.argmax(stop) if stop.any() else order.size
    unfinished = np.zeros(M, bool); unfinished[order[first:]] = True
    pk = order[:first][pos[order[:first]]]                                  # processed positives give packages
    pk = pk[rng.permutation(pk.size)]
    unrev = np.zeros(M, bool); unrev[pk[int(reserve[1]):]] = True
    return k, unfinished, unrev, bool(infeasible), bool(stop.any()), pk.size > reserve[1]


def scenario_masks(rng, cat, bmap, reserve):
    """Combined masks for every scenario and combination, observable warning counts, and flags."""
    hy, ay = cat["hy"], cat["ay"]
    nf = hy.size
    pos = np.concatenate([hy, ay.ravel()])                                  # order: historical, then config, attempt, function
    author = np.concatenate([np.full(nf, 2), np.repeat([0, 1], K * nf)])
    mh, ma = mech_masks(cat, bmap)
    mflat = np.concatenate([mh, ma.reshape(NC, -1)], 1)                     # (NC, M)
    HU, AU, X, N, FL = [], [], [], [], []
    for k_pos, R, mode in SCEN:
        k, unf, unrev, inf, st_c, st_r = exhaust(rng, pos, reserve, k_pos, R, mode)
        ex = unf | unrev
        comb = mflat | ex[None]
        HU.append(comb[:, :nf]); AU.append(comb[:, nf:].reshape(NC, 2, K, nf))
        rec_unf = np.where(unf, k, 0) + (unrev & ~unf) + np.where(~ex & mflat & (k > 0), np.where(pos, 1, k), 0)   # (NC, M)
        X.append(np.stack([(rec_unf * (author == a)).sum(1) for a in (0, 1, 2)], 1))
        N.append(np.array([k[author == a].sum() for a in (0, 1, 2)]))
        FL.append((inf, st_c, st_r))
    return np.concatenate(HU), np.concatenate(AU), np.array(X), np.array(N), np.array(FL)


def warn(X, N):
    """X: (S, NS, NC, 3); N: (S, NS, 3). Returns fire counts (NS, NC) and unassessable counts (NS,)."""
    Nb = np.broadcast_to(N[:, :, None, :], X.shape)
    with np.errstate(invalid="ignore", divide="ignore"):
        lo = np.where(X > 0, stats.beta.ppf(0.05, np.maximum(X, 1), np.maximum(Nb - X + 1, 1)), 0.0)
    fire = ((lo > LIMITS) & (Nb > 0)).any(-1)
    return fire.sum(0), (N == 0).any(-1).sum(0)


def job(args):
    fi, ci = args
    size, group, name, rc, spec = v42.FRAMES[fi]
    fr = v42.Frame(*spec)
    tr = fr.set_target(rc, np.array(CONDS[ci][1], float))
    rng = np.random.default_rng([4301, fi, ci])
    outs, Xs, Ns, FLs, unres = [], [], [], [], []
    for _ in range(N_STUDIES):
        cat = v42.draw(rng, fr, rc)
        hu, au, X, N, FL = scenario_masks(rng, cat, fr.bmap, RES_MAIN)
        _CACHE["m"] = (hu, au)
        o = v42.evaluate(cat, fr.bmap)
        outs.append(o[:7]); Xs.append(X.reshape(NS, NC, 3)); Ns.append(N); FLs.append(FL)
        unres.append(np.stack([au[:, 0].mean((-1, -2)), au[:, 1].mean((-1, -2)), hu.mean(-1)], 1))
    L, sL, U, sU, zL, zU = (np.array([o[i] for o in outs]) for i in range(6))
    df = np.array([o[6] for o in outs]) - 1.0
    dfb = df[:, None, None]
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
    fire, unass = warn(np.array(Xs), np.array(Ns))
    FLa = np.array(FLs)                                                     # (S, NS, 3)
    r = dict(err=err, pw=pw, cov=hit.sum(0), undef=undef, fire=fire, unass=unass, flags=FLa.sum(0), unres=np.mean(unres, 0))
    if ci == 0:                                                              # development samples
        dX, dN = [], []
        for _ in range(N_DEV):
            cat = v42.draw(rng, fr, rc, 3, fr.pi3)
            if cat is None:
                continue
            _, _, X, N, _ = scenario_masks(rng, cat, fr.bmap, RES_DEV)
            dX.append(X.reshape(NS, NC, 3)); dN.append(N)
        dfire, dun = warn(np.array(dX), np.array(dN))
        r["dev"] = dict(fire=dfire, unass=dun, n=len(dN))
    return fi, ci, r


if __name__ == "__main__":
    init()
    nfr = len(v42.FRAMES)
    res = {}
    with mp.Pool(8, initializer=init) as pool:
        for fi, ci, r in pool.imap_unordered(job, [(fi, ci) for fi in range(nfr) for ci in range(len(CONDS))], chunksize=1):
            res[fi, ci] = r
    import pickle
    pickle.dump(res, open(os.path.join(os.environ.get("CLAUDE_JOB_DIR", "."), "tmp", "power_results_v43_raw.pkl") if os.environ.get("CLAUDE_JOB_DIR") else "power_results_v43_raw.pkl", "wb"))
    n = N_STUDIES
    m_err, m_cov, m_pw = 3 * NC * nfr, len(CONDS) * NC * nfr * 2, NC * nfr * 2
    lines = [f"V43: fixed-reserve stopping rule; frames of 230 (all {nfr} frames of V42); frozen estimator; {n} studies per frame and condition; main reserves {RES_MAIN}, development {RES_DEV}; "
             f"Bonferroni per scenario over {m_err} error, {m_cov} coverage and {m_pw} power checks"]
    rows = []
    for si, (k_pos, R, mode) in enumerate(SCEN):
        tag = f"positive bundle {k_pos}, candidate rate {R:.3f}, cost {mode}"
        fl0 = sum(res[fi, 0]["flags"][si] for fi in range(nfr)) / (n * nfr)
        fl15 = sum(res[fi, 3]["flags"][si] for fi in range(nfr)) / (n * nfr)
        lines.append(f"\n{tag}: infeasible share {fl0[0]:.3f} (null) / {fl15[0]:.3f} (+0.15); confirmation reserve ran out in {fl0[1]:.3f} / {fl15[1]:.3f}; review reserve ran out in {fl0[2]:.3f} / {fl15[2]:.3f}")
        for c, (mech, vec) in enumerate(COMBOS):
            k = si * NC + c
            eub = max(v30.ucb(int(res[fi, ci]["err"][k]), n, m_err) for fi in range(nfr) for ci in (0, 1, 2))
            clb = min(v30.lcb(int(x), n, m_cov) for fi in range(nfr) for ci in range(len(CONDS)) for x in res[fi, ci]["cov"][k])
            plb = min(v30.lcb(int(x), n, m_pw) for fi in range(nfr) for x in res[fi, 3]["pw"][k])
            pmin = min(x / n for fi in range(nfr) for x in res[fi, 3]["pw"][k])
            und = max(res[fi, ci]["undef"][k] for fi in range(nfr) for ci in range(len(CONDS))) / n
            u0 = np.mean([res[fi, 0]["unres"][k] for fi in range(nfr)], 0); u15 = np.mean([res[fi, 3]["unres"][k] for fi in range(nfr)], 0)
            fm = sum(res[fi, ci]["fire"][si, c] for fi in range(nfr) for ci in range(len(CONDS))) / (n * nfr * len(CONDS))
            fm15 = sum(res[fi, 3]["fire"][si, c] for fi in range(nfr)) / (n * nfr)
            dv = sum(res[fi, 0]["dev"]["fire"][si, c] for fi in range(nfr)) / sum(res[fi, 0]["dev"]["n"] for fi in range(nfr))
            ok = eub <= 0.05 and clb >= 0.95 and plb >= 0.60
            lines.append(f"  {mech} {vec if vec else ''}: error {eub:.4f}; coverage {clb:.4f}; +0.15 power {pmin:.3f}/{plb:.3f}{'' if ok else ' FAIL'}; undefined {und:.4f}; "
                         f"unresolved share (A1, A2, H) null {u0[0]:.3f}/{u0[1]:.3f}/{u0[2]:.3f}, +0.15 {u15[0]:.3f}/{u15[1]:.3f}/{u15[2]:.3f}; warning main {fm:.3f} (at +0.15 {fm15:.3f}), development {dv:.3f}")
            rows.append([k_pos, f"{R:.4f}", mode, mech, vec, f"{eub:.4f}", f"{clb:.4f}", f"{pmin:.4f}", f"{plb:.4f}", f"{und:.5f}", f"{fm:.4f}", f"{fm15:.4f}", f"{dv:.4f}", int(ok)])
        un_m = sum(res[fi, ci]["unass"][si] for fi in range(nfr) for ci in range(len(CONDS))) / (n * nfr * len(CONDS))
        un_d = sum(res[fi, 0]["dev"]["unass"][si] for fi in range(nfr)) / sum(res[fi, 0]["dev"]["n"] for fi in range(nfr))
        lines.append(f"  warning unassessable share: main {un_m:.3f}, development {un_d:.3f}")
    lines.append("done")
    open("power_results_v43.txt", "w").write("\n".join(lines) + "\n")
    with open("power_results_v43_scenarios.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["positive_bundle", "candidate_rate", "cost_mode", "mechanism", "vector", "error_upper_bound", "coverage_lower_bound", "lowest_power_015", "power_lower_bound_015", "worst_undefined_share", "warning_main", "warning_main_015", "warning_development", "passes"])
        wr.writerows(rows)
    print("\n".join(lines))
