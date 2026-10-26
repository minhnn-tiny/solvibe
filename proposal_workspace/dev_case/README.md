# Development case 1: protocol for the student-timed case

**Why this exists.** The committee (iteration 3, item 10) will not accept the proposal unless (a) you commit in writing, with dates, to the month-one development cases, and (b) you complete at least one development case yourself, doing every step the proposal gives to the student, with a probability-selected set of N functions, and keep failures in the record. This folder is that case.

**What it measures.** The time a person needs for each human step of the proposal (`proposal_v32.md`, sections 5.2, 5.4, 5.5, 5.7, 5.8 and 8, "One capped development schedule" and "Exact development decision procedure"), and every unresolved outcome with its reason (section 6.3). Automated steps (agent generation, fuzzing, LLM reviewers) are timed separately as machine time, plus the time you spend supervising them.

**Files to fill in.**

| File | What goes in it |
|---|---|
| `commitment.md` | Your written commitment with dates, hours per week, other duties, and the people for the unexposed and adjudicator roles |
| `exposure_record.md` | Before step 1: which audit findings each person has already seen |
| `timesheet.csv` | One row per work session, filled in as you go, never reconstructed later |

**Timesheet rules.**

- Write the start and end time of every session when it happens.
- `step_id` is one of the steps below (for example `S3`).
- `function_code` is the sealed code from the task list (for example `F07`), or `protocol` for protocol-level work.
- `who` is `student`, `second person`, `adjudicator 1`, `adjudicator 2`, or `machine`.
- `llm_assistance`: `none`, or the tool and model you used. LLM help is allowed where the proposal allows it, but it must be recorded.
- `outcome`: `done`, `failed`, `stopped at allowance`, or `deviation`.
- A failed attempt is a row like any other. Do not delete it and do not retry it silently.

## Step 0. Draw the three development protocols (before anything else)

The three development protocols are drawn by probability sampling, not chosen. This is a protocol-level draw; it is separate from S2, which samples functions inside each drawn protocol.

1. Build `protocol_frame.csv` from the eligible frame: one row per eligible protocol audit, with `protocol_id` and `n_eligible` (its eligible N count). Record every exclusion and its reason under the frame rules. Do not exclude a protocol because you know its audit.
2. Run `python3 draw_protocols.py protocol_frame.csv --count 3 --seed <integer> --out drawn_protocols.csv`. Write the seed and the printed SHA-256 in the timesheet before any other step. The script uses randomized systematic sampling with probabilities proportional to N, as in proposal section 5.2.
3. The three drawn protocols are the development sample. They are not replaced for any reason, and they are removed from the frame used for the main sample.
4. Exposure changes who does the work, not which protocols are in the sample. If you have read a drawn protocol's audit findings (for example one of the five pilot protocols: Licredity, Sorella L2 Angstrom, Ammplify, Sequence, Wannabet), the funded unexposed person performs its blind steps (proposal section 5.4, second sequence). You still time your own steps.

Record the drawn protocols and your exposure in `commitment.md` and `exposure_record.md`.

**Status (26 October 2026).** Step 0 is done. The frame was built in `../evidence/frame_build/` and the draw is in `drawn_protocols.csv`: case 1 The Wildcat Protocol, case 2 Perennial V2 Update #3, case 3 Fenix Finance. Work on the commit that was counted, not on the current branch:

| Case | Repository | Commit |
|---|---|---|
| 1 | `code-423n4/2024-08-wildcat` | `7c5d8389b2a368ce6c4fc79e50c39eac3516ea5e` |
| 2 | `sherlock-audit/2024-08-perennial-v2-update-3` | `ac46a2fc8baf6c827ee20c69eecae66561a5c65f` |
| 3 | `code-423n4/2024-09-fenix-finance` | `33d2b53c972bf8a030e6a33581227844fff8db7b` |

The frame was corrected after the draw (debate round 29). The draw stands. The main sample will be drawn later from `../evidence/frame_build/main_frame.csv`: 152 project units, without Wildcat, Fenix and any Perennial audit.

