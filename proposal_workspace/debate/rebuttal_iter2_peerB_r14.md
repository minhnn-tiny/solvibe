
# Rebuttal to the iteration-2 meta-review

Authors: Peer A and Peer B.

This response refers to proposal version 15. It distinguishes implemented design changes, executable evidence and outstanding human work.

We do not claim that every empirical requirement is complete. Human development timings remain absent. Final inference validation under the proposed frame, construction process and unresolved-outcome scenarios remains required. Confirmatory collection must not begin until the readiness conditions are met.

## Structurally different changes

The repeated issues receive the following changes.

- **Design comparison:** RQ1a is a principal estimand with a meaningful-difference threshold and an operational precision criterion. Its uncertainty includes unresolved outcomes and estimated constructible stratum shares. Failure to support the criterion does not trigger an unspecified benchmark-paper fallback.
- **Feasibility:** The throughput-dependent stopping design is withdrawn. The proposed minimum is a fixed probability sample with fixed resource ceilings. Each function receives its own construction procedure and allowance. One function’s workload cannot determine another function’s eligibility.
- **Population and estimation:** The primary target is the domain constructible under that rule. Weighted constructed counts estimate its stratum shares. Every uncertainty replicate recomputes those shares. Original-frame bounds remain secondary.
- **Repair extension:** The experiment uses matched endorsed-behavior outcomes and contrary evidence. It is outside the protected contribution. Its log-odds null is a modeling choice.
- **63008:** Version 2 repairs the empty-range regression, adds fixed-state assertions and runs all recorded states through an outcome-checking runner.
- **Unresolved outcomes:** Both principal comparisons have identification bounds. V17 to V20 provide planning evidence with their limits stated. Construction exclusions cannot retrospectively remove difficult evaluations.

## Open committee question: C7

No development case has been timed with a person performing every designated human-review step. The student has been asked about participation, but no answer has been received.

The recorded timings measure automated, LLM-assisted work starting from pilot material. They are not human throughput measurements.

Section 8 states resource ceilings, a fixed minimum study, its minimum evaluable output and the evidence needed before readiness can be declared. Those specifications do not themselves satisfy the committee’s request for measured human feasibility.

The peers have reached a stalled question and exclude C7 from further peer votes. We ask the committee to decide:

**Can this be accepted as a conditional development proposal with binding launch requirements, or must the human development cases be completed before proposal acceptance?**

Under either decision, confirmatory collection cannot begin until the human cases, funded resource reconciliation and inference checks are complete. The open question does not waive those requirements.

## New evidence and its limits

- The version-2 63008 package contains a one-body correction preserving empty ranges, fixed-state assertions and a runner whose recorded execution matched all 12 expected outcomes.
- The fix-scope record classifies the 43 pilot findings with public history.
- The timing record reports 1,373 seconds for the original package, 598 seconds for version 2 and 864 seconds for the fix-scope work.
- V17 evaluates a two-attempt directional procedure using adverse bounds in both directions.
- V18 evaluates precision separately by configuration and scenario using the bound toward zero.
- V19 evaluates the full interval enclosing both identification bounds.
- V20 includes independent construction selection and estimates constructible stratum shares within every jackknife replicate.
- V20 does not simulate construction that depends on difficulty or vulnerability. Its RQ1b results do not calibrate null error for the new domain.

The simulation source and result files identify the planning procedures. The manifest records versioned evidence. Updated files must be included in the frozen manifest used for release. Stored results are not presented as new reruns by Peer B.

These results do not substitute for human adjudication, human development timings or final finite-frame inference validation.

## Responses to required changes

