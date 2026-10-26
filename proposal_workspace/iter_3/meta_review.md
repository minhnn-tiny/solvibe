# Meta-review, iteration 3

**Proposal:** "AI Agent Function-Body Replacements in Audited Solidity: Executable Vulnerability Comparisons with Historical Developer Code", version 15 (`proposal_workspace/iter_3/proposal.md`).

**Reviews:** R1 to R5, all in `proposal_workspace/iter_3/reviews/`.

**What I checked myself:**
- **V19 and V20 results.** I checked the V19 results (`tools/power_results_v19.txt`) and the V20 results (`tools/power_results_v20.txt`). Every number the reviewers quote from them matches.
- **The RQ1 data generator** (`tools/power_sim_v8.py`):
  - agents compile with probability 0.9 and pass with probability 0.8, so 0.72 of agent attempts work;
  - historical code always works;
  - vulnerability is drawn independently of whether the code works;
  - every protocol has 2 + Poisson(2) V functions and 30 to 120 N functions.
- **File hashes.** I computed the SHA-256 hashes of five files: the generator, the V19 script, the V20 script and the two result files. All five match the manifest of cited files (`tools/MANIFEST.md`).
- **The fix-scope record** (`evidence/frame_count/README.md`):
  - the one-function V counts per protocol are [9, 2, 2, 0, 1, 1, 1, 1, 0, 0];
  - Ammplify has 13 High and 23 Medium findings, and only one of them is among the 43.
- **The pilot process log** (`docs/pilot/process_log.md`, step 18). The pilot's LLM security reviewers were given "the five High and Medium findings of the audit report".
- **The 63008 package README** (`evidence/63008/README.md`). Fix commit `c01b6c7` also edited the library `@dev` note and the `initDown` `@param` notes.
- **Budget arithmetic.** I redid the budget arithmetic of R1, R3 and R5 against section 8. I also redid R3's split of the design difference against the generator.

I did not rerun any simulation. Where I rely on a reviewer's rerun, I say so.

## Actionability check

All five reviews score 3 or lower, so I checked all five.

| Review | Score | Example of a concrete required change | Result |
|---|---|---|---|
| R1 | 3 | W1: Replace the single allocation with a short preregistered table of allocations. For each one, give its cost at the low, middle and high assumed rates, and its RQ1a and RQ1b precision from the V20 script (`tools/power_sim_v20.py`). Fix now a rule that picks one allocation from the month-1 measured unit costs alone, before sampling. R1 names W1, W2 and W3 as the changes that raise its score to 4. | Pass |
| R2 | 3 | W2: Produce a readiness analysis that uses the refreshed list of eligible functions. Its simulations of a finite population must include construction that depends on difficulty, unresolved outcomes and sparse strata. R2 names this and W1 (a measured feasibility record) as "a concrete basis for raising the score to 4". | Pass |
| R3 | 3 | W2: Preregister that RQ1a on D is always reported in two parts for each stratum: security among working outputs, and the part caused by functional failure. The 0.10 reading applies to the security part. R3 names W2, W3 and W4 for a 4. | Pass |
| R4 | 3 | W1: Produce one frame-based readiness analysis. It uses the refreshed eligible counts and a fully enumerated simulated finite population, and it includes construction that depends on difficulty and unresolved outcomes. R4 calls W1 and W2 "concrete changes that would raise my score". | Pass |
| R5 | 2 | W2: Evaluate the section 8 reservation inequality for the maximum allocation at the low, middle and high rates, with separate V and N construction allowances. Then change the allocation or the hour ceiling so that the inequality holds at the middle rates. R5 names W1 to W3 for a 3, and W4 to W6 in addition for a 4. | Pass |

No review is sent back.

One caution. R2 and R4 tie their higher score partly to a measured human development record. Only the PhD student and paid people can produce that record. The two authors cannot. It is still a concrete change, so both reviews pass. I come back to this under open question OQ1.

## R4 overlap check

R4 names eight prior papers. All eight are VERIFIED in the master index of searched papers (`lit/master_index.tsv`, *status* column). So I did not need to open any URL.

