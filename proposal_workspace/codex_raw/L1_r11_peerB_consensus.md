## Status of the 19 required changes

I checked the new simulation code against its recorded outputs, inspected the evidence tests, patches and logs, and verified all 61 hashes in the manifest. I did not rerun Docker or the simulations.

| AC item | Status and reason |
|---|---|
| 1 | **Partly.** RQ1a has a principal estimand and precision target, but the simulation checks an average half-width, the budget uses a different allocation, and the fallback has no demonstrated minimum scientific value. |
| 2 | **Not resolved.** Human timings remain absent; the time box guarantees a stopping date, not a useful completed study, and its claimed sampling justification is incorrect. |
| 3 | **Resolved as a workflow.** Section 5.4 now keeps primary confirmation ahead of audit access and assigns known protocols to an unexposed confirmer. |
| 4 | **Resolved for the protected proposal.** The matched outcome and contrary evidence address the earlier structural problem, and the experiment is no longer a claimed contribution; its log-odds interpretation still needs qualification. |
| 5 | **Partly.** The monthly ceiling and operation costs are explicit, but the throughput calculations budget two V functions while the precision allocations require four or six, and several validation activities lack quantities in the budget. |
| 6 | **Partly.** Entitlement, backing, capital, ordering and independent H-02 checks now have executable evidence; the correction still breaks ordinary empty-range behavior, and the reproduction script stops early. |
| 7 | **Partly.** Counts, cells and investigation budgets are specified, but additional unresolved cases exceed the stated hours, sparse cells lack a complete allocation rule, and the uncertainty summary ignores unequal selection and clustering. |
| 8 | **Partly.** An audit-missed validation set is planned, but its availability is unmeasured and its recall interval is treated too directly as a bound for historical N sensitivity. |
| 9 | **Not resolved.** V13 supplies alternative power under one adverse bound, but no null calibration, no 0.10 unresolved scenario, no opposite-direction analysis, and no validation of the new two-attempt design. |
| 10 | **Resolved at design level.** The cutoff-based subset analyses and frame count are specified; unavailable or incomplete cutoff information must remain explicitly unknown. |
| 11 | **Resolved at design level.** Reviewer identities must be frozen, and the other-family analysis is specified when overlapping families remain. |
| 12 | **Partly.** Revision opportunities and thresholds are fixed, and the binomial arithmetic is correct, but the advertised pass probabilities require independence assumptions not established for the development cases. |
| 13 | **Partly.** Zero-V protocols and the observed pilot spread enter simulations, but the spread is not the refreshed eligible frame, and “about 50 V functions” is not an allocation-independent threshold. |
| 14 | **Resolved as a reporting rule.** RQ1a accompanies rediscovery and audit-supplemented estimates, with an explicit criterion for interpreting a small difference. |
| 15 | **Partly.** The template and duplicate-request exercise are specified, but the second builder may already know the mapping, and the request-diagnostic timing contradicts the new audit-access sequence. |
| 16 | **Resolved.** Paper 1 drops the earlier equivalence claim. |
| 17 | **Partly.** A non-inferiority test is named, but the algebra has the wrong sign, the margin does not establish “does not fall,” and the required simulation is absent. |
| 18 | **Partly.** Most factual questions are answered, but the new allocation and numerical summaries contain inconsistencies, and measured-cost selection remains prospective. |
| 19 | **Resolved for source provenance.** The default random draw is fixed and all manifest hashes match; I verified the files and code change, not the claimed full reruns. |

## Remaining issues

### R11.1 [Blocking] [C4, C6] Time-based stopping does not preserve simple random sampling

**Sections:** 5.2 and 8.

**Problem and evidence:** The proposal says that a random order and fixed stopping date make processed protocols “themselves a simple random sample.” Processing time determines how far through that order the study gets. It can depend on complexity, candidate counts and confirmation difficulty.

