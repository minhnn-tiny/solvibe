"""Version 28: one simulation that combines the parts checked separately in v24, v25 and v27 (round-16 Major point 1).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v28.py [observed|upper]
Frame: M = 200 protocols whose (V, N) counts are resampled from the 25 audited pairs of evidence/frame_audit/ (argument
"observed": strict V from observed fixes only; "upper": strict V including fixes classified from the recommendation;
both from evidence/frame_audit/strict/, with strict N counts). Everything in the frame is fixed across studies:
protocol effects, protocol-by-author effects, function effects, each historical implementation's vulnerability, each agent
configuration's vulnerability probability per function, and whether each function's task is built under its own fixed
allowance (probability expit(b - difficulty), difficulty linked to the function effect by `link`, b set to the target yield).
Target: the constructible-domain security component of proposal_v17 section 6.2: for each stratum, the agents' detected-
vulnerability rate among working attempts minus the historical rate, standardized by the domain's stratum shares. It is set
EXACTLY on the frame for each configuration by shifting the agents' N-stratum intercept (bisection).
Study: 20 protocol draws with probability proportional to N count (with replacement; Hansen-Hurwitz weights), up to 2 V and
6 N functions per draw, unbuilt functions dropped, two attempts per configuration, agents working with probability 0.9 x 0.8,
detection by author and stratum. Unresolved results: each agent attempt and each historical implementation is unresolved with
probability u; the bounds of section 6.2 are used: the lower conditional rate treats every unresolved implementation as
working and not vulnerable, the upper as working and vulnerable. Decision: for each configuration, the t(P - 1) test on the
bound on the claimed side (lower bound of the difference for "agents worse": agents' lower rate minus historical upper rate;
upper bound for "agents better"), delete-one-draw jackknife, Holm across the two configurations. The Holm level is calibrated
on exact domain nulls without unresolved results (largest on a grid with worst family-wise error <= 0.05), then validated on
exact nulls with u = 0.005 and 0.013, on a partial null, and used for power at exactly +0.10 and +0.15 (u = 0 and 0.013).
Scenarios: recall equal / agents higher / humans higher; historical N rate 0.05 or 0.10; construction (link 0, yield 0.9)
or (link 0.6, yield 0.7); agents' V rate 0.6, historical V rate 0.9. 400 studies per condition.
"""
import sys
import numpy as np
from scipy import stats
import power_sim_v8 as v8

expit = v8.expit
M, P, VCAP, NPER, K = 200, 20, 2, 6, 2
V_OBS = [5, 0, 0, 6, 0, 9, 2, 6, 10, 0, 0, 1, 1, 0, 3, 0, 0, 1, 1, 4, 0, 1, 1, 0, 3]   # strict, evidence/frame_audit/strict/
V_REC = [5, 0, 2, 6, 11, 9, 2, 6, 15, 5, 6, 1, 2, 1, 4, 1, 7, 1, 1, 6, 1, 1, 1, 11, 4]   # strict upper bound
N_AUD = [177, 108, 49, 123, 327, 672, 139, 62, 381, 246, 161, 67, 70, 46, 183, 39, 92, 67, 38, 158, 73, 32, 24, 53, 233]   # strict N
RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}


