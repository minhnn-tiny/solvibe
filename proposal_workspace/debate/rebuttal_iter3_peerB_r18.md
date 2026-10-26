# Rebuttal to the iteration-3 meta-review

Authors: Peer A and Peer B.

This response refers to proposal version 19.

We distinguish completed evidence, revised design rules and outstanding readiness requirements. We do not claim that every requirement has been completed.

## Proposed changes in principal estimand and power requirement

We request approval to make RQ1b principal and RQ1a secondary. This departs from the iteration-3 AC’s explicit resolution.

The principal estimand is the difference in detected vulnerability among working agent and historical implementations, standardized across the constructible strata. Functional failure and the joint endpoint D are reported separately.

The examined allocations do not support the earlier RQ1a precision promise. V27 gives a largest mean security-component half-width of 0.338 for the proposed allocation, and 0.422 under observed-fix-only V counts. Those runs precede the strict recount and assume complete construction and resolved outcomes. We do not infer that every affordable design has been ruled out.

We also request approval to reduce the RQ1b power requirement. The earlier requirement was at least 0.80 correct directional power for each configuration at exactly +0.15 in every retained scenario. V29 does not meet it.

The proposed replacement is at least 0.60 at that same effect in every retained scenario. Final validation must establish this with a lower Monte Carlo confidence bound. This is a substantive reduction in ambition, chosen after the planning evidence. It is not presented as equivalent to the earlier requirement.

The study may miss a large difference. Null results with broad intervals remain inconclusive. The proposed contribution must be judged with that limitation.

The new requirement is not yet demonstrated. A valid calibration may reduce power below the recorded V29 values. Committee approval of the changed requirement would not waive validation.

The proposed contribution remains an empirical historical comparison in real Solidity using probability sampling, blind discovery and executable function attribution. It is not a claim that unconditional comparison or sampling weights are new.

## Structurally different changes

- The frame evidence includes a random-order audit sample with all High and Medium findings read, followed by a strict recount of identities and correction scope.
- Sampling in proportion to N counts addresses the large differences in protocol size.
- Exact conditional-security nulls and targets replace D-null calibration for the principal decision.
- V29 combines the strict counts, a fixed finite population, difficulty-dependent construction, estimated constructible shares and uncertain working status.
- V29 now uses the planned randomized systematic sampling of distinct protocols.
- Fixed campaign time limits replace expected candidate counts as the definition of reserved work.
- Conditional-rate bounds include uncertain working denominators.
- Audit-assisted secondary work has explicit sampling probabilities and a weighted increment estimator.

The sampling mismatch raised in round 17 is fixed. The final inference settings have not passed validation.

## Evidence and remaining limits

### Strict frame recount

The random audit record contains 25 processed audits and 352 High and Medium findings. Its initial counts were 62 observed-fix V functions, 118 when recommendations were included, and 3,621 N functions.

The strict recount replaces those planning counts:

| Strict count | Total | Mean per audit | Median | Audits with zero |
|---|---:|---:|---:|---:|
| V supported by observed fixes | 54 | 2.16 | 1 | 10 of 25 |
| V supported by observed fixes or admissible recommendations | 109 | 4.36 | 4 | 1 of 25 |
| Eligible N functions | 3,620 | 144.8 | 92 | 0 of 25 |

The recount separates 94 colliding names involving 198 functions. It uses full paths, enclosing contracts and parameter types. Strict V corrections cannot require new declarations or other changes outside the target body.

This resolves the earlier identity and body-only classification concern at proposal stage. It does not make the record a final eligible census. Severity harmonization, close calls and provenance exceptions remain frame-freezing checks.

Recommendation-based counts are not proven upper bounds. The simulation label “upper” identifies recommendation-inclusive counts only.

### V29 combined planning evidence

V29 uses 24 fixed simulated frames covering both strict count lists. Each frame contains 200 protocols. It samples 20 distinct protocols with inclusion probabilities proportional to N, capped at one. It uses inverse-inclusion weights and a delete-one-protocol jackknife.

