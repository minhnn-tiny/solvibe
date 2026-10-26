"""Version 42: one frozen final estimator across every frame group and five unresolved-outcome mechanisms (round-25
points R25.3 to R25.6; copied from power_sim_v39.py and changed as listed).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v42.py
Changes from power_sim_v39.py run as power_sim_v41.py:
- Estimator fixed: empty-stratum rule and rates bounded by 0 and 1 (ZERO_SHARE and VACUOUS True), jackknife over every
  sampled protocol, frozen Holm 0.03 and multiplier 1.175. Frames of 230 protocols less three development protocols; all
  three frame groups (base, linked working, low V yield); 4,000 fresh studies per frame and condition (seed 4201).
- Five mechanisms: independent, task (one draw per function shared by every author), protocol, difficulty (threshold
  expit(b + s), b set per frame so that the mean over built functions equals the author rate) on the 76 ordered vectors,
  and package (only implementations with a detected flaw can be unresolved) on the 64 per-package vectors.
- The reading of the upper limit (Holm 0.01, margin +0.05) is checked at every condition in which a configuration is at or
  above the margin: (0, +0.10), (+0.10, 0), (+0.05, +0.05), (+0.05, 0), (0, +0.05), +0.10 and +0.15.
- Package diagnostic (R25.4). For each author, n = implementations with a package (a detected flaw) in the sample and x =
  those whose package is unresolved; limit = one-sided 95% Clopper-Pearson lower limit for x of n. It fires when a
  configuration's limit exceeds 0.05 or the historical limit exceeds 0.2 (the per-package region). An author with no
  package gives no evidence and does not fire; such samples are counted as unassessable. Reported for the 22-protocol main
  samples (all conditions pooled) and for 4,000 development samples of three protocols per frame (exact null).
Outputs: power_results_v42.txt and power_results_v42_vectors.csv.

History of the copied code (power_sim_v39.py):
Version 39: the checks the iteration-4 meta-review asks for (items 3, 4, 6, 7 and 9), in one rerun.

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v39.py
Design and frozen procedure: 22 protocols, up to one V and six N functions, two attempts per configuration; Holm level 0.03,
interval multiplier 1.175, the widening terms of power_sim_v32.py. No recalibration.
What is new:
- Frame size (item 7). Frames of 50 and 70 protocols, resampled from the 25 strict (V, N) pairs. Three development
  protocols are drawn first (randomized systematic sampling, probabilities proportional to N, sample size 3) and removed;
  the domain and the main inclusion probabilities are defined on the remaining 47 or 67 protocols.
- Certainty protocols (item 7). Option JK = "noncert" treats a protocol with inclusion probability 1 as its own stratum:
  never deleted in the jackknife, factor (n - 1) / n with n the non-certain sampled protocols, t with n - 1 degrees of
  freedom. Option JK = "all" (used; see the jackknife note below) deletes every sampled protocol, as in V33.
- Working status (item 4). Setting "linked": each function has a score s = 0.6 x (shared vulnerability effect) / 1.5 +
  0.8 x N(0, 1). Each agent attempt works with probability expit(a - s), a set so that the mean over built functions is
  0.72 (the 0.9 x 0.8 of earlier versions). The historical body works with probability expit(h - s), h set to a mean of
  0.95, drawn once per function and fixed. Exact targets are conditional rates among working implementations. Setting
  "independent" is the earlier model (agents 0.72 regardless of the function; historical always works).
- Low V yield (item 9). V functions are built with mean probability 0.3 (same difficulty link), N functions as before.
- Package-linked unresolved outcomes (item 6). Only an implementation with a detected flaw (a package) can be unresolved,
  at a rate per package for each author: (r_A1, r_A2, r_H) on {0, 0.05, 0.1, 0.2}^3, ordered (64 vectors). The earlier
  independent and protocol mechanisms (rates per implementation, 76 ordered vectors as in V37) are kept.
- Reading of the upper limit (item 3). Margin m = +0.05. For each configuration, p = t-cdf((U + zU - m) / se(U)); Holm
  across the two configurations at each level in RD_LEVELS; a claim states that the configuration's difference is below
  m. Its error is a claim made when the true difference is at least m; it is checked at exact (m, m) and (m, 0). This run
  only calibrates the level (the error bounds are computed on the same draws); fresh validation is a separate run.
- Jackknife (item 7). JK = "all" keeps the V33 delete-one-protocol jackknife over every sampled protocol, including those
  selected with certainty. A small test with JK = "noncert" (certainty protocols never deleted, as the meta-review
  suggested) gave family-wise error 0.25 to 0.28 at the exact null in two of three 50-protocol frames: it ignores the
  variance from sampling functions inside certainty protocols. JK = "all" is therefore used.
Frames: for each size, 24 base frames (two strict count lists, three recall patterns, historical N rate 0.05 or 0.10,
construction (link 0, yield 0.9) or (link 0.6, yield 0.7)) with independent working; the same 24 with linked working; and
12 low-V frames (both count lists, three recall patterns, both historical N rates, link 0.6, N yield 0.7, V yield 0.3).
Conditions: exact (0, 0), (0, +0.10), (+0.10, 0), (+0.025, +0.025), (+0.05, +0.05), (+0.05, 0), (+0.10, +0.10),
(+0.15, +0.15), and the negative target max(-0.05, half the lowest attainable contrast). 2,000 studies per frame and condition
(seed 3901 + size); common random numbers across mechanisms and vectors.
Checks per frame size, frame group and mechanism, with one-sided Clopper-Pearson bounds and Bonferroni over that family:
family-wise error at (0, 0), (0, +0.10) and (+0.10, 0) for every vector; marginal coverage in every condition and vector;
+0.15 power at every vector; error of the reading at (+0.05, +0.05) and (+0.05, 0).
Outputs: power_results_v39.txt, power_results_v39_vectors.csv, power_results_v39_frames.csv.
"""
import csv
import itertools
import multiprocessing as mp
import numpy as np
from scipy import stats
import power_sim_v29 as v29
import power_sim_v30 as v30

