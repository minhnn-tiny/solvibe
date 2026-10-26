# Meta-review, iteration 4

**Proposal:** "AI Agent Function-Body Replacements in Audited Solidity: Executable Vulnerability Comparisons with Historical Developer Code", version 25 (`proposal_workspace/iter_4/proposal.md`).

**Reviews:** R1 to R5, in `proposal_workspace/iter_4/reviews/`.

**What I checked myself.** I did not rerun any simulation script. I ran one short resampling and some arithmetic in memory, and I wrote no file.

- **Where the confirmation limit comes from.** The cost model (`tools/power_sim_v22.py`, line 21 and the `cost` function) sets the middle rates at 0.178 candidates per implementation and 1.0 hour per candidate, and its cost term is `op + cand * conf`. So the 0.178-hour limit in section 5.7 is the expected confirmation time per implementation. That average includes the many implementations that have no candidate at all. R1 and R3 read this correctly.
- **The budget after correcting the limit.** At the high candidate rate of 3/13 and 1.0 hour per candidate, one protocol costs 9 + 7 × 2.25 + 35 × (0.15 + 0.231) + 3.75 ≈ 41.8 student hours. For 22 protocols that is about 920 hours, which is 20 more than the 900 available. This matches R3.
- **The review reservation.** Section 8 divides each adjudicator's hours by the number of implementations that could produce a package. A package is the PoV, body-only correction and evidence sent to the two adjudicators. Even if all 121 hours went to the 770 main implementations, each would get at most 0.157 hours, about 9.4 minutes. At 0.5 hours per package and the high candidate rate, the main study alone needs about 770 × 3/13 × 0.5 ≈ 89 hours from each adjudicator.
- **How the simulator models working status.** In the V37 simulation script (`tools/power_sim_v37.py`), line 76 draws agent working status from two independent draws (0.9 and 0.8) that do not depend on the function. Line 77 draws vulnerability independently of working status. In `tools/power_sim_v35.py`, line 128 sets the historical working total to `S(~hu)`, so every resolved historical implementation counts as working. R1, R3 and R5 read this correctly.
- **Frame size.** The frame audit description (`evidence/frame_audit/README.md`) lists 70 audits. The simulations use frames of 200 protocols (`M = 200` in `tools/power_sim_v29.py`). I resampled the 25 strict N counts in the per-audit table (`evidence/frame_audit/strict/per_audit_strict.csv`) and drew 22 protocols with probability proportional to N count, capping certainty units. With 200 protocols, no protocol was selected with certainty. With 67 protocols, about 3.2 were. With 50, about 5.8 were. This matches R1.
- **Simulation numbers the reviewers quote.** The +0.10 power in the V33 results (`tools/power_results_v33.txt`, line 48) has a worst value of 0.395 and quartiles 0.51, 0.58 and 0.68. The V38 development firing rates (`tools/power_results_v38.txt`, lines 22–25) are 0.014 at (0, 0, 0.013) and 0.031 at (0, 0, 0.02). Both match what R1 and R3 quote. The V38 values in the proposal also match.
- **The development kit.** In the commitment form (`dev_case/commitment.md`), every field is blank and the signature line is empty. The timesheet (`dev_case/timesheet.csv`) contains only its header row.
- **The rediscovery results.** The results file (`evidence/rediscovery/RESULTS.md`, line 12) calls the match rates "upper bounds on confirmed rediscovery". R3 quotes this correctly.

## Actionability check

All five reviews score 3 or lower, so I checked all five.

