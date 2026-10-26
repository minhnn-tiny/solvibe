# Round 2, slice S2: tests and comments that assert buggy behaviour

Search date: 21 October 2026. Round 2 bibliography agent, slice S2.

Scope: evidence about tests and comments in real repositories that assert buggy or vulnerable behaviour, and how they affect developers, tools and AI agents. The four questions were: (1) how often fix commits change or delete existing tests; (2) tests that pass on buggy code because they encode the bug, including the exact meaning of "fault-enforcing tests"; (3) LLMs and agents that treat tests or comments as the specification, or copy bugs from the surrounding code; (4) test quality in smart-contract projects.

Only papers that are not in the round 1 index are reported as new. I checked every title against both the round 1 index (`master_index_partial.tsv`) and the full index (`master_index.tsv`), as they stood at the end of this search. Three papers I found turned out to be indexed already. They are listed under "Indexed papers that bear on this slice" and are not counted as new.

API notes. DBLP returned HTTP 429, and its mirrors returned a bot check, so DBLP was not used. The OpenAlex anonymous daily budget was used up; a key needs an email address, which the protocol forbids sending, so OpenAlex was not used. Semantic Scholar worked only some of the time (HTTP 429 on many calls). Search therefore relied on WebSearch, the arXiv API, Crossref, Semantic Scholar when it answered, and full-text PDFs.

Saturation: reached. Queries 68, 69 and 70 were new queries and gave no new relevant paper.

## Queries run

