# Loop 1, round 12: you are the author

Peer A checked your round-11 critique (`codex_raw/L1_r11_peerB_consensus.md` in your own thread) and agrees with all of R11.1 to R11.14 and with your 16 rebuttal corrections. Peer A's vote on proposal_v12 was DISAGREE on R11.1 to R11.9.

Revise /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/proposal_v12.md into proposal_v13, resolving R11.1 to R11.14 as you specified them. Also produce the revised rebuttal to the iteration-2 meta-review (start from /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/iter_2/rebuttal.md, apply your corrections, and update every row to match proposal_v13).

New evidence Peer A produced for this round (check it before you use any number; all paths under /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/):
- tools/power_sim_v17.py and tools/power_results_v17.txt (R11.4): the final RQ1b decision under the adverse-bound rule, two attempts, both directions; Holm level calibrated on exact nulls without unresolved results; validation on nulls with unresolved shares 0, 0.05 and 0.10, on partial nulls, and power across a grid of unresolved shares by author up to 0.10, at 15 and 20 protocols.
- tools/power_sim_v18.py and tools/power_results_v18.txt (R11.5, R11.6): the RQ1a criterion evaluated per configuration and per scenario (largest mean calibrated half-width, not an average), with the rate at which the calibrated interval of the bound toward zero excludes -0.10, for unresolved shares 0, 0.01 and 0.05, under three allocations.
- tools/power_sim_v8.py gained `unres_val` (bound values per stratum and author); with defaults it reproduces power_results_v13.txt exactly (checked by Peer A).
- evidence/63008/ Version 2 (R11.7): README.md section "Version 2", patches/tickiterator_function_body_v2.patch (one added line in the body of reset(TickIteratorDown); empty-range behaviour preserved), tests/Fixed63008_State.t.sol (fixed-state assertions), reproduce_v2.sh (no set -e; checks 12 expected outcomes), logs/v2_*.log and logs/v2_summary.log. It ran end to end and matched all 12 expected outcomes. Repository suite on the corrected code: 56 pass, 4 fail, the four tests that assert the old boundary behaviour.
- evidence/timings.md: measured wall-clock times of the three automated jobs (version 2 of the package took about 10 minutes).

Constraint on item 2 and R11.2: no development case has been timed with a person doing the human-review steps, and none can be produced by the two peers. Do not invent such data, and do not present LLM timings as human ones. The user (the PhD student) has been asked whether they will time development cases; there is no answer yet. Write the proposal so that it is honest about this: specify the fixed, capped minimum study you asked for in R11.2, with its total resource limit and its minimum evaluable output, and state exactly what the human development cases must show before the study is declared ready for confirmatory collection.

Keep the section structure and everything not touched by these points. Use only numbers that are in the files. Follow the writing rules in /Users/minh/Documents/workspaces/secure-solvibe/CLAUDE.md. The abstract must have at most 150 words. Header: "Proposal version 13 (author of this revision: Peer B, Loop 1 round 12; version 12 was written by Peer A in round 11)."

Output, in this order:
1. `## Response to the agenda`: one row per point (R11.1 to R11.14): decision, what changed, sections.
2. `## Remaining concerns`: anything you still consider Blocking or Major in your own revision, or "none".
3. `===BEGIN PROPOSAL===`, the complete proposal_v13, `===END PROPOSAL===`.
4. `===BEGIN REBUTTAL===`, the complete revised iteration-2 rebuttal, `===END REBUTTAL===`.