| Paper R4 names | Index row | Result |
|---|---|---|
| SolEval (EMNLP 2025) | `Peng2025-SolEval` | Confirmed |
| SolAgent (arXiv 2601.23009) | `Chen2026-SolAgent` | Confirmed |
| SecureVibeBench (ACL 2026) | `Chen2026-SecureVibeBench` | Confirmed |
| How Safe Are AI-Generated Patches? (Sajadi et al., arXiv 2507.02976) | `Sajadi2025-HowSafePatches` | Confirmed |
| SpecGuard (arXiv 2610.09159) | `Biyani2026-SpecGuard` | Confirmed |
| RAPO-Sol (arXiv 2610.08429) | `Wang2026-RAPOSol` | Confirmed |
| SPLASH (arXiv 2610.26001) | `Rahman2026-SPLASH` | Confirmed. The arXiv number places it in October 2026. The index does not record the day, so R4's "October 19" is [uncertain] to me. |
| MAGen (Empirical Software Engineering) | `Liu2026-MAGen` | Confirmed. R4 marked its date [uncertain]. The search notes (`lit/r1_L4_solidity_codegen.md`) record online publication on 28 July 2026, in volume 32 (2027). So it predates this proposal. That does not change R4's verdict. |

**R4's answer to "same technique, same problem, same claim?" is No. I agree.**

- No verified paper does both of the following:
  - sample flagged and unflagged functions with known probabilities;
  - measure how much a flagged-only view changes an agent-versus-developer comparison, using executable evidence attributed to one function.
- The closest papers differ as follows:
  - SolEval, SolAgent, RAPO-Sol and MAGen judge security by static analysis, text metrics or generated tests.
  - SecureVibeBench selects only historical failures.
  - Sajadi et al. compare human and agent patches, but without this sampling design.
  - SPLASH scores generated code and has no historical baseline.
- SpecGuard touches only the repair extension, which is not a claimed contribution.

Two other reviewers cite work showing that selecting cases by failure biases a comparison in general. These are Bird et al. (ESEC/FSE 2009, cited by R1) and Coston and Kennedy (cited by R5). Both are VERIFIED in the index. They show the bias exists. They do not measure it for this problem. So they bear on how informative the result is (C1). They do not bear on condition (c).

## Decision

| Review | Score |
|---|---|
| R1 | 3 |
| R2 | 3 |
| R3 | 3 |
| R4 | 3 |
| R5 | 2 |

Mean: 14 / 5 = **2.8**.

| Condition | Holds? |
|---|---|
| (a) Every score at least 4 | **No.** Four scores are 3 and one is 2. |
| (b) Mean at least 4.0 | **No.** The mean is 2.8. |
| (c) R4 reports no prior work using the same technique on the same problem to make the same claim | **Yes.** R4 answers No, and I agree. |
| (d) The AC concurs | Does not apply, because (a) and (b) fail. |

**Result: NOT ACCEPT.**

The mean fell from 3.0 to 2.8, because R5 moved from 3 to 2. The revision did resolve most iteration-2 items in the text. Making RQ1a principal and writing out the budget per protocol also helped. They let the reviewers check the plan against its own numbers.

Three of those checks fail, and none of them needs human data:
- By the proposal's own rates, the maximum allocation does not fit the 45-hour cap per protocol, even at the optimistic end. All five reviewers raise this.
- Under the only counted V distribution, the fixed allocation fails the RQ1a precision criterion. All five reviewers raise this.
- The "little difference" reading cannot occur at the planned precision. R1, R3 and R5 raise this.

All three can be fixed with arithmetic, an automated frame count and the existing simulators.

The iteration-2 meta-review warned that a version which again only schedules the human cases was unlikely to change the decision. That happened.

Ratings for this iteration:
- C2, C3, C5 and C8: all five pass.
- C6: all five concern.
- C1: R2 and R4 pass; R1, R3 and R5 concern.
- C4: R2 and R4 pass; R1, R3 and R5 concern.
- C7: R2 and R4 concern; R1, R3 and R5 fail.

## Prioritized required changes

The labels mean:
- **Blocking:** the main claim cannot stand without the change.
- **Major:** acceptance needs it.
- **Minor:** it improves clarity or precision.

### 1. Blocking. The fixed minimum study does not fit its own budget rule.

**Raised by:** R1 (W1), R3 (W3), R5 (W2). R2 (W1) and R4 (W2) raise the same gap using the averages.

