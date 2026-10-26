# Rebuttal to the iteration-4 meta-review

Authors: Peer A and Peer B. Revised by Peer B in Loop 1 round 30.

This response refers to proposal version 31.

## Student evidence

The student signed a dated commitment on 26 October 2026. It gives 37.5 research hours a week with no coursework or teaching. Timed case 1 is planned from 30 October to 13 November 2026.

The first complete timed case is still unsupplied. The committee requires it before acceptance. We agree. A schedule is not a substitute.

The exposure record, second person, both adjudicators and funding remain open.

The three development audits were drawn from the original frame with a seed recorded before that frame was built. The draw is retained with its original probabilities. Case 1 is The Wildcat Protocol.

The corrected main frame groups related audits into project units and removes every project containing a development audit. Development results do not enter the main vulnerability estimates.

Selected-demand and final-frame results remain pending until development and preparation supply their inputs.

## Responses to required changes

| Item | Status | Response | Sections |
|---|---|---|---|
| 1. Confirmation and review limits | Revised | Each candidate has a 1.0-hour student cap and each package has 0.5 hours per adjudicator. The fixed state machine registers working implementations, reserves complete bundles, stops at the first student-confirmed candidate and returns unused reservation to the same source. Independent review determines the final label. Exhausted work remains unresolved. The initial adjudicator ceiling is 205 hours each. A fixed pre-collection funding sequence can enlarge confirmation capacity without changing the main sample. | 5.7, 6.2, 8 |
| 2. Commitment and timed case | Commitment supplied; timed case not supplied | The signed commitment and original development draw are recorded. The timed case remains a committee precondition. It must include probability-selected functions, valid roles, candidate confirmation and both adjudications, with human and machine time separated. | 8 |
| 3. Reading a null result | Revised | The +0.05 margin remains a judgment of material excess, not a safety threshold. Reading uses Holm 0.01. V46 retains all ten conditions, including both ordered partial-margin conditions and the feasible negative alternative. Its worst full-grid reading-error upper bound is 0.0369. A broad null remains inconclusive. | 3, 6.3 |
| 4. Working status and difficulty | Revised | The linked-working frame group remains in V46. Only known-working implementations register confirmation bundles, so reserve exhaustion cannot turn a known functional failure into a possible positive. Separate unknown-working mechanisms retain adverse bounds. | 5.5, 5.7, 6.2, 6.3 |
| 5. Same-function comparison | Retained | The secondary comparison uses functions where historical code works and at least one agent attempt works. It reports retained counts and preserves sampling weights. Its interval is not presented as validated. | 6.1, 6.3 |
| 6. Package-linked unresolved outcomes | Revised | V46 includes the package mechanism alongside reserve exhaustion. The warning uses candidate assessment statuses. “Not needed” and non-working closures are excluded from its denominator. Unfinished confirmation and review remain included. An unassessable warning does not automatically stop launch; missing demand information receives conservative defaults. | 5.7, 6.3, 8 |
| 7. Frame size and certainty units | Revised with corrected project units | The corrected frame has 185 retained audits grouped into 155 projects. Removing all development projects leaves 152 main units. V46 samples project units using their recorded size measures and deletes whole units in the jackknife, including the certainty unit. Dependencies and duplicate audit snapshots no longer supply separate sampling units. The final frame check remains mandatory. | 5.1, 5.2, 6.3 |
| 8. Cut candidates | Retained | Separate natural-investigation cells assess campaigns with cut or unfinished lists, within 48 first assessments and 120 auditor hours. Weighted sensitivity estimates remain secondary. | 5.9 |
| 9. V construction | Retained | Development returns to review if V tasks were sampled but none was built. Yields remain descriptive. Low-V settings remain in the simulation checks. The main cap is one V function per project unit, not per audit. | 5.2, 6.3, 8 |
| 10. Confirmed rediscovery gate | Retained and funded | Gate success requires execution and both adjudications. Both assessments reserve 16 target packages and 18.4 student hours for operation and confirmation. | 5.9, 8 |
| 11. RQ1a and V share | Retained with clearer provenance | The flagged-only analysis is descriptive. The earlier hand count gives V shares of 1.5% to 2.9%; these are not measured shares of the corrected main frame. V46 still uses imputed strict counts for most audits. No validated RQ1a interval is claimed. | 3, 5.1, 6.4 |
| 12. Related work | Retained | Mahmud et al. and SolBehave remain included with distinctions in tasks, generators, sampling and security outcomes. | 7 |
| 13. Factual answers | Updated | Appendix B states the corrected population, project units, development treatment, candidate statuses, released reservations, warning denominators, funding limits and conservative demand defaults. Human timing and compute prices remain missing. | 8, Appendix B |

