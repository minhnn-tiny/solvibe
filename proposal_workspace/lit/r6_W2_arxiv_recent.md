## Queries run

Search date: 21 October 2026. Round 6, topic W2: a full title screen of every arXiv paper in cs.SE and cs.CR submitted between 15 September and 21 October 2026. The newest paper the API returned was submitted on 20 October. Papers submitted on 21 October were not yet announced, so they are not covered.

How the screen worked. Every title was read. A title went to the candidate list when it could touch the brief's N1 to N7 or the screening topics (AI or agent code security, human versus AI code, smart contracts with LLMs or agents, exploit or PoC generation, vulnerability repair, patch overfitting and held-out tests, tests that encode bugs, task description wording, LLM judges, benchmark contamination). For each candidate the abstract in the arXiv API record was read. For each paper judged tier A or B, the arXiv abstract page was then opened. A keyword pass over all abstracts (smart contract, Solidity, DeFi, EVM, proof of concept, exploit generation, vulnerability repair, overfitting, held-out or hidden tests, human-written, AI-generated code, LLM judge, contamination, memorization) was run afterwards as a recall check. It found no further candidate.

"Already found" counts titles whose arXiv ID or title is in the master index (`lit/master_index.tsv`) or in any round file (`lit/r1_*.md` to `lit/r5_*.md`). The number in brackets counts candidates that an earlier round had already screened out by name: SyzHarness, COMPASS, VulValidate, SWE-DeceptionBench, SWE-Bench Pro V2, and the side-effect loopholes paper (2610.09142). "New relevant" counts tier A or B papers that are in neither.

| # | Query or listing | Source | Titles screened | Candidates opened (abstract read) | Already found | New relevant |
|---|---|---|---|---|---|---|
| 1 | `cat:cs.SE AND submittedDate:[202609150000 TO 202610212359]`, sorted by submission date, 2 pages of 500 | arXiv API | 844 | 73 | 49 [+5] | 12 (1 A: Liu2026-Spoilers; 11 B) |
| 2 | `cat:cs.CR AND submittedDate:[202609150000 TO 202610212359]`, sorted by submission date, 4 pages of 500 | arXiv API | 1,529 | 29 | 42 [+2] | 2 (1 A: Heldt2026-Nonpublic; 1 B: Zhang2026-MobileCybench) |
| 3 | Both listings together, after removing the 107 papers listed in both | arXiv API | 2,266 unique | 94 unique | 70 unique [+6] | 14 (2 A, 12 B) |
| 4 | `https://arxiv.org/list/cs.SE/pastweek?show=2000` and `https://arxiv.org/list/cs.CR/pastweek?show=2000`, as a check that the API missed nothing | arXiv listing pages | 431 IDs; 4 were not in the API set (3 submitted in July 2026 but announced now, 1 replacement of a 2025 paper) | 0 | 0 | 0 |
| 5 | Abstract pages of the 14 tier A and B papers | arXiv abstract pages | 14 | 14 | 0 | 14 (same papers as rows 1 and 2) |

The API did not refuse any call. Calls were made one at a time, 3 seconds apart.

## Tier A papers