Construction is decided once per function and can depend on difficulty. The conditional-security target is set exactly on the constructible frame. Both authors can have unresolved working and security outcomes. The decision uses the adverse bound and Holm across configurations.

One Holm level and one interval multiplier are selected across both count lists. The recorded settings are 0.045 and 1.1.

| Validation condition | Worst family-wise error | Lowest marginal coverage |
|---|---|---|
| Exact null, no unresolved outcomes | 0.062 ± 0.024 | 0.940 ± 0.023 |
| Exact null, unresolved share 0.005 in both authors | 0.030 ± 0.017 | 0.963 ± 0.019 |
| Exact null, unresolved share 0.013 in both authors | 0.022 ± 0.015 | 0.978 ± 0.015 |
| Exact null, agent share 0.013 and historical share 0 | 0.037 ± 0.019 | 0.963 ± 0.019 |
| Exact null, agent share 0 and historical share 0.013 | 0.040 ± 0.019 | 0.963 ± 0.019 |
| Partial null: 0 and +0.10, no unresolved outcomes | 0.048 ± 0.021 | 0.945 ± 0.022 |

The code checks whether the interval extending both estimated bounds contains the true contrast. It reports the lower marginal coverage across configurations. This is not simultaneous coverage across configurations or coverage of both population identification-bound endpoints.

The reported undefined-estimate share is 0.000 throughout. Final validation must also report unconditional coverage and retain undefined studies as failures to supply an interval.

| Exact difference | Unresolved shares: agents, historical | Lowest correct directional power |
|---|---|---|
| +0.10 | 0, 0 | 0.41 ± 0.05 |
| +0.10 | 0.013, 0.013 | 0.27 ± 0.04 |
| +0.15 | 0, 0 | 0.74 ± 0.04 |
| +0.15 | 0.013, 0.013 | 0.63 ± 0.05 |
| +0.15 | 0.013, 0 | 0.75 ± 0.04 |
| +0.15 | 0, 0.013 | 0.63 ± 0.05 |
| −0.05, feasible frames only | 0, 0 | 0.18 ± 0.04 |

The negative target is infeasible in 16 of 24 frames under the generating constraints. Its result is limited to the remaining frames.

Each condition uses 400 studies. The displayed Monte Carlo half-widths are approximate and do not account for selecting extrema across frames. They cannot establish compliance merely because a target lies inside the interval.

The exact-null error of 0.062 exceeds 0.05. Coverage falls below 0.95 in several conditions. We therefore do not declare calibration successful.

Section 6.3 requires larger calibration and fresh validation. Selection must use uncertainty bounds across the retained checks. No candidate that fails may be replaced automatically by a grid endpoint. Power must be recomputed for the accepted procedure.

## Responses to required changes

