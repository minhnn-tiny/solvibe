# Repair input study, first experiment: results (finding 63008)

Date: 2026-10-20. Scope: one finding (63008, Sorella L2 Angstrom, `reset(TickIteratorDown)`), one model (GPT-5.4-mini) under three agents, 12 arms, 12 runs per arm, 144 runs, plus 4 calibration runs. The design is in `IDEA.md`, section "Extension: how the input given to a repair agent changes the repair". How it was run is in `IDEA.md`, Method, Step 11, and in the process log (`docs/pilot/process_log.md`, Steps 25 to 29). The task files and the checks made before any data are described in the README of the study's task folder (`pilot/tasks/63008/extension/README.md`).

The numbers below come from the analysis script (`pilot/analysis/stats_study.py`). It writes:
- `pilot/results/repair_input_study/summary.json`;
- one row per run (`runs.csv`), one row per arm (`arms.csv`) and one row per contrast (`contrasts.csv`);
- the charts (`figures/`).

Every run is in `pilot/runs/repair_input_study/<setup>/<arm>/rep<NN>/`.

**Follow-up on 26 October.** 36 more runs filled in the information arms at E0 for OpenHands: L-E0, R-E0 and RP-E0. Section 12 reports them. Sections 1 to 11 describe the first experiment and keep its numbers. The analysis files now hold all 180 runs.

## 1. Summary

1. **Neither primary contrast shows a difference.** Both are on OpenHands + GPT-5.4-mini.
   - (a) Adding the shown PoV to a full terminal (L-E2 against P-E2): 0 of 12 against 2 of 12 succeed. The difference is +16.7 points, with a 95% interval of −10.4 to +44.8 and a Holm-adjusted p of 0.96.
   - (b) Letting the agent rerun the shown PoV (P-E0 against P-E1): 10 of 12 against 9 of 12. The difference is −8.3 points, with an interval of −39.0 to +24.1 and an adjusted p of 1.0.
   - With 12 runs per arm, these results do not show that the inputs make no difference. The intervals are wide.
2. **The largest effect is the full terminal. It is exploratory, because it was not a primary contrast.** OpenHands with the shown PoV succeeded in:
   - 10 of 12 runs when it could run nothing (P-E0);
   - 9 of 12 when it could rerun only the shown test (P-E1);
   - 2 of 12 when it had a full terminal (P-E2).

   From P-E0 to P-E2 the drop is 66.7 points, with an interval of −83.6 to −26.9 and a Fisher p of 0.003, unadjusted. Codex shows the same direction, but smaller and not clearly (11 of 12 at E0, 6 of 12 at E2).
3. **With a terminal, the agents kept the repository's own tests passing, and those tests expect the bug.** The audited test file has four downward tests that assert the start tick is skipped. Both the human fix and the reference repair fail them.
   - In P-E2 and RP-E2, 7 of 12 OpenHands repairs each still pass all four. In P-E0 none does, and in P-E1 one does.
   - Almost every OpenHands run opened or ran that test file, at every level: 11 of 12 at E0, 11 of 12 at E1, and 12 of 12 at P-E2. Agents at E0 and E1 read the tests but could not run them, and they mostly succeeded. So reading the tests did not mislead the agent; running them did.
   - The final summaries say so. For example: "Still preserves the existing exclusive-boundary behavior for the normal cases covered by the iterator tests" (P-E2 rep02).
4. **With a terminal, the agents fitted the shown test.** In P-E2 and RP-E2, 6 and 7 of 12 OpenHands repairs block the shown P2 while another attack still works. Their conditions include the start tick only in the case P2 happens to meet: the start tick aligned and the end tick not, a different bitmap word, or the start equal to the pool's tick. At E0 and E1 this happened in 1 of 24 OpenHands runs.
5. **Location alone was not enough, and the written report helped OpenHands. Both are exploratory.**
   - With only the function named (L-E2), every OpenHands repair left P2 working (12 of 12). Codex succeeded in 3 of 12.
   - With the report (R-E2), OpenHands succeeded in 5 of 12, against 0 of 12 in L-E2. That is +41.7 points, interval +8.7 to +68.0, unadjusted p 0.037.
   - Adding the report to the PoV (RP-E2) did not help: 2 of 12, the same as P-E2.