| Review | Score | Example of a concrete required change | Result |
|---|---|---|---|
| R1 | 3 | W1: give the student 1.0 hour per candidate and each adjudicator 0.5 hours per package. Fund the totals at a high quantile of the candidate count. If a reserve still runs out, preregister random subsampling with recorded probabilities that enter the weights. R1 names W1, W2 and W6 as the changes that would raise its score to 4. | Pass |
| R2 | 3 | W1: supply the dated student commitment and one complete, probability-selected, student-timed development case under the proposed caps. The record must show the quality and outcome of the confirmation work. R2 says this would raise its score to 4. | Pass |
| R3 | 3 | W1 and W2: set confirmation and review limits per candidate and per package, provisioned at the high candidate rate of 3/13, and recheck the 900-hour and 121-hour bounds. In its overall section, R3 names W1, W2, W3 and W6 for a 4. Its answer to OQ1 lists only W1, W2 and W6. I treat the longer list as binding. | Pass |
| R4 | 3 | W1: submit one completed human development record. It must contain the dated commitment and an end-to-end timed case reconciled against the stated reservations. R4 says this would raise its score to 4. | Pass |
| R5 | 2 | W1: the completed development record, which R5 says would raise its score from 2 to 3. W2 to W4 each give a concrete change: new working-status settings in the simulations, a probability sample of candidates cut by the confirmation limit, and a preregistered criterion for adequate precision. | Pass |

No review is sent back.

One caution about R5. R5 says clearly what earns a 3. It says what earns a 4 only by implication: in its answer to OQ1, W2 to W4 "remain". In iteration 5, R5 should state which changes would earn a 4.

## R4 overlap check

R4 names eight prior papers. All eight are VERIFIED in the master index of searched papers (`lit/master_index.tsv`, *status* column). So I did not need to open any URL.

| Paper R4 names | Index row | Result |
|---|---|---|
| SolEval (EMNLP 2025) | `Peng2025-SolEval` | Confirmed |
| SolAgent (arXiv 2601.23009, 2026) | `Chen2026-SolAgent` | Confirmed |
| SecureVibeBench (ACL 2026) | `Chen2026-SecureVibeBench` | Confirmed |
| How Safe Are AI-Generated Patches? (Sajadi et al., arXiv 2507.02976, 2025) | `Sajadi2025-HowSafePatches` | Confirmed |
| The Illusion of Safety (Mahmud et al., arXiv 2607.00107, 2026) | `Mahmud2026-IllusionOfSafety` | Confirmed. The search notes (`lit/r1_L3_human_vs_ai.md`, `lit/r1_L2_repo_agent_benchmarks.md`) record that it controls for code length and test pass rate. They do not record the section number R4 cites (V-A4). That detail is [uncertain] to me. It does not change the verdict. |
| SolBehave (arXiv 2610.18745, 2026) | `Delvecchio2026-SolBehave` | Confirmed |
| SPLASH (arXiv 2610.26001, October 2026) | `Rahman2026-SPLASH` | Confirmed |
| RAPO-Sol (arXiv 2610.08429, October 2026) | `Wang2026-RAPOSol` | Confirmed |

**R4's answer to "same technique, same problem, same claim?" is No. I agree.**

- The closest paper to the new principal question is Mahmud et al. It compares human and AI code on the same tasks and confirms runtime violations by execution. It also accounts for test pass rate. But the differences are large:
  - its tasks are competitive-programming problems, not functions in audited repositories;
  - its generators are plain open-weight LLMs, not agents;
  - its checks are sanitizers and bounded model checking, not attacker violations under a threat model;
  - it has no probability sample of functions in a real codebase, and no attribution to one function body.
- SolEval and SolAgent judge security with Slither. SolBehave measures behavioural equivalence, not attacker violations. SecureVibeBench selects only historical failures. Sajadi et al. compare patches, without this sampling design. SPLASH has no historical baseline. RAPO-Sol is a training method.

One consequence matters for the revised claim. Making RQ1b principal moves the contribution closer to Mahmud et al. The proposal does not cite that paper or SolBehave. Item 12 asks for both. This bears on related work, not on condition (c).

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

The scores are the same as in iteration 3: 3, 3, 3, 3 and 2. That hides real progress:
- the frame is now counted;
- the "little difference" reading is gone;
- security and functional failure are separated;
- checks that endorse a flaw have a rule;
- the inference is validated over all 76 ordered rate vectors.

R1 and R3 now rate feasibility (C7) as a concern rather than a fail.

Two things kept the scores down.
- **The human evidence is still missing.** All five reviewers name item 10. The proposal itself says the committee requires it "before resubmission".
- **The budget fits only because averages became hard limits.** The confirmation and review limits were derived as averages over all implementations, then applied to each implementation as a ceiling. I checked this in the cost model. By the proposal's own rates, no single candidate can be confirmed or reviewed within these limits.

