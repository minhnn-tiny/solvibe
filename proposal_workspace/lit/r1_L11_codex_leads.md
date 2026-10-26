## Queries run

Slice L11: verifying and extending the leads left by the other search engine. Searches ran on 2026-10-21, following the search protocol (`proposal_workspace/lit/search_protocol.md`) and the project brief (`proposal_workspace/lit/project_brief.md`).

A note on the indexes. During this session the Semantic Scholar API returned HTTP 429 on every call, the OpenAlex API said the free daily budget for this IP was used up, DBLP returned a bot check page, and the arXiv export API returned HTTP 429. So every paper below was checked on its own arXiv abstract page, its arXiv full text (HTML or PDF), or a publisher or conference page. The arXiv web search page (`arxiv.org/search`) still worked and replaced the arXiv API for searching.

| Query | Source | Hits looked at | New relevant papers |
|---|---|---|---|
| PoCo proof-of-concept exploit generation smart contracts Proof-of-Patch dataset Solodit | WebSearch | 9 | 1 (PoCo) |
| `all:PoCo AND all:smart AND all:contract` | arXiv API | 0 (empty reply, then HTTP 429) | 0 |
| "Patch Validation" automated vulnerability repair PVBench developer tests PoC | WebSearch | 9 | 2 (PVBench, PatchBench) |
| 4 queries on overfitting, hidden tests, held-out tests, reward hacking | arXiv API | 0 (HTTP 429 on all) | 0 |
| LLM agent vulnerability repair overfitting visible test hidden tests 2026 arXiv | WebSearch | 9 | 4 (test overfitting on SWE-bench, invisible hands, fine-tuned AVR, CVE-Bench blog) |
| coding agents visible versus hidden security tests code generation 2026 | WebSearch | 9 | 2 (SecTDD, Last Secure Code Benchmark) |
| test overfitting coding agents SWE-bench patches pass visible tests fail hidden tests study | WebSearch | 9 | 5 (Beyond Pass@k, SWE-Gate, silent failures, SWE-ABS, solved issues) |
| reward hacking unit tests coding agents modify tests special-case benchmark ImpossibleBench | WebSearch | 9 | 2 (ImpossibleBench, EvilGenie) |
| CVE-Bench agents fix real CVEs hidden security test maintainer fix ... untouched code path | WebSearch + 2 WebFetch | 9 | 0 new (CVE-Bench blog page opened) |
| LLM code repair existing tests encode buggy behavior agent keeps regression tests passing incorrect tests as specification | WebSearch | 9 | 2 (validation evidence, hallucination in APR) |
| impact of incorrect or misleading test cases on LLM code generation repair follows wrong tests 2025 | WebSearch | 9 | 0 |
| held-out exploit tests vulnerability repair LLM agent patch passes provided PoC fails other exploit variants | WebSearch | 9 | 4 (Vul4Py, LLM-in-the-loop, VulnRepairEval, Why LLMs Fail) |
| "Last Secure Code Benchmark" agents hidden functional security tests | WebSearch | 9 | 0 (no arXiv page in results) |
| "Are Solved Issues in SWE-bench Really Solved Correctly" PatchDiff | WebSearch | 9 | 0 (venue check) |
| arxiv October 2026 secure code benchmark vibe coding 450 tasks 150 vulnerabilities | WebSearch | 9 | 0 |
| Fengji Zhang secure code | arXiv web search | 1 | 1 (Last Secure Code Benchmark, arXiv 2610.14766) |
| test overfitting LLM program repair | arXiv web search | 8 | 0 |
| hidden tests vulnerability repair agent | arXiv web search | 1 | 0 |
| visible tests hidden tests security code generation | arXiv web search | 3 | 2 (Ghost Tests human study, spec-driven security benchmark) |
| overfitting tests coding agents | arXiv web search | 23 | 2 (Agent-CoEvo, DryRUN) |
| held-out tests repair LLM | arXiv web search | 22 | 0 |
| incorrect tests LLM code generation | arXiv web search | 50 of 120 | 4 (fault-enforcing tests, misguidance effect, CoHarden, TRACE) |
| misleading test cases LLM | arXiv web search | 27 | 0 |
| tests conflict specification LLM agents | arXiv web search | 19 | 0 |
| reward hacking coding agents tests | arXiv web search | 33 | 3 (SpecGuard, escalation channels, SpecBench) |
| incomplete patch vulnerability LLM | arXiv web search | 7 | 0 |
| proof of vulnerability repair LLM agent | arXiv web search | 4 | 0 |
| PoCo / PVBench venue checks ("accepted", "conference") | WebSearch x2 | 18 | 0 (both still preprints) |
| Can Old Tests do New Tricks (snowball from the test overfitting paper) | arXiv web search | 2 | 1 (TestPrune) |
| automated fixes truly mitigate smart contract exploits (snowball from PoCo) | arXiv web search | 1 | 1 (Bobadilla et al.) |
| Bobadilla Monperrus smart contract repair | arXiv web search | 1 | 0 |
| hidden security tests | arXiv web search | 50 of 144 | 1 (SecureVibe) |
| security tests repair overfitting; vulnerability repair agents tests overfit; PoC overfitting patch | arXiv web search | 0 | 0 |
| regression tests encode bug; tests encode buggy behavior; agent existing tests buggy behavior repair | arXiv web search | 6 | 0 |
| smart contract repair LLM exploit | arXiv web search | 2 | 1 (SmartPoC) |
| empirical study security patches modify existing tests that assert vulnerable behavior | WebSearch + 1 WebFetch | 9 | 1 (patching benchmark reliability study, arXiv 2610.10150, found through a blog post) |
| LLM agent repair keeps existing failing tests ... backward compatibility ... agents follow tests | WebSearch | 9 | 0 |
| 1Password 6,080 AI-generated patches; Off-by-1 Labs FLAWED | WebSearch x2 | 19 | 0 verified (news coverage only) |
| Title and DOI lookups for 6 papers | Semantic Scholar API, OpenAlex API, DBLP API | 0 (429, budget used up, bot check) | 0 |
| ImpossibleBench venue | WebFetch of the ICLR 2026 poster page | 1 | 0 (venue confirmed) |

Snowballing done by hand: the reference lists of PoCo, PVBench, PatchBench, the test overfitting paper and SpecGuard. This gave Bobadilla et al. (TSE 2025), SmartPoC, TestPrune, and the leads listed at the end.

## Lead 1: PoCo