6. **The agent mattered.**
   - Codex + GPT-5.4-mini did best: 11 of 12 at P-E0.
   - Aider + GPT-5.4-mini did worst: 3 of 12 at P-E0 and 0 of 12 at P-E1. In 11 of its 24 runs the bug stayed, and Aider never runs anything at E0.
7. **The frozen checks were not enough.** 64 repairs compiled, passed all 61 functional tests and blocked every held-out attack. The LLM judge reviewed them. Seven of those 64 still have a flaw that a reviewer reported and a test confirmed:
   - one keeps the known bug, at bit 255 of a bitmap word (Aider);
   - five scan the bitmap with no end, so a swap with no initialized tick below the price runs out of gas (Codex 3, Aider 1, OpenHands 1);
   - one never sets the current tick on an empty range, so a swap that keeps the pool at a negative tick reverts (Codex).

   Claude Opus 5.5 reported all seven. GPT-6.1 Sol reported two of them. Two reports were rejected because their own scenarios did not reproduce as tests.
8. **No run failed for operational reasons.** There were no timeouts, no API errors, no runs without an edit, and no repeated runs. The agents cost $24.45 in all and used 143 million tokens. Aider's 0.55 million tokens are not priced. The calibration (OpenHands P-E2, 4 runs) gave 0 of 4, which warned that this setup is near the floor. The full design ran anyway, as the user decided.
9. **A blind code review of all 144 repairs agrees with the checks on 143.** Claude subagents did it without knowing the arm (section 7).
   - It classed 17 of the 24 OpenHands repairs in P-E2 and RP-E2 as narrow conditions, against 3 of 24 in P-E0 and P-E1.
   - The one disagreement is a success that returns an uninitialized tick. That breaks requirement 4, but no security effect was shown, so the outcome stands.
   - A person has not yet reviewed the repairs.
10. **The follow-up on 26 October supports the effect of the terminal (section 12).**
    - Without a terminal, OpenHands succeeded in 6 of 12 runs with only the function named, 10 of 12 with the report, 10 of 12 with the PoV, and 11 of 12 with both.
    - With a terminal, each of these four inputs did worse, by 42 to 75 points.
    - The contrast fixed for the follow-up is adding the PoV when the agent can run nothing (L-E0 against P-E0). It is +33.3 points, with an interval of −4.1 to +60.7 and a p of 0.19. So it does not show a difference.

## 2. What was run

| Agent + GPT-5.4-mini | Arms (12 runs each) | Runs |
|---|---|---|
| OpenHands SDK 1.53.0 | L-E2, R-E2, P-E2, RP-E2, P-E0, P-E1 | 72 |
| Codex CLI 0.160.1 | L-E2, P-E2, P-E0, P-E1 | 48 |
| Aider 0.86.2 | P-E0, P-E1 | 24 |

- An arm joins what the agent was told and what it could run:
  - **what it was told:** L, the function named; R, plus the written report; P, plus the shown PoV as a failing test with its output; RP, both;
  - **what it could run:** E0, nothing; E1, only the shown test, through the shared test script; E2, a full terminal.
- Every agent started from the human's vulnerable code at the audited commit, with the git history hidden.
- The prompts are in the study prompt file (`pilot/prompts/repair_input_study.md`).
- The runs went in a random order (seed 20261020), 6 and then 8 at a time.
- **A repair is a success** when all of these hold:
  - it compiles;
  - all five frozen attacks are blocked: P1, P2 (the evaluation version), P3, and the new held-out attacks P4 and P5;
  - all 61 functional tests pass;
  - no High or Medium flaw that a reviewer reported has been confirmed by a test.
- **An attack counts as blocked** only when its test fails at the place recorded on the human fix.

## 3. Success per arm

