"""Version 45: the V44 checks rerun on the real frame instead of frames of 230 resampled protocols (iteration-4 item 7 and
R1's frame-size rerun).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v45.py [demand]
Frame: the 190 counted 2024 and 2025 Code4rena and Sherlock audits of ../evidence/frame_build/protocol_frame.csv, less the
three development protocols already drawn (../dev_case/drawn_protocols.csv): 187 protocols. Main inclusion probabilities
are proportional to the automated eligible count (the size measure actually used), certainty units capped at 1.
True strict counts per protocol: for the 20 protocols that are also in the 25-audit hand count, the hand strict N and strict
V (observed or upper bound, as the frame's V list); for the others, imputed per frame from a randomly chosen hand-counted
audit j: linked functions = round(size x linked_j / eligible_j), strict N = size - linked, strict V ~ Binomial(linked,
V_j / linked_j). So the size measure differs from strict N as in the accuracy check (ratio 1.03 to 1.40 on the 20 overlaps).
Everything else is V44 unchanged (power_sim_v44.job, the same 60 frame configurations, conditions, mechanisms, state
machine, reserves, warning and the frozen estimator). The development diagnostic samples three protocols with probability
proportional to size from the 187, as in V42 and V44.
Outputs: power_results_v45.txt and power_results_v45_vectors.csv; with argument "demand", power_results_v45_demand.txt
(confirmation demand without a reserve, the V44 demand computation on these frames). Studies per frame and condition:
4,000 (environment variable V45_N overrides it, for smoke tests only).
power_sim_v46.py runs the same code on project units (init("units")): a unit's size measure and strict counts are the sums
over its audits, and its audits share one protocol effect. With one audit per unit (V45) the random draws are unchanged.
"""
import csv
import multiprocessing as mp
import os
import pickle
import sys
from pathlib import Path
import numpy as np
import power_sim_v29 as v29
import power_sim_v30 as v30
import power_sim_v42 as v42
import power_sim_v44 as v44
import power_sim_v44_demand as v44d

HERE = Path(__file__).resolve().parent
WS = HERE.parent
N = int(os.environ.get("V45_N", 4000))
expit, P = v29.expit, v42.P
SOURCE = "audits"   # "audits": protocol_frame.csv, one unit per audit (V45); "units": protocol_units.csv, project units (V46)
TAGS = {"audits": ("v45", "V45: V44 on the real frame ({n} protocols: 190 counted Code4rena and Sherlock audits less three development protocols)"),
        "units": ("v46", "V46: V44 on the corrected frame of project units ({n} units: 185 counted audits grouped by project, development units removed)")}


def load(source="audits"):
    """Frame units as (unit_id, [(audit slug, automated eligible count), ...]), and the hand counts."""
    fb = WS / "evidence" / "frame_build"
    if source == "units":
        fr = [(r["unit_id"], [(m.rsplit(":", 1)[0], int(m.rsplit(":", 1)[1])) for m in r["members"].split()])
              for r in csv.DictReader(open(fb / "protocol_units.csv")) if r["development"] == "0"]
    else:
        dev = {r["protocol_id"] for r in csv.DictReader(open(WS / "dev_case" / "drawn_protocols.csv"))}
        fr = [(r["protocol_id"], [(r["protocol_id"], int(r["n_eligible"]))]) for r in csv.DictReader(open(fb / "protocol_frame.csv")) if r["protocol_id"] not in dev]
    hand = {r["slug"]: r for r in csv.DictReader(open(WS / "evidence" / "frame_audit" / "strict" / "per_audit_strict.csv"))}
    return fr, list(hand.values()), hand


FR, HAND, HMAP = load()


def counts(rng, vcol):
    """Size measure and true strict (V, N) per unit for one frame (sums over its audits); vcol is strict_v_observed or
    strict_v_upper_bound."""
    SM, NV, NN = [], [], []
    for _, members in FR:
        sm = sv = sn = 0
        for slug, m in members:
            h = HMAP.get(slug)
            if h is not None:
                nv, nn = int(h[vcol]), int(h["strict_n"])
            else:
                j = HAND[rng.integers(len(HAND))]
                linked = int(round(m * int(j["linked_eligible_functions"]) / int(j["eligible_functions"])))
                nn = m - linked
                nv = int(rng.binomial(linked, int(j[vcol]) / int(j["linked_eligible_functions"]))) if int(j["linked_eligible_functions"]) else 0
            sm += m; sv += nv; sn += nn
        SM.append(sm); NV.append(sv); NN.append(sn)
    return np.array(SM), np.array(NV), np.array(NN)


