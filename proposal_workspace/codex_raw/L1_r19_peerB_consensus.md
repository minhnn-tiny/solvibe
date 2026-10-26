## Status of the agenda

| Point | Status | Judgment |
|---|---|---|
| R18.1 | Mostly resolved | V33 calibrates on every listed condition, uses fresh validation draws, has no fallback setting, and implements the zero-detection adjustment. Its numerical results support the stated planning-model error and coverage claims. The adjustment is not an exact confidence bound for clustered, weighted observations, however. |
| R18.2 | Not resolved | Changing the allocation and development attempt count is structurally different. But the pooled development limit does not bound author-specific unresolved rates, and repeated attempts do not supply independent evidence about shared failures. The proposed launch implication is therefore unsupported. |
| R18.3 | Resolved | The text distinguishes the simulated negative targets, approximately −0.045 to −0.011, from the −0.05 target attainable in eight frames. |
| Earlier C6 validation concern | Resolved for the tested planning model | V33 supplies the requested combined calibration and independent validation. This does not validate the new rule that converts development outcomes into retained scenarios. That is the remaining substantive gap. |

## Numerical and implementation checks

The reported V30–V33 simulation results match the result files and frame tables. The code implements the stated grid selection and uses separate calibration and validation seeds.

For each V33 design, the Bonferroni counts are correct:

- **216 error checks:** 24 frames × nine null conditions.
- **1,008 coverage checks:** 24 frames × 21 conditions × two configurations.
- **384 power checks:** 24 frames × eight +0.15 conditions × two configurations.

For the preferred allocation, the reported level **0.03**, multiplier **1.175**, error upper bound **0.0386**, coverage lower bound **0.9581**, and power table agree with the files. Undefined intervals count as coverage failures. The zero-detection terms affect intervals but not directional decisions, as the text states.

The cost arithmetic also matches:

- Main allocation: \(22(9+7\times2.25+35\times0.328+3.75)=879.56\) hours, reported as **880**.
- Per-protocol low and high costs round to **24.7** and **57.1** hours.
- Development expression: \(3(9+8\times2.25+72\times0.328+3.75)=163.098\) hours.

The development total is arithmetically correct **for that expression**. The kit prescribes additional or differently limited work, discussed below.

The zero-event calculations of **0.0074 from 216**, **214 as the minimum denominator**, and approximately **0.065 from 24 historical outcomes** are correct under their independent-binomial assumptions. Those assumptions do not justify the proposed pooling rule.

The V32 cost correction is necessary and correctly reflected in V33. Its frame CSV contains no validation rows because none of its screened designs passed the screening threshold.

## Remaining issues

### R19.1 [Blocking] [C4, C6] The pooled limit does not support the author-specific readiness scenarios

**Section:** 6.3, “Readiness scenarios”; rebuttal, disagreement 7.

**Problem:** Development contributes at most 24 historical outcomes and 192 agent outcomes. A pooled rate gives historical failures only one-ninth of the weight. Placing the pooled limit on historical outcomes alone does not place the “whole” uncertainty on that author.

For example, under independent outcomes, a historical unresolved rate of 0.06 and an agent rate of zero produce a pooled rate below 0.0075. Yet the historical rate is far outside the retained historical-only scenario. Even observing no historical failures has probability \(0.94^{24}\), approximately 0.227, under that example.

The proposal acknowledges the historical upper limit of about 0.065 but dismisses it as reflecting sample size. That uncertainty is precisely what readiness must retain. Additional agent attempts cannot remove it.

**Required change:** Replace the pooled-to-author mapping with a justified joint uncertainty region for author-specific unresolved rates, and require the allocation to pass throughout that region.

### R19.2 [Major] [C6] Repeated attempts do not establish the claimed development precision

**Section:** 6.3, development denominator and dependence rule.

**Problem:** The expression \(1-0.2^{1/216}\) treats outcomes as independent trials. The 216 outcomes share only 24 task constructions and three protocol environments. Build, harness, property and adjudication problems can affect several implementations together.

Increasing attempts from two to four measures additional run-level failures. It does not double independent evidence about these shared failures. The sentence requiring “conservative dependence assumptions” does not specify a usable limit or show that the launch condition remains attainable.

There is also a transfer problem: development has two V functions and four attempts per configuration, while the main study has one V function and two attempts. Pooling without a model does not account for the different author and stratum mixtures.

**Required change:** Specify and evaluate a development-to-main uncertainty model that separates shared protocol and task failures from attempt-level failures and preserves the main study’s author and stratum composition.

### R19.3 [Major] [C6] The extension after one unresolved outcome changes the confidence procedure

**Section:** 6.3, paragraph beginning “One unresolved outcome needs at least 399 outcomes.”

**Problem:** The proposal first allows launch after zero unresolved outcomes, then adds observations after one unresolved outcome and applies another fixed-sample limit. The complete stopping rule is not covered by either fixed-sample confidence statement.