Item 10 alone would not lead to acceptance. By the reviewers' own answers to OQ1:
- R2, R3 and R4 would give 4 if the timed case shows the limits are workable;
- R1 also needs the frame-size rerun;
- R5 would move only from 2 to 3.

Ratings for this iteration:
- C2, C3, C5 and C8: all five pass.
- C1: R1, R2 and R4 pass; R3 and R5 concern.
- C4: R2 and R4 pass; R1, R3 and R5 concern.
- C6: R2 and R4 pass; R1, R3 and R5 concern.
- C7: R1, R2, R3 and R4 concern; R5 fail.

## Prioritized required changes

The labels mean:
- **Blocking:** the main claim cannot stand without the change.
- **Major:** acceptance needs it.
- **Minor:** it improves clarity or precision.

### 1. Blocking. The confirmation and review limits are averages, used as limits for each implementation.

**Raised by:** R1 (W1), R3 (W1, W2). R2 (W1), R4 (W1) and R5 (W1, W3) point to the same 0.178-hour figure.

**Problem.**
- The student's limit is 0.178 hours, about 11 minutes, per implementation. It covers confirmation, body-only correction, packaging and lock administration for up to three candidates. In the cost model this figure is 0.178 expected candidates × 1.0 hour. So an implementation that has one candidate gets about 11 minutes for work the plan prices at 30 to 90 minutes.
- Each adjudicator's reservation works out to at most about 9.4 minutes per implementation. The plan's own workload assumption is 0.5 hours per package.
- Under the section 6.2 rules, a candidate cut by the limit is "not confirmed", and a package whose review runs out of time is "unresolved". So the limits push both quantities that the power claim depends on:
  - recall falls below the 0.5 to 0.8 assumed in V37 (R3 W1);
  - unresolved shares rise toward 0.12 to 0.23, far above the retained limit of 0.013 for agents (R1 W1).
- Development step 5 does not catch the recall loss, because a cut is a legitimate recorded outcome (R1 W1, R3 W1).
- The loss may also differ by author. If one author's flaws are quicker to demonstrate, the limit counts more of them (R1 W1, R5 W3).

**Required change.** Replace the per-implementation limits in sections 5.7 and 8 with:
- 1.0 student hour per candidate, at most three candidates per implementation;
- 0.5 hours per package for each adjudicator, the same for every author.

Provision both totals at the high candidate rate of 3/13, and recheck the 900-hour and 121-hour bounds. If a reserve still runs out, preregister R1's rule: subsample the remaining candidates at random, record the probabilities and enter them in the weights.

My arithmetic gives about 920 student hours. Find the extra 20 hours in the schedule rather than dropping to 21 protocols. The power margin at 22 protocols is thin: the lowest lower bound in the retained region is 0.608. Dropping a protocol would require a new power check.

My arithmetic for review gives about 89 hours per adjudicator for the main study alone. That leaves about 32 hours for development, duplicate requests, seeds, controls and audit-assisted work. State each source's hours. If they do not fit, raise the ceiling.

### 2. Blocking. The student's dated commitment and one timed case that exercises confirmation and review.

**Raised by:** R1 (W6), R2 (W1), R3 (W9), R4 (W1), R5 (W1). This is iteration-3 item 10, still open.

**Problem.**
- The commitment form is blank, and the timesheet has only its header. I checked both.
- The student's statement of 2026-10-22 is not the written, dated commitment the committee asked for.
- Without one human-timed step, every limit in section 8 is still a planning number.
- R2 and R4 tie their 4 to this record alone. R1, R3 and R5 also need it.
- A case that produces no candidate would show only that construction and campaign operation fit. It would say nothing about confirmation or review (R1 OQ1, R3 OQ1).

**Required change.** Supply the signed, dated commitment, and one complete development case timed by the student. The case must:
- be drawn with the kit (`dev_case/draw_protocols.py`, `dev_case/sample_and_seal.py`);
- include probability-selected N functions;
- use the actual eligible roles and the limits from item 1;
- keep every failure in the record;
- record time per candidate for confirmation and per package for each adjudication (R3 W9);
- reconcile measured resource use against the reservations (R4 W1);
- state how each confirmation ended and why (R2 W1).

