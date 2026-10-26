# Rebuttal to the iteration-3 meta-review

Authors: Peer A and Peer B.

This response refers to proposal version 24.

We distinguish completed evidence, revised design rules and remaining preconditions. We do not claim that every required change has been completed.

## Requested changes to the committee’s decisions

We request approval for RQ1b as principal and RQ1a as secondary and descriptive. This departs from the iteration-3 AC’s resolution.

The principal estimand is detected vulnerability among working agent implementations minus that among working historical implementations, standardized across the constructible strata. Functional failure and D remain separate reported quantities.

V27’s half-widths of 0.338 and 0.422 concern the earlier 20-protocol allocation. They do not support the old RQ1a precision promise. V37 now evaluates the proposed allocation and reports a largest mean RQ1a half-width of 0.711 under its independent unresolved-outcome mechanism. We do not claim that every affordable alternative has been ruled out.

We retain the request for a minimum power of 0.60 at +0.15 within stated operating assumptions. This is lower than the earlier 0.80 requirement and needs committee approval.

We also request approval to replace development-based certification of rare unresolved rates with conditional planning assumptions and a fixed diagnostic. Adverse bounds remain in the principal analysis. We are not adopting a primary missing-at-random analysis.

The reason is that development has few historical implementations and shared protocol environments. Repeated agent attempts do not remove that uncertainty. The former pooled limit and adaptive extension were unsound.

A further correction concerns construction. The fixed development sample contains at most three V functions. We withdraw the requirement that a construction-yield lower confidence limit exceed 0.7. Development instead checks valid execution within fixed caps, reports yields descriptively and applies a stated warning rule for gross construction failure.

We request committee approval for this change. The construction settings in the simulation remain planning assumptions. Development does not certify them by stratum.

The proposal cannot guarantee before collection that the study will remain within its construction and unresolved-outcome assumptions. If the committee requires that guarantee, this revision does not meet it.

## New evidence

### Ordered rates and the retained region

V37 keeps the V33 procedure frozen: Holm level 0.03 and interval multiplier 1.175 for 22 protocols with up to one V and six N functions and two attempts per configuration.

It evaluates 76 ordered unresolved-rate vectors on 24 fixed frames, with 4,000 fresh studies per frame and condition. It removes the configuration-swap shortcut.

The mechanisms are independent outcomes, shared function failures, shared protocol failures and difficulty-dependent outcomes. Samples and underlying outcomes are common across rate vectors and mechanisms.

Bonferroni counts per mechanism are 5,472 error checks, 21,888 coverage checks and 3,648 power checks. Confidence adjustment is separate by mechanism and criterion.

The worst error upper bound is 0.0408. The worst marginal-coverage lower bound is 0.9567. The corrected worst undefined share is 0.00075.

V37’s passing region has maximal vector \((0.013,0.013,0.0075)\). We retain the smaller region with maximal vectors:

- \((0.0075,0.013,0.0075)\);
- \((0.013,0.0075,0.0075)\);
- \((0.013,0.013,0.005)\).

The omitted corner’s protocol-mechanism power lower bound was 0.598 in V35 and 0.606 in V37. We do not enlarge the region on that crossing. V37 validates both ordered assignments directly; V35 is supporting evidence for the assignments it actually tested.

Validation applies to tested vectors. Extending the region continuously below these corners is an explicit planning assumption.

Every tested vector with historical unresolved rate 0.02 or greater fails the power requirement under every mechanism.

### Diagnostic within the study generator

V38 evaluates the diagnostic on fresh samples from the V37 generator. It uses 4,000 main samples and 4,000 development samples per frame. The main and development sample sizes are 22 and three protocols.

The diagnostic uses each author’s count of protocols with an unresolved outcome, the number with scheduled outcomes, and the largest author-specific outcome count in one protocol. It borrows a binomial lower-limit formula to define a score.

We no longer call that score an exact population confidence limit or claim that division guarantees conservatism. V38 supplies empirical operating characteristics within the planning model.

For the retained region, the largest pooled firing rates among tested inside-region vectors are:

| Mechanism | Main | Development |
|---|---:|---:|
| Independent | 0.019 | 0.018 |
| Task | 0.011 | 0.006 |
| Protocol | 0.000 | 0.000 |
| Difficulty | 0.018 | 0.017 |

These rates pool frames. They are not worst-frame guarantees. Displayed zeros are rounded results.

At \((0,0,0.065)\), main firing rates are 0.927, 0.928, 0.053 and 0.926. Development rates are 0.224, 0.222, 0.012 and 0.222.

The diagnostic is weak for shared protocol failures. A non-flagging result does not establish that the study lies inside the region.

### Construction warning

The former construction lower-limit gate is removed.

After the fixed three cases, the study computes the upper binomial-limit formula for pooled built functions divided by sampled functions. A value below 0.7 stops launch and returns the design to review.

