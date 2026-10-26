# R3 T4. Task descriptions, contamination checks, LLM judges and differential testing

Search run on 2026-10-21 by the round-3 T4 bibliography agent. It follows the search protocol (`proposal_workspace/lit/search_protocol.md`) and the project brief (`proposal_workspace/lit/project_brief.md`). This round tests saturation. It used new wording, and it reports only tier A and B papers that are not in the benchmark index (`proposal_workspace/lit/master_index.tsv`, 770 papers when read).

## Queries run

Columns:
- *Hits looked at*: distinct papers or pages read in the result list. Several links to the same paper count once. Platform documentation and glossary pages count as zero.
- *Already seen*: in the index, or named in an earlier round's file.
- *New A/B*: relevant papers not seen before that got a block below. A paper found by several rows is counted in the first row only.

| # | Query | Source | Hits looked at | Already seen | New A/B | Notes |
|---|---|---|---|---|---|---|
| 1 | all:"task description" AND all:leakage AND all:code | arXiv API | 1 | 0 | 0 | one off-topic hit (prompt extraction, 2408.02416) |
| 2 | memorization probe code completion verbatim training data | Semantic Scholar API | 30 | 0 | 0 | all C (privacy memorization: Unveiling Memorization in Code Models, code membership inference, credential memorization); 10 other S2 queries got HTTP 429 |
| 3 | ten queries: task description leakage code generation benchmark; prompt specificity vulnerability rate LLM generated code; underspecified requirements secure code generation LLM; issue description quality coding agent success rate; contamination detection code language models benchmark; LLM judge vulnerability report validation; LLM auditor false positives smart contract; differential fuzzing smart contracts; equivalence checking LLM generated code reference implementation; semantic equivalence smart contract versions | Semantic Scholar API | 0 | 0 | 0 | HTTP 429 on every retry; three were retried later (rows 46 to 48) |
| 4 | task description leakage code benchmark solution hints in problem statement LLM evaluation | WebSearch | 6 | 3 | 0 | new but C: 2410.16292 (Codewars leakage), 2606.05037 (validator messages leak fix) |
| 5 | prompt specificity vulnerability rate LLM generated code study | WebSearch | 6 | 2 | 1 | Minimal Prompt Perturbations (2605.29737) B; C: SecureForge 2605.08382, 2507.10054 |
| 6 | underspecified requirements secure code generation LLM implicit security requirements | WebSearch | 9 | 3 | 2 | Unsaid Unsafe RTL (2608.26588) B; Poster Real-World Risk Scenarios (2607.23088) B; C: 2504.20612 |
| 7 | issue description quality effect on coding agent success SWE-bench underspecified issues | WebSearch | 8 | 4 | 1 | Ambig-SWE (2502.13069, ICLR 2026) B |
| 8 | memorization probe code completion verbatim reproduction benchmark LLM code model | WebSearch | 1 | 1 | 0 | only The SWE-Bench Illusion (indexed), 9 links to it |
| 9 | contamination detection code LLM 2026 benchmark leakage software engineering | WebSearch | 3 | 1 | 0 | Cross-Context Verification (screened C in r2); C: GEM 2026 contamination review; Poisoned Chalice competition report |
| 10 | LLM judge vulnerability report validation agreement with security experts | WebSearch | 7 | 1 | 0 | C: bug-bounty invalid reports 2511.18608; VA report validation review 2505.04265; grey: Giskard, ISGroup, promptfoo; SoK 2603.29403 screened C in r2 |
| 11 | LLM auditor false positives smart contract audit evaluation real findings | WebSearch | 7 | 5 | 0 | Logic Meets Magic and ToB blog screened C in r2; C: AuditGPT 2404.04306, CTFBench post |
| 12 | differential fuzzing smart contract; differential testing smart contract; prompt sensitivity code generation | DBLP API | 0 | 0 | 0 | DBLP returned a bot-check page instead of results |
| 13 | all:equivalence AND all:LLM AND all:generated AND all:code AND all:reference | arXiv API | 21 | 1 | 0 | C: MintEval 2610.03080 (behavioural equivalence vs reference, trading code); FEAgent 2610.04371; Functional Memorization 2606.12764; SrDetection 2606.29815 |
| 14 | semantic equivalence smart contract versions upgrade | OpenAlex API | 0 | 0 | 0 | HTTP 429, anonymous budget at zero |
| 15 | abs:"security-neutral" OR abs:"security-agnostic prompt" OR abs:"without mentioning security" | arXiv API | 0 | 0 | 0 | no hits |
| 16 | differential fuzzing smart contracts two implementations same function Solidity | WebSearch | 6 | 0 | 1 | Diffusc (Trail of Bits blog, grey) B; C: EVMFuzz 1903.08483, Solidity miscompilation 2607.07217, Echidna, Beacon Fuzz |
| 17 | semantic equivalence smart contract versions upgrade differential analysis paper | WebSearch | 6 | 0 | 0 | C: USCSA 2512.08372, history-version comparison 2010.02509, Certora Concord (governance posts), Myth of Immutability 2504.02719 |
| 18 | equivalence checking LLM-generated code against reference implementation differential testing study | WebSearch | 3 | 0 | 1 | Dristi and Dwyer 2602.15761 B; C: PROBEGEN 2502.18473, CINDER thesis |
| 19 | LLM-generated Solidity compared with human-written reference contract fuzzing behavioral differences | WebSearch | 7 | 3 | 0 | C: LLM4Fuzz 2401.11108, Human Side of SC Fuzzing 2506.07389, FuzzLGen poster; Logic Meets Magic screened C in r2 |
| 20 | "security-neutral" prompts code generation LLM vulnerabilities functional prompt only | WebSearch | 6 | 3 | 0 | GoodVibe, PromSec indexed; How Secure is Secure Code Generation screened in r2; Minimal Prompt Perturbations already counted (row 5); C: 2608.30025 |
| 21 | benchmark task description hints function signature leak implementation repository-level code generation evaluation bias | WebSearch | 7 | 2 | 0 | C: Mouselinos et al. hint-removal bias probe (ACL Findings 2023, 2211.00609), LessLeak-Bench 2502.06215, WybeCoder 2603.29088, PythonSaga 2401.03855, PrivCode++ |
| 22 | multi-LLM consensus voting vulnerability detection smart contract cross-model agreement false positives | WebSearch | 7 | 4 | 0 | LogicScan, LLM-BSCVM, GPTLens indexed; LLM-SmartAudit screened C in r2; C: LLMBugScanner 2512.02069, TU Delft thesis, Reddit vendor post |
| 23 | LLM vulnerability findings validated proof-of-concept exploit execution reduce false positives agent audit | WebSearch | 8 | 2 | 1 | Antiproof 2607.12316 B; VulnRepairEval indexed; PoC-Gym already in r2_S1; C: SAST-Genius 2509.15433, monetizing exploits 2505.11449, web PoC study 2510.10148 |
| 24 | LLM-as-a-judge security code review agreement human experts Cohen kappa vulnerability assessment study 2026 | WebSearch | 8 | 4 | 0 | CoV-Eval/VC-Judge, Insight into Security Code Review, LLM-as-judge for code gen indexed; C: ProjDevBench, 2603.22214, code-review curation 2607.09524 and 2502.03425 |
| 25 | knowledge cutoff time-split evaluation vulnerability detection LLM post-cutoff CVEs memorization smart contract exploits | WebSearch | 6 | 2 | 0 | JavaVulBench and Should-We-Evaluate-on-Open-Source indexed; C: CWE-Trace 2606.20502 (contamination gave no advantage), VulnSage 2503.17885, patch localization 2509.15777 |
| 26 | all:underspecified AND all:security AND all:code | arXiv API | 8 | 1 | 0 | Usability as a Weapon indexed; rest off-topic (repository poisoning, prompt injection, RPKI) |
| 27 | self-preference bias LLM judge AI-generated code versus human-written code evaluation | WebSearch | 5 | 2 | 0 | Panickssery et al. (self-preference) and LLM-as-judge for code indexed; C: Comparing Developer and LLM Biases 2603.24586; hiring study off-topic |
| 28 | feature request wording steers coding agent to introduce vulnerability security not mentioned in prompt agent study | WebSearch | 4 | 2 | 0 | SusVibes and SecureVibeBench indexed; C (grey): DryRun Security report via Help Net Security |
| 29 | secure code benchmark prompt mentions CWE leaks vulnerability hint evaluation validity critique | WebSearch | 8 | 4 | 1 | Rethinking CyberSecEval 2411.08813 B; SecCodePLT, SecCodeBench-V2, CWEval indexed; Reflexion screened in r2; C: Appen report, AlquistCoder VulnBench, 2602.15485 |
| 30 | LLM Solidity smart contract translation equivalence testing differential execution generated contract versus original | WebSearch | 5 | 1 | 1 | Certora Concordance blog (LLM rewrite checked by Concord equivalence checker, grey) B; SolMover indexed; C: OpDiffer 2504.12034 (ISSTA 2025, EVM clients), Black Hat Asia 2026 slides, LinkedIn post |
| 31 | LLM memorized smart contract audit reports Code4rena findings contamination knowledge cutoff evaluation | WebSearch | 6 | 2 | 0 | GiAnt indexed; LLM-SmartAudit screened C in r2; C: FTSmartAudit 2410.13918, Decoupled SC Audits 2606.03128, SCALM 2502.04347, HackerNoon post |
| 32 | consistency of LLM security code review across repeated runs and different models nondeterminism vulnerability findings | WebSearch | 1 | 0 | 1 | Snyk VulnBench JS 1.0 (2606.15762) B; other links are the same study |
| 33 | all:"issue description" AND all:agent AND all:quality | arXiv API | 9 | 3 | 0 | C: REAgent 2604.06861, SWE-Fuse 2603.07927, Automated Benchmark Generation 2503.07701, SWE-Tester, SWE-Bench ProMax |
| 34 | smart contract generation LLM natural language requirements ambiguity security requirements omitted vulnerabilities study | WebSearch | 6 | 6 | 0 | all indexed (SmartEval, Vulnerability Landscape, Efficacy of Various LLMs, Hyperledger case study, Vella GeCoIn, formal-specification comparison) |
| 35 | vulnerability repair benchmark data leakage LLM memorized fix commit CVE patch contamination study | WebSearch | 8 | 6 | 0 | PatchBench, Learned or Memorized, Why LLMs Fail, Invisible Hands indexed; AgenticRepair, MemRepair, KeaRepair screened C in r2; C: MultiFixer 2607.26591 |
| 36 | rephrased issue statements SWE-bench paraphrase robustness coding agent performance sensitivity to problem statement wording | WebSearch | 3 | 1 | 1 | RealSWE 2608.27831 B; UTBoost indexed; rest grey (Cognition report, glossaries) |
| 37 | LLM judge audit contest submissions validity severity Code4rena Sherlock judging automated agreement with human judges | WebSearch | 0 | 0 | 0 | only platform documentation (Code4rena judging criteria, Sherlock scoring); no study of LLM judging of contest findings |
| 38 | security review of AI agent pull requests compared with human pull requests LLM reviewer vulnerabilities empirical 2026 | WebSearch | 2 | 2 | 0 | both indexed (Agentic PRs on GitHub 2601.00477; Security-Related AI PRs, EASE 2026) |
| 39 | differential testing human-written versus LLM-generated implementation same function behavioral divergence hidden bugs study | WebSearch | 4 | 1 | 0 | PatchDiff (Are Solved Issues Really Solved) indexed; C: TrickCatcher 2404.10304, DiffSpec 2410.04249, Differential Prompting 2304.11686 |
| 40 | LLM filtering Slither static analysis warnings smart contract false positive triage evaluation against manual labels | WebSearch | 3 | 1 | 0 | GPTLens (New Perspectives) indexed; C: Reentrancy Detection in the Age of LLMs 2603.26497, SmartLLM 2502.13167; rest are practitioner pages |
| 41 | inter-model agreement two LLMs reviewing same code for vulnerabilities Fleiss kappa disagreement security findings | WebSearch | 6 | 2 | 0 | Snyk VulnBench JS already counted (row 32); Insight into Security Code Review and To Err is Machine indexed; C: inter-model consensus 2411.16797, assurance-case judges 2511.02203, architecture-decision LLMs 2602.07609 |
| 42 | contamination-free smart contract vulnerability benchmark post-cutoff exploits temporal holdout LLM agents 2026 | WebSearch | 3 | 3 | 0 | all indexed: Re-Evaluating EVMbench (post-release incidents), EVMbench, CyberChainBench |
| 43 | all:"LLM-as-a-judge" AND all:vulnerability | arXiv API | 40 | 5 | 0 | indexed: Correct Verdicts Flawed Reasoning, GiAnt, Turning Bias into Bugs; SoK 2603.29403 and Everything You Wanted to Know screened in r2; rest are general judge-robustness papers (C or off-topic) |
| 44 | all:contamination AND all:"smart contract" | arXiv API | 5 | 2 | 0 | Re-Evaluating EVMbench and DMind indexed; rest off-topic |
| 45 | all:differential AND all:"smart contract" AND all:fuzzing | arXiv API | 4 | 2 | 0 | SolBehave (LLM Solidity vs reference behaviour) and smart-contract generation benchmark 2503.01098 indexed; C: EVMFuzz, Solidity miscompilation study |
| 46 | LLM judge vulnerability report validation (retry) | Semantic Scholar API | 0 | 0 | 0 | HTTP 429 |
| 47 | differential fuzzing smart contracts (retry) | Semantic Scholar API | 30 | 3 | 1 | Mukherjee et al., LLM-guided Solidity migration with equivalence checking (ICSOFT 2026) B; Midas, SolBehave, smart-contract generation benchmark 2503.01098 indexed; rest are smart-contract fuzzers (C), e.g. EVMFuzzer, ContractFuzzer, Uncovering SC VM Bugs via Differential Fuzzing, GasZero |
| 48 | task description leakage code generation benchmark (retry) | Semantic Scholar API | 0 | 0 | 0 | HTTP 429 |
| 49 | human auditors validate LLM smart contract audit findings expert evaluation precision of AI audit reports study | WebSearch | 2 | 0 | 0 | C: Co-Auditing with GPT-4 code interpreter 2406.18075 (two Quantstamp auditors checked outputs), SmartAuditFlow 2505.15242 |
| 50 | function names docstrings comments cue insecure code generation LLM identifier names steer vulnerabilities study | WebSearch | 7 | 4 | 0 | SALLM, LLMSecEval, CWEval indexed; How Secure is Secure Code Generation screened in r2; C: docstring reformulation (EACL SRW 2024), SLR 2412.15004, Ocassionally Secure 2402.00689 (named in round 1) |
| 51 | LLM smart contract migration or translation semantic equivalence checking counterexample differential fuzzing symbolic execution EVM bytecode | WebSearch | 7 | 1 | 0 | EF/CF indexed; C: Foundational Refinement Proofs for Deployed Bytecode 2607.26306, LLAMA 2507.12084, Bug Searching in Smart Contract 1905.00799, Coq EVM block equivalence (CAV 2023), hevm tool page |
| 52 | LLM Solidity gas optimization rewrite verified equivalent original contract neuro-symbolic | WebSearch | 6 | 4 | 0 | GiAnt and optimized Solidity for ML models indexed; GasAgent named in an earlier round; Concordance already counted (row 30); C: 2509.23976, PolyU GPT-4 gas study |
| 53 | hevm fast symbolic execution framework EVM bytecode equivalence checking two contracts CAV 2024 | WebSearch | 3 | 0 | 0 | hevm repository (tool with equivalence checking), Formally Verified EVM Block-Optimizations (CAV 2023), Albert et al. extended version: all C; no hevm paper found |
| 54 | coding agents underspecified task description security clarifying question vulnerability insecure assumptions 2026 study | WebSearch | 3 | 1 | 0 | Ambig-SWE already counted (row 7); C: Ask or Assume? 2603.26233, UnderSpecBench 2607.02294 (agent action boundaries, not code security) |
| 55 | LLM triage exploitability vulnerability reports agreement with human security analysts evaluation 2026 false positive judge | WebSearch | 1 | 0 | 0 | C (grey): Elastic Security Labs post, triage agent agrees with engineers on 85% of 764 bug-bounty reports |
| 56 | coding agent benchmark tasks created after model training cutoff contamination time-split security vulnerabilities 2026 | WebSearch | 7 | 2 | 0 | SecureVibeBench indexed; KEX-bench screened in r2; C: RustMizan 2607.04729, contamination taxonomy 2608.29463, poisoned benchmarks 2609.17817, WorkBuddy Bench and N-Day-Bench (blog summaries) |
| 57 | all:equivalence AND all:Solidity | arXiv API | 40 | 0 | 0 | arXiv stemming matched 'solid', so most hits are physics; C: semantic clones of Solidity functions 2604.26526, IDOL compiler testing 2506.12760 |