class Frame:
    def __init__(self, rng, vlist, hN, link, yld, aV=0.6, hV=0.9, aN0=0.10):
        pick = rng.integers(0, len(vlist), M)
        self.NV, self.NN = np.array(vlist)[pick], np.array(N_AUD)[pick]
        sd_tot = np.sqrt(0.5**2 + 1.5**2 + 0.5**2)
        self.bA = {"V": v8.calib(aV, sd_tot), "N": v8.calib(aN0, sd_tot)}
        bH = {"V": v8.calib(hV, np.hypot(0.5, 1.5)), "N": v8.calib(hN, np.hypot(0.5, 1.5))}
        up, upa = rng.normal(0, 0.5, M), rng.normal(0, 0.5, M)
        self.f = {}
        for p in range(M):
            for s, n in (("V", self.NV[p]), ("N", self.NN[p])):
                if n == 0:
                    continue
                sh = rng.normal(0, 1.5, n)
                hum = 0.3 * sh + np.sqrt(0.91) * rng.normal(0, 1.5, n)
                lat = np.array([up[p] + upa[p] + np.sqrt(0.5) * sh + np.sqrt(0.5) * rng.normal(0, 1.5, n) for _ in range(2)])
                diff = link * sh / 1.5 + np.sqrt(1 - link**2) * rng.normal(0, 1, n)
                self.f[p, s] = dict(yh=rng.random(n) < expit(bH[s] + up[p] + hum), lat=lat, diff=diff)
        alld = np.concatenate([d["diff"] for d in self.f.values()])
        lo, hi = -20.0, 20.0
        for _ in range(100):
            mid = (lo + hi) / 2
            lo, hi = (lo, mid) if expit(mid - alld).mean() > yld else (mid, hi)
        for d in self.f.values():
            d["built"] = rng.random(d["diff"].size) < expit((lo + hi) / 2 - d["diff"])
        self.shift = np.zeros(2)

    def pa(self, s, d):                                   # agents' vulnerability probability per configuration
        return np.array([expit(self.bA[s] + (self.shift[c] if s == "N" else 0.0) + d["lat"][c]) for c in range(2)])

    def truth(self, recall, shift=None):
        sAV, sAN, sHV, sHN = recall
        old = self.shift.copy()
        if shift is not None:
            self.shift = shift
        out, cnt = {}, {}
        for s, sA, sH in (("V", sAV, sHV), ("N", sAN, sHN)):
            ds = [d for (p, ss), d in self.f.items() if ss == s]
            pa = np.concatenate([self.pa(s, d)[:, d["built"]] for d in ds], axis=1)
            yh = np.concatenate([d["yh"][d["built"]] for d in ds])
            out[s] = pa.mean(1) * sA - yh.mean() * sH
            cnt[s] = yh.size
        self.shift = old
        shr = cnt["V"] / (cnt["V"] + cnt["N"])
        return shr * out["V"] + (1 - shr) * out["N"]

    def set_target(self, recall, target):
        target = np.broadcast_to(np.asarray(target, float), (2,))
        for c in range(2):
            lo, hi = -15.0, 15.0
            for _ in range(60):
                mid = (lo + hi) / 2
                sh = self.shift.copy(); sh[c] = mid
                lo, hi = (mid, hi) if self.truth(recall, sh)[c] < target[c] else (lo, mid)
            self.shift[c] = (lo + hi) / 2
        tr = self.truth(recall)
        assert np.allclose(tr, target, atol=1e-6), (tr, target)
        return tr


def study(rng, fr, recall, u):
    sAV, sAN, sHV, sHN = recall
    pp = fr.NN / fr.NN.sum()
    draws = rng.choice(M, P, p=pp)
    # per draw and stratum: agents [config] (Y, W, U) and historical (Y, W, U), weighted
    A = np.zeros((2, 2, 3, P)); H = np.zeros((2, 3, P)); B = np.zeros((2, P))
    for j, p in enumerate(draws):
        hh = 1.0 / (P * pp[p])
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
            hu = rng.random(idx.size) < u
            H[st, :, j] = w * np.array([(hy & ~hu).sum(), (~hu).sum(), hu.sum()])
            pa = fr.pa(s, d)[:, idx]
            for c in range(2):
                work = (rng.random((K, idx.size)) < 0.9) & (rng.random((K, idx.size)) < 0.8)
                y = work & (rng.random((K, idx.size)) < pa[c]) & (rng.random((K, idx.size)) < sA)
                au = rng.random((K, idx.size)) < u
                A[st, c, :, j] = w * np.array([(y & ~au).sum(), (work & ~au).sum(), au.sum()])
    def bounds(m):                                        # lower and upper difference bounds of the standardized component
        lo_, hi_ = 0.0, 0.0
        shr_v = (B[0] * m).sum(-1); shr = (shr_v / (shr_v + (B[1] * m).sum(-1)))[..., None]
        out = []
        for st in (0, 1):
            Ay, Aw, Au = [(A[st, :, i] * m[..., None, :]).sum(-1) for i in range(3)]
            Hy, Hw, Hu = [((H[st, i] * m).sum(-1))[..., None] for i in range(3)]
            vAL, vAU = Ay / (Aw + Au), (Ay + Au) / (Aw + Au)
            vHL, vHU = Hy / (Hw + Hu), (Hy + Hu) / (Hw + Hu)
            out.append((vAL - vHU, vAU - vHL))
        wv = shr; wn = 1 - shr
        return wv * out[0][0] + wn * out[1][0], wv * out[0][1] + wn * out[1][1]
    with np.errstate(invalid="ignore", divide="ignore"):
        L0, U0 = bounds(np.ones(P)); Lj, Uj = bounds(1.0 - np.eye(P))
    seL = np.sqrt((P - 1) / P * ((Lj - np.nanmean(Lj, 0)) ** 2).sum(0))
    seU = np.sqrt((P - 1) / P * ((Uj - np.nanmean(Uj, 0)) ** 2).sum(0))
    return L0, seL, U0, seU