For example, conditional on processing only one protocol, that protocol can disproportionately be one that took a long time. Recording started failures does not make the resulting sample a fixed-size simple random sample. The stated inclusion probabilities and jackknife do not address this stopping mechanism.

**Required change:** Replace the throughput-dependent sample with a fixed probability sample selected before main work, using predetermined per-protocol work limits and retaining every selected protocol in the analysis, including those whose work limit is exhausted.

### R11.2 [Blocking] [C1, C7] A stopping date is not a viable minimum deliverable

**Sections:** 3, 8 and 10.

**Problem and evidence:** Section 8 says the plan “no longer depends on these unknown hours to finish.” Yet its pessimistic case produces about 11 protocols, makes RQ1b descriptive, and demotes RQ1a. The replacement contribution is then an unspecified “validated benchmark.”

That is structurally different from the previous fixed-size plan, but it does not answer the committee’s concern. The design can finish with neither its principal precision target nor its alternative inferential claim supported. Automated timing of an audit-assisted package does not establish the feasibility of blind human construction and confirmation.

At proposal stage, measured hours need not establish every future cost. Here, however, the committee explicitly required the development evidence after repeated unsupported assumptions. The new stopping rule cannot substitute for it.

**Required change:** Replace the open-ended throughput promise with a fixed, capped minimum study whose total resource limit and minimum evaluable output are specified in advance, and support that minimum with the requested human development cases before presenting it as ready for confirmatory collection.

### R11.3 [Major] [C7] The costed allocation is not the precision allocation

**Sections:** 5.2, 6.4 and 8.

**Problem and evidence:**

- Section 5.2 specifies up to **four V functions**.
- The counted-frame allocation reaching mean half-width **0.196** uses **six V functions per protocol**, 40 protocols and two attempts.
- Section 8 calculates throughput using **two V functions per protocol**.
- Paid adjudication is illustrated with 1,000 campaigns, whereas the cited counted-frame precision allocation has 1,080.
- The additional audit-missed cases, development gate reserve and duplicated request construction have no complete quantity-based allocation.

Consequently, the optimistic throughput row does not establish that the precision allocation fits.

**Required change:** Replace the throughput table with one reconciled resource ledger for each candidate allocation, using its actual V cap, N allocation, attempts, validation work, paid work and operational limits.

### R11.4 [Major] [C6] V13 does not validate the declared adverse-bound decision

**Sections:** 6.3 and 8; `tools/power_sim_v13.py`.

**Problem and evidence:** V13 uses the old levels `{15: 0.04, 20: 0.035}` and the generator’s default three attempts. It generates only positive alternatives and tests only the lower bound for “agents worse.” Unresolved scenarios stop at 0.05, apart from asymmetric 0.02 cases. There is no independent null validation or confidence-bound coverage check.

The proposal nevertheless permits Holm testing from 12 protocols and uses an unresolved share of 0.005 as a launch criterion. Neither rule is validated by V13. The quoted power numbers match the file, but they concern a different design.

**Required change:** Produce a calibration-and-validation study of the final adverse-bound procedure for the selected allocation, including both directions, nulls, partial nulls, author-dependent unresolved rates through 0.10, and the actual two-attempt design, and derive the launch rule from that study.

### R11.5 [Major] [C4, C6] RQ1a is incorrectly exempted from unresolved outcomes

**Sections:** 6.2–6.4.

**Problem and evidence:** Section 6.3 says “RQ1a is unaffected, because it is judged by its interval.” An interval around a zero-filled estimate does not account for unresolved labels.

The design difference is \((1-\pi_V)(d_V-d_N)\). Unknown labels in either stratum affect it. Its adverse assignments also differ by stratum because the N contribution is subtracted. V12 and V15 simulate no unresolved outcomes.

The narrowed definition also conflicts with section 5.4, where an incoherent specification remains unresolved, and section 8, where unfinished construction remains in the sample.

**Required change:** Define and validate identification bounds for RQ1a that cover unresolved construction and evaluation outcomes, and apply the precision target to intervals incorporating those bounds.