It must take at least one candidate through confirmation and both adjudications. If no natural candidate arises, use a seeded flaw from the pattern catalogue that is outside the discovery-gate reserve (R1 W6). Someone other than the student must insert the seed, so that the student stays blind to its location.

### 3. Major. A result without a directional claim has no stated reading, and the +0.15 target is not justified on substance.

**Raised by:** R1 (W3), R3 (W5, W6), R5 (W4).

**Problem.**
- The proposal never reports the expected RQ1b interval width (R1 W3, R3 W6).
- In the planning model, the historical detected rate on N functions is about 0.025 to 0.08. So +0.15 is a three- to seven-fold excess (R1 W3, R3 W5). I checked the model's rates (`tools/power_sim_v29.py`: historical N rate 0.05 or 0.10, recall 0.5 to 0.8).
- Power at +0.10 is 0.395 in the worst frame.
- Negative targets have power near zero, so the design cannot show that agents are safer.
- The rule that "withdraws the planned power statement" changes no inference once data exist (R3 W6).
- R3's run of the generator suggests that, at the null, the upper limit often falls below +0.10. If so, a null study could still rule out a large agent excess. I did not rerun this.

**Required change.** In section 6.3, pre-specify a reading of the upper confidence limit of RQ1b. The reading states:
- the largest agent excess consistent with the data;
- whether that excess lies below a stated margin.

Choose and justify the margin on substance before looking at simulated widths (R5 W4). For example, use the excess that doubles the historical detected N rate (R3 W5). Validate the reading in the final-frame check, with the margin as an exact condition and the same multiplicity rule as directional claims.

Report, for each frame:
- the historical and agent detected N rates at +0.15, and their ratio;
- the mean RQ1b half-width;
- power at +0.05 and +0.10;
- the share of studies whose upper limit falls below the margin at the null and at +0.05.

This reading replaces the rule that withdraws the power statement. Section 3 must say plainly that the study cannot conclude that agents are safer (R1 OQ2.2).

### 4. Major. The simulations never let working status depend on the function, and historical code always works.

**Raised by:** R5 (W2), R3 (W7). R1 (W4) gives the same evidence.

**Problem.**
- RQ1b compares rates among working implementations.
- Suppose agents fail more often on hard functions, and hard functions are more often vulnerable. Then the agents' working set is easier, and their rate falls for reasons that have nothing to do with security.
- Section 6.2 admits this can happen. The pilot saw it: Aider "wrote the bug but broke the function" (R3 W7).
- The generator cannot produce this, as I checked: lines 76–77 of the V37 script and line 128 of the V35 script.
- The final-frame check keeps the same working model (section 6.3).

**Required change.** Add generator settings with two features:
- historical implementations can fail ordinary checks;
- the agent working probability falls as the function's difficulty score rises, and that score is linked to vulnerability.

Recompute the exact conditional targets under these settings. Apply the error, coverage and power checks to them, in the rerun of item 7 and in the final-frame check.

### 5. Major. No comparison is made on the same set of functions.

**Raised by:** R1 (W4), R3 (W7). R1 makes it a condition of approving OQ2.1.

**Problem.** The D decomposition shows how much functional failure contributes. It does not compare the two authors on the same functions. R1 cites Shaw (VERIFIED, `Shaw2026-ComparedToWhat`), who shows that a confounder like code size can create or hide differences between human and AI code.

**Required change.** Preregister a secondary estimate restricted to functions where the historical body works and at least one attempt of the configuration works, with equal weight per function. Report how many functions it keeps, by stratum and configuration.

### 6. Major. Unresolved outcomes are simulated in the wrong units.

**Raised by:** R3 (W3). R1 (W1) describes the same effect.