This is a warning rule, not an exact population confidence bound. It does not establish either stratum’s construction yield.

V37 reports pooled firing rates of 0.000 at target construction yield 0.9 and 0.033 at target yield 0.7. Mean development yields are 0.900 and 0.700. No sample in those runs had nothing built.

Sensitivity below these settings and to poor V construction masked by N outcomes is not established. The proposal makes no such claim.

## Structurally different response to the repeated readiness failure

The revised rules are:

- Development consists of three fixed probability-selected cases using the main task allocation and attempt count.
- Development tests valid execution and resource limits.
- Construction yields are descriptive, with a fixed warning rule.
- No zero-unresolved requirement remains.
- No sample extension is triggered by an unresolved outcome or an unfavorable warning.
- Main sampling is fixed before evaluation.
- Unresolved counts are recorded separately by author and stratum.
- The diagnostic cannot replace tasks, add attempts or change primary analysis.
- Adverse bounds remain primary.
- A development warning or diagnostic flag prevents launch.
- A main diagnostic flag withdraws the planned power statement.
- A non-flagging result leaves that statement conditional.
- Missing or inconclusive required adjudication remains unresolved.
- Two completed substantive decisions that fail to confirm jointly produce “not confirmed,” with a secondary unresolved bound.
- A documented departure outside the validated error-control domain prevents a validated directional claim.

Section 8 gives the exact order, formulas and failure rules for the development kit. It does not claim that the combined development pass probability has been validated.

## Responses to required changes

| Item | Status | Response | Proposal sections |
|---|---|---|---|
| 1. Allocation and budget | Revised; human adequacy pending | The allocation remains 22 protocols with one V and six N functions. Its middle planning cost is 880 hours. The student campaign cap is 0.328 hours, including confirmation. Development uses the same task allocation and attempts. Paid work has fixed source reservations. These are caps, not measured proof of adequate time. | 5.2, 5.7, 8 |
| 2. Counted frame and readiness simulation | Reconciliation complete at proposal stage; planning validation expanded | Strict counts are 54 observed-fix V functions, 109 including admissible recommendations and 3,620 N functions. Final severity and provenance checks remain. V37 combines the finite frame, sampling, construction, adverse bounds, all ordered author rates and four failure mechanisms. V38 evaluates the diagnostic within that generator. | 5.1, 6.3 |
| 3. Security and functional failure | Retained | Conditional security, the D decomposition, weighted estimation, admissible outcome sets and the undefined-denominator rule remain explicit. No causal or paired-new-flaw interpretation is claimed. | 3, 6.2, 6.3 |
| 4. Checks endorsing flaws | Retained | Blind-process check revisions occur before locking and apply to all implementations. Audit-derived revisions remain secondary and cannot reopen primary labels. | 5.5 |
| 5. “Little difference” | Removed | RQ1a is descriptive. V37’s largest mean half-width is 0.711 with the uncalibrated multiplier. No null result is interpreted as equivalence or a small difference. | 6.4 |
| 6. RQ1b precision | Reduced target requested; grid evidence complete | The request remains 0.60 power at +0.15 under stated assumptions. The retained region is smaller than V37’s largest passing box because its additional boundary failed V35. Continuous extension is an assumption, not a simulated guarantee. | 3, 6.3 |
| 7. Retained scenarios | Explicit departure requested | Development no longer certifies rare unresolved rates. Separate author rates and four mechanisms define planning scenarios. Construction assumptions are also conditional. The fixed diagnostic does not select the sample or analysis. | 3, 6.3, 8 |
| 8. Recall sensitivity | Retained | Author and design comparisons use sensitivity assumptions by author and stratum. D sensitivity includes working rates. Validation populations are not treated as interchangeable. | 6.5 |
| 9. Blind candidate rediscovery | Completed at candidate level | Claude matches 17 of 17 and Codex 13 of 17; excluding weak keys gives 14 of 14 and 13 of 14. Independent-trial intervals are not population recall guarantees. Executable 63008 evidence governs the H-02 causal claim. | 5.9, 5.11 |
| 10. Student commitment and timing | Pending from the student | The dated commitment and complete student-timed case remain preconditions before resubmission. The full three-case record remains required before launch. Automated timings do not substitute for human work. | 8, 10 |
| 11. Candidate cuts | Retained and clarified | Cut lists receive a secondary unresolved bound. Missing, unfinished or inconclusive required assessments remain unresolved in the principal analysis. Completed substantive disagreement fails joint confirmation and receives a secondary unresolved bound. | 5.7, 6.2 |
| 12. Historical reproduction | Retained | The recall flag covers distinctive fixes and historical-body reproduction. Thresholds are frozen before generation. Exclusion analyses remain secondary. | 6.8 |
| 13. Duplicate requests | Retained | Both evaluable requests receive generation and discovery. Campaigns and coordination share the reserve. Construction and review enter paid ledgers. | 5.4, 8 |
| 14. Simulation history | Updated | Appendix A identifies V37 as current inference evidence and V38 as current diagnostic evidence. V35’s shortcut and V36’s simplified design are disclosed. The corrected diagnostic checks six quantities. | 6.3, Appendix A |
| 15. Factual answers | Updated | Appendix B states the fixed development design, retained region, continuous-extension assumption, descriptive construction yields, diagnostic limits and remaining unknowns. | Appendix B |

