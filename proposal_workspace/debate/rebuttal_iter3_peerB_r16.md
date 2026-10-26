
# Rebuttal to the iteration-3 meta-review

Authors: Peer A and Peer B.

This response refers to proposal version 17.

We distinguish completed evidence, revised design rules and outstanding readiness requirements. We do not claim that every requirement has been completed.

## Proposed change in principal estimand

We request approval to make RQ1b principal and RQ1a secondary. This departs from the iteration-3 AC’s explicit resolution.

The principal estimand is the difference in detected vulnerability among working agent and historical implementations, standardized across the constructible strata. Functional failure and the joint endpoint D are reported separately.

The examined allocations do not support the earlier RQ1a precision promise. V27 gives a largest mean security-component half-width of 0.338 for the proposed allocation, and 0.422 under observed-fix-only V counts. We do not infer that every affordable design has been ruled out.

The proposed RQ1b target is +0.15 with at least 0.80 power for each configuration across retained readiness scenarios. Current simulations support investigating that target, not declaring it attained under the combined design.

The proposed contribution remains an empirical historical comparison in real Solidity using probability sampling, blind discovery and executable function attribution. It is not a claim that unconditional comparison or sampling weights are new.

## Structurally different changes

- The frame evidence now includes a random-order audit sample with all qualifying findings read, rather than only a distribution modeled from finding counts.
- Sampling in proportion to N counts is proposed because the audited N counts vary substantially.
- Exact conditional-security nulls and targets replace D-null calibration for the principal decision.
- A finite-population simulation now includes difficulty-dependent construction.
- Fixed campaign time limits replace expected candidate counts as the definition of reserved work.
- Conditional-rate bounds include uncertain working denominators.
- Audit-assisted secondary work has explicit sampling probabilities and a weighted increment estimator.

These changes do not yet constitute a validated combined design.

## Evidence and remaining limits

The random audit record contains 25 processed audits and 352 findings. It reports 62 V functions supported by observed fixes and 118 when clear recommendations are included. It records 3,621 N functions.

These counts need reconciliation with strict body-only eligibility, unique signatures and consistent treatment of unresolved findings. Recommendation-based counts are not proven upper bounds.

V24 validates exact security nulls and tests exact effects under the older modeled count distribution. V25 holds a synthetic finite frame fixed and includes difficulty-dependent construction. V27 uses audited count pairs and sampling in proportion to N, but assumes complete construction and resolved outcomes.

No supplied run combines all those features with the proposed finite sampling procedure and conditional-rate bounds.

## Responses to required changes

| Item | Status | Response | Proposal sections |
|---|---|---|---|
| 1. Allocation and budget | Revised design; human adequacy pending | The proposal keeps an explicit allocation menu and fixed resource ceilings. Candidate workload assumptions no longer define guaranteed confirmation capacity. Each implementation has a fixed campaign allowance, with count and time cuts recorded. Duplicate-request campaigns and coordination share an explicit inequality within the existing reserve. Paid reservations must cover all package sources. The earlier 877-hour middle calculation is retained as an assumption-based comparison, not proof of adequate reservations. | 5.2, 5.7, 8 |
| 2. Counted frame and readiness simulation | Substantial new evidence; partly complete | The audit sample processes 25 audits from a fixed random order, records eight replacements, and reads 352 findings. Counts are uncapped and paired with N counts. Observed fixes and recommendations are separated. V25 supplies a finite-population construction check; V26 and V27 use the audited count pairs. Final eligibility reconciliation and a combined finite-population validation remain outstanding. | 5.1, 6.3, 8 |
| 3. Security and functional-failure components | Revised | The proposal defines \(v_A-v_H\) as its conditional security component and reports the exact residual functional-failure component of D. It now supplies the weighted conditional-rate estimator, domain standardization, admissible \((W,D)\) bounds and undefined-denominator rule. It explicitly rejects a causal or paired-new-flaw interpretation. | 3, 6.2, 6.3 |
| 4. Checks endorsing a flaw | Revised | Blind primary confirmation can trigger author-blind removal of a check that asserts the forbidden outcome. The suite is then applied consistently before primary locking. Later audit-derived revisions affect a separately labeled secondary suite and cannot reopen primary labels. | 5.5, 5.8 |
| 5. “Little difference” and interpretation | Revised | “Little difference” is removed. RQ1a is secondary and reported with its full interval. The proposal gives scenario-specific security-component exclusion rates rather than a universal detectable-distortion threshold. A positive distortion claim requires positive-scenario validation. | 3, 6.4 |
| 6. RQ1b precision and calibration | Partly complete | V24 calibrates the security-component family decision on exact security nulls. Its selected level is 0.035. Without unresolved outcomes, exact +0.10 power is 0.51–0.78 and exact +0.15 power is 0.84–0.95. V27 reports +0.15 power of 0.86–0.98 for the proposed count-weighted allocation without construction losses or unresolved outcomes. The target is now +0.15. Combined validation remains required; no +0.10 power promise is made. | 6.3, 8 |
| 7. Retained scenarios | Revised rule; combined execution outstanding | The rule uses reconciled count scenarios, lower construction-yield limits without upward truncation, upper unresolved-outcome limits with a floor, actual denominators and dependence assumptions. One final decision procedure must pass across the retained scenarios. Failure prevents inferential launch. The nominal development count is explicitly a maximum. | 5.2, 6.3, 8 |
| 8. Recall-gap sensitivity | Revised | Sensitivity now uses detected rates among working implementations for the principal estimand. It defines both the standardized author difference and the conditional design difference with separate sensitivities by author and stratum. D sensitivity additionally includes working rates. The old −0.47 example is identified as a D quantity. | 6.5 |
| 9. Blind candidate rediscovery | Completed at the requested candidate level; interpretation corrected | The recorded matches are Claude 17 of 17 and Codex 13 of 17; excluding weak keys gives 14 of 14 and 13 of 14. Wilson intervals are labeled as independent-trial calculations, not cluster-adjusted population recall intervals. Candidate matches constrain confirmations from those lists, not recall of the future full campaign. The executable 63008 package supersedes the judge’s contrary H-02 dependency note. | 5.9, 5.11 |
| 10. Student commitment and timed case | Pending from the student | The student has committed to participate. The dated written commitment and complete timed case are not yet available. Both remain committee preconditions before resubmission. The full three-case record remains the launch requirement. The kit is not presented as measured human evidence. | 8, 10 |
| 11. Candidate cuts | Retained and extended | Count and time cuts are recorded by author and stratum. A secondary bound treats cut lists as unresolved. Missing required adjudication remains unresolved in the primary analysis. | 5.7, 6.2 |
| 12. Historical-body reproduction | Retained | The recall flag covers both distinctive fixes and reproduction of historical bodies. Its threshold is frozen before generation after development checking. Both principal and secondary comparisons receive flagged-case exclusion analyses. | 6.8 |
| 13. Duplicate requests | Revised | Both requests receive generation and discovery when evaluable. At most \(15\times5\) extra campaigns and coordination must fit the stated reserve inequality. Independent construction and adjudication are charged to explicit paid reservations. Failures remain recorded. | 5.4, 8 |
| 14. Simulation history | Retained and updated | Main sections distinguish V24, V25 and V27 because they establish different facts. Appendix A identifies their limits and superseded versions. V23’s rounded-key aggregation defect is acknowledged. | 6.3, Appendix A |
| 15. Factual answers | Updated, with unknowns retained | Appendix B replaces the old N-count assumption and empty-stratum approximation. It distinguishes known audit counts from final eligibility, and planned costs from funded resources. Named personnel, post-cutoff counts and verified audit-missed availability remain unknown where evidence is absent. | Appendix B |

