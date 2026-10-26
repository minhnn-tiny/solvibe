# Meta-review, iteration 2

**Proposal:** "AI Agent Function-Body Replacements in Audited Solidity: Executable Vulnerability Comparisons with Historical Developer Code", version 11 (`proposal_workspace/iter_2/proposal.md`).

**Reviews:** all five are in `proposal_workspace/iter_2/reviews/`.
- R1: SE PC member
- R2: security PC member
- R3: evaluation expert
- R4: novelty hunter
- R5: general PC member

**What I checked myself.** I checked these against the cited files:
- the arithmetic of the person-hour table;
- the binomial pass rates for the month-one gate;
- R3's rates behind the equivalence margin;
- the quotes from the 63008 files;
- the reviewer models used in the two pilots;
- the calibrated half-width in the calibration results for the design comparison (`tools/power_results_v11_calib.txt`);
- line 53 of the RQ1 data generator (`tools/power_sim_v8.py`).

All of them match what the reviewers say. I did not rerun any simulation. Where I use R3's reruns, I say so.

## Actionability check

All five reviews score 3, so I checked all five. Each one names concrete changes that would raise its score.

| Review | Score | Example of a concrete required change | Result |
|---|---|---|---|
| R1 | 3 | W3: add a month-by-month table of student hours at 150 hours a month. It must place every planning row, give a separate row for running generation, discovery and replay, and state paper 2's student hours. All 8 weaknesses end in a required change. The review names W1 to W3 as the changes that would raise its score to 4. | Pass |
| R2 | 3 | W2: complete the 63008 evidence package. It needs victim-entitlement and backing assertions, a correction to the target body only, a record of capital and ordering, and the attack rerun with H-02 corrected. All 4 weaknesses end in a required change. The review names W1 to W3 for a 4. | Pass |
| R3 | 3 | W1: rerun the calibration and power analysis with the adverse-bound rule as the decision rule. Use unresolved rates from 0 to 0.10 that may differ by author, and add a launch criterion on the unresolved rate. All 8 weaknesses end in a required change. The review names W1 to W3 for a 4. | Pass |
| R4 | 3 | W3: complete the timed end-to-end development pilot. It must include probability-selected N functions, failures kept in the record, and real human adjudication. Then replace the assumed budget with measured throughput. All 3 weaknesses end in a required change. The review names W3 and W1 as its route to a higher score. | Pass |
| R5 | 3 | W2: specify and enforce a primary-confirmation workflow. Attack completion and correction would use only the originating campaign's materials. Audit-derived help would be recorded in the secondary analysis only. All 5 weaknesses end in a required change. The review names W1 and W4. | Pass |

No review is sent back.

## R4 overlap check

R4 names nine prior papers. All nine are VERIFIED in the master index of searched papers (`lit/master_index.tsv`, *status* column). So I did not need to open any URL myself. The title, venue and arXiv number R4 gives match the index row each time.

| Paper R4 names | Where checked | Result |
|---|---|---|
| SolEval (EMNLP 2025) | VERIFIED, row `Peng2025-SolEval` | Confirmed |
| SolAgent (arXiv 2601.23009) | VERIFIED, row `Chen2026-SolAgent` | Confirmed |
| SecureVibeBench (ACL 2026) | VERIFIED, row `Chen2026-SecureVibeBench` | Confirmed |
| How Safe Are AI-Generated Patches? (Sajadi et al., arXiv 2507.02976) | VERIFIED, row `Sajadi2025-HowSafePatches` | Confirmed |
| The Illusion of Safety (arXiv 2607.00107) | VERIFIED, row `Mahmud2026-IllusionOfSafety` | Confirmed |
| TestPrism (arXiv 2610.12289) | VERIFIED, row `Li2026-TestPrism`. It is not in the literature review (`lit_review.md`), but it is in the index. | Confirmed |
| ImpossibleBench (ICLR 2026) | VERIFIED, row `Zhong2026-ImpossibleBench` | Confirmed |
| On the Risks of using LLM-Generated Tests for Regression Testing (arXiv 2610.11835) | VERIFIED, row `Charoosaei2026-FaultEnforcingTests` | Confirmed |
| SpecGuard (arXiv 2610.09159) | VERIFIED, row `Biyani2026-SpecGuard`. The literature review quotes the same session-fixation example that R4 cites. | Confirmed |

**R4's answer to "same technique, same problem, same claim?" is No. I agree.**

