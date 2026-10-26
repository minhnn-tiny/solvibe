## Status of the 15 AC items

1. **Partly:** The allocation table and common construction allowance are present, and its arithmetic matches V22; expected candidate costs still do not establish the promised reservations, and the duplicate-request work is not fully budgeted.
2. **Not resolved:** The inventory counts findings and linked functions, then models eligible V counts; it does not classify all qualifying fixes in a random protocol sample, and V21–V23 do not simulate an enumerated finite frame or difficulty-dependent construction.
3. **Partly:** The decomposition is algebraically valid, but the new principal security component lacks a complete estimator, unresolved-outcome bounds and matching confirmatory test in the proposal.
4. **Partly:** The check-removal rule is present, but its timing relative to audit-assisted evaluation and primary locking is unspecified.
5. **Partly:** “Little difference” is removed, but reported detection thresholds concern D rather than the security component, and some thresholds are extrapolations beyond the simulated results.
6. **Not resolved:** V23 calibrates Holm for D, not the principal security component; its larger-effect results do not demonstrate the stated +0.10 target.
7. **Partly:** Confidence-limit rules are specified, but construction yields are optimistically floored, development counts are maxima rather than guaranteed observations, and the required joint readiness simulation remains absent.
8. **Partly:** The sensitivity analysis explicitly includes both RQs, but its formulas and example still concern D rather than the new principal conditional security comparison.
9. **Resolved for the requested candidate-level exercise:** The reported match counts agree with the judge records and mapping; this is not executable confirmation or a population recall estimate.
10. **Partly, pending from the student:** The commitment is reported, but the dated form and timed case are absent; this item is excluded from my vote.
11. **Resolved:** Cut candidate lists are recorded, reported by author and stratum, and treated as unresolved in a secondary bound.
12. **Resolved:** Historical-body reproduction is included in the recall flag, with secondary exclusion analyses.
13. **Partly:** Both requests now receive generation and discovery, but their added work is charged to an already allocated reserve without a complete cost reconciliation.
14. **Resolved:** Superseded simulations have moved to Appendix A.
15. **Partly:** Appendix B answers the questions, but several answers remain assumptions or unknowns, and its empty-stratum calculation does not establish the requested probability under the actual design.

## Remaining issues

### R15.1 [Blocking] [C4, C6] The principal security component has no matching analysis specification

**Sections:** 6.2, 6.3 and 6.5.

**Problem and evidence:** Section 6.2 now defines the security component as \(v_A-v_H\), where each rate is conditional on working outputs. That decomposition is valid. However, section 6.3 still specifies an average of per-function endpoint differences and gives the design-difference formula using \(d^D\). These are not the conditional-rate estimator implemented in `est_sec()`.

The code instead divides weighted vulnerable-and-working totals by weighted working totals separately for each author and stratum. It then standardizes these differences using domain stratum shares. This is neither the ordinary D difference nor, generally, the unstratified difference among all working outputs.

The unresolved-outcome rules still bound D. They do not specify how uncertainty about working status affects the conditional denominators, or what happens when an author has no working outputs in a stratum. Section 6.5 likewise defines sensitivity using “detected D rates.”

**Required change:** Replace the principal analysis specification with one complete definition of the standardized conditional security estimand, its weighted ratio estimator, admissible unresolved-outcome bounds, zero-denominator treatment and matching sensitivity analysis.

### R15.2 [Blocking] [C6] V23 does not validate the declared principal decision or target

**Section:** 6.3; `tools/power_sim_v23.py`.

**Problem and evidence:** V23’s Holm calibration uses output indices 0–2, which are D estimates and truths. Its null scenarios satisfy zero D difference. They do not impose zero security-component difference. The security-component results use indices 12–14 and report exclusion by separate pointwise intervals, without the declared Holm family decision.

The stated target is +0.10, but the cited evidence concerns true security differences of +0.129 to +0.152 and +0.062 to +0.084. Success at the larger alternatives does not establish success at +0.10. Nor does failure to obtain high power in selected smaller-effect scenarios prove that +0.05 is unaffordable under every candidate allocation.

