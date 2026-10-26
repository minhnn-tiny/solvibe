"""Alternative RQ1 designs (per-configuration with 8 group N functions; pooled over six configurations). Run: uv run --with numpy --with statsmodels python tools/power_sim_v2_designs.py"""
import sys; sys.path.insert(0, "tools")
from power_sim_v2 import rq1
pi, aV = 0.10, 0.6
print("design                         protocols nV nN runs level   aN   hN  trueD  rej(0.5,1.5) rej(1.0,2.0)")
for label, nv, nn, k, level in (("per config, Holm 0.05/6", 2, 8, 3, 1-0.05/6),
                                ("pooled 6 configs, 0.05", 2, 4, 18, 0.95),
                                ("pooled 6 configs, 0.05", 2, 8, 18, 0.95)):
    for P in (25, 30):
        for aN, hN in ((0.0644, 0.02), (0.10, 0.02), (0.15, 0.02), (0.15, 0.05)):
            r1, d = rq1(P, nv, nn, k, pi, aV, aN, hN, 0.5, 1.5, level, sims=300)
            r2, _ = rq1(P, nv, nn, k, pi, aV, aN, hN, 1.0, 2.0, level, sims=300)
            print(f"{label:30s} {P:5d} {nv:3d} {nn:2d} {k:4d} {level:.4f} {aN:.3f} {hN:.2f} {d:+.3f}  {r1:.2f}        {r2:.2f}")