**Problem.**
- Under the section 6.2 rules, the sources of unresolved outcomes that the time limits drive both need a package. An adjudicator cannot assess one, or review time runs out.
- So unresolved outcomes grow with the number of detected flaws. They therefore grow with the agent excess the study is trying to detect.
- For a positive claim, an unresolved agent package counts as not vulnerable. That removes exactly the evidence the claim needs.
- V37's four mechanisms draw unresolved status per implementation, per function, per protocol or from a function score. None of them depends on whether a package exists.
- In development, the diagnostic fires at 0.014 and 0.031 just outside the region, against up to 0.018 inside it. I checked these values in the V38 results.

**Required change.** Add a fifth mechanism in which unresolved status arises only among implementations with a package, at a rate per package for each author. Restate the retained region and the development diagnostic in units per package.

### 7. Major. The simulations use frames three to four times larger than the only listed frame.

**Raised by:** R1 (W2).

**Problem.**
- The only listed frame has 70 audits. At the replacement rate seen in the frame audit (8 of 33), about 53 would be usable.
- The simulations use 200 protocols. I reproduced R1's finding: with 50 to 67 protocols, about 3 to 6 of the 22 are selected with certainty, and the sampling fraction rises to between a third and a half.
- Sections 6.3 and 8 do not say how protocols selected with certainty enter the delete-one-protocol jackknife.
- If this fails at the month-2 final-frame check, the design returns to review only after the student's development month is spent.

**Required change.** Before the next submission, rerun the V37 checks with the frozen Holm level and multiplier on frames of 50 and 70 protocols. Resample them from the strict counts, and remove three development protocols first.

Include in this one rerun:
- the settings from items 4 and 6;
- a setting in which V construction fails while the pooled yield is adequate (R5, answer to OQ2.4).

State in section 6.3 how protocols selected with certainty enter the jackknife. One standard choice treats each as its own stratum with no between-protocol variance. State the expected size of the frozen frame (R1 Q2).

### 8. Major. Candidates the campaign did not process are not investigated.

**Raised by:** R5 (W3). R1 (W1) raises the risk that the limit favours one author.

**Problem.**
- Item 1 removes most cuts caused by time.
- The limit of three candidates per implementation remains. Candidates beyond it are "not confirmed".
- The natural investigation samples broad campaign categories. It does not guarantee that it looks at any campaign whose candidate list was cut.

**Required change.** Within the existing 120 auditor hours for natural investigation, make "campaign whose candidate list was cut" a separate sampling category, by author and stratum. Give the sampled cases an extended independent confirmation. Report a weighted estimate of how the principal contrast would change.

### 9. Major. The pooled construction warning cannot see V construction fail.

**Raised by:** R1 (W5). R5 and R4 raise it in their answers to OQ2.4. R3 (OQ2.4) asks that the limitation stay stated.

**Problem.**
- Every function gets 2.25 construction hours, and the reason is sound: different allowances could reveal the stratum.
- An earlier version of this proposal priced V construction at 4 to 8 hours.
- RQ1b barely notices poor V construction, because V is 1.5% to 2.9% of the frame. But the descriptive flagged-only comparison, the audit-assisted rediscovery and one source of detection evidence all need constructed V functions.
- The warning pools V and N, and section 6.8 admits it cannot see this failure.

**Required change.** Add a stratum V rule to development step 7: if V functions were sampled across the three cases and none was built within the limit, return the design to review. Report V construction time against the limit in the timed case.

### 10. Minor. The discovery gate counts matches, not confirmed flaws.

**Raised by:** R3 (W4).

**Problem.** The only recall evidence is candidate matching. The results file calls it an upper bound on confirmed rediscovery. The gate in section 5.9 does not require execution or adjudication.

**Required change.** In section 5.9, count a gate rediscovery only if it is confirmed by execution and passes both adjudications within the item-1 limits.

### 11. Minor. The research questions overstate what RQ1a and RQ1b can answer.

**Raised by:** R3 (W5, W8). R3 makes this a condition of approving OQ2.1.

**Problem.**
- V is 1.5% to 2.9% of the frame, so RQ1b is mostly a comparison on functions the audit did not flag.
- RQ1a has a largest mean half-width of 0.711 and no calibrated interval. Yet it is still listed as a research question.

