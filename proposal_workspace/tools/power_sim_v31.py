"""Version 31: version 30 with the negative alternatives and exact +0.10 inside the calibration set, run for each of the
three candidate allocations of proposal_v19 section 8 (round-18 Peer A support work).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v31.py
Why: in power_results_v30.txt the frozen procedure (Holm 0.0325, multiplier 1.175) passed the error bound on fresh draws
but failed coverage in the negative alternatives (they were not calibrated) and failed the +0.15 power requirement
(lower bound 0.558 < 0.60). This version (1) calibrates on every validation condition, so the multiplier covers the
near-zero negative targets, and (2) repeats calibration and fresh validation for 20 x (2, 6), 24 x (2, 4) and 17 x (2, 8).
Everything else is power_sim_v30.py: same 24 frames (seed 2901), same selection rules and Bonferroni-adjusted
Clopper-Pearson bounds, no fallback, 2,000 calibration and 4,000 validation studies per frame and condition.
Per-frame results go to power_results_v31_frames.csv.
"""
import csv
import multiprocessing as mp
import numpy as np
import power_sim_v29 as v29
import power_sim_v30 as v30

ALLOCS = [(20, 2, 6), (24, 2, 4), (17, 2, 8)]
CONDS = v30.VAL_CONDS


def init(alloc):
    v29.P, v29.VCAP, v29.NPER = alloc
    v30.init()


def report(rows, conds, attain):
    out = []
    for ci, (cond, target, u) in enumerate(conds):
        ks = [k for k in rows if k[1] == ci]
        e = max(rows[k][1] for k in ks); cv = min(rows[k][3].min() for k in ks); sim = min(rows[k][4] for k in ks); und = max(rows[k][5] for k in ks)
        line = f"    {cond}, unresolved {u}: worst error {e:.3f}; lowest marginal coverage {cv:.3f}; lowest simultaneous coverage {sim:.3f}; undefined share up to {und:.4f}"
        pws = np.array([rows[k][2].min() for k in ks if np.all(np.abs(rows[k][0]) > 1e-9)])
        if pws.size:
            line += f"; minimum configuration power lowest {pws.min():.3f}, quartiles {np.percentile(pws, 25):.2f} / {np.median(pws):.2f} / {np.percentile(pws, 75):.2f}"
        if target == "neg":
            t = np.array([rows[k][0] for k in ks])
            line += f"; targets {t.min():+.3f} to {t.max():+.3f} (-0.05 attainable in {attain} of {len(ks)} frames; target reached -0.05 in {int((t <= -0.05 + 1e-6).all(1).sum())})"
        out.append(line)
    return out


if __name__ == "__main__":
    fh = open("power_results_v31_frames.csv", "w", newline="")
    wr = csv.writer(fh)
    wr.writerow(["allocation", "frame", "condition", "unresolved", "target_c1", "target_c2", "studies", "familywise_error", "power_c1", "power_c2", "coverage_c1", "coverage_c2", "simultaneous_coverage", "undefined_share"])
    n_cal, n_val = 2000, 4000
    print(f"Calibration on all {len(CONDS)} conditions ({n_cal} studies) and fresh validation ({n_val} studies), 24 frames, per allocation; Bonferroni-adjusted one-sided Clopper-Pearson bounds, family confidence 0.95", flush=True)
    for k, alloc in enumerate(ALLOCS):
        init(alloc)
        attain = sum(int((fr.truth(rc, np.full(2, -15.0)) <= -0.05).all()) for _, rc, fr in v30.FRAMES)
        names = [f[0] for f in v30.FRAMES]
        tag = f"{alloc[0]} protocols, V cap {alloc[1]}, N take {alloc[2]}"
        with mp.Pool(8, initializer=init, initargs=(alloc,)) as pool:
            cal = v30.run(pool, 3101 + k, CONDS, n_cal)
            a_star = next((a for a in v30.ALPHAS if v30.check(cal, CONDS, n_cal, a, v30.CS[-1])[0]["err"] <= 0.05), None)
            c_star = next((c for c in v30.CS if v30.check(cal, CONDS, n_cal, v30.ALPHAS[0], c)[0]["cov"] >= 0.95), None)
            if a_star is None or c_star is None:
                print(f"  {tag}: calibration failed (Holm level {a_star}, multiplier {c_star}); no procedure selected", flush=True)
                continue
            w, _, m = v30.check(cal, CONDS, n_cal, a_star, c_star)
            print(f"  {tag}: selected Holm level {a_star}, multiplier {c_star}; calibration bounds: error {w['err']:.4f}, coverage {w['cov']:.4f}, +0.15 power {w['pw']:.3f}", flush=True)
            val = v30.run(pool, 3201 + k, CONDS, n_val)
        w, rows, m = v30.check(val, CONDS, n_val, a_star, c_star)
        print(f"  {tag}, validation (fresh draws, procedure frozen):")
        print(f"    worst family-wise error upper bound {w['err']:.4f} over {m[0]} null checks (<= 0.05): {'pass' if w['err'] <= 0.05 else 'FAIL'}")
        print(f"    worst marginal coverage lower bound {w['cov']:.4f} over {m[1]} checks (>= 0.95): {'pass' if w['cov'] >= 0.95 else 'FAIL'}")
        print(f"    worst +0.15 power lower bound {w['pw']:.3f} over {m[2]} checks (>= 0.60): {'pass' if w['pw'] >= 0.60 else 'FAIL'}")
        print("\n".join(report(rows, CONDS, attain)), flush=True)
        for (fi, ci), (tr, e, pw, cv, sim, und) in sorted(rows.items()):
            cond, _, u = CONDS[ci]
            wr.writerow([tag, names[fi], cond, u, f"{tr[0]:.4f}", f"{tr[1]:.4f}", n_val, f"{e:.4f}", f"{pw[0]:.4f}", f"{pw[1]:.4f}", f"{cv[0]:.4f}", f"{cv[1]:.4f}", f"{sim:.4f}", f"{und:.4f}"])
        fh.flush()
    fh.close()
    print("done")