expit = v29.expit
P, VCAP, NPER, K = 22, 1, 6, 2
A_STAR, C_STAR, MARGIN, N_STUDIES = 0.03, 1.175, 0.05, 4000
JK = "all"          # "all": delete each sampled protocol (V33 procedure); "noncert": certainty protocols never deleted
RD_LEVELS = [0.01]   # Holm level of the reading of the upper limit (chosen in V39)
ZERO_SHARE = True    # True (power_sim_v40.py): a stratum with no built function in the sample or replicate contributes 0
VACUOUS = True       # True (power_sim_v41.py): an author-stratum rate with no working or unresolved implementation is bounded by 0 and 1
GROUPS = None        # restrict frame groups, for example ("low V yield",)
SIZES = (230,)
N_DEV = 4000
PKG_LIMITS = (0.05, 0.05, 0.2)   # per-package region: configuration 1, configuration 2, historical
BASE = [0.0, 0.005, 0.0075, 0.013]
V76 = list(itertools.product(BASE, BASE, BASE)) + [(a1, a2, h) for a1 in (0.0, 0.0075) for a2 in (0.0, 0.0075) for h in (0.02, 0.03, 0.065)]
VPK = list(itertools.product([0.0, 0.05, 0.1, 0.2], repeat=3))
MECHS = [("independent", V76), ("task", V76), ("protocol", V76), ("difficulty", V76), ("package", VPK)]
OFF = np.cumsum([0] + [len(v) for _, v in MECHS])
MV = int(OFF[-1])
CONDS = [("exact null", (0.0, 0.0)), ("partial null (0, +0.10)", (0.0, 0.10)), ("partial null (+0.10, 0)", (0.10, 0.0)),
         ("exact +0.025", (0.025, 0.025)), ("margin (+0.05, +0.05)", (0.05, 0.05)), ("margin (+0.05, 0)", (0.05, 0.0)), ("margin (0, +0.05)", (0.0, 0.05)),
         ("exact +0.10", (0.10, 0.10)), ("exact +0.15", (0.15, 0.15)), ("negative", "neg")]
NULLC, POW15, READERR = [0, 1, 2], 8, [1, 2, 4, 5, 6, 7, 8]
FRAMES = None


def calib_mean(score, target, sign=-1.0):
    lo, hi = -30.0, 30.0
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if expit(mid + sign * score).mean() < target else (lo, mid)
    return (lo + hi) / 2


