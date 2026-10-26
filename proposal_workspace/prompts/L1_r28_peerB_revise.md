# Loop 1, round 28: you are the author

Peer A agrees with all of your round-27 points (R27.1 to R27.8) and votes DISAGREE on R27.1 to R27.6. Before your turn Peer A built and ran the support simulation. Check every number and the code before using them (files under /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/):

- tools/power_sim_v44.py: an explicit confirmation-and-review state machine (its docstring states it step by step). Only working implementations register bundles, so known non-working implementations keep (W, D) = (0, 0) (R27.1). Rejected candidates are Binomial(3, (3/13)/3) per working implementation without a detected flaw, fixed per scenario and independent of the sample (R27.3). A bundle starts only if 1.0 h per candidate can be reserved; processing stops at the first bundle that cannot; a bundle stops at its first student-confirmed candidate; later candidates are "not needed"; reserved but unused time returns at bundle end; packages are reviewed in random order up to the review reserve (R27.2). The warning is computed from candidate-level statuses (R27.5). All ten V42 conditions including the margin and negative conditions; region corners for six scenarios; full V42 grids for the binding scenario (three candidates at 0.5 h) (R27.4). Stated simplification: the student confirms only true flaws and completed reviews confirm them.
- tools/power_results_v44.txt and _vectors.csv (4,000 studies; a 2,000-study run is kept as power_results_v44_2000.txt because its Bonferroni bounds were too wide to certify even the no-unresolved case).
- tools/power_sim_v44_demand.py and tools/power_results_v44_demand.txt: confirmation demand per main study by scenario at the null and at +0.15.

Peer A's reading (verify): validity (error, coverage, reading) passes in every scenario and mechanism. Power holds when candidates take about 0.5 h, or with one-candidate bundles and adverse time; it fails when every candidate takes the full 1.0 h, or with three-candidate bundles and adverse time, because the 177.7-h reserve runs out at +0.15 (39% to 96% of studies). The binding passing scenario reproduces the frozen region. The decisive unknown is time per candidate, which only the timed case measures.

Peer A's proposal for R27.6 (you decide): a preregistered measured-demand rule.
1. Inputs from development, per author: candidates per working implementation (including unfinished ones), position of the confirming candidate, time used per candidate (an unfinished candidate counts at its 1.0-h cap), rejected-candidate rate.
2. Uncertainty set: each rate and mean time at its upper limit from a protocol-level calculation, or, with fewer than two protocols with data or with no candidate for an author, the least favourable passing V44 scenario (three-candidate bundles at 0.5 h with the planning rejected rate) or the measured value if worse.
3. Reserve rule: run the V44 demand simulation with those inputs; the confirmation reserve must cover the 95th percentile of main-study demand at +0.15. If it does not, enlarge it in a fixed order: first reduce seeded validation from 60 to 45 pairs (frees about 46 student hours), then use the remaining month-10 analysis hours down to 30; if it still does not fit, the design returns to review. Then rerun V44 with the chosen reserve as part of the final check.

Revise /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/proposal_v28.md into proposal_v29 resolving R27.1 to R27.8, and revise debate/rebuttal_iter4_peerA_r27.md to match. Make the state machine in sections 5.7 and 6.2 identical to the simulator's; Peer A will update dev_case/README.md to match. Item 2 (the student's commitment and timed case) stays unsupplied; keep that plain. Follow /Users/minh/Documents/workspaces/secure-solvibe/CLAUDE.md. Abstract at most 150 words. Header: "Proposal version 29 (author of this revision: Peer B, Loop 1 round 28; version 28 was written by Peer A in round 27)." Mark any number that would need a new simulation as [pending] with exact conditions.

Output, in this order:
1. `## Response to the agenda`: R27.1 to R27.8: decision, what changed, sections.
2. `## Simulations needed`: each [pending] number with exact conditions, or "none".
3. `## Vote`: exactly one line, "AGREE: no Blocking/Major issues remain" or "DISAGREE: [list]", for proposal_v29 as you wrote it, excluding item 2 and the final-frame check.
4. `===BEGIN PROPOSAL===`, the complete proposal_v29, `===END PROPOSAL===`.
5. `===BEGIN REBUTTAL===`, the complete revised iteration-4 rebuttal, `===END REBUTTAL===`.
