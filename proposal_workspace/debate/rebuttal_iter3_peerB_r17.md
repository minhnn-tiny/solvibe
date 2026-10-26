
# Rebuttal to the iteration-3 meta-review

Authors: Peer A and Peer B.

This response refers to proposal version 18.

We distinguish completed evidence, revised design rules and outstanding readiness requirements. We do not claim that every requirement has been completed.

## Proposed change in principal estimand

We request approval to make RQ1b principal and RQ1a secondary. This departs from the iteration-3 AC’s explicit resolution.

The principal estimand is the difference in detected vulnerability among working agent and historical implementations, standardized across the constructible strata. Functional failure and the joint endpoint D are reported separately.

The examined allocations do not support the earlier RQ1a precision promise. V27 gives a largest mean security-component half-width of 0.338 for the proposed allocation, and 0.422 under observed-fix-only V counts. Those runs precede the strict recount and assume complete construction and resolved outcomes. We do not infer that every affordable design has been ruled out.

The proposed RQ1b target remains +0.15 with at least 0.80 power for each configuration across retained readiness scenarios. V28 does not establish that this target is attained. Some scenarios fall below it even without unresolved outcomes.

The proposed contribution remains an empirical historical comparison in real Solidity using probability sampling, blind discovery and executable function attribution. It is not a claim that unconditional comparison or sampling weights are new.

## Structurally different changes

- The frame evidence includes a random-order audit sample with all High and Medium findings read, followed by a strict recount of identities and correction scope.
- Sampling in proportion to N counts is proposed because the audited N counts vary substantially.
- Exact conditional-security nulls and targets replace D-null calibration for the principal decision.
- V28 combines a fixed finite population, difficulty-dependent construction, estimated constructible shares, uncertain working status and the family decision.
- Fixed campaign time limits replace expected candidate counts as the definition of reserved work.
- Conditional-rate bounds include uncertain working denominators.
- Audit-assisted secondary work has explicit sampling probabilities and a weighted increment estimator.

These changes do not yet constitute validation of the planned sampling and inference procedure. V28 samples protocols with replacement, whereas the proposal samples distinct protocols without replacement.

## Evidence and remaining limits

### Strict frame recount

The random audit record contains 25 processed audits and 352 High and Medium findings. The earlier counts were 62 observed-fix V functions, 118 when recommendations were included, and 3,621 N functions.

The strict recount in `evidence/frame_audit/strict/` replaces those planning counts:

| Strict count | Total | Mean per audit | Median | Audits with zero |
|---|---:|---:|---:|---:|
| V supported by observed fixes | 54 | 2.16 | 1 | 10 of 25 |
| V supported by observed fixes or admissible recommendations | 109 | 4.36 | 4 | 1 of 25 |
| Eligible N functions | 3,620 | 144.8 | 92 | 0 of 25 |

The recount separates 94 colliding names involving 198 functions. It uses full paths, enclosing contracts and parameter types. Strict V corrections cannot require new declarations or other changes outside the target body. N excludes functions linked to findings under the recount’s rules.

This resolves the earlier identity and body-only classification concerns at proposal stage. It does not make the record a final eligible census. The study’s severity rubric has not yet replaced the original High and Medium labels. The record also identifies findings outside functions, close calls, snapshot-provenance exceptions and readings without a second reader. These remain frame-freezing checks.

Recommendation-based counts are not proven upper bounds. Unresolved findings may contain additional eligible functions, and a recommendation may understate the correction actually required. The V28 file name “upper” identifies its recommendation-inclusive scenario, not a mathematical bound.

### Combined planning evidence

V24 validates exact security targets under the older count model. V25 supplies a fixed finite-population construction check. V27 examines unequal protocol sizes using the earlier audited count pairs.

V28 combines more of the required features. It uses strict count pairs resampled into a fixed frame of 200 protocols. Construction is decided once per function and can depend on difficulty. The conditional-security target is set exactly on the constructible frame. Both authors can have unresolved working and security outcomes. The decision uses the adverse identification bound and Holm across configurations.

