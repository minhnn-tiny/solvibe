I accept Peer A’s proposal-stage standard for C7. Completed development measurements are not a prerequisite. Explicit assumptions, a complete pessimistic budget, a useful minimum deliverable, and a rule for replacing assumptions with measurements can suffice.

V8 substantially improves the proposal, but three Major issues remain. I would no longer retain a Blocking label merely because development work has not started.

## Status of the previous concerns

| Concern | Judgment |
|---|---|
| Feasibility | Improved; **Major remains** because the validation allocation does not support the stated precision target. |
| RQ1 inference and paper-2 power | Partly resolved; **Major issues remain** in equivalence validation and the paper-2 outcome definition. |
| Audit-blind discovery not demonstrated | **Resolved at proposal stage.** Sections 5.4–5.9 specify separation, independent campaigns, validation, and an early demonstration. Actual performance remains a research risk. |
| Missing 63008 package | **Resolved at proposal stage.** Section 5.11 explicitly identifies the missing evidence, and section 8 prohibits treating the case as validated until it meets the standard. Completing it can reasonably be an early milestone. |

## Remaining issues

### R7.1 [Major] [C7] The budget does not yet cover the promised validation

**Sections:** 5.9 and 8.

**Evidence:** Section 5.9 targets a “95% interval half-width of 0.05 for the paired recall difference,” with results separated by stratum and configuration and uncertainty accounting for clustering. Section 8 instead budgets a fixed **60 seeded artifacts and 30 hours**, without connecting that allocation to the precision requirement.

The student-hour totals add correctly from the displayed rows. However, they establish feasibility only for that fixed validation allocation. They do not establish feasibility for the precision-based validation promised elsewhere.

Even under independent paired observations, precision depends on how often the two implementations’ detection outcomes disagree. Sixty artifacts cannot be assumed to meet the target without specifying those assumptions, the number of complete matched pairs, and allocation across strata and configurations. Clustering adds another consideration.

The table also needs to make clear where development demonstrations, campaign supervision, and failed construction attempts enter the totals. Calendar throughput from assisted pilot work does not directly measure these costs.

**Required change:** Replace the fixed validation allowance with one internally consistent budget scenario that specifies matched-pair allocation, assumed discordance and clustering, attainable precision, and all development and operational labor; either fund that scenario within the pessimistic total or explicitly relax the precision target and associated claims.

This requires a defensible calculation, not completed development cases.

### R7.2 [Major] [C6] Equivalence has not been validated for the declared outcome model

**Section:** 6.3.

**Evidence:** In `power_sim_v9.py`, `false_eq()` tests `d + sh` for shifts of ±0.05 while retaining the zero-effect standard errors. The proposal acknowledges this.

That checks a location-shift approximation. It does not establish false-equivalence control when the binary outcome-generating process actually has a difference of ±0.05. Changing vulnerability rates can change the variance, skewness, pairing, and relationship between estimates and standard errors.

The implementation also takes the maximum **individual configuration’s** false-equivalence rate. It does not validate a family decision permitting equivalence claims for either configuration.

The revised month-two checklist no longer explicitly requires genuine boundary generation or the family-level equivalence check. “The same calibrate-then-validate procedure” could therefore preserve this limitation indefinitely.

For difference testing, the independent-stream implementation is a real improvement. The displayed values match `power_results_v9_partA.txt`. I do **not** regard 0.055 or 0.060 alone as evidence of failure given their Monte Carlo uncertainty. The problem is what was simulated.

The earlier v8 power and interval-width tables also precede the new testing levels and interval multipliers. They must not be read as performance of the revised procedure.

**Required change:** Rewrite the inference commitment so that confirmatory equivalence requires data generated at both actual margin boundaries and validation of the declared family decision, with power and interval widths recomputed for the selected procedure; until then, label the shifted-null results as diagnostic and withhold confirmatory equivalence claims.

### R7.3 [Major] [C4] Paper 2’s simulated outcome differs from its declared primary outcome

**Section:** 6.6 and `power_sim_v9.py`, Part B.

**Evidence:** Section 6.6 declares:

> “The primary security outcome is retention or reproduction of the attributable vulnerability.”

The simulation documentation instead defines the outcome as:

> “keeps or writes the vulnerable or wrong behaviour”

For ordinary assertions, retaining an ordinary incorrect behavior is not necessarily retaining the vulnerability. Comparing vulnerability retention in one assertion condition with ordinary-error retention in the other estimates a different contrast from measuring vulnerability retention across both conditions.

The numerical rejection rates in the proposal match the Part B output. Their interpretation is the unresolved issue.

Furthermore, the only simulated null has both interaction parameters equal to zero. It does not test equal nonzero interactions or other settings where the **probability-scale contrast being tested** is zero. The statement that the test “holds its level under the null” should be limited to the tested scenario.

Finally, 80 functions is not itself a sufficient criterion for a confirmatory study. Its adequacy depends on the declared effect of interest and the chosen outcome. The reported 0.258 power already demonstrates that dependence.

**Required change:** Define one common outcome and its probability-scale contrast across both assertion types, then align the simulation and preregistration with that definition, including relevant zero-contrast scenarios and an effect-based criterion for the confirmatory allocation.

## Minor corrections

- **Scenario count:** Part A generates **six scenarios per protocol count**: three recall patterns times two historical N rates. The two configuration outcomes are not two additional scenarios. Correct “12 null scenarios” in the output and proposal.
- **Result provenance:** The Part A lines in `power_results_v9.txt` differ from the current code’s output and the separate Part A file. Mark them as superseded and identify which code version produced them.
- **Discovery gate:** Section 5.9 triggers revision below three rediscoveries out of eight, but requires at least half after revision. State one consistent acceptance rule and use only cases meeting the applicable confirmation standard in its denominator.

## Whole-proposal assessment

I found no additional Blocking or Major issue under C1–C8. The comparison of sampling designs, restricted historical claim, own-campaign endpoint, explicit threat model, current native agents, separate repair paper, and disclosure procedure should be retained.

The remaining objections concern internal consistency and the scope of statistical evidence. They do not require the student to complete the proposed study before the proposal can be approved.

DISAGREE: [R7.1 validation budget and precision mismatch; R7.2 incomplete equivalence validation; R7.3 paper-2 outcome and simulation mismatch]