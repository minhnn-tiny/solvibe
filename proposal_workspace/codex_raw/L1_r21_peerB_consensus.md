## Status of the round-20 points

| Point | Status | Reason |
|---|---|---|
| R20.1 | Partly resolved | V35 supplies results and a reproducible region, but the configuration-swap argument does not establish coverage of the omitted assignments within each fixed frame. |
| R20.2 | Partly resolved | The flagging rule is explicit. Its claimed confidence-limit interpretation is not established for the planned sampling design. |
| R20.3 | Partly resolved | Development now has a fixed stop rule, with its low sensitivity disclosed. V36 does not validate that rule under the full planning model. |
| R20.4 | Resolved, with a Minor clarification | Completed disagreement can mean failure to meet a two-adjudicator confirmation standard. An unfinished or inconclusive assessment must remain unresolved. |
| R20.5 | Resolved | RQ1a is now descriptive. Its simulated precision does not support a directional comparison. |
| Pending C6 concern | Not resolved | The operating region and monitoring claims need the corrections below. |

The structural change is sound in principle: development checks execution and cost; power remains conditional on stated assumptions; monitoring cannot change the sample or analysis. This is an explicit departure requiring committee approval. Weak monitoring alone does not invalidate that design, provided it is not presented as certification that the assumptions hold.

## Evidence and code checks

The V35 power table, maximal-vector table, error bound **0.0405**, coverage bound **0.9573**, and undefined share **0.00100** agree with the result files. The V36 table also agrees with its recorded results.

The following implementation details check out:

- V35 implements independent, function-shared, protocol-shared and difficulty-dependent unresolved outcomes. The difficulty thresholds are calibrated over built functions in each frame.
- The sampled functions and underlying outcomes are shared across mechanisms and rate vectors. Independent and difficulty-dependent masks reuse implementation-level uniforms; the other mechanisms use their own shared uniforms.
- Storing `sh` in V29 adds no random draw.
- The reported Bonferroni counts are correct **per mechanism**: \(3\times49\times24=3,528\), \(6\times49\times24\times2=14,112\), and \(49\times24\times2=2,352\). These are separate confidence families, not one joint 95% certificate across all mechanisms and criteria.
- The downward-closure calculation implements the stated rule on the reduced grid, subject to the symmetry problem below.
- The revised undefined diagnostic checks both bounds, both standard errors and both widening terms.
- RQ1a uses the difference between the stratum contrasts, estimated constructible shares and a joint delete-one-protocol calculation. Its multiplier is correctly described as uncalibrated for RQ1a.
- The development kit now uses one V function, six N functions and two attempts per configuration. Its student-stage caps match the proposal.

I checked the code and recorded results without rerunning the simulations.

## Remaining issues

### R21.1 [Major] [C6] Configuration symmetry does not hold exactly within the fixed frames

**Section:** 6.3, V35; rebuttal’s operating-region claims.

**Problem:** The proposal says that “a vector and its configuration swap are equivalent” because the configurations are generated in the same way. This is true as a distributional statement before generating a frame. It is not an exact symmetry conditional on the realized frame.

**Evidence:** In `power_sim_v29.py`, `Frame.__init__` generates separate random latent arrays for the two configurations. Those arrays remain fixed across studies. Setting their mean contrasts to the same target does not make their function-level vulnerability probabilities identical. V35 nevertheless simulates only `u_A1 <= u_A2` and extends the resulting region by swapping coordinates. Running both partial-null assignments does not supply the omitted rate assignments at the global null or the power alternatives.

**Required change:** Rerun V35 with every ordered agent-rate assignment on each fixed frame, update the check counts, and derive the operating region from those results without the symmetry shortcut.

### R21.2 [Major] [C4, C6] V36 does not establish a lower confidence limit for the study’s population rate

**Section:** 6.3, V36; rebuttal’s monitoring description.

**Problem:** The claim that division by the largest outcome count makes the limit “err toward low values” has a narrower justification than the proposal states.

**Evidence:** `monitor_oc_v36.py` gives every protocol the same built-function count and every outcome of an author the same marginal unresolved probability. It does not implement the finite frame, unequal inclusion probabilities, variable construction yields or difficulty-dependent rates. Its protocol failures are also drawn separately for each author, whereas V35 shares one protocol draw across authors.

The union-bound argument is valid under the homogeneous model used by V36. It does not establish that an unweighted binomial limit on selected protocols is a confidence limit for the function-weighted constructible-domain rate under the actual design. Counting protocols addresses within-protocol dependence; it does not establish the remaining sampling and weighting assumptions.