| Item | Status | Response | Proposal sections |
|---|---|---|---|
| 1. Allocation and budget | Revised design; human and inferential adequacy pending | The proposal retains a bounded allocation menu and fixed resource ceilings. Each implementation has a fixed campaign allowance. Duplicate campaigns and coordination share an explicit reserve inequality. Paid reservations cover all package sources. The earlier 877-hour calculation is an assumption-based comparison, not proof of adequate capacity. The preferred allocation has V29 evidence, but its final inference settings and revised power requirement have not passed. | 5.2, 5.7, 6.3, 8 |
| 2. Counted frame and readiness simulation | Strict recount and combined simulation completed; validation remains open | The audit processes 25 audits from a fixed random order, records eight replacements and reads 352 findings. Strict counts are 54 observed-fix V functions, 109 including admissible recommendations and 3,620 N functions. Unique identities and body-only corrections are reconciled. V29 now combines these counts with finite-population construction, unresolved outcomes and the planned without-replacement sampling design. Severity and provenance checks remain before frame freezing. The inference procedure has not passed calibration and validation. | 5.1, 5.2, 6.3, 8 |
| 3. Security and functional-failure components | Revised | The proposal defines \(v_A-v_H\) as its conditional security component and reports the residual functional-failure component of D. It supplies the weighted conditional-rate estimator, domain standardization, admissible \((W,D)\) bounds and undefined-denominator rule. It rejects causal and paired-new-flaw interpretations. | 3, 6.2, 6.3 |
| 4. Checks endorsing a flaw | Revised | Blind primary confirmation can trigger author-blind removal of a check asserting the forbidden outcome. The suite is applied consistently before primary locking. Later audit-derived revisions define a separate secondary suite and cannot reopen primary labels. | 5.5, 5.8 |
| 5. “Little difference” and interpretation | Revised | “Little difference” is removed. RQ1a is secondary and reported with a full interval. Positive distortion claims require positive-scenario validation. V29’s RQ1b multiplier is not transferred to RQ1a without checking coverage. | 3, 6.4 |
| 6. RQ1b precision and calibration | Requirement changed for approval; validation incomplete | We withdraw the unsupported 0.80 requirement and propose at least 0.60 correct directional power at exactly +0.15 in every retained scenario, established by a lower Monte Carlo bound. V29’s recorded minimum powers are 0.74 without unresolved outcomes and 0.63 with unresolved share 0.013 in both authors. Its level 0.045 and multiplier 1.1 are provisional because validation error reaches 0.062 and coverage falls to 0.940. Valid recalibration may reduce power. No +0.10 power promise is made. | 3, 6.3, 8 |
| 7. Retained scenarios | Rule specified; final execution outstanding | The rule retains count uncertainty, lower construction-yield limits without upward truncation, upper unresolved-outcome limits with a floor, actual denominators and dependence assumptions. One procedure must pass across retained scenarios. V29 covers many of these features but not the final frame or all development-supported departures. Failure prevents inferential launch. | 5.2, 6.3, 8 |
| 8. Recall-gap sensitivity | Revised | Sensitivity uses detected rates among working implementations. It covers both the standardized author difference and the conditional design difference, with separate sensitivities by author and stratum. D sensitivity also includes working rates. The old −0.47 example is identified as a D quantity. | 6.5 |
| 9. Blind candidate rediscovery | Completed at the requested candidate level; interpretation limited | Recorded matches are Claude 17 of 17 and Codex 13 of 17; excluding weak keys gives 14 of 14 and 13 of 14. Wilson intervals are independent-trial calculations, not cluster-adjusted population recall intervals. Candidate matches concern those lists, not the future full campaign. The executable 63008 package supersedes the judge’s contrary H-02 dependency note. | 5.9, 5.11 |
| 10. Student commitment and timed case | Pending from the student | The student has committed to participate. The dated written commitment and complete timed case remain unavailable. Both are committee preconditions before resubmission. The full three-case record remains a launch requirement. The kit and automated timings are not presented as human evidence. | 8, 10 |
| 11. Candidate cuts | Retained and extended | Count and time cuts are recorded by author and stratum. A secondary bound treats cut lists as unresolved. Missing required adjudication remains unresolved in the primary analysis. | 5.7, 6.2 |
| 12. Historical-body reproduction | Retained | The recall flag covers distinctive fixes and reproduction of historical bodies. Its threshold is frozen before generation after development checking. Both comparisons receive flagged-case exclusion analyses. | 6.8 |
| 13. Duplicate requests | Revised | Both requests receive generation and discovery when evaluable. At most \(15\times5\) extra campaigns and coordination must fit the reserve inequality. Independent construction and adjudication use explicit paid reservations. Failures remain recorded. | 5.4, 8 |
| 14. Simulation history | Updated | Section 6.3 now presents V29 as the current main evidence. Appendix A distinguishes earlier checks, V28’s sampling mismatch and V29’s remaining calibration limits. V23’s aggregation defect remains acknowledged. The main allocation table does not pair older favorable power with the combined design as though readiness had been shown. | 6.3, 8, Appendix A |
| 15. Factual answers | Updated, with unknowns retained | Appendix B records strict counts and identities, the remaining eligibility checks, V29’s reported undefined share and the limits of that result. Named personnel, post-cutoff counts, compute cost and verified audit-missed availability remain unknown where evidence is absent. Section 8 no longer lists completed strict reconciliation as an outstanding Major task. | 5.1, 8, Appendix B |