## Corrected population and sampling unit

The earlier 190-record count contained defects.

The Krystal records `code4rena-396` and `code4rena-399` referred to the same counted repository and commit. Inverse Finance had been counted from Solmate after the contest repository failed to fetch. Unruggable also included another contest’s repository. Coded Estate was counted from an older contest repository. reNFT and Garden used repositories outside the contest organisations.

The corrected operational rule admits only represented audits with linked code in `code-423n4` or `sherlock-audit`, where the repository’s year-month prefix is within one month of the inventory audit month. The linked version must be accessible and contain scoped Solidity code.

This is an explicit population restriction. It does not establish that excluded audits have no public code elsewhere. Exact sampled mapping still verifies that the retained repository and snapshot match the audit.

The corrected outputs contain:

- 185 retained audits: 83 Code4rena and 102 Sherlock;
- 143 audits from 2024 and 42 from 2025;
- 22,322 automatically eligible function occurrences;
- 155 project units, including 24 with more than one retained audit;
- 152 main project units after development-project exclusion, with size measures totaling 21,211.

The exclusive scope categories are 74 `scope.txt`, 109 README and two automatic.

Resolved commits, scope-file hashes and in-scope file-list hashes are recorded in `frame_snapshots.csv`. Later work uses those commits rather than moving branches.

The main population is conditional on the corrected frame without the development projects. It is not all public audits or all Solidity projects.

The main sample remains 22 units. Each unit supplies up to one V and six N functions pooled across its retained audits. We do not sample one audit first or grant the function allowance separately to each member audit.

The jackknife deletes all observations from a project together.

## Treatment of development

We retain the original draw: Wildcat, Perennial V2 Update #3 and Fenix Finance. Their records and automated counts were not changed by the correction.

Their original probabilities describe the original draw. We do not replace those probabilities with corrected-frame probabilities.

The development cases are not claimed to represent the corrected project frame. They support procedure and workload planning under explicit transfer assumptions. They do not enter the main outcome estimates.

The entire Perennial project is removed from the main frame, including Updates #2 and #4. Wildcat and Fenix are also removed.

V45’s hypothetical development diagnostic samples from its remaining audit frame. V46’s samples from its remaining project frame. Neither is a conditional validation of the three selected development cases.

## What the simulations establish

V44 fixed the sample-dependent rejected-candidate calibration. Working implementations without a detected flaw receive a fixed Binomial rejected-candidate distribution with mean 3/13. This is a planning conditional rate, not the observed overall pilot rate.

The six workloads differ in positive bundle size and candidate time. All receive corner checks over all ten conditions. The three-candidate, 0.5-hour workload receives the full mechanism grids.

V45 applied this procedure to the original audit frame. That frame has now been corrected, so V45 is historical evidence.

V46 uses the corrected 152-unit frame. Unit size measures and strict counts are sums across member audits. Generated functions share a project effect. Most strict counts remain imputed from the hand-counted audits.

V46’s full-grid bounds are:

| Criterion | Worst bound |
|---|---:|
| Directional error, upper | 0.0433 |
| Coverage, lower | 0.9545 |
| Margin-reading error, upper | 0.0369 |
| Recorded undefined share | 0 |

Power is lower than under the earlier frame.

For the favorable workloads, the no-added-unresolved corner has lowest +0.15 power 0.722, with lower bound 0.693.

Under the protocol mechanism:

- \((0.0075,0.0075,0.0075)\) has lowest power 0.611 and lower bound 0.580;
- \((0.013,0.013,0.005)\) has lowest power 0.622 and lower bound 0.592.

Both former corners fail the 0.60 requirement in every workload.

The common full-grid implementation region has maximal vectors \((0.013,0.0075,0.005)\) and \((0.013,0.013,0)\).

We adopt only vectors that also pass with the two configurations swapped. The symmetric region therefore has maximal vectors:

- \((0.0075,0.0075,0.005)\);
- \((0.013,0.013,0)\).

The separate package region remains \((0.05,0.05,0.2)\).

This is a restriction of the observed passing sets, not a symmetry assumption used to omit simulations.

The region is narrow. It is an operating assumption, not a completion rate established by development. We preserve the 0.60 requirement and do not add unfunded units.

The full-grid workload is not proved to dominate the other workloads. Every retained launch profile must pass the full matrix.

## State-machine scope and simplifications