- **Paper 1.** No verified paper samples flagged and unflagged Solidity functions with known probabilities, and none compares the flagged-only estimate with the weighted estimate using executable, function-attributed evidence.
  - SolEval and SolAgent judge security with static analysis.
  - SecureVibeBench selects only historical failures.
  - Sajadi et al. and The Illusion of Safety compare human and AI code without this sampling design.
- **Paper 2.** The margin is narrow.
  - ImpossibleBench, the fault-enforcing tests paper and SpecGuard together already show three things: agents follow wrong tests, such tests keep faults in place, and following them can remove a security defense.
  - What remains new is the matched contrast between security and ordinary wrong assertions, with PoV evidence and hidden attacks.
  - That remainder depends on fixing the contrast (item 4 below). If the fixed contrast is null, paper 2 shows for Solidity what these papers already show in general.

## Decision

| Review | Score |
|---|---|
| R1 | 3 |
| R2 | 3 |
| R3 | 3 |
| R4 | 3 |
| R5 | 3 |

Mean: 15 / 5 = **3.0**.

| Condition | Holds? |
|---|---|
| (a) Every score is at least 4 | **No.** Every score is 3. |
| (b) The mean is at least 4.0 | **No.** The mean is 3.0. |
| (c) R4 reports no prior work with the same technique, problem and claim | **Yes.** R4 answers No, and I agree. |
| (d) The AC concurs | Does not apply, because (a) and (b) fail. |

**Result: NOT ACCEPT.**

The revision is a real improvement. The mean rose from 2.4 to 3.0. All five reviewers now agree on every rating criterion:
- pass on C2, C3, C5 and C8;
- concern on C1, C4, C6 and C7.

## Prioritized required changes

The labels mean:
- **Blocking:** the main claim cannot stand without the change.
- **Major:** acceptance needs it.
- **Minor:** it improves clarity or precision.

### 1. Blocking. Paper 1's stated contribution is a secondary analysis with wide intervals.

**Raised by:** R1 (W1), R2 (W4), R4 (W1), R5 (W1).

**Problem.**
- Section 3 calls the comparison between the V-only and weighted estimates paper 1's key insight. Section 7 calls it the first contribution.
- But Section 6.3 makes it secondary "unless separately included in the preregistered multiplicity plan."
- At 15 protocols, its calibrated mean half-width is 0.252 (the calibration results for the design comparison, `tools/power_results_v11_calib.txt`; I checked the file).
- When the true difference is 0.18 to 0.26, intervals exclude zero in only 25% to 48% of simulated studies (Section 6.4).
- The only primary test, D for two configurations, has power of 0.13 to 0.38 for the smaller differences.
- So the likely paper has an inconclusive primary test, and its headline rests on a wide secondary interval. At that width, the sentence "A result showing little difference is informative" (Section 3) does not hold.

**Required change.** Make the design difference for each configuration a principal estimand in the preregistered multiplicity plan. Then:
- State the smallest difference that would matter to someone building a benchmark.
- State the largest half-width that would still be useful.
- Choose the allocation (protocols, V functions per protocol, attempts) that meets that half-width within the measured budget.
- Call a result "little difference" only when the calibrated interval excludes that smallest difference.
- If no affordable allocation meets the target, stop presenting the design comparison as paper 1's contribution.

### 2. Blocking. The feasibility case still rests on assumed hours.

**Raised by:** R2 (W3), R4 (W3), R5 (W4). R1 (W3) and R3 (C7 rating) raise the same budget concern. This is the still-open part of iteration-1 item 1.

**Problem.**
- Iteration 1 asked for at least three timed development cases, with people doing every human-review step.
- The rebuttal (item 1) says: "These measurements remain outstanding."
- Section 8 still labels every unit cost an assumption. It also says the pilot's human-review steps were done by LLM subagents.
- Three reviewers now make this measurement a condition for a higher score.

**Required change.** Complete at least three development cases to the full standard of Sections 4 and 5, with:
- a person doing every designated human-review step;
- at least one probability-selected set of N functions;
- failures kept in the timing record.

Then replace the assumed rows of the person-hour table in Section 8 with the measured hours, before the next submission.

### 3. Blocking. An audit-exposed person confirms the primary candidates.

**Raised by:** R5 (W2). R2 asks the same thing (Question 4). I rate it Blocking for the reasons below.