**Problem.**
- Section 8 says the reservation must cover the maximum allocation within 45 student hours per protocol. The maximum allocation is 6 V and 8 N functions, which means 70 campaigns.
- I checked the reviewers' sum at the optimistic end of every section 8 rate:

  | Work | Hours |
  |---|---:|
  | Protocol preparation | 6 |
  | V construction, 6 × 4 | 24 |
  | N construction, 8 × 1.5 | 12 |
  | Campaign operation, 70 × 0.1 | 7 |
  | Confirmation, 70 × 8/64 candidates × 0.5 | about 4.4 |
  | **Total, before generation and secondary work** | **about 53** |

- At the middle of every range, the same sum is about 86 hours. This is my arithmetic. It uses a candidate rate of 0.18, the midpoint of 8/64 and 3/13.
- R3 adds a point about blinding. Builders receive the stratum labels sealed (section 5.4). A different allowance for V and N would tell the builder the label. With one common allowance of 4 hours, construction alone takes 14 × 4 = 56 hours.
- With one common allowance equal to the V construction rate, I find that about 8 functions per protocol fit at the optimistic end, and about 4 at the middle. This is my arithmetic, and it leaves out generation and secondary work.
- The proposal reports only averages, from about 43 to about 100 hours. Section 8 itself says that averages are not enough.
- This item and item 2 pull in opposite directions, because fewer functions per protocol widen the RQ1a interval. The reviewers suggest two ways to ease this:
  - R1's rerun shows that cutting N from 8 to 4 per protocol costs little for RQ1a. The largest raw half-width goes from 0.146 to 0.154. It costs more for RQ1b, from 0.055 to 0.075.
  - R5 suggests sampling protocols with probability proportional to their V count.

**Required change.** Add a preregistered table of candidate allocations to section 8. Each row gives the number of protocols, the V cap and the number of N functions per protocol. For each row, report:
- its reservation for the maximum allocation at the low, middle and high rates, using one common construction allowance;
- its RQ1a and RQ1b precision from the reruns in item 2.

Fix now a rule that picks one row from the month-1 measured unit costs alone, before sampling. At least one row must fit at the middle rates and also pass the RQ1a criterion. If no row does, say so in section 8.

### 2. Blocking. The V distribution that decides RQ1a has not been counted, and the only counted one fails.

**Raised by:** R1 (W2), R3 (W4), R5 (W1), R2 (W2), R4 (W1).

**Problem.**
- Every passing planning result draws 2 + Poisson(2) V functions per protocol. No data support this distribution.
- The only counted distribution comes from the fix-scope record. Under it, V19 gives these results with no unresolved outcomes:
  - largest mean full-interval half-width 0.314, against a criterion of 0.20;
  - the interval excludes −0.10 near a true value of −0.33 in 0.38 of studies, against a criterion of 0.80.
- The counted vector may understate the frame. Only 1 of Ammplify's 36 High and Medium findings is among the 43 classified. So neither distribution describes the frame.
- V20 makes construction independent of outcomes and of difficulty. R2 and R4 ask for construction that depends on difficulty.
- R3 reran V20 with a V construction probability of 0.4. The half-widths were 0.22 to 0.26, and exclusion rates were 0.49 to 0.55. I did not rerun this.
- The count needs no student. Classifying the 43 findings took 864 seconds of automated work (the timing record, `evidence/timings.md`).

**Required change.** Count the frame and rerun the planning simulations on the count:
1. Draw 20 to 30 protocols at random from the contest-listing frame.
2. Classify the fix scope of every qualifying High and Medium finding, as in `evidence/frame_count/`.
3. Report the eligible V count per protocol after the exclusion of fixes that span several functions.
4. Rerun V19 and V20 on that distribution for every allocation in item 1. The reruns must use:
   - a fully enumerated simulated finite frame;
   - at least one scenario in which construction depends on difficulty and on vulnerability;
   - a V construction probability that the item-1 allowance can justify.

### 3. Blocking. On endpoint D, much of the design difference can come from agent code that does not work.

**Raised by:** R3 (W2), R5 (W4). R1 (Question 4) asks the same.

**Problem.**
- Within one stratum, the author difference splits into two parts:

  d = w_A(v_A − v_H) + (w_A − w_H)·v_H

  Here w is the share of working outputs, and v is the detected-vulnerability rate among working outputs.