### R11.6 [Major] [C6] The precision evidence does not implement the stated target

**Section:** 6.4; `tools/power_sim_v12.py` and `tools/power_sim_v15.py`.

**Problem and evidence:** The target is stated “for each configuration” as a half-width at most 0.20. Both scripts calculate an average across studies, configurations and scenarios:

`np.mean([(c * q * sed).mean() ...])`

The recorded 0.196 therefore does not establish that each configuration or retained scenario meets the target. Likewise, excluding zero at a true difference near 0.33 is not the same decision as establishing a magnitude greater than the stated meaningful difference of 0.10.

The statement that about 50 V functions are needed is a summary of selected scenarios, not a general sample-size result.

**Required change:** Specify one operational precision criterion—including how it aggregates configurations, scenarios and repeated studies—and evaluate that criterion together with interval exclusion of the meaningful-difference threshold, rather than substituting mean width and exclusion of zero.

### R11.7 [Major] [C4, C5] The 63008 package remains incomplete under the attribution standard

**Section:** 5.11; `evidence/63008/`.

**Problem and evidence:** The package provides substantial new evidence. The logs support the entitlement and backing loss and show that correcting H-02 alone leaves this attack intact.

However, the README explicitly says the proposed correction produces a “phantom tick” for an empty range. That is an ordinary regression, not one of the four assertions endorsing the vulnerability. Section 4 requires the correction to preserve functionality. Saying the historical fix had the same behavior does not satisfy that condition.

There are also reproduction defects:

- `reproduce.sh` uses `set -e`, then runs an entitlement test expected to fail; `dock.sh` propagates its exit status, so the script stops before later states.
- The script copies the additional loss-test contract but excludes only the entitlement contract from the repository-suite run, unlike the recorded original-suite totals.
- Fixed-state backing and withdrawal success are logged, but execution stops at the first failed violation assertion rather than asserting the fixed-state properties.

**Required change:** Complete a replacement package with a function-body correction that preserves empty-range behavior, explicit fixed-state assertions, and a runner that checks expected outcomes and reproduces every recorded state.

### R11.8 [Major] [C4, C6] Validation intervals are treated as transportable natural-recall bounds

**Sections:** 5.9 and 6.5.

**Problem and evidence:** Section 6.5 sets agent sensitivity ranges by multiplying historical intervals by seeded recall-ratio intervals. That assumes the seeded author ratio transfers to natural flaws. The proposal elsewhere correctly says seeded recall does not identify natural-flaw recall.

Similarly, later-discovered flaws are selected because someone eventually found them. Their rediscovery interval does not, without a transport assumption, bound sensitivity on all flaws that survived an earlier audit. The rule also needs to establish that each flaw existed in the same earlier-audited code, rather than being introduced afterward.

Finally, “where [the auditor sample] contradicts a range” has no operational definition. Auditor disagreement is not itself a sensitivity estimate.

**Required change:** Rewrite section 6.5 as an explicitly assumption-based sensitivity analysis, separating observed validation intervals from transport assumptions and retaining feasible natural-recall ranges when those assumptions lack support.

### R11.9 [Major] [C6, C7] The natural-auditor plan is not fully specified or costed

**Sections:** 5.9 and 8.

**Problem and evidence:** The stated 120 hours cover 48 first assessments and 12 duplicate assessments at two hours each. Additional unresolved cases therefore exceed that total. If cells contain fewer than four implementations, the plan no longer necessarily supplies 48 implementations or eight campaign-negative implementations per author.

The “about ±0.3” uncertainty ignores selection weights, protocol dependence and varying realized cell sizes. Those features matter when interpreting author disagreement.

**Required change:** Replace the auditor plan with a fixed-budget allocation algorithm covering sparse and unresolved cells, duplicate assessments, inclusion weights and design-aware uncertainty for the declared disagreement estimand.

### R11.10 [Minor] [C6] Gate probabilities are conditional calculations