The recorded results are:

| V count scenario | Selected Holm level | Worst validation family error at unresolved shares 0, 0.005 and 0.013 | Partial-null family error | Exact +0.15 power: minimum and median, no unresolved outcomes | Exact +0.15 power: minimum and median, unresolved share 0.013 |
|---|---:|---|---:|---|---|
| Observed fixes and admissible recommendations | 0.045 | 0.043, 0.048, 0.028 | 0.045 | 0.75, 0.90 | 0.60, 0.75 |
| Observed fixes only | 0.04 | 0.033, 0.030, 0.018 | 0.040 | 0.73, 0.89 | 0.62, 0.76 |

Power entries summarize the minimum configuration power in each frame. They are not probabilities that both configurations succeed. Medians summarize the selected scenarios; they do not estimate performance in a “typical” real population.

The validation error estimates are encouraging but have Monte Carlo uncertainty. Each condition uses 400 studies. The recorded point estimates do not prove exact family-wise control.

V28 uses with-replacement protocol draws, Hansen–Hurwitz weights and a delete-one-draw jackknife. It does not validate the proposal’s without-replacement design or coverage of its full identification-bound intervals. It selects separate levels for the two count scenarios. The final procedure must be calibrated across the scenarios retained for the actual design.

The power results also leave the stated readiness target unmet in some scenarios. No inferential launch is justified by these results alone.

## Responses to required changes