class Frame45(v42.Frame):
    def __init__(self, seed, vcol, hN, link, yld, working, vyield=None, aV=0.6, hV=0.9, aN0=0.10):
        rng = np.random.default_rng(seed)
        self.SM, self.NV, self.NN = counts(rng, vcol)
        M = self.SM.size
        # the rest of this block is v29.Frame.__init__ with the given counts
        sd_tot = np.sqrt(0.5**2 + 1.5**2 + 0.5**2)
        self.bA = {"V": v29.v8.calib(aV, sd_tot), "N": v29.v8.calib(aN0, sd_tot)}
        bH = {"V": v29.v8.calib(hV, np.hypot(0.5, 1.5)), "N": v29.v8.calib(hN, np.hypot(0.5, 1.5))}
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
                self.f[p, s] = dict(yh=rng.random(n) < expit(bH[s] + up[p] + hum), lat=lat, diff=diff, sh=sh)
        alld = np.concatenate([d["diff"] for d in self.f.values()])
        b = v42.calib_mean(alld, yld)
        for d in self.f.values():
            d["built"] = rng.random(d["diff"].size) < expit(b - d["diff"])
        self.shift = np.zeros(2)
        # v42.Frame.__init__ without the development draw: the three development protocols are already out of the frame
        rng = np.random.default_rng([seed, 7])
        self.pi = v29.incl_probs(self.SM.astype(float), P)
        self.working = working
        for key in sorted(self.f):
            d = self.f[key]
            d["score"] = 0.6 * d["sh"] / 1.5 + 0.8 * rng.normal(0, 1, d["sh"].size)
        if vyield is not None:
            vd = np.concatenate([d["diff"] for k, d in sorted(self.f.items()) if k[1] == "V"])
            bv = v42.calib_mean(vd, vyield)
            for k in sorted(self.f):
                if k[1] == "V":
                    d = self.f[k]; d["built"] = rng.random(d["diff"].size) < expit(bv - d["diff"])
        built = np.concatenate([d["score"][d["built"]] for d in self.f.values()])
        if working == "linked":
            a = v42.calib_mean(built, 0.72); h = v42.calib_mean(built, 0.95)
            for k in sorted(self.f):
                d = self.f[k]
                d["wa"] = expit(a - d["score"]); d["hw"] = rng.random(d["score"].size) < expit(h - d["score"])
        else:
            for d in self.f.values():
                d["wa"] = np.full(d["score"].size, 0.72); d["hw"] = np.ones(d["score"].size, bool)
        self.cert = self.pi >= 1 - 1e-12
        self.pi3 = v29.incl_probs(self.SM.astype(float), 3)
        self.bmap = {u: (-np.inf if u == 0 else v42.calib_mean(built, u, sign=1.0)) for u in sorted({x for v in v42.V76 for x in v})}


def build_frames():
    """The 60 V42 frame configurations, on the real frame."""
    out, i = [], 0
    for vname, vcol in (("upper", "strict_v_upper_bound"), ("observed", "strict_v_observed")):
        for rname, rc in v29.RECALLS.items():
            for hN in (0.05, 0.10):
                for link, yld in ((0.0, 0.9), (0.6, 0.7)):
                    for working in ("independent", "linked"):
                        out.append((len(FR), "base" if working == "independent" else "linked working", f"{vname}, recall {rname}, hN {hN}, link {link}, yield {yld}", rc, (4500 + i, vcol, hN, link, yld, working)))
                        i += 1
                out.append((len(FR), "low V yield", f"{vname}, recall {rname}, hN {hN}, link 0.6, yield 0.7, V yield 0.3", rc, (4500 + i, vcol, hN, 0.6, 0.7, "independent", 0.3)))
                i += 1
    return out


def init(source=None):
    global SOURCE, FR, HAND, HMAP
    if source is not None:
        SOURCE = source
        FR, HAND, HMAP = load(source)
    v44.N_STUDIES = v44.N_DEV = N
    v42.init(dict(sizes=(230,), zero_share=True, n_studies=N, rd_levels=[0.01], vacuous=True, groups=None, n_dev=N))
    v42.Frame, v42.FRAMES = Frame45, build_frames()