| # | Query | Source | Hits looked at | New relevant papers |
|---|---|---|---|---|
| 1 | Reference list of Charoosaei et al. 2026 (arXiv 2610.11835, full PDF), plus arXiv `id_list` check of the cited arXiv papers | Snowball (references) and arXiv API | 41 references, 5 arXiv records | 4: Konstantinou2026-CodingBeforeTesting, Haroon2026-TestGenEvolution, Vahabzadeh2015-TestBugs, Barr2015-OracleProblem |
| 2 | empirical study bug-fix commits modify existing test assertions co-evolution test code | WebSearch | 9 | 2: Rafi2023-Defects4JTests, Levin2017-TestMaintenance |
| 3 | "Is this a bug or an obsolete test" Hao ECOOP 2013 | WebSearch | 9 | 1: Hao2013-BugOrObsoleteTest (unverified) |
| 4 | "Understanding myths and realities of test-suite evolution" Pinto Sinha Orso | WebSearch | 10 | 1: Pinto2012-TestSuiteEvolution |
| 5 | Labuschagne Inozemtseva Holmes "Measuring the cost of regression testing in practice" | WebSearch | 9 | 1: Labuschagne2017-RegressionTestCost |
| 6 | myths realities test-suite evolution; bug or an obsolete test; co-evolution production test code | DBLP API (3 queries) | 0 (HTTP 429; mirrors gave a bot check) | 0 |
| 7 | myths realities test-suite evolution; bug or an obsolete test | OpenAlex API (2 queries) | 0 (anonymous budget used up) | 0 |
| 8 | understanding myths and realities of test-suite evolution (title search, several tries) | Semantic Scholar API | 0 (HTTP 429) | 0 |
| 9 | "broken tests" OR "test breakage" empirical study developers repair tests after code change fix | WebSearch | 9 | 0 |
| 10 | Yaraghi "Automated Test Case Repair Using Language Models" TaRGet | WebSearch | 10 | 1: Yaraghi2025-TaRGET |
| 11 | "An empirical study of bugs in test code" Vahabzadeh Mesbah silent horrors false negatives | WebSearch | 9 | 0 (Vahabzadeh2015 already found in query 1) |
| 12 | Zaidman "co-evolution of production and test code" repository mining | WebSearch | 10 | 0 (leads only) |
| 13 | vulnerability-fixing commits include test changes percentage empirical study security patches tests | WebSearch | 9 | 0 |
| 14 | smart contract bug fix commits test files co-change empirical study Solidity GitHub | WebSearch | 10 | 0 (Wang et al. 2023 is indexed; Salzano et al. 2026 checked in full text, no test findings) |
| 15 | empirical study testing practices smart contract projects Hardhat Foundry coverage mutation score | WebSearch | 9 | 4: Barboni2021-SuMo, Hartel2020-MutationAtScale, Jain2023-MindTheGap, Bouafif2025-PRIMG |
| 16 | Barboni Morichetta Polini mutation testing Solidity "test suites" shipped applications low mutation score | WebSearch | 10 | 0 |
| 17 | "smart contract" developers testing practices survey interviews "unit tests" "test coverage" | WebSearch | 9 | 1: Palechor2022-SolidityTesting |
| 18 | Foundry invariant tests fuzz tests empirical study open-source DeFi protocols | WebSearch | 9 | 0 |
| 19 | ti:"Solidity" AND ti:tested | arXiv API | 25 | 0 |
| 20 | test smells smart contracts Solidity test code quality Truffle Hardhat | WebSearch | 10 | 0 |
| 21 | arXiv 2025 2026 empirical study Foundry tests Solidity "forge" test suite adequacy mutation audit contest | WebSearch | 9 | 0 |
| 22 | "silent horrors" OR "fault-masking" tests pass on buggy code | WebSearch | 9 | 1: Cerioli2021-TestWizard |
| 23 | misleading comments LLM code generation robustness incorrect comments | WebSearch | 9 | 3: Lam2025-CodeCrash, Kang2024-InaccurateComments, Thornton2026-AdversarialComments |
| 24 | "Large Language Models of Code Fail at Completing Code with Potential Bugs" | WebSearch | 9 | 1: Dinh2023-BuggyCodeCompletion |
| 25 | code-comment inconsistency large language models misled outdated comments | WebSearch | 10 | 1: Radmanesh2024-CommentInconsistencyBugs |
| 26 | LLM vulnerability detection misleading comments adversarial comments smart contract audit | WebSearch | 9 | 1: Wu2026-ALIBI (Alexopoulos et al. 2026 is indexed) |
| 27 | Reference list of Thornton 2026 (arXiv 2602.16741, full PDF) | Snowball (references) | 33 | 2: Zeng2025-HACKODE, Przymus2026-AdversarialBugReports |
| 28 | arXiv misleading code comments degrade LLM code generation HumanEval+ ClassEval | WebSearch | 9 | 1: Li2025-FPBench |
| 29 | LLM code generation incorrect test cases in prompt misled faulty tests | WebSearch | 9 | 2: Huang2026-IncorrectCodeTests, Mathews2024-TestGenDesignChoices |
| 30 | "Rethinking the Influence of Source Code on Test Case Generation" | WebSearch | 9 | 0 |
| 31 | coding agents treat existing repository tests as specification, modify tests to pass, SWE-bench | WebSearch | 10 | 1: Hora2026-OverMockedTests |
| 32 | LLM code completion replicates bug or vulnerability from surrounding context | WebSearch | 9 | 0 |
| 33 | agentic pull requests test code changes deleted tests weakened assertions | WebSearch | 9 | 2: Banik2026-AllSmokeNoAlarm, Dipongkor2026-AgentPRCoverage |
| 34 | LLM conflicting software artifacts tests documentation code which to trust | WebSearch | 9 | 1: Abdelsalam2026-SemanticConflicts |
| 35 | test-driven development LLM incorrect tests mislead Mathews Nagappan | WebSearch | 9 | 0 |
| 36 | outdated or incorrect API documentation misleads LLM code generation | WebSearch | 9 | 0 |
| 37 | Peitek Apel Wyrich LLM misleading identifiers comments | WebSearch | 9 | 0 |
| 38 | "Does automated unit test generation really help software testers" | WebSearch | 10 | 1: Fraser2015-GeneratedTestsHelp |
| 39 | ti:"test oracles" AND LLMs; ti:"pseudo-tested"; ti:"test oracle generation" | arXiv API (3 queries) | 24 | 4: Li2026-SelfRepairTrap, Mughal2026-OracleAuthority, VeraPerez2019-PseudoTested, Liu2023-RealisticOracleEval |
| 40 | obsolete test cases identification update production-test co-evolution CEPROT LLM | WebSearch | 9 | 3: Wang2026-TestEvoBench, Chi2025-REACCEPT, Liu2024-SYNTER |
| 41 | percentage of bug-fixing commits that also change test code | WebSearch | 9 | 0 (Herbold et al. 2022 is indexed) |
| 42 | LLM unit test generation Solidity smart contracts real-world DeFi coverage mutation | WebSearch | 9 | 0 |
| 43 | smart contract audit findings test coverage correlation DeFi Code4rena Sherlock | WebSearch | 9 | 1: Groce2020-ActualFlaws |
| 44 | SmartCoCo comment-code inconsistency smart contracts NatSpec | WebSearch | 9 | 2: Hao2023-SmartCoCo, Zhang2026-SmartComment |
| 45 | security regression tests added in vulnerability fix commits | WebSearch | 10 | 1: Braz2022-RegressionVulnerabilities |
| 46 | LLM program repair misled by incorrect existing test, agent preserves buggy behaviour to pass tests | WebSearch | 9 | 0 |
| 47 | "Do automatically generated unit tests find real faults" Shamshiri | WebSearch | 9 | 0 (lead only) |
| 48 | vulnerable code examples in prompt context propagate vulnerabilities LLM code generation | WebSearch | 9 | 1: Wu2025-SoKAI4Code |
| 49 | smart contract development challenges survey Zou TSE 2019 | WebSearch | 10 | 0 |
| 50 | coding agent trajectories modify or delete existing tests to make them pass, SWE-bench | WebSearch | 10 | 1: Chen2026-AgentWrittenTests |
| 51 | LLM generated tests "assert the buggy behavior" OR "encode the bug" OR "bug-preserving" | WebSearch | 9 | 2: Zhao2026-ProxyMetricsReplication, Khatib2026-AssertFlip |
| 52 | agent patches pass SWE-bench Verified keep code the human patch deleted | WebSearch | 9 | 1: Ebrahimi2026-DeletionAvoidance |
| 53 | LLMPROPHET regression test assertions conflict expected behaviour | WebSearch | 10 | 1: Yu2025-DeCon |
| 54 | how DeFi projects fix audit findings, commits after audit report, tests added | WebSearch | 10 | 0 |
| 55 | Solidity vulnerability fixing commits "test" files modified percentage | WebSearch | 10 | 0 |
| 56 | abs:"smart contract" AND abs:"test suites" | arXiv API | 10 | 0 |
| 57 | Papers citing Dinh et al. 2023 (arXiv 2306.03438) | Semantic Scholar citations | 60 | 1: Shen2026-LexicalCues |
| 58 | Papers citing "LLMs are Bug Replicators" (arXiv 2503.11082) | Semantic Scholar citations | 4 | 0 |
| 59 | Papers citing Konstantinou et al. 2024 (arXiv 2410.21136) | Semantic Scholar citations | 28 | 3: Xue2025-DISTINCT, Hamidi2026-TestCriteria, Canedo2026-OracleAnchoring |
| 60 | repository-level code completion buggy context propagation, completion follows existing bug | WebSearch | 9 | 0 |
| 61 | developers decide a failing test is wrong and change the assertion, "update the test" | WebSearch | 9 | 1: Rahman2025-UTFix |
| 62 | "fault-enforcing" tests | WebSearch | 9 | 0 (confirms the term's origin) |
| 63 | iComment bugs or bad comments; large-scale study of code-comment inconsistencies | Crossref (2 queries) | 4 | 1: Tan2007-iComment |
| 64 | repository tests assert vulnerable behaviour, security fix breaks existing tests, agent keeps tests passing | WebSearch | 9 | 0 |
| 65 | assertion changes in bug-fix commits, expected values updated in existing unit tests | WebSearch | 9 | 1: Peruma2021-TestFileBugs |
| 66 | Solidity smart contract test code empirical analysis GitHub Hardhat Foundry 2024 to 2026 | WebSearch | 9 | 0 |
| 67 | (not a search) Crossref and Semantic Scholar lookups to confirm venues, about 25 calls | Crossref, Semantic Scholar | not counted | 0 |
| 68 | SWE-bench gold patch modifies existing tests, PASS_TO_PASS tests updated in the fix pull request | WebSearch | 9 | 0 |
| 69 | LLM smart contract auditing misled by NatSpec or developer comments | WebSearch | 9 | 0 |
| 70 | snapshot tests, approval tests, golden files accept incorrect output | WebSearch | 9 | 0 |

## Verified definition of "fault-enforcing tests"

Source: Charoosaei, Richter and Papadakis, "On the Risks of using LLM-Generated Tests for Regression Testing", arXiv 2610.11835v1 (8 October 2026), arXiv preprint. This paper is already in the index (Charoosaei2026-FaultEnforcingTests). I opened the abstract page (https://arxiv.org/abs/2610.11835) and the full PDF (https://arxiv.org/pdf/2610.11835).

The paper coins the term. In the introduction it says: "When the code is defective, a generated test can thus encode the defect as expected behavior: the buggy implementation passes it, while a corrected version fails. We call such tests fault-enforcing (Figure 1)." A web search for the exact phrase "fault-enforcing" found no earlier use. The only other hit was a practitioner page (agentpatterns.ai) that cites this paper.

Abstract wording: "We distinguish between fault-revealing tests, which assert correctly implemented behavior, and fault-enforcing tests, which assert faulty behavior."

Formal definition (Section 3.1, "Behavioral Taxonomy"). Each generated test T runs on the faulty version C_fault and on the reference (fixed) version C_ref:
- "Fault-Enforcing (FE): T passes on C_fault and fails on C_ref, so it asserts behavior of the faulty code that the reference does not exhibit."
- The other three classes are Fault-Revealing (fails on C_fault, passes on C_ref), Weak (passes on both) and Invalid (fails on both).
- "A fault-enforcing test silently accepts the fault: it passes on the faulty code and thus gives the developer no signal of the fault, but it fails once the fault is fixed, which makes it a false alarm."

Why such tests appear (Section 6.1): "Two factors produce it. The first is the oracle problem: a model that sees only the faulty implementation may take its behavior as the intended one and write an assertion accordingly. The second is the acceptance criterion commonly applied in LLM-based regression testing (Section 3.3): a test is accepted only if it passes on the code the generator sees."

Setting and numbers, checked against Table 3 of the PDF:
- Tests were written by Claude Haiku 4.5 (claude-haiku-4-5-20251001). The model refined each test from execution feedback for up to six turns, until it passed on C_fault.
- The faults are injected mutants that survive the project's own suite: 60,780 mutants across 145 merged pull requests. They are not real bugs.
- Fault-enforcing tests: SciPy 587 (16.9%), Qiskit 281 (8.4%), pandas 1,614 (16.9%). Fault-revealing tests: 2.6%, 2.4% and 4.8%. Most tests were weak (passed on both versions): 64.6%, 69.5% and 41.4%.
- After several later commits, 83% to 91% of the fault-enforcing tests still applied and still passed.
- When the faults of all pull requests were put into one code base, 83% to 92% were still enforced at the end of the history. The developers' own suite detected only 14% to 30% of them.

Fit with the project. The pilot's repository test fits the formal definition exactly. The downward iterator test passes on the human's vulnerable code, which is C_fault, and fails on the human's fix, which is C_ref. The difference is who wrote it: a human developer, not an LLM. So the term can be used with a citation, but the paper's numbers describe LLM-generated tests on injected faults, not human-written tests on real vulnerabilities.

## Indexed papers that bear on this slice (not re-reported)

These are already in the index. They are listed by title only so that the synthesis can find them:
- On the Risks of using LLM-Generated Tests for Regression Testing.
- Can we find bugs using LLM-generated oracles? (Konstantinou et al.; its earlier arXiv title was "Do LLMs Generate Test Oracles that Capture the Actual or the Expected Program Behaviour?").
- Evaluating and Mitigating the Misguidance Effect of Buggy Code in LLM-Generated Unit Tests.
- LLMs are Bug Replicators: An Empirical Study on LLMs' Capability in Completing Bug-prone Code.
- Large Language Models and Simple, Stupid Bugs.
- Measuring LLM Trust Allocation Across Conflicting Software Artifacts.
- ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases.
- SpecGuard: Proving a Task Is Broken Before the Agent Cheats.
- Can Old Tests Do New Tricks for Resolving SWE Issues?
- Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution.
- Validation Evidence in LLM Repair Agents: How Much of What Passes Actually Tests the Bug?
- Investigating Test Overfitting on SWE-bench.
- Assessing GitHub Copilot in Solidity Development: Capabilities, Testing, and Bug Fixing.

Found again in this search and already indexed:
- "A Fine-grained Data Set and Analysis of Tangling in Bug Fixing Commits" (Herbold et al., Empirical Software Engineering). In 289,904 changed lines of validated bug-fixing commits (2,328 bugs, 28 Java projects), 39.6% of the lines changed tests and only 25.1% were part of the fix.
- "An Empirical Study on Real Bug Fixes from Solidity Smart Contract Projects" (Wang et al., Journal of Systems and Software 2023). In 6,146 bug-fix commits from 46 Solidity projects, 47% touch no Solidity file, and about 92% touch at least one other source file (JavaScript, TypeScript or Python, used for tests and deployment). The paper does not separate test files from other files, so it gives no share of fix commits that change tests. This is the only Solidity-specific number I found for question 1.
- "Measuring and Exploiting Contextual Bias in LLM-Assisted Security Code Review" (Alexopoulos et al., arXiv 2603.18740).

## Question 1: tests changed in fix commits, obsolete tests and breaking tests

### Pinto2012-TestSuiteEvolution Understanding Myths and Realities of Test-Suite Evolution
- Authors: Leandro Sales Pinto et al.; Year: 2012; Venue: Proceedings of the ACM SIGSOFT 20th International Symposium on the Foundations of Software Engineering (FSE 2012), DOI 10.1145/2393596.2393634 (venue from Crossref; the author's PDF file name says "ICSE12", which is wrong).
- URL opened: http://web.archive.org/web/20250214153409/https://faculty.cc.gatech.edu/~orso/papers/pinto.sinha.orso.ICSE12.pdf (author PDF, archived copy; the live link returns 404), and https://api.crossref.org/works/10.1145/2393596.2393634 (Crossref record).
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: The authors followed many versions of six Java programs and their JUnit suites, 17,427 test changes in all. 29% of the changes modified a test, 15% deleted one and 56% added one. Only 1,121 of the 5,111 modifications (22%, or 6% of all test changes) repaired a broken test. Repairs that changed only assertions were rare: below 10% in every program except Commons Math. Deleted failing tests mostly failed because they no longer compiled (over 92%).

### Levin2017-TestMaintenance The Co-Evolution of Test Maintenance and Code Maintenance through the lens of Fine-Grained Semantic Changes
- Authors: Stanislav Levin, Amiram Yehudai; Year: 2017; Venue: ICSME 2017 (arXiv comment: "postprint, ICSME 2017").
- URL opened: https://arxiv.org/abs/1709.09029 (arXiv record) and https://arxiv.org/pdf/1709.09029v1 (PDF).
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: The study covers 61 open-source projects, over 240,000 commits and over 4,000 developers. In the median project, test maintenance appears in less than 24.7% of corrective (bug-fix) commits. The figure is less than 30.4% for adaptive commits and less than 35% for perfective commits. Corrective commits have the lowest share (Wilcoxon test, p < 0.01). So developers usually fix code without updating or adding a test in the same commit.

### Rafi2023-Defects4JTests Back to the Future! Studying Data Cleanness in Defects4J and its Impact on Fault Localization
- Authors: Md Nakhla Rafi et al.; Year: 2023 (v3 August 2024); Venue: arXiv preprint 2310.19139. A short version, "Exploring Data Cleanness in Defects4J and Its Influence on Fault Localization Efficiency", is in the ICSE 2024 Companion (DOI 10.1145/3639478.3643125, Crossref). The same authors have an MSR 2025 paper, "Revisiting Defects4J for Fault Localization in Diverse Development Scenarios" (DOI 10.1109/MSR66628.2025.00022, Crossref). Whether that is the full version of this preprint is [uncertain].
- URL opened: https://arxiv.org/abs/2310.19139 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: The paper looks at the fault-triggering tests in Defects4J. 55% were newly added to reproduce the bug or to guard against it coming back. 22% were changed after the bug report was filed. Developers often add assertions or change test code to match the fix. Fault localization gets much worse without this knowledge from the developers (up to 415% worse on Mean First Rank).

### Labuschagne2017-RegressionTestCost Measuring the Cost of Regression Testing in Practice: A Study of Java Projects using Continuous Integration
- Authors: Adriaan Labuschagne et al.; Year: 2017; Venue: ESEC/FSE 2017, DOI 10.1145/3106237.3106288.
- URL opened: https://www.cs.ubc.ca/~rtholmes/papers/fse_2017_labuschange.pdf (author PDF).
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: The authors examined real test failures in 61 Java projects on Travis CI. They classified each failure by how the developers resolved it. 18% of test-suite runs failed, and 13% of the failures were flaky. Of the failures that were not flaky, 74% came from a bug in the system under test and 26% from incorrect or obsolete tests.

### Hao2013-BugOrObsoleteTest Is This a Bug or an Obsolete Test?
- Authors: Dan Hao et al.; Year: 2013; Venue: ECOOP 2013 (European Conference on Object-Oriented Programming), LNCS, DOI 10.1007/978-3-642-39038-8_25.
- URL opened: https://api.crossref.org/works/10.1007/978-3-642-39038-8_25 (Crossref record) and https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/978-3-642-39038-8_25 (Semantic Scholar record; the publisher hides the abstract there).
- Status: UNVERIFIED. The Springer page redirected to a login, ACM DL returned a bot check, and the Newcastle repository host did not resolve. Title, authors, venue and DOI are confirmed. The abstract was seen only in search snippets.
- Tier: B
- Touches: N4
- Summary (from search snippets, so treat as unverified): When a regression test fails, the developer must decide whether the code has a bug or the test is obsolete. The paper treats this as a classification problem and trains a Best-first Decision Tree on features of earlier failures in Java/JUnit projects. Its motivation is that test-repair techniques assume every failure comes from an obsolete test. I did not see its numbers.
- Delta: This is the decision an agent faces when its repair makes a repository test fail. In the project, agents with a terminal judged the failing repository test right and their fix wrong, while in fact the test was the thing that encoded the vulnerability. Hao et al. help humans classify failures after ordinary code changes. They do not study security fixes, tests that assert a vulnerability, or AI agents.

### Yaraghi2025-TaRGET Automated Test Case Repair Using Language Models
- Authors: Ahmadreza Saboor Yaraghi et al.; Year: 2025; Venue: IEEE Transactions on Software Engineering 51(4), DOI 10.1109/TSE.2025.3541166 (arXiv comment and DOI). It was also presented at FSE 2025 in the journal-first track, per the conference page seen in search results.
- URL opened: https://arxiv.org/abs/2401.06765 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: TaRBench holds 45,373 repairs of broken tests from 59 open-source projects. This shows how often tests break when the code under test changes. TaRGET fine-tunes code language models on context that describes the breakage and reaches 66.1% exact match.

### Rahman2025-UTFix UTFix: Change Aware Unit Test Repairing using LLM
- Authors: Shanto Rahman et al.; Year: 2025; Venue: OOPSLA 2025 (arXiv comment); Semantic Scholar lists Proceedings of the ACM on Programming Languages, DOI 10.1145/3720419.
- URL opened: https://arxiv.org/abs/2503.14924 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: An LLM repairs unit tests that fail after their focal method changes. It fixes assertion failures and restores lost coverage. It repaired 89.2% of assertion failures on the authors' synthetic benchmark and 60% on real-world cases. The abstract cites a Meta study saying that 14% to 22% of failures come from outdated tests; I did not find that study. On my reading of the abstract, the changed code is taken as the correct behaviour, as in other test-repair work.

### Chi2025-REACCEPT REACCEPT: Automated Co-evolution of Production and Test Code Based on Dynamic Validation and Large Language Models
- Authors: Jianlei Chi et al.; Year: 2024 (arXiv) / 2025; Venue: Proceedings of the ACM on Software Engineering, DOI 10.1145/3728930 (per Semantic Scholar; issue [uncertain]).
- URL opened: https://arxiv.org/abs/2411.11033 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: The tool uses LLMs, retrieval and test execution to find obsolete tests and update them. On 537 Java projects it reached 60.16% update accuracy on correctly identified obsolete tests, 90% above the earlier tool CEPROT.

### Liu2024-SYNTER Fix the Tests: Augmenting LLMs to Repair Test Cases with Static Collector and Neural Reranker
- Authors: Jun Liu et al.; Year: 2024; Venue: ISSRE 2024 (arXiv comment; DOI 10.1109/ISSRE62328.2024.00043 per Semantic Scholar).
- URL opened: https://arxiv.org/abs/2407.03625 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: The paper repairs tests made obsolete by breaking changes to code syntax. Static analysis gathers class, usage and environment context, and a reranker picks the most useful parts for the LLM. With this context, hallucinations fell by 57.1%.

### Wang2026-TestEvoBench TestEvo-Bench: An Executable and Live Benchmark for Test and Code Co-Evolution
- Authors: Jiale Amber Wang et al.; Year: 2026; Venue: arXiv preprint 2607.02469.
- URL opened: https://arxiv.org/abs/2607.02469 (arXiv record).
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: The benchmark has 746 test-generation tasks and 509 test-update tasks. They come from 152 Java projects, chosen from 59,950 candidate records. In a test-update task, the agent must change failing existing tests to fit the changed code. Claude Code, Gemini CLI and SWE-Agent, run with Claude Opus 4.7 or Gemini 3.1 Pro, reach up to 77.5% on generation and 74.6% on update. Scores are lower on the most recent tasks and under a tight cost budget.
- Delta: The benchmark rewards an agent for changing an old test to match new code, so it treats the code change as right. The project needs that same step in a security repair: the repository test asserts the vulnerable behaviour, so a correct repair must change it. Agents with a terminal did not change it. TestEvo-Bench does not single out bug fixes whose old tests asserted the bug (as far as the abstract says), and it has no security or Solidity tasks.

### Braz2022-RegressionVulnerabilities An Exploratory Study on Regression Vulnerabilities
- Authors: Larissa Braz et al.; Year: 2022; Venue: ESEM 2022, DOI 10.1145/3544902.3546250.
- URL opened: https://arxiv.org/abs/2207.01942 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: At Mozilla the authors studied 78 regression vulnerabilities and 72 bug reports in which a bug fix introduced a vulnerability, and they interviewed five developers. Security was not discussed during the bug fixes. Developers assumed that tools would catch regressions, and dynamic analysis tools found about 30% of them.

### Peruma2021-TestFileBugs On the Distribution of "Simple Stupid Bugs" in Unit Test Files: An Exploratory Study
- Authors: Anthony Peruma, Christian D. Newman; Year: 2021; Venue: MSR 2021 Mining Challenge (per the conference page seen in search results; not opened).
- URL opened: https://arxiv.org/abs/2103.09388 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: The authors compared single-statement bug fixes in test files and production files of Java Maven projects. These fixes are more common in production files. In test files, most fixes touch assertion statements, so wrong expected values in tests do get fixed later. Most test files with such fixes also show test smells. The abstract gives no percentages.

## Question 2: tests that pass on buggy code because they encode the bug

### Vahabzadeh2015-TestBugs An Empirical Study of Bugs in Test Code
- Authors: Arash Vahabzadeh, Amin Milani Fard, Ali Mesbah; Year: 2015; Venue: ICSME 2015.
- URL opened: https://people.ece.ubc.ca/amesbah/resources/papers/icsme15.pdf (author PDF).
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: The authors mined 211 Apache projects, found 5,556 bug reports about test code, and classified a sample of 443. About half of the projects had bugs in their test code. 97% of test bugs were false alarms, where the test fails while the production code is correct. 3% were what the authors call "silent horrors": the test passes while the production code is incorrect. 67% of those came from incorrect or missing assertions. Obsolete tests caused 14% of the false alarms.
- Delta: This is the closest human-side evidence that real test suites contain tests which pass on wrong code. Such tests are rarely reported (3% of fixed test bugs), which suggests they are rarely noticed. The paper counts reported bugs in Java projects and does not study how tools or agents react to such tests. The project has a concrete case in a Solidity repository and measures what agents do with it.

### Fraser2015-GeneratedTestsHelp Does Automated Unit Test Generation Really Help Software Testers? A Controlled Empirical Study
- Authors: Gordon Fraser et al.; Year: 2015; Venue: ACM Transactions on Software Engineering and Methodology 24(4), Article 23, DOI 10.1145/2699688.
- URL opened: https://eprints.whiterose.ac.uk/96274/1/j15.pdf (submitted version, White Rose repository).
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: Two controlled experiments had 97 participants test Java classes with seeded faults, either by hand or with EvoSuite. EvoSuite writes assertions that record what the current, faulty class does. The tool raised coverage (up to 300%) but did not raise the number of faults found. Participants with EvoSuite kept more tests that asserted the faulty behaviour. Tests that failed on the correct class rose from 1.22 to 8.5 on average for one class (Option, p = 0.001) and from 0.75 to 2.5 for another (DocType, p = 0.026). The count did not drop during the session.
- Delta: People who were handed tests that assert a fault mostly kept them. The project sees the same pattern with AI agents and human-written repository tests. Fraser et al. study test writing with seeded faults, not repair of real vulnerabilities, and their participants are humans.

### Konstantinou2026-CodingBeforeTesting On the risk of coding before testing: An empirical study on LLM-based test generation workflow
- Authors: Michael Konstantinou, Florian Tambon, Mike Papadakis; Year: 2026; Venue: arXiv preprint 2607.05139.
- URL opened: https://arxiv.org/abs/2607.05139 (arXiv record).
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: When an LLM writes tests after, and from, faulty code that it generated, the faults are copied into the tests. Code and tests then agree with each other and hide the defect. Fault detection falls from 25% when tests are generated on their own to 14% when they are generated after the faulty code. The effect remains with chain-of-thought prompting and in multi-step agent workflows.
- Delta: It shows how a test comes to assert a bug when one author writes both the code and the test. In the project the human developer wrote both the iterator and its test, and the agent inherited them. The paper studies generation on programming tasks, not repair, and not security.

### Huang2026-IncorrectCodeTests Measuring the Influence of Incorrect Code on Test Generation
- Authors: Dong Huang et al.; Year: 2024 (arXiv v1; v3 March 2025); Venue: arXiv preprint 2409.09464 (comment: "Under review"). Semantic Scholar lists ICSE 2026, DOI 10.1145/3744916.3764532; I did not check the publisher page. An earlier title was "Rethinking the Influence of Source Code on Test Case Generation" (per search results).
- URL opened: https://arxiv.org/abs/2409.09464 (arXiv record).
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: The study uses 11 LLMs (5 open, 6 closed), three benchmarks and 41 real repository examples. Compared with incorrect code under test, correct code gives tests that are 57% more accurate, with 12% more coverage and 24% more bug detection. On real code, tests written for incorrect code detect 47% fewer bugs. Adding a natural-language description of the code gives +18% accuracy, +4% coverage and +34% bug detection.
- Delta: It measures how buggy code shapes the tests an LLM writes. The project looks at the opposite direction: how tests that already assert a bug shape the code an agent writes during repair.

### Mathews2024-TestGenDesignChoices Design choices made by LLM-based test generators prevent them from finding bugs
- Authors: Noble Saji Mathews, Meiyappan Nagappan; Year: 2024; Venue: arXiv preprint 2412.14137.
- URL opened: https://arxiv.org/abs/2412.14137 (arXiv record) and https://arxiv.org/pdf/2412.14137v1 (PDF).
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: The authors ran GitHub Copilot, CodiumAI CoverAgent and CoverUp on 287 buggy student programs from the Refactory dataset. CoverAgent and CoverUp keep a test only if it passes on the code under test. Their final suites contained tests that confirm the bug in 59.6% (CoverAgent) and 68.1% (CoverUp) of cases, against 4.2% for Copilot, which has no such filter. Tests that would have exposed the bug were thrown away or "fixed".
- Delta: A rule that keeps only tests passing on the current code turns a test generator into something that confirms bugs. The project sees the same rule at work in agents with a terminal: a repair that makes a repository test fail gets undone, even when that test asserts the vulnerability. The paper studies test generation on student code, not repair agents or security.

### Li2026-SelfRepairTrap Escaping the Self-Repair Trap: Improving Test Oracle Generation via Dual-Context Awareness
- Authors: Kefan Li, Hongyue Yu, Yuan Yuan; Year: 2026; Venue: ASE 2026 (arXiv comment), DOI 10.1145/3832783.3834421.
- URL opened: https://arxiv.org/abs/2608.05917 (arXiv record).
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: In regression-oracle completion, the model fills in the assertions for a given test, and the current program is taken as the expected behaviour. When the model fixes its assertions in rounds, using execution results as feedback, it drifts toward assertions that are easy to satisfy and poor at detecting faults. The authors call this the "Self-Repair Trap". A single-pass method with better static and runtime context finds more faults at lower cost.
- Delta: Feedback that rewards passing pushes the model toward whatever the current code does. The project saw the same direction when agents could run tests: they kept the tests passing and kept the bug. The paper studies assertion writing for given test inputs, not repair, and has no security setting.

### Haroon2026-TestGenEvolution Evaluating LLM-Based Test Generation Under Software Evolution
- Authors: Sabaat Haroon et al.; Year: 2026; Venue: arXiv preprint 2603.23443.
- URL opened: https://arxiv.org/abs/2603.23443 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: The study used 8 LLMs and 22,374 program variants. After changes that alter what a program does, only 66% of newly generated tests pass. Over 99% of the failing tests pass on the original program while running the changed region, so they still assert the old behaviour.

### Xue2025-DISTINCT DISTINCT: A Description-Guided Branch-Consistency Analysis Framework for Non-Regressive Test Case Generation
- Authors: Pengyu Xue et al.; Year: 2025; Venue: arXiv preprint 2506.07486.
- URL opened: https://arxiv.org/abs/2506.07486 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: On defective methods, EvoSuite, ChatTester and ChatUniTest reach up to 83% branch coverage, but none of their tests exposes the defects. Giving the LLM a natural-language description and checking each branch against it raises defect detection by 95.22% on average (Defects4J-Desc and QuixBugs-Desc).

### Hamidi2026-TestCriteria How effective are traditional test criteria at detecting bugs in large language models generated code?
- Authors: Asma Hamidi et al.; Year: 2026; Venue: arXiv preprint 2609.09315.
- URL opened: https://arxiv.org/abs/2609.09315 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: The setting has an LLM write both the code and the tests: 5 LLMs, 4 benchmarks and over 6,000 faulty programs. Fault detection is extremely low, often near zero, because the assertions do not capture the faulty behaviour that the test inputs trigger. Mutation testing is only a little better than coverage.

### Canedo2026-OracleAnchoring Oracles That Cannot Fail: Anchoring and the Expectation That Moves With the Fault
- Authors: Arquimedes Canedo; Year: 2026; Venue: arXiv preprint 2608.17214.
- URL opened: https://arxiv.org/abs/2608.17214 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: If a test takes its expected value from the code it checks, a fault that moves both values together can never make it fail. The study covers one deployed air traffic control simulator and 366 mutants. Basing one oracle on the published procedure instead caught 8 of 46 mutants that it had missed. It is a single-author, single-system study.

### Zhao2026-ProxyMetricsReplication Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness? (Replicability Study)
- Authors: Junda Zhao, Shurui Zhou, Eldan Cohen; Year: 2026; Venue: ISSTA 2026, Proceedings of the ACM on Software Engineering 3 (ISSTA), Article ISSTA002, DOI 10.1145/3832093 (arXiv comment).
- URL opened: https://arxiv.org/abs/2607.22880 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: When the code given to the LLM may already be buggy, and the goal is to expose that bug, coverage and mutation score do not predict real-bug detection. They are useful only in the regression setting, where the code is assumed correct. This is by the same group as the indexed "misguidance" paper.

### Yu2025-DeCon DeCon: Detecting Incorrect Assertions via Postconditions Generated by a Large Language Model
- Authors: Hao Yu et al.; Year: 2025; Venue: arXiv preprint 2501.02901.
- URL opened: https://arxiv.org/abs/2501.02901 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: Over 62% of assertions written by four LLMs for HumanEval were wrong: they failed on the reference solution. Postconditions written by an LLM and filtered with the given input/output examples flag over 64% of the wrong assertions and raise Pass@1 by 4%.

### Khatib2026-AssertFlip AssertFlip: Reproducing Bugs via Inversion of LLM-Generated Passing Tests
- Authors: Lara Khatib, Noble Saji Mathews, Meiyappan Nagappan; Year: 2025 (arXiv); Venue: arXiv preprint 2507.17542. Semantic Scholar lists ICSE 2026, DOI 10.1145/3744916.3773127.
- URL opened: https://arxiv.org/abs/2507.17542 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N3, N4
- Summary: The LLM first writes a test that passes on the buggy behaviour. The tool then inverts the test so that it fails while the bug is present. This reaches 43.6% fail-to-pass on SWT-Bench-Verified. A repository test that asserts a bug is the passing half of this method, so it could be flipped into a proof of the bug.

### Liu2023-RealisticOracleEval Towards More Realistic Evaluation for Neural Test Oracle Generation
- Authors: Zhongxin Liu et al.; Year: 2023; Venue: ISSTA 2023 (arXiv comment).
- URL opened: https://arxiv.org/abs/2305.17047 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: Building the test inputs from the bug-fixed version, rather than the buggy one, inflates the bugs found by the oracle generator TOGA by 61.8%. TOGA's precision is 0.38%. A simple baseline that only expects no exception finds 61% of TOGA's bugs with twice the precision.

### VeraPerez2019-PseudoTested A Comprehensive Study of Pseudo-tested Methods
- Authors: Oscar Luis Vera-Pérez et al.; Year: 2018 (online) / 2019; Venue: Empirical Software Engineering, DOI 10.1007/s10664-018-9653-2 (arXiv journal reference).
- URL opened: https://arxiv.org/abs/1807.05030 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: A method is pseudo-tested when the suite covers it but no test fails if the method body is removed. A replication on over 28,000 methods found such methods in every project studied. A manual analysis of 101 of them showed they are less tested than other methods, and developers would often not pay to fix this. So a suite can cover code and pass while being blind to what that code does.

### Mughal2026-OracleAuthority LLM-Based Test Oracles: Source-of-Authority Taxonomy -- A Systematic Literature Review
- Authors: Ali Hassaan Mughal, Muhammad Bilal; Year: 2026; Venue: IEEE Access vol. 14, DOI 10.1109/ACCESS.2026.3729738 (arXiv journal reference).
- URL opened: https://arxiv.org/abs/2607.05031 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: The review covers 83 studies of LLM test oracles. Just over half reach a verdict with no specification at all. Oracle quality is most often judged by how closely it resembles a known oracle, not by whether it catches injected faults.

### Barr2015-OracleProblem The Oracle Problem in Software Testing: A Survey
- Authors: Earl T. Barr et al.; Year: 2015; Venue: IEEE Transactions on Software Engineering 41(5), DOI 10.1109/TSE.2014.2372785.
- URL opened: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/TSE.2014.2372785 (Semantic Scholar record with title, authors and abstract) and the Crossref record.
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: This is the standard survey of the test oracle problem: given an input, how to tell correct behaviour from incorrect behaviour. When no specification or model is adequate, the human remains the last source of oracle information. It is the classic citation for why tests can end up asserting what the code does rather than what it should do.

### Cerioli2021-TestWizard Fight silent horror unit test methods by consulting a TestWizard
- Authors: Maura Cerioli et al.; Year: 2021; Venue: Journal of Software: Evolution and Process, DOI 10.1002/smr.2396.
- URL opened: https://api.crossref.org/works?query.bibliographic=TestWizard (Crossref record with the publisher's abstract).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: The paper targets tests that pass on incorrect implementations, which it calls "silent horrors" or false-negative tests. TestWizard checks each test against its written specification. Across 1,012 tests written by 123 students, it was more accurate than code review by students and slightly better than three senior experts. It flagged up to 21.22% of test methods as false negatives.

## Question 3: LLMs and agents that follow tests, comments or buggy context

### Dinh2023-BuggyCodeCompletion Large Language Models of Code Fail at Completing Code with Potential Bugs
- Authors: Tuan Dinh et al.; Year: 2023; Venue: Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Main Conference Track.
- URL opened: https://papers.neurips.cc/paper_files/paper/2023/hash/819cebb05f993840e8a52d7564c5c282-Abstract-Conference.html (NeurIPS proceedings abstract page).
- Status: VERIFIED
- Tier: B
- Touches: N1, N4
- Summary: The paper studies code completion when the existing code already contains a likely bug. It builds two datasets: buggy-HumanEval, with synthetic operator changes, and buggy-FixEval, with real user submissions. One such bug in the context cuts CodeGen-2B-mono's pass rate on buggy-HumanEval by more than half. Post-hoc fixes recover only part of the loss.
- Delta: A bug in the surrounding code pulls completions toward wrong programs. This bears on N1, because the project's agents rewrite one function inside the human's code base, where related code and tests may carry the same flaw. The paper uses short single-function contexts, with no repository, no tests and no security bugs.

### Lam2025-CodeCrash CodeCrash: Exposing LLM Fragility to Misleading Natural Language in Code Reasoning
- Authors: Man Ho Lam et al.; Year: 2025; Venue: NeurIPS 2025 (arXiv comment; Semantic Scholar agrees).
- URL opened: https://arxiv.org/abs/2504.14119 (arXiv record).
- Status: VERIFIED
- Tier: B
- Touches: N4, N6
- Summary: CodeCrash has 1,279 questions from CruxEval and LiveCodeBench. Each comes with structural changes or misleading natural-language context. Across 17 LLMs, models rely too much on the natural-language cues: output prediction drops by 23.2% on average, and still by 13.8% with chain-of-thought. Reasoning models given plausible but wrong hints spend 2 to 3 times more tokens and sometimes fail badly.
- Delta: It measures how misleading text next to code changes a model's reading of that code. In the project the misleading signal is an executable test plus the code's own design, and the task is repair. CodeCrash has no agents, no tests and no security.

### Abdelsalam2026-SemanticConflicts A Mechanistic Lens on Semantic Conflicts: Using Activation Patching to Understand LLM Behavior
- Authors: Youssef Abdelsalam et al.; Year: 2026; Venue: arXiv preprint 2607.05587.
- URL opened: https://arxiv.org/abs/2607.05587 (arXiv record).
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: The authors built 45 sets of Python snippets in which comments or identifiers suggest different behaviour from what the code does. They tested four open-weight LLMs on output prediction and on unit-test generation. In both tasks the conflicts significantly reduced correctness, and all models often followed the misleading cues. Activation patching showed where in the model the conflict signal sits.
- Delta: When comments and code disagree, models often write tests that follow the comment. The project's case is the mirror image: the test follows the buggy code, and the agent follows the test. The study uses small snippets, with no agents and no repair.

### Ebrahimi2026-DeletionAvoidance To Add Is Machine, To Delete Is Human: Measuring and Mitigating Deletion Avoidance in LLM Code Editing
- Authors: Amir M. Ebrahimi et al.; Year: 2026; Venue: arXiv preprint 2607.28887.
- URL opened: https://arxiv.org/abs/2607.28887 (arXiv record).
- Status: VERIFIED
- Tier: B
- Touches: N3, N4
- Summary: The five leading models on SWE-bench Verified remove at most 71.7% of the lines the developer's patch removes, even on tasks that all five solve. They reach the right file for over 92% of required deletions but cut the exact line in under 52% of cases. 29.0% of passing patches wrap the code that should go in a guard or fallback, which the authors call "Guard-and-Go". On 34 tasks given tests that fail if that code remains, four models drop from 63.2% to 41.9%.
- Delta: Passing tests let agents keep old behaviour alive behind a guard. This matches the project's shallow repairs, which blocked the shown PoV but left a path that a held-out PoV used. The paper uses general SWE-bench tasks and added deletion checks, not exploits. It does not vary what the agent can run.

### Przymus2026-AdversarialBugReports Adversarial Bug Reports as a Security Risk in Language Model-Based Automated Program Repair
- Authors: Piotr Przymus, Andreas Happe, Jürgen Cito; Year: 2025 (arXiv) / 2026; Venue: MSR 2026 per Semantic Scholar, DOI 10.1145/3793302.3793352.
- URL opened: https://arxiv.org/abs/2509.05372 (arXiv record).
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: The authors wrote 51 adversarial bug reports and gave them to a leading LLM-based repair system. 90% of the reports led to patches that did what the attacker wanted. The best filter applied before repair blocked 47% of them, and checks after repair (GitHub Copilot, CodeQL) caught 58%.
- Delta: It shows that the written report steers the repair even when the report is wrong. In the project the written audit report is one of the repair inputs and is correct; the misleading signal comes from the repository tests instead. The paper studies deliberate attacks rather than honest but wrong artefacts, and does not vary what the agent can run.

### Thornton2026-AdversarialComments Can Adversarial Code Comments Fool AI Security Reviewers -- Large-Scale Empirical Study of Comment-Based Attacks and Defenses Against LLM Code Analysis
- Authors: Scott Thornton; Year: 2026; Venue: arXiv preprint 2602.16741. The v1 PDF carries a different title: "LLM Code Reviewers Are Harder to Fool Than You Think: Adversarial Comments Fail Where Vulnerability Patterns Succeed". Round 1 listed it only as a lead (in the human-versus-AI file); it is not in the index.
- URL opened: https://arxiv.org/abs/2602.16741 (arXiv record) and https://arxiv.org/pdf/2602.16741v1 (PDF).
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: The benchmark has 100 code samples in Python, JavaScript and Java, each with 8 comment variants, and was run on 8 frontier models (9,366 trials). Adversarial comments had small, non-significant effects on vulnerability detection (McNemar p > 0.21). Cross-checking against static analysis reached 96.9% detection. Misses cluster in hard classes: race conditions, timing side channels and complex authorization logic.
- Delta: For the project's LLM security review, this suggests that comments in the code change detection little, while hard logic flaws are what get missed. The project's flaws are business-logic and accounting bugs in Solidity, close to the hard classes here. The paper has no Solidity and confirms nothing with an executable test.

### Wu2026-ALIBI ALIBI: Adaptive Agentic Attacks on LLM-Based Vulnerability Detectors via Adversarial Code Comments
- Authors: Zixuan Wu, Cristina Nita-Rotaru; Year: 2026; Venue: arXiv preprint 2607.24964.
- URL opened: https://arxiv.org/abs/2607.24964 (arXiv record).
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: A coding agent implements a feature, adds a vulnerability, and keeps refining source comments using the detector's own feedback. Against four LLM-based detectors, attacks succeed over 90% of the time on 125 real null-pointer-dereference vulnerabilities, and 100% on one system. Removing comments before detection and isolating the detector help. Defences written into the prompt help little.
- Delta: Unlike Thornton2026, comments refined against the detector do fool it. This matters for the project's review, which runs the same prompt on agent code and human code. If agent code carries more or different comments, the reviewer may treat it differently. The project confirms every reported flaw with a PoV, which removes that risk for confirmed flaws but not for missed ones.

### Wu2025-SoKAI4Code SoK: Understanding (New) Security Issues Across AI4Code Use Cases
- Authors: Qilong Wu et al.; Year: 2025; Venue: arXiv preprint 2512.18456. Round 1 opened it (secure code generation and repository benchmark files) but did not index it.
- URL opened: https://arxiv.org/abs/2512.18456 (arXiv record) and https://arxiv.org/pdf/2512.18456 (PDF, Section 5.2).
- Status: VERIFIED
- Tier: B
- Touches: N1, N4
- Summary: In one experiment, six models were shown 200 vulnerable C/C++ functions (75 CWE types, from BigVul) before a related generation task. Vulnerabilities rose by only 1.0% to 5.5% over controls (Fisher's exact test, p > 0.31). Showing the patched version instead did not lower the rate. The base rate of vulnerable output was about 45%.
- Delta: This is counter-evidence to the claim that LLMs copy bugs they see: one vulnerable example in the prompt did not raise the rate. The project's setting is different. The flaw sits in the design of the same function and in the repository's tests, and agents with a terminal work to keep those tests passing. The SoK has no repository, no tests and no agents.

### Zeng2025-HACKODE Inducing Vulnerable Code Generation in LLM Coding Assistants
- Authors: Binqi Zeng et al.; Year: 2025; Venue: arXiv preprint 2504.15867.
- URL opened: https://arxiv.org/abs/2504.15867 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: Attackers hide attack sequences in external material that coding assistants look up, so that the assistants write vulnerable code such as buffer overflows and missing validation. Success was 84.29% across four LLMs and 75.92% on a real application.

### Li2025-FPBench Refining Critical Thinking in LLM Code Generation: A Faulty Premise-based Evaluation Framework
- Authors: Jialin Li et al.; Year: 2025; Venue: arXiv preprint 2508.03622.
- URL opened: https://arxiv.org/abs/2508.03622 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4, N5
- Summary: FPBench gives 15 LLMs code-generation inputs that contain one of three kinds of false premise. Most models reason poorly under false premises and catch the error only when told to look for one. A search snippet says one kind uses comments that misdescribe the code [uncertain; not checked in the full text]. This relates to the pilot result that feature requests describing the human's flawed design led every compiled run to the bug.

### Shen2026-LexicalCues On the Lexical Superstition of Large Language Models for Code Comprehension: Re-evaluation on Code of Low Lexical Quality
- Authors: Xin Shen et al.; Year: 2026; Venue: arXiv preprint 2609.26388.
- URL opened: https://arxiv.org/abs/2609.26388 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N6
- Summary: The authors rename identifiers without changing what the code does. Model performance falls as names are removed or made misleading, and answers follow the meaning the misleading names suggest. Prompting and fine-tuning do not remove the effect.

### Radmanesh2024-CommentInconsistencyBugs Investigating the Impact of Code Comment Inconsistency on Bug Introducing
- Authors: Shiva Radmanesh et al.; Year: 2024; Venue: arXiv preprint 2409.10781.
- URL opened: https://arxiv.org/abs/2409.10781 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: GPT-3.5 detected cases where code and its comments disagree. Changes that left code and comment inconsistent were about 1.5 times more likely to lead to a bug-introducing commit than consistent changes. The effect was strongest right after the inconsistency appeared.

### Kang2024-InaccurateComments Identifying Inaccurate Descriptions in LLM-generated Code Comments via Test Execution
- Authors: Sungmin Kang, Louis Milliken, Shin Yoo; Year: 2024; Venue: arXiv preprint 2406.14836.
- URL opened: https://arxiv.org/abs/2406.14836 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: For the best of three LLMs, about a fifth of the comments it wrote contained statements that were shown to be false. Existing tools that check code-comment consistency had no significant relationship with accuracy. Having an LLM write tests from the comment and running them did track accuracy.

### Tan2007-iComment /*icomment: bugs or bad comments?*/
- Authors: Lin Tan, Ding Yuan, Gopal Krishna, Yuanyuan Zhou; Year: 2007; Venue: Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP 2007), DOI 10.1145/1294261.1294276; also in ACM SIGOPS Operating Systems Review, DOI 10.1145/1323293.1294276.
- URL opened: https://api.crossref.org/works?query.bibliographic=iComment (Crossref record with the publisher's abstract, DOI 10.1145/1323293.1294276).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: When comments and code disagree, either the code is buggy or the comment is wrong, and wrong comments can mislead programmers into new bugs. On Linux, Mozilla, Wine and Apache, iComment extracted 1,832 rules from comments (90.8% to 100% accuracy). It found 60 inconsistencies: 33 new bugs and 27 bad comments.

### Hora2026-OverMockedTests Are Coding Agents Generating Over-Mocked Tests? An Empirical Study
- Authors: Andre Hora, Romain Robbes; Year: 2026; Venue: MSR 2026 (arXiv comment). Round 1 listed it only as a lead (repair file); it is not in the index.
- URL opened: https://arxiv.org/abs/2602.00409 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: The authors analysed 1.2 million commits from 2025 in 2,168 TypeScript, JavaScript and Python repositories. 23% of commits by coding agents add or change test files, against 13% of other commits. 36% of agent commits add mocks to tests, against 26% of other commits.

### Banik2026-AllSmokeNoAlarm All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code
- Authors: Dipayan Banik et al.; Year: 2026; Venue: IEEE AITest 2026 (arXiv comment), DOI 10.1109/AITest70988.2026.00038.
- URL opened: https://arxiv.org/abs/2606.18168 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: The authors examined 86,156 test-file patches from 33,596 pull requests by Codex, Copilot, Devin, Cursor and Claude Code. 80.2% had weak or no explicit assertions. Pull requests with strong assertions were more likely to be merged (odds ratio 1.28).

### Dipongkor2026-AgentPRCoverage Test Coverage Analysis of Agentic Pull Requests
- Authors: Atish Kumar Dipongkor et al.; Year: 2026; Venue: to appear at ICSME 2026 (arXiv comment); arXiv preprint 2607.18057.
- URL opened: https://arxiv.org/abs/2607.18057 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: The study covers 4,882 agent pull requests from the AIDev dataset. Agents changed tests in only 49.6% of the pull requests that changed tested code. Existing tests covered 61.5% of the changed lines in Java and 27.0% in Python. In 64.8% of Python pull requests, no existing test ran any changed line.

### Chen2026-AgentWrittenTests Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents
- Authors: Zhi Chen et al.; Year: 2026; Venue: arXiv preprint 2602.07900.
- URL opened: https://arxiv.org/abs/2602.07900 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: The authors analysed six LLMs on SWE-bench Verified. Solved and unsolved tasks show similar rates of test writing. Tests that agents write are mostly print statements rather than assertions. Changing the prompt to get more or fewer tests did not significantly change outcomes.

## Question 4: test quality in smart-contract projects, and comments in smart contracts

### Palechor2022-SolidityTesting How are Solidity smart contracts tested in open source projects? An exploratory study
- Authors: Luisa Palechor, Cor-Paul Bezemer; Year: 2022; Venue: IEEE/ACM 3rd International Conference on Automation of Software Test (AST 2022), DOI 10.1145/3524481.3527228.
- URL opened: http://asgaard.ece.ualberta.ca/papers/Conference/AST_2022_Palechor_How_are_Solidity_smart_contracts_tested_in_open_source_projects.pdf (author PDF).
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: The study covers 139 open-source Solidity projects. Core developers write most of the tests, and Truffle and Hardhat are by far the most used tools. 93% of projects do functional testing, 9.4% do security testing, and none do performance testing. 34 projects mentioned or published external audit reports. The lab's announcement page says 25, but the paper says 34.

### Groce2020-ActualFlaws What are the Actual Flaws in Important Smart Contracts (and How Can We Find Them)?
- Authors: Alex Groce et al.; Year: 2020; Venue: Financial Cryptography and Data Security (FC 2020), LNCS, DOI 10.1007/978-3-030-51280-4_34 (Crossref).
- URL opened: https://arxiv.org/abs/1911.07567 (arXiv record) and https://arxiv.org/pdf/1911.07567v2 (PDF).
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: The paper reviews 23 professional audits by Trail of Bits with 246 findings. Of the audited code bases, 14 had considerable unit tests, 2 moderate, 2 modest, 3 weak and 2 none. Mean findings per audit were almost the same at every level: 11.1, 10.5, 11.5 and 11. The rank correlation (Kendall τ) between unit-test quantity and findings was 0.09 (p = 0.61), and it pointed the wrong way. The authors conclude that even extensive unit tests do not prevent the flaws that audits find. 37% of all findings, and 63% of high-severity, low-difficulty findings, could plausibly be caught with user-defined properties.

### Barboni2021-SuMo SuMo: A Mutation Testing Strategy for Solidity Smart Contracts
- Authors: Morena Barboni, Andrea Morichetta, Andrea Polini; Year: 2021; Venue: AST 2021, DOI 10.1109/AST52587.2021.00014 (per Semantic Scholar). The extended version is "SuMo: A mutation testing approach and tool for the Ethereum blockchain", Journal of Systems and Software 2022, DOI 10.1016/j.jss.2022.111445 (Crossref; I saw no abstract).
- URL opened: https://arxiv.org/abs/2105.03626 (arXiv record of the 2021 version).
- Status: VERIFIED (2021 version; for the 2022 journal version, only the metadata was seen)
- Tier: C
- Touches: N2
- Summary: SuMo has 44 Solidity mutation operators. A first run on open-source projects with test suites was called encouraging. A repository record of the 2022 journal version, seen only in a search snippet, reports that the test suites shipped with the studied applications repeatedly scored low on mutation [not opened; uncertain].

### Hartel2020-MutationAtScale Mutation testing of smart contracts at scale
- Authors: Pieter Hartel, Richard Schumi; Year: 2020; Venue: Tests and Proofs (TAP 2020, at STAF), LNCS, DOI 10.1007/978-3-030-50995-8_2 (Crossref and Semantic Scholar).
- URL opened: https://arxiv.org/abs/1909.12563 (arXiv record) and https://arxiv.org/pdf/1909.12563v4 (PDF).
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: The authors generated 71,314 mutants of real contracts, of which 47,870 were usable. Each of the 963 contracts was tested by replaying 50 past transactions; these are not test suites written by developers. 64.4% of the mutants survived. The paper adds a killing condition based on gas use.

### Jain2023-MindTheGap Mind the Gap: The Difference Between Coverage and Mutation Score Can Guide Testing Efforts
- Authors: Kush Jain et al.; Year: 2023; Venue: ISSRE 2023, DOI 10.1109/ISSRE59848.2023.00036 (Crossref).
- URL opened: https://arxiv.org/abs/2309.02395 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: Code that is covered by tests but has a low mutation score is run by the tests without being checked; the authors call this difference the "oracle gap". They measure it on Maven projects and in a small study of well-tested blockchain projects, and use it to find files where weak assertions guard important code.

### Bouafif2025-PRIMG PRIMG : Efficient LLM-driven Test Generation Using Mutant Prioritization
- Authors: Mohamed Salah Bouafif et al.; Year: 2025; Venue: EASE 2025 (per Semantic Scholar, DOI 10.1145/3756681.3756991).
- URL opened: https://arxiv.org/abs/2505.05584 (arXiv record).
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: A model ranks the surviving mutants, and an LLM writes and refines Solidity tests that kill them. On real Code4rena projects this gives smaller suites with high mutation coverage.

### Hao2023-SmartCoCo SmartCoCo: Checking Comment-code Inconsistency in Smart Contracts via Constraint Propagation and Binding
- Authors: Sicheng Hao, Yuhong Nan, Zibin Zheng, Xiaohui Liu; Year: 2023; Venue: ASE 2023, DOI 10.1109/ASE56229.2023.00142 (Crossref).
- URL opened: https://www.se.cs.uni-saarland.de/conferences/ASE/ase2023/details/ase-2023/ase-2023-papers/127/SmartCoCo-Checking-Comment-code-Inconsistency-in-Smart-Contracts-via-Constraint-Prop.html (ASE 2023 programme page with the abstract) and the Crossref record.
- Status: VERIFIED
- Tier: C
- Touches: N2, N4
- Summary: The tool checks comments about roles, parameters and events, which can matter for security. On 101,780 unique Ethereum contracts it reported 4,732 inconsistencies in 1,745 contracts. Precision was over 79% on 439 hand-labelled cases, at 2.64 seconds per contract.

### Zhang2026-SmartComment Detecting Code-Comment Inconsistencies in Smart Contracts by Combining LLM and Program Analysis
- Authors: Jiashuo Zhang et al.; Year: 2026; Venue: Proceedings of the ACM on Software Engineering (FSE 2026), DOI 10.1145/3808112.
- URL opened: https://api.crossref.org/works?query.bibliographic=Detecting+Code-Comment+Inconsistencies+in+Smart+Contracts (Crossref record with the publisher's abstract).
- Status: VERIFIED
- Tier: C
- Touches: N2, N4
- Summary: An LLM plays the roles of code reviewer and developer, helped by program analysis, to find places where a comment and the code disagree. On 1,000 real contracts it found 203 valid inconsistencies at 79.9% precision. It found over 90% of the inconsistencies that earlier tools missed. Program analysis raised the F1 score from 58.7% to 81.3%.

## Gaps this search could not fill

- No study gives the share of Solidity fix commits, or of audit-fix pull requests, that change or delete existing tests. The closest number is the indexed Wang et al. 2023 result: 92% of 6,146 Solidity bug fixes touch JavaScript, TypeScript or Python files, which include tests, but test files are not counted separately.
- No study measures how AI coding agents treat an existing repository test that asserts a vulnerability during a security repair. The nearest are the indexed ImpossibleBench and SpecGuard papers (tests deliberately made to conflict with the specification), Mathews2024 (tools keep tests that confirm bugs), Li2026 (feedback toward passing weakens assertions) and Ebrahimi2026 (passing patches keep old code behind guards).
- No empirical study of Foundry or Hardhat test suites in audited DeFi protocols, or of test adequacy in Code4rena or Sherlock codebases, was found. Groce2020 (23 audits) is the only link between test effort and audit findings that I found.

## Leads not followed

- Zaidman et al., "Studying the co-evolution of production and test code in open source and industrial developer test processes through repository mining" (Empirical Software Engineering 2011; ICST 2008 version). Seen in query 12 results; not opened.
- Daniel et al., ReAssert, which suggests repairs for broken unit tests. Seen in query 9 results (Illinois IDEALS PDF); not opened.
- Kash et al. 2021, a replication study on which refactorings break tests. Seen in query 9 results (USI PDF); not opened.
- Shamshiri et al., "Do Automatically Generated Unit Tests Find Real Faults? An Empirical Study of Effectiveness and Challenges" (ASE 2015). Seen in query 47; not opened.
- A Meta study reported in the UTFix abstract: 14% to 22% of failures come from outdated tests. The original was not found.
- Hossain et al., "Neural-Based Test Oracle Generation: A Large-scale Evaluation and Lessons Learned" (arXiv 2307.16023), and Bodicoat et al., "Understanding LLM-Driven Test Oracle Generation" (AIware 2025, arXiv 2601.05542). Seen in query 39; judged marginal.
- Molina, Gorla (and d'Amorim), "Test Oracle Automation in the Era of LLMs" (arXiv 2405.12766; TOSEM 2025, DOI 10.1145/3715107). Seen in queries 1 and 39; a position paper.
- Hossain, Taylor, Dwyer, "Doc2OracLL: Investigating the Impact of Documentation on LLM-based Test Oracle Generation" (arXiv 2412.09360). Seen in query 39.
- Liang et al. 2026, "Auditing and Decomposing Feedback-Driven Evolution in LLM Test Generation under the Oracle Problem" (arXiv 2608.19626). Seen in query 59; judged marginal.
- LLMPROPHET, "From Implemented to Expected Behaviors: Leveraging Regression Oracles for Non-regression Fault Detection using LLMs" (ICST 2025 AIST workshop; JRC repository record JRC141000). Seen in query 53; not opened.
- A Czech thesis on short misleading comments as a black-box attack on code generation (CodeGen, CodeLlama, DeepSeek-Coder; HumanEval+, ClassEval). Record at invenio.nusl.cz/record/775216, seen in queries 23 and 28; not opened.
- HoarePrompt (arXiv 2503.19599), which gives a case of wrong LLM-generated expected outputs used as feedback. Seen in query 29.
- C4RLLaMA, "Code Comment Inconsistency Detection and Rectification Using a Large Language Model" (ICSE 2025), and Yichi Zhang, "Detecting code comment inconsistencies using LLM and program analysis" (FSE 2024 Companion). Seen in query 25 and in Thornton's references.
- Wen, Nagy, Bavota, Lanza, "A Large-Scale Empirical Study on Code-Comment Inconsistencies" (ICPC 2019). Crossref record seen in query 63, with no abstract.
- "The Silence of the Comments: Patterns and Pitfalls in Smart Contract Code Documentation" (SANER 2026 workshop) and "Towards Detecting Comment-Code Inconsistency in Smart Contract via Pre-Training Techniques" (SpaCCS 2024). Seen in query 44; not opened.
- Alchemist (Barboni et al., ICBC 2025 and AITest 2025), which generates mutant-killing Solidity tests with LLMs. Seen in queries 16 and 42; not opened.
- MuSe, a mutation testing plugin for the Remix IDE (arXiv 2603.23441). Seen in query 56.
- A Trail of Bits blog post on mutation testing with slither-mutate (18 September 2025). Seen in query 21; grey literature, not opened.
- A KAIST thesis, "Gap between theory and practice: an empirical study of security patches in Solidity". Seen in query 55; not opened.
- "Benchmarking LLM-Based Static Analysis for Secure Smart Contract Development" (arXiv 2605.11163), which reports variable names misleading detectors. Seen in query 69; this belongs to the N6 slice.
- Haque, Ingale, Csallner, "Do Autonomous Agents Contribute Test Code? A Study of Tests in Agentic Pull Requests" (arXiv 2601.03556). Verified in query 33; judged marginal.
- Le et al., "When names disappear: Revealing what LLMs actually understand about code" (arXiv 2510.03178), and TrojanPuzzle. Both in Thornton's reference list (query 27); not opened.
- Ahmed et al., "Is the Cure Still Worse Than the Disease?" (arXiv 2511.16858). Seen in query 46; probably the same work as the indexed "Investigating Test Overfitting on SWE-bench" [uncertain].
