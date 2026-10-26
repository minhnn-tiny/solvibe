# Rebuttal to the iteration-3 meta-review

Authors: Peer A and Peer B.

This response refers to proposal version 22.

We distinguish completed evidence, revised design rules and remaining preconditions. We do not claim that every required change has been completed.

## Requested changes to the committee’s decisions

We request approval for RQ1b as principal and RQ1a as secondary. This departs from the iteration-3 AC’s resolution.

The principal estimand is detected vulnerability among working agent implementations minus that among working historical implementations, standardized across the constructible strata. Functional failure and D remain separate reported quantities.

V27’s half-widths of 0.338 and 0.422 concern the earlier 20-protocol allocation, not the proposed 22-protocol allocation. They do not support the old RQ1a precision promise. We do not claim that every affordable alternative has been ruled out.

We retain the request for a minimum power of 0.60 at +0.15 within a validated operating region. This is lower than the earlier 0.80 requirement and needs committee approval.

We now request a further departure. Development will no longer supply a pooled confidence limit intended to certify low unresolved rates. Instead, launch requires a validated author-specific operating region, a feasible procedure and explicit acceptance of conditional power. Monitoring occurs during the fixed main sample.

Adverse bounds remain in the principal analysis. We are not adopting a primary missing-at-random analysis or moving bounds to a sensitivity analysis.

The reason for the change is that development has few historical implementations and shared protocol environments. Repeated agent attempts do not remove that uncertainty. The former pooled limit and adaptive extension were unsound.

The proposal cannot guarantee before collection that the main study will remain within the operating region. If the committee requires that guarantee, this revision does not meet it.

## New evidence

V33 validates the stated planning procedure on its independent-missingness scenarios. For 22 protocols with one V and six N functions, it selects Holm level 0.03 and interval multiplier 1.175.

Its error upper bound is 0.0386 over 216 null checks. Its marginal-coverage lower bound is 0.9581 over 1,008 checks.

The lowest +0.15 power bounds are 0.721 with no unresolved outcomes, 0.658 at 0.0075 in both authors, and 0.583 at 0.013 in both authors.

V34 keeps that procedure fixed and raises historical unresolved rates.

| Unresolved share: agents, historical | Lowest +0.15 power | Lower bound |
|---|---:|---:|
| 0, 0.02 | 0.595 | 0.555 |
| 0, 0.03 | 0.493 | 0.454 |
| 0, 0.065 | 0.222 | 0.190 |
| 0.0075, 0.02 | 0.563 | 0.523 |
| 0.0075, 0.065 | 0.210 | 0.179 |

The V34 power bounds adjust over 240 checks. Its error and coverage summaries are point estimates, not a new confidence-bound validation.

V34 confirms that historical missingness cannot be represented by a much smaller limit pooled with agent outcomes.

V35 separates both agent configurations and historical code. It includes independent, task-shared, protocol-shared and difficulty-dependent unresolved outcomes. With the frozen V33 procedure, error and coverage pass at every tested rate vector under every mechanism (worst error upper bound 0.0405; worst coverage lower bound 0.9573). The power requirement holds in a frozen region: historical rate at most 0.005 with each configuration at most 0.013, or historical at most 0.0075 with the configurations at most 0.0075 and 0.013. Every vector with a historical rate of 0.02 or more fails power.

## Structurally different response to the repeated readiness failure

The following rules replace the previous development-rate gate:

- Development consists of three fixed cases using the main task allocation and attempt count.
- Development tests the method and resource limits, not rare population failure rates.
- No zero-unresolved requirement remains.
- No sample extension is triggered by an unresolved outcome.
- Main sampling is fixed before evaluation.
- Unresolved rates are monitored separately by author and stratum.
- Monitoring cannot replace tasks, add attempts or change the primary analysis.
- Adverse bounds remain primary regardless of the monitoring result.
- Evidence of leaving the region is judged by one preregistered rule (V36): a protocol-level 95% lower confidence limit for each author's rate, compared with the region. In development the rule stops launch; in the main study it withdraws the planned power statement. It rarely fires by mistake (at most 6.7% of simulated main studies inside the region) but is weak: it detects a historical rate of 0.065 in the main study in 96% to 97% of studies when failures are independent and in 5% to 17% when they cluster by protocol.
- Each source of unresolved outcomes has one closing rule, applied to both authors. Adjudicator disagreement after one comparison of reasons means the confirmation standard is not met; a secondary bound treats those packages as unresolved.
- A departure outside the validated error-control domain prevents a validated directional claim.