def frame_summary():
    lines = []
    for fi in (0, 30):
        fr = Frame45(*v42.FRAMES[fi][4])
        v, n = fr.NV.sum(), fr.NN.sum()
        lines.append(f"frame {fi} ({v42.FRAMES[fi][2]}): {fr.SM.size} protocols; size measure total {fr.SM.sum()}; strict N {n}, strict V {v} (V share {v / (v + n):.4f}); "
                     f"certainty protocols {int(fr.cert.sum())}; largest main inclusion probability below 1: {fr.pi[~fr.cert].max():.3f}")
    return lines


def demand():
    jobs = [(fi, t) for fi in range(len(v42.FRAMES)) for t in ((0.0, 0.0), (0.15, 0.15))]
    with mp.Pool(8, initializer=init, initargs=(SOURCE,)) as pool:
        res = pool.map(v44d.jobd, jobs)
    lines = [f"{TAGS[SOURCE][0].upper()} demand: confirmation hours per main study with no reserve, {len(v42.FRAMES)} real-frame configurations, 400 studies per frame and target"]
    for ti, t in enumerate(("null", "+0.15")):
        arr = np.concatenate([res[i] for i in range(len(jobs)) if i % 2 == ti])
        lines.append(t + " positives per study: median %.0f, 95th %.0f" % (np.median(arr[:, 0, 1]), np.percentile(arr[:, 0, 1], 95)))
        for si, sc in enumerate(v44.SCEN):
            d = arr[:, si, 0]
            lines.append("   " + str(sc) + " demand hours: median %.0f, 95th %.0f, 99th %.0f, max %.0f; share > 177.7: %.3f" % (np.median(d), np.percentile(d, 95), np.percentile(d, 99), d.max(), (d > 177.7).mean()))
        per = [np.percentile(res[i][:, si, 0], 95) for i in range(len(jobs)) if i % 2 == ti for si in range(len(v44.SCEN))]
        lines.append(f"   largest frame-specific 95th percentile over all scenarios: {max(per):.0f}")
    open(f"power_results_{TAGS[SOURCE][0]}_demand.txt", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))