**Required change.** Remove RQ1a from the numbered research questions in section 6.1. Report the V-only estimates as a descriptive table with sample sizes. State in section 3 that V makes up about 1.5% to 2.9% of the frame, so RQ1b is mostly a comparison on unflagged functions.

### 12. Minor. Related work omits the paper closest to the new principal question.

**Raised by:** R4 (overlap table and answer to the same-claim question). R3 (W5) cites Mahmud et al.

**Required change.** Add Mahmud et al. (*The Illusion of Safety*) and SolBehave to section 7 and its table. State the differences R4 gives: competitive-programming tasks and plain LLMs for Mahmud et al., and behavioural equivalence rather than attacker violations for SolBehave.

### 13. Minor. Short factual answers.

**Raised by:** R1 (Q1, Q3, Q4, Q5), R3 (Q2, Q3, Q4, Q5), R4 (W1), R5 (W1).

**Required change.** Answer each of these in Appendix B:
- What share of cut candidates would development count as failure (R1 Q1)? With item 1 this may become moot.
- What share of audited High and Medium findings does the one-body rule exclude, by severity (R1 Q3)?
- What does the development diagnostic add as a launch gate, beyond reporting unresolved counts (R1 Q4)?
- What is the compute cost per implementation for the agents and reviewers, and who funds it (R1 Q5, R4 W1, R5 W1)?
- How much LLM help may confirmation use, which part of the limit is human time, and how is that LLM kept away from audit material (R3 Q2)?
- How many adjudicator hours does each source receive (R3 Q3)? Item 1 also asks this.
- Will the final-frame check include a protocol-effect standard deviation near 0.9 (R3 Q4)?
- Is the recall flag also applied to reviewer candidate lists (R3 Q5)?

## Disagreements among reviewers

1. **Is item 10 the only remaining obstacle?**
   - *Positions:* R2 and R4 say that apart from item 10 the proposal meets the bar for a 4. R1, R3 and R5 say it does not, because of design problems that need no student.
   - *Resolution:* I side with R1, R3 and R5. The confirmation and review limits are averages used as limits, and I checked this in the cost model. The working-status model and the frame size are also as R1, R3 and R5 describe. These need arithmetic, text and one rerun (items 1, 4 to 7). Item 10 alone would also not reach unanimity: R5 has said it would move only to 3.

2. **Can a timed case replace the change to the limits?**
   - *Positions:* R1 and R3 accept either evidence from a timed case or a change in the limits. R2 and R4 think the 0.178-hour limit "may be workable" with automation.
   - *Resolution:* Change the limits regardless (item 1). The limit was derived as an expected value over all implementations. One case has at most a handful of candidates. It cannot show that about 11 minutes suffices for every implementation that has a candidate. Automation could justify a smaller allowance per candidate later. But only measured time can show that, and the case in item 2 should measure it.

3. **How to provision the corrected limits.**
   - *Positions:* R1 funds at a high quantile of the candidate count and adds random subsampling as a backstop; its expected cost equals the current cost. R3 provisions at 3/13, which adds about 20 hours or removes one protocol.
   - *Resolution:* Combine them, as item 1 does. Keep 22 protocols and find the 20 hours. The lowest power lower bound in the retained region is 0.608, so one fewer protocol would likely fail the 0.60 requirement.

4. **When the new simulation settings must run.**
   - *Positions:* R1 wants the realistic-frame rerun before acceptance. R3 (W3, W7) and R5 (W2) ask only that the new settings be added to the final-frame check.
   - *Resolution:* Run them now, in one rerun (item 7), and keep them in the final-frame check. R1 and R3 both point out the cost of the other order. A failure found in month 2 sends the design back to review after the student's development month is spent.

5. **What happens to RQ1a.**
   - *Positions:* R3 wants it removed as a research question. R1, R2, R4 and R5 accept it as a secondary descriptive analysis.
   - *Resolution:* Both positions keep the same numbers, so I take R3's form: a descriptive table, not a numbered research question (item 11). The proposal already refuses to present an RQ1a interval as validated.