This changes what readiness establishes. It does not disguise an unverified low failure rate as measured evidence.

## Responses to required changes

| Item | Status | Response | Proposal sections |
|---|---|---|---|
| 1. Allocation and budget | Revised; human adequacy pending | The preferred main allocation remains 22 protocols with one V and six N functions. Its middle planning cost is 880 hours. The student campaign cap is 0.328 hours, including confirmation. Development now uses the same allocation and attempts, with one stage-capped schedule. Paid work uses fixed source reservations within the existing ceilings. These are enforceable caps, not measured proof of adequate time. | 5.2, 5.7, 8 |
| 2. Counted frame and readiness simulation | Frame reconciliation complete at proposal stage; robustness validation complete for the planning model (V35) | Strict counts are 54 observed-fix V functions, 109 including admissible recommendations and 3,620 N functions. Identities and body-only scope are reconciled. Severity and provenance checks remain before freezing the frame. V33 combines the main design features. The next check separates authors and includes shared and selective unresolved outcomes. | 5.1, 6.3 |
| 3. Security and functional failure | Retained | The conditional security component, D decomposition, weighted estimator, admissible outcome sets and undefined-denominator rule remain explicit. No causal or paired-new-flaw interpretation is claimed. | 3, 6.2, 6.3 |
| 4. Checks endorsing flaws | Retained | Blind-process check revisions occur before locking and apply consistently to all implementations. Audit-derived revisions remain secondary and cannot reopen primary labels. | 5.5 |
| 5. “Little difference” | Retained | The reading remains removed. RQ1a is secondary and may be inconclusive. V35 gives it a mean half-width up to 0.71 under the new allocation; it is descriptive only. | 6.4 |
| 6. RQ1b precision | Lower requirement requested; author-specific region validated (V35) | The request remains 0.60 power at +0.15 within a validated operating region. V34 shows that higher historical missingness can violate it. No pooled development limit is used to declare that region satisfied. | 3, 6.3 |
| 7. Retained scenarios | Explicit departure requested | The development confidence-limit rule is withdrawn. Separate configuration and historical rates, shared failures and difficulty dependence define planning scenarios. The largest passing regions on the tested grid will be reported before collection. Main monitoring does not select the analysis or sample. | 6.3, 8 |
| 8. Recall sensitivity | Retained | Both the author comparison and design difference use separate sensitivity assumptions by author and stratum. D sensitivity also includes working rates. Validation populations are not treated as interchangeable. | 6.5 |
| 9. Blind candidate rediscovery | Completed at candidate level | Claude matches 17 of 17 and Codex 13 of 17; excluding weak keys gives 14 of 14 and 13 of 14. Independent-trial intervals are not population recall guarantees. The executable 63008 package governs the H-02 causal claim. | 5.9, 5.11 |
| 10. Student commitment and timing | Pending from the student | The dated commitment and complete student-timed case remain preconditions before resubmission. The full three-case record remains a launch requirement. Automated timings do not substitute for human work. | 8, 10 |
| 11. Candidate cuts | Retained | Cut lists are recorded by author and stratum and receive a secondary unresolved bound. Missing required evaluation or adjudication remains unresolved in the primary analysis. | 5.7, 6.2 |
| 12. Historical reproduction | Retained | The recall flag covers distinctive fixes and reproduction of historical bodies. Thresholds are frozen before generation. Exclusion analyses remain secondary. | 6.8 |
| 13. Duplicate requests | Retained | Both evaluable requests receive generation and discovery. Added campaigns and coordination share the existing reserve. Construction and review enter paid ledgers. | 5.4, 8 |
| 14. Simulation history | Updated | Appendix A distinguishes V33’s planning validation from V34’s historical-missingness stress test , V35's author-specific robustness check and V36's rule for leaving the region. The zero-detection adjustment is no longer called exact. The undefined diagnostic must include the widening terms. | 6.3, Appendix A |
| 15. Factual answers | Updated | Appendix B records the new fixed development design, removal of the zero-unresolved rule, the frozen operating limits and remaining unknowns. V27 results are correctly labeled as earlier-allocation evidence. | 6.4, Appendix B |

