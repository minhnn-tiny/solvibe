## Checks and AC item status

The revision fixes the per-candidate and per-package allowances. It also adds useful evidence on working status and small frames. It does not yet validate the complete procedure that v26 proposes.

I checked the simulation code and recorded outputs without rerunning the simulations. The inventory counts match: **235 audits in 2024 and 78 in 2025**. The severity counts also match: the strict rule retains **50 of 119 High findings** and **81 of 233 Medium findings**, or **50 of 91** and **81 of 163** among findings with determined fix scope.

Intersecting the passing vectors from V40’s base and linked-working groups with V41’s low-V group gives the stated three maximal implementation-rate vectors and the package-rate corner **(0.05, 0.05, 0.2)**. This verifies the calculation, but not the claim that all those results validate the same final estimator.

| AC item | Status | Reason |
|---|---|---|
| 1 | Partly resolved | The unit allowances are corrected, but reserve subsampling lacks a defined estimator and the paid ledger omits required work. |
| 3 | Partly resolved | The margin and its limited usefulness are stated, but validation omits the reversed partial-margin condition and some reported numbers use the superseded estimator. |
| 4 | Partly resolved | The generator correctly links working status to difficulty and allows historical failures; that setting has not been checked with the final V41 estimator. |
| 5 | Resolved | The secondary comparison uses the same functions and reports retained counts, with no unsupported power claim. |
| 6 | Partly resolved | A package mechanism and package-rate region are added, but the development diagnostic remains in implementation units. |
| 7 | Partly resolved | The requested small-frame runs and certainty rule are supplied, but the final estimator differs from the one used in those runs, and the enlarged frame has no reconciled preparation budget. |
| 8 | Resolved | Cut campaigns receive separate cells by author and stratum, extended confirmation and a weighted sensitivity estimate. |
| 9 | Resolved | Development stops for review when sampled V functions yield no constructed task. |
| 10 | Resolved | Gate rediscoveries now require execution and both adjudications within the stated allowances. Their funding remains an item-1 problem. |
| 11 | Resolved | The flagged-only comparison is descriptive, and the small V share is stated. |
| 12 | Resolved | Both requested papers and their relevant distinctions are included. |
| 13 | Partly resolved | Most factual answers are supplied, but the adjudicator ledger remains incomplete and the diagnostic has not been restated as requested. |

Item 2 remains pending from the student and is excluded from this vote.

## Remaining issues

### R25.1 [Blocking] [C4] Reserve subsampling has no defined estimator

**Sections:** 5.7, 6.2 and 8.

The proposal says that remaining candidates are randomly subsampled and that their probabilities “enter the analysis weights.” The principal outcome, however, is whether an **implementation has any confirmed vulnerability**, not the number of confirmed candidates.

An implementation may have several candidates, including candidates for the same flaw. Weighting individual confirmed candidates does not directly estimate that binary outcome. The proposal also leaves “remaining candidates” undefined when a reserve approaches exhaustion before all campaigns finish. The simulation contains neither candidate subsampling nor review subsampling.

**Required change:** Specify and validate a probability-sampling procedure for complete implementation-level candidate bundles, with positive recorded inclusion probabilities, an explicit estimator and variance calculation for the binary implementation outcome, and a reserve rule that can actually execute that procedure.

### R25.2 [Major] [C7] The paid-review ledger omits mandatory packages

**Sections:** 5.9 and 8; rebuttal item 1.

The listed sources require approximately **194.46 hours per adjudicator**, consistent with the rounded 194.5. That leaves about **0.54 hours** under the 195-hour ceiling.

The separate discovery gate now requires both adjudications. Even its five successful rediscoveries require **2.5 hours per adjudicator**, before unsuccessful assessments or the permitted second gate. There is no gate row. The audit-assisted row funds 22 main tasks, but the development procedure also includes audit-assisted work.

The main reservation inequality has a smaller inconsistency: its stated inputs give about **920.2 hours**, exceeding its literal ceiling of 920.

**Required change:** Replace the resource tables with one reconciled ledger that includes gate assessments, the permitted gate revision and development audit-assisted packages, uses executable whole-package reservations, and sets student and adjudicator ceilings consistent with those totals.

### R25.3 [Major] [C6] The passing region combines different estimators

**Section:** 6.3; rebuttal items 4, 7 and 9.

V40 uses `ZERO_SHARE=True` and `VACUOUS=False`. V41 uses both rules but restricts `GROUPS` to `"low V yield"`.

Thus V40’s base and linked-working results do not validate v26’s final rule for author-strata with no working or unresolved implementation. This is not merely a theoretical distinction: V40 reports undefined shares of **0.00125** and **0.00250** in those groups.

The statement that the retained region passes every frame group combines V40 results for one estimator with V41 results for another. Moreover, the new runs retain only the independent and protocol mechanisms alongside the package mechanism. Earlier checks of the other mechanisms used older estimator settings.

**Required change:** Validate one frozen final estimator across all retained frame groups and unresolved-outcome mechanisms, and derive the retained region from that common procedure.

### R25.4 [Major] [C6] The package diagnostic requested by the AC is still absent

**Sections:** 6.3, Appendix B and development decision step 8; rebuttal item 6.

AC item 6 and disagreement resolution 7 explicitly require the development diagnostic to be restated in units per package. The rebuttal instead says: “The diagnostic stays in implementation units.”

Reporting package counts alongside the old diagnostic does not meet that requirement. Its denominator remains scheduled implementation outcomes, so it can dilute a high failure rate among the relatively few packages requiring review.

