# Loop 1, round 14: you are the author

Peer A agrees with your round-13 points R13.1 (Major) and R13.2 (Minor). Peer A's vote on proposal_v14 was DISAGREE on R13.1. C7 is stalled (your own finding in round 13) and goes to the committee as an open question; it is no longer on the peers' agenda, and votes from now on exclude it. The proposal must still state it plainly.

Revise /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/proposal_v14.md into proposal_v15, resolving R13.1 and R13.2 as you specified them: a fixed per-function construction procedure and allowance, eligibility defined by it, domain-weighted estimation with estimated constructible stratum shares and their uncertainty, and the construction-selection process in the readiness simulation.

New evidence by Peer A (check before you use any number; paths under /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/):
- tools/power_sim_v8.py gained `p_build` (probability, by stratum, that a sampled function's task is built within its own fixed allowance, independent of outcomes and of other functions) and a domain estimator: stratum means over built functions with inclusion weights, and constructible stratum shares estimated from the weighted built counts inside every jackknife replicate. The domain's true values use the constructible share pi_c = pi pV / (pi pV + (1 - pi) pN). With p_build unset it reproduces power_results_v11.txt exactly (checked).
- tools/power_sim_v20.py and tools/power_results_v20.txt: the fixed allocation (20 protocols, V cap 6, two attempts, earlier V assumption) under build probabilities (all built; 0.9/0.9; 0.7/0.9; 0.9/0.7; 0.6/0.6): RQ1a full-interval criterion with unresolved shares 0 and 0.005, and RQ1b power, coverage and half-width.
- The simulation assumes building is independent of outcomes. Building that depends on function difficulty, and so possibly on vulnerability, is not simulated; say so.

Also update the revised iteration-2 rebuttal (your round-12 version is /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/debate/rebuttal_iter2_peerB_r12.md) so every row matches proposal_v15, and add the open question (C7) in the form the committee should see.

Keep the section structure and everything not touched by these points. Use only numbers that are in the files. Follow the writing rules in /Users/minh/Documents/workspaces/secure-solvibe/CLAUDE.md. Abstract at most 150 words. Header: "Proposal version 15 (author of this revision: Peer B, Loop 1 round 14; version 14 was written by Peer A in round 13)."

Output, in this order:
1. `## Response to the agenda`: R13.1, R13.2: decision, what changed, sections.
2. `## Remaining concerns`: anything you still consider Blocking or Major, excluding the open question C7, or "none".
3. `===BEGIN PROPOSAL===`, the complete proposal_v15, `===END PROPOSAL===`.
4. `===BEGIN REBUTTAL===`, the complete revised iteration-2 rebuttal, `===END REBUTTAL===`.
