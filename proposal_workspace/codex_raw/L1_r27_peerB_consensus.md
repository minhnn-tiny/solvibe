## Status of the round-26 issues

**R26.1: not resolved.** V43 is a useful stress test, and its reported results are reproducible from the saved tables. However, it does not implement the declared outcome rules or the full S1 validation scope. Its workload model also suppresses an important source of demand variation.

**R26.2: resolved in principle, but not consistently implemented.** Recording an unassessable warning without automatically blocking launch is reasonable. It supplies no evidence either way. Section 8’s decision step 8 and rebuttal item 6 still contain the opposite instruction.

The measured-demand launch condition is not yet executable. “Less favourable 80% limits” has no defined calculation, and the rule does not handle absent, unfinished or selectively observed confirmations.

## V43 implementation audit

| S1 component | What V43 does | Assessment |
|---|---|---|
| Fixed design and estimator settings | Uses the V42 frames, allocation, construction groups, Holm 0.03 and multiplier 1.175. | Matches the requested starting point. |
| Candidate multiplicity | Positive implementations receive one or three candidates, with one confirming candidate at a uniform position. | A useful specified model, but not evidence covering all candidate mixtures or ordering rules. |
| Rejected candidates | Sets their Binomial probability separately in each simulated sample to offset that sample’s positive-candidate count. | Material deviation. This makes rejected demand fall when positive demand rises. |
| Infeasible pilot rates | Sets the rejected-candidate probability to zero and records infeasibility without removing positives. | Correctly preserves positives. Such rows must not be described as realizing the pilot candidate rate. |
| Bundle admission | Checks the full allowance before starting each randomly ordered bundle and stops at the first bundle that cannot fit. | Matches S1. |
| Positive stopping | Stops confirmation at the confirming candidate. | Changes the full-bundle procedure unless explicitly adopted. The remaining candidate records need defined statuses. |
| Released reservations | Returns unused reservation to the source reserve. | Potentially reasonable, but it needs one consistent operational rule and matching ledger instructions. |
| Review demand | Produces exactly one review package per processed positive and none from rejected candidates. | A simplifying assumption. It does not exercise erroneous or inconclusive packages submitted for adjudication. |
| Known working status | Passes reserve failures into V42’s generic unresolved mask. | Does **not** preserve known working status in the estimator. |
| Observable warning | Uses registered candidate records as the denominator, but constructs unfinished counts from implementation-level masks. | Denominator improvement is real; the numerator does not consistently follow candidate-record completion. |
| Combined mechanisms | Combines exhaustion with two implementation-region corners and one package corner. | Useful corner stress tests, not validation across the requested grids. |
| Conditions | Checks the global null, both +0.10 partial nulls and equal +0.15. | Omits the margin conditions, negative alternative and other coverage conditions. It does not evaluate reading-test error. |
| Multiplicity | Uses 1,800 error, 4,800 coverage and 1,200 power checks per workload scenario. | These counts match the checks actually run. They do not cover omitted checks. |
| Development summaries | Simulates three-protocol samples at the exact null. Samples with no built function are skipped. | Empty samples should be counted and reported, not silently removed from the diagnostic denominator. |

## Numerical checks

The following v28 figures match the recorded results:

- Worst error upper bound: **0.0424**.
- Worst coverage lower bound: **0.9569**.
- Worst undefined-estimate share: **0**.
- **10 of 12** workload scenarios pass all their tested combinations.
- Across passing scenarios’ tested mechanism corners, power lower bounds range from **0.6165 to 0.6555**, supporting the rounded **0.617–0.656**.
- The two failing scenarios have power from **0.2452 to 0.3380**, with lower bounds from **0.2191 to 0.3089**.
- Their pooled confirmation-exhaustion frequency at +0.15 is **0.442**.
- The largest corresponding exhaustion frequency among passing scenarios is **0.094**.
- The largest reported development warning frequency is **0.0606**.
- Development unassessability ranges from **0.014 to 0.279**.

Two qualifications are necessary:

1. The **0.842** infeasibility frequency for the 8/64 target applies to **one-candidate positive bundles**. For three-candidate positive bundles, it is **1.000** at +0.15. The proposal’s unqualified “84%” statement omits that distinction.
2. Warning frequencies near **35%–37%** are pooled frequencies in the high-demand scenarios. They are not probabilities conditional on the reserve having run out.

The phrase “power holds unless…” is too broad. The results establish that ten specified workload scenarios pass the tested combinations. They do not establish that the two failing scenarios exhaust all ways power can fail.

## Remaining issues

### R27.1 [Major] [C4] Reserve exhaustion does not preserve known working status

**Sections:** 6.2 and 6.3; `power_sim_v43.py::job` and `power_sim_v42.py::evaluate`.

V43 delegates estimation to V42 after combining reserve failures with the generic unresolved mask. V42 computes, for example:

```python
Hw = S(hw & ~hu)
Hu = S(hu)
```

Its conditional-rate denominator then includes `Hw + Hu`. Thus a known non-working implementation with an unfinished rejected-candidate bundle can enter the admissible working denominator and vulnerable numerator.

This contradicts the proposal’s rule that a known functional failure retains \((W,D)=(0,0)\). The same masking also affects working counts used by the widening adjustment.

**Required change:** Implement separate masks for unknown functionality and unfinished security assessment, preserving observed W and established positives throughout bounds, jackknife replicates and widening calculations, then rerun validation.

