# Rebuttal to the iteration-4 meta-review

Authors: Peer A and Peer B. Revised by Peer A in Loop 1 round 29.

This response refers to proposal version 30.

## Student evidence

The student signed a dated commitment on 26 October 2026. It gives 37.5 research hours a week with no coursework or teaching, and plans timed case 1 from 30 October to 13 November 2026.

The three development protocols were drawn that day from the built frame, with a seed fixed before the frame was built. Case 1 is The Wildcat Protocol (Code4rena 2024).

The first complete timed case is still unsupplied. The committee requires it before acceptance. We agree. A schedule is not a substitute. The exposure record, the second person, both adjudicators and funding are also still open.

The proposal now separates prototype simulation evidence from the final launch decision. Selected-demand and frozen-frame results remain pending until development and frame preparation supply their inputs.

## Responses to required changes

| Item | Status | Response | Sections |
|---|---|---|---|
| 1. Confirmation and review limits | Revised | Each candidate has a 1.0-hour student cap and each package has 0.5 hours per adjudicator. A fixed state machine registers working implementations, reserves complete bundles, stops at the first student-confirmed candidate and returns unused reservation to the same source. Independent review determines the final label. Exhausted work remains unresolved. The initial adjudicator ceiling is 205 hours each. A fixed pre-collection funding sequence can enlarge confirmation capacity without changing the main sample. | 5.7, 6.2, 8 |
| 2. Commitment and timed case | Commitment supplied; timed case not supplied | The signed commitment and the development draw are recorded. The timed case remains a committee precondition. It must include probability-selected functions, valid roles, candidate confirmation and both adjudications, with human and machine time separated. | 8 |
| 3. Reading a null result | Revised | The +0.05 margin remains a judgment of material excess, not a safety threshold. Reading uses Holm 0.01. V44 checks all ten conditions, including both ordered partial-margin conditions and the feasible negative alternative. Its full-grid workload has reading-error upper bounds at most 0.0357. A broad null remains inconclusive. | 3, 6.3 |
| 4. Working status and difficulty | Revised | The linked-working frame group remains in V44. Only known-working implementations register confirmation bundles, so reserve exhaustion cannot turn a known functional failure into a possible positive. Separate genuinely unknown-working mechanisms retain adverse bounds. | 5.5, 5.7, 6.2, 6.3 |
| 5. Same-function comparison | Retained | The secondary comparison uses functions where historical code works and at least one agent attempt works. It reports retained counts and preserves sampling weights. Its interval is not presented as validated. | 6.1, 6.3 |
| 6. Package-linked unresolved outcomes | Revised | V44 includes the package mechanism alongside reserve exhaustion. The warning now uses candidate assessment statuses. “Not needed” and non-working closures are excluded from its denominator. Unfinished confirmation and review remain included. An unassessable warning is recorded without an automatic launch stop; missing demand information receives conservative defaults. | 5.7, 6.3, 8 |
| 7. Frame size and certainty units | Revised with the real frame | The frame is built: 190 Code4rena and Sherlock audits with public linked code, 187 after the development draw. Cantina private reviews have no linked code and are outside the population. V45 reruns V44 on this frame, with one certainty protocol. Validity passes; one power corner is lost (below). Every sampled protocol still enters the jackknife. The final frame check remains mandatory. | 5.1, 6.3 |
| 8. Cut candidates | Retained | Separate natural-investigation cells assess campaigns with cut or unfinished lists, within 48 first assessments and 120 auditor hours. Weighted sensitivity estimates remain secondary. | 5.9 |
| 9. V construction | Retained | Development returns to review if V tasks were sampled but none was built. Yields remain descriptive. Low-V frames remain in the simulation checks. | 5.2, 6.3, 8 |
| 10. Confirmed rediscovery gate | Retained and funded | Gate success requires execution and both adjudications. Both assessments reserve 16 target packages and 18.4 student hours for operation and confirmation. | 5.9, 8 |
| 11. RQ1a and V share | Retained | The flagged-only analysis is descriptive. V represents 1.5% to 2.9% of the strict frame, so the principal result mainly concerns unflagged functions. No validated RQ1a interval is claimed. | 3, 6.4 |
| 12. Related work | Retained | Mahmud et al. and SolBehave remain included with distinctions in tasks, generators, sampling and security outcomes. | 7 |
| 13. Factual answers | Updated | Appendix B states candidate statuses, released reservations, non-working outcomes, warning denominators, funding limits and conservative demand defaults. Human timing and compute prices remain missing. | 8, Appendix B |

## What V44 establishes

V44 fixes the sample-dependent rejected-candidate calibration. Working implementations without a detected flaw receive a fixed Binomial rejected-candidate distribution with mean 3/13. This is a planning conditional rate, not the observed overall pilot rate.