A student-confirmed package is provisional. The actual procedure still requires both adjudicators.

The bundle stops at that provisional package. Later candidates are “not needed,” and the queue is not reopened after a completed review rejection.

V44 through V46 assume the student submits only true flaws and completed reviews confirm them. The proposal states that assumption. Material rejection workload observed in development must be added to the final model.

Known non-working implementations retain W = 0 and D = 0. Their security is not measured by primary confirmation.

Unknown-working failures remain distinct from confirmation exhaustion.

## Demand selection and funding

The pooled +0.15 95th demand percentiles are:

| Workload | V44 | V45 | V46 |
|---|---:|---:|---:|
| One candidate, 0.5 hours | 111 | 109 | 110 |
| One candidate, 1.0 hour | 222 | 217 | 220 |
| One candidate, adverse time | 172 | 168 | 170 |
| Three candidates, 0.5 hours | 173 | 169 | 170 |
| Three candidates, 1.0 hour | 346 | 338 | 341 |
| Three candidates, adverse time | 234 | 230 | 231 |

All entries are hours. The earlier “within eight hours” comparison concerns only these six V45 pooled percentiles relative to V44.

These pooled values cannot select the reserve. The rule uses the largest frame-specific percentile across retained workload profiles.

V46’s largest frame-specific 95th percentile at +0.15 is 383 hours across the tested workloads. This exceeds the approximately 256-hour maximum reachable reserve. Conservative defaults can therefore return the design to review.

Missing demand information uses the full relevant cap, not the passing 0.5-hour workload.

The proposal defines planning limits from the original development cases, including observed maxima, unfinished work at its allowance and conservative zero-information handling. They are not exact or simultaneous population confidence bounds for the corrected frame.

Retained planning profiles include three-candidate positive bundles, uniform and last-position confirmation, and a tail check for rejected candidates. Results for those selected profiles remain pending.

If the initial reserve is insufficient, the funding sequence is fixed:

1. Reduce seeded validation from 60 to 45 pairs.
2. Use month-10 analysis time only down to 30 hours.
3. Return to review if capacity remains insufficient.

The seed reduction frees

\[
30(0.15+1.0)+30(0.15+3/13)
\]

student hours, approximately 46 hours. It also requires revised validation precision. The 60-pair figures cannot be reused.

A demand percentile is only a reservation screen. The chosen reserve must still pass full inference validation under the actual bundle-admission rule and review capacity.

## Resource ledger after project grouping

The initial review ledger remains:

| Source | Hours per adjudicator |
|---|---:|
| Main | 89.0 |
| Development | 12.5 |
| Development audit-assisted | 1.5 |
| Gate and revision | 8.0 |
| Duplicate requests | 9.0 |
| Seeded artifacts | 60.0 |
| Controls | 14.0 |
| Main audit-assisted | 11.0 |
| Total | 205.0 |

Initial main student work remains about 920.2 hours within a 921-hour ceiling. Main work, seeds and duplicates total about 1,137.9 hours.

These are fixed allowances. The main preparation allowance now applies to a project unit, including every snapshot reached by its sampled functions. It is not multiplied by member audits.

The preparation budget retains 19 audit spot checks at 0.5 hours each. Its 100-hour exact-mapping allowance must cover the three development audits and all member audits of selected main units. The earlier per-audit expression is no longer presented as evidence that this work will fit.

A complete named mapping and environment plan is required before collection. Missing members cannot be dropped, assigned zero counts or called unconstructible merely to meet the budget.

Preparation retains its 112-hour ceiling within the 220-hour support budget. Natural investigation retains 120 auditor hours.

The funding sequence does not raise the 1,800-hour student ceiling. No source is assigned to extra project units.

## Final validation and current status

The final check uses the corrected project frame, recorded size measures, pooled function sampling, deletion of whole project units, the selected reserves and every retained workload profile.

It includes all ten conditions, all 76 ordered vectors under four implementation-level mechanisms, and all 64 package vectors.

Error and coverage are required outside the power region. Power is required only inside the retained symmetric region and separate package region. Calibration and fresh validation use the same scope and recomputed multiplicity counts.

The additional protocol-effect setting, strict-count interpretations, recall settings, construction settings, linked working status and low V yield remain required.

An unassessable warning does not itself stop launch. It also supplies no evidence of low demand. Conservative defaults can still make the resource rule fail.

The student commitment is signed. The timed case remains missing. Complete preparation capacity, selected-demand results, any reduced-seed precision calculation and final-frame validation remain pre-collection requirements. No new result is claimed for them.