| Agent | Arm | Success | 95% interval (Wilson) | Compile, attacks and tests pass | Flaw confirmed by the judge | Repairs that still pass all 4 bug-expecting tests |
|---|---|---|---|---|---|---|
| OpenHands | L-E2 | 0/12 | 0 to 24% | 0 | 0 | 12 |
| OpenHands | R-E2 | 5/12 | 19 to 68% | 5 | 0 | 3 |
| OpenHands | P-E2 | 2/12 | 5 to 45% | 2 | 0 | 7 |
| OpenHands | RP-E2 | 2/12 | 5 to 45% | 3 | 1 | 7 |
| OpenHands | P-E0 | 10/12 | 55 to 95% | 10 | 0 | 0 |
| OpenHands | P-E1 | 9/12 | 47 to 91% | 9 | 0 | 1 |
| Codex | L-E2 | 3/12 | 9 to 53% | 3 | 0 | 8 |
| Codex | P-E2 | 6/12 | 25 to 75% | 7 | 1 | 4 |
| Codex | P-E0 | 11/12 | 65 to 99% | 11 | 0 | 0 |
| Codex | P-E1 | 6/12 | 25 to 75% | 9 | 3 | 0 |
| Aider | P-E0 | 3/12 | 9 to 53% | 3 | 0 | 6 |
| Aider | P-E1 | 0/12 | 0 to 24% | 2 | 2 | 5 |

The chart of success per arm is `figures/success_by_arm.png`. The outcome of every run is in `figures/outcomes_by_arm.png`.

**Success on the held-out attacks** counts only P1, P3, P4 and P5, which no arm shows. It equals the success count in every arm, because no repair blocked those four without also blocking P2.

## 4. Contrasts

Each difference is the second arm's success rate minus the first's. The interval is Newcombe's hybrid score interval at 95%, not adjusted. The p-value is the two-sided Fisher's exact test.

| Kind | Agent | First → second | Rates | Difference | 95% interval | p | Holm p |
|---|---|---|---|---|---|---|---|
| primary (a), adding the PoV | OpenHands | L-E2 → P-E2 | 0/12 → 2/12 | +16.7 | −10.4 to +44.8 | 0.48 | 0.96 |
| primary (b), rerunning the shown PoV | OpenHands | P-E0 → P-E1 | 10/12 → 9/12 | −8.3 | −39.0 to +24.1 | 1.00 | 1.00 |
| adding the report | OpenHands | L-E2 → R-E2 | 0/12 → 5/12 | +41.7 | +8.7 to +68.0 | 0.037 | |
| adding the report to the PoV | OpenHands | P-E2 → RP-E2 | 2/12 → 2/12 | 0.0 | −30.6 to +30.6 | 1.00 | |
| the PoV instead of the report | OpenHands | R-E2 → P-E2 | 5/12 → 2/12 | −25.0 | −54.0 to +10.9 | 0.37 | |
| a terminal instead of the test tool | OpenHands | P-E1 → P-E2 | 9/12 → 2/12 | −58.3 | −78.4 to −18.5 | 0.012 | |
| a terminal instead of nothing | OpenHands | P-E0 → P-E2 | 10/12 → 2/12 | −66.7 | −83.6 to −26.9 | 0.003 | |
| (a), repeated | Codex | L-E2 → P-E2 | 3/12 → 6/12 | +25.0 | −12.5 to +54.4 | 0.40 | |
| (b), repeated | Codex | P-E0 → P-E1 | 11/12 → 6/12 | −41.7 | −67.2 to −5.1 | 0.069 | |
| a terminal instead of the test tool | Codex | P-E1 → P-E2 | 6/12 → 6/12 | 0.0 | −34.8 to +34.8 | 1.00 | |
| (b), repeated | Aider | P-E0 → P-E1 | 3/12 → 0/12 | −25.0 | −53.2 to +4.1 | 0.22 | |

Only the first two rows were fixed before the runs. All the others are exploratory, and their p-values are not corrected for the number of contrasts.

The Codex fall from P-E0 to P-E1 comes mostly from flaws the judge found: 3 of the 6 failures in P-E1 are the unbounded bitmap scan. Codex at E1 often rewrote the search loop. At E0 it did not. With 12 runs per arm, this may be chance.

## 5. How the repairs failed

| Outcome | What it means | OpenHands (72) | Codex (48) | Aider (24) |
|---|---|---|---|---|
| success | every check passes | 28 | 26 | 3 |
| P2 still works | the report's own attack still succeeds | 13 | 8 | 11 |
| P2 blocked, another attack works | incomplete repair | 16 | 4 | 0 |
| attacks blocked, function broken | the functional suite fails | 14 | 6 | 7 |
| flaw confirmed by the judge | passes every frozen check, but a reported flaw is confirmed | 1 | 4 | 2 |
| does not compile | | 0 | 0 | 1 |