class Frame(v29.Frame):
    def __init__(self, seed, size, vlist, hN, link, yld, working, vyield=None):
        v29.M, v29.P = size, P
        super().__init__(np.random.default_rng(seed), vlist, hN, link, yld)
        rng = np.random.default_rng([seed, 7])
        dev = set(v29.sys_pps(rng, v29.incl_probs(self.NN.astype(float), 3)).tolist())
        self.f = {k: d for k, d in self.f.items() if k[0] not in dev}
        keep = np.array([p not in dev for p in range(size)])
        self.pi = np.zeros(size); self.pi[keep] = v29.incl_probs(self.NN[keep].astype(float), P)
        self.working = working
        for key in sorted(self.f):
            d = self.f[key]
            d["score"] = 0.6 * d["sh"] / 1.5 + 0.8 * rng.normal(0, 1, d["sh"].size)
        if vyield is not None:                                       # low V yield: rebuild V construction only
            vd = np.concatenate([d["diff"] for k, d in sorted(self.f.items()) if k[1] == "V"])
            b = calib_mean(vd, vyield)
            for k in sorted(self.f):
                if k[1] == "V":
                    d = self.f[k]; d["built"] = rng.random(d["diff"].size) < expit(b - d["diff"])
        built = np.concatenate([d["score"][d["built"]] for d in self.f.values()])
        if working == "linked":
            a = calib_mean(built, 0.72); h = calib_mean(built, 0.95)
            for k in sorted(self.f):
                d = self.f[k]
                d["wa"] = expit(a - d["score"]); d["hw"] = rng.random(d["score"].size) < expit(h - d["score"])
        else:
            for d in self.f.values():
                d["wa"] = np.full(d["score"].size, 0.72); d["hw"] = np.ones(d["score"].size, bool)
        self.cert = self.pi >= 1 - 1e-12
        keep = self.pi > 0
        self.pi3 = np.zeros(size); self.pi3[keep] = v29.incl_probs(self.NN[keep].astype(float), 3)
        self.bmap = {u: (-np.inf if u == 0 else calib_mean(built, u, sign=1.0)) for u in sorted({x for v in V76 for x in v})}

    def rates(self, recall, shift=None):
        """Exact detected rates among working implementations, by stratum: agents (2,), historical, and built counts."""
        sAV, sAN, sHV, sHN = recall
        old = self.shift.copy()
        if shift is not None:
            self.shift = shift
        out = {}
        for s, sA, sH in (("V", sAV, sHV), ("N", sAN, sHN)):
            ds = [d for (p, ss), d in self.f.items() if ss == s]
            pa = np.concatenate([self.pa(s, d)[:, d["built"]] for d in ds], axis=1)
            wa = np.concatenate([d["wa"][d["built"]] for d in ds]); hw = np.concatenate([d["hw"][d["built"]] for d in ds])
            yh = np.concatenate([d["yh"][d["built"]] for d in ds])
            out[s] = ((pa * wa).sum(1) / wa.sum() * sA, (yh & hw).sum() / max(hw.sum(), 1) * sH, wa.size)
        self.shift = old
        return out

    def truth(self, recall, shift=None):
        r = self.rates(recall, shift)
        shr = r["V"][2] / (r["V"][2] + r["N"][2])
        return shr * (r["V"][0] - r["V"][1]) + (1 - shr) * (r["N"][0] - r["N"][1])


def build_frames():
    out = []
    for size in SIZES:
        i = 0
        for vname, vlist in (("upper", v29.V_REC), ("observed", v29.V_OBS)):
            for rname, rc in v29.RECALLS.items():
                for hN in (0.05, 0.10):
                    for link, yld in ((0.0, 0.9), (0.6, 0.7)):
                        for working in ("independent", "linked"):
                            out.append((size, "base" if working == "independent" else "linked working", f"{vname}, recall {rname}, hN {hN}, link {link}, yield {yld}", rc, (3900 + size * 100 + i, size, vlist, hN, link, yld, working)))
                        i += 1
                    out.append((size, "low V yield", f"{vname}, recall {rname}, hN {hN}, link 0.6, yield 0.7, V yield 0.3", rc, (3900 + size * 100 + 50 + i, size, vlist, hN, 0.6, 0.7, "independent", 0.3)))
    return out


def init(cfg=None):
    global FRAMES, SIZES, ZERO_SHARE, N_STUDIES, RD_LEVELS, VACUOUS, GROUPS
    if cfg:
        SIZES, ZERO_SHARE, N_STUDIES, RD_LEVELS = cfg["sizes"], cfg["zero_share"], cfg["n_studies"], cfg["rd_levels"]
        VACUOUS, GROUPS = cfg.get("vacuous", False), cfg.get("groups")
        globals()["N_DEV"] = cfg.get("n_dev", N_DEV)
    FRAMES = [f for f in build_frames() if GROUPS is None or f[1] in GROUPS]