There is also an output aggregation defect: the dictionary keyed by rounded true effect in V23 overwrites scenarios sharing that rounded value. Thus the displayed range does not establish the claimed minimum over every scenario.

**Required change:** Produce a validation of the actual security-component family decision at exact security nulls, partial nulls and the exact declared meaningful effect, retaining every scenario separately and using the final unresolved-outcome rule.

### R15.3 [Blocking] [C6] The requested frame-based readiness analysis remains undone

**Sections:** 5.1, 6.3, 6.4 and 8.

**Problem and evidence:** The inventory is useful evidence about the downloaded data. It is not the requested eligible-function census.

The inventory README states that:

- 61.0% of findings could not be mapped;
- the modeled count uses 0.729 distinct functions per mapped finding;
- each resulting function is retained using the pilot proportion 17/34;
- counts are capped at six.

The mean 2.15 comes from one modeled draw, not observed eligibility. The 22.9% zero share comes from the adjustment model. The subset of 42 audits is **at least 80% mapped**, not fully mapped.

In V8, `rng.choice(..., P)` samples modeled V counts with replacement, while N counts are independently generated between 30 and 120. Only sampled functions receive outcomes. This is not the fully enumerated finite population requested by the AC. V21–V23 also leave construction selection unset.

Capping modeled population V counts at six before calculating population shares further confuses a sampling cap with a population count.

**Required change:** Replace the modeled-frame readiness claim with an audited random-protocol inventory of uncapped eligible V and N counts and a finite-population simulation that includes difficulty-dependent construction under the proposed allowance.

### R15.4 [Major] [C7] Expected workload is still presented as a hard reservation

**Sections:** 5.7, 8 and Appendix B.

**Problem and evidence:** The selected row’s 43.9 hours is correctly calculated from expected candidate workload. It uses \(c=0.178\) candidates per campaign. Yet Appendix B allows three confirmations per implementation, and section 8 itself says an expected candidate count is insufficient.

The proposal therefore has not shown that every implementation can receive its promised confirmation allowance within the resource ceiling. The paid adjudicator quantities similarly use expected package counts.

The common construction allowance also changes from the earlier V assumptions of 4–8 hours to 1.5–3 hours. This can be proposed as a shorter fixed procedure, but it is not evidence that comparable construction yield will remain achievable.

**Required change:** Replace the claimed hard reservation with a fully costed schedule of fixed per-stage allowances, including confirmation and adjudication caps, and carry the resulting construction and confirmation losses into readiness analysis.

### R15.5 [Major] [C7] Duplicate-request evaluation consumes an already allocated reserve

**Sections:** 5.4 and 8.

**Problem and evidence:** Section 5.4 adds \(15\times5\) campaigns and charges running and confirmation to the 30-hour “coordination reserve.” At the stated middle assumptions, these campaigns consume most of that reserve before coordination, independent construction, packaging, adjudication or replay.

The ledger still labels the reserve as duplicate-request coordination. The allocation table does not show this added workload or how the original coordination work is reduced. The paid package counts also describe the main 800 campaigns rather than all validation and duplicate-request packages.

**Required change:** Add a reconciled duplicate-request budget covering construction, generation, discovery, confirmation, adjudication and coordination, with explicit deductions from the existing student and paid ceilings.

### R15.6 [Major] [C4, C6] Readiness rules can discard adverse evidence and disagree about whether collection starts

**Sections:** 5.2, 6.3 and 8.

**Problem and evidence:** Section 6.3 floors the lower confidence limit for construction yield at 0.7. If the observed yield exceeds 0.7 but its lower limit does not, this replaces adverse uncertainty with a more favorable value. Section 5.2’s rule based on the observed proportion does not resolve that case.

The proposed 120 development evaluations are \(3\times8\times5\), a maximum under the selected allocation. Small strata, failed construction and incomplete evaluations reduce the actual denominator. Independent binomial confidence limits also need justification when failures cluster within protocols and functions.