- **Narrow conditions.** Most failed repairs add a condition, so the start tick is included only in some cases. The calibration runs showed the same pattern (process log, Step 26). P5, which starts at a bitmap word boundary, caught more incomplete repairs than any other attack: it still works on 7 of the 12 RP-E2 repairs.
- **Broken functions.** The functional suite caught 27 repairs that block every attack but break the walk. For example, one returns the start tick itself when its bitmap bit is set, even when the start tick is not a multiple of the tick spacing.
- **The shown test.** Every repair in a P or RP arm that compiles makes the shown test pass, except the ones where P2 still works. So passing the shown test said little about the repair.

## 6. The LLM judge and the checks written after the runs started

- **What was reviewed.** Claude Opus 5.5 and GPT-6.1 Sol reviewed 64 repairs with prompt 4: every repair that compiles, passes the functional suite and blocks every held-out attack. They also reviewed two controls:
  - on the audited code, both report finding 63008 as High;
  - on the reference repair, both report nothing.
- **11 reports. Each was confirmed or rejected with a test** (`pilot/runs/repair_input_study/llm_judge/decisions.json`).

| Repair | Report | Check | Decision |
|---|---|---|---|
| Aider P-E1 rep03 | both: the known bug, at bit 255 | P6 | confirmed |
| Aider P-E1 rep01; Codex P-E1 rep02, rep10, rep11; OpenHands RP-E2 rep06 | Claude Opus 5.5: unbounded bitmap scan, out of gas | P7 | confirmed (5) |
| Codex P-E2 rep04 | both: empty range not handled | P8 | confirmed |
| Aider P-E0 rep07 | both: an uninitialized tick returned at bit 255 | their own scenarios | rejected (2) |

- **The three checks** are in `pilot/tasks/63008/extension/repair_checks/`. They were written after the runs started, so they are not part of the frozen set.
  - P6 is P2's attack starting at bit 255 of a bitmap word.
  - P7 is a taxed swap with no initialized tick below the price, which must fit in a 30-million-gas block. On the five flawed repairs it uses 147 to 153 million gas, against about 133,000 on the audited code.
  - P8 is a taxed swap that keeps the pool at a negative tick.
- **Each check passes on the flawed repair and fails on the audited code and on the reference repair.**
- **P6 to P8 were then run on all 64 reviewed repairs.** No repair failed them without a reviewer having reported it.
- **The two rejected reports.** Neither the revert nor the reward effect that the reviewers described appeared in a test. The repair does break requirement 4, because it returns a tick that is not initialized. But no security effect was shown.
- **Recall on these seven flaws:**
  - Claude Opus 5.5 reported all seven, and one of its eight reports was rejected.
  - GPT-6.1 Sol reported two, and one of its three reports was rejected.
- **The human fix and the empty range.** P8 also passes on the human fix's `TickIterator.sol` placed on the audited code, by a different path: the fix returns the tick above the start for an empty range, and the hook's arithmetic overflows. A taxed zero-for-one swap that keeps the pool at the same tick reverted there in both our tests, at tick 10 and at tick −10. We did not check the full fix commit, which changes other files. This is one more reason the study follows V1 requirement 6 and the reference repair, not the fix commit's own empty-range test.

## 7. Blind review

- **Who reviewed.** Four Claude subagents, Claude Opus 5.5, reviewed all 144 repairs: 36 each, on 20 October.
- **What they saw.** Each repair was in a folder with a random name (`pilot/scripts/study_blind_pack.py`). The folder held:
  - the repair's diff;
  - the compile result, the functional failures and each attack's state;
  - the full forge output of the attacks;
  - the LLM judges' reports, where there were any.
- **What they did not see.** The arm, the agent, the key and every run folder. They ran no code.
- **What they returned for each repair:**
  - how the change treats the start tick;
  - whether requirements 4 to 6 hold, with a counterexample if not;
  - any new High or Medium flaw;
  - their view of each judge report.

  Their files are in `pilot/runs/repair_input_study/blind_review_claude/`, and a summary per run is in `blind_review_summary.json`.

**Agreement with the checks.** The review counts a repair as correct when the requirement holds and it found no new flaw. On that reading it agrees with the check-based outcome on 143 of 144 repairs.
- **The one disagreement is Aider P-E0 rep07.** It passes every check, but returns an uninitialized tick when the start tick's compressed position is bit 255 of a word. The review marks this as breaking requirement 4, but finds no Medium or High security effect. That matches the two rejected judge reports in section 6. The outcome stays a success, because the design counts only confirmed security flaws.
- **The other three repairs it calls correct are not successes.** These are Codex P-E1 rep10, OpenHands RP-E2 rep06 and Aider P-E1 rep01. Their walk is right, but their search loop never stops (P7). The review reported that flaw itself, and agreed with Claude Opus 5.5.
- **No new flaw in any success.** The review found no new flaw in any repair that the checks count as a success.

