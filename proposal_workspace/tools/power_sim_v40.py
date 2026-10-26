"""Version 40: power_sim_v39.py on frames of the expected frozen size, with the empty-stratum rule (iteration-4 items 4, 6,
7 and 9; round 25).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v40.py
Why: V39 used frames of 50 and 70 protocols. The planned frame (proposal section 5.1, round 25) covers Code4rena, Sherlock
and Cantina audits from 2024 and 2025 with Solidity code: 313 in the inventory (evidence/frame_inventory/), about 237 usable
at the replacement rate of the frame audit (25 processed of 33 drawn). This run uses frames of 230 protocols, less three
development protocols. A stratum with no built function in a sample or jackknife replicate contributes 0 (V39 showed that,
without this rule, samples with no built V function make the estimate undefined). The reading of the upper limit uses Holm
level 0.01, the largest level whose error bound passed in every V39 group; these are fresh draws (seed 3901 + 230), so they
validate that choice. Everything else is power_sim_v39.py: frozen Holm 0.03 and multiplier 1.175, jackknife over every
sampled protocol, three frame groups (base, linked working, low V yield), three unresolved mechanisms, nine conditions,
4,000 studies per frame and condition. Outputs: power_results_v40.txt, power_results_v40_vectors.csv,
power_results_v40_frames.csv.
"""
import power_sim_v39 as v39

CFG = dict(sizes=(230,), zero_share=True, n_studies=4000, rd_levels=[0.01])

if __name__ == "__main__":
    v39.main(CFG, out="power_results_v40")