def draw(rng, fr, recall, n_prot=None, pi=None):
    n_prot = P if n_prot is None else n_prot
    pi = fr.pi if pi is None else pi
    sAV, sAN, sHV, sHN = recall
    sel = v29.sys_pps(rng, pi)
    assert len(set(sel.tolist())) == n_prot
    rows = []
    for j, p in enumerate(sel):
        hh = 1.0 / pi[p]
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
            hw = d["hw"][idx]
            hy = d["yh"][idx] & hw & (rng.random(idx.size) < sH)
            pa = fr.pa(s, d)[:, idx]
            work = rng.random((2, K, idx.size)) < d["wa"][idx]
            ay = work & (rng.random((2, K, idx.size)) < pa[:, None, :]) & (rng.random((2, K, idx.size)) < sA)
            rows.append(dict(st=np.full(idx.size, st), j=np.full(idx.size, j), w=np.full(idx.size, w), hw=hw, hy=hy, aw=work, ay=ay, score=d["score"][idx]))
    if not rows:
        return None
    cat = {k: np.concatenate([r[k] for r in rows], axis=-1) for k in rows[0]}
    nf = cat["hy"].size
    cat["Uh"] = rng.random(nf); cat["Ua"] = rng.random((2, K, nf)); cat["Up"] = rng.random(n_prot)[cat["j"]]; cat["Ut"] = rng.random(nf)
    cat["cert"] = fr.cert[sel]
    return cat


def masks(cat, bmap):
    out_h, out_a = [], []
    shp = (None, 2) + cat["Ua"].shape[1:]
    for name, vecs in MECHS:
        u = np.array(vecs); tA, tH = u[:, :2, None, None], u[:, 2, None]
        if name == "independent":
            out_h.append(cat["Uh"][None] < tH); out_a.append(cat["Ua"][None] < tA)
        elif name == "task":
            out_h.append(cat["Ut"][None] < tH); out_a.append(np.broadcast_to(cat["Ut"] < tA, (len(vecs),) + shp[1:]))
        elif name == "difficulty":
            bH = np.array([bmap[x] for x in u[:, 2]]); bA = np.array([[bmap[x] for x in r] for r in u[:, :2]])
            with np.errstate(over="ignore"):
                pH = expit(bH[:, None] + cat["score"][None]); pA = expit(bA[:, :, None] + cat["score"][None, None])
            out_h.append(cat["Uh"][None] < pH); out_a.append(cat["Ua"][None] < pA[:, :, None, :])
        elif name == "protocol":
            out_h.append(cat["Up"][None] < tH); out_a.append(np.broadcast_to(cat["Up"] < tA, (len(vecs),) + shp[1:]))
        else:
            out_h.append(cat["hy"][None] & (cat["Uh"][None] < tH)); out_a.append(cat["ay"][None] & (cat["Ua"][None] < tA))
    return np.concatenate(out_h), np.concatenate(out_a)


def pkg_counts(cat, hu, au):
    """Packages (implementations with a detected flaw) and unresolved packages per author: arrays (MV, 3), order A1, A2, H."""
    hy, ay = cat["hy"], cat["ay"]
    n = np.array([ay[0].sum(), ay[1].sum(), hy.sum()], float)
    x = np.stack([(ay[0][None] & au[:, 0]).sum((-1, -2)), (ay[1][None] & au[:, 1]).sum((-1, -2)), (hy[None] & hu).sum(-1)], 1)
    return x, n


