"""Confirmation demand per main study under the V44 state machine, by scenario, at the exact null and at +0.15 (no
reserve applied): hours of student confirmation time if every registered bundle were processed. 400 studies per frame
and target, all 60 frames of 230 protocols (seed 4499). Run (from proposal_workspace/tools):
uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v44_demand.py
Output: power_results_v44_demand.txt.
"""
import sys
import numpy as np, multiprocessing as mp
import power_sim_v44 as v
import power_sim_v42 as v42

def jobd(args):
    fi, tgt = args
    size, group, name, rc, spec = v42.FRAMES[fi]
    fr = v42.Frame(*spec); fr.set_target(rc, np.array(tgt, float))
    rng = np.random.default_rng([4499, fi, int(tgt[0] * 100)])
    out = []
    for _ in range(400):
        cat = v42.draw(rng, fr, rc)
        nf = cat["hy"].size
        pos = np.concatenate([cat["hy"], cat["ay"].ravel()]); work = np.concatenate([cat["hw"], cat["aw"].ravel()])
        row = []
        for k_pos, mode in v.SCEN:
            k = np.where(work, np.where(pos, k_pos, rng.binomial(3, v.R_REJ / 3, pos.size)), 0)
            jpos = rng.integers(1, k_pos + 1, pos.size)
            c_rej, c_conf = {"0.5": (0.5, 0.5), "1.0": (1.0, 1.0), "adverse": (0.5, 1.0)}[mode]
            cost = np.where(pos, (jpos - 1) * c_rej + c_conf, k * c_rej)
            row.append((cost.sum(), pos.sum()))
        out.append(row)
    return np.array(out)

if __name__ == "__main__":
    v.init()
    jobs = [(fi, t) for fi in range(len(v42.FRAMES)) for t in ((0.0, 0.0), (0.15, 0.15))]
    with mp.Pool(8, initializer=v.init) as pool:
        res = pool.map(jobd, jobs)
    lines = []
    for ti, t in enumerate(("null", "+0.15")):
        arr = np.concatenate([res[i] for i in range(len(jobs)) if i % 2 == ti])   # (studies, scen, 2)
        lines.append(t + " positives per study: median %.0f, 95th %.0f" % (np.median(arr[:, 0, 1]), np.percentile(arr[:, 0, 1], 95)))
        for si, sc in enumerate(v.SCEN):
            d = arr[:, si, 0]
            lines.append("   " + str(sc) + " demand hours: median %.0f, 95th %.0f, 99th %.0f, max %.0f; share > 177.7: %.3f" % (np.median(d), np.percentile(d, 95), np.percentile(d, 99), d.max(), (d > 177.7).mean()))
    open("power_results_v44_demand.txt", "w").write("\n".join(lines) + "\n"); print("\n".join(lines))