**Problem.**
- Section 5.4 has the student open the audit of every protocol after the blind commit, to build PoVs and function-only corrections.
- The person-hour table in Section 8 then gives the student 66 to 363 hours of "candidate confirmation by a person".
- The timeline puts construction in months 2 to 5 and confirmation in months 5 to 7.
- So, as written, every primary candidate is turned into a working attack and a correction by someone who has read that protocol's audit. That person can rescue a weak blind candidate on a historical V function, because they already know the flaw.
- Blinded adjudication comes later and cannot undo this.
- The primary endpoint is defined by audit-blind discovery, so the main claim cannot stand until this is fixed. The fix is a staffing rule, so it should be cheap.

**Required change.** Add a confirmation rule for the primary endpoint and add this role and its hours to Section 8. The rule:
- A person who has not read that protocol's audit, fix commits or audit-derived PoVs does the confirmation work: completing the attack, writing the function-only correction and checking attribution.
- That person uses only the originating campaign's materials and the permitted context.
- A candidate confirmed with any audit-derived help counts only in the secondary audit-assisted view.

### 4. Major. Paper 2's security-specific contrast comes out positive for any agent that simply obeys tests.

**Raised by:** R1 (W4), R3 (W2), R4 (W2), R5 (W5). R2 disagrees (see disagreement 1).

**Problem.**
- Every arm in Section 6.6 measures whether the vulnerability is kept.
- A wrong security assertion endorses the vulnerability. A wrong ordinary assertion endorses a different error. So an agent that obeys every wrong test gives θ > 0.
- R3 shows that the paper-2 power code hides this. In `contrast_power` (`tools/power_sim_v10.py`), both assertion types get the same +0.5 and −0.5 effects.
- R1 adds that in the repair arms, only the security arm has a shown failing test that contradicts its wrong assertion.
- R5 adds that the two wrong assertions can differ in repair effort, in overlap with the target code, and in how much they conflict with the supplied evidence.

**Required change.** Rebuild the ordinary arm to mirror the security arm, and test θ on a matched outcome:
- In both arms, the primary outcome is whether the final code keeps the behavior the wrong assertion endorses. For a security assertion that is the vulnerability. For an ordinary assertion it is the wrong output.
- Give both arms matched contrary evidence: the shown PoV in the security arm, and a shown failing test derived from the specification in the ordinary arm.
- Admit a pair of assertions only after a recorded check that both concern the same target function and need comparable repair effort.
- Keep vulnerability retention as the security endpoint for the security arms.

### 5. Major. The hour budget does not fit the months at pessimistic rates.

**Raised by:** R1 (W3).

**Problem.** I checked R1's arithmetic.
- At 15 protocols, the rows of the person-hour table add up to 756 to 1,443 hours. The proposal writes this as "726 to 1,413, plus 30".
- The construction rows alone add up to 450 to 840 hours. Months 2 to 5 hold about 600 student hours at 150 a month.
- At the pessimistic end, 1,443 hours plus the 357-hour reserve uses the whole 1,800-hour year. That leaves paper 2 no student hours.
- Running 900 generation attempts and 1,050 discovery campaigns has no row. It draws on the same reserve as the development work.

**Required change.** Add a month-by-month table of student hours against 150 hours a month. It must:
- place every row of the planning table;
- add a separate row for running generation, discovery and replay;
- add the month-one development work;
- state paper 2's student hours, writing zero if there are none.

### 6. Major. The 63008 worked example still does not meet the proposal's own standard.

**Raised by:** R2 (W2). R4 (W3) and R5 (W4) also note it. This is iteration-1 item 16.

**Problem.** I checked R2's evidence:
- The reward PoV (`pilot/tasks/63008/pov/PoV63008_StealRewards.t.sol`) ends with `assertGt(profitInEth, 0, ...)`. That asserts attacker profit, not victim loss.
- The fix check in the 63008 loss record (`pilot/tasks/63008/loss_estimate.json`) replaces the whole file `src/libraries/TickIterator.sol` with the version from `c01b6c7`.
- The copy of the audit report (`pilot/tasks/63008/extension/report.md`) depends on H-02 and on winning the top-of-block swap.
- Section 5.11 says: "That package has not been completed."

**Required change.** Complete the 63008 evidence package. It needs:
- executable assertions of victim entitlement and backing;
- a correction to the target function body only, which preserves functionality;
- a record of attacker capital and transaction ordering;
- the attack outcome with H-02 corrected independently.

