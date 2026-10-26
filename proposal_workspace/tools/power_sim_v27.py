"""Version 27 (copy of version 26 with protocols drawn in proportion to their N count, power_sim_v8.py option pps_n).

Version 26 docstring follows. Version 26: the allocation question again, on the audited frame of evidence/frame_audit/ (25 random 2025+ contest
audits; uncapped V counts including fixes classified from the recommendation, and eligible N counts, drawn together
per protocol through power_sim_v8.py option frame_pairs).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v26.py
For each allocation: (a) the principal security-part decision as in power_sim_v24.py (Holm level calibrated on exact
security nulls, then power at exactly +0.10 and +0.15; no unresolved results); (b) RQ1a on D and on the security part:
multiplier chosen on a calibration stream, then largest mean half-width and the lowest configuration rate of the interval
lying wholly below -0.10, by true value. Scenarios: agents' V rate 0.6 or 0.9, three recall patterns, historical N rate
0.05 or 0.10. 200 studies per scenario. Also the observed-fixes-only V list as a lower-bound frame for the chosen row.
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8
from power_sim_v21 import RECALLS

V_REC = [6, 0, 2, 7, 11, 10, 2, 6, 15, 5, 6, 1, 2, 1, 4, 1, 7, 1, 4, 7, 2, 1, 1, 11, 5]
V_OBS = [6, 0, 0, 7, 0, 10, 2, 6, 10, 0, 0, 1, 1, 0, 3, 0, 0, 1, 4, 5, 0, 1, 1, 0, 4]
N_AUD = [177, 108, 49, 123, 327, 672, 139, 63, 381, 246, 161, 67, 70, 46, 183, 39, 92, 67, 38, 158, 73, 32, 24, 53, 233]
BASE = [(aV, rc, hN) for aV in (0.6, 0.9) for rc in RECALLS.values() for hN in (0.05, 0.10)]
ALLOC = [("20 x (2, 6), protocols in proportion to N", 20, 2, 6, V_REC), ("20 x (2, 6), proportional to N, observed-fix V counts", 20, 2, 6, V_OBS), ("24 x (2, 4), proportional to N", 24, 2, 4, V_REC), ("17 x (2, 8), proportional to N", 17, 2, 8, V_REC)]


def kw(vcap, nper, vl):
    return dict(parts=True, max_v=vcap, k=2, n_per=nper, sec=True, frame_pairs=list(zip(vl, N_AUD)), pps_n=True)


if __name__ == "__main__":
    cs = np.round(np.arange(1.0, 1.81, 0.02), 2)
    for name, P, vcap, nper, vl in ALLOC:
        q = stats.t.ppf(0.975, P - 1)
        rs = np.random.default_rng(2600 + P + vcap)
        # (a) principal decision on the security part
        def run_t(t, n=200):
            return [v8.run(P, ([aV] * 2, ("sec_target", t), 0.9, hN), rc, n, np.random.default_rng(rs.integers(2**62)), "D", **kw(vcap, nper, vl)) for aV, rc, hN in BASE]
        def holm_rej(r, a):
            d, se = r[12], r[13]
            return np.array([v8.holm(x, a) for x in 2 * stats.t.sf(np.abs(d) / se, P - 1)]), np.sign(d)
        nulls = run_t(0.0)
        a_star = max([a for a in (0.05, 0.045, 0.04, 0.035, 0.03, 0.025, 0.02) if max(holm_rej(r, a)[0].any(1).mean() for r in nulls) <= 0.05], default=0.02)
        line = [f"{name}: security-part Holm level {a_star}"]
        for t in (0.10, 0.15):
            pw = [(lambda rj: (rj[0] & (rj[1] > 0)).mean(0).min())(holm_rej(r, a_star)) for r in run_t(t)]
            line.append(f"power at exactly +{t:.2f}: {min(pw):.2f} to {max(pw):.2f} (median {np.median(pw):.2f})")
        # (b) RQ1a on D and security part
        scen = [(aV, rc, hN, add) for aV, rc, hN in BASE for add in (None, 0.10)]
        def run_d(seed):
            ss = np.random.default_rng(seed).integers(2**62, size=len(scen))
            return [v8.run(P, ([aV] * 2, None if add is None else [add] * 2, 0.9, hN), rc, 200, np.random.default_rng(s), "D", **kw(vcap, nper, vl)) for s, (aV, rc, hN, add) in zip(ss, scen)]
        cal, val = run_d(2700 + P + vcap), run_d(2800 + P + vcap)
        for key, idx in (("RQ1a on D", 6), ("RQ1a security part", 9)):
            pick = lambda data: [(r[idx], r[idx + 1], r[idx + 2]) for r in data]
            cover = lambda data, c: min(((d - c * q * se <= t) & (t <= d + c * q * se)).mean(0).min() for d, se, t in data)
            c = min([c for c in cs if cover(pick(cal), c) >= 0.95], default=cs[-1])
            vd = pick(val)
            hw = max((c * q * se).mean(0).max() for d, se, t in vd)
            rates = sorted((round(float(t.mean()), 2), (d + c * q * se < -0.10).mean(0).min()) for d, se, t in vd if t.mean() < -0.15)
            line.append(f"{key}: multiplier {c}, largest mean half-width {hw:.3f}; wholly below -0.10 by true value " + ", ".join(f"{t:+.2f}: {e:.2f}" for t, e in rates))
        print("\n    ".join(line), flush=True)