Finally, section 6.3 says a failed target leads to estimates without directional claims, whereas section 8 says confirmatory collection does not begin. The allocation-selection rule can change protocol count but refers to a rerun that currently omits the retained construction and unresolved-outcome scenarios.

**Required change:** Replace these provisions with one preregistered readiness algorithm using actual denominators, dependence-aware uncertainty and untruncated adverse limits, with one consistent action when any required target fails.

### R15.7 [Major] [C1, C6] The change of principal contribution needs an explicit, supported case

**Sections:** 2, 3, 6.4, 7 and rebuttal.

**Problem and evidence:** Moving RQ1b to principal is a defensible proposal to discuss. It is not implementation of the iteration-3 AC decision, which explicitly says to keep RQ1a principal and make RQ1b co-principal only if its target is met.

The claimed reason is stronger than the evidence: the simulations evaluate a small allocation menu under modeled counts and changed assumptions, not every affordable allocation under a measured eligible frame.

The manuscript also remains inconsistent. Section 3 makes the author comparison principal, while section 7 says the intended contribution is “the empirical size of the sampling effect.” The new title of section 3 asks whether agents add flaws “where the developer did not,” but a marginal conditional-rate difference does not identify that paired event.

**Required change:** Present a consistent, explicit rebuttal of the AC’s principal-estimand decision, defining the new empirical contribution and its attainable evidence standard without claiming that all affordable alternatives have been ruled out.

### R15.8 [Major] [C4] Functional-check correction can reopen the primary endpoint after audit access

**Sections:** 5.5 and 5.8.

**Problem and evidence:** The new rule drops a faulty functional check “for every implementation” when a correction exposes it. It does not say whether audit-derived corrections discovered after primary locking can trigger this change.

That matters because audit-assisted work is now performed on a random half of V functions. Allowing those discoveries to change primary L would give selected audited cases an extra source of primary-outcome revision. Refusing all such revisions without explanation would leave the manuscript’s “for every implementation” rule inaccurate.

**Required change:** Specify that primary check revisions must arise from the audit-blind primary process before locking, while later audit-derived revisions produce a separately labeled secondary outcome recomputed consistently across the cohort.

### R15.9 [Major] [C4, C6] Half-sampling audit-assisted evaluation changes the secondary estimands

**Sections:** 5.2 and 5.8.

**Problem and evidence:** Section 5.2 now performs audit-informed work for a random half of V functions. Section 5.8 still promises audit-supplemented comparisons and rediscovery results without defining the selection probabilities, treatment of small strata, or estimation for the unassessed half.

An unassessed audit flaw cannot be treated as missed or absent. The audit-supplemented full-domain comparison cannot be obtained by simply adding discoveries from the assessed half to the full primary dataset.

**Required change:** Specify a probability-sampling and weighted-estimation procedure for the audit-assisted subset, including its uncertainty and the handling of unassessed cases.

### R15.10 [Minor] [C6] Several numerical interpretations exceed the result files

**Sections:** 6.4, 6.5, 8 and Appendix B.

**Problem and evidence:**

- V22’s 17-protocol row reaches 0.78 at the largest displayed distortion, −0.64. It does not establish a detectable distortion of “about 0.65.”
- Rounded effect keys in V22 overwrite scenarios, so “smallest distortion” is not a validated worst-scenario threshold.
- “Fits exactly” is inaccurate: the file reports 877 middle-rate hours against a 900-hour protocol budget.
- The −0.47 example is the latent D difference, not the conditional security difference.
- The empty-stratum approximation \(0.229^{20}\) uses a modeled zero share and independent draws. It omits construction failure and does not describe the proposed finite sampling design.
- A +0.10 conditional rate difference does not mean that one in ten paired functions gained a vulnerability absent from the developer implementation.

**Required change:** Replace these interpretations with statements tied to the actual estimand, simulated scenarios and sampling assumptions, removing unsupported threshold and paired-incidence claims.