**Section:** 5.9.

**Problem and evidence:** The binomial values are correct under independent trials with the stated recall. The development reserve contains clustered findings, and a revised campaign can have different behavior. Thus the text’s unconditional claim that a weak campaign passes with probability below 0.10 is stronger than the calculation supports.

**Required change:** Label the table as an independent-trial planning calculation and state that its error bound is not established for the actual clustered, revised campaign.

### R11.11 [Minor] [C4] Request procedures conflict with the new blindness sequence

**Sections:** 5.4 and 5.9.

**Problem and evidence:** Section 5.4 places the audit-informed request diagnostic after primary locking, but later says it occurs “before evaluated runs.” It also asks both builders to write requests even though one normally performed the audit-informed mapping. Section 5.9 permits mapping-review access after blind inputs are committed, whereas the new sequence requires waiting until primary confirmation is locked.

**Required change:** Replace these passages with one consistent request and access schedule that records builder exposure, freezes requests before runs, and withholds audit and mapping-review material from confirmers until primary locking.

### R11.12 [Minor] [C4, C6] The security reading rule has a sign error and a different meaning from its wording

**Section:** 6.2.

**Problem and evidence:** If \(\Delta_D=D_A-D_H\), the planning difference in working outputs without a confirmed flaw is

\[
(0.72-D_A)-(1-D_H)=-0.28-\Delta_D.
\]

The shortfall is therefore \(0.28+\Delta_D\), not “0.28 minus the difference in D.” A non-inferiority margin of 0.05 permits a decline; it does not establish that the rate “does not fall.” No supplied simulation tests this added decision.

**Required change:** Rewrite the reading rule with the correct contrast and an explicitly justified non-inferiority interpretation, withholding the “better security” wording until its joint decision has been validated.

### R11.13 [Minor] [C4] The extension’s null is a modeling choice, not a theorem about obedience

**Section:** 6.6.

**Problem and evidence:** Matching endorsed outcomes is an improvement. But generic obedience does not necessarily produce equal log-odds interactions. Equal conditional interactions also need not yield equal interactions in aggregated protocol probabilities. V14 defines particular generating scenarios; it does not establish that every generic-obedience mechanism lies in its null.

The claim that the probability-scale test “rejects too often” also compares different estimands: unequal probability effects can be real under equal logit parameters.

**Required change:** Describe equal log-odds interactions as the extension’s operational null and limit calibration and interpretation claims to that model, rather than equating it with generic obedience.

### R11.14 [Minor] [C4] Correct factual summaries

**Sections:** 1, 5.1 and 6.4.

**Problem and evidence:**

- The abstract has 174 whitespace-separated words, exceeding the retained 150-word limit.
- The counted ten-protocol vector has **three**, not four, zero-V entries.
- V12’s recorded maximum validation coverage is **0.965**, not 0.963.
- V15 reports **0.040** for the 20-protocol rows; 0.039 applies to the rows with 30 or 40 total protocols and N functions in 20.

**Required change:** Correct these summaries and shorten the abstract to at most 150 words.

## Rebuttal check

The draft represents all 19 items and nine disagreements. These corrections are needed before it can be co-signed.

### Opening structural-fix claims and disagreement 5

**Problem:** The time box is presented as guaranteeing a scientifically complete deliverable and preserving the sampling design.

**Exact replacement text for the feasibility bullet:**

> Feasibility (item 2): the proposed revision limits processing to fixed dates. This caps elapsed work but does not establish a useful minimum sample or preserve simple random sampling when processing time varies by protocol. Human development timings remain outstanding. The sampling and minimum-deliverable claims therefore still require revision.

**Exact replacement text for the final sentence of “What we could not do”:**

> The time box is a proposed resource limit, not evidence that the intended minimum study is feasible. It does not yet resolve the committee’s requirement.

**Exact replacement text for disagreement 5:**