def decide(res, a, tr):
    L, sL, U, sU = (np.array([r[i] for r in res]) for i in range(4))
    pl, pu = 2 * stats.t.sf(np.abs(L) / sL, P - 1), 2 * stats.t.sf(np.abs(U) / sU, P - 1)
    p = np.where(L > 0, pl, np.where(U < 0, pu, 1.0)); sign = np.where(L > 0, 1, np.where(U < 0, -1, 0))
    p = np.nan_to_num(p, nan=1.0)
    rej = np.array([v8.holm(x, a) for x in p])
    err = (rej & ((np.abs(tr) < 1e-9) | (np.sign(tr) != sign))).any(1).mean()
    pw = (rej & (sign == np.sign(tr)) & (np.abs(tr) > 1e-9)).mean(0)
    return err, pw


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "upper"
    vlist = V_OBS if which == "observed" else V_REC
    rng = np.random.default_rng(2801 if which == "upper" else 2802)
    alphas = [0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02]
    frames = []
    for rname, rc in RECALLS.items():
        for hN in (0.05, 0.10):
            for link, yld in ((0.0, 0.9), (0.6, 0.7)):
                frames.append((f"recall {rname}, hN {hN}, link {link}, yield {yld}", rc, Frame(rng, vlist, hN, link, yld)))
    print(f"V counts: {which}; frame M = {M}; draws in proportion to N; {len(frames)} frames; 400 studies per condition", flush=True)
    cal = []
    for name, rc, fr in frames:
        tr = fr.set_target(rc, 0.0)
        cal.append((tr, [study(rng, fr, rc, 0.0) for _ in range(400)]))
    a_star = max([a for a in alphas if max(decide(res, a, tr)[0] for tr, res in cal) <= 0.05], default=0.02)
    print(f"Holm level {a_star} (exact domain nulls, no unresolved results)", flush=True)
    for cond, target, u in (("null", 0.0, 0.0), ("null", 0.0, 0.005), ("null", 0.0, 0.013), ("partial null", (0.0, 0.10), 0.0),
                            ("+0.10", 0.10, 0.0), ("+0.10", 0.10, 0.013), ("+0.15", 0.15, 0.0), ("+0.15", 0.15, 0.013)):
        errs, pws = [], []
        for name, rc, fr in frames:
            tr = fr.set_target(rc, target)
            e, pw = decide([study(rng, fr, rc, u) for _ in range(400)], a_star, tr)
            errs.append(e); pws.append(pw.min() if np.all(tr > 1e-9) else np.nan)
        if cond.endswith("null"):
            print(f"  {cond}, unresolved {u}: family-wise error by frame " + ", ".join(f"{e:.3f}" for e in errs) + f"; worst {max(errs):.3f}", flush=True)
        else:
            pws = np.array(pws)
            print(f"  exact {cond}, unresolved {u}: minimum configuration power by frame " + ", ".join(f"{x:.2f}" for x in pws) + f"; lowest {np.nanmin(pws):.2f}, median {np.nanmedian(pws):.2f}", flush=True)