## How the search was run

The topic has four parts:
- (a) how task descriptions in code benchmarks are written, whether they leak or steer the solution, and how prompt wording changes the security of generated code;
- (b) memorization and contamination probes for code models, and time-split evaluation;
- (c) LLM-as-a-judge and multi-LLM review for vulnerabilities or audits, and agreement with human experts;
- (d) differential testing, differential fuzzing or equivalence checking between two implementations of the same smart-contract function, or between LLM code and a reference.

The search worked as follows.
- Sources: WebSearch, the arXiv API and the Semantic Scholar API. No email address, name or other personal identifier was sent. Requests carried only a generic user-agent string.
- Three sources were partly or fully unavailable. The DBLP API returned a bot-check page instead of results. OpenAlex returned HTTP 429 with its anonymous budget at zero. Semantic Scholar returned HTTP 429 for 12 of 14 requests, so only two Semantic Scholar queries gave results. The arXiv API was slow and also returned HTTP 429 at times, so its failed queries were rerun later (rows 43 to 45).
- Every title was compared with the title column of the benchmark index, after removing case and punctuation, with a near-match check and a check on the first six words. It was also compared with the text of every round-1 and round-2 file and of the round-3 file `r3_T3_repair_execution.md`. A paper named in an earlier round's file counts as already seen, even if it never reached the index. When an earlier round screened a paper and put it at tier C, this round kept that decision.
- Tiers follow the brief and the bar used in round 2. General papers on the reliability of LLM judges, general contamination detection, and LLM smart-contract detectors tested on labelled datasets are tier C.
- Only tier A and B papers get a block. Tier C papers that were read are named in the *Notes* column of the queries table and in the short list after the blocks.