def evaluate(cat, bmap):
    G = np.zeros((cat["hy"].size, 2 * P)); G[np.arange(cat["hy"].size), cat["st"] * P + cat["j"]] = 1.0
    hu, au = masks(cat, bmap)
    px, pn = pkg_counts(cat, hu, au)
    w, hw, hy, aw, ay = cat["w"], cat["hw"], cat["hy"], cat["aw"], cat["ay"]
    S = lambda x: (x * w) @ G
    Hy, Hw, Hu = S(hy & ~hu), S(hw & ~hu), S(hu)
    Ay, Aw, Au = [S(x).sum(2) for x in (ay & ~au, aw & ~au, au)]
    B = w @ G
    rs = lambda x: x.reshape(x.shape[:-1] + (2, P))
    Hy, Hw, Hu, Ay, Aw, Au, B = map(rs, (Hy, Hw, Hu, Ay, Aw, Au, B))
    cnt = lambda x: (x.astype(float) @ G).reshape(x.shape[:-1] + (2, P)).sum(-1)
    he, hn = cnt(hy & ~hu), cnt(hw & ~hu)
    ae, an = cnt(ay & ~au).sum(2), cnt(aw & ~au).sum(2)
    nc = np.flatnonzero(~cat["cert"]) if JK == "noncert" else np.arange(P); n = nc.size

    def bounds(m):
        Bm = B @ m.T; shr = Bm[0] / (Bm[0] + Bm[1])
        h = [x @ m.T for x in (Hy, Hw, Hu)]
        a = [x @ m.T for x in (Ay, Aw, Au)]
        vlo = a[0] / (a[1] + a[2]); vhi = (a[0] + a[2]) / (a[1] + a[2])
        hlo = (h[0] / (h[1] + h[2]))[:, None]; hhi = ((h[0] + h[2]) / (h[1] + h[2]))[:, None]
        if VACUOUS:
            vlo, vhi = np.nan_to_num(vlo, nan=0.0), np.nan_to_num(vhi, nan=1.0)
            hlo, hhi = np.nan_to_num(hlo, nan=0.0), np.nan_to_num(hhi, nan=1.0)
        dlo, dhi = vlo - hhi, vhi - hlo
        if ZERO_SHARE:
            part = lambda sh, x: np.where(sh > 0, sh * x, 0.0)
            return part(shr, dlo[:, :, 0]) + part(1 - shr, dlo[:, :, 1]), part(shr, dhi[:, :, 0]) + part(1 - shr, dhi[:, :, 1]), shr
        return shr * dlo[:, :, 0] + (1 - shr) * dlo[:, :, 1], shr * dhi[:, :, 0] + (1 - shr) * dhi[:, :, 1], shr
    with np.errstate(invalid="ignore", divide="ignore"):
        L0, U0, shr0 = bounds(np.ones((1, P)))
        jm = np.ones((n, P)); jm[np.arange(n), nc] = 0.0              # delete one non-certain protocol at a time
        Lj, Uj, _ = bounds(jm)
        se = lambda x: np.sqrt((n - 1) / n * ((x - np.nanmean(x, -1, keepdims=True)) ** 2).sum(-1))
        share = np.array([shr0[0], 1 - shr0[0]])
        ucl = np.where(hn > 0, 1 - 0.025 ** (1 / np.maximum(hn, 1)), np.nan)
        ucla = np.where(an > 0, 1 - 0.025 ** (1 / np.maximum(an, 1)), np.nan)
        live = share > 0 if ZERO_SHARE else True                      # with ZERO_SHARE, an empty stratum adds no widening
        if VACUOUS:                                                   # a rate already bounded by 0 and 1 needs no widening
            ucl, ucla = np.nan_to_num(ucl, nan=0.0), np.nan_to_num(ucla, nan=0.0)
        zL = np.where((he == 0) & live, share * ucl, 0.0).sum(-1)
        zU = np.where((ae == 0) & live, share * ucla, 0.0).sum(-1)
    return L0[..., 0], se(Lj), U0[..., 0], se(Uj), np.broadcast_to(zL[:, None], (len(zL), 2)), zU, n, int(cat["cert"].sum()), px, pn


def holm2(p, a):
    o = np.argsort(p, -1, kind="stable"); ps = np.take_along_axis(p, o, -1)
    r1 = ps[..., 0] <= a / 2; r2 = r1 & (ps[..., 1] <= a)
    rej = np.zeros_like(p, bool); np.put_along_axis(rej, o, np.stack([r1, r2], -1), -1)
    return rej


def pkg_diag(x, n):
    """x: (S, MV, 3) unresolved packages; n: (S, 3) packages. Returns fire counts (MV,) and the number of unassessable samples."""
    nb = np.broadcast_to(n[:, None, :], x.shape)
    with np.errstate(invalid="ignore", divide="ignore"):
        lo = np.where(x > 0, stats.beta.ppf(0.05, np.maximum(x, 1), np.maximum(nb - x + 1, 1)), 0.0)
    fire = ((lo > np.array(PKG_LIMITS)) & (nb > 0)).any(-1)
    return fire.sum(0), int((n == 0).any(-1).sum())


def dev_diag(rng, fr, rc):
    xs, ns, empty = [], [], 0
    for _ in range(N_DEV):
        cat = draw(rng, fr, rc, 3, fr.pi3)
        if cat is None:
            empty += 1; continue
        hu, au = masks(cat, fr.bmap)
        x, n = pkg_counts(cat, hu, au); xs.append(x); ns.append(n)
    fire, unass = pkg_diag(np.array(xs), np.array(ns))
    return dict(fire=fire, unass=unass + empty, n=N_DEV)