**How the repairs treat the start tick:**

| Agent | Arm | General fix | Narrow condition | Wrong in another way | No effective change | Hides the symptom |
|---|---|---|---|---|---|---|
| OpenHands | L-E2 | 0 | 0 | 0 | 12 | 0 |
| OpenHands | R-E2 | 5 | 7 | 0 | 0 | 0 |
| OpenHands | P-E2 | 2 | 10 | 0 | 0 | 0 |
| OpenHands | RP-E2 | 3 | 7 | 2 | 0 | 0 |
| OpenHands | P-E0 | 10 | 2 | 0 | 0 | 0 |
| OpenHands | P-E1 | 9 | 1 | 1 | 0 | 1 |
| Codex | L-E2 | 3 | 0 | 1 | 8 | 0 |
| Codex | P-E2 | 6 | 4 | 2 | 0 | 0 |
| Codex | P-E0 | 11 | 0 | 1 | 0 | 0 |
| Codex | P-E1 | 7 | 1 | 4 | 0 | 0 |
| Aider | P-E0 | 2 | 0 | 5 | 5 | 0 |
| Aider | P-E1 | 1 | 1 | 8 | 2 | 0 |

- **A narrow condition** includes the start tick only under extra conditions. Examples are the tick's alignment, the bitmap word, the pool's current tick, or a non-zero net liquidity.
- **Wrong in another way** covers general changes that break something else. Examples are a wrong bitmap word at bit 0 or bit 255, ticks above the start, or an unbounded search.
- **A note on independence.** The pack the subagents saw by mistake included the forge output of the checks P6 to P8, where those had run. So on those three flaws the review was not independent of our checks. Its classification of the approaches, and its verdicts on the requirement, did not depend on them. The pack has since been rebuilt without them and without Claude's reviews, with the same random names, for a person to review.

## 8. What the agents did

| Arm | Runs that ran a test | Median test runs | Median tokens | Cost | Median agent minutes |
|---|---|---|---|---|---|
| OpenHands L-E2 | 12 | 1.5 | 1.15 M | $2.37 | 3.3 |
| OpenHands R-E2 | 11 | 2 | 1.30 M | $2.80 | 4.8 |
| OpenHands P-E2 | 12 | 3 | 2.23 M | $5.57 | 6.2 |
| OpenHands RP-E2 | 11 | 3 | 1.56 M | $3.06 | 5.2 |
| OpenHands P-E0 | 0 | 0 | 0.98 M | $2.10 | 2.2 |
| OpenHands P-E1 | 12 | 1 | 0.68 M | $1.87 | 2.3 |
| Codex L-E2 | 9 | 1 | 0.57 M | $2.03 | 3.1 |
| Codex P-E2 | 12 | 1 | 0.34 M | $2.27 | 1.6 |
| Codex P-E0 | 0 | 0 | 0.21 M | $1.10 | 1.4 |
| Codex P-E1 | 12 | 1 | 0.26 M | $1.29 | 1.8 |
| Aider P-E0 | 0 | 0 | 0.01 M | not priced | 0.3 |
| Aider P-E1 | 12 | 1 | 0.02 M | not priced | 0.8 |

- At E2, "ran a test" means a `forge test` command in the terminal, usually the repository's iterator tests or the whole suite. At E1, it means the shared test tool. At E0 nothing could run, and the level checks confirmed that no command ran.
- Every OpenHands run ended with the finish tool. Every Codex run ended its task normally.

## 9. Conclusions

These conclusions hold for finding 63008, GPT-5.4-mini, and these three agents. They rest on 12 runs per arm.

1. **For research question 2 ("Does a runnable exploit give a more trustworthy repair?").**
   - Being able to rerun the shown PoV did not change the success rate (primary contrast b).
   - Giving the agent a full terminal lowered it sharply, from 10 of 12 to 2 of 12 for OpenHands (exploratory). The follow-up found the same kind of drop for the other three inputs (section 12).
   - In the terminal arms, the agents ran the repository's iterator tests and kept them passing. Those tests encode the bug, so the agents shaped their fix around a wrong specification.
   - So whether an agent can execute code helps or hurts depending on what it executes. A runnable exploit on its own did not make the repair more trustworthy here.