### 7. Major. Validation on natural flaws has no sampling plan.

**Raised by:** R2 (W1), R5 (W3).

**Problem.**
- Section 5.9 promises that two auditors investigate a probability sample of natural implementations.
- But Section 8 leaves the count E open and gives only "about 100 auditor hours".
- The 60 seeded pairs measure inserted patterns, not natural flaws.

**Required change.** Turn the 100 auditor hours into a stated plan with:
- a count E;
- sampling probabilities;
- a minimum count in each cell of author by stratum by campaign result;
- a fixed investigation budget per implementation;
- the expected uncertainty of the disagreement between campaign and auditors, by author;
- a rule for how the results set the sensitivity ranges in Section 6.5.

### 8. Major. Nothing measures how well the campaign finds flaws that an audit missed.

**Raised by:** R3 (W3). This is related to R2 (W1).

**Problem.**
- About 95% of the simulated frame is stratum N.
- Historical N code has passed an audit, so its remaining flaws are the ones the auditors missed.
- None of the three validation sources measures recall on such flaws:
  - seeds are equally hard in both authors' code, by design;
  - blind rediscovery uses flaws the auditors found;
  - at the planning rates, the auditor sample would meet about one historical N flaw per 20 to 50 implementations.
- So the sensitivity range for historical N code in Section 6.5 will be a guess.

**Required change.** Add a small validation set of flaws that an earlier audit of the same code missed and a later review found, for example in a later contest, a mitigation review or a bounty report. Run the blind campaign on the code before the fix. Use its rediscovery rate to set the range for historical N code in Section 6.5. Count the available cases during the month-one frame refresh, because R3 does not know how many exist [uncertain].

### 9. Major. The power analysis leaves out the decision rule for unresolved outcomes.

**Raised by:** R3 (W1). This follows up iteration-1 item 13.

**Problem.**
- Section 6.2 requires every directional claim to survive the adverse bound.
- The generator produces no unresolved outcomes.
- R3 reran the selected 15-protocol procedure with the adverse bound. With 2% of outcomes unresolved, the lowest configuration power for the larger differences fell from 0.55–0.92 to 0.27–0.54. With 5% unresolved, it fell to 0.05–0.13.
- I did not rerun this.

**Required change.**
- Rerun the Section 6.3 calibration and power analysis with the adverse-bound rule as the decision rule.
- Use unresolved rates from 0 to 0.10 that may differ by author.
- Add to the month-two launch criteria the largest unresolved rate at which the core keeps useful power.

### 10. Major. Training exposure can differ between strata.

**Raised by:** R1 (W2).

**Problem.**
- A V function has a public audit report and a public fix. An N function has neither.
- An agent that saw them in training can avoid the historical bug in V functions by recall. That inflates the design difference.
- Section 5.3 is right that dates cannot prove the code was unseen. But a report or fix published after a model's training cutoff cannot be in that model's training data.
- Section 5.3 already records these dates, but no analysis uses them.
- In the pilot, two configurations wrote "the same line as the human fix `c01b6c7`" (the 63008 agent results, `pilot/tasks/63008/feature_tasks/results.md`).
- Both papers R1 cites are VERIFIED in the master index: Al-Kaswan et al. (MSR 2026) and Liang et al. (ICSE-SEIP 2026).

**Required change.**
- For each V function, record whether its audit report and its fix commit were public before each pinned model's training cutoff.
- Preregister the V-stratum D difference, and the design comparison, separately for functions whose report and fix appeared after both cutoffs.
- Report how many such functions the frame contains at month two.

### 11. Major. The LLM reviewers may share a model family with the agents they review.

**Raised by:** R1 (W5), R3 (W7).

**Problem.**
- Section 5.7 only reports this relationship.
- In the pilots, the reviewers were a Claude model and a GPT model. So each agent's code would be judged by one reviewer from its own family, and the historical code by neither.
- Both papers cited on this bias are VERIFIED in the master index: Panickssery et al. (NeurIPS 2024) and Li et al. (ICLR 2026).

**Required change.**
- Name the two primary reviewers before the month-two freeze.
- Preregister a secondary D analysis for each configuration that uses fuzzing plus only the reviewer from the other model family, on both the agent and the historical implementations.

### 12. Major. The month-one detection gate is too small to tell a weak campaign from an adequate one.