- Suppose the agents' working code is as vulnerable as the developer's, and recall is 0.7. Then d_V ≈ (0.72 − 1) × 0.9 × 0.7 ≈ −0.18. That is larger than the 0.10 threshold, with no security difference at all.
- I checked the scenario that sets the −0.33 target, where the agent V rate is 0.6. In it, 0.176 of the 0.328 comes from functional failure. The security part is only about −0.15.
- Section 3 says: "A lower vulnerability count caused by failed generation is not evidence of better security." RQ1a, as defined on D, breaks that rule.
- The effect can also run the other way. A check that a blind builder writes may fail the historical V body. Item 4 deals with that.

**Required change.** Preregister that RQ1a on D is always reported with this split in each stratum. Apply the 0.10 reading and the precision criterion to the design difference of the security part, which is vulnerability among implementations that compile and pass. Report the other part as the share caused by functional failure. Redo the item-2 precision analysis for the security part. In the target scenario that part is about −0.15, not −0.33.

### 4. Major. Functional checks written from the documentation can endorse the flaw.

**Raised by:** R1 (W3). R3 (W2 and Question 2) and R5 (Question 2) raise the same problem.

**Problem.**
- Blind builders write the ordinary functional checks from permitted documentation (5.4), before generation (5.5).
- A counted flaw needs a correction that passes those checks (section 4, *Attribution*).
- Suppose the documentation describes the vulnerable behaviour. Then the blind builder writes a check that asserts it. Two things follow, and both shrink d_V:
  - the correct body-only correction fails that check, so the historical flaw cannot be counted;
  - a correct agent body also fails L.
- 63008 shows this can happen. Four repository tests assert the faulty boundary. The fix commit also edited the `@dev` and `@param` notes.
- Section 5.5 says "Assertions endorsing known faulty behavior are not accepted as correctness checks". A builder who has not seen the audit cannot apply that rule.

**Required change.** Preregister R1's rule. Suppose a correction removes a confirmed violation but fails a frozen functional check. Then adjudicators who are blind to the author decide whether that check asserts the attacker outcome. If it does, the check is dropped for every implementation of that function. L is recomputed for both authors. The number of such cases is reported by stratum.

### 5. Major. The "little difference" reading cannot occur at the planned precision.

**Raised by:** R1 (W4), R3 (W1), R5 (W5).

**Problem.**
- "Little difference" needs the full interval to lie inside ±0.10. That needs a half-width below 0.10.
- Every reported scenario has a largest mean half-width of 0.163 or more (V19, V20).
- R1 and R3 reran the setting. Neither found a single simulated study inside ±0.10, in any scenario. I did not rerun this, but it follows from the reported widths.
- R3's rerun shows how often the interval excludes −0.10 at smaller true values:
  - 0.11 to 0.13 of studies at a true −0.18;
  - 0.51 to 0.53 at a true −0.26.

  So most distortions between 0.10 and 0.30 would come out inconclusive.

**Required change.** In sections 3 and 6.4, do three things:
- Remove the "little difference" reading, unless an allocation in item 1 gives it a real chance when the true difference is near zero.
- State the smallest distortion that the chosen allocation detects with probability 0.80.
- For each planning scenario, report the simulated share of each possible reading.

### 6. Major. RQ1b has no precision target and no calibrated interval.

**Raised by:** R1 (W6), R5 (W6). R3 (W5) notes the uncalibrated RQ1b intervals.

**Problem.**
- In the planning model, about 4 V functions face 30 to 120 N functions per protocol. So the V share is about 0.05, and the weighted comparison is close to the N-stratum comparison.
- Where RQ1a can succeed, it mostly restates the flagged-only gap. Benchmarks such as SecureVibeBench already measure that gap (R1).
- The new information is whether agents add exploitable flaws to ordinary functions. That is RQ1b.
- The readiness decision checks only RQ1a. For RQ1b, the evidence is weak:
  - V20's plain RQ1b intervals cover only 0.925 to 0.935;
  - V17 gives power of 0.19 to 0.47 for a difference of −0.05 at 20 protocols.

**Required change.** Add an RQ1b precision target to the readiness decision:
- state the smallest agent excess in D on ordinary functions that would matter (R1 suggests +0.05);
- calibrate the RQ1b interval;
- report what each allocation in item 1 achieves for that target.

Call RQ1b co-principal only if the chosen allocation meets the target.

### 7. Major. No rule fixes which scenarios decide readiness.

**Raised by:** R3 (W5), R5 (W9 and W10). R2 and R4 ask the same in their questions.