2. **For research question 3 ("Does the kind of feedback affect AI repair agents?").** Yes. The feedback that mattered most was not the PoV but the repository's own tests.
   - With a terminal, the shown PoV mostly led to repairs that fit the shown test: P2 blocked, other attacks still working.
   - The written report helped OpenHands find the bug when no PoV was shown (0 to 5 of 12, exploratory).
3. **A passing PoV, or even the full frozen set, is not proof of a fix.**
   - 18 of 108 repairs in the P and RP arms made the shown test pass but failed a held-out attack.
   - 7 of 64 repairs that passed every frozen check still had a flaw, found by an LLM judge and confirmed by a test.
   - So a study like this needs held-out attacks, a functional suite, and a reviewer whose reports are checked by running them.
4. **The agent changes the answer.** The same input gave 3 of 12 to 11 of 12 successes depending on the agent (P-E0). Results from one agent should not be read as results about "AI repair" in general.

## 10. Limits

- **One finding.** The effect of the terminal depends on the repository having tests that encode the bug. That is true for 63008, and probably common, but it is not tested here.
- **One model, 12 runs per arm.** The intervals are wide. Every contrast other than the two primary ones is exploratory and uncorrected.
- **The calibration warned of a floor.** P-E2 gave 0 of 4 in calibration and 2 of 12 in the main runs.
- **The frozen checks have known gaps.** The adapted empty-range test uses positive ticks only, so a repair that never sets the current tick passes it. And none of P1 to P5 starts at bit 255. The checks written afterwards (P6 to P8) are reported on their own, and only a reported and confirmed flaw changes an outcome.
- **The judge was fixed during the runs, and every run was judged again at the end.** Results were the same on all 143 runs that had a result the first time.
- **No person has reviewed the repairs yet.** Claude subagents did the blind review that the design gives to a person. Their pack included, by mistake, the output of the checks written after the runs started.
- **The setups differ, so agents are compared only with themselves.** Codex uses its fallback prompt and tools with GPT-5.4-mini, and it has the study's file tools in every arm. OpenHands asks for high reasoning effort, and Codex for medium.

## 11. Next steps

1. Repeat on more findings, especially ones whose repository tests do not encode the bug. That separates the effect of the terminal from the effect of misleading tests.
2. Add the deferred arm that shows corrected repository tests, or hides the misleading ones, at E2.
3. Add a held-out attack at bit 255 of a bitmap word, and an empty-range test at a negative tick, to the frozen set for the next round.
4. A person should review the blinded pack (`pilot/runs/repair_input_study/blind_review/`) before the results are cited.
5. Run the next configurations named in the design: Sonnet 4.5, and Codex + Sonnet 4.5.

## 12. Follow-up: the information arms without a terminal (2026-10-26)

**Why.** The first experiment compared the information arms only at E2, and the execution levels only in arm P. At E2 the repository's iterator tests, which expect the bug, pulled every arm down. So primary contrast (a) compared two arms near zero, and it could not tell whether the PoV helps when the agent cannot run those tests. The plan, with its one fixed contrast, was written in `IDEA.md` (section "Follow-up: the information arms without a terminal") before these runs.

**What was run.**
- OpenHands + GPT-5.4-mini in L-E0, R-E0 and RP-E0, 12 runs each, 36 runs.
- The prompts, tools, model and judge were the same as in the first experiment.
- The runs went in a random order (seed 20261026, `pilot/runs/repair_input_study/run_order_e0.json`), 6 at a time.
- No run was repeated. There were no timeouts and no API errors, and every run made an edit.
- Every run was offered only the file editor, the task tracker, and the finish and think tools. No run ran a test.
- The agents cost $4.36 and used 21.0 million tokens.

**Success with and without a terminal.** OpenHands + GPT-5.4-mini. The E2 column and P-E0 come from the first experiment.

