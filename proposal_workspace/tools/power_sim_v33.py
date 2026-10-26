"""Version 33: full calibration and fresh validation, with the zero-event rule of power_sim_v32.py, for the two designs that
round 19 considers (Loop 1 point R18.2), reporting the +0.15 power bound separately for each unresolved setting.

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v33.py
Designs (two attempts per configuration; middle-rate cost with one audit-assisted task of 3.75 h per protocol):
20 x (V cap 2, N take 6), 877 h, and 22 x (V cap 1, N take 6), 880 h.
Conditions: power_sim_v32.CONDS (nine null conditions, +0.15 at eight unresolved settings, +0.10, negative alternatives).
Unresolved setting 0.0075 is the upper 80% limit when development sees no unresolved outcome in 216 (three cases, eight
functions, one historical and 2 x 4 agent implementations); 0.013 is the same for 120 outcomes (2 x 2 agent implementations).
Calibration 2,000 studies, validation 4,000 studies per frame and condition; Bonferroni-adjusted Clopper-Pearson bounds as
in power_sim_v30.py; the +0.15 power bound uses the Bonferroni count of all +0.15 checks (8 settings x 24 frames x 2).
"""
import csv
import multiprocessing as mp
import numpy as np
import power_sim_v30 as v30
import power_sim_v32 as v32

DESIGNS = [(20, 2, 6, 2), (22, 1, 6, 2)]
CONDS = v32.CONDS


def cost(P, vcap, nper, k):
    f = vcap + nper
    return P * (9 + f * 2.25 + f * (1 + 2 * k) * 0.328 + 3.75)


if __name__ == "__main__":
    fh = open("power_results_v33_frames.csv", "w", newline="")
    wr = csv.writer(fh)
    wr.writerow(["design", "frame", "condition", "unresolved", "target_c1", "target_c2", "studies", "familywise_error", "power_c1", "power_c2", "coverage_c1", "coverage_c2", "simultaneous_coverage", "undefined_share"])
    print("Full calibration (2,000 studies) and fresh validation (4,000 studies) on 24 frames and all conditions; zero-event rule for intervals", flush=True)
    for k, d in enumerate(DESIGNS):
        tag = f"{d[0]} protocols, V cap {d[1]}, N take {d[2]}, {d[3]} attempts per configuration ({cost(*d):.0f} h at middle rates)"
        v32.init(d)
        names = [f[0] for f in v30.FRAMES]
        with mp.Pool(8, initializer=v32.init, initargs=(d,)) as pool:
            cal = v32.run(pool, 3601 + k, CONDS, 2000)
            a_star = v32.holm_level(cal, CONDS, 2000)
            c_star = next((c for c in v30.CS if v30.check(cal, CONDS, 2000, v30.ALPHAS[0], c)[0]["cov"] >= 0.95), None)
            if a_star is None or c_star is None:
                print(f"  {tag}: calibration failed (Holm level {a_star}, multiplier {c_star})", flush=True); continue
            w, _, m = v30.check(cal, CONDS, 2000, a_star, c_star)
            print(f"  {tag}: selected Holm level {a_star}, multiplier {c_star}; calibration bounds: error {w['err']:.4f}, coverage {w['cov']:.4f}", flush=True)
            val = v32.run(pool, 3701 + k, CONDS, 4000)
        w, rows, m = v30.check(val, CONDS, 4000, a_star, c_star)
        print(f"  {tag}, validation (fresh draws, procedure frozen):")
        print(f"    worst family-wise error upper bound {w['err']:.4f} over {m[0]} null checks (<= 0.05): {'pass' if w['err'] <= 0.05 else 'FAIL'}")
        print(f"    worst marginal coverage lower bound {w['cov']:.4f} over {m[1]} checks (>= 0.95): {'pass' if w['cov'] >= 0.95 else 'FAIL'}")
        for ci, (cond, target, u) in enumerate(CONDS):
            ks = [key for key in rows if key[1] == ci]
            e = max(rows[key][1] for key in ks); cv = min(rows[key][3].min() for key in ks); sim = min(rows[key][4] for key in ks); und = max(rows[key][5] for key in ks)
            line = f"    {cond}, unresolved {u}: worst error {e:.3f}; lowest marginal coverage {cv:.3f}; lowest simultaneous coverage {sim:.3f}; undefined share up to {und:.4f}"
            pws = np.array([rows[key][2].min() for key in ks if np.all(np.abs(rows[key][0]) > 1e-9)])
            if pws.size:
                line += f"; minimum configuration power lowest {pws.min():.3f}, quartiles {np.percentile(pws, 25):.2f} / {np.median(pws):.2f} / {np.percentile(pws, 75):.2f}"
            if cond == "exact +0.15":
                lb = min(v30.lcb(round(x * 4000), 4000, m[2]) for key in ks for x in rows[key][2])
                line += f"; power lower bound {lb:.3f} ({'pass' if lb >= 0.60 else 'FAIL'} at 0.60)"
            print(line, flush=True)
        for (fi, ci), (tr, e, pw, cv, sim, und) in sorted(rows.items()):
            cond, _, u = CONDS[ci]
            wr.writerow([tag, names[fi], cond, u, f"{tr[0]:.4f}", f"{tr[1]:.4f}", 4000, f"{e:.4f}", f"{pw[0]:.4f}", f"{pw[1]:.4f}", f"{cv[0]:.4f}", f"{cv[1]:.4f}", f"{sim:.4f}", f"{und:.4f}"])
        fh.flush()
    fh.close()
    print("done")
