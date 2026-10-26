
# Rebuttal to the iteration-2 meta-review

Authors: Peer A and Peer B.

This response refers to `proposal_v13.md`. It distinguishes implemented design changes, executable evidence and outstanding human work.

We do not claim that every required change is complete. Human development timings remain absent. Final inference validation under the proposed frame, allocation and missingness process also remains incomplete. Confirmatory collection must not begin until those requirements are met.

## Structurally different changes

The repeated issues receive the following changes.

- **Design comparison:** RQ1a is a principal estimand with a meaningful-difference threshold and an operational precision criterion. Its uncertainty includes unresolved outcomes. Failure to support the criterion no longer triggers an unspecified benchmark-paper fallback.
- **Feasibility:** The throughput-dependent stopping design is withdrawn. The proposed minimum is a fixed probability sample with fixed work allowances and complete accounting for failures. A deadline is not treated as feasibility evidence.
- **Repair extension:** The experiment uses matched endorsed-behavior outcomes and contrary evidence. It is outside the protected contribution. Its log-odds null is stated as a modeling choice.
- **63008:** Version 2 repairs the empty-range regression, adds fixed-state assertions and runs all recorded states through an outcome-checking runner.
- **Unresolved outcomes:** Both principal comparisons now have identification bounds. V17 and V18 provide new planning evidence, with their remaining validation limits stated.

## What remains unmeasured

No development case has been timed with a person performing every designated human-review step. The student has been asked about participation, but no answer has been received.

The recorded timings measure automated, LLM-assisted work starting from pilot material. They are not human throughput measurements.

Section 8 now states the proposed resource ceilings, minimum evaluable output and evidence needed before readiness can be declared. Those specifications do not themselves satisfy the committee’s empirical feasibility requirement.

## New evidence

- The version-2 63008 package contains a one-body correction preserving empty ranges, fixed-state assertions and a runner whose recorded execution matched all 12 expected outcomes.
- The fix-scope record classifies the 43 pilot findings with public history.
- The timing record reports 1,373 seconds for the original package, 598 seconds for version 2 and 864 seconds for the fix-scope work.
- V17 evaluates a two-attempt directional procedure using adverse bounds in both directions.
- V18 evaluates precision separately by configuration and scenario and tests exclusion of the meaningful-difference threshold using the bound toward zero.
- The manifest records the cited scripts, results and evidence files. Its current hashes were checked against the files.

These results do not substitute for human adjudication, human development timings or final finite-frame inference validation.

## Responses to required changes