## Responses to the reviewers’ disagreements

### 1. Novelty and contribution

The proposed principal question requires a revised contribution statement. We do not transfer the earlier RQ1a novelty judgment automatically.

The contribution is a probability-defined historical comparison of detected security in working Solidity replacements. It exposes functional failure, executable attribution and detection uncertainty. The secondary comparison measures how a flagged-only view changes the result.

The reduced power requirement weakens the empirical promise. The committee should judge whether the bounded study remains worthwhile. We do not present probability weighting itself as novel.

### 2. Soundness

The estimator matches the conditional security component. Its bounds include uncertain working denominators. The decomposition is descriptive and does not compare a causal common set of successful implementations.

Functional-check changes are separated by whether they occur before blind primary locking or after audit access.

V29 now uses the planned sampling design. This resolves the earlier procedural mismatch. It does not establish valid error control from the recorded settings. The proposal treats those settings as provisional and specifies a fresh validation requirement.

### 3. Feasibility

Fixed reservations prevent workload from silently expanding. They do not establish that valid work fits those reservations.

Human timing and completion rates remain essential.

A peer-addressable inference concern also remains. Error and coverage validation have not passed, and the power under a valid final procedure is unknown. We do not say that only the student’s timed case is missing.

### 4. Common construction allowance

V and N use the same fixed allowance. Different visible limits would reveal the stratum to blind staff.

Construction yield under that allowance enters readiness analysis. Shortening the allowance does not show that the same domain remains constructible.

V29 assigns construction once per function and allows it to depend on difficulty. The final analysis must still use development-supported stratum-specific yield limits.

### 5. “Little difference”

The reading is removed. Broad intervals remain inconclusive.

RQ1a concerns the conditional security component and its full uncertainty. D is displayed separately. A reduction in the power requirement does not justify a stronger interpretation of a null result.

### 6. Principal estimand

We request a departure from the AC’s resolution: RQ1b principal and RQ1a secondary.

We also request a reduced minimum power requirement of 0.60 at +0.15. Both changes need committee approval.

The evidence does not establish that the original 0.80 requirement is met, nor that every alternative RQ1a design is unaffordable. It also does not establish the revised requirement under a final validated family procedure.

If the committee rejects either proposed change, a different reviewed design is required before collection.

### 7. Unresolved outcomes

Bounds remain in the principal analysis. They operate on feasible working-status and detected-vulnerability pairs.

V29 models unresolved status for both authors and includes asymmetric rates. Its lowest recorded +0.15 power is 0.63 when both authors have unresolved share 0.013, and also when only historical outcomes have that share.

The readiness rule retains adverse development limits. It does not lower them to preserve power. If the approved requirement fails, inferential collection does not launch.

### 8. Frame-based readiness

The strict recount resolves the earlier identity and body-only correction concern at proposal stage. Severity and provenance checks remain before the final frame is frozen.

V29 uses strict count pairs in fixed simulated finite populations and selects distinct protocols using the planned procedure. This is stronger evidence than combining conclusions from separate simulations.

Its frames remain resampled from 25 audits. Historical working status, outcome-dependent missingness and the final development scenarios are not fully represented. These limits remain explicit.

### 9. Human evidence before acceptance

The dated commitment and one complete student-timed case remain pending. The full three-case record remains a launch gate.

The measurements must inform construction allowances, review reservations, completion rates and readiness scenarios. Automated work and empty forms are not substitutes.

Human measurements do not replace the separate requirement for valid inferential calibration.

## Current status

The strict frame reconciliation is complete at proposal stage. V29 resolves the combined simulation’s sampling mismatch and supplies directly relevant validation results.

Those results do not pass the stated error and coverage requirements. The proposal therefore retains one peer-addressable Major concern: final inferential calibration and validation, including power under the accepted procedure.

The revised power requirement and principal estimand require committee approval. Item 10 remains separately pending from the student.

The proposal is not ready for confirmatory collection and does not claim that every iteration-3 requirement has been completed.