## Result in brief

- 57 rows, covering 68 query attempts. 52 queries returned results; 16 attempts failed (rows 3, 12, 14, 46 and 48). About 400 hits were looked at, and about 100 of them were already seen.
- 12 new tier B papers. No new tier A paper.
- By part of the topic: (a) task descriptions and prompt wording gave 6 new papers; (b) contamination and time-split evaluation gave none; (c) LLM review and judges gave 2; (d) differential testing and equivalence checking gave 4.
- Saturation: of the 21 rows after row 36, only row 47 gave a new paper. Row 47 was a Semantic Scholar retry that ran in the background while rows 34 to 50 were being run. The seven queries run after every background query had returned (rows 51 to 57) gave nothing new.
- Part (b) looks saturated: every relevant contamination or time-split paper that came up was already in the index or had been screened in round 2. Part (d) was the least covered before this round. The index held SolBehave, which compares LLM-written Solidity function bodies with the originals by differential fuzzing, and Midas, which uses differential analysis to find profitable exploits. It held no ready tool for differential fuzzing between two Solidity implementations, and no equivalence checker for two versions of a contract.

## New entries: (a) task descriptions and prompt wording

### Kim2026-RealSWE RealSWE: A Compositional Evaluation of Coding Agents under Realistic User Requests
- Authors: Gyuhyeong Kim et al. (with Hyojung Gwon, Jeonghyeon Kim, Kyuhong Shim, Sunjae Lee); Year: 2026; Venue: arXiv preprint (arXiv:2608.27831; v1 28 Aug 2026, v3 5 Oct 2026)
- URL opened: https://arxiv.org/abs/2608.27831 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: The paper compares real requests that users give coding agents (from SWE-chat) with SWE-bench Verified and Pro problems. It uses a six-category taxonomy of what a request states and four dimensions of writing style. Requests that hold only a problem statement, alone or with little context, are 88% of real prompts but 7% of benchmark problems, and 87% of real prompts are casual while 94% of benchmark problems are formal. RealSWE has 381 task families whose variants share the task and the gold patch but differ in what they state and how; across seven LLMs, realistic inputs lower the resolution rate by 6.4 points on average and can change model rankings, and stating the desired behaviour and the motivation matters most.
- Delta: RealSWE keeps the task and the gold patch fixed, varies what the request states, and measures the effect on functional resolution. It has no security tasks, and it does not ask whether a request hints at a bug or at its fix. The project keeps the task and the starting code fixed and varies whether the request describes the human's design or states the rule that the fix restores; its judge is an exploit, and it compares the agent with the human who wrote the same function. RealSWE's finding that a statement of desired behaviour helps most matches the pilot, where 12 of 15 runs avoided the bug when the request stated the rule. Its taxonomy gives the project a published way to describe what each feature request contains.