### Heldt2026-Nonpublic Does AI Help Cyber Attackers or Defenders? Evidence from Nonpublic Vulnerabilities and Subsequent Attacks
- Authors: Tobias Heldt et al. (4 authors, with Mario Fritz); Year: 2026; Venue: arXiv preprint arXiv:2610.06584 (submitted 5 October 2026, 8 pages)
- URL opened: https://arxiv.org/abs/2610.06584 (arXiv abstract page)
- Status: VERIFIED
- Tier: A
- Touches: N3; also benchmark contamination and exploit generation from the screening list
- Summary: Public vulnerability benchmarks may expose models to published advisories, exploits and fixes, so a high score can reflect prior exposure. The authors test open-weight and proprietary models on exploit generation, vulnerability repair and later attacks in five nonpublic software environments. Some of the vulnerabilities were privately disclosed by the authors and were still unpatched. Deterministic graders written and reviewed by the researchers decide the scores, not LLM judges. Compared with 209 disclosed vulnerabilities and cryptographic challenges, repair scores beat attack scores in two nonpublic environments and fall below them in three. Passing the first security test is not enough: after the first exploit is stopped, another exploit still succeeds in 92 of 524 defender test intervals (the authors note these are not independent).
- Delta: This paper makes the same point as the project's held-out PoV: a repair that blocks the first exploit can still fall to a second one. It also uses unpublished vulnerabilities to rule out training exposure, which is a stronger control than the project's training cutoff (models whose data ends before the findings were published). The paper does not do several things the project does. Its targets are general software, not Solidity contracts with business-logic bugs. The abstract does not say that the second exploit comes from a fixed set written in advance and held back from the repairing agent; it may come from continued attack [uncertain]. It does not show the agent one exploit as a failing test, does not vary what the agent is told or what it can run, has no human-written baseline, and measures no losses in funds. The project should cite it for the "a fix that stops one exploit is not a fix" claim and for its contamination control.

### Liu2026-Spoilers Between Spoilers and Guesswork: Avoiding Over-Specification in Coding Benchmarks
- Authors: Yuanzhe Liu et al. (6 authors, with Avraham Shinnar and Jatin Ganhotra); Year: 2026; Venue: arXiv preprint arXiv:2610.22760 (submitted 16 October 2026)
- URL opened: https://arxiv.org/abs/2610.22760 (arXiv abstract page)
- Status: VERIFIED
- Tier: A
- Touches: N5
- Summary: Coding benchmarks suffer from two opposite problems in how tasks are written. When a task is under-specified, solutions must guess, or fall back on contamination or reward hacking. When a task is over-specified, the text gives away hard steps the benchmark meant to measure. SWE-bench Pro, FEA-bench, Doc2Feat-bench and Multi-SWE-bench add hints taken from the ground-truth solution to their task statements. The authors show that this leaks ground-truth information and over-specifies tasks in some of these benchmarks. They try several levels of task detail and recommend ways to write the smallest useful hints, which they will release. The abstract gives no numbers.
- Delta: This is the closest paper to N5. Both works hold that task text written from the known solution can give the answer away, and both check for this. The paper studies general feature and issue tasks and measures how success rates change. It does not look at security, and it does not test whether wording makes an agent write a vulnerability. The project's pilot found that the wording decided the outcome: when the request described the human's design, all 13 compiled runs wrote the bug, and when it stated the rule the fix restores, 12 of 15 avoided it. The project must keep the request free of hints about the bug and the fix, which is a narrower leak than the one this paper checks. Its method for writing minimal hints could be reused for the project's request-writing check.

## Tier B papers

### Pan2026-SWEMaintain Do Modifications Made by Coding Agents Make Subsequent Software Maintenance Harder?
- Authors: Ruwei Pan et al. (6 authors); Year: 2026; Venue: arXiv preprint arXiv:2610.14768 (submitted 10 October 2026)
- URL opened: https://arxiv.org/abs/2610.14768 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N4
- Summary: SWE-Maintain holds 100 maintenance episodes from 50 real Python repositories. Each episode has three tasks in sequence, with hidden tests checked across the sequence. Each later task is run twice with the same agent and the same tests: once starting from the developers' earlier patches and once starting from the agent's own earlier changes. Across five coding systems, two models and 1,996 paired later tasks, starting from the agent's history lowers resolution by 5.6 percentage points, and by 14.0 points when all earlier tests must also pass. Two thirds of the agent-history starting repositories already fail earlier tests. When the inherited code passes earlier tests, the gap disappears (+2.7 points, 95% CI -0.5 to +6.1).
- Delta: Like N1, it compares human-written and agent-written code under the same agent and the same tests. It measures later functional success, not security. It does not have the agent rewrite a function the human wrote, uses no exploit tests, and has no control group. Its finding that agents leave earlier tests failing contrasts with the project's finding: with a terminal, the agents kept the repository's tests passing even though those tests assert the vulnerable behaviour.