6. **What makes a result without a directional claim informative.**
   - *Positions:* R3 proposes reading the upper limit against a margin such as +0.10. R1 asks for the smallest agent excess the design would rule out. R5 asks for a precision criterion justified independently of what is affordable.
   - *Resolution:* Do all three in one reading (item 3). Fix the margin on substance first, as R5 asks. Then report what the design achieves against it, as R1 and R3 ask. If the design rarely achieves it, section 3 says so. The committee then judges whether the remaining contribution is enough.

7. **What the unresolved-outcome diagnostic is worth.**
   - *Positions:* R1 (Q4) asks what it adds as a launch gate. R3 says it is stated in the wrong units (W3) and that withdrawing a power statement changes no inference (W6). R2, R4 and R5 accept it as a warning only.
   - *Resolution:* Keep it as a warning and as a development launch condition. Restate it in units per package (item 6). Replace the main-study withdrawal rule with the upper-limit reading (item 3). It must never be presented as evidence that the study lies inside the region. All five agree on that.

8. **C1, novelty.**
   - *Positions:* R1, R2 and R4 pass. R3 and R5 rate it a concern: the selection effect that motivated the project is no longer estimated, and novelty now depends on an informative result.
   - *Resolution:* C1 passes. R4's search and my check of condition (c) find no paper with the same technique, problem and claim. The R3 and R5 concern is about how informative the result will be. That belongs under C6 and is handled by items 3 and 11.

9. **C4, soundness of claims.**
   - *Positions:* R2 and R4 pass. R1, R3 and R5 rate it a concern.
   - *Resolution:* The concern stands. It rests on mechanisms I checked: the cost model behind the limits, and the working-status model in V37 and V35. R2 and R4 do not discuss these mechanisms. Items 1, 4, 5 and 6 address it.

10. **C6, evaluation.**
    - *Positions:* R2 and R4 pass. R1, R3 and R5 rate it a concern.
    - *Resolution:* The concern stands. The RQ1b width is unreported, and the simulated frames are larger than the listed one, which I reproduced. Items 3 and 7 address it.

11. **C7, feasibility.**
    - *Positions:* R5 rates it a fail. R1 to R4 rate it a concern.
    - *Resolution:* Concern, for the plan with item 1 applied. The corrected budget is within about 2% of the student ceiling. The rating becomes fail if the student does not commit. Only measured human time can raise it to pass.

## Status of iteration-3 required changes

| # | Iteration-3 item | Status now | Reviewers' view |
|---|---|---|---|
| 1 | Blocking: the fixed minimum study does not fit its budget rule | **Partly resolved** | R1 (status W1) "partly resolved"; R3 (status 3) "resolved in the arithmetic"; R4 (W2) "partially resolved"; R2 (W1) "unresolved empirically". The sums fit only because averages became limits (new item 1). R1 notes that no rule picks an allocation from measured month-1 costs. |
| 2 | Blocking: count the V distribution and rerun the simulations | **Resolved** | R1 (status W2), R3 (status 4), R2 (W2) "addressed", R4 (W1) "superseded by an acceptable scope change". A new problem is the frame size (item 7). |
| 3 | Blocking: separate security from functional failure in D | **Resolved** | R3 (status 2) checked the identity. A new problem is what conditioning on working outputs means (items 4 and 5). |
| 4 | Major: checks that endorse the flaw | **Resolved** | R1 (status W3). |
| 5 | Major: "little difference" reading | **Resolved** | R1 (status W4), R3 (status 1). |
| 6 | Major: RQ1b precision target | **Partly resolved** | R1 (status W6) "resolved in form only". R3 (W5, W6) and R5 (W4) say the target is not justified and the RQ1b width is unreported (item 3). |
| 7 | Major: rule for retained scenarios | **Resolved as a procedure, through a requested change** | R3 (status 5). All five approve replacing certification with a stated region (OQ2.3). R3 (W3) says the region uses the wrong units (item 6). |
| 8 | Major: recall gap and the design difference | **Resolved** | R1 (status W5). |
| 9 | Major: audit-blind rediscovery | **Resolved at candidate level** | No reviewer disputes it. R3 (W4) notes that matches are upper bounds and asks the gate to require confirmation (item 10). |
| 10 | Major: student commitment and one timed case | **Still open** | All five: R1 (W6), R2 (W1), R3 (W9), R4 (W1), R5 (W1). See item 2. |
| 11 | Minor: candidates cut by the limit | **Resolved as asked** | R3 (status 6). The 11-minute limit makes cuts common, so items 1 and 8 replace this concern. |
| 12 | Minor: recall flag and reproduction of the historical body | **Resolved** | No reviewer disputes it. R3 (Q5) asks about reviewer lists (item 13). |
| 13 | Minor: generation on both duplicate requests | **Resolved** | No reviewer disputes it. |
| 14 | Minor: simulation history | **Resolved** | R3 (strength 2) finds every number matches its file. |
| 15 | Minor: factual answers | **Mostly resolved** | R3: its iteration-3 questions 3 to 6 are answered, question 1 (the post-cutoff subset) is deferred and question 2 is partly answered. R1 (Q2, Q5): frame size and compute remain open (items 7 and 13). |