**Problem.**
- Section 6.4 requires the criterion to hold "for every retained planning scenario". Nothing says how a scenario is retained.
- Every scenario that is not optimistic fails at least one requirement. I checked each:

  | Scenario | Failing result |
  |---|---|
  | Counted V distribution | half-width 0.314 and exclusion 0.38 |
  | Construction probabilities V 0.7, N 0.9 | exclusion 0.71 |
  | Construction probabilities V 0.6, N 0.6 | half-width 0.211 |
  | Unresolved share 0.02 | exclusion 0.69 |

- V20 picks a different multiplier for each construction scenario, from 1.08 to 1.14. But the study must fix its multiplier before it knows its construction yield.
- R5 adds a point about unresolved outcomes. Suppose development sees zero unresolved outcomes in n evaluations. The 95% upper limit is then about 3/n. Under R3's 80% rule it is about 1.6/n, so supporting a share near 0.01 needs about 160 evaluations.

**Required change.** Preregister how frame and development measurements become retained scenarios. Use R3's example as the default:
- the measured V distribution from item 2;
- the V construction probability at the lower 80% confidence limit of the development yields;
- unresolved shares at the upper 80% limit, with a stated floor.

Then:
- calibrate one RQ1a multiplier and one RQ1b level across all retained scenarios;
- add R5's minimum construction yield per stratum, for example 0.7, below which RQ1a and RQ1b are reported only as descriptive results;
- state how many development evaluations the plan will produce.

### 8. Major. A recall gap between authors can move RQ1a across the 0.10 threshold.

**Raised by:** R1 (W5).

**Problem.**
- In the generator, the detected V difference is aV × 0.72 × s_AV − 0.9 × s_HV.
- With an agent V rate of 0.6, the latent V difference is −0.47 in all three cases below. I checked R1's figures. The detected V difference, and so roughly the design difference, changes with recall alone:

  | Agent recall | Historical recall | Detected V difference |
  |---:|---:|---:|
  | 0.7 | 0.7 | −0.33 |
  | 0.8 | 0.5 | −0.10 |
  | 0.5 | 0.8 | −0.50 |

- The seeded pairs bound the recall difference only to a half-width of 0.135 to 0.194 (5.9).
- The sensitivity analysis in section 6.5 covers the author difference, not the design difference.

**Required change.** Extend the section 6.5 sensitivity analysis to the design difference, with separate agent and historical recall in each stratum. Report which RQ1a conclusions hold over the full feasible recall range, and which need a stated transfer assumption.

### 9. Major. There is no audit-blind evidence that the campaign can rediscover flaws of the kind auditors find.

**Raised by:** R5 (W3). R1 (Question 6) raises the related problem of the gate reserve.

**Problem.**
- The pilot's LLM reviewers were given the audit findings (process log, step 18). So the pilot gives no audit-blind evidence of rediscovery.
- The RQ1a reading rule needs a lower 95% rediscovery bound of at least 0.5. At recall 0.5, the development gate passes with probability 0.455.
- R5 cites two VERIFIED papers that give reasons for doubt: Khalid et al. (ESEM 2026) and Peng et al. (Re-Evaluating EVMBench).
- R1 notes that the gate reserve includes pilot material that already shaped the campaign prompts.

**Required change.** Now, before acceptance:
1. Run the frozen LLM-reviewer step without audit findings on the historical bodies of the 17 one-function pilot findings.
2. Report how many each reviewer flags at candidate level, with an interval.
3. State which of these cases leave the gate reserve because they shaped the campaign prompts.

### 10. Major. The student's commitment and one development case timed with the student.

**Raised by:** R1 (answer to OQ1) and R5 (answer to OQ1). R2 (W1) and R4 (W2) ask for the full three-case record. This is the open part of iteration-2 item 2.

**Problem.**
- No development case has been timed with a person doing the human steps.
- The student has not said whether they will take part (`iter_3/open_questions.md`).
- A conditional acceptance needs someone who will meet the condition (R1).
- The largest unknown is how long blind V construction takes. It decides both the budget (item 1) and the size of the constructible domain (item 2).
- R2 and R4 tie their score of 4 to measured human evidence.

**Required change.** Before the next submission, take two steps:
1. Obtain the student's written commitment, with dates, to the month-1 development cases.
2. Complete at least one development case on a pilot protocol. The student does every designated human step, the case includes a probability-selected set of N functions, and failures stay in the record.

