# Meta-review, iteration 1

Proposal: "AI Coding Agents and Human Developers on Audited Solidity Contracts" (`proposal_workspace/iter_1/proposal.md`).
Reviews: R1 (SE PC member), R2 (security PC member), R3 (evaluation expert), R4 (novelty hunter), R5 (fresh general PC member), all in `proposal_workspace/iter_1/reviews/`.

## Actionability check

All five reviews scored 3 or lower, so all five were checked. Each one has at least one concrete required change that the authors can act on.

| Review | Score | Concrete required change (example) | Result |
|---|---|---|---|
| R1 | 2 | Run the automatic search, without the audit report, on every sampled human function in stratum V, and report the share of audit findings it finds again (Weakness 1). Every one of its 12 weaknesses ends in a required change. | Pass |
| R2 | 3 | Produce one complete evidence package for finding 63008 that asserts victim entitlement and validates a correction to the function body only (Weakness 2). Every one of its 5 weaknesses ends in a required change. | Pass |
| R3 | 2 | State the value an unresolved attempt takes in the primary test, and rerun the test with every unresolved attempt set to each bound (Weakness 6). Every one of its 13 weaknesses ends in a required change. | Pass |
| R4 | 3 | Report the estimate from functions linked to findings only next to the weighted estimate on the same data (Weakness 1). Every one of its 4 weaknesses ends in a required change. | Pass |
| R5 | 2 | Add a pre-registered screen for signs of AI tools at each function's introducing commit (Weakness 2). Every one of its 9 weaknesses ends in a required change. | Pass |

No review is sent back to its reviewer.

## R4 overlap check

R4 claims eight overlaps. I checked each against the literature files. The master index of searched papers (`lit/master_index.tsv`) has a *status* column. VERIFIED there means a search agent opened the page. For the two papers that are not in the literature review (`lit_review.md`), I opened the URL myself.