### Hariharan2024-RethinkingCyberSecEval Rethinking CyberSecEval: An LLM-Aided Approach to Evaluation Critique
- Authors: Suhas Hariharan et al. (with Zainab Ali Majid, Jaime Raldua Veuthey, Jacob Haimes); Year: 2024; Venue: arXiv preprint (arXiv:2411.08813, v1 13 Nov 2024). The arXiv comment reads "NeurIPS 2024, 2 pages", which points to a NeurIPS 2024 workshop [uncertain which one].
- URL opened: https://arxiv.org/abs/2411.08813 (arXiv abstract page); https://arxiv.org/html/2411.08813v1 (full text)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: The paper critiques the insecure-code part of Meta's CyberSecEval. Many Autocomplete prompts contain identifiers or comments that hint at an insecure practice. The authors used GPT-4o to strip them, checked 50 rewrites by hand, and found that the share of code marked secure rose by 12.2 to 22.2 percentage points per model, 17.7 points overall. In the Instruct set, 23.5% of prompts could not be met without breaking the static-analysis rules, and removing those prompts raised the secure share by 8.3 to 13.1 points.
- Delta: This is direct evidence that cue words in a security benchmark's prompts change the measured security, and it uses an LLM to find and remove the cues. That is close to the check the project needs for its own feature requests. The paper works on short completions judged by static-analysis rules, with no agents, no executable exploit and no human baseline. The project asks for whole Solidity functions in a real repository and judges them with a PoV, and the cue it must avoid is a hint at one specific audited bug or at its fix, not a generic insecure practice. The pilot's result that a request describing the human's design led all 13 compiled runs to write the bug is the same effect, seen in the project's setting.