The full three-case record remains the binding launch gate of section 8.

### 11. Minor. Candidates cut off by the confirmation limit now count as "not confirmed".

**Raised by:** R3 (W6).

**Problem.** Section 5.2 now treats candidates left unchecked at the confirmation limit as "not confirmed". The limit is the same for every implementation, but campaigns produce different numbers of candidates. Suppose one author's code draws more reviewer flags. Then the limit cuts off more of that author's real flaws, and the identification bounds no longer show it.

**Required change.** For each implementation, record whether the candidate limit cut its list. Report that share by author and stratum. Add a secondary bound that treats implementations with a cut list as unresolved.

### 12. Minor. The recall flag misses reproduction of the historical body.

**Raised by:** R5 (W7). R1 (Question 2) and R3 (Question 1) ask about the post-cutoff subset.

**Problem.**
- The recall flag checks only for distinctive fix lines.
- An agent that reproduces the historical body pulls the agent results toward the developer's results in both strata.
- The pilot audits date from September 2025 to January 2026. The subset with report and fix after the model cutoffs may therefore be empty. This is [uncertain] for any specific model.

**Required change.** Extend the recall flag to reproduction of the historical body in both strata, with a similarity threshold fixed before generation. Report RQ1a and RQ1b with flagged cases removed.

### 13. Minor. Request wording is not in the uncertainty.

**Raised by:** R5 (W8). R1 (Question 3) asks the same.

**Problem.** In the pilot, the request decided the outcome. The bug was in 13 of 13 compiled runs whose request described the vulnerable behaviour, against 3 of 15 whose request stated the corrected rule. The second request in the duplicate exercise is never used for generation.

**Required change.** For the 15 functions that receive two independent requests, run generation and the primary campaign on both requests as a secondary analysis. Report how much D changes between the two requests, beside RQ1a. Budget this in the item-1 table.

### 14. Minor. It is hard to see which numbers support the current plan.

**Raised by:** R5 (W11).

**Problem.** Sections 6.3 and 6.4 present four simulation versions, V17 to V20. They include allocations that were dropped, such as 15 protocols with a V cap of 4.

**Required change.** Replace the simulation history in sections 6.3 and 6.4 with one table for the current allocation. Move the superseded versions to an appendix.

### 15. Minor. Several factual questions have short answers that belong in the text.

**Raised by:** R1 (Questions 1, 2, 5, 8), R2 (Question 2), R3 (Questions 3 to 6), R5 (Questions 1, 4, 5, 6).

**Required change.** Answer each of these in the proposal:
- Can a script apply the rule "meaningful computation or state changes" for N eligibility? (R1 Q1)
- How many V functions in the item-2 count have their report and fix dated after the documented model cutoffs? (R1 Q2, R3 Q1)
- What unit values are assumed for h_generation and h_secondary? (R1 Q5)
- Which audit platforms make up the contest-listing frame, and what threshold triggers the recall flag? (R1 Q8. Both have been open since iteration 2.)
- Which named and funded people take the unexposed roles? (R2 Q2)
- What is the candidate limit per campaign, and how much of h_campaign is reserved for it? (R3 Q3)
- Do the earlier audits listed in the fix-scope record give a first count of flaws that an audit missed? (R3 Q4)
- What can four assessments per cell estimate? (R3 Q5)
- How often is a stratum empty in a jackknife replicate under the counted distribution? (R3 Q6)
- How many N functions are expected per protocol, and what V share does that imply? (R5 Q1)
- What is the order-of-magnitude compute cost per protocol? (R5 Q4)
- What does "agent ordering" add when there are only two configurations? (R5 Q5)
- Why does the repair extension stay in this proposal? (R5 Q6)

## Disagreements among reviewers

1. **C1, novelty and contribution.**
   - *Positions:* R2 and R4 rate C1 pass. R1, R3 and R5 rate it a concern. Their reasons: the sign of RQ1a is known in advance, RQ1a mostly restates the flagged-only gap, and D mixes in functional failure.
   - *Resolution:* This is not a duplication problem. R4's search and my check of condition (c) stand. The concern is about what the estimand can tell us, and it is valid. Items 3, 5 and 6 address it. Until they are done, I side with "concern".

