"""Version 41: the low-V-yield frames of power_sim_v40.py with one added rule (round 25).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v41.py
Why: in V40 the 12 low-V-yield frames (230 protocols, V construction yield 0.3) failed coverage (lower bound 0.92) because
about 7% of estimates were undefined. With one V function per protocol and a 0.3 yield, a sample often has a built V
function on which no agent attempt works, so the V working denominator is zero. Rule added: an author-stratum rate with no
working or unresolved implementation is bounded by 0 and 1 (its admissible range), and needs no further widening. Because V
is 1.5% to 3% of the domain, this widens the bounds by at most that share. Everything else is power_sim_v40.py (empty-stratum
rule, jackknife over every sampled protocol, frozen Holm 0.03 and multiplier 1.175, reading at Holm 0.01, 4,000 fresh
studies per frame and condition, seed 3901 + 230 with the low-V frames' own indices). Outputs: power_results_v41.txt,
power_results_v41_vectors.csv, power_results_v41_frames.csv.
"""
import power_sim_v39 as v39

CFG = dict(sizes=(230,), zero_share=True, n_studies=4000, rd_levels=[0.01], vacuous=True, groups=("low V yield",))

if __name__ == "__main__":
    v39.main(CFG, out="power_results_v41")