### Sternfeld2026-PromptFragility Minimal Prompt Perturbations Lead to Code Vulnerabilities: Prompt Fragility and Hidden-State Signals in Coding LLMs
- Authors: Alexander Sternfeld et al. (with Andrei Kucharavy, Ljiljana Dolamic); Year: 2026; Venue: arXiv preprint (arXiv:2605.29737, v1 28 May 2026)
- URL opened: https://arxiv.org/abs/2605.29737 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: Earlier work showed that small prompt changes lower functional correctness; this paper asks whether they also change security. It applies token-level mutations to prompts across three models and five programming languages, and finds that a change as small as one character can turn secure generated code into vulnerable code. Probes on the models' hidden states predict input-handling flaws (mean AUC 0.753) better than flaws that come from one insecure default choice (mean AUC 0.674).
- Delta: The paper measures how much the security of generated code depends on trivial wording, on function-level prompts, and it looks inside the model. The project does not vary wording, and its pilot ran each request once per setup. The paper's result means that a near-identical wording of a feature request could reverse an outcome, so the project should run several paraphrases of each request that keep the same content and report whether the agent-versus-human result holds across them. The project's tasks are repository-level Solidity functions judged by an executable exploit and compared with the human's code; the paper has none of these.

### Yang2026-UnsaidUnsafe Unsaid, Unsafe? Implicit Security Obligations in LLM-Based RTL Code Generation
- Authors: Guang Yang et al. (with Xing Hu, Xiang Chen, Xin Xia); Year: 2026; Venue: arXiv preprint (arXiv:2608.26588, v1 27 Aug 2026; arXiv comment "Under Review")
- URL opened: https://arxiv.org/abs/2608.26588 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: SECRTL-GEN has 392 hardware-design tasks over five CWE families and four languages (Verilog, SystemVerilog, VHDL and Python), each with black-box functional and security testbenches. The functional specifications leave out the security obligations on purpose, as real functional documents often do. Under plain prompts, five frontier LLMs pass the functional tests in about 73 to 79% of cases but the security tests in only 14 to 35%; adding CWE knowledge raises security, and security-oriented prompts lower functional pass rates. The proposed RTL-Obliger infers the missing obligations from the specification and raises the mean rate of passing both kinds of test to 61.6%, against 49.6 to 51.4% for the baselines.
- Delta: The design principle matches the project's: the request states the function but not the security rule, and an executable security test judges the result. The paper builds its tasks from CWE families on hardware IP, and it has no human baseline, no control group, and no check that the specification does not hint at the fix. The project takes its tasks from accepted audit findings in real Solidity repositories, compares the agent with the human who wrote the same function, and checks its requests for hints. The paper's trade-off, where naming the weakness raises security but lowers functional pass rates, is the trade-off the project's two request versions (describe the design, or state the rule) would show.