2. **C4, soundness of claims.**
   - *Positions:* R2 and R4 rate C4 pass. R1, R3 and R5 rate it a concern.
   - *Resolution:* The concerns rest on mechanisms I checked: the generator's working rates and the 63008 notes and tests. R2 and R4 do not discuss these mechanisms. The concern stands until items 3 and 4 are done.

3. **C7, feasibility.**
   - *Positions:* R1, R3 and R5 rate C7 fail. R2 and R4 rate it a concern.
   - *Resolution:* The fail ratings rest on the arithmetic for the maximum allocation, which I checked. R2 and R4 discuss only the averages. "Fail" stands for the plan as written. Item 1 can lift it to "concern". Only measured human time can lift it to "pass".

4. **How to fix the budget, and whether V and N can have different allowances.**
   - *Positions:*
     - R1 wants a table of allocations, chosen by a rule from measured costs.
     - R3 wants an allocation that fits at the stated rates, using one common allowance.
     - R5 wants the inequality to hold at the middle rates.
     - R1 and R5 compute with separate V and N construction rates.
   - *Resolution:* Combine all three, as item 1 does. On the allowance, R3 is right. A visibly different allowance reveals the stratum label. In protocols unfamiliar to the student, the same student later confirms primary candidates (5.4, step 3). So use one common allowance, unless the authors show that a stratum-specific allowance stays hidden from everyone who later builds or confirms. R1's rule does not conflict with the proposal's ban on samples that depend on throughput, because the choice is made before sampling and before any outcome.

5. **What to do with "little difference".**
   - *Positions:* R1 and R3 want the reading removed or shown to be reachable. R5 wants RQ1a restated as a one-sided question.
   - *Resolution:* Remove the reading (item 5). Section 6.4 already says that a claim in both directions needs positive scenarios. Keep the two-sided wording only if those scenarios are simulated. Otherwise restate RQ1a as one-sided, as R5 asks.

6. **Which estimand is principal.**
   - *Positions:* R5 wants RQ1b co-principal, with the design difference derived from the two stratum differences. R1 keeps RQ1a principal but adds an RQ1b precision target. R2, R3 and R4 accept RQ1a as principal.
   - *Resolution:* Keep RQ1a principal, because R4's novelty verdict rests on it. Add R1's precision target. Call RQ1b co-principal only if the allocation meets that target (item 6).

7. **Unresolved outcomes in the readiness check.**
   - *Positions:* R5 (W9) suggests moving the worst-case bounds into a sensitivity analysis, behind a primary analysis with a stated missingness assumption. R3 (W5) keeps the bounds and asks for a rule that sets the retained unresolved shares.
   - *Resolution:* Keep the bounds in the principal analysis. Iteration-2 item 9 settled this, and R3, who raised that item, still wants the bounds there. Use R3's 80% rule with a floor (item 7). That rule addresses R5's point that the 95% rule needs about 150 evaluations to reach 2%. If the rule still fails, the allocation does not launch, as section 8 already says.

8. **Readiness evidence based on the frame.**
   - *Positions:* R1, R3 and R5 ask for the V count and a rerun of V19 and V20. R2 and R4 also ask for finite-population simulations with construction that depends on difficulty.
   - *Resolution:* These do not conflict. Do both, as item 2 says. Neither needs the student.

9. **What feasibility evidence must exist before acceptance.** See my resolution of OQ1 below.

## Status of iteration-2 required changes