## Responses to the reviewers’ disagreements

### 1. Novelty and contribution

The contribution is an empirical historical comparison with probability sampling, executable attribution and explicit detection limits. Probability weighting itself is not claimed as novel.

The principal-estimand change and reduced power weaken the original promise. Their adequacy remains a committee decision.

### 2. Soundness

The estimator and adverse bounds remain aligned with the conditional security component.

The zero-detection term is a binomial-based widening adjustment, not an exact bound for weighted, clustered observations.

V37 validates the frozen procedure under its tested ordered-rate scenarios. V38 evaluates the diagnostic under the same sampling and construction model. The final analysis does not depend on whether the diagnostic flags.

Neither diagnostic formula is presented as an exact population confidence limit. Continuous interpolation of the region and transfer to the actual study remain assumptions.

### 3. Feasibility

Section 8 gives one capped development schedule and an exact decision sequence for the kit. Per-candidate time cannot be added outside the campaign cap. Audit-assisted work covers at most one constructed V task per case.

Human adequacy remains unmeasured. If fixed caps cannot support valid work, development fails the operational requirement.

The main plan remains bounded. It accepts a risk of inconclusive results if construction or unresolved outcomes depart from the planning assumptions.

The impossible construction lower-limit gate is removed. Its replacement does not claim to certify either stratum’s yield.

### 4. Common construction allowance

V and N retain the same visible allowance. Different limits could reveal stratum labels.

Construction failure remains a pre-evaluation decision. Shared budget exhaustion or missing staff cannot redefine a function as unconstructible.

Development reports construction by stratum and protocol. The pooled warning is not substituted for those records and cannot establish that V construction is adequate.

### 5. “Little difference”

No such reading is restored. RQ1a remains descriptive, and broad results remain inconclusive.

The conditional operating region does not strengthen interpretation of a null result.

### 6. Principal estimand

We continue to request RQ1b as principal and RQ1a as secondary.

V35 reports a largest mean RQ1a half-width of 0.710, or 0.635 with no unresolved outcome. V37 reports 0.711 and 0.634. Both use multiplier 1.175 without RQ1a calibration.

V37’s lowest coverage ranges from 0.940 to 0.945 across conditions. These results do not support validated RQ1a directional claims.

If the committee rejects the principal-estimand change, a different reviewed design is required.

### 7. Unresolved outcomes

Adverse bounds remain primary, as the AC required.

We request a departure from development-based certification of unresolved-rate scenarios. The replacement is a fixed-sample study with stated conditional performance and a diagnostic with measured but limited sensitivity.

The diagnostic can miss substantial protocol-wide failures. It does not certify population rates, and a non-flagging result does not establish the power assumptions.

The adjudication rule distinguishes completed substantive disagreement from inability to assess. Only the former can close as not confirmed. The latter remains unresolved in the principal analysis.

### 8. Frame-based readiness

Strict reconciliation is complete at proposal stage. Final severity and provenance checks remain.

V37 now preserves the finite frame, unequal sampling probabilities, dependent construction and adverse bounds while evaluating every ordered author-rate assignment.

V38 evaluates both candidate-region diagnostics on fresh draws. We retain the smaller region because the added boundary crossed the power threshold between runs.

The construction settings are not certified by development. We request approval to treat them as conditional planning assumptions, with descriptive records and the stated warning rule.

### 9. Human evidence before acceptance

The dated commitment and first complete timed case remain pending. The complete three-case record remains required before launch.

Cases must test the actual caps and blindness rules. Deviations cannot count as successful demonstrations. No additional cases are triggered to obtain a favorable construction or unresolved count.

## Current status

The revision removes the configuration-swap shortcut, the unsupported population-confidence interpretation of monitoring and the unattainable construction lower-limit gate.

It retains a fixed probability sample, equal procedures, adverse bounds and explicit outcome records. V37 supports the tested inference conditions. V38 supplies diagnostic operating characteristics within the planned generator.

The diagnostic and construction warning do not certify the study’s assumptions. Their limits are stated in the proposal.

Before main sampling, the V37 checks are repeated on the frozen frame, with the development protocols removed and main inclusion probabilities computed on the remaining frame. If the frozen procedure fails there, a replacement is calibrated on a separate stream and validated on fresh draws; if none passes, or power fails inside the frozen region, the preferred allocation does not launch.

Committee approval remains required for the principal estimand, reduced power requirement, conditional readiness approach and revised construction rule. Item 10 remains separately pending from the student.

The proposal is not ready for main collection.