| Paper R4 names | Where checked | Result |
|---|---|---|
| SecureVibeBench (ACL 2026) | VERIFIED in the master index; also in the literature review | Confirmed |
| How Safe Are AI-Generated Patches? (Sajadi et al., arXiv 2507.02976) | VERIFIED in the master index; also in the literature review | Confirmed |
| EVMbench (ICML 2026) | VERIFIED in the master index; also in the literature review | Confirmed |
| ImpossibleBench (ICLR 2026) | VERIFIED in the master index; also in the literature review | Confirmed |
| On the Risks of using LLM-Generated Tests for Regression Testing (arXiv 2610.11835) | VERIFIED in the master index; also in the literature review | Confirmed |
| SolAgent (arXiv 2601.23009) | VERIFIED in the master index; also in the literature review | Confirmed |
| ExecCritic: Learn to Test, Test to Improve for Coding Agents (https://arxiv.org/html/2609.09133v1) | I opened the page. Title, authors (Tao, Peng, et al.) and date (8 September 2026) match. The abstract says that agent-written tests "can encode incomplete or incorrect behavioral targets". It describes a harness that "qualifies and freezes" independently written tests, which then guide a separate repair agent. This matches R4's description. The paper is not in the literature review. But it is VERIFIED in the master index (row `Tao2026-ExecCritic`, from the PoV-guided repair search, `lit/r1_L6_pov_guided_repair.md`). | Confirmed |
| Calibration, Not Compilation: Detecting and Repairing Misspecified Probabilistic Programs Written by Language Models (https://arxiv.org/abs/2606.31630) | I opened the page. Title, authors (Xu, Zeng, Paisley, Zhao) and date (30 June 2026) match. The abstract reports that "unit-test feedback ... is itself significantly worse than no feedback at all" in repair. This matches R4's description. The paper is not in any literature file. | Confirmed |

R4's answer to "same technique, same problem, same claim?" is **No**. I agree. None of the eight papers samples flagged and unflagged Solidity functions with known probabilities and compares agents with the historical author using executable evidence. None crosses fault-enforcing tests with permission to run them in a security setting. ExecCritic studies test-guided repair on SWE-bench. "Calibration, Not Compilation" studies statistical programs. Both narrow RQ2's novelty, but neither duplicates it.

## Decision

| Review | Score |
|---|---|
| R1 | 2 |
| R2 | 3 |
| R3 | 2 |
| R4 | 3 |
| R5 | 2 |

Mean: 12 / 5 = **2.4**.

Applying the rule:
1. Every score at least 4: **failed**. No score reaches 4.
2. Mean at least 4.0: **failed**. The mean is 2.4.
3. R4 reports no prior work with the same technique, the same problem and the same claim: **met**.
4. AC concurs: does not apply, because conditions 1 and 2 already fail.

**Result: NOT ACCEPT.** The proposal goes back to the authors for revision. The AC adds no Blocking reason of its own beyond the items below.

## Prioritized required changes

Labels: **Blocking** means the main claim cannot stand without the change. **Major** means acceptance needs it. **Minor** means it improves clarity or scope.

1. **Blocking. The plan does not fit one first-year student in 12 months.** Raised by all five: R1 (W4), R2 (W5), R3 (W13), R4 (W4), R5 (W3). R1, R3 and R5 rate feasibility as a fail. The proposal admits that the pilot has not measured the labour cost. R3 estimates from pilot rates that 780 to 1,440 RQ1 implementations would each need a confirming PoV and a person's decision.
   *Required change:* Build at least three development cases to the full standard of Sections 4 and 5, with a person doing every human-review step. Include at least one probability-selected set of stratum N functions. Time every step. From these hours and the pilot confirmation rates, write a costed plan. It must give the smallest RQ1 the student can build in months 2 to 5 (protocols, configurations, attempts) and the precision that size gives. Everything beyond that core becomes a named extension.

2. **Blocking. Human code and agent code do not face the same search for flaws.** Raised by R1 (W1), R2 (W1), R3 (W1, W2) and R5 (W1). The audit found the human flaws in stratum V. Agent flaws are found only by fuzzing, two LLM reviewers and replay. The LLM reviewers come from the same model families as the agents. Their recall in the pilot ranged from 2 of 7 to 7 of 7. RQ4 has about a dozen implementations per cell, which is too few to measure a difference in recall between authors. The abstract's claim that "Discovery budgets are matched" does not show equal detection.
   *Required change:* Run the common discovery procedure, without the audit report or the audit's known findings, on every sampled human function in stratum V. Report the share of audit findings it finds again. Record which campaign first found each confirmed flaw. Size RQ4 from a target interval width for the difference in recall between human and agent code. If natural positives are too rare, seed the same known flaw patterns into matched human and agent code. Before collection, state the missed-flaw rates that would reverse the sign of the primary result (R2).

3. **Blocking. The "human" baseline may itself be AI-assisted.** Raised by R1 (W2), R3 (W3) and R5 (W2). The note on the 63008 control group (`pilot/tasks/63008/control_group.md`, Section 7) found a `CLAUDE.md` in the Angstrom repository three days before the commit that introduced the bug. It also found agent files in other pilot repositories. The proposal prefers recent findings, and recent code is the most likely to be AI-assisted. Section 6.8 does not mention this threat.
   *Required change:* For every sampled function, record signs of AI help at the commit that introduced it: agent instruction files, AI co-author trailers and pull-request text. Add this threat to Section 6.8. Pre-register how flagged functions are treated (see disagreement 3). Where AI help cannot be ruled out, call the baseline "the historical developer implementation".

4. **Major. The primary agents are dated or run through a translation layer.** Raised by R1 (W6), R3 (W10) and R5 (W5). The six primary configurations use GPT-5.4-mini and Claude Sonnet 4.5. Two of them reach their model through a translation proxy. The current vendor-supported agents run only on a subset.
   *Required change:* Make the vendor-supported current agents (for example Claude Code and Codex CLI with current models, versions pinned at month two) the primary Holm family on the full RQ1 sample. Move translated and mini-model configurations to an exploratory family. RQ2 may keep a harness the authors control, because the native agents' tools cannot be restricted (R5, Question 7).

5. **Major. The primary endpoint counts broken code, and failures look like security.** Raised by R1 (W5), R3 (W4) and R5 (W6). K (compiled and confirmed vulnerable) counts outputs that fail the project's own tests. The pilot's only added flaws are of this kind. K also falls whenever an agent fails to compile or writes code that does little, so a negative difference can reflect weak capability rather than better security.
   *Required change:* Make D (compiled, passing the legitimate-behaviour suite, and confirmed vulnerable) co-primary with K, and simulate its power before the month-two freeze. Pre-register R3's reading rule. A negative difference in K is reported as better agent security only if the rate of working outputs with no confirmed flaw does not fall.

6. **Major. The power analysis rests on guessed rates and leaves out effects that matter.** Raised by R1 (W3), R3 (W5) and R5 (W6). The human rate in stratum N is fixed at 0.02, and the agent rates are 5.5 to 7.5 times higher, with no data behind either. Power at a difference of about +0.04 is 0.12 to 0.47. R3 reran the authors' code with a protocol effect that differs between agents and humans. The lowest configuration power then fell from 0.72 and 0.55 to as low as 0.40 and 0.35. The simulation also assumes perfect detection.
   *Required change:* In month one, run the full RQ1 pipeline on the stratum N functions of the ten development cases and set the power scenarios from the observed rates. Add a protocol-by-author random effect, a range of human stratum N rates and a detection step to the simulation. State the minimum detectable difference under the worst scenario kept. Declare a smallest difference of interest and pre-register an equivalence test (two one-sided tests) against it.

7. **Major. The main methodological contribution is not tested on data.** Raised by R4 (W1) and R5 (W9). R1 and R2 also rate novelty as a concern. The idea that designs built from human mistakes differ from unconditional designs is already stated in prior work. The proposal does not show that weighting in unflagged functions changes any conclusion.
   *Required change:* Pre-register a comparison on the same collected data. Report the estimate and the agent ranking that a design using only stratum V would give (the SecureVibeBench or Foresight-SWE design) next to the weighted estimate, with intervals for the difference.

8. **Major. RQ2 does not separate a security effect from ordinary obedience to wrong tests.** Raised by R2 (W4), R4 (W2) and R5 (W7). R1 (W9) adds that the technique delta against ImpossibleBench is not stated. ImpossibleBench, ExecCritic and "Calibration, Not Compilation" already show that wrong tests can make feedback harmful.
   *Required change:* Add a matched control in which the injected assertion is wrong about non-security behaviour, within the same tasks where possible (R4). State in advance which result would show that faulty tests specifically preserve the exploitable behaviour (R2, Question 3).

9. **Major. RQ2's practical weight is unknown.** Raised by R1 (W10) and R5 (W7). The confirmatory RQ2 test uses injected tests, and no one knows how often audited DeFi repositories contain natural fault-enforcing tests. Of the eight pilot tasks, only 63008 had one.
   *Required change:* Report how common natural fault-enforcing tests are among stratum V functions, with a confidence interval, as a descriptive RQ2 result (see disagreement 6 on how to count).

10. **Major. The pilot result that motivates RQ2 is reported without the results that point the other way.** Raised by R1 (W11), R3 (W9) and R5 (W7). Section 3 cites "10 of 12 runs without execution and 2 of 12 runs with a terminal". It omits three facts from the repair study report (`docs/pilot/repair_input_study_results.md`). Both pre-registered contrasts were null. OpenHands succeeded in 9 of 12 runs with the shown-test tool. Codex scored 6 of 12 both with that tool and with a full terminal.
    *Required change:* In Section 3, add the two pre-registered contrasts, the 9 of 12 result and the Codex 6 of 12 against 6 of 12 result. Say that the 10 against 2 contrast was exploratory and used a full terminal. Say that no person has reviewed the repairs yet, and that the RQ2 hypothesis was formed after the pilot.

11. **Major. Severity and attribution are judged by people who know which code is the human's.** Raised by R2 (W3) and R3 (W12). Severity follows each audit platform's own criteria, with no shared rule for newly found agent flaws. The construction team makes these calls unblinded.
    *Required change:* Freeze one severity rubric across platforms before evaluation, with thresholds for financial harm and for loss of availability. Have two adjudicators from outside the construction team apply it, blinded to author and arm as far as the code allows. Report how often they agree.

12. **Major. The request text can decide the outcome in stratum V.** Raised by R5 (W4). In the pilot, 13 of 13 runs reproduced the bug when the request described the vulnerable design, against 3 of 15 when it stated the fixed rule. In 63008, a source comment calls the start tick "exclusive", and an agent quoted it.
    *Required change:* Before any run, pre-register whether a stratum V task whose sources describe the vulnerable behaviour is kept and scored or marked unresolved. Report stratum V results separately for requests that favour the vulnerable behaviour, neutral requests and requests that favour the corrected behaviour.

13. **Major. The primary test does not say what value an unresolved attempt takes.** Raised by R3 (W6). Section 6.2 gives unresolved attempts "bounds", but the test statistic needs a number. The simulation generates no unresolved outcomes.
    *Required change:* State the value an unresolved attempt takes in the primary statistic. Require that the primary claim keeps its sign when every unresolved attempt is set to each bound.

14. **Major. The RQ2 model assumes the same treatment effect for every function.** Raised by R3 (W7). With varying effects, R3 measured a false-rejection rate of up to 0.073 at a nominal 0.05. At pilot-like cell rates, power fell from 0.90 to 0.78.
    *Required change:* Add function-level random slopes for test content, execution and their interaction, or use a function-level difference-in-differences with inference clustered by protocol. Redo the RQ2 calibration with effects that vary by function and with pilot-like cell rates.

15. **Major. RQ2's confirmatory result may rest on one agent.** Raised by R3 (W8). Reduction 4 removes the replication configuration. In the pilot, the same input gave 3 of 12 to 11 of 12 successes depending on the agent.
    *Required change:* Take the RQ2 replication off the reduction list. Claim the RQ2 effect beyond one configuration only if both configurations show the same sign.

16. **Major. The flagship example does not yet meet the proposal's own standard.** Raised by R2 (W2). The 63008 PoV asserts only attacker profit. The loss estimate replaces the whole `TickIterator.sol` file, not only the function body. The attack also depends on finding H-02 and on ordering assumptions that are not recorded.
    *Required change:* Produce one complete evidence package for 63008. It must assert victim entitlement and backing, validate a correction to the function body only, and record the capital, ordering and other-finding assumptions. Say whether the attack still works once H-02 is fixed.

17. **Major. Bugs that span several functions may drop out of the population.** Raised by R1 (W8). A flaw counts only if correcting the target function alone removes it. The 63185 and 63008 fixes already touch more than one function.
    *Required change:* In the month-one frame refresh, count the High and Medium findings whose fix changes more than one function. Before sampling, state one rule: sample the changed functions as one unit, or exclude them and report their weighted share as a limit on the population.

18. **Minor. Tests written against the human function may steer the agent.** Raised by R1 (W7).
    *Required change:* When each task is built, record whether the workspace has tests that call the target function directly. Pre-register RQ1 estimates split by this property as a secondary analysis.

19. **Minor. The protocol pool contains only protocols where a human already failed.** Raised by R3 (W11).
    *Required change:* Build the protocol frame from audit contest listings. If that cannot be done, name the RQ1 population "protocols with at least one qualifying finding".

20. **Minor. The title and abstract claim more than the design measures.** Raised by R5 (W8); R1 (W2) asks for the same renaming.
    *Required change:* Retitle the paper and restate RQ1 as a comparison of function-body replacements in audited snapshots.

21. **Minor. Related work leaves out close papers.** Raised by R1 (W9) and R4 (W2).
    *Required change:* Add SolEval, Cotroneo et al. (ISSRE 2025), ExecCritic and "Calibration, Not Compilation" to Section 7 and its table. Write one sentence on the technique delta of RQ1 against SolEval, and one for RQ2 against ImpossibleBench.

22. **Minor. The closest Solidity-specific generator is not a baseline.** Raised by R4 (W3).
    *Required change:* If the costed plan in item 1 allows it, replace one lower-priority integration with a documented SolAgent adaptation on the common RQ1 subset.

23. **Minor. Four research questions will not fit one ICSE paper.** Raised by R1 (W12) and R5 (W3).
    *Required change:* Plan two papers: RQ1 with RQ4 for ICSE, and RQ2 for a venue such as FSE or ISSTA. Give each its own month-two freeze and submission date.

24. **Minor. The estimand and the decision rule are unclear.** Raised by R3 (Questions 1 and 2). The jackknife has no finite-population correction. At 25 protocols, a Holm test and the interval can disagree on whether a difference is real.
    *Required change:* State whether the RQ1 estimand is the finite set of eligible functions or a superpopulation. State whether the Holm test or the interval decides the reported claim.

## Points of disagreement among reviewers

1. **Which way the detection gap biases the result.** R1 and R5 argue that the audit gives human code an extra search, so agents look safer than they are. R3 argues the reverse. Common replay gives a flaw shared by many agent attempts many chances to be found. Human code in stratum N has also already survived an audit, so its remaining flaws are harder to find. Both effects push agents toward looking worse. R2 does not take a side.
   *How to resolve:* Both effects can be present at once, so the authors should not argue for a net direction. They should measure it. Item 2 measures recall by author and stratum. The authors should also report three estimates side by side: the primary one, R3's version that counts only flaws found by the implementation's own campaign or the audit PoV, and the version that counts only flaws found by the common procedure.

2. **Which endpoint is primary.** R5 wants the primary endpoint to count only flaws the common procedure finds. R1 wants that count as co-primary, and D co-primary as well. R3 wants that count as a sensitivity analysis, and a reading rule on K rather than a new endpoint.
   *How to resolve:* Too many co-primary endpoints will cut power further (item 6). Choose one primary endpoint and justify it with the new power simulation. The AC suggests counting only flaws the common procedure finds, because it is the only version in which both authors face the same search. Make D co-primary only if the simulation shows useful power for it. Otherwise keep it as the main secondary endpoint, together with R3's reading rule.

3. **What to do with human functions that show signs of AI help.** R5 wants them out of the primary estimate, with their inclusion as a sensitivity analysis. R1 and R3 want them kept, with a sensitivity analysis on the functions with no such signs.
   *How to resolve:* Count the flagged share during the month-one frame refresh, before sampling and before any outcome is seen. Pre-register a threshold. If the flagged share is below it, exclude flagged functions from the primary estimate (R5). If it is above, keep them, use the name "historical developer implementation", and report the unflagged subset as a pre-registered sensitivity analysis (R1, R3).

4. **Shrink the study or add to it.** R5 asks for a core of about 10 to 12 protocols and two configurations. R1 warns that fewer than 25 protocols makes power worse. Several reviewers also ask for more work: keep the RQ2 replication (R3), add a non-security control (R4), add SolAgent (R4), and run current agents on the full sample (R1, R3, R5).
   *How to resolve:* The costed plan in item 1 decides. Each addition enters the core only if its measured cost fits. Otherwise it is listed as an extension. A smaller core must report its expected precision openly. The equivalence test in item 6 keeps a null result informative at that size.

5. **How to show that RQ2 is about security.** R4 asks for a matched control with wrong assertions about non-security behaviour. R2 asks for an analysis of agent trajectories that shows the exploitable behaviour is kept despite contrary PoV evidence.
   *How to resolve:* R4's control directly tests the alternative explanation that R2 raises in Question 3. Use it as the confirmatory contrast if item 1 finds room for it. Run R2's trajectory analysis as a secondary analysis on runs already collected.

6. **How to count natural fault-enforcing tests.** R1 asks for a weighted share from the RQ1 sample of stratum V. R5 asks for a full count over all stratum V functions in the refreshed frame in month one.
   *How to resolve:* R5's count comes earlier and can show whether RQ2 is worth its cost. Do it in month one if the screening is cheap. If not, report R1's weighted estimate.

7. **Novelty and soundness ratings.** R3 rates novelty (C1) a pass, while R1, R2, R4 and R5 rate it a concern. R4 rates soundness (C4) a pass, while R1, R2, R3 and R5 rate it a concern.
   *How to resolve:* Follow the majority. Item 7 and item 21 address novelty. Items 1 to 3 address soundness.