### Ma2026-RiskScenarios Poster: Rethinking Security in LLM Code Generation through Real-World Risk Scenarios
- Authors: Lixun Ma et al. (with Ruolong Ma, Bei Wang, Feng Wei, Zhenguang Liu, Lorenzo Cavallaro, Wentao Chen); Year: 2026; Venue: arXiv preprint (arXiv:2607.23088, v1 25 Jul 2026). The title marks it as a poster, but the page names no venue [uncertain].
- URL opened: https://arxiv.org/abs/2607.23088 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: Most secure-coding benchmarks state the security requirement in the prompt. This poster builds prompts for three situations that lead to insecure code in practice: ambiguous requirements, missing information about the operating context, and a conflict between security and functionality. On 2,700 test cases, all eight LLMs tested have average vulnerability rates above 56% across the three situations, and security-aware prompting lowers the risk by up to 45%.
- Delta: The paper shows that vulnerability rates are high when the prompt is silent or vague about security, which is the condition the project's feature requests create on purpose. It uses synthetic function-level cases, and the abstract does not say how vulnerabilities are judged. The project uses real audited functions, an executable exploit as judge, the human's code as the comparison point, and a check that the request does not hint at the bug or the fix. The paper has no such check and no human baseline.

### Vijayvargiya2026-AmbigSWE Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering
- Authors: Sanidhya Vijayvargiya et al. (with Xuhui Zhou, Akhila Yerukola, Maarten Sap, Graham Neubig); Year: 2026 (v1 18 Feb 2025, v3 21 Feb 2026); Venue: ICLR 2026, per the arXiv comment "Accepted at ICLR 2026"
- URL opened: https://arxiv.org/abs/2502.13069 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: The paper builds Ambig-SWE, a version of SWE-bench Verified whose issue texts leave out information the agent needs. It tests agents on three steps: noticing that a request is underspecified, asking targeted questions, and using the answers. Models struggle to tell well-specified requests from underspecified ones, but when they do interact on underspecified inputs, performance rises by up to 74% over the setting without interaction.
- Delta: Ambig-SWE removes information from the task text and measures what agents lose and what they recover by asking. The project's requests also leave something out on purpose: the security rule that the fix restores, so that the request does not hint at the fix. The project does not let agents ask questions, and it judges security with an exploit; Ambig-SWE judges functional resolution only and has no security tasks and no human baseline. Its way of building and checking underspecified variants of the same task is a precedent for the project's requests, which are written at a controlled level of detail.

## New entries: (c) LLM review and judges

### Tal2026-VulnBenchJS Snyk VulnBench JS 1.0: Can LLMs Find the Same Bugs Twice?
- Authors: Liran Tal et al. (with Johannes Kloos, Arsenii Rudich, Stephen Thoemmes, Manoj Nair; Snyk); Year: 2026; Venue: arXiv preprint (arXiv:2606.15762, v1 14 June 2026); vendor-authored
- URL opened: https://arxiv.org/abs/2606.15762 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: The authors ran 300 repeated vulnerability scans to measure how consistent an agentic LLM security review is on the same JavaScript code, prompt and harness. Findings that matched the Snyk Code reference were stable: 134 of 158 appeared in all five repetitions. Extra findings were not: across 250 model runs, 80 of 161 findings outside the reference appeared in only one of five identical repetitions, and only 22 appeared in all five. The authors conclude that LLM review and deterministic static analysis should be used together.
- Delta: The project's control group relies on an LLM security review, with two reviewers run on the agent's and the human's version, to find new flaws. This paper shows that the extra findings of one review run mostly do not repeat, so a difference between the agent's and the human's version seen in one run may be chance. That supports the project's rule that every reported flaw needs a confirming PoV. It also argues for several runs of each reviewer, because a flaw missed in one run may be reported in the next. The paper covers JavaScript web code, does not compare who wrote the code, and, as far as the abstract says, does not confirm findings by execution.

### Shakevsky2026-Antiproof Antiproof: Synthesizing Vulnerability Detectors and Proofs of Exploitability
- Authors: Alon Shakevsky et al. (with Corban Villa, Ion Stoica, Raluca Ada Popa); Year: 2026; Venue: arXiv preprint (arXiv:2607.12316, v1 14 July 2026)
- URL opened: https://arxiv.org/abs/2607.12316 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: Antiproof learns static detectors from vulnerability datasets to find candidates with high recall, then accepts a candidate only if an executable proof shows a concrete attacker capability. On BountyBench and the authors' KEVBench it detects 64 of 66 vulnerabilities, more than 60 percentage points more recall than static-analysis and neuro-symbolic baselines. A scan of 50 widely deployed systems found several hundred previously unknown vulnerabilities, with 12 CVEs assigned so far.
- Delta: Like the project, Antiproof accepts a finding only when an executable proof confirms it. Its aim is discovery at scale in web and AI-infrastructure software, and its candidates come from synthesized detectors, not from an LLM review. The project runs an LLM review on the agent's and the human's versions of the same Solidity functions, confirms each finding with a Foundry PoV, and compares the two authors; Antiproof has no comparison of authors, no control group and no smart contracts. It is a recent precedent for making an executable proof the bar for a finding, next to AnyPoC and SmartPoC, which are in the index.