## Responses to the reviewers’ disagreements

### 1. Novelty and contribution

The new principal question requires a revised contribution statement. We do not transfer the earlier RQ1a novelty judgment automatically.

The proposed contribution is a probability-defined historical comparison of detected security in working Solidity replacements, with functional failure, executable attribution and detection uncertainty exposed. The secondary design comparison still measures how a flagged-only view changes that result.

Acceptance should depend on whether that empirical contribution and its proposed precision are sufficient, not on a claim that probability weighting is novel.

### 2. Soundness

The revised estimator matches the conditional security component. Its bounds include uncertain working denominators. The decomposition is descriptive and does not compare a causal common set of successful implementations.

Functional-check changes are separated by whether they arise before blind primary locking or after audit access.

The remaining soundness requirement is validation of the combined sampling, construction and inference procedure.

### 3. Feasibility

The resource ceiling is now enforced through fixed reservations rather than expected candidate counts. This prevents workload from silently expanding.

It does not establish that valid work fits those reservations. Human timing and the resulting completion rates remain essential.

Peer-addressable frame and inference work also remains. We do not say that only the student’s timed case is missing.

### 4. Common construction allowance

V and N use the same fixed allowance. Different visible limits would reveal the stratum to blind staff.

Construction yield under that allowance enters readiness analysis. Shortening an allowance is not treated as evidence that the same domain remains constructible.

### 5. “Little difference”

The reading is removed. Broad intervals remain inconclusive.

RQ1a claims concern the conditional security component and its full uncertainty. D is displayed separately.

### 6. Principal estimand

We explicitly request a departure from the AC’s resolution: RQ1b principal, RQ1a secondary.

The evidence supports investigating a +0.15 RQ1b target under sampling in proportion to N counts. It does not establish high power at +0.10 or rule out every alternative RQ1a design.

If the committee rejects this change, a different reviewed design is required. The proposal does not silently retain the old contribution claim.

### 7. Unresolved outcomes

Bounds remain part of the principal analysis.

The revised bounds operate on feasible working-status and detected-vulnerability pairs. They do not assume the working denominator is known when it is not.

Adverse development limits are not truncated to favorable values. If retained scenarios fail, inferential collection does not launch.

### 8. Frame-based readiness

The random audit sample is new evidence, with explicit replacements and evidence classes. It is not yet the final eligible frame.

V25 demonstrates a finite-frame construction analysis. V27 demonstrates the effect of unequal protocol sizes under a different generator. Their results cannot be combined as though one run validated the final design.

Eligibility reconciliation and a combined validation are still required.

### 9. Human evidence before acceptance

The dated commitment and one complete student-timed case remain pending. The full three-case record remains a launch gate.

The student’s commitment is reported accurately, without treating an empty form or automated work as the required evidence.

## Current status

The revision resolves the endpoint definition, locking rules, secondary sampling rules and interpretation errors in the text. It also replaces the previous calibration claim with directly relevant security-component evidence.

Two peer-addressable Major concerns remain: reconciliation of the audited frame and validation of the combined inferential design. Item 10 remains separately pending from the student.

The proposal is not yet ready for confirmatory collection or for a claim that every iteration-3 requirement has been completed.