| Item | Status | Response | Sections |
|---|---|---|---|
| 1. Principal contribution and precision | Design specified; final readiness conditional | RQ1a is principal within the constructible domain. The meaningful difference is 0.10. The criterion requires the largest scenario- and configuration-specific mean half-width of the full interval to be at most 0.20. It also requires at least 0.80 probability of excluding −0.10 near a true difference of −0.33 in retained scenarios. V19 evaluates the full interval. V20 adds construction selection and estimated domain shares. Under construction probabilities 0.9 and 0.9, its displayed half-widths are 0.166 and 0.174, with exclusion rates 0.82 at unresolved shares 0 and 0.005. Other construction scenarios perform worse. These are conditional planning results, not proof of final readiness. Monte Carlo uncertainty must enter the final decision. | 3, 6.3, 6.4, 8 |
| 2. Human feasibility evidence | Outstanding; open committee question C7 | The requested human cases have not been completed. The proposal specifies a fixed minimum allocation, total ceilings and per-function construction reservations. At least three complete human development cases, including a probability-selected set of N functions, must support workload, staffing and construction assumptions before launch. Failures remain recorded. The committee is asked whether this conditional proposal is acceptable before those measurements exist. | 5.2, 8, 10 |
| 3. Audit-blind confirmation | Addressed in the protocol | Primary confirmation occurs before audit access. An unexposed second person handles protocols already known to the student. Audit-derived assistance is confined to the secondary view. Access remains restricted until adjudication and primary locking are complete. Failure to supply an unexposed role is a protocol deviation, not discretionary construction exclusion. | 5.4, 8 |
| 4. Security-specific repair contrast | Addressed by scope and redesign | The experiment is a separately funded extension, not a claimed contribution of the protected year. Each type measures its endorsed behavior and receives matched contrary evidence. Pair admission checks target, correction effort and conflict. Equal log-odds interactions are an operational modeling null, not a universal definition of ordinary obedience. | 3, 6.6, 7 |
| 5. Monthly resource plan | Specified; human feasibility unmeasured | The plan allocates 1,800 student hours over twelve months, with 150 per month. The processing period has 1,050 hours, including 120 for seeded operation and 30 for duplicate-request coordination. The remaining allocation is 45 hours per protocol. Before launch, fixed preparation, per-function construction and operation reservations must fit that ceiling even at the maximum sampled allocation. The ledger includes failed construction, generation, discovery, confirmation, replay and paid work. The extension has zero student hours. No coursework or teaching is included. | 8 |
| 6. Complete 63008 package | Executable defects addressed | Version 2 changes only the target body and preserves empty ranges. Fixed-state tests establish reward payment, backing and principal withdrawal. The attack remains with H-02 corrected alone. All 12 recorded runner outcomes match. Corrected repository suites have 56 passes and four failures that assert the old boundary behavior. Independent human adjudication remains separate from the automated package. | 5.11 |
| 7. Natural investigation plan | Specified | Up to 48 first assessments and 12 duplicates fit within 120 hours. The cells contain implementations from constructed tasks. Unresolved cases are included within non-confirmed-cell allocations rather than added beyond the budget. Sparse cells are censused and unused slots are not redistributed after outcomes. Selection probabilities support weighted disagreement estimates. The earlier ±0.3 statement is not presented as validated precision. | 5.9, 8 |
| 8. Audit-missed flaws | Planned; availability outstanding | A separate set targets 10–20 flaws demonstrably present in code covered by an earlier audit. Later-introduced flaws are excluded. Availability is not yet counted. Rediscovery measures these selected cases; transfer to historical N sensitivity in the constructible domain requires an explicit assumption. Fewer than 10 cases retain the full feasible range unless another justified assumption is examined. | 5.9, 6.5 |
| 9. Adverse-bound inference | Planning evidence available; final validation required | V17 uses two attempts and both directions. At 20 protocols, positive-alternative power is 0.65–0.97 without unresolved outcomes and 0.47–0.85 with equal unresolved shares of 0.01. It uses a two-V cap and does not validate the revised domain. V20 uses the six-V allocation and construction selection. Its plain RQ1b interval coverage ranges from 0.925 to 0.935 across the displayed construction scenarios, so calibrated coverage is not claimed. Exact domain nulls, partial nulls, both directions, estimated shares and difficulty-dependent construction must enter final validation. There is no universal 0.005 launch rule. | 6.2–6.4, 8 |
| 10. Differential training exposure | Specified | Report and fix dates are compared with documented model cutoffs where available. Unknown cutoffs remain unknown. The V comparison and RQ1a are also reported for the constructible subset with post-cutoff artifacts, if it exists. This does not prove the underlying code was unseen. | 5.3, 6.8 |
| 11. Reviewer-family overlap | Specified | Reviewer identities are frozen before main collection. Where suitable other-family reviewers are unavailable, the secondary analysis filters to fuzzing and the other-family reviewer for both authors. It is a filtered campaign view, not a rerun with reallocated effort. | 5.7 |
| 12. Detection gate | Specified with limits | The first gate is five of eight; one revision permits six of eight on fresh cases. The recorded overall probabilities—0.069, 0.455 and 0.913—assume independent trials at recalls 0.3, 0.5 and 0.7. They are planning calculations, not established error guarantees under clustered findings and adaptive revision. | 5.9 |
| 13. Frame-aware allocation | Revised to include construction selection | The counted pilot vector includes three zero-V protocols. It remains a filtered pilot distribution, not the refreshed frame. The assertion that about 50 V functions generally suffice is withdrawn. V20 models independent construction selection under the earlier V assumption. The final analysis estimates constructible stratum shares from weighted constructed counts. Final readiness must use the actual frame and include difficulty-dependent construction, sparse domains and undefined estimates. | 5.1, 5.2, 6.3, 6.4 |
| 14. Detection-aware interpretation | Specified | RQ1a accompanies historical V rediscovery and the audit-supplemented domain comparison. “Little difference” requires the full interval inside ±0.10 and a rediscovery lower bound of at least 0.5. These are reporting conditions, not proof of complete detection. | 5.8, 6.4 |
| 15. Request construction | Revised and specified consistently | The template, materials, steps, checklist, assignment rule and per-function allowance are frozen before main sampling. A random subset of 15 functions receives two independent construction attempts from unexposed builders. The designated primary procedure determines construction eligibility and the generation request. The duplicate cannot rescue primary construction failure. Audit-informed classification occurs only after primary locking and without agent outcomes. Mapping staff cannot later provide blind duplicate construction for the same protocol. | 5.2, 5.4, 8 |
| 16. Equivalence margin | Addressed | Paper 1 makes no author-security equivalence claim. The design-difference threshold serves a separate purpose. Its uncertainty includes unresolved outcomes and estimated domain shares. | 6.3, 6.4 |
| 17. “Better security” rule | Addressed by removing the unsupported verdict | The unvalidated non-inferiority decision is removed. Working-output and detected-vulnerability differences are reported separately. The corrected planning contrast is −0.28 − ΔD. A negative D difference alone is not described as better security. | 6.2 |
| 18. Factual clarifications | Addressed, with measurements distinguished from plans | The fix classes remain 17 one-body, 2 multi-body, 15 declaration-related and 9 undetermined. Pilot contrast (a) had a full terminal in both arms. The quantity ledger distinguishes sampled construction attempts from constructed functions receiving generation and discovery. Extension functions would come from the whole refreshed frame. The year assumes no teaching or coursework. Final inference must use the finite frame and constructible domain. Seeds use at least 20 patterns and at most three pairs per pattern. Two attempts are supported by raw precision comparisons, not measured total-cost superiority. | 3, 5.1, 5.2, 5.9, 6.3, 6.6, 8 |
| 19. Reproducible simulation sources | Source changes documented; final release freeze required | The unused random-draw fault is fixed. Peer A reports that the added options preserve the specified earlier results under their defaults, including exact reproduction of V11 when construction selection is unset. V20 explicitly distinguishes its estimated-domain scenarios from the all-built baseline. Final source versions, results, streams and manifest hashes must be frozen together. Stored outputs are distinguished from new independent reruns. | 6.3, 6.4; simulation sources and manifest |

