M2 is substantially resolved. M1 remains unresolved for protocols the student already knows. The revision also introduces an incomplete cost rule for increasing the V allocation.

## Agenda status

| Point | Status | Reason |
|---|---|---|
| **M1: assignment of audit-blind work** | **Not resolved** | The second person first reads findings and checks labels, then performs blind construction for previously known protocols. That person is no longer audit-blind for those protocols. |
| **M2: design-comparison precision** | **Resolved** | The generator now computes the paired design difference and its jackknife error. Independent calibration, reported precision, and conditional allocation planning address the missing evidence. Two reporting and budgeting issues remain below. |
| **m1: header** | **Resolved** | The header identifies the current author and round and attributes v9 to Peer B. |
| **m2: pilot V rate** | **Partly resolved** | The 16-of-32 count is correct, but “one request style” misdescribes the pilot, and code-reading results do not directly establish the expected difference for the new endpoint. |

## Simulation audit

I checked the code and recorded outputs without rerunning the simulations.

- The added `parts` and `max_v` arguments preserve the earlier defaults. With `parts=False` and `max_v=2`, the generator retains the previous sampling and returns.
- The design difference is correctly computed as
  \[
  \widehat{\Delta}_V-\widehat{\Delta}
  =(1-\pi_V)(\widehat{\Delta}_V-\widehat{\Delta}_N).
  \]
  Each jackknife replicate recomputes both components together. Their covariance is therefore retained.
- Calibration and validation use separate streams. The reported multipliers **1.16 and 1.14**, validation coverage **0.947 and 0.955**, and mean calibrated half-widths **0.252 and 0.211** match `power_results_v11_calib.txt`.
- The power ranges in section 6.4 match the recorded rows. They are minimum configuration-specific rejection rates, not probabilities that both configurations establish a difference.
- The four-V experiment correctly uses `min(4, NV)`. Its reuse of the two-V multiplier is disclosed as an approximation.
- About **52 V functions** is consistent with the expected allocation under the simulated frame. It is not a fixed sample count.

## Remaining issues

### R9.1 [Major] [C4, C7] The substitute builder has already read the audit

**Sections:** 5.4, 5.9 and 8.

**Evidence:** Step 1 assigns the second person responsibility for manually mapping findings and checking V and N labels and multi-function exclusions. Step 4 then assigns that same person the blind step for protocols on the student’s prior-exposure list. Section 5.9 explicitly uses this arrangement for the pilot protocols.

This contradicts the requirement that people familiar with a finding cannot provide its blind construction evidence. Sealing labels from the student does not remove the second person’s knowledge.

The sequence works for unfamiliar protocols where the student performs blind construction. It does not work for the stated exception.

**Required change:** Give previously known protocols a separate sequence: the audit-informed student prepares and seals the sampled task list, while an unexposed second person freezes the blind artifacts before receiving any findings, labels, fixes, or mapping-review work.

### R9.2 [Major] [C7] The V-expansion rule counts construction but omits downstream work

**Sections:** 6.4 and 8.

**Evidence:** The expansion rule permits up to four V functions when “the measured V-task hours fit the extra functions inside the reserve.” Section 8 charges approximately 22 additional functions at 4–8 hours each, or 88–176 hours.

However, each additional function also adds:

- six agent generation attempts;
- the historical implementation and agent discovery campaigns;
- candidate confirmation and independent adjudication;
- replay and campaign operation.

These quantities already appear in the proposal’s general workload formulas, but they are absent from the new expansion decision. The reserve also has protected uses for development, failures, and operation. It is not entirely available for extra task construction.

This does not invalidate the two-V minimum. It makes the newly stated rule for selecting the larger allocation incomplete.

**Required change:** Replace the expansion condition with a complete incremental budget based on the actual additional functions, covering construction, generation, discovery, confirmation, paid review, and replay while retaining the protected development and operational reserve.

### R9.3 [Minor] [C6] The allocation paragraph mixes calibrated power with uncalibrated widths

**Section:** 6.4, “V allocation per protocol.”

**Evidence:** The paragraph reports narrowing from **0.200–0.230** to **0.146–0.172** while discussing reuse of the calibrated multiplier.

In `power_sim_v11.py`, the printed half-width is:

```python
(q * sed).mean()
```

It does not include `C_DESIGN[P]`. The reported power does include that multiplier. The width comparison is valid as an uncalibrated comparison, but its current placement implies otherwise.

**Required change:** Rewrite this sentence to label both width ranges explicitly as uncalibrated and distinguish them from intervals widened by the reused 1.16 multiplier.

### R9.4 [Minor] [C4] The pilot paragraph overstates its support for a large expected difference

**Section:** 6.4, pilot interpretation.

**Evidence:** The pilot report supports **16 of 32 runs containing the bug by code reading**. Its section 5.4 also distinguishes requests describing the vulnerable design from requests stating the corrected rule. It reports 13 of 13 versus 3 of 15 compiled runs containing the bug in those groups.

Thus “one request style” obscures the pilot’s strongest confound. Furthermore, code-reading bug presence is not the primary endpoint \(D\), which requires functionality and discovery by the implementation’s own blind campaign. The pilot does not directly estimate that endpoint or the N-stratum contribution.

**Required change:** Replace the pilot paragraph with a statement retaining the 16-of-32 observation but naming the two request groups and explaining that it motivates the scenario range without establishing the expected design difference.

### R9.5 [Minor] [C6] The design-comparison power table needs its decision scope stated

**Section:** 6.4.

**Evidence:** The code computes the minimum across configuration-specific rejection rates using a pointwise calibrated interval. The table calls this the “chance of showing a nonzero design difference.”

That wording can be read as a joint or multiplicity-controlled claim about the configurations. Section 6.3 correctly leaves this comparison secondary unless added to the multiplicity plan.

**Required change:** Add a table note stating that the entries are minimum configuration-specific rejection rates from pointwise intervals, without correction across configurations, and are not probabilities of a joint conclusion or ranking reversal.

## Whole-proposal judgment

I found no other new Blocking or Major issue against C1–C8. The narrower historical claim, own-campaign primary labels, bounded validation claims, executable attribution, separate repair paper, and disclosure safeguards remain intact.

The remaining Major issues are concrete implementation defects in the new staffing and expansion rules. They do not require completed development measurements or reopening the earlier inference debate.

DISAGREE: [R9.1 audit-informed substitute assigned blind construction; R9.2 incomplete incremental budget for V expansion]