## Steps

The cap column comes from the proposal's capped development schedule. A cap is the most student time the step may use, not an estimate of what is enough. When a cap is reached, stop and record `stopped at allowance`. Time saved in one step does not move to another step or another implementation.

| Step | Who | What you do | Allowed inputs | Output | Cap |
|---|---|---|---|---|---|
| S1 Frame mapping | Second person, or a script plus a recorded check | List the protocol's audit-scope functions at the pinned commit; mark each finding's root-cause function; apply the single-function rule; label V and N. Record the mapping time in its own timesheet row (proposal section 8, mapping rule) | Audit report, fix commits, code | Labelled frame (kept from you) | 2–4 h per protocol; a mapping that is unfinished or runs over 4 h fails development |
| S2 Sampling and sealing | Script (`sample_and_seal.py`) | Draw up to 1 V and 6 N functions with recorded inclusion probabilities; give you a shuffled list with codes only | Labelled frame | `task_list.csv` (codes, no labels) and a sealed label file with its SHA-256 | minutes |
| S3 Protocol preparation | Student | Threat-model record: assets, entitlements, attacker capital, ordering, oracles; build environment offline | Documentation, code, tests, not the audit | `threat_model.md`, build log | 9 h per case |
| S4 Construction, per function | Student | Request from the template; legitimate behaviour; ordinary functional checks; primary security properties; reachable test setup; checklist | Documentation, signatures, callers, surrounding code; not the audit, fixes or the historical body | Per function: request, checks, properties, checklist result (`built` or reason for failure) | 2.25 h per sampled function, the same for every function, failures included |
| S5 Generation | Machine, supervised by student | Two attempts each for Claude Code and Codex CLI on every built task, as in the main study | Frozen request and workspace | Implementations | S5 and S6 together: 0.15 h per scheduled implementation (historical and each agent attempt) |
| S6 Discovery campaigns | Machine, supervised by student | For every implementation, including the historical one: fuzzing with the frozen properties, and the two LLM reviewers | Implementation, context, properties, request; no audit, no author label | Candidate list per implementation | (inside the S5 cap) |
| S7 Primary confirmation | Student, still without the audit | For each candidate: complete the attack as a PoV, write a function-body-only correction, check attribution; stop at the candidate limit | The originating campaign's material and permitted context only | Confirmation packages | 1.0 h per candidate (at most three per implementation), from the development confirmation reserve of about 24 h; packaging and lock administration included; record the time of each candidate |
| S8 Adjudication and lock | Two adjudicators, then student | Severity and attribution decisions, blind to author as far as possible; then hash and lock the primary records | Packages | Decisions; locked records with hash | paid; 0.5 h per package for each adjudicator, the same for every author; record the time of each package; a package without the required decisions stays unresolved |
| S9 Audit-informed work | Student | Only now open the audit: trace each V finding, build the audit-derived PoV and variant, function-only correction, request diagnostic, check whether the blind campaign rediscovered the audit flaw | Audit, fixes | Secondary records; rediscovery yes or no per V function | S9 and S10 together: 3.75 h per case, for the one constructed V function, scheduled replay and case packaging |
| S10 Replay and packaging | Student | Replay validated PoVs across each function's cohort; package evidence; disclosure check | Locked records | Replay log; package | (inside the S9 cap) |

If a role has no person yet (second person or adjudicators), do the case anyway, mark the step `deviation` in the timesheet, and say who did it instead. The record is still useful, and the committee will see exactly what was and was not done by the planned people.

## Confirmation and review order (proposal section 5.7)