### Takerngsaksiri2026-FollowUpFixes Who Finishes the Job? A Study of Follow-Up Fixes and Commit Authorship on AI Coding Agent Pull Requests
- Authors: Wannita Takerngsaksiri et al. (3 authors); Year: 2026; Venue: arXiv preprint arXiv:2609.26847 (submitted 22 September 2026, 21 pages)
- URL opened: https://arxiv.org/abs/2609.26847 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: The authors follow 6,774 merged pull requests from five coding agents (OpenAI Codex, GitHub Copilot, Devin, Cursor, Claude Code) in the AIDev-pop dataset into their later fixes. They compare them with 5,044 human pull requests from the same repositories and period. Fix links are checked by human annotators and by an LLM judge (Cohen's kappa 0.78 against humans, where two humans reach 0.77). Merged agent pull requests get verified fixes at 1.62 times the odds of human ones. 69.6% of fixes to agent merges come from the same agent, and 76.4% of fix pull requests are agent-authored.
- Delta: This is field evidence that agent code needs fixing more often than human code in the same repositories. It is observational: the agent and human changes are different features, with no shared starting code and no shared test, and fixes are of any kind, not security. The project compares the agent and the human on the same feature, from the same starting code, judged by the same exploit, in Solidity.

### Shi2026-RegressionTasks From Software History to Executable Regression Tasks: A System for Evaluating Software Agents
- Authors: Ruikai Shi et al. (5 authors); Year: 2026; Venue: arXiv preprint arXiv:2610.25308 (submitted 18 October 2026, 22 pages)
- URL opened: https://arxiv.org/abs/2610.25308 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1 (task construction), N3
- Summary: The system builds executable tasks from pairs of bug-introducing and bug-fixing commits and the developers' tests. It takes tests from the fixing side, uses agents to move them into the older version and set up each version's environment, and then replays them. A task is accepted only if its test fails on the introducing version and passes on the fixing version. It builds 172 validated tasks from 522 candidates in 11 Python projects. On 83 enriched tasks, three agents with ten models reach up to 68.7% on repair and 77.1% on regression-test generation; finding the exact root line stays hard.
- Delta: It uses the same introducing and fixing commits as the project and the same check that a test tells the two versions apart (the project's PoV succeeds on the vulnerable version and fails on the fix). The bugs are general Python bugs with developer tests, not security bugs with exploits from audit reports. No agent rewrites the human's function, no tests are held back to judge repairs, and there is no control group.

### Yang2026-CRBugBench (When) Should a Software Factory be Lights-off? Benchmarking Code Review Agents on Bug Detection
- Authors: Chenyang Yang et al. (7 authors); Year: 2026; Venue: arXiv preprint arXiv:2610.13668 (submitted 9 October 2026)
- URL opened: https://arxiv.org/abs/2610.13668 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: CRBugBench pairs human-verified bugs mined from repository history with the pull request that introduced each one. It has 1,000 review tasks from 98 open-source repositories and 800 tasks from one company's private repositories. The best review agent (claude-opus-5 with copilot-cli) catches 71.9% of bugs within its top five comments, up from 47.7% for opus-4.6 five months earlier. Agents do worse on complex changes, on bugs that need reasoning across files, and on the private repositories. Prompts that push the agent to explore more gain up to 5.8% at 10% more cost.
- Delta: It measures LLM review of a change against a known bug, built from bug-introducing pull requests, which is close to how the project traces vulnerability-introducing commits. It only measures recall on known bugs. It does not review human and agent versions of the same code with the same prompt, does not confirm new findings with executable tests, and is not about smart contracts. The project's N6 looks for new flaws in agent code on the control group and requires a PoV for each.

### Guo2026-Groundability Groundability, Not Scale Alone: When Weak Reviewers Can Audit Strong Coding Agents
- Authors: Junyu Guo et al. (4 authors); Year: 2026; Venue: arXiv preprint arXiv:2610.01023 (submitted 1 October 2026)
- URL opened: https://arxiv.org/abs/2610.01023 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6, N3
- Summary: Coding agents can return plausible patches that leave out required behaviour. The authors ask when a weaker model can decide whether a patch really solves its issue, using 411 traces from three agents labelled by execution and 101 controlled cases. Structured evidence that has not been checked raises both the catch rate and wrong rejections. With the official execution results, five of six reviewers improve on both counts on 122 held-out traces. Without official tests, a cascade of static errors and generated tests that first fail on the unpatched repository reaches catch 0.76 and 0.80 with wrong-rejection 0.66 and 0.67 (GPT-5.4 and Gemini traces).
- Delta: It shows that LLM review of patches becomes reliable only when an executable check backs it. This supports the project's rule that every flaw an LLM reviewer reports must be confirmed by a PoV. The paper is about functional issue fixes, not security. It has no human-versus-agent comparison, and "held-out" here means held-out traces for testing reviewers, not held-out exploits for judging repairs.

### Song2026-CrossModel When Does a Second Model Help? Cross-Model Review in LLM Verification
- Authors: Tae-Eun Song (single author); Year: 2026; Venue: arXiv preprint arXiv:2610.01471 (v2; submitted 1 October 2026)
- URL opened: https://arxiv.org/abs/2610.01471 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: A controlled experiment on whether a second review by a different model helps: 30 artifacts with 150 planted errors, 10 review conditions, 900 review sessions, three reviewer models from two developers. The top cross-model reviewer is not significantly different in F1 from the same model reviewing again in a fresh session. The two find partly different errors (Jaccard 41.2%). One fresh same-model review plus one cross-model review finds more planted errors than two same-model reviews (56.7% vs 42.7%, Holm-adjusted p = .006), but not more than two reviews by the top cross-model reviewer.
- Delta: This bears directly on the project's choice of two LLM reviewers. The errors are planted in general code, documents and analyses, not real security flaws in Solidity. Nothing is confirmed by an executable test, and human and agent code are not reviewed side by side.

### Mitsui2026-DecisionPins Pinning Decisions Before Failure: Executable Records of Underspecified Choices in AI-Assisted Code Generation
- Authors: Takeharu Mitsui (single author); Year: 2026; Venue: arXiv preprint arXiv:2610.03237 (submitted 2 October 2026, 24 pages)
- URL opened: https://arxiv.org/abs/2610.03237 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: A natural-language requirement leaves questions open, and a model settles them without saying so. Across 600 test suites generated by three models, 42.7% contain no test that tells the competing readings apart. The method names each open point, builds two throwaway implementations that differ only there, and keeps an input only if running both gives different results. The person's choice is then recorded with that input. On 40 tasks, a separating input is found for 92.5% of open points. As checks on 703 implementations, these records agree with the benchmark's labels on 96-97%, and models honour them in all 210 generations.
- Delta: It shares the pilot's lesson that the wording of a request decides what behaviour the model writes. It studies functional tasks, not security. It adds information to the request on purpose, while the project must keep the request free of hints about the bug and the fix. Its execution check of two readings could be adapted to test whether a project request leaves the safety rule open.

### Kato2026-GTDD GTDD: Generative Test-Driven Development for AI Coding Agents with Adversarial Testing
- Authors: Masahiro Kato (single author); Year: 2026; Venue: arXiv preprint arXiv:2610.02952 (submitted 2 October 2026)
- URL opened: https://arxiv.org/abs/2610.02952 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3, N4
- Summary: Coding agents adapt their code to the examples they see, so passing a fixed set of tests can leave much of the intended behaviour missing. In GTDD a separate testing agent writes new inputs after each candidate is fixed, guided by a human-written behaviour contract. A trusted evaluator checks the inputs and sends reduced counterexamples back to the coding agent. A finite-population analysis bounds false acceptance and shows that fresh random checks after the candidate is committed keep false acceptance under control. On a stateful key-value store, regenerating tests during development gave lower mean failure rates than tests generated once.
- Delta: It names the same risk as N3 and N4, that agents fit the tests they are shown, and the same remedy, judging on inputs the agent never saw. It is about functional correctness on one small system. It has no exploits, no repair of existing vulnerable code, and no study of what the agent is told or can run. The project measures this fitting in real repairs: one repair blocked the shown PoV while a held-out PoV still stole 48.88 ETH.

### Liu2026-InterpretiveLockIn Passing Tests, Missing Semantics: Evidence of Interpretive Lock-In in Plan-Based DataFrame Code Generation
- Authors: Jingjing Liu et al. (4 authors); Year: 2026; Venue: arXiv preprint arXiv:2610.15797 (submitted 11 October 2026); the arXiv comment says it was accepted at the International Conference on Electrical and Computer Engineering Researches (ICECER 2026). I did not check this on a publisher page.
- URL opened: https://arxiv.org/abs/2610.15797 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: On 30 DataFrame tasks derived from TPC-DS, test-guided revision raised test passes from 22/30 to 29/30 and 30/30, yet no generated solution matched its stored reference output. All 77 runs that passed their tests still disagreed with the reference. The failure analysis found tests that left out requirements, took over the candidate's own data layout, used fixtures that could not tell right from wrong, or repeated the code's wrong logic. The study uses one model and one main generation per task, and the authors call the results diagnostic, not causal.
- Delta: It is evidence that tests can encode the wrong behaviour and that passing them misleads. This matches the project's finding that agents with a terminal kept the repository's tests passing while those tests asserted the vulnerable behaviour. Here the tests are written by the model itself, not inherited from the repository, and the code is data processing, not security, with no repair setting.

### Ulesov2026-RiggedBacktest Can LLMs Catch a Rigged Backtest? A Clean-Control Calibration Benchmark
- Authors: Makar Ulesov et al. (4 authors); Year: 2026; Venue: arXiv preprint arXiv:2609.28090 (submitted 23 September 2026)
- URL opened: https://arxiv.org/abs/2609.28090 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: A 96-item benchmark in which every flawed trading backtest has a clean twin that differs in one methodology detail. A deterministic scorer reports flaw recall, false alarms on the clean twins, localization and fix relevance. Over 1,440 audits from four model endpoints, the main DeepSeek auditor reaches 100.0% recall on code, but open prompts flag 93.8% of the clean code twins. A warning that clean twins exist cuts DeepSeek's false alarms on code from 20.8% to 0.0% with no loss of recall. Recall alone ranks three of the four models the same; the false-alarm rate on clean twins separates them by 79 points.
- Delta: It uses the same idea as the project's control group in the LLM review: pair flawed code with correct code to count false alarms. The flaws are planted in finance backtests, not real vulnerabilities, flagged flaws are not confirmed by running code, and there is no human-versus-agent comparison. It supports reporting the reviewers' false-alarm rate on the human version, not only the flaws they find.

### Zhang2026-MobileCybench MobileCybench: Evaluating Agent Vulnerability Discovery via Executable Probes
- Authors: Andy K. Zhang et al. (24 authors); Year: 2026; Venue: arXiv preprint arXiv:2609.23980 (submitted 21 September 2026)
- URL opened: https://arxiv.org/abs/2609.23980 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6; exploit generation from the screening list
- Summary: Agent vulnerability reports are judged by replaying the reported exploit and then running probes, which are executable checks of the app's security properties. A triggered probe shows that the exploit worked and which property it broke, and can catch vulnerabilities nobody knew of when the probe was written. The benchmark covers 13 Android apps with 495 probes. Five coding agents are tested (OpenCode with GPT-5.5, GPT-5.6-Sol and GLM-5.2; Claude Code with Opus 4.8 and Opus 5) in four settings. With only an obfuscated APK, the best agent triggers probes in 53.8% of apps as a malicious app and 16.7% as a remote attacker. Source code raises the overall trigger rate from 28.8% to 32.8%. The work found 23 previously unreported vulnerabilities.
- Delta: Like the project, a reported flaw counts only when an executable check confirms it. Here agents attack apps; they do not write code, and there is no human-versus-agent comparison. The probes are written in advance for general properties, while the project writes a new Foundry PoV for each flaw an LLM reviewer reports.

### Li2026-TestPrism TestPrism: Rethinking Test Evaluation Beyond a Single Reference
- Authors: Han Li et al. (9 authors); Year: 2026; Venue: arXiv preprint arXiv:2610.12289 (submitted 8 October 2026)
- URL opened: https://arxiv.org/abs/2610.12289 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: Judging generated tests against one reference solution ignores other valid solutions and overstates test quality. TestPrism has 300 test tasks from 17 sources and 3,000 candidate implementations, half valid and half not. Its main metric requires the tests to fail on the starting code, accept every valid candidate and reject every invalid one. Across 14 coding-agent setups this reaches 28.00%, against 59.67% when judged on one reference. The authors' TestHelix method adds 8.67 to 9.00 points.
- Delta: The project uses PoVs as the judge of repairs. TestPrism's criterion, reject every wrong solution and accept every valid one, is the property a set of held-out PoVs must have, and its numbers show how often a single check falls short. It is about functional unit tests written by agents, with no exploits and no repair-input study.

## Candidates judged tier C or not relevant

Abstracts read, not written up as blocks:
- Exploit, PoC and vulnerability discovery: TAILOR CVE reproduction (2609.37006); Multi-SWT-Bench reproduction tests (2609.34752); RedHerring decoys against agentic discovery (2609.35909); token costs of agents in vulnerability discovery (2610.11602); security skills for kernel vulnerability detection (2610.25705); belief-guided LLM code auditing (2610.15729); bug-exposing test generation (2610.27694); EviLLM vulnerability injection (2610.03857); JsVul dataset (2609.38012).
- Task wording and clarification: CONTRA (2610.01769); ReqClarifyBench (2610.13022); requirement smells in code generation (2609.29208); prompt language and code generation (2609.18311); prompt-side complexity index (2609.19616); identity cues in prompts (2609.22511); agent instruction categories (2610.21421); Lean specification elicitation (2610.22382); Code of Theseus (2610.20068).
- Benchmark validity, harnesses and judges: SWE-bench leaderboard convergence (2609.17394); harness design studies (2609.20804, 2609.32459); run-to-run variance of coding agents (2609.33812); oracle failures in an agent benchmark (2610.16067); re-executing coding-agent evaluations (2610.14460); executable-contract audit of agent benchmarks (2609.37315); SpecGuardBench (2610.16870); multi-agent code judge grounding (2609.30328); CRJudgeBench (2609.37216); cross-provider review contract (2610.10961); LLM judge scoring format (2610.17158); judge request presentation (2610.11436); deployment-integrity blindness of judges (2610.21135); execution traces misleading video judges (2609.28564); Codoku (2609.34661); specification-driven APR benchmarks (2609.28896).
- Human versus AI and agent code quality: student versus LLM code (2610.00863); humans versus agents in reverse engineering (2610.14960); agent versus human pull request review (2610.15567); LLM fixing versus reimplementing (2609.29410); static quality of LLM code (2610.19167); security risk framework for AI coding tools (2609.18658); case study of assuring AI-written software (2610.08651); vibe coding case study (2610.14103); PACE PRD benchmark (2610.26394); ParanoiaEval (2610.08662); over-defense in coding agents (2610.24949); performance fixes by agents (2609.37985).
- Repair: APR generalizability with ChatGPT (2609.22844); multi-dimensional APR evaluation (2610.08173); PreciseCoder (2610.18755); Poison Valleys (2610.21514); runtime error healing (2609.39086); CrypSteer (2610.25133); HardEval (2610.23685); KEVGraph (2609.24164); approval-to-execution repair analysis (2609.26529); AI-assisted remediation field study (2609.29172).
- Smart contracts and DeFi: Polymarket ghost-filled orders (2609.17902); SoK on DeFi vaults (2610.01300); blockchain IoT logic vulnerabilities (2609.18344); Werracle (2609.30719); L2 deployment decision engine (2610.24198).

## Leads not followed

- Papers submitted on 21 October 2026 were not yet announced on arXiv and could not be screened. A re-run of the same two API queries after 22 October would close this gap.
- Liu2026-InterpretiveLockIn: the ICECER 2026 acceptance comes from the arXiv comment only; the publisher page was not checked.