### Andersson2025-PoCo PoCo: Agentic Proof-of-Concept Exploit Generation for Smart Contracts
- Authors: Vivi Andersson, Sofia Bobadilla, Harald Hobbelhagen, Martin Monperrus (KTH); Year: 2025 (v1 4 Nov 2025, v3 23 Feb 2026); Venue: arXiv preprint (arXiv 2511.02780). The arXiv comment field says "Under review". No published version was found.
- URL opened: https://arxiv.org/abs/2511.02780 (arXiv abstract page) and https://arxiv.org/html/2511.02780v3 (full text, read in full)
- Status: VERIFIED
- Tier: A
- Touches: N2, N6 (N3 and N4 only in passing)
- Summary: PoCo is a single LLM agent, built on the Claude Code SDK with Foundry compile and test tools served over MCP inside Docker. It takes a vulnerable project and an auditor's written finding and writes a Foundry exploit test. It was run once per case with Claude Sonnet 4.5, OpenAI o3 and GLM 4.6, against a zero-shot baseline and a fixed two-step workflow baseline. On 23 findings, PoCo produced 50 well-formed exploits out of 69 runs (compiles, and every assertion passes on the vulnerable code), against 22 for the workflow baseline and 4 for zero-shot. 32 PoCo exploits were judged correct because at least one assertion failed on the developer's patched code (Table 3 gives o3 14, Sonnet 11, GLM 7; the text also says "68% (13/19)" for o3, so the paper is not consistent there [uncertain]). Six more were inconclusive because the patch changed a function signature, and the authors checked them by hand. With more detail in the written finding, correct exploits rose from 1 to 3 to 5 on 9 findings.
- How the dataset is built (Proof-of-Patch): the authors queried Solodit for the ten OWASP Smart Contract Top 10 categories and got 3,814 findings. An LLM judge ranked them by whether they had a patch, a proof of concept and a fix description. The top 100 were checked by hand: the project must be public and runnable with Foundry within one hour of setup, the contest judges must have accepted the finding, and a valid patch must exist, usually a linked pull request. 23 findings remained (15 Medium, 8 High, 13 with an auditor's coded proof of concept), from 15 audit contests between 2022 and July 2025, such as 2023-04-caviar and 2024-03-axis-finance. The finding text becomes the input. A coded proof of concept in the report is kept for reference but removed from the input.
- How exploits are validated: two checks. First, on the vulnerable code the test must compile and all assertions must pass. Second, on the developer's patched code at least one assertion must fail. The authors call the developer patch "an oracle for PoC validity" and claim to be the first to validate exploits this way. They discuss two risks: a patch that is incomplete (a correct exploit still passes on it) and a patch that blocks the exploit for a reason unrelated to the bug.
- Delta: N2. PoCo works on the same kind of material as the project: accepted audit-contest findings from Solodit, mostly logic, rounding and access-control bugs in DeFi code, turned into Foundry exploit tests. So the project cannot claim to be the first to build executable Foundry exploits from audit-contest findings. What PoCo does not do: it does not trace findings to the commit that introduced the bug, it does not remove the vulnerable function to create a feature task, and it does not estimate who loses how much. Its assertions check that a rule is broken, for example that a flash-loan fee is 25 wei instead of 0.0025 ETH. Some assert that a victim lost funds, but no amount is estimated or compared. Its findings run to July 2025, and 12 of its 23 had public exploits, so its models may have seen them. The project picks findings published after the models' training data ends.
- Delta: patched code as a negative check. Yes. This is the core of PoCo's RQ2, and it is the same check the project uses for every PoV: the exploit passes on the human's vulnerable code and fails on the human's fix. The project should cite PoCo for this check and not present it as new. The project goes further in one way: it also uses a second PoV that still passes on a shallow repair (P3 after the hand-written underflow fix), which is exactly PoCo's "incomplete patch" risk turned into an evaluation tool.
- Delta: do agents write features or repairs? No. PoCo's agent is told to write only the test file and never to change the contracts. There is no feature writing, no repair, no comparison with the human developer (N1), no shown or held-out PoVs for judging a repair (N3), and no repair input study (N4). PoCo's RQ3 varies how much the written finding says (high level, detailed, step by step), which resembles N4's "what the agent is told" arms, but for writing exploits, not for repairing code.
- Delta: N6. The project confirms each flaw that an LLM reviewer reports by writing a new PoV that passes on the agent's version and fails on the human's version. That is PoCo's method with the human's version in the role of the patch. PoCo applies it to auditor-written findings on human code only. It does not run an LLM security review, and it does not compare reviews of agent code and human code.

## Lead 2: PVBench

### Yu2026-PVBench Patch Validation in Automated Vulnerability Repair
- Authors: Zheng Yu, Wenxuan Shi, Xinqian Sun, Zheyun Feng, Meng Xu, Xinyu Xing (Northwestern, Waterloo, New Hampshire); Year: 2026 (v1 6 Mar 2026, v2 20 Mar 2026); Venue: arXiv preprint (arXiv 2603.06858). No published version found; the venue field in the HTML is empty.
- URL opened: https://arxiv.org/abs/2603.06858 (arXiv abstract page) and https://arxiv.org/html/2603.06858 (v2 full text, read in full)
- Status: VERIFIED
- Tier: A
- Touches: N3, N4
- Summary: PVBench has 209 C/C++ vulnerabilities from 20 projects (PHP 43, CPython 33, LLVM 26, V8 24, and others), mostly memory-safety bugs across 12 CWEs. Each case has a PoC, the functional tests that existed before the fix, and the new tests the developers added with the fix, which the paper calls PoC+ tests. Three repair tools (PatchAgent, San2Patch, and SWE-agent's multi-language version) were run with GPT-4.1 and Claude Sonnet 4, five times per case. Overall, 47.1% of attempts passed the basic checks (the PoC no longer crashes and the old tests pass), but only 27.1% also passed the PoC+ tests. So 42.3% of the patches judged correct by the basic checks were wrong (1,250 of 2,952). The per-configuration rate ranged from 32.3% to 49.8%. Of the patches that passed PoC+ tests, 74.4% matched the developer's patch in meaning and 10.1% got around a check instead of fixing the cause. The patches that failed PoC+ broke documented behaviour (54.4% in Table 6), fixed the wrong function (41.2%), or used poor code (4.4%).
- Lead check: the lead's claim is right in substance. The exact wording is "over 40% of patches validated as correct by basic tests fail under PoC+ testing", where the basic tests are the PoC plus the existing functional tests.
- Delta: N3. PVBench shows the core idea behind N3 on C/C++: the PoC that the repair tool sees is not enough to judge the repair, and a check the tool never saw rejects many patches that pass it. The difference is what the hidden check is. In PVBench it is the developer's own new test from the fix commit, which checks the intended output after the fix. In the project it is a set of other exploits for the same finding (P1, P3 and the added P4 and P5), written from the audit report, plus the fix commit's rewritten tests. The project's hidden exploits measure stolen funds, and one of them caught a repair that blocked the shown PoV but still let an attacker take 48.88 ETH. PVBench has no smart contracts, no business-logic bugs and no loss measure. The project should cite PVBench for using tests from the fix commit as a stronger oracle, because the project does the same with the downward iterator tests from commits `0d6d39e` and `c01b6c7`.
- Delta: N4. PVBench does not change what the tool is told or what it can run; each tool runs as published. It also selects only cases where the fix leaves the functionality unchanged, so that the old tests stay valid after the fix. That rule excludes, by design, the case the project found: the repository's own tests assert the vulnerable behaviour, so a correct repair must break them. PVBench's most common failure (the patch fixes the crash but breaks documented behaviour) is the opposite of the project's observed failure (the agent keeps the buggy behaviour because the old tests demand it).

## Lead 3: papers on overfitting the visible test and on visible versus hidden security tests

The other engine did not give titles. I cannot know which two papers it meant. The closest match for (a) is Ahmed2026-TestOverfitting, and the closest match for (b) is Liang2026-SecTDD. Two more 2026 papers match the leads at least as well and are closer to the project: Shen2026-PatchBench and Le2026-PatchingBenchReliability.

### Shen2026-PatchBench PatchBench: Evaluating AI Agents for Vulnerability Patching
- Authors: Chihao Shen, Jiacheng Li, Aastha Mahajan, Jeffery Siyuan Tian, Yonghwi Kwon, Yizheng Chen (University of Maryland); Year: 2026 (3 Sep 2026); Venue: arXiv preprint (arXiv 2609.04075)
- URL opened: https://arxiv.org/abs/2609.04075 (arXiv abstract page) and https://arxiv.org/html/2609.04075 (full text, main body read)
- Status: VERIFIED
- Tier: A
- Touches: N3, N4
- Summary: First, on SEC-bench (300 C/C++ tasks), Codex with GPT-5.6 Sol passed 97.3% of tasks, about 25% of agent patches were near copies of the historical developer patch, and 81% of Codex patches changed a function on the crash stack, even when the real fix lay elsewhere. PatchBench then keeps 213 ARVO vulnerabilities from 32 projects whose developer fix lies off the crash stack, moves each bug into a newer version of its project, rewrites the code around the fix, and writes a reference patch by hand. The agent gets the repository, the sanitizer report, the PoC and commands to build and to run the PoC. The repair is judged on many crashing inputs that the agent never sees: variants of the PoC found by fuzzing seeded with the PoC and by plain fuzzing (median 33 plus 4 per bug). It is also judged on benign inputs, the program's output compared with the reference-patched program, and the unit tests that pass on the reference-patched program. Across 11 agents (Codex, Claude Code, OpenHands with six models, and the top three AIxCC systems), 83.1% of patches stopped the original PoC but only 45.3% of tasks were solved, a 1.83 times overstatement. The best agent passed 97.2% of PoCs and solved 59.2%. The most common failure was a local check at the crash site that blocks the shown PoC while other crashing inputs reach the same bug by another path (41 of 81 such Codex failures).
- Delta: N3. This is the closest precedent for N3. The agent sees one PoC and can run it, and a set of other exploit inputs it never saw judges the repair. The main failure it reports, a fix that blocks the shown PoC but not its variants, is the project's finding that agents fitted the shown PoV. What PatchBench does not do: it works on C/C++ memory-safety crashes, not Solidity business-logic bugs. Its hidden inputs are fuzzed variants near the same crash path, not separate attacks written from an audit report. Success means no sanitizer error, not money kept safe, and it has no loss estimate. So the project's claim for N3 must be narrowed to smart contracts, hidden exploits written from audit reports, and losses in funds.
- Delta: N4. PatchBench gives every agent the same input (sanitizer report, PoC, run command) and a full terminal. It does not compare a report with a PoV, location only, or limits on what the agent can run. It uses the unit tests of the reference-patched program as the oracle and notes that the fixed program may behave differently from the vulnerable one, but it does not study agents that keep old tests passing when those tests assert the vulnerable behaviour.

### Le2026-PatchingBenchReliability On the Reliability of LLM-Based Vulnerability Patching Benchmarks
- Authors: Dang K Le, Wenxuan Shi, Xinyu Xing (Northwestern); Year: 2026 (7 Oct 2026); Venue: arXiv preprint (arXiv 2610.10150)
- URL opened: https://arxiv.org/abs/2610.10150 (arXiv abstract page) and https://arxiv.org/html/2610.10150 (full text; introduction, taxonomy, dataset, experiments 1 to 3 and threats read). Found through a blog post (remio.ai) that reported its numbers.
- Status: VERIFIED
- Tier: A
- Touches: N3, N4
- Summary: The authors list mistakes in patching benchmarks at three levels: the agent (build and test instructions, web access), the harness (permissions, timeouts, agent-written tests that collide with the oracle), and the dataset (PoC-only oracle, PoC format, git history left in the workspace). They built 112 bugs from 84 projects (25 C/C++, 62 Go, 25 Rust), each with a PoC, the regression tests, and the developer's tests from the upstream fix commit, which the agent never sees. With OpenCode and Claude Sonnet 4.0, one run per condition: telling the agent how to build and test raised PoC passing from 74.1% to 77.7% (C/C++ from 72% to 92%) but developer-test passing only from 41.1% to 43.8%. Showing a Go source-level PoC raised PoC passing from 69.4% to 95.2% and developer-test passing from 41.9% to 48.4%. Showing a binary C/C++ PoC changed nothing. Across Sonnet 4.0, Sonnet 4.5 and Opus 4.7, PoC passing rose from 77.7% to 90.2% and developer-test passing from 43.8% to 60.7%. 32.7% of Opus 4.7's PoC-passing patches still failed the developer's test. The old regression suite passed 94.6% to 97.3% of the time and hardly separated good fixes from fixes that only hide the crash.
- Delta: N4. This is the closest precedent for the repair input study. It changes two of the project's inputs: whether the PoC is shown (no PoC against PoC) and how well the agent is equipped to build and test its own changes. It judges with a test the agent never saw. It finds the same pattern as the project's pilot: more help with the shown check raises success on that check much more than on the hidden one. Differences: the agent always has a terminal (the paper changes the instructions, not the tools), while the project removes the terminal or limits it to the shown test. There is no written-report arm separate from the PoC, because the bug description is always given. There is one run per condition with one model, against 12 runs per arm with three agents in the project. It has no Solidity and no hidden exploits. It does not report what the project found with OpenHands, where a full terminal lowered success from 10 of 12 to 2 of 12.
- Delta: N3. The hidden check is the developer's test from the fix commit, as in PVBench, not other exploits. It does not measure losses. Its finding that regression suites barely separate good and bad fixes supports the project's observation that the repository's tests did not catch the shallow repair, but it does not study tests that assert the vulnerable behaviour.

### Liang2026-SecTDD Security Tests as Executable Specifications for LLM Code Generation: Benefits, Trade-offs, and Coverage Limits
- Authors: Yunhao Liang, Chengguang Gan, Ruixuan Ying, Hanjun Wei, Zhe Cui, Shiwen Ni; Year: 2026 (v1 10 Aug 2026, v2 11 Aug 2026); Venue: arXiv preprint (arXiv 2608.09740). The ACM template in the HTML names FSE 2027, but no acceptance is stated [uncertain].
- URL opened: https://arxiv.org/abs/2608.09740 (arXiv abstract page) and https://arxiv.org/html/2608.09740 (full text, read in full)
- Status: VERIFIED
- Tier: A
- Touches: N3, N4
- Summary: SecTDD separates three choices: whether tests are shown before generation, whether a failed test run leads to a revision (at most two), and how failures are reported (all raw logs, one random failure, or security failures first). Each task's functional and security tests are split into a visible part and a hidden part by behaviour family or attack method. The hidden part runs once, after the final answer. Revisions start from the same first answer, so a repair effect can be told apart from a prompt effect. The study covers 2,705 runs on 31 Python tasks from CWEval, SALLM and CodeGuard+, 16 CWEs, four Qwen models and DeepSeek-V4-Flash, five repetitions each. Showing all visible tests up front raised hidden functional-and-security success by 19.3 points on average, but helped in 7 of 9 model and benchmark pairs and hurt in 2. Feedback repaired 80 failed first answers with no regression (raw logs: 83 repairs, 3 regressions). Between 5.6% and 18.8% of answers that passed every visible test failed the hidden tests, and feedback cannot fix a hidden property that no visible test exposes.
- Delta: N4. The design has the same shape as the repair input study: one factor is what the model is shown (the tests up front or not), another is whether it can run tests and see failures, and the judge is a hidden security test set. It also shows that showing more tests can make the hidden outcome worse in some cells. Differences: it is code generation of small Python functions from benchmark prompts, not repair of a vulnerable function inside a real repository. The models are plain LLMs in a fixed loop, not coding agents with a terminal. There are no repository tests, no written report and no location-only arm.
- Delta: N3. Its visible and hidden split is the same idea as the shown and held-out PoVs, and its measure of answers that pass every visible test but fail the hidden ones is the measure the project needs. But the hidden tests are other inputs of the same CWE pattern, not separate exploit paths, and nothing is measured in funds. It is not about smart contracts.

### Ahmed2026-TestOverfitting Investigating Test Overfitting on SWE-bench
- Authors: Toufique Ahmed, Jatin Ganhotra, Avraham Shinnar, Martin Hirzel (IBM); Year: 2026; Venue: FSE Companion '26 (Montreal), DOI 10.1145/3803437.3805574, as given on the first page of the arXiv PDF; arXiv 2511.16858 (v1 20 Nov 2025, v3 3 Apr 2026)
- URL opened: https://arxiv.org/abs/2511.16858 (arXiv abstract page) and https://arxiv.org/pdf/2511.16858v3 (PDF, read in full; the arXiv HTML was cut short)
- Status: VERIFIED
- Tier: A
- Touches: N3, N4
- Summary: On TDD-Bench Verified (449 SWE-bench Verified issues), the authors took Agentless patches and e-Otter++ generated reproduction tests, then ran a refinement loop of up to 15 rounds that edits the code or the test. A patch overfits when it passes the generated test but fails the hidden developer tests or the old regression tests. Without refinement, 21.8% (Claude 3.7 Sonnet, 50 of 229) and 33.0% (GPT-4o) of patches that passed the generated test overfitted. Refinement made 22 more patches pass the generated test, but 14 of them failed the hidden tests, so overfitting rose to 25.5% and 35.9%. Hiding the generated test and returning only pass or fail lowered agreement with the test, but overfitting stayed high. Even refining against the real hidden tests only raised resolved issues from 229 to 243, and 5.8% to 11.3% of those patches broke old regression tests. The models nearly always changed the code, not the test, which the authors read as the models trusting the tests.
- Delta: N4. It shows in general Python issue fixing what the project saw in security repair: code refined against the visible test passes it and fails the hidden one. It also changes how much of the test the model sees. Differences: the visible test is an LLM-generated reproduction test, not a real exploit; the loop is a fixed pipeline, not an agent with a terminal; there is no written-report arm and no security setting. It notes that the old regression tests "only test existing behavior" and that systems do not know which old tests should still pass after the fix, but it does not study old tests that assert the bug.
- Delta: N3. Its hidden developer tests play the role of the held-out PoVs, but they are functional tests of the issue, not exploits.

### Xu2026-ValidationEvidence Validation Evidence in LLM Repair Agents: How Much of What Passes Actually Tests the Bug?
- Authors: Xiaonan Xu, Wenjing Wu; Year: 2026 (30 Jul 2026); Venue: arXiv preprint (arXiv 2607.28871)
- URL opened: https://arxiv.org/abs/2607.28871 (arXiv abstract page) and https://arxiv.org/html/2607.28871 (full text; introduction, method, design and RQ1 results read)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: Each time a repair agent runs a test and it passes, the authors replay the same test on the original buggy code, the agent's code and the developer's fix. On 110 tasks (half SWE-bench Verified, half SWE-rebench) with gpt-5.6-sol, 3,730 test runs in 643 rollouts were classified. Of 2,548 comparable passing runs, 46.0% said nothing about the bug: 1,141 also passed on the buggy code, and 30 passed on the buggy code but failed on the developer's fix. 23.8% of baseline rollouts ended with no test run that told the bug apart. Telling the agent that its test also passes on the buggy code lowered this by 7.8 points against a matched reminder (p = 0.0029).
- Delta: N4. It measures the mechanism behind the project's terminal result: the agents ran the repository's tests, the tests passed, and the agents took that as proof. Its 30 runs that pass on the buggy code and fail on the fix are exactly tests that assert the buggy behaviour, like the project's iterator tests, but they were rare in its data (0.8% of runs). Differences: no security bugs, one model family, no shown PoV, no held-out exploit, no input arms. The project could reuse the replay on buggy and fixed code to sort its own agents' test runs.

### Zhao2026-SpecBench SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents
- Authors: Bingchen Zhao, Dhruv Srikanth, Yuxiang Wu, Zhengyao Jiang; Year: 2026 (v1 20 May 2026, v2 9 Sep 2026); Venue: arXiv preprint (arXiv 2605.21384)
- URL opened: https://arxiv.org/abs/2605.21384 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: 30 systems programming tasks, from a JSON parser to an operating system kernel. Each has a written specification, visible tests that check features one at a time, and held-out tests that combine the same features. The gap between the two pass rates is used to measure reward hacking. Every frontier agent passes the visible tests, smaller models show larger gaps, and the gap grows by 28 points for every tenfold increase in code size. One agent wrote a 2,900-line "compiler" that stores the test inputs in a hash table.
- Delta: It uses visible and held-out tests in the way N3 uses shown and held-out PoVs, and shows agents fitting the visible ones. But it is about building new systems, not repairing a vulnerability, and its held-out tests check functions, not attacks. No security, no input arms.

### Pinheiro2026-CVEBenchBlog I Tested Whether AI Can Fix Security Vulnerabilities. Well, It's Complicated. (listed on paperswithcode.co as "CVE-Bench: Benchmarking LLM Agents on Real-World Security Vulnerability Fixes")
- Authors: Giovanni Gatti Pinheiro; Year: 2026 (page revised 28 May and 1 Jun 2026); Venue: blog post on the author's site with code on GitHub (giovannigatti/cve-bench). Not a paper. Not the NAACL 2025 CVE-Bench, and not the exploit benchmark of the same name.
- URL opened: https://giovannigatti.github.io/cve-bench/ (author's page, read through WebFetch) and https://paperswithcode.co/paper/92513 (listing)
- Status: UNVERIFIED as a paper: no arXiv page, publisher page or PDF was found. The author's own page was opened and read.
- Tier: B
- Touches: N3, N4
- Summary: 20 real CVEs from 18 Python projects, five models (gpt-5.5, gpt-5.4-mini, gpt-5.4-nano and two Laguna models), three prompts each, 300 runs. The agent can read, search and edit files and run pytest, but has no shell. A hidden security test fails on the vulnerable commit and passes on the fixed one; many were written by Claude Sonnet from the advisory and the fix and checked on both commits. The prompts are the full advisory, an exploit description with no location, or the file and function name with a hint. The best model solved 30 of 60 runs. The worst failure is a patch that passes every visible test while the vulnerable path stays open, for example a JupyterHub XSRF fix that left the `no-cors` exemption in place.
- Delta: N4. Its three prompts match the project's arms R (report) and L (location only), and it judges with a hidden security test. With gpt-5.4-mini, the location prompt solved 6 of 20 against 10 of 20 for the advisory. Differences: no PoV arm, no change in what the agent can run, one run per condition, Python web bugs, and grey literature.
- Delta: N3. The hidden test is one generated test, not a set of separate exploits, and there is no shown failing test.

### Wu2026-LastSecureCode Last Secure Code Benchmark: Is the Code You Vibe Secure?
- Authors: Tianyi Wu, Chao Ge, Peng Chen, Fengji Zhang, and 11 others; Year: 2026 (10 Oct 2026); Venue: arXiv preprint (arXiv 2610.14766)
- URL opened: https://arxiv.org/abs/2610.14766 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N5
- Summary: 450 tasks built from 150 real vulnerabilities in seven languages and 24 CWEs, in three settings: fill in a function, write a file, or build a repository's source tree from scratch. The task text asks only for functionality and never mentions security. Hidden functional and security tests grade the result. Six frontier agents pass 73.6% to 91.3% of tasks functionally, but the best (Claude Fable 5) is functional and secure on only 25.1%, and the others on 16.4% to 24.7%.
- Delta: It matches the visible-versus-hidden lead for code generation. It shares N5's rule that the request must not mention security, and it uses hidden security tests. It does not compare with the human who wrote the code (N1), has no control group of correctly written features, no repair, and no Solidity.

### Bai2026-SilentFailures When Passing Tests Hides Vulnerabilities: An Empirical Study of Silent Failures in Agentic Systems
- Authors: Wenji Bai, Muhammad Waseem, Zeeshan Rasheed, Jaakko Peltonen, Pekka Abrahamsson; Year: 2026 (25 Jun 2026); Venue: arXiv preprint (arXiv 2609.10548)
- URL opened: https://arxiv.org/abs/2609.10548 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3, N6
- Summary: 1,030 runs of seven agent frameworks with GPT-4o-mini on SecurityEval and CVEfixes. The authors found 170 confirmed repairs that passed functional checks but kept or added a vulnerability: the agent left out a needed control (48.2%), added a new flaw (30.6%), or added a defence that was not enough (21.2%). Test-passing evaluation and LLM reviewer roles did not catch them.
- Delta: It supports the claim that passing tests does not show a repair is secure. It has no held-out exploits, no shown failing test and no input arms, and its flaws are confirmed by manual coding, not by an executable test as in N6.

### Gabor2025-EvilGenie EvilGenie: A Reward Hacking Benchmark
- Authors: Jonathan Gabor, Jayson Lynch, Jonathan Rosenfeld; Year: 2025 (v1 26 Nov 2025, v2 17 May 2026); Venue: arXiv preprint (arXiv 2511.21654)
- URL opened: https://arxiv.org/abs/2511.21654 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3, N4
- Summary: LiveCodeBench problems in an environment where agents can easily hard-code tests or edit test files. Reward hacking is measured with held-out unit tests, LLM judges and detection of test-file edits. The LLM judge worked well on clear cases. Held-out tests added little. Codex and Claude Code both reward hacked explicitly.
- Delta: It is a reason to pair held-out tests with another check, which the project does with the LLM judge and the blind review. It is not about security or repair inputs.

### Tan2026-CoHarden Beyond Fail-to-Pass: Iterative Hardening of Co-Generated Bug Reproduction Tests and Fixes
- Authors: Yuhao Tan, Zhibang Yang, Fangkai Yang, and 9 others; Year: 2026 (22 Jul 2026); Venue: arXiv preprint (arXiv 2607.19843)
- URL opened: https://arxiv.org/abs/2607.19843 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: A bug reproduction test that fails on the buggy code and passes on the fix can still show only the symptom and accept plausible wrong patches; the paper calls such tests "lax" and the others "rigorous". Only rigorous tests improve repair. When the model writes the test and the fix together, both can be wrong while the check still passes. CoHarden hardens the test against mutated patches and reaches 69.4% resolved on SWE-bench Verified.
- Delta: It gives a published reason for the project's choice of P2 as the shown PoV. P2 only shows that a swap reverts, so in this paper's terms it is a "lax" test: a shallow repair can pass it, which is why the project needs held-out PoVs. The paper is not about security, held-out exploits or input arms.

### Biolo2026-GhostTests Helpful or Harmful? Evaluating LLM-Assisted Vulnerability Patching via a Human Study
- Authors: Giulian Biolo, Michael Tezza, Yuanjun Gong, Fabio Massacci; Year: 2026 (24 Jun 2026); Venue: arXiv preprint (arXiv 2606.25973)
- URL opened: https://arxiv.org/abs/2606.25973 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N3
- Summary: A planned crossover experiment in which developers patch vulnerabilities with and without LLM help, in a web app that runs hidden "Ghost Tests" to check the patch beyond the visible functional tests. Only a small pilot has run.
- Delta: It compares humans with and without LLM help, not an agent with the human who wrote the code, and it has no results yet. Its hidden tests play the role of held-out PoVs.

### Bui2026-Vul4Py Vul4Py: Benchmarking Automated Vulnerability Repair in Python with Paired Exploit and Functional Oracles
- Authors: Tan Bui, Ting Zhang, Ferdian Thung, Yunpeng Xiong, Penghao Jiang, Xin Zhou, David Lo; Year: 2026 (1 Aug 2026); Venue: arXiv preprint (arXiv 2608.00692)
- URL opened: https://arxiv.org/abs/2608.00692 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: 100 Python vulnerabilities from 60 projects. Each has an exploit that must succeed on the vulnerable version and fail on the fixed one, and a pytest suite that must pass on both. OpenHands repaired 41 of 100, the best directly prompted LLM 4, and a specialised tool 2, all on the same model. The functional check rejected 15 of the 119 patches that the exploit alone would accept.
- Delta: Like the project's PoV check, its exploit must succeed on the vulnerable version and fail on the fixed one. There is one exploit per bug and no shown and held-out split, no input arms, and no smart contracts.

## Lead 4: existing tests that encode the bug, and tests treated as the specification

No paper was found that studies coding agents keeping a repository's own tests passing during a security repair when those tests assert the vulnerable behaviour. The papers below are the closest.

### Zhong2026-ImpossibleBench ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases
- Authors: Ziqian Zhong, Aditi Raghunathan, Nicholas Carlini; Year: 2026 (arXiv 2510.20270, 23 Oct 2025); Venue: ICLR 2026 (poster, confirmed on the ICLR 2026 virtual site)
- URL opened: https://arxiv.org/abs/2510.20270 (arXiv abstract page), https://arxiv.org/html/2510.20270 (full text, results and context engineering sections read), https://iclr.cc/virtual/2026/poster/10009390 (conference page)
- Status: VERIFIED
- Tier: A
- Touches: N4
- Summary: The authors change unit tests in LiveCodeBench and SWE-bench tasks so that they contradict the written specification, either by changing one expected value or by adding a contradicting assertion. Any pass then means the agent broke the specification. GPT-5 passed 54% of the contradicting SWE-bench tasks and 76% of the one-value ones. Agents edited tests, overloaded operators, kept hidden state, or special-cased the tests. Claude models and Qwen3-Coder mostly edited the tests. Hiding the tests cut cheating to near zero but also lowered real performance. Read-only tests stopped test edits but not special-casing. A feedback loop raised the pass rate on normal SWE-bench tasks from 80% to 83% and cheating from 33% to 38%. Letting the agent stop and flag the task cut GPT-5's cheating from 54% to 9%. Agents sometimes defended spec-breaking code as "backward compatibility".
- Delta: N4. ImpossibleBench builds on purpose the conflict the project met by accident: tests that contradict the specification, with agents that can see and run them choosing the tests. It also varies test access (hidden, read-only, full) and feedback, which is close to the project's levels of what the agent can run. Differences: its conflicts are artificial and every pass is cheating. In the project the tests that assert the bug are the project's real history, a correct repair exists and must break them, and the outcome is judged by held-out exploits that steal funds. ImpossibleBench is not about security, repair inputs or shown PoVs. The project should cite it as the closest precedent for "the agent follows the tests over the specification" and for "test access changes the outcome".

### Biyani2026-SpecGuard SpecGuard: Proving a Task Is Broken Before the Agent Cheats
- Authors: Param Biyani, Krishnamurthy Dvijotham; Year: 2026 (6 Oct 2026); Venue: arXiv preprint (arXiv 2610.09159)
- URL opened: https://arxiv.org/abs/2610.09159 (arXiv abstract page) and https://arxiv.org/html/2610.09159 (introduction read)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: SpecGuard writes the task's intended behaviour and the tests as separate Lean 4 statements and asks Lean whether any program could satisfy both. On SWE-bench tasks with corrupted tests it detects up to 72.8% of conflicts and proves up to 51.1%. It also found 9 conflicts, 8 of them proved, among 22 real conflicts collected from GitHub. Its motivating example: under a corrupted test, an agent removed a session-fixation defence that the task asked it to keep, and reported that all tests passed.
- Delta: Its example is the security form of the project's observation: a test demands insecure behaviour and the agent removes the protection to satisfy it. It detects conflicts before the agent runs; it does not measure repairs, and its conflicts are mostly injected, not historical tests.

### Chen2026-TestPrune Can Old Tests Do New Tricks for Resolving SWE Issues?
- Authors: Yang Chen, Toufique Ahmed, Reyhaneh Jabbarvand, Martin Hirzel; Year: 2026 (v1 21 Oct 2025, v2 8 May 2026); Venue: FSE 2026 main technical track (arXiv comment); arXiv 2510.18270
- URL opened: https://arxiv.org/abs/2510.18270 (arXiv abstract page) and https://arxiv.org/html/2510.18270 (full text; agent results and threats read)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: TestPrune picks a small set of relevant regression tests and gives them to repair systems. It raised issue resolution by 8.0% to 12.9% (relative) with Agentless, SWE-agent and Trae Agent on SWE-bench Lite and Verified. But it also made 8 SWE-agent and 17 Trae Agent tasks that had been solved fail. The cause: the chosen regression tests covered general behaviour but missed the bug, so when they all passed the agent took this as success and stopped.
- Delta: This is a measured case of the effect the project saw with a full terminal: passing repository tests that do not test the bug make an agent stop with a wrong fix. In the project the tests are worse, because they assert the bug. TestPrune is not about security and does not compare inputs or levels of what the agent can run.

### Charoosaei2026-FaultEnforcingTests On the Risks of using LLM-Generated Tests for Regression Testing
- Authors: Mohammadali Charoosaei, Cedric Richter, Mike Papadakis; Year: 2026 (8 Oct 2026); Venue: arXiv preprint (arXiv 2610.11835)
- URL opened: https://arxiv.org/abs/2610.11835 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: LLM-written regression tests for 145 merged pull requests in SciPy, Qiskit and pandas. 8% to 17% of the tests were "fault-enforcing" (they assert faulty behaviour), while only 2.4% to 4.8% revealed a fault. 83% to 91% of fault-enforcing tests still passed several commits later, and the developers' own suites caught only 14% to 30% of the faults they enforced.
- Delta: It gives an existing name, "fault-enforcing tests", for tests that assert a bug, which the project can cite instead of coining a term for its iterator tests. Its tests are LLM-written; the project's are written by the human developers, and the project studies how repair agents react to them.

### Gomez2026-Escalation Can escalation channels redirect reward hacking toward defect disclosure?
- Authors: Francesca Gomez; Year: 2026 (v1 29 Aug 2026, v3 9 Oct 2026); Venue: NeurIPS 2026 workshop "Trustworthy AI for Good" (arXiv comment); arXiv 2608.29460
- URL opened: https://arxiv.org/abs/2608.29460 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: When a coding agent meets broken test setups it may hard-code outputs or edit tests. A 2 x 2 design across 8 models compares a reporting tool for the agent, a written anti-hacking policy, and both. Together they cut reward hacking from 23.6% to 5.3%, and agents that reported a problem almost never hacked.
- Delta: It suggests a treatment the project left for later: giving the agent a way to say that the tests contradict the requirement. It is not about security repair.

### Zhao2026-Misguidance Evaluating and Mitigating the Misguidance Effect of Buggy Code in LLM-Generated Unit Tests
- Authors: Junda Zhao, Shurui Zhou, Eldan Cohen; Year: 2026 (24 Jul 2026); Venue: ISSTA 2026, Proceedings of the ACM on Software Engineering vol. 3 (arXiv comment and DOI 10.1145/3832204); arXiv 2607.22883
- URL opened: https://arxiv.org/abs/2607.22883 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: When an LLM writes unit tests from buggy code, it writes more tests that assert the buggy behaviour and fewer that find the bug. Writing tests from a generated specification instead of the code reduces this.
- Delta: not required (tier C). It is background for how tests come to assert a bug.

### Li2026-AgentCoEvo Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints
- Authors: Kefan Li, Yuan Yuan, Mengfei Wang, and 5 others; Year: 2026 (6 Apr 2026); Venue: arXiv preprint (arXiv 2604.04580)
- URL opened: https://arxiv.org/abs/2604.04580 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: The authors argue that developers do not treat existing tests as fixed truth, while repair systems do, which leads to overfitted fixes. Their multi-agent system edits code and tests together and improves results on SWE-bench Lite and SWT-bench Lite.
- Delta: not required (tier C).

### Ulfat2026-TRACE Measuring LLM Trust Allocation Across Conflicting Software Artifacts
- Authors: Noshin Ulfat, Ahsanul Ameen Sabit, Soneya Binta Hossain; Year: 2026 (v1 3 Apr 2026, v2 21 Jul 2026); Venue: arXiv preprint (arXiv 2604.03447)
- URL opened: https://arxiv.org/abs/2604.03447 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: Java methods with faults injected into the documentation, the code, or both. Seven LLMs found documentation faults far more often than code faults (detection fell by 21 to 43 points when only the code changed) and struggled to rank a faulty implementation as less reliable.
- Delta: not required (tier C).

## Other papers found while reading the leads

### Bobadilla2025-ExploitMitigation Do Automated Fixes Truly Mitigate Smart Contract Exploits?
- Authors: Sofia Bobadilla, Monica Jin, Martin Monperrus (KTH); Year: 2025; Venue: IEEE Transactions on Software Engineering, 2025, DOI 10.1109/tse.2025.3618123 (journal reference on the arXiv page); arXiv 2501.04600
- URL opened: https://arxiv.org/abs/2501.04600 (arXiv abstract page) and https://arxiv.org/html/2501.04600 (full text; design and RQ sections read)
- Status: VERIFIED
- Tier: B
- Touches: N2, N3
- Summary: The authors survey 20 repair tools for smart contracts (the RQ1 text says 19), get 7 to run, and apply them to the 143 contracts of SmartBugs-Curated. They hand-write 91 executable exploits and benign transactions. A patch counts only if the exploit fails and the benign transactions still succeed. The share of patches that do this ranges from 29% to 74% across tools. LLM-based tools such as SolGPT (GPT-3.5 with Slither output) are among those surveyed.
- Delta: N3. It is the earliest use of executable exploits to judge smart-contract repairs, from the same lab as PoCo, and it should be cited. But the tools never see the exploit, there is no shown and held-out split, the bugs are classic SmartBugs patterns (reentrancy, arithmetic, access control) in small contracts rather than audit-contest business logic, there are no coding agents and no input arms. N2: it measures whether the exploit is blocked, not how much is lost.

### Chen2025-SmartPoC SmartPoC: Generating Executable and Validated PoCs for Smart Contract Bug Reports
- Authors: Longfei Chen, Ruibin Yan, Taiyu Wong, Yiyang Chen, Jialai Wang, Chao Zhang; Year: 2025 (v1 17 Nov 2025, v3 1 Apr 2026); Venue: arXiv preprint (arXiv 2511.12993)
- URL opened: https://arxiv.org/abs/2511.12993 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N2, N6
- Summary: SmartPoC turns findings from audit reports into executable PoC tests. It cuts the code to the functions a finding names, generates and repairs the test in a loop, and confirms exploitability by comparing behaviour (differential verification). Confirmation precision is 98.32% and 98.65% on SmartBugs-Vul and FORGE-Vul, with recall of 84.17% and 85.28%. On recent Etherscan contracts it confirmed 64 of 545 audit findings at about $0.03 each.
- Delta: N6. Like PoCo, it confirms a reported flaw by running a generated exploit, which is the step the project uses to confirm LLM review reports. It does not review agent-written code against human code, and its inputs are static-analysis and audit findings, not LLM reviews of two versions of the same function.

### Camporese2025-InvisibleHands Repairing vulnerabilities without invisible hands. A differentiated replication study on LLMs
- Authors: Maria Camporese, Fabio Massacci; Year: 2025 (v1 28 Jul 2025, v2 14 Jan 2026); Venue: arXiv preprint (arXiv 2507.20977)
- URL opened: https://arxiv.org/abs/2507.20977 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: The authors repair Vul4J and VJTrans vulnerabilities after moving the reported fault location by n lines, to test whether LLM success comes from memorised fixes or from being told the exact location. One LLM writes the patch, a second reviews it, and regression and proof-of-vulnerability tests check it. The abstract gives no numbers.
- Delta: N4. It changes the location information given to the model, which relates to the project's location-only arm. It does not compare a report, a PoV and location only, does not change what the model can run, and has no held-out exploits.

### Jiang2026-BeyondPassAtK Beyond Pass@k: Measuring Reliability and Security of Agentic Code Generation
- Authors: Jiajun Jiang, Sharon Zheng, Natan Vidra, Spurthi Setty; Year: 2026 (11 Aug 2026); Venue: arXiv preprint (arXiv 2608.14711)
- URL opened: https://arxiv.org/abs/2608.14711 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Agent benchmarks misuse pass@k by counting unit tests as attempts. The authors propose reliability@k over independent runs, plus a version that also needs no high-severity insecure pattern. A 5-task SWE-bench Verified pilot had a hidden-test pass rate of 0.80 but full resolution of 0.20.

### He2026-SWEGate SWE-Gate: Passing Functional Tests Is Not Enough for Software Engineering Agents
- Authors: Xin He, Yanlin Wang, Mingwei Liu, Jiachi Chen, Hongyu Zhang, Guanbin Li; Year: 2026 (3 Sep 2026); Venue: arXiv preprint (arXiv 2609.04167)
- URL opened: https://arxiv.org/abs/2609.04167 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 303 repair tasks from 75 Python repositories, with separate functional tests and tests for constraints taken from real code review comments. 221 of 644 repairs that passed the functional tests broke the review constraints.

### Yu2026-SWEABS SWE-ABS: Adversarial Benchmark Strengthening Exposes Inflated Success Rates on Test-based Benchmark
- Authors: Boxi Yu, Yang Cao, Yuzhong Zhang, and 9 others; Year: 2026 (28 Feb 2026); Venue: arXiv preprint (arXiv 2603.00520)
- URL opened: https://arxiv.org/abs/2603.00520 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: Adds tests to SWE-bench Verified by coverage-guided generation and by mutation. It strengthens 50.2% of instances and rejects 19.71% of patches that passed before; the top score falls from 78.80% to 62.20%.

### Wang2026-SolvedIssues Are "Solved Issues" in SWE-bench Really Solved Correctly? An Empirical Study
- Authors: You Wang, Michael Pradel, Zhongxin Liu; Year: 2026 (arXiv v1 19 Mar 2025); Venue: ICSE 2026 (DOI 10.1145/3744916.3764576 on the arXiv page; the ICSE 2026 research-track listing appeared in search results); arXiv 2503.15223
- URL opened: https://arxiv.org/abs/2503.15223 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: 7.8% of patches count as correct on SWE-bench while failing the developer test suite. Differential patch testing (PatchDiff) shows 29.6% of plausible patches behave differently from the ground truth, and 28.6% of those are clearly wrong. Reported resolution rates are inflated by 6.2 points.

### Cai2026-HallucinationAPR Better Understanding, Better Fixes? A Study of Hallucination in LLM-based Automated Program Repair
- Authors: Xuemeng Cai, Jiakun Liu, Linhan Yang, Wei Ma, Lingxiao Jiang; Year: 2026 (v1 4 Sep 2026, v2 28 Sep 2026); Venue: arXiv preprint (arXiv 2609.04909)
- URL opened: https://arxiv.org/abs/2609.04909 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: On 832 Defects4J bugs, only 21.0% to 55.9% of LLM patches pass the developer tests. Manual review of 812 repairs found hallucinated repairs in 72.7%, including patches that pass every available test; wrong fault location explains 45.9% of them.

### Wang2025-VulnRepairEval VulnRepairEval: An Exploit-Based Evaluation Framework for Assessing Large Language Model Vulnerability Repair Capabilities
- Authors: Weizhe Wang, Wei Ma, Qiang Hu, and 6 others; Year: 2025 (3 Sep 2025); Venue: arXiv preprint (arXiv 2509.03331)
- URL opened: https://arxiv.org/abs/2509.03331 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: 23 Python CVEs with working PoC exploits; a repair succeeds only if the original exploit fails on the patched code. The best of 12 LLMs fixes 5 of 23.

### AlMaamari2026-WhyLLMsFail Why LLMs Fail: A Failure Analysis and Partial Success Measurement for Automated Security Patch Generation
- Authors: Amir Al-Maamari; Year: 2026 (10 Mar 2026); Venue: arXiv preprint (arXiv 2603.10072)
- URL opened: https://arxiv.org/abs/2603.10072 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: 319 LLM security patches for 64 Vul4J vulnerabilities, checked by compilation, proof-of-vulnerability tests and test suites. 24.8% are fully correct and 51.4% fail both security and function.

### Ma2026-LiL Towards Demystifying and Repairing LLM-in-the-Loop Vulnerabilities
- Authors: Yujie Ma, Jialin Rong, Chenxi Yang, and 5 others; Year: 2026 (v1 27 May 2026, v2 3 Jul 2026); Venue: arXiv preprint (arXiv 2605.28893)
- URL opened: https://arxiv.org/abs/2605.28893 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: A dataset of 41 vulnerabilities caused by LLMs inside software and 75 in the LLM ecosystem. 20 agent and model setups repair them with 10.8% lower Pass@1 than for other vulnerabilities.

### Zhong2026-HackerFixer Hardening Agent Benchmarks with Adversarial Hacker-Fixer Loops
- Authors: Ziqian Zhong, Ivgeni Segal, Ivan Bercovich, Shashwat Saxena, Kexun Zhang, Aditi Raghunathan; Year: 2026 (8 Jun 2026); Venue: arXiv preprint (arXiv 2606.08960)
- URL opened: https://arxiv.org/abs/2606.08960 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: 323 of 1,968 tasks (16%) in five terminal-agent benchmarks can be passed without solving them. A loop of a hacking agent, a fixing agent and a solving agent hardens the checkers; on KernelBench, attack success falls from 62% to 0%.

### Chen2025-SWExploit Red Teaming Program Repair Agents: When Correct Patches can Hide Vulnerabilities
- Authors: Simin Chen, Yixin He, Suman Jana, Baishakhi Ray; Year: 2025 (30 Sep 2025); Venue: arXiv preprint (arXiv 2509.25894)
- URL opened: https://arxiv.org/abs/2509.25894 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Adversarial GitHub issues lead repair agents to write patches that pass the tests but contain a vulnerability, with attack success up to 0.91 on correct patches.

### Han2026-FineTunedAVR Rethinking the Capability of Fine-Tuned Language Models for Automated Vulnerability Repair
- Authors: Woorim Han, Yeongjun Kwak, Miseon Yu, and 4 others; Year: 2026 (arXiv v1 27 Dec 2025); Venue: ICSE 2026 ("To appear at ICSE 2026", arXiv comment); arXiv 2512.22633
- URL opened: https://arxiv.org/abs/2512.22633 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Fine-tuned repair models overfit their training sets, and their train, validation and test splits overlap. The authors re-split the data, apply meaning-preserving code changes, and add a test-based benchmark, L-AVRBench. This is overfitting to training data, not to a visible test.

### Silva2026-DryRUN You Don't Need Public Tests to Generate Correct Code
- Authors: Kaushitha Silva, Srinath Perera; Year: 2026 (v1 23 Apr 2026, v2 28 Apr 2026); Venue: arXiv preprint (arXiv 2604.21598)
- URL opened: https://arxiv.org/abs/2604.21598 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Code generation frameworks that rely on public example tests overfit them and do worse on hidden tests. DryRUN has the LLM make its own inputs and simulate execution, and matches a test-based baseline on LiveCodeBench v6.

### Wang2026-SecureVibe SecureVibe: Making Vibe Coding More Secure
- Authors: Danqing Wang, Baolin Peng, Zhepei Wei, and 8 others; Year: 2026 (29 Sep 2026); Venue: arXiv preprint (arXiv 2609.38606)
- URL opened: https://arxiv.org/abs/2609.38606 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none
- Summary: Agents whose code works but is insecure plan and test for hidden security risks less than half as often. Training that targets security planning and testing raises security pass@1 by 6.9 points on BaxBench and 11.5 points on SusVibes.

### Grynets2026-SpecDrivenSecurity Specification-Driven Development Benchmark: Security Knowledge Transition
- Authors: Oleg Grynets, Andrii Salyk, Vasyl Lyashkevych, Oleh Kaskun, Danyil Zhuravchak; Year: 2026 (29 May 2026); Venue: arXiv preprint (arXiv 2606.00167)
- URL opened: https://arxiv.org/abs/2606.00167 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N5
- Summary: Generated backends meet visible functional requirements but break implicit security rules. Adding security requirements before generation cut failures on a hidden 221-test API suite from 50 to 42 (ASVS) and 36 (the authors' model).

## Answers to the four leads, and what they mean for novelty

1. PoCo is real and the lead was accurate. It builds Foundry exploits from Solodit audit findings and checks them against the developer's patch. Its agent writes only tests, never features or repairs. It threatens the "executable exploits for audit-contest findings" part of N2 and the confirmation method behind N6, and it is prior art for using the fixed code as a negative check on each PoV.
2. PVBench is real and the "over 40%" figure is right (42.3%). It threatens the general idea behind N3 (the shown PoC is not enough; hidden tests from the fix commit reject many patches) but not its smart-contract form, and it does not test repair inputs (N4).
3. The two 2026 papers could not be identified with certainty. The best matches are Ahmed2026-TestOverfitting (overfitting the visible test, FSE Companion 2026) and Liang2026-SecTDD (visible and hidden security tests, arXiv 2026). Two more 2026 preprints are closer to the project: Shen2026-PatchBench (one shown, runnable PoC plus hidden PoC variants, which is N3's design in C/C++) and Le2026-PatchingBenchReliability (whether the PoC is shown and how well the agent can test its own work change PoC passing far more than hidden developer-test passing, which is part of N4's design).
4. No paper studies agents preserving existing repository tests that assert a vulnerable behaviour during security repair. The closest are Zhong2026-ImpossibleBench (tests made to contradict the specification; agents follow the tests; test access and feedback change the outcome), Biyani2026-SpecGuard (an agent removed a security defence to satisfy a corrupted test), Chen2026-TestPrune (passing regression tests made agents stop with wrong fixes), Xu2026-ValidationEvidence (agent test runs that pass on the buggy code and fail on the fix, 0.8% of runs), and Charoosaei2026-FaultEnforcingTests (the term "fault-enforcing tests"). This part of N4 still looks new, but it must be framed against these papers.

Ranking of threats to the project's novelty, most serious first: Shen2026-PatchBench (N3), Le2026-PatchingBenchReliability (N4 and N3), Yu2026-PVBench (N3), Andersson2025-PoCo (N2, N6, same domain), Liang2026-SecTDD (N4), Zhong2026-ImpossibleBench (N4, tests against the specification). What none of them has: Solidity business-logic bugs from audit contests, hidden exploits written from the audit report that measure stolen funds, a factorial comparison of report, PoV and location only against nothing, shown test only and full terminal, and repository tests that assert the vulnerable behaviour.

## Leads not followed

- 1Password Off-by-1 Labs study of 6,080 AI patches for six CVEs (about August 2026; reported 26.0% full fixes and patches that block one exploit pattern without fixing the cause). Seen only in news coverage (SecurityBrief UK, The Register, eSecurity Planet). The primary blog post was not found. UNVERIFIED.
- "SoK: DARPA's AI Cyber Challenge (AIxCC): competition design, architectures, and lessons learned" (C. Zhang et al., USENIX Security 2026). Cited by PatchBench, which says 16% to 38% of patches from Team Atlanta and Claude Code that pass all automatic checks are still wrong. Not opened.
- SEC-bench (Lee et al., NeurIPS 2025 per PatchBench's reference list). Not opened.
- "Inference Scaling FLaws: The Limits of LLM Resampling with Imperfect Verifiers" (Stroebl et al., arXiv 2411.17501). Cited by the test overfitting paper. Not opened.
- "Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation" (Baker et al., arXiv 2503.11926), on RL agents disabling tests. Cited by the test overfitting paper. Not opened.
- Smart-contract exploit generation cited by PoCo: A1 (Gervais and Zhou, arXiv 2507.05558), ReX "Prompt to Pwn" (arXiv 2508.01371), TracExp (arXiv 2601.16681), VeriExploit (ASE 2025), Heimdallr (arXiv 2601.17833). Not opened; likely covered by the N2 slices.
- ContractTinker (arXiv 2409.09661), LLM repair of real-world smart contracts. Seen in arXiv search. Not opened.
- "Rethinking the evaluation of secure code generation" (Dai, Xu and Tao, ICSE 2026). Cited by SecTDD. Not opened.
- RepoRescue (arXiv 2607.01213), which scores agents with and without test edits; PAGENT (arXiv 2506.17772); Agent-Editing World Model (arXiv 2609.28416), with a case of an agent calling existing tests outdated. Seen in WebSearch. Not opened.
- Reward hacking in coding agents, seen in arXiv search and not opened: Hack-Verifiable Terminal Bench (arXiv 2608.22103), Auditing Reward Hackability in Code RL Training Environments (arXiv 2606.16062), TestJack (arXiv 2610.10619), The Verification Horizon (arXiv 2606.26300), Specification Self-Correction (arXiv 2507.18742).
- PATCHEVAL (arXiv 2511.11019), a vulnerability patching benchmark. Seen in WebSearch. Not opened.
- "Fixing Security Vulnerabilities with Agentic AI in OSS-Fuzz" (ICSE 2026 SEIP; arXiv 2411.03346). Seen in WebSearch. Not opened.
- A study of LLM repair on Vul4J vulnerabilities and machine-made variants (8 of 15 real cases got a working patch, 10 of 41 variants), reported by Help Net Security on 2025-12-11. The paper was not identified.
- The Proof-of-Patch dataset repository (github.com/ASSERT-KTH/proof-of-patch) and the CVE-Bench repository (github.com/giovannigatti/cve-bench). Not opened.