| Item | Status | Response | Proposal sections |
|---|---|---|---|
| 1. Allocation and budget | Revised design; adequacy remains open | The proposal keeps an explicit allocation menu and fixed resource ceilings. Candidate workload assumptions no longer define guaranteed confirmation capacity. Each implementation has a fixed campaign allowance, with count and time cuts recorded. Duplicate-request campaigns and coordination share an explicit inequality within the existing reserve. Paid reservations must cover all package sources. The earlier 877-hour middle calculation is an assumption-based comparison, not proof of adequate reservations. V28 does not establish that the preferred allocation meets its inference target. Human work must still establish that the allowances permit valid construction and review. | 5.2, 5.7, 6.3, 8 |
| 2. Counted frame and readiness simulation | Strict recount completed; actual-design validation outstanding | The audit sample processes 25 audits from a fixed random order, records eight replacements and reads 352 findings. The strict recount gives 54 observed-fix V functions, 109 including admissible recommendations and 3,620 N functions. It separates unique function identities and excludes corrections requiring changes outside the body. Severity harmonization and documented classification and provenance checks remain before frame freezing. V28 combines strict count pairs, a finite population, difficulty-dependent construction and unresolved outcomes, but uses with-replacement sampling rather than the planned without-replacement design. | 5.1, 6.3, 8 |
| 3. Security and functional-failure components | Revised | The proposal defines \(v_A-v_H\) as its conditional security component and reports the exact residual functional-failure component of D. It supplies the weighted conditional-rate estimator, domain standardization, admissible \((W,D)\) bounds and undefined-denominator rule. It explicitly rejects a causal or paired-new-flaw interpretation. | 3, 6.2, 6.3 |
| 4. Checks endorsing a flaw | Revised | Blind primary confirmation can trigger author-blind removal of a check that asserts the forbidden outcome. The suite is then applied consistently before primary locking. Later audit-derived revisions affect a separately labeled secondary suite and cannot reopen primary labels. | 5.5, 5.8 |
| 5. “Little difference” and interpretation | Revised | “Little difference” is removed. RQ1a is secondary and reported with its full interval. The proposal gives scenario-specific security-component exclusion rates rather than a universal detectable-distortion threshold. A positive distortion claim requires positive-scenario validation. | 3, 6.4 |
| 6. RQ1b precision and calibration | Partly complete; target not demonstrated | V28 tests exact constructible-domain security targets with strict audited count pairs, construction losses and unresolved working status. Its selected levels are 0.045 for recommendation-inclusive counts and 0.04 for observed-fix counts. At exactly +0.15, the minimum configuration power across scenarios is 0.75 and 0.73 without unresolved outcomes, and 0.60 and 0.62 at unresolved share 0.013. These results do not meet the proposed 0.80 requirement in every scenario. The actual sampling design, full-interval coverage and one procedure across retained scenarios still require validation. No +0.10 power promise is made. | 6.3, 8 |
| 7. Retained scenarios | Rule specified; full execution outstanding | The rule uses reconciled count scenarios, lower construction-yield limits without upward truncation, upper unresolved-outcome limits with a floor, actual denominators and dependence assumptions. One final decision procedure must pass across the retained scenarios. V28 covers only part of that set and uses a different sampling procedure. Failure prevents inferential launch. The nominal development count is explicitly a maximum. | 5.2, 6.3, 8 |
| 8. Recall-gap sensitivity | Revised | Sensitivity uses detected rates among working implementations for the principal estimand. It defines both the standardized author difference and the conditional design difference with separate sensitivities by author and stratum. D sensitivity additionally includes working rates. The old −0.47 example is identified as a D quantity. | 6.5 |
| 9. Blind candidate rediscovery | Completed at the requested candidate level; interpretation corrected | The recorded matches are Claude 17 of 17 and Codex 13 of 17; excluding weak keys gives 14 of 14 and 13 of 14. Wilson intervals are labeled as independent-trial calculations, not cluster-adjusted population recall intervals. Candidate matches constrain confirmations from those lists, not recall of the future full campaign. The executable 63008 package supersedes the judge’s contrary H-02 dependency note. | 5.9, 5.11 |
| 10. Student commitment and timed case | Pending from the student | The student has committed to participate. The dated written commitment and complete timed case are not yet available. Both remain committee preconditions before resubmission. The full three-case record remains the launch requirement. The kit is not presented as measured human evidence. | 8, 10 |
| 11. Candidate cuts | Retained and extended | Count and time cuts are recorded by author and stratum. A secondary bound treats cut lists as unresolved. Missing required adjudication remains unresolved in the primary analysis. | 5.7, 6.2 |
| 12. Historical-body reproduction | Retained | The recall flag covers both distinctive fixes and reproduction of historical bodies. Its threshold is frozen before generation after development checking. Both principal and secondary comparisons receive flagged-case exclusion analyses. | 6.8 |
| 13. Duplicate requests | Revised | Both requests receive generation and discovery when evaluable. At most \(15\times5\) extra campaigns and coordination must fit the stated reserve inequality. Independent construction and adjudication are charged to explicit paid reservations. Failures remain recorded. | 5.4, 8 |
| 14. Simulation history | Updated evidence; presentation cleanup remains | Section 6.3 distinguishes the separate V24, V25 and V27 checks from V28’s combined planning check. V28 does not validate the final without-replacement procedure. Appendix A still ends at V27 and needs a V28 entry and an updated status summary. V23’s rounded-key aggregation defect remains acknowledged. | 6.3, Appendix A |
| 15. Factual answers | Updated, with unknowns retained | Section 5.1 now gives strict identities and revised counts. Appendix B distinguishes parser-based eligibility from the final frame and planned costs from funded resources. Named personnel, post-cutoff counts and verified audit-missed availability remain unknown where evidence is absent. The section 8 status list needs to distinguish completed strict reconciliation from the remaining frame-freezing checks. | 5.1, 8, Appendix B |

## Responses to the reviewers’ disagreements

### 1. Novelty and contribution

The new principal question requires a revised contribution statement. We do not transfer the earlier RQ1a novelty judgment automatically.

The proposed contribution is a probability-defined historical comparison of detected security in working Solidity replacements, with functional failure, executable attribution and detection uncertainty exposed. The secondary design comparison still measures how a flagged-only view changes that result.