**Required change:** Validate the flagging rule within the V35 sampling and outcome generator under all four mechanisms, reporting it as a calibrated diagnostic rather than an exact population confidence limit unless that stronger property is established.

The disclosed low sensitivity is not itself a new rejection reason. In particular, the proposal correctly says that a rule that does not fire is not evidence that the study lies inside the region.

### R21.3 [Major] [C7] The retained construction-confidence gate conflicts with the fixed development sample

**Section:** 5.2 and 8.

**Problem:** Section 5.2 retains a launch gate based on a construction-yield lower confidence limit of at least 0.7. The revised development design supplies at most three V functions. The interval method and confidence level are unspecified.

**Evidence:** The proposal says:

> “Construction yield is reported by stratum. A lower confidence limit below 0.7 prevents launch…”

It also fixes three development protocols with at most one V function each. Even with all three successfully constructed, a one-sided exact binomial lower limit is only \(0.05^{1/3}\approx0.368\) at 95% confidence, or \(0.20^{1/3}\approx0.585\) at 80% confidence. This problem exists even under independent construction outcomes. Additional agent attempts do not add construction observations.

This is a design inconsistency, separate from the student’s pending timed case.

**Required change:** Replace the construction-confidence launch gate with a fixed-case operational check and descriptive construction yields, explicitly requesting committee approval to make the construction assumptions conditional planning assumptions rather than quantities certified by three development cases.

### R21.4 [Minor] [C4] Distinguish completed rejection from inconclusive adjudication

**Section:** 6.2, unresolved-outcome table.

**Problem:** “They still disagree” needs a precise decision definition.

**Evidence:** The primary endpoint requires two positive adjudications. Two completed substantive decisions that fail to supply joint confirmation can therefore produce “not confirmed” without asserting that the implementation is safe. That rule is symmetric between authors and fits the stated detector-based endpoint.

However, an adjudicator who cannot assess attribution, lacks required evidence or stops at the cap has not supplied a completed rejection. Such a case belongs in the primary adverse bounds.

**Required change:** Define the disagreement row to cover only two completed substantive decisions, and explicitly classify any inconclusive or incomplete required assessment as unresolved in the primary analysis.

### R21.5 [Minor] [C4, C6] The continuous region exceeds the demonstrated grid result

**Section:** 6.3, “Frozen region”; Appendix B; rebuttal.

**Problem:** The text states that power “holds” whenever rates are below the maximal vectors, then acknowledges that only a grid was tested.

**Evidence:** The code makes the passing set downward-closed over **tested vectors**. It does not prove monotonicity of rejection probability for the full procedure between grid points. Adverse bounds widen with added unresolved observations, but the estimated standard errors, zero-detection adjustment and Holm decision also change.

**Required change:** Describe the continuous downward extension as a planning assumption, while reserving the validated-power statement for the tested rate vectors.

### R21.6 [Minor] [C6] Two RQ1a statements need updating

**Section:** 5.2 and 6.4.

**Problem:** Section 5.2 still says the allocation’s effect on RQ1a precision “remains unmeasured.” Section 6.4 gives the no-unresolved maximum mean half-width as 0.63.

**Evidence:** V35 now measures that precision. Its results report a maximum of **0.635** without unresolved outcomes, under the exact +0.15 condition, and **0.710** overall. The coverage range **0.933–0.947** is correctly reported.

**Required change:** Replace these statements with the V35 values, retaining three decimal places and the restriction to the independent mechanism.

### R21.7 [Minor] [C6] The rebuttal and development instructions contain stale descriptions

**Section:** Rebuttal rows 2, 7 and 14; disagreement 8; development kit.

**Problem:** Parts of the rebuttal still describe completed V35 work as future work. The kit points to v21 and omits the new adjudication closing rule.

**Evidence:**

- Row 2: “The next check separates authors…”
- Row 7: “The largest passing regions… will be reported…”
- Row 14: “The undefined diagnostic must include…”
- Disagreement 8: “The next simulation… adds separate agent rates…”
- `dev_case/README.md` references v21 and does not distinguish completed disagreement from an unresolved assessment.

**Required change:** Synchronize these passages with the corrected v22 evidence and rules, identifying completed V35 work, remaining validation, and the exact development decision procedure.

The major remaining concerns concern validation and an unattainable retained gate. They do not concern the absence of item 10, which remains excluded from this vote.

DISAGREE: [R21.1, R21.2, R21.3]