def job(args):
    fi, ci = args
    size, group, name, rc, spec = FRAMES[fi]
    fr = Frame(*spec)
    cond, target = CONDS[ci]
    if target == "neg":
        target = np.maximum(-0.05, 0.5 * fr.truth(rc, np.full(2, -15.0)))
    tr = fr.set_target(rc, np.array(target, float))
    rN = fr.rates(rc)["N"]
    rng = np.random.default_rng([4201, fi, ci])
    out = [evaluate(draw(rng, fr, rc), fr.bmap) for _ in range(N_STUDIES)]
    L, sL, U, sU, zL, zU = (np.array([o[i] for o in out]) for i in range(6))
    df = np.array([o[6] for o in out]) - 1.0                                   # (n,)
    ncert = np.array([o[7] for o in out])
    pkg_fire, pkg_unass = pkg_diag(np.array([o[8] for o in out]), np.array([o[9] for o in out]))
    dfb = df[:, None, None]
    with np.errstate(invalid="ignore", divide="ignore"):
        q = stats.t.ppf(0.975, dfb)
        pl, pu = 2 * stats.t.sf(np.abs(L) / sL, dfb), 2 * stats.t.sf(np.abs(U) / sU, dfb)
        sign = np.where(L > 0, 1, np.where(U < 0, -1, 0))
        p = np.nan_to_num(np.where(L > 0, pl, np.where(U < 0, pu, 1.0)), nan=1.0)
        rej = holm2(p, A_STAR)
        null = np.abs(tr) < 1e-9
        err = (rej & (null | (np.sign(tr) != sign))).any(-1).sum(0)
        pw = (rej & (sign == np.sign(tr)) & ~null).sum(0)
        lo, hi = L - C_STAR * q * sL - zL, U + C_STAR * q * sU + zU
        hit = (lo <= tr) & (tr <= hi)
        undef = (~(np.isfinite(L) & np.isfinite(sL) & np.isfinite(U) & np.isfinite(sU) & np.isfinite(zL) & np.isfinite(zU))).any(-1).sum(0)
        pr = np.nan_to_num(stats.t.cdf((U + zU - MARGIN) / sU, dfb), nan=1.0)   # reading: difference below the margin
        rd = [holm2(pr, a) for a in RD_LEVELS]
        rd_err = np.array([(x & (tr >= MARGIN - 1e-9)).any(-1).sum(0) for x in rd])       # (levels, MV)
        rd_claim = np.array([x.sum(0) for x in rd])                                     # (levels, MV, 2)
        hw = np.nanmean(np.where(np.isfinite(hi - lo), (hi - lo) / 2, np.nan), 0)
    return fi, ci, tr, rN, dict(err=err, pw=pw, cov=hit.sum(0), undef=undef, rd_err=rd_err, rd_claim=rd_claim, hw=hw, cert=float(np.mean(ncert > 0)), ncert=float(np.mean(ncert)), pkg_fire=pkg_fire, pkg_unass=pkg_unass, dev=dev_diag(rng, fr, rc) if ci == 0 else None)


