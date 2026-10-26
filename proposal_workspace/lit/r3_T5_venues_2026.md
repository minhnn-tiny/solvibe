# Round 3, topic T5: 2026 accepted-paper lists, checked against the master index

Search date: 21 October 2026. All requests were anonymous. No email, name or other identifier was sent to any service.

## Queries run

One row per venue list. "Titles screened" counts the distinct titles on the list. For the small security lists (S&P, NDSS, USENIX Security) I read every title. For the larger lists I ran a broad keyword filter on the titles and read every title it flagged. For CCS 2026 and the five software-engineering lists I also skimmed the titles the filter missed that mention AI, LLMs, agents, code or contracts. "Relevant titles" counts titles that touch a T5 topic at any tier (A, B or C), including titles already in the master index (`master_index.tsv`); counts marked "~" are approximate. "Already indexed" counts list titles that match a title in the master index. "New relevant papers" counts tier A and B papers that are not in the master index and that earlier rounds did not already screen out.

| Venue list | URL | Titles screened | Relevant titles | Already indexed | New relevant papers |
|---|---|---|---|---|---|
| IEEE S&P 2026, both cycles (accepted list, cross-checked with the program) | https://sp2026.ieee-security.org/accepted-papers.html and https://sp2026.ieee-security.org/program.html | 254 (118 in cycle 1, 136 in cycle 2; all read) | 3 | 0 | 1 (A: SlicePatch) |
| NDSS 2026 | https://www.ndss-symposium.org/ndss2026/accepted-papers/ | 265 (all read) | 8 | 3 | 1 (B: Trust Me, I Know This Function) |
| NDSS 2027 | https://www.ndss-symposium.org/ndss2027/ (the home page links no accepted papers; /ndss2027/accepted-papers/ redirects to the NDSS 2017 list) | 0 | none | none | not online |
| USENIX Security 2026, all cycles (full program; the cycle 1 list has 165 papers, all in the program) | https://www.usenix.org/conference/usenixsecurity26/technical-sessions and https://www.usenix.org/conference/usenixsecurity26/cycle1-accepted-papers | 377 (all read) | 11 | 3 | 0 |
| ACM CCS 2026, both cycles | https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html | 482 | 12 | 4 | 1 (B: SKANF) |
| ICSE 2026 research track page (its program also shows papers of other tracks in the same sessions) | https://conf.researchr.org/track/icse-2026/icse-2026-research-track | 659 (322 research track) | ~40 | 19, plus 1 indexed under its arXiv title | 1 (B: When AI Takes the Wheel) |
| ICSE 2027 research track | https://conf.researchr.org/track/icse-2027/icse-2027-research-track | 0 | none | none | not online (notification was 20 October 2026; the page lists no papers yet) |
| FSE 2026 research papers page | https://conf.researchr.org/track/fse-2026/fse-2026-research-papers | 441 (211 research papers) | ~26 | 13 | 0 |
| ASE 2026 research track page | https://conf.researchr.org/track/ase-2026/ase-2026-research-track | 440 (263 research papers) | ~36 | 18 | 0 |
| ISSTA 2026 research papers | https://conf.researchr.org/track/issta-2026/issta-2026-research-papers | 210 | ~19 | 9 | 1 (B, unverified: RollGain) |
| MSR 2026 technical papers page | https://2026.msrconf.org/track/msr-2026-technical-papers | 157 (48 technical papers, 62 mining challenge papers, the rest from other tracks) | ~22 | 8 | 1 (B: Model See, Model Do?) |
| ICLR 2026 (orals and posters, from the conference site's data file; the OpenReview API returned a challenge page) | https://iclr.cc/static/virtual/data/iclr-2026-orals-posters.json | 5,468 (filter flagged 134) | ~13 | 7 | 0 |
| ICML 2026 (main and position-paper tracks) | https://icml.cc/static/virtual/data/icml-2026-orals-posters.json | 6,646 (filter flagged 182) | ~21 | 9 | 0 |
| NeurIPS 2026 (main track, Evaluations and Datasets track, position papers) | https://neurips.cc/static/virtual/data/neurips-2026-orals-posters.json | 6,243 (5,386 main, 717 Evaluations and Datasets, 56 position, 84 journal; filter flagged 190) | ~18 | 5 | 0 |
| ACL 2026 (long, short, Findings, industry, demo, student research) | https://aclanthology.org/events/acl-2026/ | 4,807 (filter flagged 194) | ~21 | 8 | 0 |
| EMNLP 2026 (main, Findings, industry, demo, TACL, CL; the Anthology has no EMNLP 2026 volumes yet, and the accepted-papers pages on 2026.emnlp.org return 404) | the program spreadsheet linked from https://2026.emnlp.org/program/ (read through its CSV export) | 5,611 (2,710 main, 2,487 Findings; filter flagged about 290) | ~25 | 6 | 1 (B: VIBEPASS) |

Lookup queries used to open candidate papers:

| Query | Source | Hits looked at | New relevant papers |
|---|---|---|---|
| Title lookups for 30 candidate titles | OpenAlex works search (api.openalex.org), anonymous | 30 (best match each) | lookup only |
| 28 title searches for 17 candidate titles | arXiv HTML search (arxiv.org/search) | about 50 | lookup only |
| Title searches | arXiv export API | 0 (it answered "Rate exceeded") | 0 |
| ICLR 2026 accepted notes | OpenReview API (api2.openreview.net) | 0 (challenge page) | 0 |
| "Web Application Vulnerability Repair via Context-Aware Fault Localization and Directed Differential Fuzzing" | WebSearch | 9 | 1 (found the author PDF) |
| "NDSS 2027 accepted papers summer cycle" | WebSearch | 9 | 0 |
| "Exploiting Ethereum Rollback Semantics" RollGain | WebSearch | 9 | 0 |
| Abstract pages opened for candidates (5 ICLR, 5 ICML and 4 NeurIPS paper pages; 5 ACL Anthology pages; 15 arXiv pages; 1 ICSE program page; 1 USENIX page; 4 PDFs) | venue and arXiv pages | 40 | 7 |

Result in one line: one new tier A paper (SlicePatch, S&P 2026) and six new tier B papers, of which two are weak B papers in a cluster that is already well covered.

## New papers

### Wang2026-SlicePatch Web Application Vulnerability Repair via Context-Aware Fault Localization and Directed Differential Fuzzing
- Authors: Chenlin Wang and Wei Meng; Year: 2026; Venue: IEEE Symposium on Security and Privacy (S&P 2026). The title is in the S&P 2026 accepted list. The OpenAlex record gives DOI 10.1109/SP63933.2026.00237. The PDF calls the system SlicePatch.
- URL opened: https://seclab.cse.cuhk.edu.hk/papers/sp26-SlicePatch.pdf (author PDF with title, authors and abstract; I read the abstract, the validation section and the failure analysis). The IEEE Xplore page (https://ieeexplore.ieee.org/document/11573512/) rendered empty.
- Status: VERIFIED
- Tier: A
- Touches: N3, N4
- Summary: SlicePatch repairs vulnerabilities in PHP web applications with LLMs. It runs the proof of concept (PoC) to find the code the exploit passes through and gives only that code to the LLM. Each candidate patch must block the PoC. It then faces "directed differential fuzzing": variants of the attack request are sent to the original and the patched application, and their responses are compared. On 96 real-world vulnerabilities and 7 LLMs it reports a 94.79% repair success rate, more than 30% above the baselines. PoC replay alone missed 35.70% of the patch failures (patches that variant inputs still exploit, syntax errors, and broken functionality). Removing the fuzzing stage lowered success from 94.79% to 83.33%. The paper names Claude 4 Sonnet and DeepSeek V3 as the models most prone to patches that variant attack inputs still exploit.
- Delta: This is the closest prior evidence for N3. On web applications, it shows that a patch which blocks the given PoC can stay exploitable, and it measures how often. It differs from the project in four ways. First, its extra attacks are generated automatically by fuzzing request parameters around the patched code. The project's held-out PoVs are written by hand from audit reports and can follow a different attack path from the shown PoV, which local fuzzing may not reach. Second, it is a fixed pipeline, not an agent with a terminal. It does not vary what the model is told (location only, report, PoV) or what it can run. Third, it does not study repository tests that assert the buggy behaviour; it checks functionality by comparing responses with the original application. Fourth, it has no smart contracts, no fund losses and no comparison with human-written code. The project should cite it for N3 and could add its variant-input check next to the held-out PoVs.

### Bernstein2026-FamiliarPatternAttack Trust Me, I Know This Function: Hijacking LLM Static Analysis using Bias
- Authors: Shir Bernstein, David Beste, Daniel Ayzenshteyn, Lea Schönherr, Yisroel Mirsky; Year: 2026; Venue: NDSS Symposium 2026 (journal reference on the arXiv page; the title is in the NDSS 2026 accepted list; DOI 10.14722/ndss.2026.242066 in the OpenAlex record).
- URL opened: https://arxiv.org/abs/2508.17361 (arXiv abstract page); numbers from the PDF at https://arxiv.org/pdf/2508.17361
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: LLMs used for code review and static analysis over-generalize familiar code patterns and skip small bugs inside them; the paper calls this abstraction bias. An automated black-box algorithm adds a small edit to a familiar pattern. The edit keeps runtime behaviour but misleads the model (the paper's "Familiar Pattern Attack"). On clean samples GPT-4o, Claude and Gemini answered correctly 90.8%, 84.3% and 92.2% of the time on average. Under the attack this fell to 8.9%, 17.1% and 24.1%. The attack transfers across model families and across Python, C, Rust and Go, and it still works when the system prompt warns about it.
- Delta: The paper studies an adversary who hides code behaviour from an LLM reviewer on purpose. The project runs an LLM security review on agent code and human code with no adversary, and confirms each reported flaw with a PoV. The paper still matters for N6. A reviewer can miss a small deviation inside code that looks like a well-known pattern. The 63008 bug, a downward tick iterator that skips its start tick, is that kind of small deviation in familiar code (this is my reading, not the paper's). This supports the project's rule that every reported flaw needs an executable test. It also means a review that reports nothing is weak evidence that the code is safe. The paper has no agent-versus-human comparison, no smart contracts and no exploits.

### AlKaswan2026-ModelSeeModelDo Model See, Model Do? Exposure-Aware Evaluation of Bug-vs-Fix Preference in Code LLMs
- Authors: Ali Al-Kaswan, Claudio Spiess, Prem Devanbu, Arie van Deursen, Maliheh Izadi; Year: 2026; Venue: MSR 2026 Technical Track (arXiv comment; the title is in the MSR 2026 program; DOI 10.1145/3793302.3793341 in the OpenAlex record).
- URL opened: https://arxiv.org/abs/2601.10496 (arXiv abstract page); numbers from the PDF at https://arxiv.org/pdf/2601.10496
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: The paper asks whether a code model prefers the buggy or the fixed version of a line, depending on which version it saw in training. It takes bug-fix pairs from ManySStuBs4J. It checks with Data Portraits whether each version appears in the Stack-v2 training corpus. It then tests StarCoder2 models and SmolLM3 with code completion and with likelihood scores. 67% of pairs had neither version in the corpus, 14% only the fix, 7% only the bug and 13% both. In generation, the models reproduced the buggy line far more often than the fix, and seeing the bug in training made this stronger. Some likelihood measures (Gini coefficient, arithmetic mean) switched to preferring the bug (56–62%) when only the bug had been seen.
- Delta: It gives a training-data reason why a model may rewrite a bug it has seen, which bears on the project's result that 4 of 6 setups rewrote the human's bug in finding 63008. The project picks models whose training data ends before each finding was published. That keeps the finding out of training data, but not the vulnerable code if the code was public before the model's cutoff. This paper shows that seeing only the buggy version raises the chance of reproducing it, so the proposal should say when each audited repository became public. The paper works on single-line Java bugs with open-data models, where exposure can be measured. It has no agents, no security bugs, no feature requests and no exploits.

### Liu2026-WhenAITakesTheWheel When AI Takes the Wheel: Security Analysis of Framework-Constrained Program Generation
- Authors: Yue Liu, Zhenchang Xing, Shidong Pan, Chakkrit Tantithamthavorn; Year: 2026; Venue: ICSE 2026 Research Track (listed under "Research Track" on the ICSE 2026 research track page; DOI 10.1145/3744916.3773142 in the OpenAlex record).
- URL opened: https://arxiv.org/abs/2510.16823 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: The authors built ChromeSecBench, 140 prompts based on known vulnerable Chrome extensions. They asked nine LLMs to generate complete extensions and analysed the results by scenario, model and vulnerability category. Between 18% and 50% of the generated programs were vulnerable, rising to 83% in Authentication & Identity scenarios and 78% in Cookie Management scenarios. Most flaws exposed cookies, history or bookmarks to untrusted code. Reasoning models produced more vulnerabilities than simpler models.
- Delta: Like the project, it starts from software in which humans wrote vulnerabilities and asks a model to write the same functionality. It differs in four ways. The model writes a whole extension from a prompt, not one function inside the audited code. It is single-shot LLM generation, not an agent working in the repository. It does not compare the output with the human's version or use a control group of features written correctly. The abstract says only that outputs were "analyzed for vulnerabilities", so I could not tell whether flaws were confirmed by running an exploit [uncertain]. There are no smart contracts.

### Bansal2026-VIBEPASS Can Vibe Coders Really Pass the Vibe Check? An Empirical Analysis of Fault-Targeted Reasoning in Frontier LLMs
- Authors: Srijan Bansal, Jiao Fangkai, Yilun Zhou, Austin Xu, Shafiq Joty, Semih Yavuz; Year: 2026; Venue: Findings of EMNLP 2026, as listed in the EMNLP 2026 program spreadsheet (paper 9323-FIND, presenter Srijan Bansal). The arXiv preprint 2603.15921 has the title "VIBEPASS: Can Vibe Coders Really Pass the Vibe Check?". I matched the two by the shared title phrase, the shared topic (fault-targeted reasoning) and the first author [uncertain until the Anthology page appears].
- URL opened: https://arxiv.org/abs/2603.15921 (arXiv abstract page); numbers from the PDF at https://arxiv.org/pdf/2603.15921, which is marked "Preprint. Under review."; the EMNLP 2026 program spreadsheet linked from https://2026.emnlp.org/program/
- Status: VERIFIED (arXiv version). The venue comes from the program spreadsheet.
- Tier: B
- Touches: N4
- Summary: VIBEPASS pairs 76 LiveCodeBench problems with model-written solutions that pass part of the tests but fail on edge cases (173 instances). It tests 12 frontier LLMs on two linked tasks: writing a test that exposes the hidden bug, and repairing the bug under different test guidance. Models almost always write valid test inputs but rarely write tests that expose the bug. Told only that the code is buggy, models reached a mean pass@1 of 58.6; asking them to write their own test first lowered it to 51.8. Tests from the first task, right or wrong, gave a success rate of 45.9 against 47.6 without tests. Tests that do not expose the fault made repair worse than no test at all.
- Delta: Like the project's repair input study, it varies the test evidence the model gets before repairing, and it finds that more test evidence can make repair worse. Its tests are model-written and may be wrong. In the project, the shown PoV is a correct exploit, and the harmful tests are the repository's own human-written tests that assert the buggy behaviour. VIBEPASS works on short competitive-programming solutions, with no agent terminal, no security bugs and no held-out exploits.

### Yang2026-SKANF Insecurity Through Obscurity: Veiled Vulnerabilities in Closed-Source Contracts
- Authors: Sen Yang, Kaihua Qin, Aviv Yaish, Fan Zhang; Year: 2026; Venue: ACM CCS 2026 (arXiv comment "Published in ACM CCS 2026"; the title is in the CCS 2026 accepted list).
- URL opened: https://arxiv.org/abs/2504.13398 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N2, N7
- Summary: SKANF analyses the EVM bytecode of closed-source and obfuscated contracts. It undoes control-flow obfuscation and runs symbolic execution seeded with historical transactions to find and exploit asset-management vulnerabilities. On real MEV bot contracts it found vulnerabilities in 1,046 contracts and generated working exploits for 394, with potential losses of $10.6M. It also found 104 real attacks on MEV bots that caused $2.76M in losses.
- Delta: A weak B. It belongs with the exploit-generation tools already indexed, such as Midas and SPSYN: it generates executable exploits and states losses in dollars. It works on deployed bytecode, while the project writes PoVs by hand from audit findings in source code and measures the loss of each exploit. It has no LLMs, agents, code generation or repair. It adds no new threat to the project's novelty; it is one more citation for N2 and N7.

### Liu2026-RollGain Exploiting Ethereum Rollback Semantics: Profit-Driven Attack Synthesis and Off-Chain Misinterpretation Testing
- Authors: Yixuan Liu, Xinlei Li, Yi Li; Year: 2026; Venue: ISSTA 2026, published in Proceedings of the ACM on Software Engineering (DOI 10.1145/3832246 in the OpenAlex record; the title and authors are on the ISSTA 2026 research papers page).
- URL opened: https://conf.researchr.org/track/issta-2026/issta-2026-research-papers (title and authors only). Abstract read in the OpenAlex record https://api.openalex.org/works/https://doi.org/10.1145/3832246
- Status: UNVERIFIED (the ACM DL page returned HTTP 403 to both curl and WebFetch; arXiv title search and a web search found no preprint; OpenAlex is not one of the page types the protocol accepts)
- Tier: B
- Touches: N2, N7
- Summary: The EVM undoes all state changes when a call fails, so an attacker can make a call fail on purpose and keep only the profitable outcomes. RollGain models contract structure and value flows, checks candidate attack executions symbolically, and replays them on a forked chain to rank them by profit. It also tests whether off-chain systems such as explorers, token trackers and RPC providers treat failed executions as successful. It reports 95.3% recall with zero false positives on its datasets. It also found 20 such misreading vulnerabilities across 18 off-chain systems: 18 confirmed, 16 fixed and 5 with CVE identifiers.
- Delta: A weak B, in the same group as SKANF. Its forked-chain replay to rank attacks by profit is close in technique to the project's loss estimate (N7). It covers one attack class and has no LLMs, agents or repair.

## Screened, not counted

Read and already screened out by round 2. My reading agrees with round 2 that these are at most tier C, with one note.

| Paper (venue) | Where round 2 judged it | Note |
|---|---|---|
| CyberGym-E2E: Scalable Real-World Benchmark for AI Agents' End-to-End Cybersecurity Capabilities (ICML 2026) | the screened-out table in the round-2 leads file (`r2_S3a_leads.md`) | 920 vulnerabilities in 139 projects; agents find the bug, write a PoC and write a patch checked with developer tests. I would call it a borderline B for N3 and N4, but CyberGym itself is indexed. |
| Benchmarking Reward Hack Detection in Code Environments via Contrastive Analysis (ICML 2026) | the screened-out table in the round-2 leads file (`r2_S3b_leads.md`) | Benchmark of 517 coding trajectories, 54 kinds of reward exploits; the best LLM judge detects 63% when it compares trajectories side by side. |
| The Undecidability of Overfitting in Automated Program Repair (ICSE 2026, New Ideas track) | `r2_S3b_leads.md` | Position paper: test suites are only partial correctness checks, so overfitting cannot be removed. Verified on its ICSE program page. |
| On the Evaluation of Large Language Models in Multilingual Vulnerability Repair (TOSEM; presented at ICSE 2026 in the journal-first track) | `r2_S3b_leads.md` | Repair across seven languages, judged without exploits. |
| AgenticSCR (ASE 2026 industry track) | `r2_S3a_leads.md` | Agentic security code review at Atlassian; no executable confirmation. |
| Evaluating Coding Agents on Kernel Exploit Generation (KEX-bench; EMNLP 2026 main) | `r2_S3a_leads.md` | 45 kernel exploit tasks; with a reference PoC the best setup solves 31 of 45. |

Read and judged tier C (venue page, arXiv page or abstract opened unless marked "title"):

| Paper | Venue | Reason for C |
|---|---|---|
| FHE-Coder: Benchmarking Secure Agentic Code Generation for Fully Homomorphic Encryption | ICLR 2026 | Method paper with a 10-task benchmark; baseline agents pass functional tests but misuse cryptographic parameters. |
| HackWorld: Evaluating Computer-Use Agents on Exploiting Web Application Vulnerabilities | ICLR 2026 | Exploitation benchmark (36 web apps; exploitation rates below 12%); same group as ExploitGym, which is indexed as C. |
| PACEbench | ICLR 2026 | Cyber-exploitation benchmark. |
| Is it Thinking or Cheating? Detecting Implicit Reward Hacking by Measuring Reasoning Effort | ICLR 2026 | Reward-hacking detection in math and coding; not specific to tests in repair. |
| RedCodeAgent | ICLR 2026 | Red-teaming of code agents for risky actions. |
| Co-RedTeam | ICML 2026 | Multi-agent vulnerability discovery and exploitation. |
| Position: Code Benchmarks Should Prioritize Rigor, Reliability, and Reproducibility | ICML 2026 | Survey of 572 code benchmarks with a 55-item checklist; general advice. |
| AdverMCTS | ICML 2026 | Code that overfits the visible tests in competitive programming; a generation method. |
| Reinforcement Learning-Guided Symbolic Execution for Efficient and Exploitable Smart Contract Analysis (RSymX) | NeurIPS 2026 | Detection tool that also outputs exploit call sequences; no loss estimate. |
| Hack-Verifiable Environments | NeurIPS 2026 | Reward hacking in text games, not code. |
| VeriVul; RustMizan | NeurIPS 2026 (Evaluations and Datasets) | Vulnerability-detection benchmarks built to resist training-data contamination. |
| EVM-QuestBench | ACL 2026 | LLM-written transaction scripts run on a forked EVM chain; tests functional correctness, not contract security. |
| SeCuRepair; SynthFix | ACL 2026; Findings of ACL 2026 | Vulnerability repair methods judged by similarity metrics and human study, not exploits. |
| RedCoder | ACL 2026 | Multi-turn adversarial prompting to make code LLMs write vulnerable code. |
| SWE-Mutation | Findings of ACL 2026 | Mutated solutions used to test LLM-written test suites. |
| Countdown-Code | EMNLP 2026 | Models learn to manipulate the test harness from 1% contaminated fine-tuning data; training-time study. |
| VEX-Bench; Breaking the Code (TACL); SABER | EMNLP 2026 | Exploitability assessment, jailbreaking of code agents, operational safety of coding agents (title only for the last two). |
| Repairing LLM Executions for Secure Automatic Programming | ICSE 2026 | Interpretability method that steers generation away from vulnerable code. |
| What's in a Benchmark? The Case of SWE-Bench in Automated Program Repair | ICSE 2026 (SE in Practice) | Who submits to the SWE-Bench leaderboards; not about test validity. |
| Diffploit | ICSE 2026 | LLM-guided exploit migration across library versions (84.2% of 689 tasks). |
| pPatch: Automated Vulnerability Unpatching | FSE 2026 | Reverts security patches to rebuild vulnerable versions for benchmarks (371 and 353 Linux kernel vulnerabilities). |
| AllocScope | FSE 2026 | Static detection of DeFi allocation-logic bugs; no AI and no exploits. |
| Assessing the Cross-Version Applicability of Java Library Vulnerability Exploits | ASE 2026 | Exploits identify affected versions with 83.0% recall and 99.3% precision; supply-chain setting. |
| AIALIB: A Threat Library for AI-Generated Code | ASE 2026 | Threat catalogue for AI-generated code (abstract read in OpenAlex only). |
| Generation of Web Apps with Agentic IDEs: An Empirical Assessment | ASE 2026 | Functional comparison of Copilot, Cursor and Windsurf; no security. |
| Insecure Coding Preferences in Long-Term Memory | ISSTA 2026 | Insecure stored preferences raise vulnerable-code rates by 2.7 to 50.3 percentage points. |
| Beyond Bug Fixes (post-merge quality of agent PRs); Bug-Fixing in the Age of AI: Human vs. Agentic Pull Requests; Studying the Footprints of AI Coding Agents in Blockchain Repositories | MSR 2026 (technical track; the last two are mining challenge papers) | Pull-request quality, acceptance and timing; no security. The human-versus-agent study reports acceptance of 71.37% against 87.62%. |
| Liquidity Mining as an Attack Surface: Incentive-Induced Liquidity Attacks in Concentrated Liquidity Market Makers | USENIX Security 2026 | Economic attack on incentive design, not a code bug; $2.87M of measured victim loss. Background for N2 and N7, in the same kind of liquidity pool as finding 63008. |
| "Tab, Tab, Bug": Security Pitfalls of Next Edit Suggestions in AI-Integrated IDEs | ACM CCS 2026 | Attacks on IDE edit suggestions through poisoned context; not the security of code written without an adversary. |

## Leads not followed

- "Evaluating Harmful Memorization in LLM Code Generation", Findings of EMNLP 2026 (paper 6401-FIND in the EMNLP 2026 program spreadsheet). Not found on arXiv, in OpenAlex or by web search. If it is about models reproducing memorized vulnerable code, it would sit next to Model See, Model Do?.
- "Code Agents Don't Understand Root Cause: Evaluating Code Agents on Linux Kernel Fault Localization", EMNLP 2026 main (paper 6985-MAIN in the EMNLP 2026 program spreadsheet). Not found on arXiv or in OpenAlex. The title suggests agents fix symptoms rather than causes, which would be close to the shallow repairs in N3.
- ICSE 2027 accepted list: decisions were sent on 20 October 2026, and the research track page has no list yet. Check again in November 2026.
- NDSS 2027 summer-cycle accepted list: the call for papers gives a camera-ready deadline of 30 September 2026, but no accepted-papers page is online. Check again before the fall cycle closes.
- Not screened: workshop volumes of ACL 2026 (for example TrustNLP and EvalEval), workshops at ICLR, ICML and NeurIPS 2026, and EMNLP 2026 student research papers, which are not in the program spreadsheet's main tab.
- The full abstracts of AIALIB (ASE 2026) and RollGain (ISSTA 2026) sit behind the ACM DL, which blocked scripted access (HTTP 403).