| # | Iteration-2 item | Status now | Reviewers' view |
|---|---|---|---|
| 1 | Blocking: design difference as principal estimand | **Resolved in the text; evidence open** | R1 (#1) "resolved as asked"; R2 (W4) "resolved as a design specification"; R3 (#4) resolved; R4 (W1) "partially resolved". The precision under a counted frame is open (items 2 and 5). |
| 2 | Blocking: measured human feasibility | **Still open** | R1 (#3) "partly resolved"; R2 (W3) and R4 (W3) "unresolved empirically"; R3 and R5 rate C7 fail. See item 10 and OQ1. |
| 3 | Blocking: audit-blind confirmation | Resolved | R2 (strengths: "Audit blindness now extends through confirmation"); R5 (strengths). No reviewer disputes it. |
| 4 | Major: repair contrast | Resolved | R1 (#4), R3 (#2), R4 (W2). |
| 5 | Major: monthly hour table | **Partly resolved** | The table exists and the extension has zero hours (R1 #3). The cap per protocol does not fit the stated rates: R1 (W1), R3 (W3), R5 (W2). See item 1. |
| 6 | Major: 63008 package | Resolved | R2 (W2) "resolved for the executable example". R1, R3, R4 and R5 list it as a strength. Human adjudication of the package is still outstanding, as the proposal says. |
| 7 | Major: plan for investigating natural implementations | Resolved | R2 (W1) "resolved at protocol level". R3 (Q5) asks what it can estimate (item 15). |
| 8 | Major: flaws missed by an earlier audit | **Partly resolved** | R3 (#3): the set is specified, but the available cases are not counted (item 15). |
| 9 | Major: adverse-bound rule in the power analysis | Resolved for planning | R3 (#1). V17 uses the two-V cap. The new "not confirmed" rule needs its own bound (item 11). |
| 10 | Major: training exposure | Resolved in the design | R1 (#2). R5 (W7) asks to extend the recall flag (item 12). |
| 11 | Major: reviewer model family | Resolved | R1 (#5), R3 (#7). |
| 12 | Major: development gate | Resolved | R1 (#7), R3 (#6). R5 (W3) raises a separate gap: there is no audit-blind evidence of rediscovery (item 9). |
| 13 | Major: allocation based on the frame | **Still open** | R1 (#8) and R3 (#5) "partly resolved"; R2 (W2), R4 (W1), R5 (W1). See item 2. |
| 14 | Major: reading RQ1a beside detection | Resolved as a rule | R3 (#4). But the "little difference" reading it governs cannot occur (item 5). |
| 15 | Minor: request construction | Mostly resolved | R1 (#6). R1 (Q3) and R5 (W8) ask for generation on the second request (item 13). |
| 16 | Minor: equivalence margin | Resolved | R3 (#8). |
| 17 | Minor: "better security" rule | Resolved | R3: the verdict was removed. |
| 18 | Minor: factual answers | Mostly resolved | R1 (strength 4) confirms the fix-scope count. R3 says its iteration-2 questions 1 and 3 to 6 are answered, and 2 and 7 are deferred. R1 (Q8) says two remain: the audit platforms and the recall-flag threshold (item 15). |
| 19 | Minor: reproducible simulation sources | Resolved | R1 (strength 5). I checked the hashes of the generator, the V19 and V20 scripts and their result files. All match `tools/MANIFEST.md`. |

### My resolution of open question OQ1

**Question.** At proposal stage, is the current treatment of feasibility acceptable? Or must the measured human development record exist before the proposal can be accepted?

**What the reviewers say:**
- **R1:** The record need not come first. But first fix the budget (W1) and the V count (W2), and confirm the student's participation with a date.
- **R2:** It approves a development phase. It withholds approval of the confirmatory plan until the record and a readiness analysis based on the frame both pass.
- **R3:** The record need not come first. But the plan must first be consistent with its own numbers (W3), and the rule for retained scenarios must be fixed (W5).
- **R4:** A bounded development phase is acceptable. It needs the record before it will recommend acceptance of the twelve-month programme.
- **R5:** The full record stays a launch requirement. But acceptance needs two things: a budget that holds at the middle rates, and one development case timed with the student.

**My resolution:**
1. **The full three-case record need not exist before acceptance.** R1, R3 and R5 say this directly. R2 and R4 accept approval of a development phase. If the full record had to come first, the month-1 launch gate in section 8 would serve no purpose.
2. **The plan must first be consistent with its own numbers.** A conditional acceptance makes sense only if the condition can be met. Today the proposal's own numbers say it cannot be met (items 1 and 2). Items 1, 2 and 7 must be done before acceptance. None of them needs the student.
3. **The condition needs a person who will meet it.** The student's written commitment, with dates, is required (item 10).
4. **One development case timed with the student is required.** Under this committee's rule, ACCEPT needs every score at 4 or more. R2 and R4 tie their 4 to measured human evidence. The smallest measurement that tests the largest unknown is one such case (R5's proposal). It is cheaper than the full record and moves C7. I ask R2 and R4 to say in iteration 4 whether one complete case, together with items 1, 2 and 7, meets their condition.
5. **If the student does not commit, the proposal cannot be accepted in any form.** In that case the authors should say so plainly. They should not submit another version that only schedules the work.