## New entries: (d) differential testing and equivalence checking

### Dristi2026-DiffFuzzRefactor A Differential Fuzzing-Based Evaluation of Functional Equivalence in LLM-Generated Code Refactorings
- Authors: Simantika Bhattacharjee Dristi, Matthew B. Dwyer (University of Virginia); Year: 2026; Venue: LLMTrust 2026 workshop at FSE 2026 (seen on the FSE 2026 programme page); also arXiv:2602.15761 (v1 17 Feb 2026)
- URL opened: https://arxiv.org/abs/2602.15761 (arXiv abstract page); https://conf.researchr.org/details/fse-2026/llmtrust-2026-papers/9/A-Differential-Fuzzing-Based-Evaluation-of-Functional-Equivalence-in-LLM-Generated-Co (FSE 2026 programme page)
- Status: VERIFIED
- Tier: B
- Touches: N3, N6
- Summary: The paper uses differential fuzzing, running the original and the LLM-refactored code on thousands of generated inputs, to check whether refactorings keep behaviour. Across six LLMs (CodeLlama, Codestral, StarChat2, Qwen-2.5, Olmo-3 and GPT-4o), three datasets and two refactoring types, 19 to 35% of refactorings are not functionally equivalent. About 21% of the non-equivalent refactorings pass the datasets' existing test suites.
- Delta: This is differential testing of LLM code against a reference, and it shows that existing tests miss about a fifth of the behaviour changes. That supports the project's choice to judge repairs with held-out PoVs and not only with the tests the agent can see. The project judges agent code with an exploit, not with an equivalence check, because the agent's function is not expected to match the human's. Fuzzing the agent's repair against the human's fix, and reading the inputs where they differ, would be an extra judge for repairs. The paper uses small Python functions, with no security, no agents and no smart contracts; SolBehave (in the index) already applies differential fuzzing to LLM-written Solidity.

### Mukherjee2026-SolidityMigrationVerify Don't Just Translate: Verify - LLM-Guided Solidity Migration with Semantic Guarantees
- Authors: Arnab Mukherjee et al. (with Soumyadip Bandyopadhyay, Raju Halder, Dominique Blouin); Year: 2026; Venue: Proceedings of the 21st International Conference on Software Technologies (ICSOFT 2026), Volume 1, pp. 557-564, SciTePress, DOI 10.5220/0015195600004088
- URL opened: https://www.scitepress.org/DigitalLibrary/Link.aspx?doi=10.5220/0015195600004088 (publisher page with abstract)
- Status: VERIFIED (abstract read; the full text was not opened, so no numbers are given)
- Tier: B
- Touches: N3, N6
- Summary: Moving legacy contracts from Solidity 0.5.x to 0.8.x changes semantics, so an LLM translation may not keep the original behaviour. The paper proposes a closed loop: the LLM translates, the result is compiled, its bytecode is checked against the original with differential fuzzing and symbolic execution over EVM semantics, and any counterexample goes back to the LLM. The publisher page reports no quantitative results.
- Delta: This is differential fuzzing plus symbolic equivalence checking between LLM-written Solidity and a reference implementation at the bytecode level. The paper wants the two versions to be equivalent. The project expects the agent's function to differ from the human's and asks only whether it carries the exploitable flaw, which an exploit decides. A bytecode-level differential check like this one could list the inputs where the agent's version and the human's fixed version disagree, as a starting point for the security review of control functions and for checking repairs beyond the shown PoV. The paper has no security focus, no agents and no human baseline; SolBehave (in the index) covers the differential-fuzzing part with numbers.

### Bodell2023-Diffusc Differential fuzz testing upgradeable smart contracts with Diffusc
- Authors: William Bodell (Trail of Bits); Year: 2023 (7 July 2023); Venue: Trail of Bits blog (grey literature), with the open-source tool crytic/diffusc, now archived
- URL opened: https://blog.trailofbits.com/2023/07/07/differential-fuzz-testing-upgradeable-smart-contracts-with-diffusc/ (blog post)
- Status: VERIFIED
- Tier: B
- Touches: N1, N3, N6
- Summary: Diffusc compares two implementations of an upgradeable contract. It uses Slither to find new and changed functions by comparing their intermediate representation, and taint analysis to find unchanged code those changes can affect. It then writes Echidna harnesses that call the same function on both versions with the same inputs and assert that both succeed or fail together and return the same output. In the post's evaluation, taint analysis cut the Compound Comptroller functions to test from 69 to 38 (45%), and cross-contract analysis cut the Comp functions from 19 to 4 and the cToken functions from 78 to 16 (79% each).
- Delta: Diffusc is a ready tool for differential fuzzing between two Solidity implementations of the same functions, which is the comparison the project makes only through one PoV and an LLM review. It could run the agent's version of each control function against the human's version and show where they behave differently, which would point the security review at those places. It could also compare an agent's repair with the human's fix beyond the shown PoV. It was built for contract upgrades, uses no LLM, measures no exploit or loss, and expected differences such as revert messages would need filtering.