1. Record each implementation's functional status first. A known non-working implementation keeps (W, D) = (0, 0); close its candidates without confirmation.
2. For each working implementation, register its first three candidates in frozen order. Register all bundles of the case before drawing the confirmation order.
3. Draw a seeded random order of the non-empty bundles. Start a bundle only if the development reserve still holds 1.0 hour for each of its candidates; otherwise stop, and mark this and every later candidate "unfinished: reserve". Do not skip to a smaller bundle.
4. Within a bundle, work through candidates in order. A failed confirmation is "rejected" (record the failed criterion). The first candidate whose PoV executes and whose body-only correction blocks the attack is "student-confirmed"; stop the bundle there and mark later candidates "not needed". Unused reserved time returns to the reserve when the bundle ends.
5. Student-confirmed packages go to review in a separately seeded random order, 0.5 hours per package per adjudicator; packages beyond the review reserve are "unfinished: review". A review rejection does not reopen the bundle.

## Closing each outcome (proposal section 6.2)

Apply these rules in the same way to the historical implementation and to every agent attempt.

- Two adjudicators each complete a substantive decision and they disagree: compare reasons once, inside the review cap. If they still do not both confirm, the package is **not confirmed**. Record it; the analysis also treats it as unresolved in a secondary bound.
- An adjudicator cannot judge a required criterion, lacks evidence, or runs out of review time: the outcome is **unresolved**. A statement of inability is not a rejection.
- A candidate cut by the three-candidate limit or the confirmation cap: **not confirmed**, recorded as cut.
- The frozen environment fails for reasons outside the implementation: one rerun in the same environment inside the S5 cap; **unresolved** if it still fails.
- Audit information reaches a primary record before it is locked: record the breach; the outcome is **unresolved** for the primary analysis.
- An implementation that does not compile, or fails ordinary checks that run normally, is a functional failure, not unresolved.

## Decision at the end of the three development cases (proposal section 8)

1. The three development protocols were drawn by `draw_protocols.py` before any outcome (step 0), and are not replaced.
2. Every stage stayed within its cap, and every failure and deviation is in the timesheet.
3. Adjudication was closed with the rules above.
4. Primary records were locked before any audit material was opened.
5. The required roles, blindness, valid execution and logging were achieved. If required work could not be done validly within the caps, the study does not launch.
6. Construction yields are reported by protocol and stratum.
7. Construction warning: let b be the number of functions built and n the number sampled over the three cases. If n = 0, the development record is inadequate and the study does not launch. If V functions were sampled and none was built within the cap, the design returns to review. Otherwise compute the one-sided 95% upper limit Beta^{-1}(0.95; b+1, n-b) (1 when b = n). If it is below 0.7, the study does not launch.
8. Package warning (proposal section 6.3): if it fires, the study does not launch. If an author has no registered candidate, the warning is unassessable: record that, but it does not stop launch.
8a. Candidate demand (proposal section 8, "Preregistered demand rule"): for every author and protocol, record working and unknown-status implementations, every registered candidate with its order and status, the first student-confirmed position, actual and reserved time, and each review outcome. An unfinished candidate counts at its full 1.0 hour. These records set the confirmation reserve before launch; with too little data the rule uses its conservative maximum, and the design may return to review.
9. The separate discovery gate (proposal section 5.9) is completed.
10. Launch also needs frame freezing, the final check on the frozen frame, funding and committee approvals. No case is added to obtain a better result.

## What the committee needs from this case

1. Your filled and signed `commitment.md`, with dates.
2. `timesheet.csv` covering S3, S4, S7, S9 and S10 at least, with one row per session, including failures.
3. For S4, how many sampled functions were built within the allowance, by stratum after unsealing.
4. For S7, how many candidates each campaign produced and how many you confirmed.
5. For every implementation (historical and agent), whether its outcome was resolved, and the reason for each unresolved outcome. There is no minimum number of resolved outcomes and no retry after an unresolved outcome.
6. Anything that did not work as the proposal assumes.

When you finish, tell me in this session. I will compute per-unit hours from the timesheet, rerun the allocation and precision simulations with your numbers, and update the proposal before committee iteration 4.

## Help I can give before you start

- Step 0 (frame and draw) is done.
- List the audit-scope functions of each drawn protocol (S1 script part).
- Run `sample_and_seal.py` once the labelled frame exists (S2).
- Set up the offline build in Docker, as for the 63008 package.
- Prepare the generation and discovery runs (S5, S6) so that your time goes to the human steps.