**Raised by:** R1 (W7), R3 (W6).

**Problem.** I checked the binomial numbers.
- With eight qualifying cases and a pass mark of four, a campaign with true recall 0.3 passes with probability 0.19.
- A campaign with recall 0.5 fails with probability 0.36.
- Each revision round gives a weak campaign another chance to pass.

**Required change.** Before month one:
- fix the development set at six or more qualifying flaws, from protocols outside the sampling frame;
- fix the maximum number of revision rounds;
- set the pass mark so that a campaign with recall 0.3 passes with probability at most 0.10, for example 4 of 6 or 5 of 8;
- report the pass probability at recall 0.3, 0.5 and 0.7.

### 13. Major. The design-comparison simulation assumes every protocol has V functions.

**Raised by:** R1 (W8), R3 (W5).

**Problem.**
- Line 53 of the RQ1 data generator (`tools/power_sim_v8.py`) reads `NV = 2 + rng.poisson(2, P)`. So every simulated protocol has at least two V functions. The refreshed frame allows protocols with none.
- R3 reran the simulation with V counts drawn from a Poisson distribution with mean 1.5. The raw half-width grew to 0.254–0.303. At a difference of 0.33, the rate of excluding zero fell from 0.73 to 0.47.
- Section 6.4 also allows four V functions only if the development cases estimate the design difference at 0.15 to 0.35. Three development cases cannot estimate that.

**Required change.**
- Rerun the design-comparison simulation with the V counts measured in the refreshed frame after all exclusions, including protocols with no V function.
- Choose two or four V functions per protocol from that rerun and the measured cost alone.
- State the smallest number of sampled V functions at which "the core can show a large design difference" still holds.

This rerun feeds item 1.

### 14. Major. A small design difference may only mean that the blind campaign missed the audit flaws.

**Raised by:** R3 (W4).

**Problem.**
- With own-campaign labels, the historical V rate is the true rate times the campaign's sensitivity on that code.
- Weak rediscovery pulls the V-only estimate toward the weighted one. The difference then shrinks for a reason that has nothing to do with sampling.
- When detection is good, the sign is predictable, because V functions are chosen for historical failure. So the informative part is the size, read together with detection.

**Required change.** Preregister three things:
- the design comparison is reported beside the blind rediscovery rate for historical V flaws (Section 5.8);
- it is also computed with the audit-supplemented labels, the third view in Section 5.8;
- a small difference is called informative only when that rediscovery rate is high.

### 15. Minor. Who writes the request is not controlled.

**Raised by:** R1 (W6).

**Problem.**
- The builder changes with the student's prior exposure, so builder and protocol are confounded.
- In the pilot, the request decided the outcome: 13 of 13 compiled runs had the bug when the request described the vulnerable design, against 3 of 15 when it stated the corrected rule.

**Required change.**
- Freeze a written request template before sampling.
- Have both builders write requests independently for a random subset of about 15 sampled functions.
- Report how often the two requests get the same classification.
- Add builder as a covariate in a secondary analysis.

### 16. Minor. The equivalence margin is large compared with the historical rate.

**Raised by:** R3 (W8).

**Problem.**
- I checked the arithmetic. Under the simulated rates, the weighted historical D is about 0.032 to 0.074.
- So an agent rate 1.7 to 2.6 times higher still falls inside the ±0.05 margin.

**Required change.** Either set the margin after development, relative to the measured historical D rate, or drop equivalence claims from paper 1.

### 17. Minor. The "better security" reading rule has no test.

**Raised by:** R3 (Question 1).

**Problem.** In the simulation, agents produce working outputs in 72% of attempts (0.9 × 0.8) and historical code in 100%. Under those rates, the rule in Section 6.2 may never be met.

**Required change.** State the test for "the rate of working outputs with no confirmed flaw does not fall": its margin, its level and its family. Show by simulation whether it can be met under the planning rates.

### 18. Minor. Several factual questions have short answers that belong in the text.

**Raised by:** R1 (Questions 1, 3, 4, 6, 7), R3 (Questions 2, 4, 5, 6).

**Required change.** Answer each of these in the proposal:
- how many of the 43 findings with public history have a fix confined to one function body (R1 asked this in iteration 1 too);
- whether both arms of pilot contrast (a) had a full terminal;
- the planning subtotal, written as 756 to 1,443;
- where paper 2's 160 validated vulnerable functions come from;
- whether the 1,800-hour ceiling assumes no coursework or teaching;
- whether the month-two simulation draws protocols from a finite frame with the measured sampling fraction;
- how many seed patterns there will be, and at most how many pairs per pattern, given the pilot's intraclass correlation of 0.69;
- whether month two chooses the number of attempts from precision per measured cost.