### Toman2025-Concordance Concordance: Automatically Simplifying Smart Contracts
- Authors: John Toman (Certora; editors Uri Kirstein and Ilya Leybovich); Year: 2025 (12 Sep 2025); Venue: Certora blog (grey literature); the tool is open source and described as pre-alpha
- URL opened: https://www.certora.com/blog/concordance-automatically-simplifying-smart-contracts (blog post)
- Status: VERIFIED
- Tier: B
- Touches: N1, N3, N6
- Summary: Concordance asks an LLM to rewrite complex, hand-optimised Solidity or assembly into simpler code with the same on-chain behaviour. Each rewrite is checked by Concord, Certora's equivalence checker built on the Certora Prover: it records storage changes, emitted logs, revert and return data, and external calls on every path of both versions and checks that they match, with gas left out. When they differ, the counterexample goes back to the LLM. The post reports no quantitative evaluation; in its example, Concord caught a rewrite of Solady's safeTransferFrom that reverted with empty data where the original reverted with TransferFromFailed().
- Delta: This is a working example of symbolic equivalence checking between LLM-written Solidity and a reference, with counterexamples. The project judges by exploit and does not check equivalence. Concord could show exactly where an agent's control function differs from the human's correct one, or where a repair differs from the human's fix, before the security review looks at those differences. Concordance has no security study, no human-written baseline and no evaluation, and real agent and human versions will differ in revert data, so the project would need a looser definition of equivalence.

## Tier C papers read (no block)

Read in this round and judged background only, mostly because they are general or outside the project's setting:
- (a): SecureForge (2605.08382), Explicit Vulnerability Generation (2507.10054), The Hidden Risks of LLM-Generated Web Application Code (2504.20612), Codewars leakage study (2410.16292), Self-Reflective APIs (2606.05037), Mouselinos et al. on biases that prompt cues cause in code generation (ACL Findings 2023, 2211.00609), Interpreting and Steering for Safe and Correct Code Generation (2608.30025), Ask or Assume? (2603.26233), UnderSpecBench (2607.02294), REAgent (2604.06861).
- (b): LessLeak-Bench (2502.06215), Detecting Functional Memorization in Code Language Models (2606.12764), SrDetection (2606.29815), CWE-Trace, "Calibration Without Comprehension" (2606.20502), RustMizan (2607.04729), Unveiling Memorization in Code Models (arXiv 2308.09932).
- (c): LLMBugScanner (2512.02069), Comparing Developer and LLM Biases in Code Evaluation (2603.24586), Co-Auditing Smart Contracts with GPT-4 Code Interpreter (2406.18075), bug-bounty invalid reports (2511.18608), Reliability and Fidelity of Automated Judgment Systems (2603.22214), SAST-Genius (2509.15433), Reentrancy Detection in the Age of LLMs (2603.26497), AuditGPT (2404.04306), Elastic Security Labs triage post.
- (d): PROBEGEN, "Disproving Program Equivalence with LLMs" (2502.18473), MintEval (2610.03080), FEAgent (2610.04371), USCSA (2512.08372), EVMFuzz (1903.08483), OpDiffer (ISSTA 2025, 2504.12034), Solidity miscompilation study (2607.07217), TrickCatcher (2404.10304), DiffSpec (2410.04249), LLM4Fuzz (2401.11108), Semantic Clones of Solidity Functions (2604.26526), Foundational Refinement Proofs for Deployed Bytecode (2607.26306).

## Leads not followed

- hevm, the EVM symbolic execution tool with an equivalence-checking mode that can compare two contracts (seen in rows 51 and 53 through its repository and tool page). A peer-reviewed paper on hevm may exist [uncertain]; none was found.
- Certora's Concord technical report, linked from the Concordance post (row 30); not opened.
- A GEM 2026 systematic review of contamination detection (aclanthology.org/2026.gem-main.50), seen in row 9; not opened.
- "The Poisoned Chalice of LLM Evaluation", a competition report on detecting prior exposure for software-engineering tasks (FSE-AIWare 2026), seen in row 9 only through a document mirror; the original was not found.
- An IEEE BigData 2025 paper on LLM-assisted review of bug-bounty reports (Stevens Institute research page), seen in row 10; not opened.
- CTFBench, a method for evaluating AI smart-contract auditors that weighs detection against false alarms (ethresear.ch post), seen in row 11; not opened.
- CINDER, a Vanderbilt thesis on differential and symbolic equivalence checking of LLM C-to-Rust translation, seen in row 18; not opened.
- BreachT5, a TU Delft thesis on a soft-voting ensemble for smart-contract detection, seen in row 22; not opened.
- RevisitVD, time-aware data splits for vulnerability detection (emergentmind topic page), seen in row 25; not opened.
- The DryRun Security report on Claude Code, Codex and Gemini building apps from specifications with no security guidance (Help Net Security article, March 2026), seen in row 28; the primary report was not opened.
- "Fortifying the Foundation", Black Hat Asia 2026 slides (i.blackhat.com, BHAS26-Ma), seen in row 30; topic and content not checked.
- Semantic Scholar results for the ten queries in row 3 and the two retries in rows 46 and 48, which all returned HTTP 429.