The simulation also uses a restricted package model: `masks()` applies unresolved status only where `hy` or `ay` is true. It therefore models one detected-positive outcome per implementation, not the full set of submitted packages, including rejected candidates.

**Required change:** Define and evaluate a package-based development warning with explicit package eligibility, author-specific denominators, zero-package handling and a stated launch decision, while identifying the detected-positive-only simulation as a simplifying assumption.

### R25.5 [Major] [C6] Validation of the new margin test is incomplete

**Section:** 6.3, “Reading of the upper limit”; rebuttal item 3.

The code checks reading error only for `READERR = [4, 5]`: **(+0.05, +0.05)** and **(+0.05, 0)**. It omits **(0, +0.05)**.

The proposal correctly refuses to assume configuration exchangeability when choosing the power region. The same standard must apply here. The code also computes reading errors at other conditions but excludes them from the reported reading-error maximum. No argument establishes that the two selected boundary conditions are least favourable for this estimated-bound procedure.

The reported **0.0323** therefore supports the tested conditions, not the full stated null that a configuration’s true difference is at least +0.05.

**Required change:** Validate the margin decision under both ordered partial-margin conditions and the retained above-margin conditions, with Bonferroni counts covering those checks, and limit the error-control claim to that validated scope.

### R25.6 [Major] [C6] The final-frame acceptance rules still omit the added settings

**Section:** 6.3, “Final check on the frozen frame.”

The introductory paragraph adds the 64 package vectors and the new margin conditions. But the binding error, coverage and power bullets still refer to “all four mechanisms” and “all six conditions.” The replacement-calibration paragraph repeats that older scope.

This leaves package failures outside the explicit acceptance rule. It also leaves unclear whether replacement calibration must preserve validity for the new conditions and final empty-denominator rules.

**Required change:** Replace the acceptance and replacement-calibration text with one explicit check matrix covering every retained mechanism, its vector set, every applicable condition, both estimator rules and the margin decision, with counts recomputed from that matrix.

### R25.7 [Major] [C7] Enlarging the frame has not been costed

**Sections:** 5.1 and 8; development kit step 0 and S1.

The frame expands from the previously listed 70 audits to an expected 230 usable audits. Before drawing development protocols, step 0 requires eligible N counts for the whole frame. S1 allows **2–4 hours per protocol** for mapping.

If that allowance applies to the expanded frame, even its lower end requires about **460 hours**, exceeding the shared **220-hour** ceiling before unexposed construction and validation support. If automated enumeration substantially reduces this work, the proposal needs a separate allowance for enumeration, exclusions and human checks. The current ledger does not make that distinction.

This is a budgeting problem the peers can specify without supplying the student’s missing timed case.

**Required change:** Add a capped preparation ledger for the entire expanded frame, separating automated counting from human scope and eligibility checks, and reconcile it with the paid ceiling before step 0 begins.

### R25.8 [Minor] [C4] Several summaries mix superseded and retained results

**Sections:** 6.3; rebuttal items 3, 6 and 9.

The low-V V40 procedure fails coverage and is replaced by V41. Yet several headline ranges still include its values.

For the currently cited combination—V40 base and linked-working groups, plus V41 low-V—the summaries should read:

| Quantity | Current text | Correct summary for that combination |
|---|---:|---:|
| Lowest power at +0.10 | 0.403–0.417 | **0.408–0.417** |
| Lowest power at +0.05 | 0.103–0.114 | **0.106–0.114** |
| Lowest null reading frequency | 0.085–0.104 | **0.090–0.104** |
| Median null reading frequency | about 0.21–0.23 | **0.222–0.230** |
| Mean half-width at +0.15 | 0.088–0.116 | **0.088–0.115** |
| Power lower bound at package rates (0.1, 0.1, 0.1) | 0.557–0.594 | **0.573–0.594** |

The reading frequencies are minima of the two configurations’ marginal claim frequencies within each frame. They are not the probability that both claims occur in the same study.

Rebuttal item 9 also attributes the approximately 7% undefined share to V41; it belongs to V40. V41 reports zero undefined estimates.

**Required change:** Rewrite these summaries and rebuttal rows using explicitly identified retained runs, label the reading-frequency aggregation, and attribute the undefined-estimate finding to V40.

### R25.9 [Minor] [C4] The frame and certainty conclusions exceed the evidence

**Sections:** 5.1, 6.3 and Appendix A; rebuttal item 7 and “Disagreements and choices.”

Three statements need narrower wording:

- “The design therefore needs a frame of about 200 protocols or more” does not follow from runs at 50, 70 and 230, especially because the estimator rules also changed.
- The claim that deleting certainty protocols “errs toward wider intervals” is not established generally by a failed alternative in a small test.
- The 313 inventory count filters firms, years and Solidity signals. It does not establish 313 **contest** audits. The frame-audit evidence explicitly includes Cantina private reviews.

The V39 small-frame summary also gives coverage down to 0.941 without stating that this excludes its low-V results, whose recorded coverage bounds reach approximately 0.710.

**Required change:** Rewrite these passages as statements about the specific tested configurations, distinguish private reviews from contests, and report or explicitly exclude the low-V small-frame results.

The pending student commitment and timed case remain necessary. They would not resolve the estimator, validation and ledger issues above.

DISAGREE: [R25.1, R25.2, R25.3, R25.4, R25.5, R25.6, R25.7]