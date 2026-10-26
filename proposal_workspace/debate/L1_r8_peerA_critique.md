# Loop 1, round 8: Peer A's critique of proposal_v9 and consensus vote

Proposal under critique: `proposal_v9.md` (written by Peer B; raw output `codex_raw/L1_r8_peerB_revision.md`).

## Check of v9 against the files

Every number v9 takes from the v10 simulation was checked against the result files.

- Section 6.3 calibration table (15 protocols: 0.04, 1.12, 1.34; 0.042, 0.948, 0.058; 20 protocols: 0.035, 1.18, 1.40; 0.038, 0.965, 0.038) matches `tools/power_results_v10_a.txt`.
- Section 6.3 power and width table matches the nine rows per protocol count in the same file. Smaller differences at 15 protocols: power 0.13, 0.22, 0.38 and half-widths 0.045 to 0.046. Larger differences: power 0.55 to 0.93 and half-widths 0.055 to 0.067. At 20 protocols: 0.13 to 0.59 with 0.039 to 0.041, and 0.70 to 0.98 with 0.049 to 0.060.
- Equivalence power at a true difference of zero (0.12 and 0.19) matches, and v9 correctly says this is the lower configuration-specific rate, not the chance that both configurations show equivalence.
- Section 6.6 tables match `tools/power_results_v10_b.txt` row by row.
- Section 5.9 precision table matches `tools/power_results_v10_c.txt`.
- The 20-protocol pessimistic subtotal (1,794 + 30 = 1,824 hours) does exceed the 1,800-hour ceiling, as v9 says. The 15-protocol reserve is 1,800 − 1,443 = 357 hours.

R7.1, R7.2 and R7.3 are resolved. The seeded validation is now funded at the size the plan states, and its precision is reported honestly. The equivalence check now uses data generated at the boundary and a family decision. Paper 2 now uses one outcome in every arm, and the allocation of 160 functions is tied to stated alternatives. The discovery gate is now one rule. Section 6.5 also states the reversal condition for each stratum (s_A/s_H = r_A/r_H), which keeps the rebuttal's promise in item 2.

## Remaining issues

### M1 (Major, C4 and C7): no workable assignment of audit-blind work in the main study

**Problem.** Section 5.4 says the request and primary-property builders "do not receive audit findings" and that "people who already know a development case's findings cannot provide its blind construction evidence". Section 8 adds that "the staffing plan identifies them", but no staffing plan is given. The same section assigns all task construction to the student. The V task row in the person-hour table bundles audit-informed work (tracing, PoV and variant, function-only correction) with blind work (specification) for the same person. Building the frame also needs audit knowledge: someone must read each finding to map it to its root-cause function and to label V and N. And the month-one demonstration uses the eight pilot findings, which the student already knows. As written, the primary endpoint depends on a blindness that the plan gives no one the means to deliver.

**Evidence.** `proposal_v9.md`, section 5.4 ("Audit-informed work uses separate records and contexts"), section 8 ("The staffing plan identifies them … The student cannot supply blinded evidence for a case they already know"), and the person-hour table (row "V task: tracing, specification, request audit, PoV and variant, function-only correction").

**Required change.** State, for each sampled protocol, who does each step and in which order, and budget it. For example: (1) a script maps finding line links to functions, and a second person, paid and outside the construction team, checks the mapping, the V and N labels and the multi-function exclusion; the sampling script then gives the student one shuffled list of sampled functions with the labels sealed; (2) the student, who has not opened that protocol's audit report or fix commits, writes the threat-model record, properties, functional checks and requests, and commits them with a timestamp; (3) only after that commit does the student open the audit for tracing, PoVs, function-only corrections and the request diagnostic; (4) for any protocol the student already knows (the five pilot protocols, and any recorded in a prior-exposure list made before sampling), the second person does the blind construction. Add the second person's hours as stated assumptions.

### M2 (Major, C6): the precision of the design comparison is not shown, although v9 rests the study's value on it

**Problem.** v9 says "the study is justified as an estimation and design-comparison study" (section 6.3), and section 6.4 reports the V-only estimate beside the weighted estimate. No simulation gives the precision of their difference. With only two V functions per protocol, this difference rests on 30 to 40 V functions, so it may be much less precise than the RQ1 difference.

**Evidence.** I ran the check. `tools/power_sim_v11.py` adds an option to the v8 data generator that also returns the V-only estimate and the design difference (V-only minus weighted), with their true values and delete-one-protocol jackknife errors. Results are in `tools/power_results_v11.txt`, `tools/power_results_v11_calib.txt` and `tools/power_results_v11_v4.txt`.

- Without calibration, the t-interval for the design difference covers in as few as 92.7% (15 protocols) and 91.8% (20 protocols) of studies on the calibration stream. A calibrated multiplier of 1.16 (15 protocols) or 1.14 (20) gives validation coverage of 0.947 (±0.018) and 0.955 (±0.017) on an independent stream. Mean calibrated half-widths are 0.252 and 0.211.
- With the calibrated multiplier, power to show a nonzero design difference at 15 protocols is 0.89 to 0.99 when the true difference is −0.40 or larger in size, 0.74 at −0.33, 0.25 to 0.48 at −0.18 to −0.26, and 0.11 to 0.25 at −0.10 to −0.19 when recall favours agents. At 20 protocols the same groups give 0.97 to 1.00, 0.86, 0.36 to 0.67, and 0.13 to 0.42.
- Allowing up to four V functions per protocol (15 protocols; the 15-protocol multiplier is reused, which is an approximation) gives half-widths of 0.146 to 0.172 instead of 0.200 to 0.230, and power 0.93 at −0.33 and 0.43 to 0.72 at −0.18 to −0.26.
- The pilot puts the likely difference in the well-powered range, with a caveat. Reading the code found the bug in 16 of 32 agent runs, against all eight historical implementations (`docs/pilot/pilot_results.md`). That is close to the scenarios with an agent V rate of 0.6. But it comes from eight findings, one request style and older configurations.

**Required change.** Add the v11 evidence to section 6.4, with the calibrated interval and the range of design differences the core can and cannot detect. Make the V allocation per protocol (two, or up to four) a month-two decision with a stated rule based on development rates and measured V-task hours, and show its cost in section 8.

### Minor

- m1. The header says "Proposal version 9." without the author and round, unlike earlier versions. Add "(author of this revision: Peer B, round 8)".
- m2. Section 6.4 could state the pilot's agent V rate (16 of 32 by code reading) as the reason the design difference is expected to be large, with its caveats.

## Vote

**DISAGREE: [M1 audit-blind work has no assignment or order; M2 precision of the design comparison not shown]**