The six workloads differ in positive bundle size and candidate time. All receive checks at the retained region corners over all ten conditions.

Three pass those power checks:

- one-candidate bundles at 0.5 hours;
- one-candidate bundles with adverse time;
- three-candidate bundles at 0.5 hours.

Three fail:

- one-candidate bundles at 1.0 hour;
- three-candidate bundles at 1.0 hour;
- three-candidate bundles with adverse time.

At +0.15, pooled confirmation-exhaustion frequencies for the failing workloads are 0.392, 0.962 and 0.419 respectively.

The three-candidate, 0.5-hour workload receives the full mechanism grids. Its worst directional-error upper bound is 0.0436, coverage lower bound is 0.9515 and reading-error upper bound is 0.0357. No estimate is undefined in the recorded checks.

Its common implementation region retains maximal vectors:

- (0.0075, 0.0075, 0.0075);
- (0.013, 0.013, 0.005).

The separate package region is (0.05, 0.05, 0.2).

This does not prove that the full-grid workload dominates all others. Every launch workload must pass the full matrix.

## What V45 changes

V45 repeats V44 unchanged on the real frame. Strict counts come from the hand count for the 20 frame protocols that have one, and are borrowed from a random hand-counted audit for the others.

Error, coverage and reading checks pass in every workload and mechanism. The worst values are 0.0466, 0.9551 and 0.0351.

Power changes in one place. Under the protocol mechanism, the corner (0.0075, 0.0075, 0.0075) has a power lower bound of 0.592, below 0.60. The common implementation region now has maximal vectors (0, 0, 0.0075) and (0.013, 0.013, 0.005). The package region is unchanged.

We adopt the smaller region. We do not change the design to recover the corner.

Demand on the real frame is within 8 hours of V44. If development leaves the planning limits at their maxima, the largest frame-specific 95th percentile is 386 hours. That is above the largest reachable reserve of about 256 hours, so the demand rule would return the design to review.

## State-machine scope and simplifications

A student-confirmed package is provisional. The actual procedure still requires both adjudicators.

The bundle stops at that provisional package. Later candidates are “not needed,” and the queue is not reopened after a completed review rejection. This rule prevents selective extensions.

V44 assumes the student submits only true flaws and completed reviews confirm them. The proposal states that assumption. Material rejection workload observed in development must be added to the final model.

Known non-working implementations retain W = 0 and D = 0. Their security is not measured by primary confirmation. This narrows the earlier treatment of K and is stated explicitly.

Unknown-working failures remain distinct from confirmation exhaustion.

## Demand selection and funding

The supplied demand file pools frames. Its +0.15 95th percentiles range from 111 hours for one-candidate bundles at 0.5 hours to 346 hours for three-candidate bundles at 1.0 hour.

Those values cannot select the reserve. The revised rule uses the largest frame-specific percentile across retained workload profiles.

We did not adopt the suggested passing-workload fallback for absent data. Missing information instead uses the full relevant cap.

The proposal defines protocol-level planning limits, including observed maxima, unfinished work at its allowance and conservative zero-information handling. These are not exact or simultaneous 80% population confidence bounds.

The retained planning profiles include three-candidate positive bundles, uniform and last-position confirmation, and a tail check for rejected candidates. Results for those selected profiles remain pending.

If the existing reserve is insufficient, the funding sequence is fixed:

1. Reduce seeded validation from 60 to 45 pairs.
2. Use month-10 analysis time only down to 30 hours.
3. Return to review if capacity is still insufficient.

The seed reduction frees

\[
30(0.15+1.0)+30(0.15+3/13)
\]

student hours, approximately 46 hours. It also requires revised validation precision. The 60-pair precision figures cannot be reused.

A demand percentile is only a reservation screen. The chosen reserve must still pass the full inference checks under the actual bundle-admission rule and review capacity.

## Resource ledger

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

The fixed funding sequence reallocates named hours before collection. It does not raise the 1,800-hour student ceiling or reduce the main probability sample.

Frame preparation retains its 112-hour ceiling within the 220-hour support budget. Natural investigation retains 120 auditor hours.

## Final validation and current status

The final check includes every retained workload profile, all ten conditions, the full ordered mechanism grids, margin-reading error and the actual reserve and review capacities.

Error and coverage are required outside the power region. Power is required only inside the retained regions. Calibration and fresh validation use the same scope and recomputed multiplicity counts.

An unassessable warning does not itself stop launch. It also supplies no evidence of low demand. Conservative defaults can still make the resource rule fail.

The student commitment is signed; the timed case remains missing. Selected-demand results, any reduced-seed precision calculation and the final frame check remain pre-collection requirements. No new result is claimed for them.