def main(cfg=None, out="power_results_v42", seed_note=""):
    init(cfg)
    jobs = [(fi, ci) for fi in range(len(FRAMES)) for ci in range(len(CONDS))]
    res = {}
    with mp.Pool(8, initializer=init, initargs=(cfg,)) as pool:
        for fi, ci, tr, rN, r in pool.imap_unordered(job, jobs, chunksize=1):
            res[fi, ci] = (tr, rN, r)
    import os, pickle
    pickle.dump(res, open(os.path.join(os.environ.get("CLAUDE_JOB_DIR", "."), "tmp", f"{out}_raw.pkl") if os.environ.get("CLAUDE_JOB_DIR") else f"{out}_raw.pkl", "wb"))
    n = N_STUDIES
    lf = 0.015 if 0.015 in RD_LEVELS else RD_LEVELS[0]                 # reading level shown in the per-frame table
    li_f = RD_LEVELS.index(lf)
    lines = [f"{out}: frozen procedure (Holm {A_STAR}, multiplier {C_STAR}), 22 x (1, 6), two attempts; frames of {', '.join(map(str, SIZES))} protocols less three development protocols; jackknife {JK}; empty-stratum rule {ZERO_SHARE}; {n} studies per frame and condition; margin {MARGIN}{seed_note}"]
    vrows, frows = [], []
    for size in SIZES:
        for group in ("base", "linked working", "low V yield"):
            fis = [fi for fi, f in enumerate(FRAMES) if f[0] == size and f[1] == group]
            if not fis:
                continue
            nf = len(fis)
            cert = np.mean([res[fi, 0][2]["cert"] for fi in fis]); ncert = [res[fi, 0][2].get("ncert", float("nan")) for fi in fis]
            lines.append(f"\nFrames of {size} protocols, {group} ({nf} frames); share of studies with at least one certainty protocol {cert:.3f}; mean certainty protocols per study {np.min(ncert):.1f} to {np.max(ncert):.1f}")
            for mi, (mech, vecs) in enumerate(MECHS):
                nvec = len(vecs)
                m_err, m_cov, m_pw, m_rd = 3 * nvec * nf, len(CONDS) * nvec * nf * 2, nvec * nf * 2, len(READERR) * nvec * nf
                passv, worst = {}, {}
                for vi, vec in enumerate(vecs):
                    k = OFF[mi] + vi
                    eub = max(v30.ucb(int(res[fi, ci][2]["err"][k]), n, m_err) for fi in fis for ci in NULLC)
                    clb = min(v30.lcb(int(x), n, m_cov) for fi in fis for ci in range(len(CONDS)) for x in res[fi, ci][2]["cov"][k])
                    plb = min(v30.lcb(int(x), n, m_pw) for fi in fis for x in res[fi, POW15][2]["pw"][k])
                    pmin = min(x / n for fi in fis for x in res[fi, POW15][2]["pw"][k])
                    rub = [max(v30.ucb(int(res[fi, ci][2]["rd_err"][li][k]), n, m_rd) for fi in fis for ci in READERR) for li in range(len(RD_LEVELS))]
                    und = max(res[fi, ci][2]["undef"][k] for fi in fis for ci in range(len(CONDS))) / n
                    passv[vec] = eub <= 0.05 and clb >= 0.95 and plb >= 0.60
                    worst[vec] = (eub, clb, pmin, plb, rub, und)
                    vrows.append([size, group, mech, *vec, f"{eub:.4f}", f"{clb:.4f}", f"{pmin:.4f}", f"{plb:.4f}", *[f"{x:.4f}" for x in rub], f"{und:.5f}", int(passv[vec])])
                ok = {v: all(passv[w] for w in vecs if all(a <= b + 1e-12 for a, b in zip(w, v))) for v in vecs}
                dc = [v for v in vecs if ok[v]]
                maxi = [v for v in dc if not any(w != v and all(a >= b - 1e-12 for a, b in zip(w, v)) for w in dc)]
                lines.append(f"  {mech}: worst error upper bound {max(x[0] for x in worst.values()):.4f}; worst coverage lower bound {min(x[1] for x in worst.values()):.4f}; "
                             "worst reading-error upper bound by Holm level " + ", ".join(f"{a}: {max(x[4][li] for x in worst.values()):.4f}" for li, a in enumerate(RD_LEVELS)) + f"; worst undefined share {max(x[5] for x in worst.values()):.5f}")
                lines.append(f"    +0.15 power: passing vectors {sum(passv.values())} of {nvec}; downward-closed set {len(dc)}; maximal: " + "; ".join(map(str, maxi)))
                sel = [(0.0, 0.0, 0.0), (0.0075, 0.013, 0.0075), (0.013, 0.0075, 0.0075), (0.013, 0.013, 0.005)] if mech != "package" else [(0.0, 0.0, 0.0), (0.05, 0.05, 0.05), (0.1, 0.1, 0.1), (0.2, 0.2, 0.2), (0.0, 0.0, 0.2), (0.2, 0.2, 0.0)]
                lines.append("    lowest +0.15 power / lower bound at " + "; ".join(f"{v}: {worst[v][2]:.3f}/{worst[v][3]:.3f}" for v in sel))
            k0 = 0                                                     # independent mechanism, no unresolved outcome
            for ci, (cond, _) in enumerate(CONDS):
                pw = np.array([res[fi, ci][2]["pw"][k0].min() / n for fi in fis])
                rc_ = np.array([[res[fi, ci][2]["rd_claim"][li][k0].min() / n for li in range(len(RD_LEVELS))] for fi in fis])
                hw = np.array([np.nanmax(res[fi, ci][2]["hw"][k0]) for fi in fis])
                lines.append(f"  no unresolved outcome, {cond}: minimum-configuration power lowest {pw.min():.3f} median {np.median(pw):.3f}; "
                             "reading 'below +0.05' by Holm level (lowest / median over frames) " + ", ".join(f"{a}: {rc_[:, li].min():.3f}/{np.median(rc_[:, li]):.3f}" for li, a in enumerate(RD_LEVELS)) + f"; mean half-width {hw.min():.3f} to {hw.max():.3f}")
            for fi in fis:
                tr, rN, r = res[fi, POW15]
                frows.append([size, group, FRAMES[fi][2], f"{rN[1]:.4f}", f"{rN[0][0]:.4f}", f"{rN[0][1]:.4f}", f"{rN[0][0] / max(rN[1], 1e-9):.2f}", f"{rN[0][1] / max(rN[1], 1e-9):.2f}",
                              f"{np.nanmax(res[fi, 0][2]['hw'][0]):.4f}", f"{np.nanmax(r['hw'][0]):.4f}",
                              f"{res[fi, 4][2]['pw'][0].min() / n:.3f}", f"{res[fi, 7][2]['pw'][0].min() / n:.3f}", f"{r['pw'][0].min() / n:.3f}",
                              f"{res[fi, 0][2]['rd_claim'][li_f][0].min() / n:.3f}", f"{res[fi, 3][2]['rd_claim'][li_f][0].min() / n:.3f}"])
            rat = np.array([[float(x[6]), float(x[7])] for x in frows if x[0] == size and x[1] == group])
            hrate = np.array([float(x[3]) for x in frows if x[0] == size and x[1] == group])
            arate = np.array([[float(x[4]), float(x[5])] for x in frows if x[0] == size and x[1] == group])
            lines.append(f"  at exact +0.15: historical detected N rate {hrate.min():.3f} to {hrate.max():.3f}; agent detected N rate {arate.min():.3f} to {arate.max():.3f}; ratio {rat.min():.2f} to {rat.max():.2f}")
    # common region over every frame group and mechanism
    lines.append("\nRegions passing in every frame group:")
    for mi, (mech, vecs) in enumerate(MECHS):
        allp = {}
        for row in vrows:
            if row[2] == mech:
                allp[(row[3], row[4], row[5])] = allp.get((row[3], row[4], row[5]), True) and bool(row[-1])
        ok = {v: all(allp[w] for w in vecs if all(a <= b + 1e-12 for a, b in zip(w, v))) for v in vecs}
        dc = [v for v in vecs if ok[v]]
        maxi = [v for v in dc if not any(w != v and all(a >= b - 1e-12 for a, b in zip(w, v)) for w in dc)]
        lines.append(f"  {mech}: {len(dc)} vectors; maximal: " + "; ".join(map(str, maxi)))
    lines.append(f"\nPackage diagnostic (limits {PKG_LIMITS}); share of samples in which it fires; samples with an author without packages are unassessable")
    for size in SIZES:
        for group in ("base", "linked working", "low V yield"):
            fis = [fi for fi, f in enumerate(FRAMES) if f[0] == size and f[1] == group]
            if not fis:
                continue
            for mi, (mech, vecs) in enumerate(MECHS):
                if mech not in ("independent", "package"):
                    continue
                mfire = {v: sum(res[fi, ci][2]["pkg_fire"][OFF[mi] + vi] for fi in fis for ci in range(len(CONDS))) / (n * len(fis) * len(CONDS)) for vi, v in enumerate(vecs)}
                dfire = {v: sum(res[fi, 0][2]["dev"]["fire"][OFF[mi] + vi] for fi in fis) / (N_DEV * len(fis)) for vi, v in enumerate(vecs)}
                lim = PKG_LIMITS if mech == "package" else (0.013, 0.013, 0.0075)
                ins = [v for v in vecs if all(a <= b + 1e-12 for a, b in zip(v, lim))]
                sel = [v for v in vecs if v not in ins][:0] + ([(0.1, 0.1, 0.1), (0.2, 0.2, 0.2), (0.2, 0.0, 0.0), (0.0, 0.0, 0.2)] if mech == "package" else [(0.0, 0.0, 0.013), (0.0, 0.0, 0.065), (0.013, 0.013, 0.013)])
                lines.append(f"  {group}, {mech}: main inside at most {max(mfire[v] for v in ins):.3f}, outside " + "; ".join(f"{v} {mfire[v]:.3f}" for v in sel)
                             + f" | development inside at most {max(dfire[v] for v in ins):.3f}, outside " + "; ".join(f"{v} {dfire[v]:.3f}" for v in sel))
            un_m = sum(res[fi, ci][2]["pkg_unass"] for fi in fis for ci in range(len(CONDS))) / (n * len(fis) * len(CONDS))
            un_d = sum(res[fi, 0][2]["dev"]["unass"] for fi in fis) / (N_DEV * len(fis))
            lines.append(f"  {group}: unassessable share main {un_m:.3f}, development {un_d:.3f}")
    lines.append("done")
    open(f"{out}.txt", "w").write("\n".join(lines) + "\n")
    with open(f"{out}_vectors.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["frame_size", "frame_group", "mechanism", "u_or_r_A1", "u_or_r_A2", "u_or_r_H", "error_upper_bound", "coverage_lower_bound", "lowest_power_015", "power_lower_bound_015", *[f"reading_error_upper_bound_holm_{a}" for a in RD_LEVELS], "worst_undefined_share", "passes"])
        wr.writerows(vrows)
    with open(f"{out}_frames.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["frame_size", "frame_group", "frame", "historical_detected_N_rate_at_015", "agent1_detected_N_rate_at_015", "agent2_detected_N_rate_at_015", "ratio1", "ratio2",
                     "mean_half_width_null", "mean_half_width_015", "power_005", "power_010", "power_015", f"reading_below_005_at_null_holm_{lf}", f"reading_below_005_at_0025_holm_{lf}"])
        wr.writerows(frows)
    print("\n".join(lines))



if __name__ == "__main__":
    main()
