"""Version 16: RQ1b precision with two attempts per configuration instead of three (iteration-2 meta-review,
disagreement 6; R3 question 5). Data model power_sim_v8.py, endpoint D, default frame (2 + Poisson(2) V functions,
up to 2 V and 8 N per protocol), 6 scenarios (three recall patterns x two historical N rates) with added N rate +0.10,
400 studies per row. Reports the mean raw 95% half-width (t quantile, no multiplier) and the discovery campaigns.
Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels python power_sim_v16.py
"""
import numpy as np
from scipy import stats
import power_sim_v8 as v8

RECALLS = {"equal": (0.7, 0.7, 0.7, 0.7), "agents higher": (0.8, 0.8, 0.5, 0.5), "humans higher": (0.5, 0.5, 0.8, 0.8)}
if __name__ == "__main__":
    rng = np.random.default_rng(1616)
    for P in (15, 20):
        q = stats.t.ppf(0.975, P - 1)
        for k in (3, 2):
            hw = [(q * v8.run(P, ([0.6] * 2, [0.10] * 2, 0.9, hN), rc, 400, rng, "D", k=k)[1]).mean()
                  for rc in RECALLS.values() for hN in (0.02, 0.05)]
            print(f"P={P}, attempts {k}: mean raw half-width {min(hw):.4f} to {max(hw):.4f}; campaigns {P * 10 * (1 + 2 * k)}", flush=True)