> Human feasibility evidence remains incomplete. Automated timings are reported separately. Fixed dates alone do not establish the sampling properties or scientific value of the completed sample.

### Row 1

**Problem:** The response treats the precision criterion as met and “about 50 V functions” as a general requirement. The reported widths are averages under particular allocations.

**Decision replacement:** `Partly addressed; allocation and precision rule remain open`

**Exact replacement text:**

> RQ1a is proposed as the principal estimand, with a meaningful difference of 0.10 and a half-width target of 0.20. The simulations report mean pointwise half-widths under specified hypothetical frames. In the counted-spread scenario, 40 protocols, a V cap of six and two attempts give mean half-width 0.196 and a minimum configuration-specific zero-exclusion rate of 0.90 near a true difference of 0.33. This does not establish a universal requirement of about 50 V functions or attainment of the target for every configuration and scenario. The criterion, allocation and budget must be reconciled before the principal contribution is secured.

### Row 2

**Problem:** “Processed protocols stay a simple random sample” is false, and the throughput range does not validate completion.

**Exact replacement text:**

> Human development timings have not been measured. The recorded automated jobs took 1,373 seconds for the 63008 package and 864 seconds for the fix-scope classification, starting from existing pilot material. The proposed time box limits processing dates. Its resulting sample size depends on processing costs, so random order alone does not establish simple random sampling. The stated throughput range is conditional on assumed costs and does not establish a minimum scientific deliverable.

### Row 4

**Problem:** Equal log-odds interactions are described as necessarily representing plain obedience, and the probability-scale test is judged against a different null.

**Exact replacement text:**

> The experiment is now a specified extension, not a claimed contribution. It uses endorsed-behavior outcomes, matched contrary evidence and recorded pair-admission checks. Equal generating log-odds interactions define the simulated null; this is a modeling assumption about generic obedience. V14 records log-odds rejection rates of 0.040 to 0.067 in those scenarios and power of 0.529 to 0.812 at 160 functions for the displayed alternatives. Different probability-scale results do not by themselves invalidate a probability-scale estimand. Further validation is required before a confirmatory extension.

### Row 5

**Problem:** The table does not reconcile all activities with the allocation needed for precision.

**Decision replacement:** `Partly addressed`

**Exact replacement text:**

> A monthly ceiling of 150 student hours and zero hours for the extension are now explicit. Campaign operation has an assumed unit cost. However, the throughput calculations use two V functions per protocol while the precision allocations use four or six. Additional validation work and paid assessments are not fully reconciled with those allocations. The table is a resource schedule, not yet a complete feasibility calculation.

### Row 6 and the opening description of the evidence package

**Problem:** “Done” and “complete” overstate the evidence.

**Decision replacement:** `Partly completed`

**Exact replacement text for row 6:**

> The package provides executable entitlement and backing evidence, a function-body intervention, capital and ordering records, and an independent H-02 check. The recorded attack persists with H-02 fixed alone. The function-body correction removes the observed theft but introduces an empty-range regression, so functionality preservation remains unproved. The reproduction script also stops at an expected failing test before completing all states. The package must be completed before it is described as satisfying the full standard.

**Exact replacement text for the evidence-list entry:**

> `evidence/63008/`: executable evidence of entitlement loss and the independent H-02 check; functionality preservation and complete automated reproduction remain open.

### Row 7

**Problem:** The total excludes the added unresolved cases and assumes full cells.

**Decision replacement:** `Partly addressed`

**Exact replacement text:**

> The proposed base allocation is four implementations in each of 12 cells, with 12 duplicate assessments. At two hours per assessment this uses 120 hours when all cells are full. Additional unresolved cases need an explicit allocation within or beyond that budget. Sparse-cell handling, weighted disagreement estimates and protocol-aware uncertainty remain to be specified. The approximate ±0.3 statement is a rough small-sample calculation, not validated precision for the actual design.

### Row 8

**Problem:** Availability is still unknown, and a selected later-discovered set does not directly establish historical N sensitivity.