### 19. Minor (raised by the AC). The cited simulation code changed after submission.

**Problem.**
- The RQ1 data generator (`tools/power_sim_v8.py`) is dated 23:47 on 21 October 2026. The proposal file is dated 23:37. The cited result files are dated 21:27 to 21:56.
- The change adds a parameter `p_nov` and a call to `rng.random(P)` that runs on every simulated study, even when `p_nov` is zero.
- From reading the code, I expect this extra draw to shift every random number that follows. If so, the saved results in `tools/power_results_v10_a.txt` and `tools/power_results_v11*.txt` can no longer be reproduced exactly from the current script.
- I did not run it [uncertain]. R3's exact reproduction was probably done before the change [uncertain].
- The new comment in the script points to a later version that this proposal does not cite. I did not use that version.
- Git status lists `proposal_workspace/` as untracked, so the earlier script cannot be recovered from history.

**Required change.** Keep each cited script under a fixed name or a commit hash. Regenerate, or cite again, every result file whose generator has changed.

## Disagreements among reviewers

1. **Is paper 2's contrast now sound?**
   - R2 marks its iteration-1 W4 "resolved at proposal level". R1, R3, R4 and R5 say θ does not separate a security-specific effect from ordinary obedience to tests.
   - *Resolution:* I follow the majority. R3's argument is logical, not empirical. Under a pure obedience agent, θ > 0 by construction. See item 4.

2. **Which outcome should be primary for θ?**
   - R1 and R3 want the primary outcome to be whether the endorsed behavior is kept. R4 keeps vulnerability retention as the endpoint and adds the endorsed-behavior outcome as a diagnostic.
   - *Resolution:* Make the endorsed-behavior outcome primary for θ (R1, R3). Under an ordinary assertion, vulnerability retention is near zero by construction, so it cannot serve as the comparison. Keep vulnerability retention as the security endpoint within the security arms (R4). Item 4 says this.

3. **Does paper 2 matter for acceptance?**
   - R4 says paper 2 "can remain deferred without weakening that route to acceptance." R3 counts θ among its three score-raising changes. R1 cites it under C1.
   - *Resolution:* While RQ2 stays among the proposal's stated contributions, its main contrast must be sound. If the authors instead turn paper 2 into a named extension with no claimed contribution, item 4 can wait. In that case, the C1 and C4 concerns tied to θ fall away.

4. **Should the design comparison be tested or estimated?**
   - R1 and R5 ask for a co-primary or primary endpoint. R2 asks for a principal analysis with a multiplicity rule. R4 asks for an allocation chosen to reach a target precision.
   - R3 points out that when detection is good, the sign is predictable, so a test against zero says little.
   - *Resolution:* Treat it as a principal estimand judged by precision against a stated smallest useful difference (R1, R4), not as a test against zero. Add R3's reading rule (item 14). Item 1 combines these.

5. **How much feasibility evidence does the proposal need now?**
   - R2, R4 and R5 want the timed development cases completed. R1 wants a month-by-month table. R3 accepts the plan "as a plan" but still rates C7 a concern.
   - *Resolution:* Both are needed (items 2 and 5). Iteration 1 already made measured development cases a Blocking requirement, and they are still not done.

6. **More precision or less work?**
   - Item 1 pushes the design toward more V functions or more protocols. Items 2 and 5 show the budget is already tight at pessimistic rates.
   - *Resolution:* Look for cheaper precision first. R3 (Question 5) shows that two attempts instead of three remove 300 of 1,050 campaigns at 15 protocols, while the raw D half-width only grows from 0.0505 to 0.0564. The freed effort could buy more V functions. If no measured allocation meets the target, take the fallback in item 1. Do not stretch the budget.

7. **What should detection validation measure?**
   - R2 and R5 ask for an auditor sampling plan. R3 asks for flaws that an earlier audit missed.
   - *Resolution:* These do not conflict. R3 notes that at the planning rates the auditors would meet very few historical N flaws. So only R3's set can inform sensitivity on historical N code. The auditor plan covers disagreement between campaign and auditors by author. Do both (items 7 and 8).