### My resolution of OQ1 (the commitment and the timed case)

- **Apart from item 10, the proposal does not meet the bar for a unanimous 4.** R2 and R4 say it does. R1, R3 and R5 say it does not, for reasons I checked (items 1, 4 and 7).
- **If item 10 were supplied and showed the limits workable:**
  - R2, R3 and R4 would give 4;
  - R1 would give 4 only with the frame-size rerun;
  - R5 would give 3.
  So item 10 alone does not lead to acceptance.
- **The case must exercise confirmation and review.** A case that ends with no candidate does not test the limits that matter most. Item 2 says how to make sure it does. Filling in dates alone does not count (R4).
- **One case before acceptance, three before launch.** All five reviewers now accept this. R4 has moved from its earlier request for all three cases.
- **The oral statement is not enough.** The student's answer of 2026-10-22 is not the written, dated commitment. I repeat the iteration-3 resolution. If the next version again lacks the commitment and the case, R2 and R4 have said they stay at 3, so acceptance is impossible. In that case the authors should say so plainly rather than submit another version that only schedules the work.

### My resolution of OQ2 (the four requested changes)

1. **RQ1b principal, RQ1a descriptive: approve, with conditions.** All five approve. In iteration 3, I kept RQ1a principal because R4's novelty verdict rested on it. R4 has now assessed RQ1b on its own and still finds no paper with the same technique, problem and claim. So that reason is gone. Conditions:
   - item 5 (the comparison on the same functions, R1);
   - item 11 (state the V share and drop RQ1a as a numbered question, R3);
   - keep W and D beside every headline RQ1b result;
   - keep the ban on causal or paired-new-flaw readings (R2, R4).
2. **Power 0.60 at +0.15: approve, with conditions.** All five approve, with conditions. This is a stated trade between cost and informativeness, not an equivalent of the former 0.80 design (R4). Conditions:
   - item 3 (a pre-specified reading of the upper limit, the ratio table and a margin justified on substance);
   - a sentence in section 3 that the design cannot show agents are safer.

   A result without a directional claim must never be read as equivalence.
3. **Conditional readiness for unresolved outcomes: approve, with conditions.** All five approve removing certification. Three development protocols cannot certify rates near 0.01. Adverse bounds stay primary, and error and coverage are checked outside the power region. So a departure costs power, not validity. Conditions:
   - item 1 first, because the current review limits would make unresolved outcomes common by design (R1);
   - item 6 (a mechanism tied to packages and units per package, R3);
   - item 4 (working-status settings, R5);
   - the diagnostic stays a warning and never serves as evidence of being inside the region (R2, R4, R5).

   The committee does not require the empirical guarantee that the rebuttal says this revision cannot give.
4. **Descriptive construction yields with a pooled warning: approve, with conditions.** All five approve. R3 approves without conditions. At most three V functions cannot certify a yield. Conditions:
   - item 9 (a stratum V stop rule);
   - the low-V-yield setting in item 7 (R5);
   - V and N yields reported separately by protocol (R2, R4).

   The proposal already keeps two things that must stay. Missing staff never makes a function unconstructible (R2). Failure to supply the procedure is recorded as a deviation.