### R15.11 [Minor] [C6] Rediscovery intervals and “upper bounds” need narrower wording

**Section:** 5.9.

**Problem and evidence:** The candidate counts match the recorded judgments. However, nine findings come from Panoptic, and several share files and related snapshots. The displayed Wilson intervals do not account for this dependence or represent sampling from a population of flaws.

Candidate matches bound confirmations only within those same candidate lists and confirmation paths. They are not upper bounds on a future campaign that also uses fuzzing, different context and potentially different reviewers.

The judge’s batch-1 note also says the 63008 theft depends on H-02, contrary to the executable package’s demonstrated H-02 independence. This does not change the root-cause match, but the evidence record should not retain the contradictory interpretation.

**Required change:** Qualify the rediscovery results as descriptive candidate-list measurements, state the interval assumptions and limits, and correct the contradictory 63008 judge note.

### Dependency on item 10

The student’s missing record is not included above as a peer-fixable issue. It remains necessary for construction allowances and yields, unit costs, funded staffing, compute pricing, actual development denominators and final allocation selection. The executable kit does not supply those measurements.

The frame audit, estimand specification, simulation corrections, budget arithmetic and rebuttal corrections can proceed without the student’s timing record.

## Rebuttal corrections

The following replacements concern the **Decision** and **What changed** cells where applicable. Unlisted response rows need no substantive correction.