Acceptance should depend on whether that empirical contribution and its proposed precision are sufficient, not on a claim that probability weighting is novel.

### 2. Soundness

The revised estimator matches the conditional security component. Its bounds include uncertain working denominators. The decomposition is descriptive and does not compare a causal common set of successful implementations.

Functional-check changes are separated by whether they arise before blind primary locking or after audit access.

V28 is a relevant combined check, but it evaluates a different sampling procedure. Validation of the planned sampling weights, uncertainty procedure, full intervals and family decision remains outstanding.

### 3. Feasibility

The resource ceiling is enforced through fixed reservations rather than expected candidate counts. This prevents workload from silently expanding.

It does not establish that valid work fits those reservations. Human timing and the resulting completion rates remain essential.

There is also a peer-addressable inference problem. V28 falls below the proposal’s power requirement in several scenarios. We do not say that only the student’s timed case is missing.

### 4. Common construction allowance

V and N use the same fixed allowance. Different visible limits would reveal the stratum to blind staff.

Construction yield under that allowance enters readiness analysis. Shortening an allowance is not treated as evidence that the same domain remains constructible.

V28 assigns construction once per function and allows it to depend on difficulty. This is an improvement over treating construction as independent attrition.

### 5. “Little difference”

The reading is removed. Broad intervals remain inconclusive.

RQ1a claims concern the conditional security component and its full uncertainty. D is displayed separately.

### 6. Principal estimand

We explicitly request a departure from the AC’s resolution: RQ1b principal, RQ1a secondary.

Earlier planning results motivated investigating a +0.15 RQ1b target under sampling in proportion to N counts. The combined V28 results now show that the selected allocation does not achieve the proposed 0.80 power requirement in every tested scenario.

The proposal therefore cannot present that target as established. It needs a supported design or an explicitly revised requirement for committee approval. It does not establish high power at +0.10 or rule out every alternative RQ1a design.

If the committee rejects the principal-estimand change, a different reviewed design is required.

### 7. Unresolved outcomes

Bounds remain part of the principal analysis.

The bounds operate on feasible working-status and detected-vulnerability pairs. They do not assume the working denominator is known when it is not.

V28 implements unresolved outcomes for both authors. Its unresolved share of 0.013 reduces the lowest recorded +0.15 power to 0.60 or 0.62, depending on the count scenario.

Adverse development limits are not truncated to favorable values. If retained scenarios fail, inferential collection does not launch.

### 8. Frame-based readiness

The strict recount resolves the earlier function-identity and body-only correction concerns at proposal stage. Its records preserve observed fixes, recommendations and unresolved classifications.

The counts still require the stated severity and provenance checks before they become the frozen study frame.

V28 uses these strict count pairs in a fixed synthetic population and combines construction and unresolved outcomes. However, the population is resampled from 25 audited pairs, and protocol sampling is with replacement. These assumptions are explicit planning simplifications, not validation of the planned without-replacement design.

### 9. Human evidence before acceptance

The dated commitment and one complete student-timed case remain pending. The full three-case record remains a launch gate.

The student’s commitment is reported accurately, without treating an empty form or automated work as the required evidence.

Those measurements must inform the construction allowance, review reservations, completion rates and readiness scenarios. They do not replace the peer-addressable inference validation.

## Current status

The strict recount resolves the earlier identity and correction-scope concern at proposal stage. V28 substantially improves the planning evidence by combining features previously examined separately.

Two Major concerns remain. First, the combined check does not validate the planned without-replacement inference or full-interval coverage. Second, its power results do not establish that the selected allocation meets the proposal’s readiness requirement.

The proposal also needs a minor update to its evidence-status summaries and simulation appendix. Item 10 remains separately pending from the student.

The proposal is not ready for confirmatory collection or for a claim that every iteration-3 requirement has been completed.