### R27.2 [Major] [C4] The simulated stopping policy is not fully specified in the study procedure

**Sections:** 5.7, 6.3 and the development kit.

V43 stops a positive bundle at its confirming candidate and returns unused reservation. Section 5.7 does not specify this stopping point or the status of its remaining registered candidates.

It also matters whether “confirming” means the student has produced a plausible package or both adjudicators have confirmed it. V43 knows the candidate’s true status before the later review step. A real procedure cannot use that knowledge.

The kit still says time saved cannot move to another implementation. Its closing rules also classify a candidate stopped by the confirmation cap as “not confirmed,” contrary to section 6.2.

**Required change:** Freeze one executable confirmation-and-review state machine, including the observable stopping event, release of reservations and treatment of remaining candidates, and make the simulator, proposal and kit implement it identically.

### R27.3 [Major] [C6] Workload is recalibrated using each sample’s realized positives

**Section:** 6.3; `power_sim_v43.py::exhaust`.

The code sets

\[
p=\frac{RM-k_{\mathrm{pos}}n_{\mathrm{pos}}}{3n_{\mathrm{neg}}}
\]

inside each simulated sample.

Consequently, a sample with more positive candidates receives fewer expected rejected candidates. This holds total expected demand near the target whenever feasible. It removes part of the workload variation that matters when studying reserve exhaustion.

Recording infeasible samples is appropriate, but does not address this dependence in feasible samples.

**Required change:** Calibrate the rejected-candidate distribution once per declared generating scenario, independently of each realized study sample, and rerun the reserve checks with that fixed workload model.

### R27.4 [Major] [C6] The reserve procedure lacks the requested validity checks

**Section:** 6.3; `CONDS` and `COMBOS` in V43.

V43 checks only four conditions and ten mechanism combinations. It omits the full ordered grids, negative-alternative coverage and every direct check of the margin-reading decision.

V42 cannot supply those missing results for the changed reserve procedure. Nor does passing corner checks establish validity at all interior or outside-region vectors.

The final-frame check may remain pending until the frame is frozen. That does not make the current claim that the reserve procedure has been validated accurate.

**Required change:** Complete the prototype reserve validation using the full section 6.3 check matrix, including margin-reading error, while requiring power only within the retained region.

### R27.5 [Major] [C6] The warning numerator does not track actual unfinished records

**Section:** 6.3; `scenario_masks()`.

The denominator counts all registered candidates. But the numerator:

- counts every candidate in an unstarted bundle;
- counts only one record for an unreviewed positive package;
- counts one or all records when an added implementation-level mechanism fires;
- does not explicitly account for candidates left unprocessed after an early positive stop.

These are different events. An implementation-level failure does not by itself identify which candidate assessments remain unfinished. A completed positive may also make further work unnecessary, which requires a defined terminal status rather than silently diluting the warning denominator.

**Required change:** Generate and retain candidate-level terminal statuses, and compute the warning directly from the same observable status definitions used in the study records.

### R27.6 [Major] [C6] The measured-demand launch rule is undefined and selectively informed

**Sections:** 6.3, “Launch condition on measured demand”; development step 8a.

The proposal requires a rerun with measured values and their “less favourable 80% limits.” It does not specify:

- which parameters receive limits;
- how clustering and the small development sample enter;
- how limits are combined;
- what happens when an author has no confirmed flaw;
- how unfinished or unreviewed candidates contribute;
- how the allowed reserve increase is selected within the remaining budget.

Using only implementations with confirmed flaws also selects observations that survived the confirmation and review process. They may underrepresent expensive positive bundles.

Allowing an unassessable warning is reasonable, but it makes the no-confirmation case especially important here.

**Required change:** Replace the sentence with a preregistered demand-selection algorithm that includes unfinished observations, explicit zero-information cases, a defined uncertainty set and a fixed budget-constrained reserve-selection rule.

### R27.7 [Minor] [C4] Launch instructions and status statements contradict each other

**Sections:** 8, Appendix A; rebuttal item 6 and introductory paragraphs.

Section 6.3 permits launch with an unassessable warning. Section 8 step 8 still says an author with no registered candidate prevents launch. Rebuttal item 6 contains both instructions in the same row.

Appendix A adds V43 as current reserve evidence but retains a separate “Reserve procedure — Pending” row without explaining the remaining scope. The rebuttal introduction and earlier explanatory paragraphs likewise retain the round-26 pending text while later claiming exact validation.

**Required change:** Synchronize the proposal, rebuttal and kit around the intended no-automatic-stop rule and an explicit account of which reserve checks are completed and which remain outstanding.

### R27.8 [Minor] [C4] Result summaries overstate their scope

**Sections:** 3, 6.3, Appendix B; rebuttal items 1 and 6 and final status.

The quoted numerical ranges mostly match the files, but several sentences change their meaning:

- “84%” omits the three-candidate scenarios’ infeasibility;
- “when the reserve runs out” reads as a conditional warning probability;
- “power holds unless…” generalizes beyond the twelve workload scenarios;
- “exact reserve procedure” overlooks the implementation differences above.

**Required change:** Replace these summaries with scenario-qualified statements, explicitly labeling pooled frequencies, infeasible-rate scenarios and the limited validation domain.

The student evidence remains excluded from this vote. I am also not treating the scheduled final-frame check itself as a defect. The unresolved issues concern the procedure being claimed as validated now.

DISAGREE: [R27.1, R27.2, R27.3, R27.4, R27.5, R27.6]