| What the agent was told | E0, can run nothing | E2, full terminal | E0 → E2 | 95% interval | p |
|---|---|---|---|---|---|
| L, the function named | 6/12 | 0/12 | −50.0 | −74.6 to −15.4 | 0.014 |
| R, plus the report | 10/12 | 5/12 | −41.7 | −67.0 to −3.1 | 0.089 |
| P, plus the shown PoV | 10/12 | 2/12 | −66.7 | −83.6 to −26.9 | 0.003 |
| RP, both | 11/12 | 2/12 | −75.0 | −88.8 to −36.0 | 0.0006 |

**Contrasts at E0.**

| Kind | First → second | Rates | Difference | 95% interval | p |
|---|---|---|---|---|---|
| fixed before the runs, (c) adding the PoV | L-E0 → P-E0 | 6/12 → 10/12 | +33.3 | −4.1 to +60.7 | 0.19 |
| adding the report | L-E0 → R-E0 | 6/12 → 10/12 | +33.3 | −4.1 to +60.7 | 0.19 |
| adding the PoV to the report | R-E0 → RP-E0 | 10/12 → 11/12 | +8.3 | −21.3 to +37.3 | 1.00 |
| adding the report to the PoV | P-E0 → RP-E0 | 10/12 → 11/12 | +8.3 | −21.3 to +37.3 | 1.00 |

The intervals and p-values are computed as in section 4. Only (c) was fixed before the runs. The E0 → E2 rows and the last three rows here are exploratory and not corrected.

**How the follow-up repairs failed.**
- **L-E0:** 4 left P2 working, 1 broke the function, and 1 has a flaw confirmed by the judge.
  - The four that left P2 working changed when the current bitmap word is loaded. They did not change which ticks the walk returns, so the start tick is still skipped and all five attacks still work. Their summaries describe other problems, for example "stale `currentWord` state when the downward walk is zero-length".
  - These four are the only follow-up repairs that still pass all four bug-expecting tests. They pass them because the walk did not change.
- **R-E0:** 1 broke the function, and 1 has a flaw confirmed by the judge.
- **RP-E0:** 1 broke the function.
- **No incomplete repairs.** In all three arms, every repair that blocks P2 also blocks the other four attacks. With a terminal, 2, 6 and 7 of 12 repairs were incomplete in R-E2, P-E2 and RP-E2.

**Reading the tests.** The agents opened the repository's iterator test file (`test/libraries/TickIterator.t.sol`) with the file editor in 11 of 12 runs in L-E0, 11 of 12 in R-E0 and 4 of 12 in RP-E0. The same count gives 11 of 12 for P-E0. As in the first experiment, reading the tests did not stop the agents from writing a general fix.

**The LLM judge.**
- Claude Opus 5.5 and GPT-6.1 Sol reviewed the 29 follow-up repairs that compile, pass the functional suite and block every held-out attack.
- Claude Opus 5.5 reported a Medium flaw in two of them, L-E0 rep05 and R-E0 rep07. Each new loop scans the bitmap down with no stop at the end tick. P7 confirms both, as it did for the five repairs with this flaw in the first experiment (section 6).
- GPT-6.1 Sol reported nothing.
- P6 to P8 were run on all 29 repairs. Only these two fail P7, so the reviewers missed none of the flaws these three checks find.

**Blind review.** The follow-up's 36 repairs have not had a blind review. The blinded pack for a person (`pilot/runs/repair_input_study/blind_review/`) still holds the 144 repairs of the first experiment only. Rebuilding it with the new runs would change every random name.

**What the follow-up shows.**
1. **The terminal lowered success for every input, not only for the PoV.** All four drops are between 42 and 75 points, and all four intervals exclude zero. These contrasts are exploratory and not corrected.
2. **Without a terminal, naming the function was enough in half the runs** (6 of 12). With a terminal, it was enough in none.
3. **The PoV and the report each raised success at E0 from 6 to 10 of 12, but neither clearly.** Contrast (c) does not show a difference. Its interval allows anything from no effect to a large one.
4. **Both together added little over either one** (10 to 11 of 12).
5. **This suggests that the low success at E2 in the first experiment came from the terminal more than from what the agent was told.**

**Limits of the follow-up.**
- **Two batches.** The new arms ran on 26 October, and every arm they are compared with ran on 20 October. The model name, the agent and the Docker image are the same, but the provider may have changed the model behind the name. Running P-E0 again next to the new arms would remove this. It was not part of the approved runs.
- **The same limits as the first experiment:** one finding, one model, 12 runs per arm.
