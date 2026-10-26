"""Version 38: the rule for evidence of leaving the region, for two candidate frozen regions (round 22 support).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v38.py
Why: V35 and V37 are independent runs of the same check. At the boundary vector (0.013, 0.013, 0.0075) under the
protocol mechanism, the +0.15 power lower bound is 0.598 in V35 (fail) and 0.606 in V37 (pass). Two regions are therefore
candidates:
  box: every vector no larger than (0.013, 0.013, 0.0075) (the V37 region);
  both runs: vectors passing in V35 and V37, maximal (0.0075, 0.013, 0.0075), (0.013, 0.0075, 0.0075), (0.013, 0.013, 0.005).
Uses power_sim_v37.py's generator and rule (same 24 frames, 76 ordered vectors, four mechanisms) on fresh draws (seed 3801):
4,000 main samples of 22 protocols and 4,000 development samples of 3 protocols per frame, at the exact null (the
unresolved draws do not depend on the target). No inference is computed. The rule's grid-level counts are saved to
power_results_v38_rule_counts.npz (arrays main and dev, shape: frame x mechanism-vector x 512 levels) so that any region on
the grid can be evaluated later.
"""
import multiprocessing as mp
import numpy as np
import power_sim_v29 as v29
import power_sim_v30 as v30
import power_sim_v35 as v35
import power_sim_v37 as v37

REGIONS = {"box": [(0.013, 0.013, 0.0075)],
           "both runs": [(0.0075, 0.013, 0.0075), (0.013, 0.0075, 0.0075), (0.013, 0.013, 0.005)]}
N = 4000


def job(fi):
    name, rc, fr = v30.FRAMES[fi]
    fr.set_target(rc, 0.0)
    rng = np.random.default_rng([3801, fi])
    MV = len(v35.MECHS) * v37.NV
    out = {}
    for key, P, pi in (("main", v29.P, fr.pi), ("dev", 3, fr.pi3)):
        h = np.zeros((MV, 512), np.int64)
        for _ in range(N):
            cat = v37.draw(rng, fr, rc, P, pi)[0]
            hu, au = v37._masks(cat, v35._SCORE[fi])
            h[np.arange(MV), v37.rule_levels(cat, hu, au, P)] += 1
        out[key] = h
    return fi, out


def below(v, w):
    return all(a <= b + 1e-12 for a, b in zip(v, w))


if __name__ == "__main__":
    v37.init()
    with mp.Pool(8, initializer=v37.init) as pool:
        res = dict(pool.imap_unordered(job, range(24)))
    main = np.stack([res[fi]["main"] for fi in range(24)]); dev = np.stack([res[fi]["dev"] for fi in range(24)])
    np.savez_compressed("power_results_v38_rule_counts.npz", main=main, dev=dev)
    lines = [f"Rule for evidence of leaving the region; {N} main (22 protocols) and {N} development (3 protocols) samples per frame; 24 frames; share of samples in which the rule fires"]
    sel = [(0.0, 0.0, 0.013), (0.0, 0.0, 0.02), (0.0, 0.0, 0.03), (0.0, 0.0, 0.065), (0.013, 0.013, 0.013)]
    for rname, maxi in REGIONS.items():
        lines.append(f"\nRegion '{rname}', maximal vectors: " + "; ".join(map(str, maxi)))
        out_combo = np.array([not v37.inside(c, maxi) for c in range(512)])
        for label, H in (("main study", main), ("development", dev)):
            lines.append(f"  {label}:")
            for mi, mech in enumerate(v35.MECHS):
                fire = {vec: H[:, mi * v37.NV + vi][:, out_combo].sum() / H[:, mi * v37.NV + vi].sum() for vi, vec in enumerate(v37.VECS)}
                ins = [fire[v] for v in v37.VECS if any(below(v, m) for m in maxi)]
                lines.append(f"    {mech}: inside, at most {max(ins):.3f}; outside: " + "; ".join(f"{v} {fire[v]:.3f}" for v in sel))
    lines.append("done")
    open("power_results_v38.txt", "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