Even under independent, identically distributed outcomes, at unresolved probability 0.0075 the probability of passing either branch is approximately

\[
(1-0.0075)^{216}
+
216(0.0075)(1-0.0075)^{398}
=
0.278.
\]

This exceeds the 0.20 error probability associated with the stated upper 80% limit. This calculation already assumes only the two prescribed looks; repeated checking would need further treatment.

**Required change:** Replace the adaptive extension with a preregistered fixed sample or a sequentially valid upper-confidence procedure, and validate the complete stopping rule.

### R19.4 [Major] [C7] The development kit does not implement the budgeted campaign procedure

**Section:** 8; `dev_case/README.md`, steps S5–S10.

**Problem:** The 163-hour expression charges each development campaign a total of 0.328 student hours. The kit instead permits supervision of 0.1–0.2 hours per campaign plus **0.5–1.5 hours per candidate**, without stating the proposal’s combined campaign cap.

The expression also reserves 3.75 hours of audit-assisted work per case. The kit instructs the student to perform that work for **each V function**, with two V functions sampled and an allowance of 2.5–5 hours per function.

Thus the kit can produce resolved outcomes under a more generous procedure than the main study. Those outcomes would not establish the main procedure’s unresolved rate. The claim that only 13 hours spill into month two also leaves the other month-one activities outside that calculation.

**Required change:** Replace the kit’s allowance table and the development ledger with one consistent, stage-capped schedule covering every prescribed task within the combined month-one and month-two reservations.

### R19.5 [Minor] [C4] The zero-detection adjustment is not exact for this sampling design

**Section:** 6.3, zero-detection rule; rebuttal, structural changes and disagreement 2.

**Problem:** \(1-0.025^{1/n}\) is the exact zero-event upper limit for independent Bernoulli trials with a common probability. Here observations have unequal inclusion weights, shared task and protocol effects, and repeated agent attempts.

The code implements the stated widening formula, and V33 validates the resulting interval empirically on its tested frames. That supports calling it a calibrated adjustment. It does not support calling it an exact upper limit for the study’s weighted rate.

**Required change:** Describe the term as a binomial-based widening adjustment whose coverage support comes from the combined simulation, rather than as an exact bound for the study estimand.

### R19.6 [Minor] [C4] The undefined-interval diagnostic omits the new widening terms

**Section:** Appendix B; `power_sim_v32.py`, `cover()`.

**Problem:** Coverage uses all six returned quantities, but the undefined-share calculation checks only `R[:4]`. A nonfinite `zL` or `zU` therefore makes an interval undefined without necessarily appearing in the reported undefined share.

This does not falsely improve coverage: the comparison still fails. It does make the diagnostic incomplete.

**Required change:** Compute the undefined-interval share from all quantities used to form the interval, including both widening terms.

### R19.7 [Minor] [C4] RQ1a statements still mix the old and new allocations

**Section:** 6.4; rebuttal, “Proposed changes in principal estimand and power requirement.”

**Problem:** The rebuttal calls V27’s 0.338 half-width a result “for the proposed allocation.” It belongs to the earlier 20-protocol allocation with two V functions.

Section 6.4 also says the new interval “will be wider.” Reducing V per protocol while increasing protocols suggests a precision tradeoff, but does not prove that ordering. The proposal correctly acknowledges that V33 does not measure it.

The V cap of one is otherwise defensible for the principal comparison under the tested frames. It reduces information for V-stratum estimates and RQ1a, which must remain explicitly unvalidated.

**Required change:** Label the V27 results as belonging to the earlier allocation and replace the asserted interval ordering with a statement that the new RQ1a precision has not been measured.

### R19.8 [Minor] [C4] The zero-unresolved requirement is stated inconsistently

**Section:** Abstract, 6.3, 8, development kit and rebuttal.

**Problem:** The abstract says development must find no unresolved outcome among 216. Section 6.3 permits at least 214 outcomes and also permits an extension after one unresolved outcome. The kit and rebuttal repeatedly present zero unresolved outcomes as an absolute requirement.

Moreover, 214 outcomes from the initial design effectively requires all 24 tasks to be constructed: losing one task removes nine outcomes. This stringent condition should be explicit rather than hidden in the denominator.

**Required change:** After correcting the statistical gate, state one identical launch rule across the proposal, rebuttal and kit, including construction failures and any permitted extension.

## Overall judgment

The allocation change is a genuine structural revision. V33 resolves the earlier simulation-calibration concern within its stated model, and the arithmetic supports its reported planning costs. The remaining obstacle is the link between development evidence and that model. A zero-unresolved gate is not inherently unsound, but its confidence claim must account for author differences, shared failures and stopping.

Item 10 remains pending and is excluded from this vote.

DISAGREE: [R19.1, R19.2, R19.3, R19.4]