8. **Is the equal search for flaws resolved?**
   - R1 and R3 say yes for the primary label. R2 says partly, because natural-flaw validation is thin. R5 finds the gap in confirmation.
   - *Resolution:* Labeling each implementation by its own blind campaign settles the design of the primary label. Confirmation (item 3) and validation (items 7 and 8) are still open.

9. **Ratings.** There is no disagreement this time. All five give pass on C2, C3, C5 and C8, and concern on C1, C4, C6 and C7. In iteration 1, R3 rated C1 a pass and R4 rated C4 a pass. Both now rate them a concern.

## Status of iteration-1 required changes

| # | Iteration-1 item | Status now | Reviewers' view |
|---|---|---|---|
| 1 | Blocking: feasibility | **Still open** for measurement | The scope cut and costed plan are done: R1 (#4) says "mostly resolved", R3 (#13) "resolved as a plan". The timed development cases are not done: R2 (W5) says "partly resolved", R4 (W4) "not resolved empirically", R5 (W4). See item 2. |
| 2 | Blocking: equal search for flaws | **Partly resolved** | The primary label from each implementation's own blind campaign is resolved: R1 (#1), R3 (#1). Measuring detection is partly resolved: R2 (W1), R3 (#2). There is a new gap in confirmation (item 3). |
| 3 | Blocking: AI-assisted baseline | Resolved | R1 (#2), R3 (#3) |
| 4 | Current native agents as primary | Resolved | R1 (#6), R3 (#10) |
| 5 | D as primary endpoint | Resolved | R1 (#5), R3 (#4). The test for the reading rule is still open (item 17). |
| 6 | Power from measured rates | **Partly resolved** | R1 (#3) says partly. R3 (#5) says mostly. Development-based rates are not yet measured. The adverse bound is missing (item 9). |
| 7 | Test the design comparison on data | **Partly resolved** | It is now reported (R4 W1: "resolved as a design omission"). But it is secondary and imprecise: R1 (W1), R2 (W4), R4 (W1), R5 (W1). See item 1. |
| 8 | RQ2: security effect against ordinary obedience | **Still open** | R2 (W4) says resolved. R1 (W4), R3 (W2), R4 (W2: "partially resolved") and R5 (W5) say open. See item 4. |
| 9 | Prevalence of natural faulty tests | Resolved | R1 (#10) |
| 10 | Full pilot reporting | Resolved | R1 (#11), R3 (#9). One small clarification remains (item 18). |
| 11 | Shared severity rubric and blinded adjudicators | Resolved | R2 (W3), R3 (#12) |
| 12 | Request text in stratum V | Resolved as written | No reviewer disputes the preregistration and the split by request type (Section 5.4). R1 (W6) raises a new, related problem (item 15). |
| 13 | Value of an unresolved attempt | **Partly resolved** | R3 (#6) says "resolved as a rule", but the rule is missing from the power analysis (item 9). |
| 14 | RQ2 effects that vary by function | Resolved | R3 (#7) |
| 15 | RQ2 replication kept | Resolved | R3 (#8) |
| 16 | 63008 evidence package | **Still open** | R2 (W2) says unresolved. R4 (W3) and R5 (W4) also note it. See item 6. |
| 17 | Bugs spanning several functions | Resolved as a rule | R1 (#8). The count of affected findings is still missing (R1 Question 1). The simulation does not reflect the exclusion yet (item 13). |
| 18 | Tests that call the target | Resolved | R1 (#7) |
| 19 | Frame from contest listings | Resolved in the text | R3 (#11). The simulation still assumes V functions in every protocol (item 13). |
| 20 | Title and RQ1 wording | Resolved | No reviewer disputes it. |
| 21 | Missing related work | Resolved | R1 (#9) and R4. R1 (W4) questions whether the difference claimed against ImpossibleBench holds (item 4). |
| 22 | SolAgent baseline | Closed | R4 (W3) withdraws the requirement. SolAgent is an extension. |
| 23 | Two papers | Resolved | R1 (#12) |
| 24 | Estimand and decision rule | Resolved in the text | Section 6.3 states the finite frame and the Holm decision. R3 (Question 2) notes that the simulation does not yet draw from a finite frame (item 18). |

Iteration 1 already made measured development cases a Blocking requirement, and the authors have still not done them. Three reviewers now make them a condition for a higher score. A third version that again only schedules this work is unlikely to change the decision.
