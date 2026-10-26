# Loop 1, round 4: Peer A's critique of proposal_v4.md

Critic: Peer A (Claude Code). Author for this round: Peer B (Codex).

## Strengths to keep

Everything Peer B listed in round 3: the attribution requirement, the semantic PoV outcomes, common replay, the historical-context limitation, the disclosure plan; plus the six-configuration primary family with Holm, the 2 V and 8 N per protocol allocation, property-based search for every function, and the natural-stratum case-series rule.

## Points

### T1 [Major] [C6] Section 6.3 must report the v5 simulation, adopt its best-calibrated test, and stop calling v4's numbers validated

Section: 6.3, 8.
Problem: Peer B's R2 still stands for v4's text. The v4 numbers come from a bootstrap with an extra scaling factor, and v4 declares a procedure the simulation did not run. The v5 simulation now runs one declared procedure (unequal frames, inclusion weights, protocols as primary sampling units, Rao-Wu with P - 1 draws, per-configuration power, coverage and family-wise error with Monte Carlo error) and compares three tests.
Evidence: `tools/power_results_v5_summary.md`. The jackknife (delete one protocol) with a t(P - 1) reference is the best calibrated: family-wise error at most 0.07 and per-configuration coverage at least 0.91, against 0.09 and 0.89 for the basic bootstrap. With 25 protocols, per-configuration power is 0.93 to 0.98 (half null) and 0.96 to 0.99 (all configurations) for a true difference of about +0.10, and only 0.24 to 0.48 for about +0.04.
Required change: Declare the jackknife-t test as the primary RQ1 procedure, report the v5 numbers with their scenarios, state the residual liberal error (up to 0.07) and that the month-two rerun will calibrate the nominal level so the simulated family-wise error is at most 0.05, state the detectable difference honestly (about +0.10, not +0.04), and keep the stated simplifications.

### T2 [Major] [C6] Section 6.4 must report the RQ2 simulation of the declared model and drop the pilot contrast as a justification

Section: 6.4.
Problem: Peer B's R5 still stands for v4's text: v4 reports a function-only model and an unchecked "no fit failed", and cites the pilot contrast as support for the interaction size.
Evidence: `tools/power_results_v5_summary.md`: the declared nested protocol-and-function model, fitted with checked convergence, with writing and repair sharing effects, holds its level at 40 functions in 20 protocols (family-wise error 0.04 under the full null; 1 to 5 failed fits per 600) and has power about 0.90 for interactions of 1.5 and about 0.5 for 1.0. With 10 or 20 functions, family-wise error rises to 0.07 to 0.08.
Required change: Replace v4's RQ2 numbers with these, declare the likelihood-ratio test with a chi-square reference as the validated primary test (the parametric bootstrap becomes a sensitivity check, since it was not simulated), report failed fits, and present interaction sizes as scenarios, not as estimates from the pilot.

### T3 [Minor] [C4] Foresight-SWE's rate is joint completion and defect avoidance

Peer B's S1. Required change: describe 11.32% to 24.53% as the share of runs that complete the task and avoid the defect.

### T4 [Minor] [C4] The nonpublic-attacks study shows later exploitation, not fitting to visible checks

Peer B's S2. Required change: in section 7, separate evidence of fitting visible checks (Building to the Test, Partial Verification, Placebo Audits) from evidence that a first repair can remain exploitable (the nonpublic-attacks study, P2Patch, PatchBench, SlicePatch).

### T5 [Minor] [C7] RQ2's sample rule does not match the main sample

Peer B's S3. With 25 protocols the main sample has about 50 group V functions, which cannot supply 40 injected and up to 20 natural functions without overlap.
Required change: state that RQ2 draws an additional probability sample of eligible group V functions not in the RQ1 sample, to reach 40 functions with injected tests from at least 20 protocols, and that the natural stratum is every sampled group V function (RQ1 or RQ2 sample) with natural fault-enforcing tests, capped at 20; make the workload table follow this rule.

## Counts

- Blocking: 0
- Major: 2
- Minor: 3

## Most important change

Bring sections 6.3 and 6.4 in line with the v5 simulation, so that the proposal declares exactly the tests that were simulated and reports their calibration and power honestly, including the effect sizes the design cannot detect.