## Disagreements among reviewers

1. **Soundness of the repair contrast.** We follow the AC’s criticism of the old common vulnerability outcome. The extension now uses matched endorsed outcomes. Its remaining modeling assumptions are explicit.

2. **Primary outcome for the extension.** Retention of the endorsed behavior is primary for the matched contrast. Vulnerability retention remains the security endpoint within security arms.

3. **Whether the extension determines acceptance.** It is outside the protected contribution and has no student hours in the year. It requires separate funding and validation.

4. **Testing or estimating the design difference.** RQ1a is a principal estimand judged by precision and a meaningful-difference threshold. Merely rejecting zero is insufficient. The estimate now concerns the declared constructible domain and includes uncertainty in its composition.

5. **Required feasibility evidence.** Human development evidence remains absent. Fixed reservations and resource ceilings correct design problems but do not manufacture that evidence. C7 is explicitly referred to the committee as an open question about conditional proposal acceptance.

6. **More precision or less work.** The proposal uses two attempts and one fixed allocation. It does not enlarge the sample according to observed throughput or allow easy tasks to fund extra work on difficult ones. Every selected function receives its own promised construction procedure. If the minimum fails budget or precision checks, it does not launch.

7. **What validation measures.** The plan includes seeded flaws, audit rediscovery, selected audit-missed flaws and natural investigation. Each measures its own validation population. Transfer to natural sensitivity is assumption-based.

8. **Equal search.** Own-campaign labeling and audit-blind confirmation are specified. Equal procedure still does not imply equal sensitivity. The domain restriction is shared across authors, but it does not establish representativeness of unbuilt functions.

9. **Ratings.** The reviewers agreed on the iteration-2 ratings. This revision does not claim that completed prose establishes empirical readiness. C7 remains the committee’s open question. Final inference and resource checks remain binding conditions before collection.

## Current readiness

The executable 63008 defects are addressed. The fixed minimum study now specifies construction eligibility without a shared stopping budget. Its domain estimator includes estimated stratum shares and their uncertainty.

V20 provides relevant planning evidence for independent construction selection. It does not validate difficulty-dependent selection, the actual finite frame or the final RQ1b error rate. Favorable rounded simulation rates are not treated as proof of readiness.

The study is not yet ready for confirmatory collection. Human development timings, funded resource reconciliation and final inference validation remain required.