| Item | Status | Response | Sections |
|---|---|---|---|
| 1. Principal contribution and precision | Partly complete | RQ1a is principal. The meaningful difference is 0.10. The criterion uses the largest scenario- and configuration-specific mean half-width of the full bound interval, with a limit of 0.20. It also requires at least 0.80 probability of excluding −0.10 near a true difference of −0.33 in the retained scenarios. V18 shows that the earlier counted-frame claim was too strong: even 40 protocols have sampling half-width 0.210 without unresolved outcomes. The proposed favorable 20-protocol case is promising, but final criterion attainment remains unproved. | 3, 6.4, 8 |
| 2. Human feasibility evidence | Outstanding | The requested human cases have not been completed. The proposal now has a fixed minimum allocation and resource limits, rather than a throughput-dependent sample. At least three complete human development cases, including probability-selected N functions, must support the workload, staffing and missingness assumptions before launch. Failures remain recorded. | 5.2, 8, 10 |
| 3. Audit-blind confirmation | Addressed in the protocol | Primary confirmation occurs before audit access. An unexposed second person handles protocols already known to the student. Audit-derived assistance is confined to the secondary view. Access remains restricted until adjudication and primary locking are complete. | 5.4, 8 |
| 4. Security-specific repair contrast | Addressed by scope and redesign | The experiment is a separately funded extension, not a claimed contribution. Each type measures its endorsed behavior and receives matched contrary evidence. Pair admission checks target, correction effort and conflict. Equal log-odds interactions are an operational modeling null, not a universal definition of ordinary obedience. | 3, 6.6, 7 |
| 5. Monthly resource plan | Specified; feasibility unmeasured | The plan allocates 150 student hours per month, with 1,800 in total. The fixed processing allowance uses the same six-V, eight-N, two-attempt allocation as the proposed minimum. The ledger includes operation, validation, duplicate requests, replay and paid work. The extension has zero student hours. No coursework or teaching is included. Human timings must show that the ceilings are credible. | 8 |
| 6. Complete 63008 package | Executable defects addressed | Version 2 changes only the target body and preserves empty ranges. Fixed-state tests establish reward payment, backing and principal withdrawal. The attack remains with H-02 corrected alone. All 12 recorded runner outcomes match. Corrected repository suites have 56 passes and four failures that assert the old boundary behavior. Independent human adjudication remains separate from the automated package. | 5.11 |
| 7. Natural investigation plan | Specified | Up to 48 first assessments and 12 duplicates fit within 120 hours. Unresolved cases are included within non-confirmed-cell allocations rather than added beyond the budget. Sparse cells are censused and unused slots are not redistributed after outcomes. Selection probabilities support weighted disagreement estimates. The earlier ±0.3 statement is not presented as validated precision. | 5.9, 8 |
| 8. Audit-missed flaws | Planned; availability outstanding | A separate set targets 10–20 flaws demonstrably present in code covered by an earlier audit. Later-introduced flaws are excluded. Availability is not yet counted. Rediscovery measures the selected cases; transfer to historical N sensitivity requires an explicit assumption. Fewer than 10 cases retain the full feasible range. | 5.9, 6.5 |
| 9. Adverse-bound inference | Partly complete | V17 uses two attempts and both directions. Independent null validation includes unresolved shares through 0.10 and a partial-null setting. At 20 protocols, no-unresolved positive-alternative power is 0.65–0.97, falling to 0.47–0.85 at equal unresolved shares of 0.01. These results use a two-V cap, not the proposed six-V cap. Actual-frame validation, correlated construction failures and full bound-interval coverage remain required. The unsupported 0.005 launch rule is removed. | 6.2–6.4, 8 |
| 10. Differential training exposure | Specified | Report and fix dates are compared with documented model cutoffs where available. Unknown cutoffs remain unknown. The V comparison and RQ1a are also reported for the post-cutoff artifact subset, if it exists. This does not prove the underlying code was unseen. | 5.3, 6.8 |
| 11. Reviewer-family overlap | Specified | Reviewer identities are frozen before main collection. Where suitable other-family reviewers are unavailable, the secondary analysis filters to fuzzing and the other-family reviewer for both authors. It is labeled as a filtered campaign view, not a rerun with reallocated effort. | 5.7 |
| 12. Detection gate | Specified with limits | The first gate is five of eight; one revision permits six of eight on fresh cases. The recorded overall probabilities—0.069, 0.455 and 0.913—assume independent trials at recalls 0.3, 0.5 and 0.7. They are planning calculations, not established error guarantees under clustered findings and adaptive revision. | 5.9 |
| 13. Frame-aware allocation | Partly complete | The counted pilot vector includes three zero-V protocols. V18 evaluates that spread but it remains a filtered pilot distribution, not the refreshed frame. The assertion that about 50 V functions generally suffice is withdrawn. The fixed minimum must meet its criterion under the actual frame before collection. | 5.1, 5.2, 6.4 |
| 14. Detection-aware interpretation | Specified | RQ1a accompanies historical V rediscovery and the audit-supplemented comparison. “Little difference” requires the full interval inside ±0.10 and a rediscovery lower bound of at least 0.5. These are reporting conditions, not proof of complete detection. | 5.8, 6.4 |
| 15. Request construction | Specified consistently | A template is frozen. A random subset of 15 functions receives two independent requests from unexposed builders. The generation request is selected in advance. Audit-informed classification occurs only after primary locking and without agent outcomes. Mapping staff cannot later provide blind duplicate construction for the same protocol. | 5.4 |
| 16. Equivalence margin | Addressed | Paper 1 makes no author-security equivalence claim. The design-difference threshold has a separate purpose and includes unresolved-outcome uncertainty. | 6.3, 6.4 |
| 17. “Better security” rule | Addressed by removing the unsupported verdict | The unvalidated non-inferiority decision is removed. Working-output and detected-vulnerability differences are reported separately. The corrected planning contrast is −0.28 − ΔD. A negative D difference alone is not described as better security. | 6.2 |
| 18. Factual clarifications | Addressed, with measurements distinguished from plans | The fix classes remain 17 one-body, 2 multi-body, 15 declaration-related and 9 undetermined. Pilot contrast (a) had a full terminal in both arms. The obsolete subtotal is replaced by one quantity-based allocation ledger. Extension functions would come from the full refreshed frame. The year assumes no teaching or coursework. Final inference must use the finite frame. Seeds use at least 20 patterns and at most three pairs per pattern. Two attempts are a planning choice supported by raw precision comparisons, not measured total-cost superiority. | 3, 5.1, 5.2, 5.9, 6.3, 6.6, 8 |
| 19. Reproducible simulation sources | Addressed for provenance | The unused random-draw fault is fixed. New options preserve default behavior; Peer A reports exact reproduction of V13 under defaults. The manifest records source and result hashes, which were checked. Stored outputs are distinguished from new independent reruns. | 6.3; manifest |

## Disagreements among reviewers

1. **Soundness of the repair contrast.** We follow the AC’s criticism of the old common vulnerability outcome. The extension now uses matched endorsed outcomes. Its remaining modeling assumptions are explicit.

2. **Primary outcome for the extension.** Retention of the endorsed behavior is primary for the matched contrast. Vulnerability retention remains the security endpoint within security arms.

3. **Whether the extension determines acceptance.** It is outside the protected contribution and has no student hours in the year. It requires separate funding and validation.

4. **Testing or estimating the design difference.** RQ1a is a principal estimand judged by precision and a meaningful-difference threshold. Merely rejecting zero is insufficient.

5. **Required feasibility evidence.** We accept that human development evidence is still needed. The fixed sample and resource caps correct the earlier design error but do not manufacture that evidence.

6. **More precision or less work.** The proposal uses two attempts and one fixed allocation. It does not enlarge the sample according to observed throughput or spend unallocated reserves. If the minimum fails budget or precision checks, it does not launch.

7. **What validation measures.** The plan includes seeded flaws, audit rediscovery, selected audit-missed flaws and natural investigation. Each measures its own validation population. Transfer to natural sensitivity is assumption-based.

8. **Equal search.** Own-campaign labeling and audit-blind confirmation are specified. Equal procedure still does not imply equal sensitivity. Validation and sensitivity analysis retain that limitation.

9. **Ratings.** The reviewers agreed on the iteration-2 ratings. This revision does not claim that completed prose alone resolves the remaining C6 and C7 evidence requirements.

## Current readiness

The executable 63008 defects are addressed, and several protocol contradictions are removed. The fixed minimum study is now reviewable as a design.

It is not yet ready for confirmatory collection. Human development timings, funded resource reconciliation and final inference validation remain required.