**Exact replacement text:**

> A separate audit-missed validation set is planned, with a target of 10 to 20 cases. Availability has not yet been counted. Each case must establish that the flaw existed in code covered by the earlier audit. Rediscovery measures performance on these selected cases. Applying that interval to historical N code requires an explicit transport assumption; without support, natural-flaw sensitivity retains a broader feasible range.

### Row 9

**Problem:** The response presents alternative power as completion of the requested calibration and omits the design mismatch.

**Decision replacement:** `Partly addressed; calibration remains open`

**Exact replacement text:**

> V13 evaluates power for positive alternatives under the lower adverse bound, using three attempts and the earlier 15- and 20-protocol Holm levels. Its quoted power ranges match the results file. It does not calibrate null error, evaluate the opposite direction, include unresolved rates of 0.10, or validate the new two-attempt allocation. The proposed 0.005 launch threshold and the rule permitting inference from 12 protocols remain unsupported by that simulation. RQ1a also requires unresolved-outcome bounds.

### Row 12

**Problem:** The binomial rates are presented as unconditional gate guarantees.

**Exact replacement text:**

> The proposed gate uses eight qualifying flaws, a pass mark of five, and at most one revision on eight fresh flaws with a pass mark of six. Under independent trials with the stated recall in both assessments, overall pass probabilities are 0.069, 0.455 and 0.913 at recall 0.3, 0.5 and 0.7. These are conditional planning calculations. The development cases have not yet been qualified, and the probabilities are not validated for protocol dependence or adaptive campaign revision.

### Row 13

**Problem:** The simulation uses a filtered pilot distribution, not the refreshed eligible frame, and does not establish a universal V-count threshold.

**Decision replacement:** `Partly addressed`

**Exact replacement text:**

> V12 includes protocols without V functions. V15 samples counts from the filtered pilot vector [9, 2, 2, 0, 1, 1, 1, 1, 0, 0]. This is planning evidence, not the refreshed eligible frame. The outcome-based allocation condition is removed. Final allocation must use the refreshed count, a defined precision criterion and reconciled costs. No allocation-independent minimum of about 50 V functions has been established.

### Row 15

**Problem:** The response omits the exposure and timing contradictions.

**Exact replacement text:**

> A frozen request template and independent requests for a random subset of 15 functions are proposed. The protocol must still distinguish an unexposed request builder from a person who has reviewed the mapping. The request-diagnostic schedule must also be reconciled with the rule that audit access follows primary locking.

### Row 17

**Problem:** The test is not simulated, and a margin of 0.05 does not establish no decline.

**Decision replacement:** `Partly addressed`

**Exact replacement text:**

> Section 6.2 specifies a one-sided non-inferiority test with margin 0.05 and Holm adjustment across two configurations, but no supplied simulation validates this decision. Under the planning completion rates, the agent-minus-historical working-without-confirmed-flaw difference is −0.28 − ΔD. The text’s subtraction has the wrong sign. Passing non-inferiority would permit a decline up to the margin; it would not establish that the rate does not fall.

### Row 18

**Problem:** Most answers are present, but “two, chosen because more protocols buy more precision” overstates what the raw-width comparison establishes.

**Exact replacement text for the attempts sentence:**

> Two attempts are proposed. V16 shows narrower raw intervals for 20 protocols with two attempts than for 15 protocols with three, under its stated scenarios. This compares campaign counts and precision, not total measured cost, because additional protocols also require preparation and construction.

### Disagreement 8

**Problem:** Validation is described as addressed without acknowledging the remaining sampling and transport problems.

**Exact replacement text:**

> The primary-confirmation sequence is corrected at design level. Natural-validation allocation, the audit-missed set and the interpretation of sensitivity ranges remain partly addressed, as recorded in items 7 and 8.

DISAGREE: [R11.1, R11.2, R11.3, R11.4, R11.5, R11.6, R11.7, R11.8, R11.9]