def main():
    nfr, n, CONDS, NC, NS = len(v42.FRAMES), N, v44.CONDS, v44.NC, v44.NS
    res = {}
    with mp.Pool(8, initializer=init, initargs=(SOURCE,)) as pool:
        for fi, ci, r in pool.imap_unordered(v44.job, [(fi, ci) for fi in range(nfr) for ci in range(len(CONDS))], chunksize=1):
            res[fi, ci] = r
    pickle.dump(res, open(os.path.join(os.environ.get("CLAUDE_JOB_DIR", "."), "tmp" if os.environ.get("CLAUDE_JOB_DIR") else "", f"power_results_{TAGS[SOURCE][0]}_raw.pkl"), "wb"))
    lines = [TAGS[SOURCE][1].format(n=len(FR)) + f"; {nfr} frame configurations; {n} studies per frame and condition; reserves main {v44.RES_MAIN}, development {v44.RES_DEV}"]
    lines += frame_summary()
    rows = []

    def checks(k, m_err, m_cov, m_pw, m_rd):
        eub = max(v30.ucb(int(res[fi, ci]["err"][k]), n, m_err) for fi in range(nfr) for ci in v44.NULLC)
        clb = min(v30.lcb(int(x), n, m_cov) for fi in range(nfr) for ci in range(len(CONDS)) for x in res[fi, ci]["cov"][k])
        plb = min(v30.lcb(int(x), n, m_pw) for fi in range(nfr) for x in res[fi, v44.POW15]["pw"][k])
        pmin = min(x / n for fi in range(nfr) for x in res[fi, v44.POW15]["pw"][k])
        rub = max(v30.ucb(int(res[fi, ci]["rd_err"][k]), n, m_rd) for fi in range(nfr) for ci in v44.READERR)
        und = max(res[fi, ci]["undef"][k] for fi in range(nfr) for ci in range(len(CONDS))) / n
        return eub, clb, pmin, plb, rub, und

    m = (3 * NC * nfr, len(CONDS) * NC * nfr * 2, NC * nfr * 2, len(v44.READERR) * NC * nfr)
    lines.append(f"Region corners, every scenario (Bonferroni per scenario over {m[0]} error, {m[1]} coverage, {m[2]} power and {m[3]} reading checks)")
    for si, (k_pos, mode) in enumerate(v44.SCEN):
        fl0 = sum(res[fi, 0]["flags"][si] for fi in range(nfr)) / (n * nfr); fl15 = sum(res[fi, v44.POW15]["flags"][si] for fi in range(nfr)) / (n * nfr)
        un = sum(res[fi, 0]["dev"]["unass"][si] for fi in range(nfr)) / (n * nfr)
        lines.append(f"\npositive bundle {k_pos}, time {mode}: confirmation reserve ran out in {fl0[0]:.3f} (null) / {fl15[0]:.3f} (+0.15); review reserve in {fl0[1]:.3f} / {fl15[1]:.3f}; development warning unassessable {un:.3f}")
        for c, (mech, vec) in enumerate(v44.CORNERS):
            k = si * NC + c
            eub, clb, pmin, plb, rub, und = checks(k, *m)
            ok = eub <= 0.05 and clb >= 0.95 and plb >= 0.60 and rub <= 0.05
            u15 = np.mean([res[fi, v44.POW15]["unres"][k] for fi in range(nfr)], 0)
            fm = sum(res[fi, ci]["fire"][si, c] for fi in range(nfr) for ci in range(len(CONDS))) / (n * nfr * len(CONDS))
            fm15 = sum(res[fi, v44.POW15]["fire"][si, c] for fi in range(nfr)) / (n * nfr)
            dv = sum(res[fi, 0]["dev"]["fire"][si, c] for fi in range(nfr)) / (n * nfr)
            lines.append(f"  {mech} {vec if vec else ''}: error {eub:.4f}; coverage {clb:.4f}; reading {rub:.4f}; +0.15 power {pmin:.3f}/{plb:.3f}{'' if ok else ' FAIL'}; undefined {und:.4f}; "
                         f"unresolved at +0.15 (A1, A2, H) {u15[0]:.3f}/{u15[1]:.3f}/{u15[2]:.3f}; warning main {fm:.3f} (+0.15 {fm15:.3f}), development {dv:.3f}")
            rows.append(["corner", k_pos, mode, mech, vec, f"{eub:.4f}", f"{clb:.4f}", f"{rub:.4f}", f"{pmin:.4f}", f"{plb:.4f}", f"{und:.5f}", int(ok)])
    lines.append(f"\nFull grids for the binding scenario (positive bundle {v44.SCEN[v44.BIND][0]}, time {v44.SCEN[v44.BIND][1]}); Bonferroni per mechanism")
    base = NS * NC
    for mi, (mech, vecs) in enumerate(v42.MECHS):
        nv = len(vecs)
        mm = (3 * nv * nfr, len(CONDS) * nv * nfr * 2, nv * nfr * 2, len(v44.READERR) * nv * nfr)
        passv, worst = {}, []
        for vi, vec in enumerate(vecs):
            k = base + int(v42.OFF[mi]) + vi
            eub, clb, pmin, plb, rub, und = checks(k, *mm)
            passv[vec] = eub <= 0.05 and clb >= 0.95 and plb >= 0.60 and rub <= 0.05
            worst.append((eub, clb, rub, und))
            rows.append(["full", v44.SCEN[v44.BIND][0], v44.SCEN[v44.BIND][1], mech, vec, f"{eub:.4f}", f"{clb:.4f}", f"{rub:.4f}", f"{pmin:.4f}", f"{plb:.4f}", f"{und:.5f}", int(passv[vec])])
        dc, maxi = v44.region(passv, vecs)
        lines.append(f"  {mech}: worst error {max(w[0] for w in worst):.4f}; worst coverage {min(w[1] for w in worst):.4f}; worst reading {max(w[2] for w in worst):.4f}; worst undefined {max(w[3] for w in worst):.4f}; "
                     f"passing {sum(passv.values())} of {nv}; maximal: " + "; ".join(map(str, maxi)))
    lines.append("done")
    open(f"power_results_{TAGS[SOURCE][0]}.txt", "w").write("\n".join(lines) + "\n")
    with open(f"power_results_{TAGS[SOURCE][0]}_vectors.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["part", "positive_bundle", "time_mode", "mechanism", "vector", "error_upper_bound", "coverage_lower_bound", "reading_error_upper_bound", "lowest_power_015", "power_lower_bound_015", "worst_undefined_share", "passes"])
        wr.writerows(rows)
    print("\n".join(lines))


if __name__ == "__main__":
    init()
    demand() if sys.argv[1:] == ["demand"] else main()
