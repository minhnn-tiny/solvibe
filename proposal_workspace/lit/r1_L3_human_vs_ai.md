# L3: Security of AI-generated code compared with human-written code (round 1)

Slice L3 of the literature search. Searched on 2026-10-21 following `proposal_workspace/lit/search_protocol.md` and the ARS bibliography agent protocol. The project is described in the project brief (`proposal_workspace/lit/project_brief.md`). The ideas N1 to N7 below are the ones listed in that brief.

## Queries run

"New relevant papers" counts papers that appear as blocks in this file for the first time at that step. Seeds are not counted as new.

| # | Query | Source | Hits looked at | New relevant papers |
|---|---|---|---|---|
| 1 | Forward snowball: papers citing Asare et al. 2023 (arXiv:2204.04741) | Semantic Scholar citations API | 188 | 17 |
| 2 | Backward snowball: reference list of Asare et al. 2023, read in the PDF | arXiv PDF | 58 | 0 (Pearce et al. 2022 is already a seed) |
| 3 | Seed check: the ten seed papers by arXiv ID | arXiv API (id_list) | 10 | 0 (seeds) |
| 4 | human-written AI-generated code security vulnerabilities comparison | OpenAlex | 50 | 4 |
| 5 | agentic pull requests security vulnerabilities human pull requests (years 2025-2026) | OpenAlex | 50 | 6 |
| 6 | coding agents vulnerabilities introduced compared with human developers commits (years 2025-2026) | OpenAlex | 50 | 1 |
| 7 | LLM reintroduce vulnerability vulnerability-introducing commit regenerate code human developer | OpenAlex | 14 | 0 |
| 8 | Title lookup: How to Compare the Security of Code Written by Humans to LLM-generated Code | OpenAlex | 50 | 0 (already found in #4) |
| 9 | user study AI code assistant security participants with and without assistant; LLM generated code compared human written code same tasks security static analysis | OpenAlex | 0 (daily limit used up, HTTP 429) | - |
| 10 | human AI generated code security; Copilot vulnerabilities | DBLP | 0 (blocked by a bot check) | - |
| 11 | Copilot human developers vulnerabilities comparison | Semantic Scholar search | 42 | 1 |
| 12 | Five further Semantic Scholar keyword searches | Semantic Scholar search | 0 (HTTP 429 after retries) | - |
| 13 | SecureVibeBench arXiv ID lookup | WebSearch | 10 | 0 |
| 14 | abs:"human-written" AND abs:"generated" AND abs:security | arXiv API | 37 | 4 |
| 15 | abs:agentic AND abs:"pull requests" AND abs:security | arXiv API | 25 | 1 |
| 16 | abs:Copilot AND abs:"human developers" AND abs:vulnerabilities | arXiv API | 1 | 0 |
| 17 | abs:"vulnerability-introducing" AND abs:LLM | arXiv API | 10 | 0 |
| 18 | abs:"user study" AND abs:AI AND abs:assistant AND abs:secure | arXiv API | 10 | 0 |
| 19 | abs:"smart contract" AND abs:"human-written" AND abs:LLM | arXiv API | 2 | 0 |
| 20 | abs:Solidity AND abs:ChatGPT AND abs:vulnerabilities AND abs:developers | arXiv API | 1 | 1 |
| 21 | abs:"bug-introducing" AND abs:"language model" | arXiv API | 2 | 0 |
| 22 | abs:"AI-generated code" AND abs:"in the wild" AND abs:security | arXiv API | 2 | 1 |
| 23 | abs:"human-written" AND abs:"LLM-generated" AND abs:CWE | arXiv API | 1 | 0 |
| 24 | abs:"Stack Overflow" AND abs:ChatGPT AND abs:vulnerabilities | arXiv API | 1 | 0 |
| 25 | "Comparing Human and LLM Generated Code" "Jury is Still Out" (lead from Egli and Balebako 2026) | WebSearch | 9 | 1 |
| 26 | difference-in-differences Cursor adoption static analysis warnings code complexity | WebSearch | 10 | 1 |
| 27 | "Human vs AI: Insecure Use of Security-Sensitive Functions" (lead from #11) | WebSearch | 9 | 0 (venue check) |
| 28 | agent-authored pull requests more vulnerabilities than human-authored pull requests CodeQL 2026 | WebSearch (extended) | 10 | 1 |
| 29 | LLM regenerate code at vulnerability-introducing commit, does the model repeat the developer's vulnerability | WebSearch (extended) | 10 | 2 |
| 30 | Schreiber Tippe security vulnerabilities AI-generated code public GitHub repositories | WebSearch | 9 | 1 |
| 31 | "Co-authored-by" Copilot or Claude commits, vulnerabilities, AI-assisted commits compared with human commits | WebSearch | 9 | 0 |
| 32 | controlled experiment developers with and without ChatGPT or Copilot, security of code, 2025 | WebSearch (extended) | 9 | 1 |
| 33 | abs:participants AND abs:AI AND abs:"secure code" AND abs:assistance | arXiv API | 3 | 1 |
| 34 | abs:participants AND abs:LLM AND abs:vulnerabilities AND abs:"with and without" | arXiv API | 10 | 0 |
| 35 | abs:"developer patches" AND abs:LLM AND abs:vulnerabilities | arXiv API | 1 | 0 |
| 36 | abs:"human-written" AND abs:agent AND abs:security AND abs:repository | arXiv API | 1 | 0 |
| 37 | abs:"AI-assisted" AND abs:"human-written" AND abs:security AND abs:commits | arXiv API | 2 | 0 |
| 38 | Forward snowball: papers citing SecureVibeBench (arXiv:2509.22097) | Semantic Scholar citations API | 20 | 0 |
| 39 | Forward snowball: papers citing SusVibes (arXiv:2512.03262) | Semantic Scholar citations API | 34 | 2 |
| 40 | Forward snowball: papers citing Cotroneo et al. 2025 (arXiv:2508.21634) | Semantic Scholar citations API | 48 | 0 (relevant ones already found) |
| 41 | Forward snowball: papers citing Perry et al. 2023 (arXiv:2211.03622); titles filtered by security and human-study words | Semantic Scholar citations API | 484 titles filtered, 31 read | 7 |
| 42 | Forward snowball: papers citing Asare et al. 2024 (arXiv:2308.06587); same filter | Semantic Scholar citations API | 36 titles filtered, 8 read | 0 |
| 43 | "The AI tool can't make it any worse" password storage study | WebSearch | 10 | 1 |
| 44 | "Exploring the Impact of Intervention Methods on Developers' Security Behavior in a Manipulated ChatGPT Study" | WebSearch | 10 | 0 (page lookup) |
| 45 | "GitHub Copilot and Code Security: An Empirical Evaluation in the Context of Developers' Professional Experience" | WebSearch | 10 | 0 |
| 46 | Backward snowball: the benchmark comparison table and related-work section of SecureVibeBench | arXiv PDF | 11 benchmarks | 1 |
| 47 | Title searches for published versions of 11 papers | Crossref | 33 | 0 (venue checks) |
| 48 | abs:"human-authored" AND abs:agent AND abs:vulnerabilities | arXiv API | 1 | 0 |
| 49 | abs:"propensity score" AND abs:AI AND abs:code | arXiv API | 1 | 0 |
| 50 | abs:"case-control" AND abs:code AND abs:vulnerabilities | arXiv API | 1 | 1 (tier C, design precedent) |
| 51 | abs:matched AND abs:human AND abs:"LLM-generated" AND abs:security | arXiv API | 2 | 0 |
| 52 | abs:Codex AND abs:"vulnerable code" AND abs:"fixed code" AND abs:prompt | arXiv API | 0 | 0 |
| 53 | LLM-generated Solidity smart contracts compared with human-written contracts, vulnerabilities | WebSearch (extended) | 9 | 1 |
| 54 | AI coding agent reproduces a human developer's vulnerability on the same task, paired comparison, selection bias | WebSearch (extended) | 9 | 0 |
| 55 | code LLM completions reproduce previously patched vulnerabilities, memorization of CVE code | WebSearch | 9 | 1 |
| 56 | DOI lookups for three titles found in #1 | Semantic Scholar paper API | 3 | 0 (counted in #1) |
| 57 | abs:Copilot AND abs:participants AND abs:security | arXiv API | 7 | 1 (tier C) |
| 58 | abs:ChatGPT AND abs:participants AND abs:"secure code" | arXiv API | 0 | 0 |
| 59 | abs:"coding agents" AND abs:"human developers" AND abs:security | arXiv API | 3 | 0 |
| 60 | abs:"gold patch" AND abs:security AND abs:agents | arXiv API | 2 | 0 |
| 61 | abs:"vulnerability-inducing" AND abs:agents | arXiv API | 4 | 0 |
| 62 | abs:"developer-written" AND abs:"LLM-generated" AND abs:vulnerabilities | arXiv API | 2 | 0 |

Saturation: queries #58 to #62 gave no new relevant paper. The last three (#60, #61, #62) meet the stopping rule.

Totals: 69 papers (10 seeds and 59 new). Tier A: 6. Tier B: 34. Tier C: 29. VERIFIED: 66. UNVERIFIED: 3.

## A. Regenerating code where a human wrote a bug or vulnerability

These studies start from real code where a human made a mistake and ask a model to write that code again. They are the closest to N1.

### Asare2023-CopilotVsHumans Is GitHub's Copilot as bad as humans at introducing vulnerabilities in code?
- Authors: Owura Asare, Meiyappan Nagappan, N. Asokan; Year: 2023; Venue: Empirical Software Engineering 28, article 129 (arXiv 2204.04741, v1 April 2022, v5 January 2024)
- URL opened: https://arxiv.org/pdf/2204.04741v5 (full PDF, read in full); https://export.arxiv.org/api/query?id_list=2204.04741 (arXiv record with title, authors, abstract); https://api.crossref.org/works/10.1007/s10664-023-10380-1 (Crossref record, venue and article number)
- Status: VERIFIED
- Tier: A
- Touches: N1 (and N5, by contrast)
- Summary: The paper asks whether Copilot repeats vulnerabilities that human developers wrote. It takes 153 C and C++ vulnerabilities from the Big-Vul dataset (CVEs published 2017 to 2019, fix commit touching one file in one contiguous block, most recent first). For each one it cuts the pre-fix version of the file just before the vulnerable lines and lets Copilot complete it in VS Code, keeping the top suggestion. The output is matched as text against the human's vulnerable code and the human's fix; three coders then re-sort the unmatched outputs without being told which side is the fix. Final result: 51 of 153 (33.3%) repeat the vulnerability, 39 (25.5%) match the fix, and 63 (41.2%) match neither and are not judged. Copilot matched the fix more often for newer CVEs (15.7% in 2017, 40.6% in 2019) and for some weakness types (CWE-20 was always repeated; CWE-190 and CWE-476 were more often fixed). The authors conclude that Copilot "is not as bad as human developers".
- Delta: What it does that the project does not: it covers many C and C++ projects and 28 CWE types; it uses blind human coders to judge closeness to the buggy or fixed code; it relates the outcome to CVE age as a hint of training-data memorization. What the project does that it does not:
  1. Starting code. The prompt is built from the file as it was just before the fix, not from the commit that introduced the vulnerability. That file can contain code written after the bug went in. The project traces each finding to the vulnerability-introducing commit and starts from the code the human had.
  2. What the tool is told. Copilot gets only the file prefix up to the vulnerable line. There is no description of the feature, and in some cases the prefix already ends inside the vulnerable statement (Figure 6 of the paper ends at `if`). The project gives a written feature request and checks that it does not point to the bug or the fix (N5). The project's pilot shows that the wording of the request can decide the outcome; the paper's design cannot observe this.
  3. How security is judged. The paper compares text with the human's buggy code and the human's fix. Nothing is executed. A suggestion that differs from both (41%) gets no security verdict, and a suggestion that matches the fix is not checked for other flaws. The project runs the same exploit test (PoV) on the human's code and the agent's code. The PoV passes on the human's vulnerable code and fails on the human's fix, so it judges any implementation whatever its text.
  4. Which tasks are sampled. Every task is a case where the human wrote a vulnerability, so the human's failure rate is 100% by construction. The 33% for Copilot is therefore a rate conditional on human failure, and it cannot support a general claim that Copilot is less vulnerable than humans. There are no tasks where the human was correct, so the opposite error, where the tool adds a vulnerability the human avoided, is never measured. The paper does not discuss this. The project adds a control group of functions from the same commit that the human wrote correctly; two LLM reviewers check the agent's and the human's versions, and each reported flaw must be confirmed by a new PoV (N6).
  5. Training data. The authors cannot rule out that Copilot saw the fix, and the rise in fixes for newer CVEs fits that explanation. The project picks models whose training data ends before the findings were published.
  6. Tool and runs. One completion tool, one suggestion per prompt, no repeated runs, and no ability to run code. The project compares six agent setups (three agents, two models) that read the repository and, in some settings, run tests.
  7. Not covered by the paper: Solidity and DeFi (N2), held-out PoVs for repair (N3), the repair input study (N4) and loss estimates (N7). The paper only argues that Copilot would be risky for repair because it repeated more bugs than fixes.

### Jesse2023-SStuBs Large Language Models and Simple, Stupid Bugs
- Authors: Kevin Jesse et al. (with Toufique Ahmed, Premkumar T. Devanbu, Emily Morgan); Year: 2023; Venue: 2023 IEEE/ACM 20th International Conference on Mining Software Repositories (MSR), pp. 563-575
- URL opened: https://arxiv.org/abs/2303.11455 (arXiv abstract page); https://arxiv.org/pdf/2303.11455 (PDF, method, results and validity sections read); Crossref record for DOI 10.1109/MSR59073.2023.00082 (venue)
- Status: VERIFIED
- Tier: A
- Touches: N1
- Summary: The study prompts Codex, PolyCoder and CodeGen with the Java code that comes just before a known single-statement bug (16,899 de-duplicated bugs from ManySStuBs4J) and checks whether the completion matches the bug or the fix. Matching is by substring, with a manual check of 401 samples. Codex and the other models produce the known bug about twice as often as the known fix; Codex avoids 13.41% (2,267) of the bugs. Bugs that Codex reproduced had taken developers longer to fix. Adding comments to the prompt lowers the bug rate.
- Delta: It uses the same idea as Asare et al. (rewrite the code at the place where a human erred, then compare with the human's bug and fix) on a much larger set, but for functional bugs, not vulnerabilities. Judgement is by text matching, not by running code, and there is no set of statements the human wrote correctly. The prompt is a code prefix, not a feature request. On training data, the authors argue that leakage would push the models toward the fix, yet the models still produced more bugs. The project uses exploit tests, a control group of human-correct functions, agents, written feature requests, and models whose training data ends before the findings.

### Guo2025-BugReplicators LLMs are Bug Replicators: An Empirical Study on LLMs' Capability in Completing Bug-prone Code
- Authors: Liwei Guo et al. (9 authors, with Jie M. Zhang, Yong Liu); Year: 2025; Venue: arXiv preprint (no published version found on Crossref)
- URL opened: https://arxiv.org/abs/2503.11082 (arXiv abstract page)
- Status: VERIFIED
- Tier: A
- Touches: N1
- Summary: The study asks seven LLMs to complete code at locations in Defects4J where a human bug was later fixed, and compares this with completing ordinary code. Completing bug-prone code is much harder: for GPT-4 the chance of correct code is 12.27% at bug-prone locations against 29.85% for normal code, and correct and buggy completions are about equally likely. 44.44% of the bugs the models write are identical to the human's pre-fix code. Post-processing methods do not lower the error rate much.
- Delta: Same family as Asare et al. and Jesse et al., for Java functional bugs. Unlike them, it contrasts bug-prone locations with ordinary completion tasks, which is a partial answer to the problem that tasks were chosen because the human failed; from the abstract alone it is [uncertain] how the ordinary tasks were chosen and whether they come from the same code. It does not use exploits, agents, feature requests, or a training-cutoff control. The project's control group is matched to the same commit and is judged by exploit tests and confirmed reviews.

### Chen2026-SecureVibeBench SecureVibeBench: Benchmarking Secure Vibe Coding of AI Agents via Reconstructing Vulnerability-Introducing Scenarios
- Authors: Junkai Chen et al. (13 authors, last author David Lo); Year: 2026 (arXiv v1 September 2025, v5 June 2026); Venue: Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (ACL 2026), Long Papers, pp. 24144-24168
- URL opened: https://arxiv.org/abs/2509.22097 (arXiv abstract page); https://arxiv.org/pdf/2509.22097 (PDF; main text and the appendix sections on requirements, functional oracle, data contamination and case studies read); Crossref record for DOI 10.18653/v1/2026.acl-long.1107 (venue)
- Status: VERIFIED
- Tier: A
- Touches: N1, N5, N6
- Summary: The benchmark places code agents in the exact situation where a human developer introduced a vulnerability. It starts from 4,993 OSS-Fuzz and ARVO vulnerabilities in C and C++. Candidate vulnerability-introducing commits come from B-SZZ, and a candidate is kept only if the PoV fails on the fix commit, triggers on the candidate, and fails on the candidate's parent. The agent gets the parent commit and a requirement written by an LLM from the commit message, the human's patch and the issue; the requirement is told to stay security-neutral and is checked by hand. Each output is judged by differential testing against the human's commit with the repository's tests, by the PoV for the original vulnerability, and by Semgrep for new risks. After filtering, 105 tasks from 41 projects remain. Across SWE-agent, OpenHands and Aider with five models, the best setup (SWE-agent with Claude Sonnet 4.5) writes code that is both correct and secure in 23.8% of tasks; Claude Code reaches 17.1% and Codex CLI 19.0%, with 26.7% and 21.8% of their outputs correct but still vulnerable to the human's PoV.
- Delta: This is the closest work to N1. What it does that the project does not: an automatic, PoV-confirmed search for the vulnerability-introducing commit; multi-file tasks in large repositories; a functional check against the human's commit; more agent and model combinations, including Aider, OpenHands, Codex CLI and Claude Sonnet 4.5, which overlap with the project's setups. What the project does that it does not:
  1. Control group. All 105 tasks are cases where the human wrote the vulnerability. There are no tasks the human got right. The only comparison with the human is one Semgrep setting: counting only findings that are not also present after the human's own commit lowers the rate of "suspicious" agent patches from 4.9% to 2.6%. The project measures new flaws on functions the human wrote correctly, from the same commit.
  2. Confirming new flaws. New flaws are Semgrep findings labelled "suspicious"; on a manual sample of 120, about half were false alarms. The project confirms each reported flaw with a new PoV.
  3. Wording of the request. The requirement is checked to be "security-neutral", but the accepted example (rawspeed, ARVO 5296) spells out implementation steps such as clamping to `numeric_limits` and adding an assert. The paper does not test whether the wording changes the outcome. The project's pilot found that wording decided it, and the project checks that requests describe neither the human's design nor the fix (N5).
  4. Training data. Contamination is argued to be small by citing results from other benchmarks. The project chooses models whose training data ends before the findings were published.
  5. Bug type and impact. Memory-safety bugs in C and C++ found by fuzzing, judged by crashes. No business-logic or accounting bugs, no funds, no loss estimate (N2, N7).
  6. No repair stage (N3, N4).

### Zhao2026-SusVibes Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks
- Authors: Songwen Zhao et al. (with Danqing Wang, Kexun Zhang, Jiaxuan Luo, Zhuo Li, Lei Li); Year: 2026 (arXiv v1 December 2025, v4 September 2026); Venue: ICML 2026 (per the arXiv comment "Accepted in ICML 2026"; proceedings page not opened)
- URL opened: https://arxiv.org/abs/2512.03262 (arXiv abstract page); https://arxiv.org/pdf/2512.03262 (PDF; benchmark construction, task verification, results and appendix B read)
- Status: VERIFIED
- Tier: A
- Touches: N1, N5
- Summary: SusVibes has 186 Python feature-request tasks, covering 79 CWE types, built from real projects where a human committed a vulnerable implementation that was later fixed. For each fix commit (from ReposVul and MoreFixes) it goes to the preceding commit, uses SWE-agent to remove the feature's code and to write a feature request, and keeps the human-written tests from the fix commit as security tests (checked and revised by hand). Twelve settings (SWE-agent, OpenHands and Claude Code with four models) are evaluated. SWE-agent with Claude 4 Sonnet solves 57% of tasks functionally, but 79.3% of those solutions are insecure; average joint pass rate is about 10%. Adding vulnerability hints to the request does not fix this.
- Delta: What it does that the project does not: a larger and broader Python benchmark, an automatic task pipeline, and a mitigation experiment. What the project does that it does not: (1) Starting code: tasks start from the commit just before the fix, not from the commit that introduced the vulnerability (SecureVibeBench makes the same point). (2) No comparison with the human beyond the fact that the human's code fails the security tests by construction, and no tasks the human got right. (3) The pipeline requires the feature request to justify every line of the fixed implementation, while not stating security requirements explicitly. So the request may describe behaviour that the fix adds. The project's pilot found that a request stating the rule the fix restores led 12 of 15 runs to avoid the bug, so this choice could change results; the paper does not measure it. (4) The judge is the fix commit's unit tests, not an exploit; no new-flaw review, no contamination control, no Solidity, no loss estimate, no repair (N2, N3, N4, N6, N7).

### Shen2025-SecRepoBench SecRepoBench: Benchmarking Code Agents for Secure Code Completion in Real-World Repositories
- Authors: Chihao Shen et al. (with Connor Dilgren, Purva Chiniya, Luke Griffith, Yu Ding, Yizheng Chen); Year: 2025 (arXiv v1 April 2025, v3 February 2026); Venue: Proceedings of the 3rd International Workshop on Large Language Models for Code (2026), pp. 159-166, per Crossref
- URL opened: https://arxiv.org/abs/2504.21205 (arXiv abstract page); https://arxiv.org/pdf/2504.21205 (PDF, construction section read); Crossref record for DOI 10.1145/3786181.3788703 (venue)
- Status: VERIFIED
- Tier: A
- Touches: N1
- Summary: 318 code completion tasks in 27 C and C++ repositories from ARVO, covering 15 CWEs. In the vulnerable version of the code, the smallest syntax-tree region that covers the developer's fix is masked, and the model fills it in. Each completion is judged by the developers' unit tests and by the OSS-Fuzz proof-of-concept input that crashes the vulnerable version. 29 standalone LLMs and 15 code agents on 3 agent frameworks are evaluated; LLMs struggle, and agents do much better than standalone models.
- Delta: Same technique as the project's main test (remove the code at the vulnerable place, let the model rewrite it, judge with the same exploit), on C and C++ memory bugs. It is framed as a benchmark, not as a comparison with the human, and has no tasks the human wrote correctly. The masked region is placed by the fix, so the location is given and the task is code completion, not a feature request. It starts from the vulnerable version, not the commit that introduced the bug. The project adds the human comparison, the control group, the request-wording check (N5), Solidity (N2), repair (N3, N4) and loss (N7).

## B. Rewriting real code or real tasks, with weaker links to the human's mistake

### Wu2026-LastSecureCode Last Secure Code Benchmark: Is the Code You Vibe Secure?
- Authors: Tianyi Wu et al. (15 authors); Year: 2026; Venue: arXiv preprint (submitted 10 October 2026)
- URL opened: https://arxiv.org/abs/2610.14766 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N5
- Summary: 450 tasks built from 150 real vulnerabilities in seven languages, covering 24 CWEs, in three settings: filling in a function, writing a file, and building a repository's source tree from scratch. Specifications ask only for functionality and never mention security; hidden functional and security tests grade the result. Six frontier agents pass 73.6% to 91.3% of tasks functionally, but the best (Claude Fable 5) is both functional and secure on only 25.1%.
- Delta: Abstract only. Like SusVibes, it builds tasks from real human vulnerabilities and hides security from the request, but it does not compare with the human, has no human-correct control, and uses tests rather than exploits. It covers more languages than the project and the "from scratch" setting, which the project does not use.

### Coppola2026-AgentDebtRR AI Writes Code, Humans Pay the Debt. An Empirical Study on the Sustainability and Evolution of Agent-Generated Code
- Authors: Antonino Coppola et al. (with Matteo Esposito, Rick Kazman, Valentina Lenarduzzi); Year: 2026; Venue: registered report accepted at ESEM 2026 (per the arXiv comment)
- URL opened: https://arxiv.org/abs/2609.04208 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: A study plan. The authors will take issue tickets from the SQuaD dataset (628k candidates), have several LLM agents implement each issue, and compare the agents' code with the developers' actual commits using static analysis, at commit level and across releases. Outcomes are issue localization accuracy and technical debt.
- Delta: It uses the same "rewrite at a real commit and compare with the human" design at large scale, but for technical debt, with static analysis and no results yet. Issues are not chosen because the human made a mistake, so it does not have the project's selection problem, and it has no exploit tests.

### Sajadi2025-PatchSecurity How Safe Are AI-Generated Patches? A Large-scale Study on Security Risks in LLM and Agentic Automated Program Repair on SWE-bench
- Authors: Amirali Sajadi, Kostadin Damevski, Preetha Chatterjee; Year: 2025 (v3 December 2025); Venue: arXiv preprint (no published version found on Crossref)
- URL opened: https://arxiv.org/abs/2507.02976 (arXiv abstract page); https://arxiv.org/pdf/2507.02976 (PDF, introduction and method read)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: For 20,000+ GitHub issues from the SWE-bench train and test sets, the study compares the developers' patches with patches from a standalone LLM (Llama 3.3 70B) and, on 2,200+ test issues, from three agent frameworks (OpenHands, AutoCodeRover, HoneyComb). New vulnerabilities are counted with CodeQL, Semgrep and Bandit. Llama introduced 135 new vulnerabilities against 12 by the developers (about 11 times more); agents also introduced vulnerabilities, more so with more autonomy. Recurring LLM vulnerabilities (CWE-95, CWE-502) differ from the developers'.
- Delta: Same task, same starting code, human versus model, at scale. Issues are not chosen because the developer made a mistake, so the comparison is unconditional. The judge is static analysis, not exploits, and there is no check that a flagged finding is real. The project focuses on known human vulnerabilities, uses executable PoVs, and adds a human-correct control from the same commit.

### Chen2025-AgentPatchQuality Evaluating Software Development Agents: Patch Patterns, Code Quality, and Issue Complexity in Real-World GitHub Scenarios
- Authors: Zhi Chen, Lingxiao Jiang; Year: 2025; Venue: 2025 IEEE International Conference on Software Analysis, Evolution and Reengineering (SANER), pp. 657-668
- URL opened: https://arxiv.org/abs/2410.12468 (arXiv abstract page); Crossref record for DOI 10.1109/SANER64311.2025.00068 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 4,892 patches from 10 top agents on the 500 SWE-bench Verified issues are compared with the developers' gold patches. 170 issues stay unresolved. Even passing patches often change different files and functions than the gold patch. Most agents kept reliability and security (no new bugs or vulnerabilities by the quality analysis used); some raised complexity, many reduced duplication.
- Delta: Agent versus human patch on the same issue and starting code, with static code-quality measures. No exploit tests, no tasks chosen for human vulnerabilities, and security is one quality dimension among several.

### Ullah2025-CVEGenie From CVE Entries to Verifiable Exploits: An Automated Multi-Agent Framework for Reproducing CVEs
- Authors: Saad Ullah et al. (8 authors, with Hammond Pearce, Christopher Kruegel, Giovanni Vigna, Gianluca Stringhini); Year: 2025 (v2 February 2026); Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2509.01835 (arXiv abstract page); https://arxiv.org/pdf/2509.01835 (PDF, applications discussion and case study read)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: CVE-Genie is an LLM multi-agent framework that rebuilds the vulnerable environment for a CVE and produces a verifiable exploit. It reproduces about 51% (428 of 841) of CVEs published in 2024-2025 at an average cost of $2.77 per CVE.
- Delta: In its applications discussion, the paper proposes to "prompt the LLM to implement the functionalities in the vulnerable functions" and test the result with the reproduced exploit. It does not run that experiment. A reviewer could cite this sentence as an earlier statement of the project's main test. The project runs the test, adds the human comparison and the control group, and works on Solidity findings from audit contests rather than CVEs.

### Karanjai2023-SmartContractCreation An Empirical Study of AI-based Smart Contract Creation
- Authors: Rabimba Karanjai, Edward Li, Lei Xu, Weidong Shi; Year: 2023; Venue: arXiv preprint (the PDF running header reads "Who is Smarter? An Empirical Study of AI-based Smart Contract Creation")
- URL opened: https://arxiv.org/abs/2308.02955 (arXiv abstract page); https://arxiv.org/pdf/2308.02955 (PDF, dataset and workflow sections read)
- Status: VERIFIED
- Tier: B
- Touches: N1, N2
- Summary: The study collects Solidity files from GitHub projects with at least 50 stars, builds prompts from their code comments, asks GPT-3.5 and PaLM 2 to write the contracts, runs the projects' own unit tests (about 7 per problem), and scans the output with MythX. It reports that the generated contracts introduce security bugs and lose correctness.
- Delta: An early Solidity study that rewrites human contracts from their documentation and reuses the projects' tests. From the parts read, it is [uncertain] whether the human contracts were scanned the same way for a direct comparison. It uses a static scanner, not exploits, and its tasks are not chosen for known human vulnerabilities. The project uses audit-contest findings with exploit tests and fund losses.

### Melo2026-PreferVulnerable Do Language Models Prefer Vulnerable Code? A Probabilistic Study of Insecure Code Preference
- Authors: Rui Melo et al. (with Sofia Reis, Andre Catarino, Rui Abreu) [uncertain: the Semantic Scholar record shows the first author as "Me-Lo Rui"]; Year: 2026; Venue: IEEE International Conference on Software Testing, Verification and Validation (ICST) 2026 [uncertain: from the DOI prefix ICST69053 and the DBLP key conf/icst/MeloRCA26 shown by Semantic Scholar]
- URL opened: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ICST69053.2026.00075 (Semantic Scholar record with abstract); the IEEE Xplore page https://ieeexplore.ieee.org/document/11600473/ returned no content
- Status: UNVERIFIED (only the Semantic Scholar record was readable; no publisher page, arXiv page or PDF opened)
- Tier: B
- Touches: N1
- Summary: Per the Semantic Scholar abstract, the study measures how likely code LLMs are to produce the vulnerable or the patched version of real code, using 2,422 vulnerability-patch pairs over 25 CWEs (Delta-Secommits). Models prefer the vulnerable version in about 92% of cases.
- Delta: It asks the Asare question (would the model write the human's vulnerable code or the fix?) through model probabilities, without generation, agents, exploits or a control group.

## B. Same task, human versus AI, tasks not chosen because the human failed

### Cotroneo2025-HumanVsAI Human-Written vs. AI-Generated Code: A Large-Scale Study of Defects, Vulnerabilities, and Complexity
- Authors: Domenico Cotroneo, Cristina Improta, Pietro Liguori; Year: 2025; Venue: 2025 IEEE 36th International Symposium on Software Reliability Engineering (ISSRE), pp. 252-263
- URL opened: https://export.arxiv.org/api/query?id_list=2508.21634 (arXiv record with abstract); https://arxiv.org/pdf/2508.21634 (PDF, contributions, dataset and RQ sections read); Crossref record for DOI 10.1109/ISSRE66568.2025.00035 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: More than 500k Python and Java functions. Human functions come from CodeSearchNet; ChatGPT versions come from the HMCorp dataset (288,508 Python and 222,335 Java pairs), and DeepSeek-Coder and Qwen-Coder versions are generated from each function's docstring and signature. Defects are mapped to Orthogonal Defect Classification and vulnerabilities (found with Semgrep) to CWE. AI code is simpler and more repetitive but has more high-risk vulnerabilities, such as command injection and hardcoded secrets (+5k vulnerable samples in Python, +18k in Java).
- Delta: A large paired comparison of human and AI code for the same function description. Pairs are not chosen for human mistakes, so it estimates average differences rather than behaviour at known human vulnerabilities. Judgement is static analysis only, and the model gets a docstring and signature, not the repository context the human had (Egli and Balebako 2026 make this point). No agents, exploits or control matched to a commit.

### Improta2026-CQBench What is the Difference Between Me and You? Benchmarking the Quality Gap Between Human-Written and AI-Generated Code
- Authors: Cristina Improta, Pietro Liguori, Domenico Cotroneo; Year: 2026; Venue: arXiv preprint (under peer review, per the arXiv comment)
- URL opened: https://arxiv.org/abs/2609.12708 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 787,562 function pairs in Python, Java and C. Each human function mined from open source is paired with versions generated from its docstring by OpenAI GPT models, DeepSeek-Coder and Qwen2.5-Coder. AI code is about half the size and branching of human code. LLMs produce more and more severe security findings in Python and Java, but fewer high-severity memory-safety findings than humans in C. Once size is controlled for, complexity metrics carry little signal. The authors release CQBench, 27,346 issue-prone tasks.
- Delta: Extends Cotroneo et al. 2025 to C and adds a size control. Same limits for the project's purpose: static analysis, docstring prompts, no selection on human vulnerabilities, no exploits, no agents.

### Licorish2025-JuryOut Comparing Human and LLM Generated Code: The Jury is Still Out!
- Authors: Sherlock A. Licorish et al. (with Ansh Bajpai, Chetan Arora, Fanyu Wang, Kla Tantithamthavorn); Year: 2025; Venue: arXiv preprint (no published version found on Crossref)
- URL opened: https://arxiv.org/abs/2501.16857 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 72 software engineering tasks are solved by human programmers and by GPT-4 in Python. Code is assessed with Pylint, Radon, Bandit and test cases. Human code follows coding standards better. Both have security flaws; human code shows a greater variety of problems, while GPT-4 code has more severe outliers. GPT-4 code passes more test cases.
- Delta: Same prompt for humans and the model, which Egli and Balebako 2026 call fairer than most designs; they also note that one person wrote all the human code. Security is judged by Bandit only. Tasks are not chosen for human mistakes. No real repositories, agents or exploits.

### Lee2026-SecuritySensitiveFunctions Human vs AI: Insecure Use of Security-Sensitive Functions in AI-generated Code in Comparison to Human-written Code
- Authors: JoonKu Lee, Sieun Ju, Seunghoon Woo, Heejo Lee; Year: 2026; Venue: Proceedings of the 41st ACM/SIGAPP Symposium on Applied Computing (SAC '26), pp. 2045-2047 (3-page short paper)
- URL opened: https://ssp.korea.ac.kr/assets/papers/SAC26.pdf (PDF with title, authors, abstract, method); Crossref record for DOI 10.1145/3748522.3779860 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 113 Stack Overflow questions about C are used as the same input for humans and LLMs. The human code is the first version of each accepted answer; the AI code comes from GPT-5, Claude Sonnet 4 and Gemini 2.5 Pro. Cppcheck, Flawfinder and Semgrep look for unsafe use of security-sensitive C library functions. LLMs use these functions more often, but humans use them more dangerously.
- Delta: Same question, human versus model, for C library misuse. Human answers are not chosen for mistakes. Static tools only; no repositories, agents or exploits.

### Hamer2024-ChatGPTvsSO Just another copy and paste? Comparing the security vulnerabilities of ChatGPT generated code and StackOverflow answers
- Authors: Sivana Hamer, Marcelo d'Amorim, Laurie Williams; Year: 2024; Venue: 2024 IEEE Security and Privacy Workshops (SPW), Deep Learning Security and Privacy Workshop, pp. 87-94
- URL opened: https://export.arxiv.org/api/query?id_list=2403.15600 (arXiv record with abstract); Crossref record for DOI 10.1109/SPW63631.2024.00014 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: Security-related Java questions from an existing Stack Overflow dataset are given to ChatGPT. 108 snippets from each source are scanned with CodeQL. ChatGPT code has 248 vulnerabilities against 302 in Stack Overflow answers, 20% fewer and a statistically significant difference; ChatGPT shows 19 CWE types against 22.
- Delta: Same question, human answer versus model answer. The human answers come from a dataset of security-related posts, not from code chosen for known mistakes. CodeQL only; snippets, not repositories; no agents, exploits or control matched to a commit.

### Rashidi2026-Provenance Open-Source Intelligence for Code Provenance and the Security Patterns that Separate Human and Large-Language-Model Implementations of Common Programming Tasks
- Authors: Mohammadreza Rashidi; Year: 2026; Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2607.12524 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 31 security-sensitive tasks (for example OAuth with PKCE, JWT verification, password hashing, SQL access) are implemented by 9 open-weight LLMs and taken from Stack Overflow answers, in four languages; 528 samples are scored with fixed security and style detectors. A classifier recovers human or model origin with 93% accuracy. The sources differ in security patterns in every language. In a repair case study, models fix 77% of 21 insecure seeds, but often remove the insecure pattern without adding the correct defence.
- Delta: Same task, human versus model, with pattern detectors instead of exploits, and no selection on human mistakes. The partial-fix finding is close to the project's observation that agents fix only the case the shown PoV covers, but it is not tested with held-out exploits.

### Mahmud2026-IllusionOfSafety The Illusion of Safety: Multi-Tier Verification of AI vs. Human C++ Code
- Authors: Saif Mahmud et al. (with Fadul Sikder, Yuede Ji, Haotian Zhang, Yu Lei); Year: 2026 (v3 August 2026); Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2607.00107 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N6
- Summary: VULBENCH-CPP holds 8,918 C++ programs for 851 competitive-programming tasks, written by humans and by three open-weight LLMs (Gemma 3 27B IT, Llama 3.3 70B Instruct, Qwen 2.5 Coder 32B Instruct). Each program is checked by functional tests, static analysis, sanitizers (ASan and UBSan) and bounded model checking (ESBMC). Accounting for clustering by task and controlling for code length and test pass rate, AI code is about twice as likely as human code to trigger a confirmed runtime violation. Under static analysis alone the two look equally safe, which the authors trace to code length.
- Delta: Same tasks, human versus model, with execution-based confirmation and an explicit statistical control for task and size; tasks are not chosen for human mistakes. The point that static findings mislead and runtime confirmation is needed supports the project's choice to confirm each flaw with a PoV (N6). Toy tasks, no repositories, no agents, no exploits for business logic.

### Shaw2026-ComparedToWhat Compared to What? A Human-Anchored Security Benchmark for LLM-Generated Infrastructure-as-Code
- Authors: Animesh Shaw; Year: 2026 (v2 September 2026); Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2608.28021 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 100 deployment scenarios, 12 model configurations, 1,196 IaC artifacts, and 634 human-written IaC templates, all scanned with Checkov, Trivy and KICS. Vulnerability density falls with artifact size, so unmatched comparisons measure size, not security. Matched by size, every model configuration exceeds the human baseline by 3.21 to 3.87 times (3.50 pooled). Version 2 corrects the paper: most scenarios prescribe a security state, so part of the result measures instruction-following.
- Delta: It builds an explicit human baseline and shows how a confounder (size) can create or hide differences. The human templates are matched by size, not by task, and judgement is by policy scanners. The v2 correction is a concrete case of the request wording shaping the outcome, which the project checks for (N5).

### Egli2026-HowToCompare How to Compare the Security of Code Written by Humans to LLM-generated Code
- Authors: Jasmine Egli, Rebecca Balebako; Year: 2026 (v2 June 2026); Venue: arXiv preprint (also listed in the ZHAW repository)
- URL opened: https://arxiv.org/abs/2606.00186 (arXiv abstract page); https://arxiv.org/pdf/2606.00186 (PDF, related work and feasibility study read)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: The paper proposes an open-source framework for "species-fair" experiments that compare human-only, LLM-only and mixed code under equal conditions, logging prompts, timing and settings and running static and dynamic checks in containers. A feasibility study uses 13 exercises (Python security exercises and Advent of Code 2024), five OpenAI models and 60 generations per pair (3,832 executed, 2,615 correct). The authors note that choosing top-ranked human solutions created a ceiling effect.
- Delta: A methods paper on fair human versus model comparison. It reviews Cotroneo et al. and Licorish et al. and notes that the human and model often start from different tasks. Its selection worry runs the other way from the project's: choosing the best human solutions makes humans look better, while the project's treatment group is chosen because the human failed. It has no real repositories, agents, exploits or control matched to a commit.

### Pearce2022-Asleep Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions
- Authors: Hammond Pearce et al. (with Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, Ramesh Karri); Year: 2022; Venue: 2022 IEEE Symposium on Security and Privacy (S&P), pp. 754-768 (reprinted in Communications of the ACM, 2025)
- URL opened: https://export.arxiv.org/api/query?id_list=2108.09293 (arXiv record with abstract); Crossref search results showing DOI 10.1109/SP46214.2022.9833571 (S&P 2022) and DOI 10.1145/3610721 (CACM 2025)
- Status: VERIFIED
- Tier: B
- Touches: N1 (background)
- Summary: Copilot completes 89 scenarios built around high-risk CWEs, varying the weakness, the prompt and the domain. Of 1,689 programs, about 40% are vulnerable (CodeQL and manual review).
- Delta: The standard reference for insecure AI code and the starting point for Asare et al. 2023. No human comparison, synthetic scenarios, static and manual judgement. The project compares with the human on real code and judges with exploits.

## B. User studies with and without an AI assistant

### Perry2023-InsecureCode Do Users Write More Insecure Code with AI Assistants?
- Authors: Neil Perry, Megha Srivastava, Deepak Kumar, Dan Boneh; Year: 2023; Venue: Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS), pp. 2785-2799
- URL opened: https://export.arxiv.org/api/query?id_list=2211.03622 (arXiv record with abstract); https://arxiv.org/pdf/2211.03622 (PDF, study design section read); Crossref record for DOI 10.1145/3576915.3623157 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 47 participants (33 with an assistant based on codex-davinci-002, 14 without) solved five security-related tasks in Python, JavaScript and C. Participants with the assistant wrote significantly less secure code on most tasks and were more likely to believe their code was secure. Participants who trusted the AI less and reworked their prompts wrote fewer vulnerabilities.
- Delta: A randomized comparison of humans with and without AI on the same tasks. Tasks are designed, not taken from real human mistakes, and judged by manual review. The project compares an autonomous agent with the original developer on real code, using exploits.

### Sandoval2023-LostAtC Lost at C: A User Study on the Security Implications of Large Language Model Code Assistants
- Authors: Gustavo Sandoval, Hammond Pearce, Teo Nys, Ramesh Karri, Siddharth Garg, Brendan Dolan-Gavitt; Year: 2023; Venue: 32nd USENIX Security Symposium (USENIX Security '23), pp. 2205-2222
- URL opened: https://www.usenix.org/conference/usenixsecurity23/presentation/sandoval (USENIX page with abstract); https://export.arxiv.org/api/query?id_list=2208.09727 (arXiv record)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 58 student programmers implemented a singly linked "shopping list" in C, with or without an LLM assistant (Codex). AI-assisted users produced critical security bugs at a rate no more than 10% higher than the control group, so the authors see little added risk in this setting.
- Delta: A controlled user study on one designed task in C. No real project history, no agents, no exploits. Its result (little difference) contrasts with Perry et al., which shows that the answer depends on the task.

### Asare2024-UserCopilot A User-centered Security Evaluation of Copilot
- Authors: Owura Asare, Meiyappan Nagappan, N. Asokan; Year: 2024; Venue: Proceedings of the IEEE/ACM 46th International Conference on Software Engineering (ICSE 2024), pp. 1-11
- URL opened: https://export.arxiv.org/api/query?id_list=2308.06587 (arXiv record with abstract); Crossref record for DOI 10.1145/3597503.3639154 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 25 participants solved programming problems with potentially vulnerable solutions, with and without Copilot. Copilot access went with more secure solutions on the harder problem and made no difference on the easier one, with no extra effect on particular vulnerability types.
- Delta: The follow-up that Asare et al. 2023 called for: a with-and-without comparison on the same tasks. Small sample, designed tasks, manual judgement. The project studies agents rather than human-AI pairs, on real audited code with exploits.

### Oh2024-PoisonedChatGPT Poisoned ChatGPT Finds Work for Idle Hands: Exploring Developers' Coding Practices with Insecure Suggestions from Poisoned AI Models
- Authors: Sanghak Oh, Kiho Lee, Seonhye Park, Doowon Kim, Hyoungshick Kim; Year: 2024; Venue: 2024 IEEE Symposium on Security and Privacy (S&P), DOI 10.1109/SP54263.2024.00046
- URL opened: https://export.arxiv.org/api/query?id_list=2312.06227 (arXiv record with abstract); Crossref search result for the DOI (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: An online survey of 238 developers and students, and a lab study with 30 professional developers doing three tasks. Developers using a poisoned ChatGPT-like tool included insecure code more often than those using an IntelliCode-like tool or no tool.
- Delta: Shows that assistant suggestions steer human security outcomes, with a no-tool control. It studies poisoned models and human developers, not agents on real project history; no exploits.

### Serafini2025-ManipulatedChatGPT Exploring the Impact of Intervention Methods on Developers' Security Behavior in a Manipulated ChatGPT Study
- Authors: Raphael Serafini et al. (with Asli Yardim, Alena Naiakshina); Year: 2025; Venue: Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems, pp. 1-26
- URL opened: https://casa.rub.de/forschung/publikationen/detail/exploring-the-impact-of-intervention-methods-on-developers-security-behavior-in-a-manipulated-chatgpt-study (Ruhr University Bochum publication page with title, authors, abstract); Crossref record for DOI 10.1145/3706598.3713989 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 76 freelance developers did a password-storage task in four conditions; three used a manipulated ChatGPT-like assistant that suggested an insecure MD5 implementation. Developers largely trusted the AI code. Security prompts, warnings and guidelines raised awareness, but 32% of developers who were warned still adopted the weak implementation, often confidently.
- Delta: A controlled study of how humans take up insecure AI suggestions. No real project code, no agents, no exploits.

### Yardim2026-PasswordStorage "The AI tool can't make it any worse." Investigating Developers' Security Behavior with AI Assistants in a Password Storage Study
- Authors: Asli Yardim et al. (with Alena Naiakshina, Joshua Speckels, Anna-Marie Ortloff, Nadine Jost, Raphael Serafini) [uncertain author order: Crossref lists Yardim first, the Bochum page lists Naiakshina first]; Year: 2026; Venue: Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems, pp. 1-33
- URL opened: https://casa.rub.de/forschung/publikationen/detail/the-ai-tool-cant-make-it-any-worse-investigating-developers-security-behavior-with-ai-assistants-in-a-password-storage-study (publication page with title, authors, abstract); Crossref record for DOI 10.1145/3772318.3791693 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1, N5
- Summary: A lab study with 21 computer science students and an online study with 80 freelance developers implemented password storage under four conditions: no instructions, AI assistance, security instructions, or both. Many participants relied on AI code for the security part and put convenience first. Explicit security instructions moved them toward secure results.
- Delta: A factorial design that separates the effect of the AI from the effect of the instructions. Its finding that instructions change outcomes parallels the project's finding that the feature request's wording changes the agent's outcome (N5). Human participants, a designed task, no exploits.

### Jost2026-Gemini The Impact of AI-Assisted Development on Software Security: A Study of Gemini and Developer Experience
- Authors: Nadine Jost et al. (with Benjamin Berens, Manuel Karl, Stefan Albert Horstmann, Martin Johns, Alena Naiakshina); Year: 2026; Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2603.15298 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 159 developers did a security-related programming task with no AI tool, the free version of Gemini, or the paid version. No significant security difference was found between conditions; programming experience improved security and was not replaced by Gemini.
- Delta: A three-arm controlled study on one designed task. Human participants, no real project history, no agents, no exploits.

### Mousavi2026-SecurityAPIs Understanding the Impact of AI Code Assistants on Security API Usage: An Empirical Study
- Authors: Zahra Mousavi et al. (with Chadni Islam, M. Ali Babar, Alsharif Abuadbba, Kristen Moore); Year: 2026; Venue: RAID 2026 (per the arXiv comment)
- URL opened: https://arxiv.org/abs/2607.11348 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 44 professional developers completed security API tasks with and without GitHub Copilot. Copilot improved functional correctness and slightly reduced some insecure patterns, but did not significantly improve secure API use. Developers rarely raised security concerns with Copilot, and many did not notice that their final code was insecure.
- Delta: With-and-without comparison on designed API tasks. Human participants, no real project history, no exploits.

### Khalid2026-DontVerify (Don't) Trust, but (Don't) Verify: Developers' Attention to Security in AI-Generated Code
- Authors: Hamza Khalid et al. (with Ronald E. Thompson III, Alejandra Sabater, Perucy Mussiba, Kelsey R. Fulton, Daniel Votipka); Year: 2026; Venue: to appear at IEEE S&P 2027 (per the arXiv comment)
- URL opened: https://arxiv.org/abs/2609.21020 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N6
- Summary: 100 participants produced secure and functional code for four C linked-list tasks by cycling through five AI suggestions of varying security and functionality, picking one and editing it. A survey and 23 interviews explore how they judged the security of AI code.
- Delta: Studies how humans check AI code for security, which relates to who reviews agent code (N6). The project uses LLM reviewers with PoV confirmation instead of human reviewers.

### Biolo2026-PatchingHumanStudy Helpful or Harmful? Evaluating LLM-Assisted Vulnerability Patching via a Human Study
- Authors: Giulian Biolo, Michael Tezza, Yuanjun Gong, Fabio Massacci; Year: 2026; Venue: arXiv preprint (study plan with a pilot)
- URL opened: https://arxiv.org/abs/2606.25973 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3, N4
- Summary: A planned balanced crossover experiment comparing LLM-assisted vulnerability patching with manual debugging. A web app runs the code and includes hidden "Ghost Tests" that check the patch beyond the visible functional tests. Speed, functional and security success, and perception will be measured; a small pilot has been run.
- Delta: Hidden tests that judge a patch beyond what the participant sees are close to the project's held-out PoVs (N3), but here the patcher is a human with or without LLM help, not an agent. No results yet.

## B. Mining studies of AI-authored code, commits and pull requests

### Fu2025-CopilotGitHub Security Weaknesses of Copilot-Generated Code in GitHub Projects: An Empirical Study
- Authors: Yujia Fu et al. (with Peng Liang, Amjed Tahir, Zengyang Li, Mojtaba Shahin, Jiaxin Yu, Jinfu Chen); Year: 2025; Venue: ACM Transactions on Software Engineering and Methodology 34, pp. 1-34
- URL opened: https://export.arxiv.org/api/query?id_list=2310.02059 (arXiv record with abstract); Crossref record for DOI 10.1145/3716848 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1, N4
- Summary: 733 code snippets from GitHub projects that were attributed to Copilot, CodeWhisperer or Codeium were analysed. 29.5% of Python and 24.2% of JavaScript snippets had security weaknesses, across 43 CWE types, eight of them in the 2023 CWE Top 25. Given the static analysers' warnings, Copilot Chat fixed up to 55.5% of the issues.
- Delta: Studies AI code in real projects, but has no human baseline, uses static analysis, and depends on developers declaring AI use. The repair step gives the model a warning message, a different input from the project's report and PoV conditions (N4).

### Xia2026-PostMergeFate Do These Violent Delights Have Violent Ends? Measuring the Post-Merge Fate of Agentic Code
- Authors: Chunqiu Steven Xia, Courtney Miller; Year: 2026; Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2607.09902 (arXiv abstract page); https://arxiv.org/pdf/2607.09902 (PDF, method and results sections read)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: Agentic and human contributions merged between May 2025 and May 2026 in 182 repositories are tracked line by line after merge with git blame. Semgrep, OSV-Scanner and SonarQube run after every commit, and models adjust for file role and repository. Agentic contributions need more corrective maintenance and introduce Semgrep security findings at 1.14 times the human rate (1.51 times for high-severity findings) and dependency vulnerabilities at 1.10 times (1.15 times for high and critical).
- Delta: A direct 2026 comparison of agent-authored and human-authored code in the same repositories, with statistical adjustment instead of task matching. Static and dependency scanners, not exploits. Contributions are not paired by feature, and author labels come from commit heuristics that can be wrong.

### Kraishan2026-FiveAgents Not All Agents Are Equal: Code Quality and Post-Merge Maintenance Across Five Autonomous Coding Agents in the Wild
- Authors: Obada Kraishan; Year: 2026; Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2609.17598 (arXiv abstract page); https://arxiv.org/pdf/2609.17598 (PDF, baseline construction and results read)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 37,623 pull requests from the AIDev dataset: 33,596 by five commercial agents (Codex, Devin, Copilot, Cursor, Claude Code) and 4,027 by humans, kept only from repositories that also have agent pull requests, in the same time window, and capped per repository. Security smells are found with a regex catalogue mapped to eight CWE classes. Pooled agent code is less likely than human code to contain a security smell (odds ratio 0.63), driven by fewer hardcoded credentials and eval-style constructs. Revert rates differ by vendor (Codex 6.1%, humans 11.5%, Devin 14.5%).
- Delta: Uses a human baseline matched by repository and time, and says that task mix and size remain confounders. Regex smells, not exploits; pull requests are not paired by feature. Its result (agents less smelly) points the other way from Xia and Miller 2026, which shows how much these comparisons depend on design.

### Wang2025-AICodeInTheWild AI Code in the Wild: Measuring Security Risks and Ecosystem Shifts of AI-Generated Code in Modern Software
- Authors: Bin Wang et al. (9 authors, Peking University); Year: 2025; Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2512.18567 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: A detector labels commits, files and functions as human-written or AI-generated in the top 1,000 GitHub repositories (2022-2025) and in 7,000+ CVE-linked changes. AI code is common but concentrated in glue code, tests, refactoring and documentation; core logic and security-critical configuration stay mostly human. Some CWE families are overrepresented in AI-tagged code, and near-identical insecure templates recur across unrelated projects. In mixed human and AI edit chains, humans act as security gatekeepers, and AI-introduced defects persist longer when review is shallow.
- Delta: Compares human and AI code inside real vulnerability life cycles, but AI authorship comes from a detector and code is not paired by task. No exploits or agents run by the authors.

### Mao2026-AICodeMeasurement A Large-Scale Comprehensive Measurement of AI-Generated Code in Real-World Repositories
- Authors: Tianhao Mao et al. (with Dongfang Zhao, Haixu Tang, XiaoFeng Wang, Hang Zhang); Year: 2026 (v3 July 2026); Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2603.27130 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: Compares AI-assisted and human-written code in real repositories on code-level metrics (complexity, style, security quality) and commit-level metrics (size, frequency, stability). Real-world differences on code-level metrics are small, unlike lab studies, and security quality varies across languages.
- Delta: Unpaired real-world comparison with static metrics. Its "small differences in the wild" finding is a useful counterpoint to lab studies, but it says nothing about behaviour at known human vulnerabilities.

### He2026-CursorDiD Speed at the Cost of Quality: How Cursor AI Increases Short-Term Velocity and Long-Term Complexity in Open-Source Projects
- Authors: Hao He, Courtney Miller, Shyam Agarwal, Christian Kästner, Bogdan Vasilescu; Year: 2026; Venue: Proceedings of the 23rd International Conference on Mining Software Repositories (MSR '26), pp. 181-193
- URL opened: https://arxiv.org/abs/2511.04427 (arXiv abstract page); Crossref record for DOI 10.1145/3793302.3793349 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: A difference-in-differences design compares GitHub projects that adopted Cursor with a matched control group of similar projects that did not. Adoption brings a large but short-lived rise in development velocity and a lasting rise in static-analysis warnings and code complexity, which in turn slow later development.
- Delta: A matched control design at the project level, a model for a causal comparison with humans. Outcomes are warnings and complexity, not vulnerabilities confirmed by exploits, and there is no pairing by feature.

### Agarwal2026-AgentAdoptionDiD AI IDEs or Autonomous Agents? Measuring the Impact of Coding Agents on Software Development
- Authors: Shyam Agarwal, Hao He, Bogdan Vasilescu; Year: 2026; Venue: Proceedings of the 23rd International Conference on Mining Software Repositories (MSR '26), pp. 857-862
- URL opened: https://arxiv.org/abs/2601.13597 (arXiv abstract page); Crossref record for DOI 10.1145/3793302.3793589 (venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: Staggered difference-in-differences with matched controls on the AIDev dataset, with adoption defined as the first agent pull request. Velocity gains are large only when the agent is the first AI tool in a project. Static-analysis warnings and cognitive complexity rise by about 18% and 39% in all settings.
- Delta: Same design family as He et al. 2026, for autonomous agents. Quality warnings, not confirmed vulnerabilities; no pairing by feature.

## C. Background

### Klemmer2024-AIAssistantsSecurity Using AI Assistants in Software Development: A Qualitative Study on Security Practices and Concerns
- Authors: Jan H. Klemmer et al. (13 authors, last author Sascha Fahl); Year: 2024; Venue: Proceedings of the 2024 ACM SIGSAC Conference on Computer and Communications Security (CCS), pp. 2726-2740
- URL opened: https://export.arxiv.org/api/query?id_list=2405.06371 (arXiv record with abstract); Crossref record for DOI 10.1145/3658644.3690283 (venue)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 27 interviews with software professionals and 190 Reddit posts and comments. Participants use AI assistants widely for security-critical tasks despite their concerns, and check AI suggestions much as they check human code.

### Majdinasab2024-CopilotReplication Assessing the Security of GitHub Copilot's Generated Code - A Targeted Replication Study
- Authors: Vahid Majdinasab et al. (with Michael Joshua Bishop, Shawn Rasheed, Arghavan Moradidakhel, Amjed Tahir, Foutse Khomh); Year: 2024 (arXiv November 2023); Venue: SANER 2024, DOI 10.1109/SANER60148.2024.00051 [per the Semantic Scholar record; publisher page not opened]
- URL opened: https://arxiv.org/abs/2311.11177 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Replicates Pearce et al. for Python with newer Copilot and CodeQL versions. The share of vulnerable suggestions falls from 36.54% to 27.25%, but Copilot still suggests insecure code.

### Firouzi2024-SOvsChatGPTEncryption Time to Separate from StackOverflow and Match with ChatGPT for Encryption
- Authors: Ehsan Firouzi, Mohammad Ghafari; Year: 2024; Venue: Journal of Systems and Software (accepted June 2024 per the arXiv comment; DOI 10.1016/j.jss.2024.112135 per Semantic Scholar)
- URL opened: https://arxiv.org/abs/2406.06164 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Studies Stack Overflow posts on symmetric encryption with the Java Cryptography Architecture and checks whether ChatGPT helps avoid the same problems. Key and IV generation and padding are common issues; ChatGPT helps when used well but does not replace expertise.

### Sajadi2025-LLMSecurityAwareness Do LLMs Consider Security? An Empirical Study on Responses to Programming Questions
- Authors: Amirali Sajadi et al. (with Binh Le, Anh Nguyen, Kostadin Damevski, Preetha Chatterjee); Year: 2025; Venue: Empirical Software Engineering (accepted per the arXiv comment; DOI 10.1007/s10664-025-10658-6 per Semantic Scholar)
- URL opened: https://arxiv.org/abs/2502.14202 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Claude 3, GPT-4 and Llama 3 answer Stack Overflow questions that contain vulnerable code. They warn about the vulnerability in only 12.6% to 40% of cases, but when they do warn they explain causes, exploits and fixes more than Stack Overflow answers.

### Belozerov2026-SecureCodingAI Secure coding with AI – from detection to repair
- Authors: Vladislav Belozerov, Peter J. Barclay, Ashkan Sami; Year: 2026; Venue: Empirical Software Engineering 31, article 93
- URL opened: https://arxiv.org/abs/2504.20814 (arXiv abstract page); Crossref record for DOI 10.1007/s10664-026-10812-8 (venue and abstract)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: 2,315 C, C++ and C# snippets from the DevGPT dataset of real ChatGPT conversations contain 56 vulnerabilities in 48 files. GPT-4.1, GPT-5 and Claude Opus 4.1 detect 44 to 46 and repair 42 to 44. LLM-generated code is about as likely to contain vulnerabilities as developer-written code.

### Schreiber2025-AICodeGitHub Security Vulnerabilities in AI-Generated Code: A Large-Scale Analysis of Public GitHub Repositories
- Authors: Maximilian Schreiber, Pascal Tippe; Year: 2025; Venue: Lecture Notes in Computer Science vol. 16219, pp. 153-172 (conference name not checked)
- URL opened: https://arxiv.org/abs/2510.26103 (arXiv abstract page); Crossref record for DOI 10.1007/978-981-95-3537-8_9 (venue)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 7,703 files attributed to ChatGPT, Copilot, CodeWhisperer or Tabnine in public repositories, scanned with CodeQL: 4,241 CWE instances of 77 types, while 87.9% of files have no CWE-mapped issue. Python has higher rates than JavaScript and TypeScript.

### Liu2026-DebtAIBoom Debt Behind the AI Boom: A Large-Scale Empirical Study of AI-Generated Code in the Wild
- Authors: Yue Liu et al. (with Ratnadira Widyasari, Yanjie Zhao, Ivana Clairine Irsan, Junkai Chen, David Lo); Year: 2026 (v3 October 2026); Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2603.28592 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 302.6k verified AI-authored commits from 6,299 repositories and five assistants; static analysis before and after each commit attributes 484,366 issues. 7.5% to 14.8% of each assistant's commits introduce at least one issue; 22.7% of tracked issues survive to the latest version. There is no human baseline.

### Farhad2026-LLMVul LLMVul: A Vulnerability-Labeled Dataset of LLM-Generated C/C++ Functions from Real Production Repositories
- Authors: Mohammad Farhad, Shuvalaxmi Dass; Year: 2026; Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2609.10945 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 21,430 C and C++ functions from 226 repositories, identified as LLM-generated from commit metadata; 1,540 labelled vulnerable by an ensemble of static tools, across 17 CWEs (manual check, Cohen's kappa 0.79).

### Siddiq2026-AgenticPRSecurity Security in the Age of AI Teammates: An Empirical Study of Agentic Pull Requests on GitHub
- Authors: Mohammed Latif Siddiq et al. (with Xinye Zhao, Vinicius Carvalho Lopes, Beatrice Casey, Joanna C. S. Santos); Year: 2026; Venue: Information and Software Technology vol. 201, article 108333 (Crossref dates the issue 2027)
- URL opened: https://arxiv.org/abs/2601.00477 (arXiv abstract page); Crossref record for DOI 10.1016/j.infsof.2026.108333 (venue)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 1,293 security-related agent pull requests (about 4%) among 33,000+ curated AIDev pull requests. Agents mostly do security hardening (tests, documentation, configuration, error handling). Security-related agent pull requests are merged less often and reviewed more slowly than other agent pull requests.

### Rabbi2026-SecurityAIPRs Insights into Security-Related AI-Generated Pull Requests
- Authors: Md Fazle Rabbi, Asif K. Turzo, Arifa I. Champa, Minhaz F. Zibran; Year: 2026; Venue: EASE 2026 (per the arXiv comment)
- URL opened: https://arxiv.org/abs/2604.19965 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 675 security-related pull requests by agents among 33,000+ AI pull requests. They introduce a small set of recurring weaknesses (regex inefficiency, injection, path traversal); many flawed ones are still merged.

### Sakib2026-SecurityDebt Trust but Verify? Uncovering the Security Debt of Autonomous Coding Agents
- Authors: A H M Nazmus Sakib, Dipayan Banik, Murtuza Jadliwala; Year: 2026; Venue: KDD 2026 Workshop on Agentic Software Engineering (per the arXiv comment)
- URL opened: https://arxiv.org/abs/2607.12428 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N6
- Summary: 16,112 file changes in 4,022 agent pull requests, checked by a validated LLM judge and manual analysis. 38.9% of pull requests contain at least one security smell, mostly supply-chain issues. Human collaborators introduced 67.6% of the genuine leaked secrets in these agent-assisted workflows, and reviews missed 81.1% of the credentials.

### Almukhtar2026-RefactoringPRs Quality and Security Signals in AI-Generated Python Refactoring Pull Requests
- Authors: Mohamed Almukhtar, Anwar Ghammam, Hua Ming; Year: 2026; Venue: arXiv preprint (Semantic Scholar lists AIware [uncertain])
- URL opened: https://arxiv.org/abs/2605.21453 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Agent refactoring pull requests in Python from AIDev, measured with PyQu, Pylint and Bandit before and after. 4.7% of modified files gain new Bandit findings; 73.5% of pull requests are merged, including some that add findings.

### Hasan2026-SilentPRs The Quiet Contributions: Insights into AI-Generated Silent Pull Requests
- Authors: S M Mahedy Hasan, Md Fazle Rabbi, Minhaz Zibran; Year: 2026; Venue: MSR 2026 Mining Challenge (per the arXiv comment)
- URL opened: https://arxiv.org/abs/2601.21102 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 4,762 AI pull requests with no comments or discussion, from five agents in Python repositories, are examined for complexity, quality issues and security vulnerabilities to explain acceptance or rejection.

### Rooijendijk2026-VulnCommunicationRR How Humans, Bots, and Agents Communicate About Vulnerabilities in Pull Requests
- Authors: Pien Rooijendijk, Christoph Treude, Mairieli Wessel; Year: 2026; Venue: arXiv preprint (registered report)
- URL opened: https://arxiv.org/abs/2606.28125 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: A study plan on the AIDev-pop dataset comparing how humans, bots and coding agents mention vulnerabilities in pull requests, and whether those mentions go with vulnerabilities introduced or fixed in the code.

### Sawada2026-AgentCodeMaintenance To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study
- Authors: Shota Sawada et al. (with Tatsuya Shirai, Yutaro Kashiwa, Ken'ichi Yamaguchi, Hiroshi Iwata, Hajimu Iida); Year: 2026; Venue: EASE 2026 (per the arXiv comment)
- URL opened: https://arxiv.org/abs/2605.06464 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Over 1,000 AI-generated files and about 3,200 changes in 100 repositories. AI files are maintained less often than human code; changes to AI code are mostly feature extensions, while human code gets bug fixes; humans do most of the maintenance.

### Denisov-Blanch2026-RAMP A Few Pages of Markdown: Committed AI Configuration and Lower Quality Cost after Coding-Agent Adoption
- Authors: Yegor Denisov-Blanch et al. (8 authors, with Hao He, Bogdan Vasilescu, Sanmi Koyejo); Year: 2026 (v2 September 2026); Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2608.25241 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Re-estimates an agent-adoption panel of 441 repositories within levels of committed AI configuration. Among agent-first repositories, those without configuration show roughly twice the increase in cognitive complexity (+53% against +27%) and 1.7 times the increase in static-analysis warnings.

### Horikawa2025-AgenticRefactoring Agentic Refactoring: An Empirical Study of AI Coding Agents
- Authors: Kosei Horikawa et al. (with Hao Li, Yutaro Kashiwa, Bram Adams, Hajimu Iida, Ahmed E. Hassan); Year: 2025; Venue: arXiv preprint (submitted to TOSEM per the comment)
- URL opened: https://arxiv.org/abs/2511.04824 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 15,451 agent refactorings in Java projects from AIDev, compared with human refactoring. Agents favour small, local edits such as renaming and type changes over the design-level changes humans make.

### Chatterjee2024-ANZCopilot The Impact of AI Tool on Engineering at ANZ Bank An Empirical Study on GitHub Copilot within Corporate Environment
- Authors: Sayan Chatterjee, Ching Louis Liu, Gareth Rowland, Tim Hogarth; Year: 2024; Venue: 10th International Conference on Software Engineering (SEC 2024), per the arXiv comment
- URL opened: https://export.arxiv.org/api/query?search_query=abs:Copilot+AND+abs:participants+AND+abs:security (arXiv record with abstract, query #57)
- Status: VERIFIED
- Tier: C
- Touches: N1
- Summary: A six-week experiment at ANZ Bank in which engineers were split into control and Copilot groups solving the same Python challenges. Productivity and code quality improved with Copilot; the effect on security was inconclusive.

### Bappy2026-PreventiveToReactive From Preventive to Reactive: How AI Coding Assistants Transform Developers' Security Awareness
- Authors: Faisal Haque Bappy et al. (8 authors); Year: 2026; Venue: Symposium on Usable Privacy and Security (SOUPS 2026), per the arXiv journal reference
- URL opened: https://arxiv.org/abs/2605.23130 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N5
- Summary: Interviews with 15 professional engineers who were also observed doing security-relevant tasks with AI. Security thinking moves from writing code to reviewing it. None of the participants put security requirements in their first prompt, even when they knew them.

### Kharma2026-SecurityTraining A Quasi-Experimental Developer Study of Security Training in LLM-Assisted Web Application Development
- Authors: Mohammed Kharma et al. (6 authors, with David Mohaisen); Year: 2026; Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2604.17763 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 12 developers built a Spring Boot backend with an LLM before and after security training. Validated weaknesses fell from 162 to 111 and critical findings from 24 to 5.

### Do2026-LLMSmartContracts Evaluating the Vulnerability Landscape of LLM-Generated Smart Contracts
- Authors: Hoang Long Do, Nasrin Sohrabi, Muneeb Ul Hassan; Year: 2026; Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2602.04039 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: Solidity contracts generated by ChatGPT, Gemini and Claude Sonnet are checked against known smart-contract vulnerabilities. Despite being syntactically correct and functionally complete, they often have severe exploitable flaws. No human baseline.

### Deng2026-VibeCodedApps Understanding the (In)Security of Vibe-Coded Applications
- Authors: Junquan Deng, Zhiyu Fan, Ruijie Meng; Year: 2026 (v4 September 2026); Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2606.23130 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 9,041 open-source applications built with Claude Code and Lovable; 200 deployed ones were audited and had 1,186 vulnerabilities. 91.0% of audited applications have at least one vulnerability and 65.77% of vulnerabilities are critical or high.

### Androcec2026-TwinPrompt Vibe Coding and Web Application Security: A Twin-Prompt Study
- Authors: Darko Andročec; Year: 2026; Venue: CECIIS 2026 (per the arXiv comment)
- URL opened: https://arxiv.org/abs/2608.20963 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N5
- Summary: Six web applications, each generated once with a baseline prompt and once with an added security-requirements section, by the same agent and model. The security-aware variant had fewer confirmed findings in every application (24 against 51).

### Morkonda2026-LLMCodeSecurity Security of LLM-generated Code: A Comparative Analysis
- Authors: Srivathsan G Morkonda, Mahmoud Selim, Hala Assal; Year: 2026; Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2605.23091 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Code from seven popular LLMs, generated in a way that imitates developer use, contains vulnerabilities, mostly of critical or high severity.

### Bai2026-SilentFailures When Passing Tests Hides Vulnerabilities: An Empirical Study of Silent Failures in Agentic Systems
- Authors: Wenji Bai et al. (with Muhammad Waseem, Zeeshan Rasheed, Jaakko Peltonen, Pekka Abrahamsson); Year: 2026; Venue: arXiv preprint
- URL opened: https://arxiv.org/abs/2609.10548 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3, N4
- Summary: 1,030 traces from seven agent frameworks with GPT-4o-mini repairing code from SecurityEval and CVEfixes. 170 confirmed patches passed tests but kept or added vulnerabilities: 48.2% omitted a needed control, 30.6% introduced a new flaw, 21.2% applied an incomplete defence. Test-passing checks and LLM reviewers did not catch them. (Relevant to the repair slices.)

### Paul2021-CaseControlReviews Why Security Defects Go Unnoticed during Code Reviews? A Case-Control Study of the Chromium OS Project
- Authors: Rajshakhar Paul, Asif Kamal Turzo, Amiangshu Bosu; Year: 2021; Venue: 43rd International Conference on Software Engineering (ICSE 2021), per the arXiv journal reference
- URL opened: https://export.arxiv.org/api/query?search_query=abs:%22case-control%22+AND+abs:code+AND+abs:vulnerabilities (arXiv record with abstract, query #50)
- Status: VERIFIED
- Tier: C
- Touches: N1 (design precedent)
- Summary: A case-control study of Chromium OS: 516 code reviews that caught security defects against 374 where the defects escaped. A logistic model (AUC 0.91) finds nine review attributes linked to catching security defects. A precedent for case-control designs on security outcomes in software engineering; it does not involve AI.

### Yuan2026-SLR Security in LLM-Assisted Coding: A Systematic Literature Review
- Authors: Liang Yuan, Maryam Khanian Najafabadi, Mashud Rana, Varvara Vetrova; Year: 2026; Venue: ACM Computing Surveys (accepted per the arXiv comment)
- URL opened: https://arxiv.org/abs/2610.15482 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: A systematic review of security risks in LLM-assisted coding, benchmark limits, and the human role. It reports data contamination and weak security metrics in current evaluations and argues that human oversight remains necessary.

### Jamil2025-LLMvsHumanQuality Can LLMs Generate Higher Quality Code Than Humans? An Empirical Study
- Authors: M. Jamil, Shamsa Abid, S. Shamail; Year: 2025; Venue: 2025 IEEE/ACM 22nd International Conference on Mining Software Repositories (MSR), DOI 10.1109/MSR66628.2025.00081 [per the Semantic Scholar record]
- URL opened: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/MSR66628.2025.00081 (Semantic Scholar record with abstract); the IEEE Xplore page https://ieeexplore.ieee.org/document/11025576/ returned no content
- Status: UNVERIFIED (only the Semantic Scholar record was readable)
- Tier: C
- Touches: N1
- Summary: Per the Semantic Scholar abstract: 984 samples from GPT-3.5-Turbo and GPT-4 with three prompt types on HumanEval are compared with HumanEval's human-written solutions using Radon, Bandit, Pylint and Complexipy. GPT-4 with advanced prompts comes closest to the ideal and beats the human code on several metrics.

### Patel2024-AIvsHumanMetrics A Comparative Analysis between AI Generated Code and Human Written Code: A Preliminary Study
- Authors: Abhi Patel, Kazi Zakia Sultana, B. Samanthula; Year: 2024; Venue: 2024 IEEE International Conference on Big Data, DOI 10.1109/BigData62323.2024.10825958 [per the Semantic Scholar record]
- URL opened: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/BigData62323.2024.10825958 (Semantic Scholar record with abstract)
- Status: UNVERIFIED (only the Semantic Scholar record was readable)
- Tier: C
- Touches: N1
- Summary: Per the Semantic Scholar abstract: relates software metrics to bugs reported by static analysers in AI-generated and human-written code.

## How the designs handle tasks that were chosen because the human erred

The orchestrator asked which studies use a matched or paired design, a case-control design, or a control group of human-correct code, and how each one deals with the fact that its tasks were chosen because the human made a mistake.

Studies whose tasks were all chosen because the human wrote a bug or vulnerability:
- Asare2023-CopilotVsHumans: does not discuss it. The human's failure rate is 100% by construction, there is no human-correct set, and the conclusion "not as bad as humans" rests on the conditional rate (33% repeated the vulnerability).
- Jesse2023-SStuBs: does not discuss it. It reports how often the model avoids the human's bug (13.41%) and the bug-to-fix ratio, with no correct statements as a contrast.
- Guo2025-BugReplicators: the only one in this group with a contrast set. It compares bug-prone locations with ordinary completion tasks (GPT-4: 12.27% correct against 29.85%). How the ordinary tasks were chosen is [uncertain] from the abstract.
- Chen2026-SecureVibeBench: says the aim is a fair comparison with humans, but all tasks are human-vulnerable. Its only human comparison is a Semgrep setting that counts only findings not present after the human's own commit (4.9% falls to 2.6%). No human-correct tasks.
- Zhao2026-SusVibes and Shen2025-SecRepoBench: framed as benchmarks; they do not compare with the human and have no human-correct tasks.
- Wu2026-LastSecureCode and Melo2026-PreferVulnerable: built from real vulnerabilities or vulnerability-patch pairs; the abstracts do not mention a control.

Paired designs where tasks were not chosen for a human mistake (so the comparison is unconditional): Cotroneo2025-HumanVsAI and Improta2026-CQBench (pairs by docstring; Improta adds a size control), Licorish2025-JuryOut (same 72 prompts), Lee2026-SecuritySensitiveFunctions and Hamer2024-ChatGPTvsSO (same Stack Overflow questions), Rashidi2026-Provenance (same 31 tasks), Mahmud2026-IllusionOfSafety (same 851 tasks, with task clustering and controls for length and pass rate), Sajadi2025-PatchSecurity and Chen2025-AgentPatchQuality (same issues, developer patch against model patch), Coppola2026-AgentDebtRR (planned, same issues). Egli2026-HowToCompare discusses the opposite selection problem: picking top-ranked human solutions gives humans a ceiling advantage.

Matched controls in mining studies: He2026-CursorDiD and Agarwal2026-AgentAdoptionDiD (difference-in-differences with matched non-adopting projects), Denisov-Blanch2026-RAMP (re-estimation within strata), Kraishan2026-FiveAgents (human pull requests from the same repositories and time window), Xia2026-PostMergeFate (statistical adjustment for file role and repository), Shaw2026-ComparedToWhat (human baseline matched by size, not by task).

Case-control designs: Paul2021-CaseControlReviews is a case-control study of security defects in code review, without AI. No case-control study of AI-generated code was found.

Control group of code the human wrote correctly, from the same commit, judged the same way as the treatment group: none found in this slice. The nearest pieces are Guo2025-BugReplicators (ordinary completion tasks as a contrast) and the relative Semgrep setting in Chen2026-SecureVibeBench.

## Search limitations and coverage

- DBLP returned a bot-check page for every request, so no DBLP results were used (query #10).
- OpenAlex's keyless daily budget for this machine ran out after five searches (query #9); the limit is shared with other agents on the same address.
- Semantic Scholar keyword search succeeded once in six attempts (HTTP 429 otherwise); the citations endpoint worked and was used for all snowballing.
- The arXiv API was throttled at times; three queries were rerun (#48 to #50) and the failed first attempts are not counted.
- IEEE Xplore pages rendered empty, and Springer redirected to a login page, so venue details for published papers come from Crossref records. Three papers known only from Semantic Scholar records are marked UNVERIFIED.
- Read in full: Asare2023-CopilotVsHumans. Read in large part: Chen2026-SecureVibeBench, Zhao2026-SusVibes, Jesse2023-SStuBs, Egli2026-HowToCompare. Targeted sections read: Shen2025-SecRepoBench, Ullah2025-CVEGenie, Cotroneo2025-HumanVsAI, Kraishan2026-FiveAgents, Xia2026-PostMergeFate, Sajadi2025-PatchSecurity, Perry2023-InsecureCode, Karanjai2023-SmartContractCreation, Lee2026-SecuritySensitiveFunctions. All others: abstract only.
- Several entries overlap with other slices: Zhao2026-SusVibes, Chen2026-SecureVibeBench, Shen2025-SecRepoBench and Asare2023-CopilotVsHumans also appear in the repository agent benchmark slice (`r1_L2_repo_agent_benchmarks.md`), with the same short IDs and the same tier.

DISTRIBUTIONAL_SKEW_ADVISORY:
- Dimension: time distribution
- Concentration: 2025-2026 = 54/69 (78%)
- Advisory: This is a coverage-distribution signal, not a defect. Consider whether the RQ warrants broader periods, sites, methods, or venue families.
- Search response: no expansion; the task asks to prioritise 2022-2026, and work on agents and agent pull requests only exists from 2025.

No skew advisory for venue type: arXiv-only papers without a stated acceptance are 28 of 69 (41%).

## Leads not followed

- "GitHub Copilot and Code Security: An Empirical Evaluation in the Context of Developers' Professional Experience" (HCII 2026, per Semantic Scholar) - seen in the citations of Perry et al. 2023 and Asare et al. 2024; no page found (query #45).
- "Insecure by design? A human-centric security perspective on AI-assisted software development" (Computers & Security 2026, per Semantic Scholar) - citations of Perry et al. 2023.
- "Google it or ask ChatGPT? Impact of software developers' information search practices on organisational information security" (Behaviour & Information Technology 2026) - citations of Perry et al. 2023.
- "Can Developers Rely on LLMs for Secure IaC Development?" (arXiv 2602.03648), "An Empirical Study of Security Calibration in Large Language Models for Code" (arXiv 2606.31159), "GitHub's Copilot Code Review: Can AI Spot Security Flaws Before You Commit?" (arXiv 2509.13650) - citations of Perry et al. 2023.
- "Software Aging in LLM-Generated Applications: Runtime Evidence, Static Analysis, and Human-Written Comparisons" (arXiv 2608.26391) - arXiv query #14.
- "Who Said CVE? How Vulnerability Identifiers Are Mentioned by Humans, Bots, and Agents in Pull Requests" (MSR 2026; arXiv 2601.19636) - OpenAlex query #5 and arXiv query #15.
- "Safer Builders, Risky Maintainers: A Comparative Study of Breaking Changes in Human vs Agentic PRs" (arXiv 2603.27524) - arXiv queries #15 and #59; about breaking changes, not security.
- "Beyond Bug Fixes: An Empirical Investigation of Post-Merge Code Quality Issues in Agent-Generated Pull Requests" (MSR 2026, DOI 10.1145/3793302.3793615) - WebSearch query #28.
- "Let's Make Every Pull Request Meaningful: An Empirical Analysis of Developer and Agentic Pull Requests" (arXiv 2601.18749), "Code Change Characteristics and Description Alignment: A Comparative Study of Agentic versus Human Pull Requests" (arXiv 2601.17627), "Mining Architectural Quality Under Agentic AI Adoption: A Causal Study of Java Repositories" (arXiv 2606.13298), "Evaluating Human- and AI-Generated Code Quality Based on Code Smell" (2026), "Who Wrote This Code? Investigating Human and AI Programming Patterns" (2025) - citations of Cotroneo et al. 2025.
- "Quality of AI-Generated vs. Human-Generated Code" (ICCTA 2024, DOI 10.1109/iccta64612.2024.10974782) - Crossref title search; no abstract available.
- "Comparing Software Developers with ChatGPT: An Empirical Investigation" (arXiv 2305.11837) - Semantic Scholar query #11.
- "How secure is AI-generated code: a large-scale comparison of large language models" (Empirical Software Engineering 2024, DOI 10.1007/s10664-024-10590-1), "DeVAIC: A tool for security assessment of AI-generated code" (Information and Software Technology 2024), "Security Vulnerability Patterns in AI-Generated Code: A Cross-Model Comparative Study" (arXiv 2607.20713) - OpenAlex query #4; they compare models with each other, not with humans.
- "RealSec-bench: A Benchmark for Evaluating Secure Code Generation in Real-World Repositories" (Findings of ACL 2026) and the benchmarks in SecureVibeBench's comparison table (CodeLMSec, LLMSecEval, SecCodePLT, CWEval, BaxBench, CyberSecEval, SafeGenBench, SecCodeBench, A.S.E.) - query #46; these belong to the benchmark slice.
- "Vulnerability Assessment of LLM-Generated Smart Contracts in Ethereum" (CEUR-WS Vol-4075, paper 1) and "SolBehave: Evaluating the Behavioural Correctness of LLM-Generated Smart Contracts" (arXiv 2610.18745) - WebSearch query #53; Solidity generation without a human comparison.
- "LLM Code Reviewers Are Harder to Fool Than You Think: Adversarial Comments Fail Where Vulnerability Patterns Succeed" (arXiv 2602.16741) - WebSearch query #54; a summary says unpaired comparisons showed an effect that disappeared when the comparisons were paired, which is a useful method point.
- "Repairing vulnerabilities without invisible hands. A differentiated replication study on LLMs" (arXiv 2507.20977), "PatchBench: Evaluating AI Agents for Vulnerability Patching" (arXiv 2609.04075), "Vul4Py: Benchmarking Automated Vulnerability Repair in Python with Paired Exploit and Functional Oracles" (arXiv 2608.00692), "SEC-bench" (arXiv 2506.11791), "Where Did the Repair First Go Wrong? Localizing the Origins of Silent Failures in Agentic Vulnerability Repair" (arXiv 2610.06163) - queries #55, #35, #60 and the Asare and SusVibes citation lists; these belong to the repair slices (N3, N4).
- "Applying Security by Design at the Point of Execution: How Governed Security Requirements Affect the Security of AI-Generated Code" (arXiv 2610.10659) - citations of SecureVibeBench; may bear on N5 (how requirements are worded).
- A Cloud Security Alliance research note on CVEs attributed to AI-generated code, and news reports of a Georgia Tech tracker of such CVEs - WebSearch queries #29 and #31; grey literature, not opened.
- A CodeRabbit vendor report comparing AI-generated and human pull requests (470 pull requests, about 1.7 times more issues for AI) - WebSearch query #31; not opened.
- Owura Asare's PhD thesis "Security Evaluations of GitHub's Copilot" (University of Waterloo, UWSpace) - WebSearch query #45; it reportedly includes a second user study with 21 participants.
- "Bugs in large language models generated code: an empirical study" (Empirical Software Engineering 2025), "Security and Quality in LLM-Generated Code: A Multi-Language, Multi-Model Analysis" (TDSC 2026; arXiv 2502.01853), "Self-Admitted GenAI Usage in Open-Source Software" (TSE 2026; arXiv 2507.10422), "Developers and generative AI: A study of self-admitted usage in open source projects" (Empirical Software Engineering 2026; arXiv 2603.26277), "Unveiling ChatGPT's Usage in Open Source Projects: A Mining-based Study" (MSR 2024) - citations of Asare et al. 2023; the self-admitted usage studies could supply human and AI labels for commits.
- "On Developers' Self-Declaration of AI-Generated Code: An Analysis of Practices" (arXiv 2504.16485) - arXiv query #14.
- "The Rise of AI Teammates in Software Engineering (SE) 3.0: How Autonomous Coding Agents Are Reshaping Software Engineering" (arXiv 2507.15003) - WebSearch query #54; the paper behind the AIDev dataset used by most agent pull-request studies above.