## Responses to the reviewers’ disagreements

### 1. Novelty and contribution

The contribution is an empirical historical comparison with probability sampling, executable attribution and explicit detection limits. Probability weighting itself is not claimed as novel.

The principal-estimand change and reduced power weaken the original promise. Their adequacy remains a committee decision.

### 2. Soundness

The estimator and adverse bounds remain aligned with the conditional security component.

The zero-detection term is now described as a binomial-based widening adjustment. It is not an exact confidence bound for weighted, clustered observations.

V33 supports its tested model. V35 supports the author-specific and shared-failure scenarios on its grid. The final analysis does not depend on the V36 rule.

### 3. Feasibility

The development kit now has one schedule consistent with the proposal. Per-candidate time cannot be added outside the campaign cap. Audit-assisted work covers at most one V task per case.

Human adequacy remains unmeasured. If the fixed caps cannot support valid work, development fails the operational requirement.

The main plan remains bounded. It accepts a risk of inconclusive results if unresolved outcomes exceed the validated operating region. It does not claim that development eliminates that risk.

### 4. Common construction allowance

V and N retain the same visible allowance. Different limits could reveal stratum labels.

Construction failure remains a pre-evaluation decision. Shared budget exhaustion or missing staff cannot redefine a function as unconstructible.

### 5. “Little difference”

No such reading is restored. Broad intervals remain inconclusive. The operating-region proposal does not strengthen interpretation of a null result.

### 6. Principal estimand

We continue to request RQ1b as principal and RQ1a as secondary.

The earlier RQ1a precision results belong to older allocations. Under the proposed allocation, V35 gives RQ1a a mean half-width up to 0.71 and coverage down to 0.933 with the uncalibrated multiplier. RQ1a is reported as a descriptive estimate only.

If the committee rejects this change, a different reviewed design is required.

### 7. Unresolved outcomes

Adverse bounds remain primary, as the AC required.

We request a departure only from the rule that development confidence limits determine unresolved-rate scenarios. The former pooling rule did not bound historical missingness. Repeated agent outcomes did not provide independent evidence about protocol failures. The optional extension after a failure also changed the confidence procedure.

The replacement is a fixed-sample study with author-specific operating limits and monitoring. Those limits describe conditional performance. They are not certified probabilities for the real study.

### 8. Frame-based readiness

Strict reconciliation is completed at proposal stage. Final severity and provenance checks remain.

The next simulation preserves the finite frame, sampling weights, dependent construction and adverse bounds. It adds separate agent rates and shared failure mechanisms.

V35 defines a tested operating region, not a universal guarantee over every missingness mechanism.

### 9. Human evidence before acceptance

The dated commitment and first complete timed case remain pending. The complete three-case record remains required before launch.

The cases must test the actual stage caps and blindness rules. Deviations cannot be counted as successful demonstrations. No additional cases are triggered merely to obtain a favorable unresolved count.

## Current status

This revision removes the unsound pooled limit, the false precision from repeated attempts and the optional extension after a failure. It aligns the development schedule with the main procedure.

It retains adverse bounds and requests an explicit change in what readiness establishes.

V35 and V36 now supply the author-specific operating region and the rule for evidence of leaving it, on their tested grid and mechanisms.

Committee approval is required for the principal estimand, reduced power requirement and conditional readiness approach. Item 10 remains separately pending from the student.

The proposal is not ready for main collection.