| Row or location | Problem | Exact replacement text |
|---|---|---|
| Opening: “What changed most” | Calls the modeled frame measured and treats the change of principal estimand as already justified. | “The inventory and allocation simulations motivate a proposed change of principal estimand. They do not yet establish that no affordable allocation can support RQ1a. We propose making the standardized conditional security comparison in RQ1b principal and RQ1a secondary. This departs from the iteration-3 AC’s instruction and requires an explicit justification. The current principal-analysis validation remains incomplete.” |
| “Stagnation rule” | Calls item 2 a frame-wide eligible count and item 10 a completed structural remedy. | “Items 1, 2 and 10 repeat earlier requirements. We added an allocation cost model and an inventory of downloaded findings. Eligible V counts are still modeled rather than obtained from the requested random-protocol fix-scope audit. The student has committed to participate, but the dated commitment and timed case remain pending.” |
| 1 | “Done,” “fits exactly,” and hard-reservation claim are unsupported. | “Partly addressed. V22 reports 27.0, 43.9 and 62.8 assumed hours per protocol for the selected row, with 877 hours at middle rates against a 900-hour protocol budget. These calculations use expected candidate counts. Fixed confirmation reservations, duplicate-request costs and all paid review work remain to be reconciled before the budget can be called sufficient.” |
| 2 | “Fully mapped,” observed V distribution and timing of the missing count are misleading. | “Partly addressed. The inventory contains 2,481 audits and 19,627 High and Medium findings. Its eligible-V planning lists use mapping and retention assumptions; the 42-audit subset has at least 80% of findings mapped, not complete mapping. The requested random-protocol fix-scope classification, uncapped eligible-function counts and finite-population simulation with difficulty-dependent construction remain outstanding.” |
| 3 | “Done” hides the mismatch between the decomposition and the declared estimator. | “Partly addressed. Section 6.2 gives an algebraically valid alternative decomposition using the conditional difference \(v_A-v_H\). The generator estimates that difference with weighted working-output denominators. The proposal still needs matching estimator formulas, unresolved-outcome bounds, zero-denominator rules and a statement that the result is standardized across constructible strata rather than a paired rate of newly introduced flaws.” |
| 4 | Omits the unresolved timing of check revisions. | “Partly addressed. The proposal adds author-blind adjudication of checks that endorse a confirmed attacker outcome. It must still distinguish revisions arising before primary locking from audit-assisted revisions made later, so secondary audit access cannot change primary outcomes.” |
| 5 | Claims every allocation’s detection threshold is established. | “Partly addressed. The ‘little difference’ reading is removed. The reported exclusion rates concern selected D scenarios. They do not establish a general smallest detectable distortion for the security component. In particular, the 17-protocol row reaches 0.78 at −0.64, so the file does not demonstrate an 0.80 threshold near −0.65.” |
| 6 | Attributes D calibration to the principal security component and asserts attainment of an untested target. | “Not yet resolved. V23 selects Holm level 0.04 for D and reports validation family-wise error 0.053. It separately reports pointwise security-component intervals with multiplier 1.2 and worst displayed coverage 0.950. It does not validate the security-component family decision at exact security nulls or demonstrate the declared +0.10 target. Larger-effect exclusion rates cannot substitute for that validation.” |
| 7 | Calls the retained-scenario rule complete despite optimistic truncation and missing simulation. | “Partly addressed. The proposal introduces confidence-limit rules, but the lower construction-yield limit must not be raised to 0.7. The nominal 120 evaluations are a maximum before small strata and construction failures. Actual denominators and dependence must inform the limits. The final retained-scenario analysis and a consistent stop-or-launch rule remain required.” |
| 8 | Describes a D example as covering the revised principal comparison. | “Partly addressed. Separate recall assumptions are now mentioned for both RQs. The displayed example and existing formulas concern D. They must be extended explicitly to the standardized conditional security component and its design difference; the −0.47 example is a latent D difference.” |
| 9 | “Upper bounds” and intervals are overgeneralized. | “The requested candidate-level exercise is complete. The recorded matches are Claude 17 of 17 and Codex 13 of 17; excluding the three weak keys gives 14 of 14 and 13 of 14. The displayed Wilson intervals assume independent trials and do not account for protocol clustering. Candidate matches constrain confirmation from those lists, not recall of the future full campaign. Training exposure and executable confirmation remain unresolved.” |
| 13 | Charging work to a reserve is presented as budgeting it. | “Partly addressed. Both requests now receive generation and discovery for the duplicate-request exercise. The added campaigns are charged to the 30-hour coordination reserve, but their full costs and the remaining coordination work have not been reconciled with student and paid ceilings.” |
| 15 | “All answered” hides remaining unknowns and an invalid design-specific probability claim. | “Partly addressed. Appendix B supplies responses to all 13 questions, but named funded personnel, eligible post-cutoff counts and verified audit-missed cases remain unknown. N counts and compute costs are planning assumptions. The empty-stratum calculation is an independent-draw approximation using a modeled zero share, not validation under the proposed finite sampling and construction process.” |
| Disagreement 1 | Treats the revised novelty case as settled. | “The proposed principal contribution has changed. It now requires a consistent empirical contribution statement and a supported precision target; the earlier novelty assessment centered on the design comparison and cannot simply be transferred.” |
| Disagreement 2 | Says C4 is addressed despite unresolved estimand and locking issues. | “Items 3 and 4 improve the design, but matching conditional-rate inference and the timing of functional-check revisions remain unresolved.” |
| Disagreement 3 | Says only human timing remains. | “Human timing remains necessary, but peer-fixable gaps also remain in fixed reservations, duplicate-request costs, frame evidence and principal-analysis validation.” |
| Disagreement 6 | Presents the principal-estimand change as compliance with the AC. | “We propose RQ1b as principal and RQ1a as secondary. This is a departure from the iteration-3 AC’s explicit resolution, not an already accepted consequence of it. The proposal must justify the departure and demonstrate the new target.” |
| Disagreement 7 | Claims the existing bounds cover the new principal analysis. | “D bounds remain specified. Bounds for the principal conditional security rates, including uncertain working denominators, still need to be defined and validated.” |
| Disagreement 8 | Says the requested frame count is done. | “The downloaded-finding inventory is complete. The requested eligible-function audit and finite-population simulation with difficulty-dependent construction remain outstanding.” |

DISAGREE: [R15.1, R15.2, R15.3, R15.4, R15.5, R15.6, R15.7, R15.8, R15.9]