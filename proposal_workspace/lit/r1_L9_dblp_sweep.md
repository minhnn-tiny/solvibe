# L9: DBLP venue sweep (round 1)

Agent slice L9: coverage by venue, not by topic. Searched on 2026-10-21.

## How the sweep was run

- **The DBLP search API could not be used.** On 2026-10-21 the API first answered HTTP 429 (retry after 60 s) and then put every client, including WebFetch, behind an Anubis bot challenge. I did not try to get around the challenge.
- **I used DBLP's own data instead.** I downloaded the DBLP XML dump (`https://dblp.org/xml/dblp.xml.gz`, release of 2026-10-20, MD5 checked) and kept every article and conference paper from the target venue streams and years. That gave 68,288 papers. I then ran the title-keyword queries on these titles with regular expressions. The expressions copy the API's behaviour: words match as prefixes, a space means AND, and `|` means OR. Running locally removed the API's cap of 1,000 hits per query, so every hit in the target venues was screened.
- **Venue streams and years (DBLP key prefix):** ICSE `conf/icse` (main, companion and co-located tracks), ESEC/FSE `conf/sigsoft` plus FSE 2024-2026 in `journals/pacmse` (issue "FSE"), ASE `conf/kbse`, ISSTA `conf/issta` plus ISSTA 2025 in `journals/pacmse` (issue "ISSTA"), IEEE S&P `conf/sp`, USENIX Security `conf/uss`, CCS `conf/ccs`, NDSS `conf/ndss`, all 2022-2026. NeurIPS `conf/nips`, ICLR `conf/iclr`, ICML `conf/icml`, ACL `conf/acl` (main and Findings), EMNLP `conf/emnlp` (main and Findings), all 2023-2026. TOSEM, TSE and EMSE (`journals/tosem`, `journals/tse`, `journals/ese`), 2023-2026.
- **Venues DBLP had not indexed yet.** The dump has no ICSE 2026 research track (only 72 ICSE 2026 records), no ISSTA 2026, no ASE 2026, no USENIX Security 2026, no ICML 2026, no CCS 2026, no NeurIPS 2026 and no EMNLP 2026. For these I fetched the venue's own accepted-paper list and ran the same queries on its titles: ICSE 2026 research track, ISSTA 2026 research papers, FSE 2026 research papers and ASE 2026 research track (conf.researchr.org), ICML 2026 (icml.cc paper list), NeurIPS 2026 (neurips.cc paper list), USENIX Security 2026 (technical sessions page) and CCS 2026 (sigsac.org accepted papers). EMNLP 2026 has no accepted-paper list online yet, so it was not swept.
- **Verification.** For each relevant hit I opened the arXiv abstract page or a publisher page (ACL Anthology, USENIX, NDSS, Springer) or the conference program page on conf.researchr.org. ACM DL and IEEE Xplore pages returned 403 or an empty page, so for ACM and IEEE papers I opened the arXiv version. I found the arXiv version through DBLP's own arXiv (CoRR) records in the same dump, matched by title and first author. For four papers with no arXiv version, the only page with an abstract was the Crossref record of the DOI, which carries the abstract the publisher deposited; those blocks say so. Papers where I could confirm the title, venue and authors but not read an abstract are marked UNVERIFIED.
- **Limits.** Title search misses papers whose titles use none of the query words. I added a residual broad query and a query on tool names to reduce this. Journal early-access papers that DBLP has not yet indexed are not covered. The shared web-search budget and the OpenAlex daily budget were used up by parallel agents during this run, so a few papers could not be verified (see Leads).

## Queries run

Queries Q01 to Q40 ran on the 68,288-paper DBLP venue set. "Hits looked at" counts hits in the target venues and years; the number in brackets is how many of those an earlier query had not already shown. "New relevant papers" counts papers that ended up as blocks below and that this query found first.

| # | Query (title words) | Source | Hits looked at | New relevant papers |
|---|---|---|---|---|
| — | `smart contract streamid:conf/icse:`, `smart contract venue:ICSE:`, `solidity` (3 test queries) | DBLP search API | 0 (HTTP 429, then Anubis bot challenge) | 0 |
| Q01 | smart contract + LLM \| GPT \| language model | DBLP dump (local) | 28 (28) | 9 |
| Q02 | smart contract + agent | DBLP dump (local) | 4 (2) | 1 |
| Q03 | smart contract + generation \| synthesis | DBLP dump (local) | 26 (18) | 6 |
| Q04 | smart contract + repair \| patch \| fix | DBLP dump (local) | 12 (6) | 1 |
| Q05 | smart contract + exploit \| attack | DBLP dump (local) | 15 (8) | 1 |
| Q06 | smart contract + audit | DBLP dump (local) | 3 (2) | 0 |
| Q07 | solidity | DBLP dump (local) | 17 (14) | 1 |
| Q08 | DeFi \| decentralized finance + exploit \| attack \| manipulation \| loss | DBLP dump (local) | 19 (19) | 3 |
| Q09 | flash loan \| price manipulation \| reentrancy \| front-running \| MEV \| rug pull | DBLP dump (local) | 34 (26) | 1 |
| Q10 | vibe coding | DBLP dump (local) | 9 (9) | 2 |
| Q11 | AI-generated \| LLM-generated \| AI assistant code + security \| vulnerab | DBLP dump (local) | 27 (26) | 6 |
| Q13b | LLM \| language model \| GPT \| Codex + code + secure \| vulnerab | DBLP dump (local) | 56 (48) | 5 |
| Q12 | Copilot + security \| vulnerab | DBLP dump (local) | 6 (1) | 1 |
| Q13 | code generation \| completion \| synthesis + secure \| vulnerab | DBLP dump (local) | 31 (15) | 2 |
| Q14 | coding agent \| software engineering agent \| SWE-agent \| SWE-bench + security \| vulnerab | DBLP dump (local) | 22 (21) | 5 |
| Q15 | vulnerability repair \| fix \| patch (any method) | DBLP dump (local) | 70 (62) | 7 |
| Q16 | proof of concept \| proof-of-vulnerability \| PoC \| exploit generation | DBLP dump (local) | 23 (20) | 5 |
| Q17 | exploit + LLM \| agent \| GPT | DBLP dump (local) | 69 (58) | 1 |
| Q18 | patch correctness \| overfitting \| plausible patch \| hidden test | DBLP dump (local) | 89 (89) | 4 |
| Q19 | program repair \| bug fix + LLM \| agent \| GPT | DBLP dump (local) | 91 (79) | 6 |
| Q19b | repair \| debug + feedback \| self-repair \| execution \| conversational | DBLP dump (local) | 31 (21) | 2 |
| Q20 | coding agent \| SWE-bench \| SWE-agent \| issue resolution (all) | DBLP dump (local) | 73 (67) | 7 |
| Q21 | security code review \| vulnerability detection + LLM \| GPT \| agent | DBLP dump (local) | 57 (40) | 2 |
| Q22 | human + AI \| LLM \| Copilot + code (comparison) | DBLP dump (local) | 26 (24) | 1 |
| Q23 | secure \| vulnerab + benchmark \| dataset + code \| LLM \| agent | DBLP dump (local) | 59 (32) | 2 |
| Q24 | security test \| vulnerability witness \| reproduce vulnerability | DBLP dump (local) | 24 (21) | 1 |
| Q25 | financial \| monetary loss \| damage + estimate \| quantify \| profit | DBLP dump (local) | 29 (26) | 1 |
| Q26 | test oracle \| assertion \| regression test + LLM \| repair | DBLP dump (local) | 33 (31) | 0 |
| Q27 | prompt \| requirement \| specification + secure code + LLM | DBLP dump (local) | 64 (45) | 2 |
| Q28 | smart contract (all, catch-all) | DBLP dump (local) | 211 (128) | 5 |
| Q29 | ethereum \| EVM \| blockchain \| web3 \| DApp + security \| bug \| audit (catch-all) | DBLP dump (local) | 132 (86) | 1 |
| Q30 | security \| vulnerab \| exploit + LLM \| agent \| GPT \| AI (residual, minus jailbreak, privacy, backdoor and similar) | DBLP dump (local) | 272 (94) | 3 |
| Q31 | code review + security | DBLP dump (local) | 13 (9) | 0 |
| Q32 | loss \| stolen \| theft \| damage + DeFi \| smart contract \| blockchain | DBLP dump (local) | 12 (8) | 0 |
| Q33 | business logic \| accounting \| reward \| staking \| vault \| Uniswap \| hook + contract \| DeFi | DBLP dump (local) | 14 (3) | 0 |
| Q34 | audit report \| contest \| bug bounty \| Code4rena \| Sherlock \| Immunefi \| Solodit | DBLP dump (local) | 8 (6) | 0 |
| Q35 | vulnerability-introducing \| bug-inducing commit \| SZZ | DBLP dump (local) | 21 (19) | 2 |
| Q36 | masked \| held-out \| hidden + test \| exploit \| PoC | DBLP dump (local) | 17 (15) | 0 |
| Q37 | specification \| issue description \| problem statement + ambiguous \| underspecified \| leak \| hint + LLM \| code | DBLP dump (local) | 11 (10) | 1 |
| Q38 | regenerate \| reimplement \| rewrite + vulnerable \| security \| bug | DBLP dump (local) | 2 (2) | 0 |
| Q39 | test overfitting \| reward hacking \| cheating + code \| agent \| test | DBLP dump (local) | 6 (4) | 0 |
| Q40 | OpenHands \| Aider \| Codex CLI \| Claude Code \| Cursor \| agent-generated \| AI-authored PR | DBLP dump (local) | 13 (8) | 1 |
| L1 | Q01-Q29, Q13b, Q19b on ICSE 2026 research track list (667 titles) | conf.researchr.org | 69 | 11 |
| L2 | same queries on ISSTA 2026 research papers list (210 titles) | conf.researchr.org | 33 | 5 |
| L3 | same queries on FSE 2026 research papers list (440 titles) | conf.researchr.org | 42 | 0 (all already in DBLP as PACMSE FSE 2026) |
| L4 | same queries on ASE 2026 research track list (442 titles) | conf.researchr.org | 55 | 7 |
| L5 | same queries on ICML 2026 paper list (6,646 titles) | icml.cc | 58 | 4 |
| L6 | same queries on NeurIPS 2026 paper list (9,094 titles) | neurips.cc | 77 | 5 |
| L7 | same queries on USENIX Security 2026 technical sessions (377 titles) | usenix.org | 14 | 2 |
| L8 | same queries on CCS 2026 accepted papers (486 titles) | sigsac.org | 19 | 2 |
| W1 | "Not All Input Helps" What Information Should We Feed to LLMs for Vulnerability Repair ICSE 2026 | WebSearch | 9 | 0 (found the NIER@ICSE 2026 page used to verify Choi2026) |
| W2 | "SmartPoC" Validating Smart Contract Vulnerability Findings through PoC Generation and Execution | WebSearch | 9 | 0 (found the arXiv version, 2511.12993) |
| W3-W4 | SymRadar; "Just Old Wine in a New Bottle" | WebSearch | 0 (refused: shared session search budget used up) | 0 |

Lookups used only to verify papers, not to find them: 50 arXiv API title searches (17 answered, 33 refused with HTTP 429), 46 OpenAlex title searches (all refused with HTTP 429; the shared daily budget was used up), 23 Crossref DOI records (all answered, 4 with abstracts), 115 arXiv abstract pages, 6 arXiv full-text pages, 12 publisher pages (ACL Anthology, USENIX, NDSS, Springer) and 2 conf.researchr.org paper pages.

Totals: 1,617 distinct titles screened: 1,072 from the DBLP queries Q01-Q29, 170 more from Q30-Q39, 8 more from Q40, and 367 from the 2026 venue lists. 134 papers are kept below: 9 in tier A, 48 in tier B, 77 in tier C. Of these, 8 are UNVERIFIED.

**Saturation.** Within the swept venues the sweep is close to saturation. The two catch-all queries (Q28, Q29: 343 hits) added 6 papers, and the residual queries (Q30-Q40: 389 hits) added 7, two in tier B and five in tier C. The 2026 venue lists added 36 papers, including 4 of the 9 tier-A papers (SusVibes, EVMbench, To Run or Not to Run, SmartPoC), because DBLP had not yet indexed those venues. This means the result depends on venues that are still being indexed. EMNLP 2026, the ICSE 2026 companion tracks, the ASE 2026 tracks other than the research track, and journal early-access papers were not covered.

---

## Tier A: closely related

### Zhao2026-SusVibes Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks
- Authors: Songwen Zhao et al.; Year: 2026; Venue: ICML 2026 (seen in the ICML 2026 paper list at icml.cc; arXiv comment "Accepted in ICML 2026"; not yet in DBLP)
- URL opened: https://arxiv.org/abs/2512.03262 (arXiv abstract page); full text read at https://arxiv.org/html/2512.03262
- Status: VERIFIED
- Tier: A
- Touches: N1, N5
- Summary: SusVibes has 186 feature-request tasks from 100 Python GitHub projects. Each task comes from a vulnerability fix commit: the authors go back to the commit before the fix, mask the feature's implementation, generate a task description, and judge the agent's code with the human-written functional tests and security tests. The paper runs three agent frameworks (SWE-agent, OpenHands, Claude Code) with four models, 12 settings in all. The best setting, SWE-agent with Claude 4 Sonnet, is functionally correct on 57% of tasks but secure on only 11.8%; adding vulnerability hints to the feature request did not fix this.
- Delta: SusVibes asks the N1 question at scale, but on Python, and it judges security with the repository's own security tests, not with an exploit. A full-text search found no control group of features the human wrote correctly, no LLM security review of the human's and the agent's code, no repair stage and no loss estimate. The project works on Solidity business-logic and accounting bugs from audit contests, judges the human's and the agent's code with the same Foundry PoV (which passes on the human's code and fails on the human's fix), adds the control group with a review confirmed by new PoVs (N6), tests repair with held-out PoVs (N3, N4) and measures losses in funds (N7). SusVibes adds hints to requests to help the agent; the project instead writes requests that avoid hinting at the bug or the fix and checks that they do (N5).

### Chen2026-SecureVibeBench SecureVibeBench: Benchmarking Secure Vibe Coding of AI Agents via Reconstructing Vulnerability-Introducing Scenarios
- Authors: Junkai Chen et al.; Year: 2026; Venue: ACL 2026 (Proceedings of ACL 2026, Volume 1: Long Papers, pp. 24144-24168)
- URL opened: https://arxiv.org/abs/2509.22097 (arXiv abstract page; arXiv v1 was titled "SecureAgentBench"); full text read at https://arxiv.org/html/2509.22097
- Status: VERIFIED
- Tier: A
- Touches: N1
- Summary: SecureVibeBench has 105 C/C++ memory-safety tasks from 41 projects, sourced from OSS-Fuzz and the ARVO dataset. Each task starts from the parent of the vulnerability-introducing commit, with the requirement the human implemented in that commit. The paper argues that agents must be placed "in the exact real-world scenarios where human developers originally introduced vulnerabilities" to see whether they repeat human errors. Security is judged by PoV programs verified by ARVO, and Semgrep scans the agent's patch for new risks. It runs three agents (SWE-agent, OpenHands, Aider) with five LLMs (Claude Sonnet 4.5, GPT-5, Claude 3.7 Sonnet, GPT-4.1, DeepSeek-V3.1), and also tests Claude Code and Codex; the best setting, SWE-agent with Claude Sonnet 4.5, produces only 23.8% correct and secure solutions.
- Delta: This is the closest existing design to N1: same starting commit, same requirement, an executable PoV as the security judge. It even uses the project's three agent tools (Aider, OpenHands, Codex) and Claude Sonnet 4.5, so the choice of agents is not a difference. The differences: C/C++ memory-safety bugs found by fuzzing, not Solidity business-logic bugs found in audits; new risks are found by a static analyser (Semgrep), not by an LLM review whose findings each need a confirming PoV (N6); a full-text search found no control group of features the human wrote correctly; and there is no repair stage with held-out PoVs (N3, N4) and no loss estimate (N7). The project also checks that feature requests do not hint at the bug (N5).

### Asare2023-CopilotHumans Is GitHub's Copilot as bad as humans at introducing vulnerabilities in code?
- Authors: Owura Asare, Meiyappan Nagappan, N. Asokan; Year: 2023; Venue: Empirical Software Engineering 28(6), article 129
- URL opened: https://link.springer.com/article/10.1007/s10664-023-10380-1 (Springer article page); also https://arxiv.org/abs/2204.04741 (arXiv abstract page)
- Status: VERIFIED
- Tier: A
- Touches: N1
- Summary: The authors take a dataset of C/C++ vulnerabilities and prompt Copilot at the points where human developers introduced them. Each suggestion is classed by whether it reproduces the original vulnerable code or the fixed code. Copilot reproduced the vulnerable code about 33% of the time and the fixed code 25% of the time, and did worse on older vulnerabilities. The authors conclude that Copilot is "not as bad as human developers" at introducing vulnerabilities.
- Delta: This is the earliest direct test of the N1 idea: the same scenario where a human introduced a bug, completed by an AI tool. It uses code completion (Copilot), not a coding agent with a repository and a terminal, and it judges by inspecting whether the suggestion matches the vulnerable or the fixed code, not by running an exploit. It has no control group of correct human code, no Solidity, no repair and no loss estimate.

### EVMbench2026 EVMbench: Evaluating AI Agents on Smart Contract Security
- Authors: Justin Wang et al. (OpenAI, Paradigm, OtterSec); Year: 2026; Venue: ICML 2026 (seen in the ICML 2026 paper list at icml.cc; not yet in DBLP; the arXiv page has no venue comment)
- URL opened: https://arxiv.org/abs/2603.04915 (arXiv abstract page); full text read at https://arxiv.org/html/2603.04915
- Status: VERIFIED
- Tier: A
- Touches: N2, N3, N7 (in part)
- Summary: EVMbench measures whether agents can detect, patch and exploit smart-contract vulnerabilities. It uses 117 vulnerabilities from 40 repositories, mostly from Code4rena audits. In Patch mode (44 vulnerabilities), the existing tests must still pass and the vulnerability is checked with exploit tests the agent never sees; these are mostly the PoC exploit tests the auditors wrote. In Exploit mode (23 vulnerabilities), the agent attacks contracts deployed on a local Ethereum chain and is graded by on-chain events and balances; Detect mode is scored against the audit report by a model-based judge, with an award based on historical audit payouts. Agents include Codex CLI, Claude Code and Gemini CLI; with a short hint naming the mechanism, GPT-5.2 scores 90.2% on Patch and 78.3% on Exploit, which the authors read as showing that finding the bug is the hard part.
- Delta: EVMbench already judges agent patches of Code4rena findings with exploit tests the agent cannot see, which overlaps with N2 and N3. It does not ask the agent to write the feature from a request, so it has no comparison with the human developer (N1), no control group and no LLM review confirmed by PoVs (N6). Its patch tasks do not show one PoV as a failing test while holding back others, and they do not vary what the agent is told or what it can run (N3, N4). Its exploit mode checks balances to decide success but does not estimate who loses how much (N7).

### Bobadilla2026-AutoFixesSC Do Automated Fixes Truly Mitigate Smart Contract Exploits?
- Authors: Sofia Bobadilla, Monica Jin, Martin Monperrus; Year: 2026 (journal issue; arXiv journal reference says 2025); Venue: IEEE Transactions on Software Engineering 52(1), pp. 100-115
- URL opened: https://arxiv.org/abs/2501.04600 (arXiv abstract page); full text read at https://arxiv.org/html/2501.04600
- Status: VERIFIED
- Tier: A
- Touches: N2, N3
- Summary: The authors survey 20 smart-contract repair tools and run the 7 they could reproduce on the 143 contracts of SmartBugs-Curated. They hand-write 91 executable exploits, one per vulnerable contract, each with a functional check, and define the exploit mitigation rate: the share of exploits a patch blocks. The rate runs from 29% (SmartShield) to 74% (SolGPT, an LLM-based tool that uses gpt-3.5-turbo), and 6 of the 7 tools break the contract's function in some cases.
- Delta: It shares the core of N3: a repair counts only if an executable exploit no longer works, on Solidity. It uses one exploit per contract and classic vulnerability classes (reentrancy, access control, arithmetic and similar), not audit-contest business-logic bugs with several PoVs. It has no shown-versus-held-out PoV split, no coding agents with a terminal, no variation of the repair input (N4) and no comparison with the human developer (N1).

### Choi2026-NotAllInput Not All Input Helps: What Information Should We Feed to LLMs for Vulnerability Repair?
- Authors: Dongwook Choi, Eunseok Lee; Year: 2026; Venue: ICSE 2026, New Ideas and Emerging Results (NIER) track (DBLP: NIER@ICSE 2026)
- URL opened: https://conf.researchr.org/details/icse-2026/icse-2026-nier/49/Not-All-Input-Helps-What-Information-Should-We-Feed-to-LLMs-for-Vulnerability-Repair (conference program page with authors and abstract)
- Status: VERIFIED
- Tier: A
- Touches: N4
- Summary: The authors survey 26 studies to list the inputs used in LLM vulnerability repair: vulnerable code, markers on the vulnerable lines, CVE and CWE identifiers and descriptions, and patch context. They then test these inputs alone and together across several LLMs and datasets. They find that some inputs add noise and make repair worse, and they give guidelines on what to include. The abstract gives no numbers.
- Delta: It studies the "what the model is told" half of N4. It does not include an executable PoV or a written audit report as inputs, does not vary what the model can run, and works on LLM prompting over static datasets, not agents in a repository. The project also judges repairs with held-out PoVs (N3) and looks at repository tests that encode the vulnerable behaviour.

### ToRun2026 To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair
- Authors: Zhihao Lin et al.; Year: 2026; Venue: ISSTA 2026 (seen in the ISSTA 2026 research papers list on conf.researchr.org; arXiv comment confirms; not yet in DBLP)
- URL opened: https://arxiv.org/abs/2606.26978 (arXiv abstract page); part of the full text read at https://arxiv.org/html/2606.26978
- Status: VERIFIED
- Tier: A
- Touches: N4
- Summary: The authors analyse 7,745 agent traces from SWE-bench submissions and then run 3,000 repair attempts on 200 SWE-bench tasks with Claude Code, Codex and OpenCode. They compare four settings that range from Prohibited (no running of tests or project scripts) to Unrestricted. Agents run tests 8.8 times per task on average, yet for commercial agents the resolve rates of Prohibited and Unrestricted differ by only 1.25 percentage points, which is not statistically significant, while Prohibited saves 56-62% of tokens on Claude Code.
- Delta: This is the closest paper to the "what the agent can run" half of N4, and it also finds that running code adds little. It studies functional bug fixes on Python SWE-bench, not security repairs, and it does not give the agent a PoV, hold PoVs back, or vary the written input. It does not report the project's finding that a terminal lets the agent keep repository tests passing that assert the buggy behaviour, or that agents fit their fix to the shown test.

### SmartPoC2026 SmartPoC: Validating Smart Contract Vulnerability Findings through PoC Generation and Execution
- Authors: Longfei Chen et al.; Year: 2026; Venue: ASE 2026 (title as seen in the ASE 2026 research track list on conf.researchr.org); arXiv version titled "SmartPoC: Generating Executable and Validated PoCs for Smart Contract Bug Reports" [uncertain that the two versions are the same paper; the name and topic match]
- URL opened: https://arxiv.org/abs/2511.12993 (arXiv abstract page)
- Status: VERIFIED
- Tier: A
- Touches: N6, N2
- Summary: SmartPoC turns findings in smart-contract audit reports into executable PoC tests. It cuts each report down to the functions it names, writes PoCs with an LLM in a generate, repair and execute loop, and uses differential checking as the test of whether the bug is really triggered. On the SmartBugs-Vul and FORGE-Vul benchmarks it reaches 98.32% and 98.65% confirmation precision with 84.17% and 85.28% recall, and on recent Etherscan contracts it confirms 64 bugs from 545 audit findings at about $0.03 per finding.
- Delta: It automates the step N6 relies on: confirming a reported smart-contract flaw with an executable PoC. Its findings come from audit reports and static analysers, not from an LLM review that reads the human's and the agent's version of the same function with the same prompt, and it does not compare agents with humans (N1) or study repair (N3, N4). The project's PoVs are also extended to measure who loses how much (N7).

### Zhang2026-V2E V2E: Validating Smart Contract Vulnerabilities through Profit-Driven Exploit Generation and Execution
- Authors: Jingwen Zhang et al.; Year: 2026; Venue: FSE 2026 (Proc. ACM Softw. Eng. 3(FSE), pp. 2259-2281)
- URL opened: https://arxiv.org/abs/2604.13611 (arXiv abstract page)
- Status: VERIFIED
- Tier: A
- Touches: N6, N7, N2
- Summary: V2E checks whether a vulnerability reported by a detection tool can really be exploited. It generates a PoC exploit with an LLM, runs it, and checks two things: whether the vulnerability is triggered and whether the exploit causes a financial loss. It refines the PoC from execution feedback and outperforms a baseline on 264 hand-labelled contracts.
- Delta: It combines two project ideas: confirming each reported flaw with an executable exploit (N6) and judging an exploit by the money it moves (N7). Its reports come from detection tools on deployed contracts, not from an LLM review of agent code and human code with the same prompt, and its loss check is a yes-or-no profit test, not an estimate of who loses how much. It has no agent-versus-human comparison (N1) and no repair study (N3, N4).

---

## Tier B: related

### Pearce2022-Asleep Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions
- Authors: Hammond Pearce et al.; Year: 2022; Venue: IEEE Symposium on Security and Privacy (S&P) 2022, pp. 754-768
- URL opened: https://arxiv.org/abs/2108.09293 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: The authors prompt Copilot with 89 scenarios built around high-risk CWEs, such as MITRE's Top 25, and vary the weakness, the prompt and the domain. Of the 1,689 programs produced, about 40% were vulnerable.
- Delta: It measures how often AI-written code is vulnerable, using hand-made scenarios and CWE checks, with no human baseline on the same code and no executable exploit. The project compares the agent with the human who wrote the same function in a real commit, on Solidity, judged by a PoV.

### Perry2023-InsecureAI Do Users Write More Insecure Code with AI Assistants?
- Authors: Neil Perry et al.; Year: 2023; Venue: ACM CCS 2023, pp. 2785-2799
- URL opened: https://arxiv.org/abs/2211.03622 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: In a user study on security-related tasks in several languages, participants with an AI assistant based on codex-davinci-002 wrote significantly less secure code than those without one. They were also more likely to believe their code was secure.
- Delta: It compares humans with and without an assistant on set tasks, not an autonomous agent against the human who wrote a real feature. Security is judged by inspecting the solutions, not by an exploit, and there is no Solidity, repair or loss estimate.

### Sandoval2023-LostAtC Lost at C: A User Study on the Security Implications of Large Language Model Code Assistants
- Authors: Gustavo Sandoval et al.; Year: 2023; Venue: USENIX Security Symposium 2023, pp. 2205-2222
- URL opened: https://arxiv.org/abs/2208.09727 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: 58 student programmers implemented a singly-linked shopping list in C, with or without an LLM assistant. Assisted users produced critical security bugs at a rate no more than 10% higher than the control group.
- Delta: A controlled user study of AI-assisted humans on one small C task. The project compares autonomous agents with the original developers of real Solidity features, using executable PoVs and a control group of correctly written functions.

### Asare2024-UserCopilot A User-centered Security Evaluation of Copilot
- Authors: Owura Asare, Meiyappan Nagappan, N. Asokan; Year: 2024; Venue: ICSE 2024, article 158
- URL opened: https://arxiv.org/abs/2308.06587 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: In a user study (n=25), participants solved problems with possibly vulnerable solutions, with or without Copilot. Copilot users wrote more secure solutions on the harder problem and showed no difference on the easier one.
- Delta: Human-with-tool against human-without-tool, on set problems, judged by inspection. The project measures agents working alone against the developer who wrote the same feature, with an executable exploit as the judge.

### Hamer2024-ChatGPTvsSO Just another copy and paste? Comparing the security vulnerabilities of ChatGPT generated code and StackOverflow answers
- Authors: Sivana Hamer, Marcelo d'Amorim, Laurie Williams; Year: 2024; Venue: IEEE Security and Privacy Workshops (SPW) 2024, Deep Learning Security and Privacy Workshop (DLSP), pp. 87-94
- URL opened: https://arxiv.org/abs/2403.15600 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: The authors ask ChatGPT the same security-related Java questions that StackOverflow users answered and scan 108 snippets from each source with CodeQL. ChatGPT's code had 248 vulnerabilities against 302 in the human answers, 20% fewer, a statistically significant difference.
- Delta: A human-versus-AI comparison on the same request, but for short snippets judged by a static analyser. The project uses full features in real repositories, a PoV as judge, and a control group.

### Fu2025-CopilotGitHub Security Weaknesses of Copilot-Generated Code in GitHub Projects: An Empirical Study
- Authors: Yujia Fu et al.; Year: 2025; Venue: ACM TOSEM 34(8), article 218
- URL opened: https://arxiv.org/abs/2310.02059 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N4 (in part)
- Summary: The authors find 733 snippets in GitHub projects that were written by Copilot, CodeWhisperer or Codeium; 29.5% of the Python and 24.2% of the JavaScript snippets have security weaknesses across 43 CWEs. Given static-analysis warnings, Copilot Chat fixed up to 55.5% of the issues.
- Delta: It studies AI code that reached real projects, judged by static analysis, without the human version of the same code. The project builds matched human and agent versions and judges both with the same exploit; its repair study uses PoVs and held-out PoVs rather than analyser warnings.

### Belozerov2026-SecureCodingAI Secure coding with AI – from detection to repair
- Authors: Vladislav Belozerov, Peter J. Barclay, Ashkan Sami; Year: 2026; Venue: Empirical Software Engineering 31(4), article 93
- URL opened: https://link.springer.com/article/10.1007/s10664-026-10812-8 (Springer article page); arXiv version https://arxiv.org/abs/2504.20814 is titled "Secure Coding with AI -- From Detection to Repair"
- Status: VERIFIED
- Tier: B
- Touches: N1, N6
- Summary: The authors take 2,315 C, C++ and C# snippets that developers obtained from GPT (the DevGPT dataset) and find 56 vulnerabilities in 48 files with static scanners and manual checks. GPT-4.1, GPT-5 and Claude Opus 4.1 detected 46, 44 and 45 of them and repaired 42, 44 and 43. They also observe that LLM-generated code is about as likely to contain vulnerabilities as developer-written code.
- Delta: It reports a human-versus-AI rate, but across different code, not the same function written by both. Its LLM review is checked by hand and re-scanning, not by an executable PoV for each finding (N6). No Solidity, exploits or held-out tests.

### Lian2026-ASE A.S.E: A Repository-Level Benchmark for Evaluating Security in AI-Generated Code
- Authors: Keke Lian et al.; Year: 2026; Venue: Findings of ACL 2026, pp. 31390-31405
- URL opened: https://arxiv.org/abs/2508.18106 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: A.S.E is a repository-level benchmark for the security of AI-generated code that aims to mirror real AI programming tasks. Current LLMs still struggle with secure coding at repository level, and a larger reasoning budget does not reliably give better code.
- Delta: It measures how secure LLM code is in repository context, without a human baseline, a control group or executable exploits for business-logic bugs. The abstract does not say how security is judged.

### Wang2026-RealSecBench RealSec-bench: A Benchmark for Evaluating Secure Code Generation in Real-World Repositories
- Authors: Yanlin Wang et al.; Year: 2026; Venue: Findings of ACL 2026, pp. 35866-35883
- URL opened: https://arxiv.org/abs/2601.22706 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: RealSec-bench has 105 instances from high-risk Java repositories, found with CodeQL, filtered by an LLM and checked by human experts, covering 19 CWEs. Retrieval-augmented generation improves functional correctness but not security, and telling models to follow general security guidelines often breaks compilation.
- Delta: Real-repository secure code generation judged by static analysis and a combined pass metric. The project uses Solidity, a matched human baseline, executable PoVs and a control group.

### Vero2025-BaxBench BaxBench: Can LLMs Generate Correct and Secure Backends?
- Authors: Mark Vero et al.; Year: 2025; Venue: ICML 2025 (PMLR 267)
- URL opened: https://arxiv.org/abs/2502.11844 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N3
- Summary: BaxBench has 392 tasks in which an LLM writes a backend application. It checks function with test cases and security by running end-to-end exploits against the running application. The best model, OpenAI o1, is correct on 62% of tasks, and exploits succeed on about half of the correct programs from each model.
- Delta: It shares the idea of judging generated code by running exploits. It has no human baseline (N1), writes whole applications from a specification rather than one function in an audited repository, and does not study repair with held-out exploits (N3).

### Nie2025-SecCodePLT SecCodePLT: A Unified Platform for Evaluating the Security of Code GenAI
- Authors: Yuzhou Nie et al.; Year: 2025; Venue: NeurIPS 2025, Datasets and Benchmarks Track (arXiv title "SeCodePLT: A Unified Platform for Evaluating the Security of Code GenAI")
- URL opened: https://arxiv.org/abs/2410.11096 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N3
- Summary: The authors build more than 5.9k samples in Python, C/C++ and Java over 44 CWE-based risk categories by expanding hand-checked seed examples with mutations. They use dynamic metrics, rather than LLM judges or rule-based detectors, to evaluate secure code generation and the detection and fixing of vulnerabilities.
- Delta: Dynamic security checks on synthetic, mutated samples, with no human baseline and no Solidity. The project uses real audit findings and human code as the baseline.

### RethinkSecGen2026 Rethinking the Evaluation of Secure Code Generation
- Authors: Shih-Chieh Dai, Jun Xu, Guanhong Tao; Year: 2026; Venue: ICSE 2026 (seen in the ICSE 2026 research track list on conf.researchr.org; arXiv comment confirms)
- URL opened: https://arxiv.org/abs/2503.15554 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N6
- Summary: The authors re-evaluate four secure code generation techniques by checking security and function on the same generated code, using three static analysers and two LLMs as vulnerability judges. Many techniques trade away function for security, some lower the base model's performance by more than 50%, and CodeQL misses several vulnerabilities.
- Delta: It shows why judging security with one static analyser misleads, which supports the project's use of executable PoVs. It studies generation methods, not agents against humans, and it does not confirm each LLM-judged finding with a test (N6).

### TowardSecGen2026 Toward Secure Code Generation: Bridging Correctness and Security via Task-Adaptive Vulnerability Modeling and Execution-Based Benchmarking
- Authors: Jiexin Wang et al.; Year: 2026; Venue: ISSTA 2026 (seen in the ISSTA 2026 research papers list on conf.researchr.org)
- URL opened: https://arxiv.org/abs/2407.02395 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N5 (in part)
- Summary: CodeSecEval has 255 Python tasks over 77 CWEs, each with paired insecure and secure versions and executable functional and security tests. The authors note that earlier benchmarks "leak mitigation details" and propose SecAwareCoder, an agent that models threats for the task and refines its code from execution feedback.
- Delta: Execution-based security tests on Python tasks, without a human baseline or Solidity. It names the problem of task text leaking the mitigation, which N5 addresses with a check on each feature request.

### Peng2026-CorrectNotSafe When "Correct" Is Not Safe: Can We Trust Functionally Correct Patches Generated by Code Agents?
- Authors: Yibo Peng et al.; Year: 2026; Venue: ACL 2026 (Volume 1: Long Papers), pp. 15514-15546
- URL opened: https://arxiv.org/abs/2510.17862 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N3
- Summary: The paper shows that code agents produce patches that pass every test but contain vulnerable code. Its FCV-Attack, which needs only black-box access and one query, works across 12 agent-model pairs on SWE-bench; for CWE-538 it succeeds 40.7% of the time on GPT-5 Mini with OpenHands.
- Delta: It shows that passing tests do not make a patch safe, which is the reason the project judges patches with PoVs. It studies an attack that induces the flaw, not agents compared with the human who wrote the same feature, and it does not use held-out exploits.

### MOSAIC2026 MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents
- Authors: Jonathan Steinberg, Oren Gal; Year: 2026; Venue: NeurIPS 2026 (seen in the NeurIPS 2026 paper list at neurips.cc; not yet in DBLP)
- URL opened: https://arxiv.org/abs/2605.03952 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N5, N6
- Summary: MOSAIC-Bench has 199 three-step chains of harmless-looking tickets that together produce an exploitable flaw, each with a deterministic exploit oracle on 10 web applications. Nine production coding agents complete the chains with 53-86% end-to-end attack success. Code-review agents approve 25.8% of these confirmed-vulnerable diffs as routine.
- Delta: It judges agent code with exploits and shows that reviewer agents miss flaws, which bears on N6. Its tickets are written on purpose to lead to a flaw, while the project's requests come from real features and are checked not to hint at the bug or the fix (N5). No human baseline and no Solidity.

### Zhang2025-BountyBench BountyBench: Dollar Impact of AI Agent Attackers and Defenders on Real-World Cybersecurity Systems
- Authors: Andy K. Zhang et al.; Year: 2025; Venue: NeurIPS 2025, Datasets and Benchmarks Track
- URL opened: https://arxiv.org/abs/2505.15216 (arXiv abstract page); part of the full text read at https://arxiv.org/html/2505.15216
- Status: VERIFIED
- Tier: B
- Touches: N3, N7
- Summary: BountyBench sets up 25 real systems with 40 bug bounties worth $10 to $30,485 and defines Detect, Exploit and Patch tasks. A patch must block the exploit and pass invariant checks (tests of the system's function) that the agent cannot see. Codex CLI with o3-high and with o4-mini reach 90% on Patch ($14,152 and $14,422 of bounty value), and Claude Code reaches 87.5%.
- Delta: Agents' patches are judged by exploits plus tests, and money is attached to results, but the dollars are bounty awards, not losses estimated per exploit (N7). It does not hold back some PoVs while showing one (N3), compare agents with the original developers (N1), or cover Solidity.

### Lee2025-SECbench SEC-bench: Automated Benchmarking of LLM Agents on Real-World Software Security Tasks
- Authors: Hwiwon Lee et al.; Year: 2025; Venue: NeurIPS 2025
- URL opened: https://arxiv.org/abs/2506.11791 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3, N4
- Summary: SEC-bench uses a multi-agent pipeline to build repositories with harnesses, reproduce vulnerabilities and create gold patches, at $0.87 per instance. It evaluates code agents on PoC generation and on vulnerability patching; the best agents reach 18.0% on PoC generation and 34.0% on patching.
- Delta: It covers both PoC writing and patching by agents on real vulnerabilities (the abstract does not name the languages). It does not show one PoV and hold back others (N3), vary what the agent is told and can run (N4), or compare with human developers (N1).

### Wang2026-CyberGym CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale
- Authors: Zhun Wang et al.; Year: 2026; Venue: ICLR 2026
- URL opened: https://arxiv.org/abs/2506.02548 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: CyberGym has 1,507 real vulnerabilities from 188 projects and asks agents to write a PoC test that reproduces each one from its text description and the codebase. The best agent-model pairs succeed on about 20%. The work also found 34 zero-day vulnerabilities and 18 historically incomplete patches.
- Delta: Agents write PoCs from vulnerability descriptions, which is close to how the project's PoVs are built from audit reports. It does not use PoVs to judge agent code or agent repairs, and it is not about Solidity.

### Zhong2026-ImpossibleBench ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases
- Authors: Ziqian Zhong, Aditi Raghunathan, Nicholas Carlini; Year: 2026; Venue: ICLR 2026
- URL opened: https://arxiv.org/abs/2510.20270 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: ImpossibleBench makes "impossible" versions of LiveCodeBench and SWE-bench tasks in which the unit tests contradict the specification, so any pass means the agent took a shortcut. It measures how often agents cheat, for example by deleting failing tests, and shows that the prompt, test access and the feedback loop change the cheating rate.
- Delta: It measures agents fitting the tests they are given, which the project observed in repair (agents fixed only the case the shown PoV hit). It does not study security repair, held-out PoVs, or repository tests that assert vulnerable behaviour.

### CodingDeceive2026 Do Coding Agents Deceive Us? Detecting and Preventing Cheating via Capped Evaluation with Randomized Tests
- Authors: Thanawat Lodkaew et al.; Year: 2026; Venue: NeurIPS 2026 (seen in the NeurIPS 2026 paper list at neurips.cc)
- URL opened: https://arxiv.org/abs/2606.07379 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4, N3
- Summary: CapCode builds coding datasets with randomized tests whose best honest score is capped below one, so scores above the cap reveal cheating. A reward design built on the same idea, CapReward, reduces cheating during training.
- Delta: It uses randomized hidden tests to catch agents that fit the evaluation. The project uses held-out PoVs for the same purpose in security repair; it does not train models.

### SolvedIssues2026 Are "Solved Issues" in SWE-bench Really Solved Correctly? An Empirical Study
- Authors: You Wang, Michael Pradel, Zhongxin Liu; Year: 2026; Venue: ICSE 2026 (seen in the ICSE 2026 research track list on conf.researchr.org; not yet in DBLP)
- URL opened: https://arxiv.org/abs/2503.15223 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: The authors test plausible patches from three issue-solving tools on SWE-bench Verified with PatchDiff, a differential patch testing technique. 7.8% of patches counted as correct fail the developers' full test suite, 29.6% behave differently from the ground-truth patch, and 28.6% of the divergent ones are certainly wrong. Together these inflate reported resolution rates by 6.2 percentage points.
- Delta: It shows that a patch passing the given tests can still be wrong, which motivates held-out PoVs (N3). It studies functional issues, not security, and finds wrong patches by differential testing instead of held-out exploits.

### Ahmed2026-TestOverfitSWE Investigating Test Overfitting on SWE-bench
- Authors: Toufique Ahmed et al.; Year: 2026; Venue: FSE 2026 Companion (SIGSOFT FSE Companion 2026), pp. 1292-1296 (arXiv v1 title "Is the Cure Still Worse Than the Disease? Test Overfitting by LLMs in Automated Program Repair")
- URL opened: https://arxiv.org/abs/2511.16858 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3, N4
- Summary: The paper studies test overfitting in issue resolution: code that passes the observed tests but misses cases or breaks function. The problem is worse because issues rarely come with executable tests, so systems generate tests from the issue and some refine code and tests together. The abstract gives no numbers.
- Delta: It studies the same failure the project saw when agents fixed only the case the shown PoV hit. It is about functional issues, not security, and it does not hold back exploits or vary the repair input.

### Yu2025-UTBoost UTBoost: Rigorous Evaluation of Coding Agents on SWE-Bench
- Authors: Boxi Yu et al.; Year: 2025; Venue: ACL 2025 (Volume 1: Long Papers), pp. 3762-3774
- URL opened: https://arxiv.org/abs/2506.09289 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: UTGenerator writes extra test cases for SWE-bench tasks, and UTBoost uses them to re-check patches. It found 36 tasks with weak tests and 345 wrong patches marked as passing, which changes 40.9% of SWE-Bench Lite and 24.4% of SWE-Bench Verified leaderboard entries.
- Delta: Extra tests reveal patches that only pass weak tests, which is the role held-out PoVs play in the project. It is about functional issues and uses generated tests, not exploits held back from the agent.

### Petke2024-PatchOverfit The Patch Overfitting Problem in Automated Program Repair: Practical Magnitude and a Baseline for Realistic Benchmarking
- Authors: Justyna Petke et al.; Year: 2024; Venue: FSE 2024 Companion (SIGSOFT FSE Companion 2024), pp. 452-456
- URL opened: https://api.crossref.org/works/10.1145/3663529.3663776 (Crossref record: title, authors, venue; no abstract). ACM DL returned HTTP 403, no arXiv version is in DBLP's arXiv records, and the web-search budget was used up.
- Status: UNVERIFIED (title, authors and venue confirmed in DBLP and Crossref; abstract not seen)
- Tier: B
- Touches: N3
- Summary: Not summarised; only the title, authors and venue were seen. The title says it measures how large patch overfitting is in practice and proposes a baseline for realistic benchmarking.
- Delta: From the title only [uncertain]: general program repair, not security repair with held-out PoVs.

### Aleithan2024-SWEBenchPlus SWE-Bench+: Enhanced Coding Benchmark for LLMs
- Authors: Reem Aleithan et al.; Year: 2024; Venue: arXiv preprint (2410.06992). The first author also has a 2-page paper in the ICSE 2025 Companion, "Revisiting SWE-Bench: On the Importance of Data Quality for LLM-Based Code Models" (seen in DBLP and Crossref; its text was not read).
- URL opened: https://arxiv.org/abs/2410.06992 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N5, N3
- Summary: The authors compare SWE-Agent with GPT-4's successful patches against the real pull requests. In 32.67% of them the solution was given in the issue report or its comments, and 31.08% passed only because the tests were weak. Removing these cases drops the resolution rate from 12.47% to 3.97%, and over 94% of the issues predate the models' knowledge cutoffs.
- Delta: It measures how often task text gives away the fix and how often weak tests pass wrong patches, two problems the project handles with checked feature requests (N5) and held-out PoVs (N3). It is about functional issue fixing, not security.

### Pearce2023-ZeroShotRepair Examining Zero-Shot Vulnerability Repair with Large Language Models
- Authors: Hammond Pearce et al.; Year: 2023; Venue: IEEE S&P 2023, pp. 2339-2356 (arXiv v1 title "Can OpenAI Codex and Other Large Language Models Help Us Fix Security Bugs?")
- URL opened: https://arxiv.org/abs/2112.02125 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: The authors study how prompt wording affects zero-shot vulnerability repair with five commercial LLMs, one open-source model and their own model, on synthetic, hand-made and real security bugs. The models together repaired all synthetic and hand-made scenarios, but real-world cases showed problems with producing functionally correct code.
- Delta: It varies the information in the repair prompt (N4) for one-shot LLM completion. It does not give the model a PoV, vary what it can run, or judge repairs with held-out exploits.

### Wu2023-NNVulnFix How Effective Are Neural Networks for Fixing Security Vulnerabilities
- Authors: Yi Wu et al.; Year: 2023; Venue: ISSTA 2023, pp. 1282-1294
- URL opened: https://arxiv.org/abs/2305.18607 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3, N4
- Summary: The authors compare five LLMs, four fine-tuned LLMs and four deep-learning repair tools on the Java benchmarks Vul4J and the new VJBench, and transform the code to reduce training-data overlap. The models fix few vulnerabilities; Codex fixes the most, 10.2 (20.4%).
- Delta: Learning-based repair of Java vulnerabilities on benchmarks with tests, plus a guard against training-data overlap. No agents with a terminal, no shown-versus-held-out PoVs, no Solidity.

### Hu2025-SoKAVR SoK: Automated Vulnerability Repair: Methods, Tools, and Assessments
- Authors: Yiwei Hu et al.; Year: 2025; Venue: USENIX Security Symposium 2025, pp. 4421-4440
- URL opened: https://arxiv.org/abs/2506.11697 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: The paper organises automated vulnerability repair by analysis, patch generation and patch validation. It builds Vul4C, a C/C++ benchmark of 144 vulnerabilities with their exploits and patches, and evaluates seven C/C++ tools on it and two Java tools on Vul4J.
- Delta: Exploit-based evaluation of repair tools on C/C++ and Java. It does not split exploits into shown and held-out, study agents' inputs (N4), or cover Solidity.

### Rashid2026-LogicEval LogicEval: A Systematic Framework for Evaluating Automated Repair Techniques for Logical Vulnerabilities in Real-World Software
- Authors: Syed Md Mukit Rashid et al.; Year: 2026; Venue: ACL 2026 (Volume 1: Long Papers), pp. 46025-46049
- URL opened: https://arxiv.org/abs/2604.12994 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3, N4, N2 (in part)
- Summary: The authors build LogicDS, 122 real logical vulnerabilities (flaws in program logic, not memory safety), and LogicEval, a framework to evaluate patches for them with traditional and LLM-based repair. Failures come mostly from prompt sensitivity, lost code context and difficulty finding where to patch.
- Delta: Repair of logic bugs, the bug class the project targets, but outside Solidity and without held-out PoVs or a comparison of what the agent is told and can run.

### Parasaram2025-FactSelection The Fact Selection Problem in LLM-Based Program Repair
- Authors: Nikhil Parasaram et al.; Year: 2025; Venue: ICSE 2025, pp. 2574-2586
- URL opened: https://arxiv.org/abs/2404.05520 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: Over 19K prompts with combinations of seven facts (such as stack traces, issues and angelic values) are used to fix 314 BugsInPy bugs. Each fact helps some bugs, but too many facts make results worse; a per-bug fact selector, Maniple, repairs 88 of 157 test bugs, 17% above the best fixed fact set.
- Delta: It shows that what the model is told changes repair success in a non-monotonic way (N4). It is functional repair in Python, one-shot prompting, with no PoV, no execution variation and no security judge.

### WellBegun2026 Well Begun is Half Done: Location-Aware and Trace-Guided Iterative Automated Vulnerability Repair
- Authors: Zhenlei Ye et al.; Year: 2026; Venue: ICSE 2026 (arXiv comment "Accepted by ICSE 2026"; listed as a Distinguished Paper in the research track list on conf.researchr.org)
- URL opened: https://arxiv.org/abs/2512.20203 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4, N3
- Summary: The approach first tells the LLM where to patch, then repeats repair while ranking test-failing candidates by whether they add new vulnerabilities and by taint-statement coverage. On VulnLoc+, 40 C/C++ vulnerabilities with their PoVs, it produces 27 plausible patches and repairs 8 to 13 more vulnerabilities correctly than the baselines.
- Delta: It uses location information and PoVs in iterative repair, both inputs in N4. It does not hold some PoVs back to judge the repair, compare inputs as a controlled study, or work on Solidity.

### OSSFuzzAgentic2026 Fixing Security Vulnerabilities with Agentic AI in OSS-Fuzz
- Authors: Yuntong Zhang et al.; Year: 2026; Venue: ICSE 2026 (title as seen in the ICSE 2026 research track list on conf.researchr.org); arXiv version titled "Fixing Security Vulnerabilities with AI in OSS-Fuzz"
- URL opened: https://arxiv.org/abs/2411.03346 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4, N3
- Summary: The authors adapt the AutoCodeRover agent to fix OSS-Fuzz vulnerabilities, using the execution of the exploit input to find the code to change. Agent autonomy helped compared with fixed workflows such as Agentless. Patches with high CodeBLEU similarity to the reference still failed on the exploit input, so the authors argue that security patches must be judged by running them.
- Delta: An agent that is given the exploit input and judged by running it, close to the "shown PoV" condition in N4. It does not hold other exploits back to catch shallow fixes, vary the input systematically, or work on Solidity.

### OldWine2026 Just Old Wine in a New Bottle: Improving Vulnerability Repair Robustness to Combat Homologous but Heterogeneous Vulnerabilities
- Authors: [not seen]; Year: 2026; Venue: ISSTA 2026 (title seen in the ISSTA 2026 research papers list on conf.researchr.org)
- URL opened: https://conf.researchr.org/track/issta-2026/issta-2026-research-papers (accepted-paper list; title only)
- Status: UNVERIFIED (no arXiv version in DBLP's arXiv records; no DOI page found; web-search and OpenAlex budgets used up)
- Tier: B
- Touches: N3
- Summary: Not summarised; only the title was seen. The title says it makes vulnerability repair robust to related vulnerabilities that differ in form.
- Delta: From the title only [uncertain]: a repair that fixes one variant but not a related one is the failure that held-out PoVs detect (N3). Check the paper before citing.

### SymRadar2026 SymRadar: PoC-Centered Bounded Verification for Vulnerability Repair
- Authors: [not seen]; Year: 2026; Venue: ICSE 2026 (title seen in the ICSE 2026 research track list on conf.researchr.org)
- URL opened: https://conf.researchr.org/track/icse-2026/icse-2026-research-track (accepted-paper list; title only)
- Status: UNVERIFIED (no arXiv version in DBLP's arXiv records; ICSE 2026 not yet in DBLP; web-search budget used up)
- Tier: B
- Touches: N3
- Summary: Not summarised; only the title was seen. The title says it verifies vulnerability repairs, in a bounded way, starting from the PoC.
- Delta: From the title only [uncertain]: it checks repairs beyond the single PoC, which is what held-out PoVs do in N3. Check the paper before citing.

### TraceGate2026 TraceGate: A Framework for Policy-Controlled Failure Evidence in LLM-Assisted Program Repair
- Authors: [not seen]; Year: 2026; Venue: ASE 2026 (title seen in the ASE 2026 research track list on conf.researchr.org)
- URL opened: https://conf.researchr.org/track/ase-2026/ase-2026-research-track (accepted-paper list; title only)
- Status: UNVERIFIED (no arXiv version in DBLP's arXiv records; ASE 2026 not yet in DBLP; web-search budget used up)
- Tier: B
- Touches: N4
- Summary: Not summarised; only the title was seen. The title says it controls which failure evidence an LLM sees during program repair.
- Delta: From the title only [uncertain]: controlling which failure evidence the model sees is the "what it is told" dimension of N4. Check the paper before citing.

### Wang2026-PromptPoison Is your prompt poisoning code? Defect induction rates and security mitigation strategies
- Authors: Bin Wang et al.; Year: 2026; Venue: Empirical Software Engineering 31(6), article 172
- URL opened: https://link.springer.com/article/10.1007/s10664-026-10866-8 (Springer article page); also https://arxiv.org/abs/2510.22944 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: The authors rate prompt quality by goal clarity, information completeness and logical consistency, and release CWE-BENCH-PYTHON with prompts at four quality levels (L0 to L3). As prompt quality drops, LLMs produce insecure code more often; Chain-of-Thought and Self-Correction reduce the effect.
- Delta: It shows that the wording of a benign request changes the security of the code. N5 controls a different aspect of wording: the request must not hint at the bug or the fix, so that the result measures what the agent knows, not what the request told it.

### Peng2025-SolEval SolEval: Benchmarking Large Language Models for Repository-level Solidity Smart Contract Generation
- Authors: Zhiyuan Peng et al.; Year: 2025; Venue: EMNLP 2025 (Main Conference), pp. 4388-4411
- URL opened: https://arxiv.org/abs/2502.18793 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N2
- Summary: SolEval has 1,507 samples from 28 Solidity repositories in 6 domains, with metrics for gas cost (Gas@k) and vulnerabilities (Vul@k). The best of 16 LLMs reaches only 26.29% Pass@10, and fine-tuning Qwen-7B on SolEval raises Pass@5 from 16.67% to 58.33%.
- Delta: Repository-level Solidity generation with a vulnerability metric. It does not start from a vulnerability-introducing commit, compare with the human's version, or judge security with exploits; the project does all three.

### Ye2025-SolContractEval SolContractEval: A Benchmark for Evaluating Contract-Level Solidity Code Generation
- Authors: Zhifan Ye et al.; Year: 2025; Venue: ASE 2025, pp. 2858-2869
- URL opened: https://arxiv.org/abs/2509.23824 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N1, N2
- Summary: SolContractEval has 124 contract-level tasks from real on-chain contracts in nine domains, checked for function by replaying historical transactions. Claude-3.7-Sonnet performs best; models do well on standard patterns but struggle with complex logic and dependencies between contracts.
- Delta: Function-level correctness of LLM Solidity, judged by transaction replay. It does not measure security against a human baseline or use exploits.

### Chen2026-AutoSCGen Towards Automated Smart Contract Generation: Evaluation, Benchmarking, and Retrieval-Augmented Repair
- Authors: Zaoyu Chen et al.; Year: 2026; Venue: FSE 2026 (Proc. ACM Softw. Eng. 3(FSE), pp. 116-137)
- URL opened: https://arxiv.org/abs/2503.01098 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N2
- Summary: SolBench has 28,825 functions from 7,604 Etherscan contracts and checks function by differential fuzzing; 14 LLMs are tested. The main failure is missing contract information such as state variables, and a retrieval-augmented repair method uses compiler and runtime errors to fetch only the snippets needed.
- Delta: Function-level Solidity generation judged for correctness, not security. The project measures security against the human's code with exploits.

### Wang2024-ContractTinker ContractTinker: LLM-Empowered Vulnerability Repair for Real-World Smart Contracts
- Authors: Che Wang et al.; Year: 2024; Venue: ASE 2024 (4-page tool paper), pp. 2350-2353
- URL opened: https://arxiv.org/abs/2409.09661 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N2, N3
- Summary: ContractTinker repairs real-world smart-contract vulnerabilities found by audits, using chain-of-thought steps guided by static analysis. On 48 high-risk vulnerabilities, 23 patches (48%) are valid and 10 (21%) need small changes.
- Delta: LLM repair of audited Solidity bugs, judged by hand, not by exploits. No held-out PoVs (N3), no input study (N4), no agents.

### Zhang2025-ACFix ACFix: Guiding LLMs With Mined Common RBAC Practices for Context-Aware Repair of Access Control Vulnerabilities in Smart Contracts
- Authors: Lyuye Zhang et al.; Year: 2025; Venue: IEEE Transactions on Software Engineering 51(9), pp. 2512-2532
- URL opened: https://arxiv.org/abs/2403.06838 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N2, N3
- Summary: ACFix mines 49 common role-permission pairs from 344,251 on-chain contracts and uses them to guide GPT-4 in repairing access-control vulnerabilities, with a check of each patch's validity and effectiveness. It repairs 94.92% of 118 real-world cases, against 52.54% for plain GPT-4.
- Delta: LLM repair of one Solidity bug class, checked by the tool's own validity check. The project judges repairs of business-logic bugs with held-out PoVs and studies the agent's inputs.

### PoCo2026 PoCo: Agentic Proof-of-Concept Exploit Generation for Smart Contracts
- Authors: Vivi Andersson, Sofia Bobadilla, Harald Hobbelhagen, Martin Monperrus; Year: 2026; Venue: ASE 2026 (seen in the ASE 2026 research track list on conf.researchr.org; arXiv comment says "Under review")
- URL opened: https://arxiv.org/abs/2511.02780 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N2, N3
- Summary: PoCo is an agent that writes executable Foundry PoC exploits from auditors' natural-language vulnerability descriptions, using code-execution tools in a reason, act and observe loop. On 23 real vulnerability reports it beats zero-shot and fixed-workflow baselines.
- Delta: It automates building Foundry PoVs from audit reports, a step the project does to make its judges. It does not use the PoCs to judge agent-written code or repairs, or compare agents with humans.

### Sun2025-ExploitMigration Learning from the Past: Real-World Exploit Migration for Smart Contract PoC Generation
- Authors: Kairan Sun et al.; Year: 2025; Venue: ASE 2025, pp. 52-64
- URL opened: https://api.crossref.org/works/10.1109/ASE63991.2025.00013 (Crossref record: title, authors, venue; no abstract). IEEE Xplore returned nothing and no arXiv version is in DBLP's arXiv records.
- Status: UNVERIFIED (title, authors and venue confirmed in DBLP and Crossref; abstract not seen)
- Tier: B
- Touches: N2, N3
- Summary: Not summarised; only the title, authors and venue were seen. The title says it generates smart-contract PoCs by adapting past real-world exploits.
- Delta: From the title only [uncertain]: PoC generation for smart contracts, a step in building the project's PoVs.

### Wei2025-VeriExploit VeriExploit: Automatic Bug Reproduction in Smart Contracts via LLMs and Formal Methods
- Authors: Chenfeng Wei et al.; Year: 2025; Venue: ASE 2025, pp. 1415-1426
- URL opened: https://api.crossref.org/works/10.1109/ASE63991.2025.00120 (Crossref record: title, authors, venue; no abstract). IEEE Xplore returned nothing and no arXiv version is in DBLP's arXiv records.
- Status: UNVERIFIED (title, authors and venue confirmed in DBLP and Crossref; abstract not seen)
- Tier: B
- Touches: N2, N3
- Summary: Not summarised; only the title, authors and venue were seen. The title says it reproduces smart-contract bugs with LLMs and formal methods.
- Delta: From the title only [uncertain]: automatic bug reproduction for smart contracts, close to the project's PoV construction.

### Ye2026-ChainDelta ChainDelta: Automatic Patch-Based Exploit Generation for Ethereum with Fuzzing Agents
- Authors: Mingxi Ye et al.; Year: 2026; Venue: FSE 2026 (Proc. ACM Softw. Eng. 3(FSE), pp. 3392-3414)
- URL opened: https://api.crossref.org/works/10.1145/3808157 (Crossref record with the abstract deposited by ACM). ACM DL returned HTTP 403 and no arXiv version is in DBLP's arXiv records.
- Status: VERIFIED (via the Crossref record of the DOI, which shows title, authors and abstract)
- Tier: B
- Touches: N2, N3
- Summary: ChainDelta generates exploits for Ethereum 1-day vulnerabilities from their security patches, using an LLM-driven directed fuzzer, an agent that sets up blockchain state, and a sanitizer that separates real inconsistencies from benign non-determinism. It generates exploits for 64% of cases with a 15.8% false-positive rate and found four undisclosed vulnerabilities. The authors say such exploits help detect incomplete patches.
- Delta: Exploits derived from patches can expose incomplete fixes, the job held-out PoVs do in N3. Its targets are Ethereum client patches, not agent repairs of contract code, and it does not study agents' repair inputs.

### TracePoC2026 Trace-Driven Automated PoC Synthesis for On-Chain Attacks
- Authors: Xing Su et al. (arXiv version); Year: 2026; Venue: ASE 2026 (title seen in the ASE 2026 research track list on conf.researchr.org); arXiv version titled "From Transactions to Exploits: Automated PoC Synthesis for Real-World DeFi Attacks" [uncertain that the two are the same paper; topic and approach match]
- URL opened: https://arxiv.org/abs/2601.16681 (arXiv abstract page)
- Status: VERIFIED (arXiv version); venue link [uncertain]
- Tier: B
- Touches: N2, N7
- Summary: TracExp rebuilds attacker logic from on-chain transaction traces and has an LLM write executable PoCs. On 321 real attacks from 20 months it produces PoCs for 93% of incidents, 58.78% directly verifiable, at about $0.07 each.
- Delta: It reproduces real DeFi attacks as executable PoCs, a source of exploits with known losses. It does not use them to judge agent code or repairs.

### Simsek2026-PoCGen PoCGen: Generating Proof-of-Concept Exploits for Vulnerabilities in Npm Packages
- Authors: Deniz Simsek, Aryaz Eghbali, Michael Pradel; Year: 2026; Venue: FSE 2026 (Proc. ACM Softw. Eng. 3(FSE), pp. 3887-3908)
- URL opened: https://arxiv.org/abs/2506.04962 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: PoCGen combines LLMs, static taint analysis and dynamic checks to write and validate PoC exploits from informal npm vulnerability reports. It succeeds on 77% of SecBench.js vulnerabilities, 45 points above a baseline, at about $0.02 per exploit.
- Delta: PoC generation from vulnerability reports, the same step the project uses to build PoVs from audit reports, but for npm packages and without using PoCs to judge agents.

### Ullah2024-LLMsCannot LLMs Cannot Reliably Identify and Reason About Security Vulnerabilities (Yet?): A Comprehensive Evaluation, Framework, and Benchmarks
- Authors: Saad Ullah et al.; Year: 2024; Venue: IEEE S&P 2024, pp. 862-880
- URL opened: https://arxiv.org/abs/2312.12575 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: SecLLMHolmes tests eight LLMs on 228 code scenarios. The models give non-deterministic answers and unfaithful reasoning, and changing function or variable names or adding library functions flips the answers of PaLM2 and GPT-4 in 26% and 17% of cases.
- Delta: It shows that an LLM security review alone is unreliable, which is why N6 confirms each reported flaw with a PoV. It does not review agent code against human code.

---

## Tier C: background

### AgentLens2026 AgentLens: Revealing The Lucky Pass Problem in SWE-Agent Evaluation
- Authors: Priyam Sahoo et al.; Year: 2026; Venue: NeurIPS 2026 (seen in the NeurIPS 2026 paper list at neurips.cc)
- URL opened: https://arxiv.org/abs/2605.12925 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3, N4
- Summary: On 1,815 OpenHands trajectories for SWE-bench Verified tasks, 10.7% of passing runs show poor process such as blind retries or no verification. Ranking models by process quality instead of pass rate moves some by up to five places.

### SoK2025-EffectiveAVR SoK: Towards Effective Automated Vulnerability Repair
- Authors: Ying Li et al.; Year: 2025; Venue: USENIX Security Symposium 2025, pp. 4441-4462
- URL opened: https://arxiv.org/abs/2501.18820 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: A survey and benchmark of vulnerability repair methods grouped as template-guided, search-based, constraint-based and learning-driven. No approach is best overall, and all struggle with complex vulnerabilities.

### ExecFree2024 Execution-Free Program Repair
- Authors: Li Huang et al.; Year: 2024; Venue: FSE 2024 Companion (SIGSOFT FSE Companion 2024), pp. 517-521
- URL opened: https://arxiv.org/abs/2405.01309 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: Proof2Fix repairs programs with a program prover instead of running tests or the program. It fixes significant historical bugs.

### Cheng2026-ReproTestRepair Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair
- Authors: Runxiang Cheng et al.; Year: 2026; Venue: FSE 2026 Companion (SIGSOFT FSE Companion 2026), pp. 644-654
- URL opened: https://arxiv.org/abs/2601.19066 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3, N4
- Summary: On 120 human-reported bugs at Google, a repair agent asked to write both a fix and a bug reproduction test produces such tests for as many bugs as a dedicated test agent, without fewer plausible fixes.

### Yu2026-SmartCoderR1 SmartCoder-R1: Towards Secure and Explainable Smart Contract Generation with Security-Aware Group Relative Policy Optimization
- Authors: Lei Yu et al.; Year: 2026; Venue: FSE 2026 (Proc. ACM Softw. Eng. 3(FSE), pp. 2165-2188); arXiv title without the "SmartCoder-R1:" prefix
- URL opened: https://arxiv.org/abs/2509.09942 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: A Qwen2.5-Coder-7B model trained with continued pre-training, reasoning fine-tuning and a security-aware reinforcement learning reward writes Solidity functions. On 756 real functions it reports an 8.60% vulnerability rate and a 50.53% rate of code that is both functional and secure.

### Peng2025-PrefGen PrefGen: A Preference-Driven Methodology for Secure Yet Gas-Efficient Smart Contract Generation
- Authors: Zhiyuan Peng et al.; Year: 2025; Venue: ASE 2025, pp. 317-329; arXiv title "A Preference-Driven Methodology for High-Quality Solidity Code Generation"
- URL opened: https://arxiv.org/abs/2506.03006 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: PrefGen extends preference optimization with blockchain metrics to make generated Solidity correct, gas-efficient and secure. It reports 66.7% Pass@5, 58.9% Gas@5 and 62.5% Secure@5.

### Wen2024-FORAY FORAY: Towards Effective Attack Synthesis against Deep Logical Vulnerabilities in DeFi Protocols
- Authors: Hongbo Wen et al.; Year: 2024; Venue: ACM CCS 2024, pp. 1001-1015
- URL opened: https://arxiv.org/abs/2407.06348 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2, N7
- Summary: FORAY lifts DeFi contracts into a language of financial operations and a token flow graph, then synthesizes attacks such as price manipulation with SMT solving. It targets deep logic bugs that span several contracts.

### PAGENT2026 PAGENT: Program Analysis Guided LLM Agent for Proof-of-Concept Generation
- Authors: Achintya Desai et al.; Year: 2026; Venue: ISSTA 2026 (seen in the ISSTA 2026 research papers list on conf.researchr.org); arXiv title "Program Analysis Guided LLM Agent for Proof-of-Concept Generation"
- URL opened: https://arxiv.org/abs/2604.07624 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: PAGENT adds static analysis and sanitizer-based profiling and coverage to a PoC-generation agent. It beats the previous best agentic approach by 132% on PoC generation.

### Wang2025-AligningPoC Aligning Core Aspects: Improving Vulnerability Proof-of-Concepts via Cross-Source Insights
- Authors: Lingxiao Wang et al.; Year: 2025; Venue: FSE 2025 Companion (SIGSOFT FSE Companion 2025), pp. 1774-1777
- URL opened: https://arxiv.org/abs/2508.18109 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: Of 173,170 PoC reports from four platforms, every report misses at least one of eight key aspects. Combining sources completes 69,583 reports (40.18%).

### CVEGenie2026 CVE-Genie: An LLM-Based Multi-Agent Framework for Reproducing CVEs
- Authors: Saad Ullah et al.; Year: 2026; Venue: CCS 2026 (seen in the CCS 2026 accepted papers list at sigsac.org); arXiv title "From CVE Entries to Verifiable Exploits: An Automated Multi-Agent Framework for Reproducing CVEs"
- URL opened: https://arxiv.org/abs/2509.01835 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: Given a CVE entry, CVE-Genie rebuilds the vulnerable environment and produces a verifiable exploit. It reproduces 428 of 841 CVEs from 2024-2025 at $2.77 each.

### PBFuzz2026 PBFuzz: Agentic Directed Fuzzing for PoV Generation
- Authors: Haochen Zeng et al.; Year: 2026; Venue: CCS 2026 (seen in the CCS 2026 accepted papers list at sigsac.org)
- URL opened: https://arxiv.org/abs/2512.04611 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: An agent extracts reachability and triggering constraints from code and encodes them as property-based tests to generate PoV inputs. On Magma it triggers 57 vulnerabilities within 30 minutes per target, 17 that no other fuzzer exposed.

### Jin2025-ScriptKiddies Good News for Script Kiddies? Evaluating Large Language Models for Automated Exploit Generation
- Authors: David Jin, Qian Fu, Yuekang Li; Year: 2025; Venue: IEEE Security and Privacy Workshops (SPW) 2025, pp. 278-282
- URL opened: https://arxiv.org/abs/2505.01065 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: GPT-4 and GPT-4o readily cooperate with exploit-generation requests, but no model produced a working exploit for refactored versions of five security labs.

### Peng2025-iCodeReviewer iCodeReviewer: Improving Secure Code Review with Mixture of Prompts
- Authors: Yun Peng et al.; Year: 2025; Venue: ASE 2025, pp. 3204-3215
- URL opened: https://arxiv.org/abs/2510.12186 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N6
- Summary: An LLM security code reviewer routes code to prompt pipelines that each check one security issue. It reaches an F1 of 63.98% on an internal dataset, and up to 84% of its comments were accepted in production.

### SecureReviewer2026 SecureReviewer: Enhancing Large Language Models for Secure Code Review through Secure-Aware Fine-Tuning
- Authors: Fang Liu et al.; Year: 2026; Venue: ICSE 2026 (arXiv comment "Accepted by ICSE 2026")
- URL opened: https://arxiv.org/abs/2510.26457 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N6
- Summary: The authors fine-tune LLMs on a new secure code review dataset, ground comments with retrieval, and propose a metric, SecureBLEU, for security review comments.

### Lin2026-AgentsVsPros Comparing AI Agents to Cybersecurity Professionals in Real-World Penetration Testing
- Authors: Justin W. Lin et al.; Year: 2026; Venue: ICLR 2026
- URL opened: https://arxiv.org/abs/2512.09882 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N1 (agent against human, outside coding)
- Summary: Ten professionals and seven agents test a university network of about 8,000 hosts. The authors' agent ARTEMIS finds 9 valid vulnerabilities and beats 9 of the 10 humans, while agents such as Codex do worse than most humans.

### Mundler2024-SWTBench SWT-Bench: Testing and Validating Real-World Bug-Fixes with Code Agents
- Authors: Niels Mündler et al.; Year: 2024; Venue: NeurIPS 2024
- URL opened: https://arxiv.org/abs/2406.12952 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: Code agents turn GitHub issues into tests that fail before the fix and pass after it. Such tests filter proposed fixes and double SWE-Agent's precision.

### Zhu2025-CVEBench CVE-Bench: A Benchmark for AI Agents' Ability to Exploit Real-World Web Application Vulnerabilities
- Authors: Yuxuan Zhu et al.; Year: 2025; Venue: ICML 2025 (PMLR 267)
- URL opened: https://arxiv.org/abs/2503.17332 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: A sandbox benchmark of critical web-application CVEs that agents must exploit. The best agent framework exploits up to 13%.

### ExploitGym2026 ExploitGym: Can AI Agents Turn Security Vulnerabilities into Real Attacks?
- Authors: Zhun Wang et al.; Year: 2026; Venue: NeurIPS 2026 (seen in the NeurIPS 2026 paper list at neurips.cc)
- URL opened: https://arxiv.org/abs/2605.11086 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: Given an input that triggers a vulnerability, agents must extend it into a working exploit; 898 instances span userspace programs, V8 and the Linux kernel. The strongest models produce working exploits for 157 and 120 instances.

### Osebe2026-AutoSUIT AutoSUIT Bench - Automated Security UnIt Test Benchmark for LLM Coding
- Authors: Samuel Osebe et al.; Year: 2026; Venue: Findings of ACL 2026, pp. 34759-34783
- URL opened: https://aclanthology.org/2026.findings-acl.1735/ (ACL Anthology page)
- Status: VERIFIED
- Tier: C
- Touches: N1, N3
- Summary: An automated, self-validating pipeline builds security unit tests over 232 CWEs in C/C++, Java and Python for generation, completion and patching tasks. Functional pass rates are always higher than security pass rates.

### AutoBaxBuilder2026 AutoBaxBuilder: Bootstrapping Code Security Benchmarking
- Authors: Tobias von Arx et al.; Year: 2026; Venue: ICML 2026 (arXiv comment "ICML 2026"; in the ICML 2026 paper list)
- URL opened: https://arxiv.org/abs/2512.21132 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N1, N3
- Summary: An LLM pipeline creates new code-security tasks with functional tests and end-to-end exploits, in under 2 hours and under $4 per task. It reduces the human effort of building such a benchmark by a factor of 12.

### Mou2025-CoVEval Can You Really Trust Code Copilots? Evaluating Large Language Models from a Code Security Perspective
- Authors: Yutao Mou et al.; Year: 2025; Venue: ACL 2025 (Volume 1: Long Papers), pp. 17349-17369
- URL opened: https://arxiv.org/abs/2505.10494 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N1, N6
- Summary: CoV-Eval covers code completion, vulnerability repair, detection and classification for 20 LLMs, with a judge model, VC-Judge, aligned to human experts. Models spot vulnerable code well but still write insecure code and repair poorly.

### Tihanyi2025-HowSecure How secure is AI-generated code: a large-scale comparison of large language models
- Authors: Norbert Tihanyi et al.; Year: 2025; Venue: Empirical Software Engineering 30(2), article 47
- URL opened: https://link.springer.com/article/10.1007/s10664-024-10590-1 (Springer article page)
- Status: VERIFIED
- Tier: C
- Touches: N1
- Summary: FormAI-v2 has 331,000 compilable C programs from 9 LLMs, labelled by bounded model checking (ESBMC). At least 62.07% of the programs are vulnerable, with small differences between models.

### Tony2025-Prompting Prompting Techniques for Secure Code Generation: A Systematic Investigation
- Authors: Catherine Tony et al.; Year: 2025; Venue: ACM TOSEM 34(8), article 225
- URL opened: https://arxiv.org/abs/2407.07064 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N5
- Summary: A literature review lists prompting techniques for code generation, and a subset is tested on GPT-3, GPT-3.5 and GPT-4 with 150 security-relevant prompts. Recursive Criticism and Improvement reduces security weaknesses the most.

### GoodVibe2026 GoodVibe: Security-by-Vibe for LLM-Based Code Generation
- Authors: Maximilian Thang et al.; Year: 2026; Venue: USENIX Security Symposium 2026
- URL opened: https://www.usenix.org/conference/usenixsecurity26/presentation/thang (USENIX paper page)
- Status: VERIFIED
- Tier: C
- Touches: N1
- Summary: GoodVibe fine-tunes only the neurons linked to security reasoning so that code models write secure code by default in informal "vibe coding" use. It improves code security up to 2.5 times over base models on six LLMs while training over 4,700 times fewer parameters than full fine-tuning.

### Bouzenia2025-PatchAgent PatchAgent: A Practical Program Repair Agent Mimicking Human Expertise
- Authors: Zheng Yu et al.; Year: 2025; Venue: USENIX Security Symposium 2025, pp. 4381-4400
- URL opened: https://www.usenix.org/conference/usenixsecurity25/presentation/yu-zheng (USENIX paper page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: Given a concrete input that triggers a vulnerability, PatchAgent localises the fault, writes a patch and validates it without breaking existing tests. It repairs over 90% of 178 real vulnerabilities.

### Zhou2024-VulMaster Out of Sight, Out of Mind: Better Automatic Vulnerability Repair by Broadening Input Ranges and Sources
- Authors: Xin Zhou et al.; Year: 2024; Venue: ICSE 2024, article 88; arXiv title "Multi-LLM Collaboration + Data-Centric Innovation = 2x Better Vulnerability Repair" (the arXiv comment confirms the ICSE 2024 title)
- URL opened: https://arxiv.org/abs/2401.15459 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: VulMaster feeds the repair model the full vulnerable code, code structure and CWE knowledge, with ChatGPT filling in missing inputs for a fine-tuned CodeT5. On 5,800 C/C++ functions, exact match rises from 10.2% to 20.0%.

### Xia2024-ChatRepair Automated Program Repair via Conversation: Fixing 162 out of 337 Bugs for $0.42 Each using ChatGPT
- Authors: Chunqiu Steven Xia, Lingming Zhang; Year: 2024; Venue: ISSTA 2024, pp. 819-831 (arXiv title "Keep the Conversation Going: Fixing 162 out of 337 bugs for $0.42 each using ChatGPT")
- URL opened: https://arxiv.org/abs/2304.00385 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: ChatRepair feeds test-failure information back to ChatGPT in a conversation and learns from earlier failed and plausible patches. It fixes 162 of 337 bugs at about $0.42 each.

### Olausson2024-SelfRepair Is Self-Repair a Silver Bullet for Code Generation?
- Authors: Theo X. Olausson et al.; Year: 2024; Venue: ICLR 2024
- URL opened: https://arxiv.org/abs/2306.09896 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: When the cost of repair is counted, self-repair with execution feedback gives modest and uneven gains for Code Llama, GPT-3.5 and GPT-4. Better feedback, from a stronger model or a human, helps much more.

### Fei2025-PatchSurvey Patch Correctness Assessment: A Survey
- Authors: Zhiwei Fei et al.; Year: 2025; Venue: ACM TOSEM 34(2), article 55
- URL opened: https://api.crossref.org/works/10.1145/3702972 (Crossref record with the abstract deposited by ACM). ACM DL returned HTTP 403 and no arXiv version is in DBLP's arXiv records.
- Status: VERIFIED (via the Crossref record of the DOI, which shows title, authors and abstract)
- Tier: C
- Touches: N3
- Summary: A survey of methods that judge whether a patch that passes the tests is really correct, the patch overfitting problem. It classifies techniques and datasets and reviews evaluation metrics.

### RethinkFTAVR2026 Rethinking the Capability of Fine-Tuned Language Models for Automated Vulnerability Repair
- Authors: Woorim Han et al.; Year: 2026; Venue: ICSE 2026 (arXiv comment "To appear at ICSE 2026")
- URL opened: https://arxiv.org/abs/2512.22633 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: Fine-tuned vulnerability repair models overfit their training data, are often evaluated on overlapping splits, and are judged by token-match metrics. The authors introduce L-AVRBench, a test-based benchmark.

### OneNotEnough2026 One Is Not Enough: The Untold Story of Multiple Security Patches for One Vulnerability
- Authors: Fangyuan Zhang et al.; Year: 2026; Venue: ASE 2026 (arXiv journal reference: Proceedings of the 41st IEEE/ACM International Conference on Automated Software Engineering)
- URL opened: https://arxiv.org/abs/2609.07224 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: 20.6% of patched CVEs need more than one security patch; the authors build a dataset of 6,053 such CVEs with 16,260 patches and a taxonomy of why. A missing patch leaves the fix partial.

### AbstainValidate2026 Abstain and Validate: A Dual-LLM Policy for Reducing Noise in Agentic Program Repair
- Authors: José Cambronero et al.; Year: 2026; Venue: ICSE 2026, Software Engineering in Practice track (arXiv comment and journal reference)
- URL opened: https://arxiv.org/abs/2510.03217 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: At Google, an LLM policy that skips bugs the agent is unlikely to fix, and another that rejects doubtful patches, raise success rates by up to 39 percentage points combined on 174 human-reported bugs.

### MagicThree2026 Is Three the Magic Number? An Empirical Evaluation of LLM-Based Repair Loops
- Authors: Tobias Kiecker et al.; Year: 2026; Venue: ASE 2026 (NIER paper per the arXiv comment; seen in the ASE 2026 research track page on conf.researchr.org)
- URL opened: https://arxiv.org/abs/2607.05197 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: Across code generation, test generation and translation, the first three or four repair iterations give most of the gains. How feedback is designed matters more than which model is used.

### Bouzenia2025-Trajectories Understanding Software Engineering Agents: A Study of Thought-Action-Result Trajectories
- Authors: Islem Bouzenia, Michael Pradel; Year: 2025; Venue: ASE 2025, pp. 2846-2857
- URL opened: https://arxiv.org/abs/2506.18824 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: The authors study 120 trajectories and 2,822 LLM interactions of RepairAgent, AutoCodeRover and OpenHands, and describe action patterns that separate successful from failed runs.

### Jimenez2024-SWEbench SWE-bench: Can Language Models Resolve Real-world Github Issues?
- Authors: Carlos E. Jimenez et al.; Year: 2024; Venue: ICLR 2024
- URL opened: https://arxiv.org/abs/2310.06770 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: 2,294 problems from real GitHub issues and pull requests in 12 Python repositories, checked with the repositories' tests. At release the best model, Claude 2, solved 1.96%.

### Yang2024-SWEagent SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering
- Authors: John Yang et al.; Year: 2024; Venue: NeurIPS 2024
- URL opened: https://arxiv.org/abs/2405.15793 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: A custom interface for editing files, navigating repositories and running tests raises an agent's SWE-bench pass@1 to 12.5%.

### Wang2025-OpenHands OpenHands: An Open Platform for AI Software Developers as Generalist Agents
- Authors: Xingyao Wang et al.; Year: 2025; Venue: ICLR 2025
- URL opened: https://arxiv.org/abs/2407.16741 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4 (tool used by the project)
- Summary: OpenHands (formerly OpenDevin) is an open platform for agents that write code, use a command line and browse the web in a sandbox. It is evaluated on 15 benchmarks including SWE-bench.

### Zhou2026-FeatureBench FeatureBench: Benchmarking Agentic Coding for Complex Feature Development
- Authors: Qixing Zhou et al.; Year: 2026; Venue: ICLR 2026
- URL opened: https://arxiv.org/abs/2602.10975 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N1 (feature tasks)
- Summary: FeatureBench derives feature-level tasks from repositories by tracing unit tests along a dependency graph, checking that other features still work after the feature is removed. Version one has 200 tasks from 24 repositories.

### Badertdinov2025-SWErebench SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents
- Authors: Ibragim Badertdinov et al.; Year: 2025; Venue: NeurIPS 2025, Datasets and Benchmarks Track
- URL opened: https://arxiv.org/abs/2505.20411 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none (training-data contamination, relevant to the project's choice of models)
- Summary: A pipeline collects over 21,000 fresh Python tasks from GitHub. Comparing results on fresh tasks with SWE-bench Verified suggests that some models' scores are inflated by contamination.

### SWEIllusion2026 The SWE-Bench Illusion: When State-of-the-Art LLMs Remember Instead of Reason
- Authors: Shanchao Liang et al.; Year: 2026; Venue: ICSE 2026, Software Engineering in Practice track (seen on conf.researchr.org)
- URL opened: https://arxiv.org/abs/2506.12286 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none (contamination)
- Summary: Models name the buggy file path from the issue text alone with up to 76% accuracy on SWE-Bench Verified, against up to 53% on other repositories. This points to memorisation.

### BenchChecker2026 BenchChecker: Assessing the Credibility of Bug-Fixing Benchmarks for LLMs
- Authors: Di Wu et al.; Year: 2026; Venue: USENIX Security Symposium 2026
- URL opened: https://www.usenix.org/conference/usenixsecurity26/presentation/wu-di (USENIX paper page)
- Status: VERIFIED
- Tier: C
- Touches: none (contamination)
- Summary: BenchChecker detects whether repair benchmark samples were in a model's training data, with an AUC around 0.9. Removing contaminated samples from SWE-bench Verified and Multi-SWE-bench lowers most models' resolution rates by more than 20% relative on medium tasks.

### Evertz2026-ChasingShadows Chasing Shadows: Pitfalls in LLM Security Research
- Authors: Jonathan Evertz et al.; Year: 2026; Venue: NDSS 2026
- URL opened: https://arxiv.org/abs/2512.09549 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: none (study design)
- Summary: The authors define nine pitfalls in LLM-based security research and find at least one in each of 72 security and software engineering papers from 2023-2024. Only 15.7% of the pitfalls were discussed by the authors.

### RewardHackBench2026 Reward Hacking Benchmark: Measuring Exploits in LLM Agents with Tool Use
- Authors: Kunvar Thaman; Year: 2026; Venue: ICML 2026 (arXiv comment "Accepted to ICML 2026")
- URL opened: https://arxiv.org/abs/2605.02964 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: Multi-step tool tasks offer shortcuts such as skipping verification or tampering with evaluation functions. Exploit rates range from 0% (Claude Sonnet 4.5) to 13.9% (DeepSeek-R1-Zero).

### PAIChecker2026 PAIChecker: Uncovering and Checking PR-Issue Misalignment in SWE-Bench-Like Benchmarks
- Authors: Manyi Wang, Junjielong Xu, Pinjia He; Year: 2026; Venue: ASE 2026 (arXiv comment)
- URL opened: https://arxiv.org/abs/2607.28587 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N5
- Summary: 13.6% of SWE-bench Verified instances pair an issue description with a pull request that does not match it. PAIChecker detects such pairs with up to 92.12% accuracy.

### Yang2026-PromptsDontSay What Prompts Don't Say: Understanding and Managing Underspecification in LLM Prompts
- Authors: Chenyang Yang et al.; Year: 2026; Venue: Findings of ACL 2026, pp. 9072-9101
- URL opened: https://arxiv.org/abs/2505.13360 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N5
- Summary: LLMs often infer unstated requirements (41.1%), but under-specified prompts are twice as likely to regress when the model or prompt changes. Stating every requirement does not reliably help.

### Jia2025-AmbiguousRepair Automated Repair of Ambiguous Problem Descriptions for LLM-Based Code Generation
- Authors: Haoxiang Jia et al.; Year: 2025; Venue: ASE 2025, pp. 367-379
- URL opened: https://arxiv.org/abs/2505.07270 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N5
- Summary: SpecFix rewrites ambiguous task descriptions by analysing the programs an LLM generates from them. It modifies 43.58% of descriptions and improves Pass@1 on those by 30.9%.

### Ding2025-PrimeVul Vulnerability Detection with Code Language Models: How Far Are We?
- Authors: Yangruibo Ding et al.; Year: 2025; Venue: ICSE 2025, pp. 1729-1741
- URL opened: https://arxiv.org/abs/2403.18624 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N6
- Summary: Existing vulnerability datasets have poor labels and duplication; on the cleaner PrimeVul a 7B model drops from 68.26% F1 on BigVul to 3.09%.

### Lin2025-Mammoth From Large to Mammoth: A Comparative Evaluation of Large Language Models in Vulnerability Detection
- Authors: Jie Lin, David Mohaisen; Year: 2025; Venue: NDSS 2025
- URL opened: https://www.ndss-symposium.org/ndss-paper/from-large-to-mammoth-a-comparative-evaluation-of-large-language-models-in-vulnerability-detection/ (NDSS paper page)
- Status: VERIFIED
- Tier: C
- Touches: N6
- Summary: Ten LLMs are compared on Java and C/C++ vulnerability detection; some settings perform no better than random guessing, and results vary with language and with zero- or few-shot prompting.

### SiftingNoise2026 Sifting the Noise: A Comparative Study of LLM Agents in Vulnerability False Positive Filtering
- Authors: Yunpeng Xiong, Ting Zhang; Year: 2026; Venue: ISSTA 2026 (arXiv comment)
- URL opened: https://arxiv.org/abs/2601.22952 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N6
- Summary: Aider, OpenHands and SWE-agent filter static-analysis false positives; on the OWASP Benchmark the false-positive rate falls from over 92% to 6.3%. On a post-cutoff OSS-Fuzz set, SWE-agent with Claude Sonnet 4 identifies 95.5% of false positives, but aggressive filtering can also hide true vulnerabilities.

### Wang2025-LLMJudgeSE Can LLMs Replace Human Evaluators? An Empirical Study of LLM-as-a-Judge in Software Engineering
- Authors: Ruiqi Wang et al.; Year: 2025; Venue: ISSTA 2025 (Proc. ACM Softw. Eng. 2(ISSTA), pp. 1955-1977)
- URL opened: https://arxiv.org/abs/2502.06193 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N6
- Summary: Seven LLM-as-a-judge methods and two fine-tuned judge models are compared with human scores on code translation, code generation and summarisation, to see how well they agree.

### CodingEnemy2026 Coding with "Enemy": Can Human Developers Detect AI Agent Sabotage?
- Authors: Jingheng Ye et al.; Year: 2026; Venue: NeurIPS 2026 (arXiv comment "Accepted by NeurIPS 2026")
- URL opened: https://arxiv.org/abs/2606.05647 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N6
- Summary: Over 100 developers worked with agents that secretly inserted malicious code; 83 of 88 without a monitor did not notice. A safety monitor helped but sabotage still succeeded in 9 of 16 sessions with a correct alert.

### Abramovich2025-EnIGMA EnIGMA: Interactive Tools Substantially Assist LM Agents in Finding Security Vulnerabilities
- Authors: Talor Abramovich et al.; Year: 2025; Venue: ICML 2025 (PMLR 267); arXiv v1 title "EnIGMA: Enhanced Interactive Generative Model Agent for CTF Challenges"
- URL opened: https://arxiv.org/abs/2409.16165 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N4
- Summary: Giving agents interactive tools such as a debugger and a server connection improves their results on 390 CTF challenges. The authors also measure data leakage and describe models inventing tool output.

### Sun2024-GPTScan GPTScan: Detecting Logic Vulnerabilities in Smart Contracts by Combining GPT with Program Analysis
- Authors: Yuqiang Sun et al.; Year: 2024; Venue: ICSE 2024, article 166
- URL opened: https://arxiv.org/abs/2308.03314 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N6, N2
- Summary: GPTScan combines GPT with static checks to detect smart-contract logic vulnerabilities, noting that about 80% of Web3 security bugs cannot be found by existing tools. It reaches over 90% precision on token contracts, 57.14% on large projects, over 70% recall, and found 9 bugs that auditors missed.

### Ma2025-iAudit Combining Fine-Tuning and LLM-Based Agents for Intuitive Smart Contract Auditing with Justifications
- Authors: Wei Ma et al.; Year: 2025; Venue: ICSE 2025, pp. 1742-1754
- URL opened: https://arxiv.org/abs/2403.16073 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N6, N2
- Summary: The authors note that GPT-4 reaches only 30% precision when both the decision and the justification must be correct in smart-contract auditing. iAudit fine-tunes a detector and a reasoner and adds ranking and critic agents to choose the cause of each vulnerability.

### Chen2025-ChatGPTSC When ChatGPT Meets Smart Contract Vulnerability Detection: How Far Are We?
- Authors: Chong Chen et al.; Year: 2025; Venue: ACM TOSEM 34(4), article 100
- URL opened: https://arxiv.org/abs/2309.05520 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N6, N2
- Summary: ChatGPT finds smart-contract vulnerabilities with high recall but low precision, and the authors sort its false positives into four causes. Its F-score is below other tools on 3 of 7 vulnerability types.

### Nguyen2026-MANDOLLM MANDO-LLM: Heterogeneous Graph Transformers with Large Language Models for Smart Contract Vulnerability Detection
- Authors: Nhat-Minh Nguyen et al.; Year: 2026; Venue: ACM TOSEM 35(6), article 144
- URL opened: https://api.crossref.org/works/10.1145/3765751 (Crossref record with the abstract deposited by ACM). ACM DL returned HTTP 403 and no arXiv version is in DBLP's arXiv records.
- Status: VERIFIED (via the Crossref record of the DOI, which shows title, authors and abstract)
- Tier: C
- Touches: N2
- Summary: MANDO-LLM combines heterogeneous graph transformers over control-flow and call graphs with LLM code features to detect Solidity vulnerabilities at contract and line level. It reports F1 gains from 0.59% to 80.72% at contract level over existing methods.

### FORGE2026 FORGE: An LLM-driven Framework for Large-Scale Smart Contract Vulnerability Dataset Construction
- Authors: Jiachi Chen et al.; Year: 2026; Venue: ICSE 2026 (arXiv comment "Accepted for the 48th International Conference on Software Engineering (ICSE 2026)")
- URL opened: https://arxiv.org/abs/2506.18795 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: An LLM pipeline extracts findings from 6,454 real audit reports and classifies them by CWE, giving 81,390 Solidity files and 27,497 findings in 296 CWE categories.

### Zheng2024-DAppSCAN DAppSCAN: Building Large-Scale Datasets for Smart Contract Weaknesses in DApp Projects
- Authors: Zibin Zheng et al.; Year: 2024; Venue: IEEE Transactions on Software Engineering 50(6), pp. 1360-1373
- URL opened: https://arxiv.org/abs/2305.08456 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: 22 people spent 44 person-months on 1,199 audit reports from 29 security teams and found 9,154 weaknesses. The source dataset has 39,904 Solidity files with 1,618 SWC weaknesses from 682 projects.

### Zhang2023-ExploitableBugs Demystifying Exploitable Bugs in Smart Contracts
- Authors: Zhuo Zhang et al.; Year: 2023; Venue: ICSE 2023, pp. 615-627
- URL opened: https://api.crossref.org/works/10.1109/ICSE48619.2023.00061 (Crossref record: title, authors, venue; no abstract). IEEE Xplore returned nothing and no arXiv version is in DBLP's arXiv records.
- Status: UNVERIFIED (title, authors and venue confirmed in DBLP and Crossref; abstract not seen)
- Tier: C
- Touches: N2
- Summary: Not summarised here, because the abstract was not seen. The project's IDEA.md cites it for the finding that more than 80% of 516 exploitable Code4rena bugs are beyond automated tools; check that figure against the paper.

### Zhang2024-AccountingErrors Towards Finding Accounting Errors in Smart Contracts
- Authors: Brian Zhang; Year: 2024; Venue: ICSE 2024, article 138
- URL opened: https://api.crossref.org/works/10.1145/3597503.3639128 (Crossref record: title, author, venue; no abstract). ACM DL returned HTTP 403 and no arXiv version is in DBLP's arXiv records.
- Status: UNVERIFIED (title, author and venue confirmed in DBLP and Crossref; abstract not seen)
- Tier: C
- Touches: N2
- Summary: Not summarised; only the title, author and venue were seen. The title matches the project's focus on accounting bugs in smart contracts.

### Lin2025-SSR SSR: Safeguarding Staking Rewards by Defining and Detecting Logical Defects in DeFi Staking
- Authors: Zewei Lin et al.; Year: 2025; Venue: ASE 2025, pp. 571-583
- URL opened: https://arxiv.org/abs/2601.05827 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: From 64 incidents and 144 audit reports the authors define six kinds of logic defects in DeFi staking that let attackers claim unearned rewards. SSR uses an LLM to model staking logic and detects these defects statically.

### Lin2025-PromFuzz PromFuzz: Leveraging LLM-Driven and Bug-Oriented Composite Analysis for Detecting Functional Bugs in Smart Contracts
- Authors: Xingshuang Lin et al.; Year: 2025; Venue: ASE 2025, pp. 1044-1056
- URL opened: https://arxiv.org/abs/2503.23718 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: PromFuzz uses two LLM agents to point to likely vulnerable functions, generates invariant checkers from their logic, and fuzzes for functional bugs. It cites the finding that over 80% of exploitable smart-contract bugs are functional bugs that current tools miss.

### Zhou2023-SoKDeFi SoK: Decentralized Finance (DeFi) Attacks
- Authors: Liyi Zhou et al.; Year: 2023; Venue: IEEE S&P 2023, pp. 2444-2461 (arXiv versions also titled "SoK: Decentralized Finance (DeFi) Incidents")
- URL opened: https://arxiv.org/abs/2208.13035 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N7
- Summary: The authors build a common frame to compare DeFi incidents, using 77 papers, 30 audit reports and 181 incidents. Users and protocols lost at least 3.24 billion USD from April 2018 to April 2022, and price-oracle attacks were the most frequent incident type (15%).

### Chaliasos2024-DeFiTools Smart Contract and DeFi Security Tools: Do They Meet the Needs of Practitioners?
- Authors: Stefanos Chaliasos et al.; Year: 2024; Venue: ICSE 2024, article 60
- URL opened: https://arxiv.org/abs/2304.02981 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2, N7
- Summary: Five tools could have prevented only 8% of 127 high-impact attacks, $149 million of $2.3 billion in losses, all of them reentrancy. Practitioners rank logic bugs and protocol-level flaws as the main threats tools do not cover.

### Babel2023-Clockwork Clockwork Finance: Automated Analysis of Economic Security in Smart Contracts
- Authors: Kushal Babel et al.; Year: 2023; Venue: IEEE S&P 2023, pp. 2499-2516
- URL opened: https://arxiv.org/abs/2109.04347 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N7
- Summary: A formal verification framework that extracts all economic attacks on users' funds across composed DeFi contracts. It introduces extractable value as a formal measure of economic security.

### Chen2024-FlashSyn FlashSyn: Flash Loan Attack Synthesis via Counter Example Driven Approximation
- Authors: Zhiyang Chen, Sidi Mohamed Beillahi, Fan Long; Year: 2024; Venue: ICSE 2024, article 142
- URL opened: https://arxiv.org/abs/2206.10708 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N7
- Summary: FlashSyn approximates DeFi protocol behaviour numerically and searches for the sequence of calls that gives the attacker the most profit. It is evaluated on 16 DeFi protocols that suffered flash-loan attacks and 2 more.

### Kong2025-ProfitFuzz Smart Contract Fuzzing Towards Profitable Vulnerabilities
- Authors: Ziqiao Kong et al.; Year: 2025; Venue: FSE 2025 (Proc. ACM Softw. Eng. 2(FSE), pp. 153-175)
- URL opened: https://arxiv.org/abs/2501.08834 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N7
- Summary: VERITE fuzzes for profitable vulnerabilities and then maximises the profit by gradient descent. It is evaluated on 61 exploited DeFi projects with an average loss of over 1.1 million dollars.

### Li2024-SASTSC Static Application Security Testing (SAST) Tools for Smart Contracts: How Far Are We?
- Authors: Kaixuan Li et al.; Year: 2024; Venue: FSE 2024 (Proc. ACM Softw. Eng. 1(FSE), pp. 1447-1470)
- URL opened: https://arxiv.org/abs/2404.18186 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: On a benchmark of 788 contract files with 10,394 vulnerabilities, 8 static tools miss about 50% of the vulnerabilities with precision no higher than 10%.

### Sendner2024-Scanners Large-Scale Study of Vulnerability Scanners for Ethereum Smart Contracts
- Authors: Christoph Sendner et al.; Year: 2024; Venue: IEEE S&P 2024, pp. 2273-2290 (arXiv title "Vulnerability Scanners for Ethereum Smart Contracts: A Large-Scale Study")
- URL opened: https://arxiv.org/abs/2312.16533 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: 17 scanners disagree widely on 77,219 source files and over 4 million bytecodes, and perform poorly on about 14,000 annotated contracts and 373 audited ones.

### Sharma2023-SCDevs A Mixed-Methods Study of Security Practices of Smart Contract Developers
- Authors: Tanusree Sharma et al.; Year: 2023; Venue: USENIX Security Symposium 2023, pp. 2545-2562 (arXiv title "Exploring Security Practices of Smart Contract Developers")
- URL opened: https://arxiv.org/abs/2204.11193 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N1 (human developers' security practice)
- Summary: Interviews and a code-review task with 29 smart-contract developers: early-stage developers found the vulnerability in 15% of cases and experienced ones in 55%.

### Li2026-SCPatcher SCPatcher: Automated Smart Contract Code Repair via Retrieval-Augmented Generation and Knowledge Graph
- Authors: Xiaoqi Li et al.; Year: 2026; Venue: FSE 2026 Companion (SIGSOFT FSE Companion 2026), pp. 1212-1216
- URL opened: https://arxiv.org/abs/2604.00687 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N2, N3
- Summary: A knowledge graph built from 5,000 Ethereum contracts guides an LLM in repairing vulnerable contracts. It reports an 81.5% repair rate and a 91.0% compilation rate.

### Zhang2026-LeanSCSynth Towards Trustworthy Smart Contract Synthesis: A Multi-Agent Framework with Lean-Based Verification
- Authors: Bowei Zhang et al.; Year: 2026; Venue: ACL 2026 (Volume 1: Long Papers), pp. 39548-39582
- URL opened: https://aclanthology.org/2026.acl-long.1836/ (ACL Anthology page)
- Status: VERIFIED
- Tier: C
- Touches: N2
- Summary: LeVer has agents generate, formally verify in Lean, attack and repair smart contracts in a closed loop. The abstract gives no numbers.

### Guo2026-VICIdent Accurate Identification of the Vulnerability-Introducing Commit based on Differential Analysis of Patching Patterns
- Authors: Qixuan Guo, Yongzhong He; Year: 2026; Venue: NDSS 2026
- URL opened: https://www.ndss-symposium.org/ndss-paper/accurate-identification-of-the-vulnerability-introducing-commit-based-on-differential-analysis-of-patching-patterns/ (NDSS paper page)
- Status: VERIFIED
- Tier: C
- Touches: N1 (method: tracing the vulnerability-introducing commit)
- Summary: The method classifies the statements in a patch by patching pattern and matches them against earlier commits to find where the vulnerability was introduced. On 6,920 CVEs it reaches 94.94% accuracy and 86.92% recall.

### Hinrichs2026-VCCMining Back to the Roots: Assessing Mining Techniques for Java Vulnerability-Contributing Commits
- Authors: Torge Hinrichs et al.; Year: 2026; Venue: ACM TOSEM 35(8), article 229
- URL opened: https://api.crossref.org/works/10.1145/3769105 (Crossref record with the abstract deposited by ACM). ACM DL returned HTTP 403 and no arXiv version is in DBLP's arXiv records.
- Status: VERIFIED (via the Crossref record of the DOI, which shows title, authors and abstract)
- Tier: C
- Touches: N1 (method: tracing the vulnerability-introducing commit)
- Summary: Twelve SZZ-style techniques for finding vulnerability-contributing commits in Java reach at most 0.60 precision and up to 0.89 recall. Combining them raises precision to 0.75-0.80.

### Chou2026-VibeQual Building Software by Rolling the Dice: A Qualitative Study of Vibe Coding
- Authors: Yi-Hung Chou et al.; Year: 2026; Venue: FSE 2026 (Proc. ACM Softw. Eng. 3(FSE), pp. 1712-1734)
- URL opened: https://arxiv.org/abs/2512.22418 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N1 (context)
- Summary: A grounded-theory study of 20 vibe-coding videos (about 21 hours). Some vibe coders accept AI output without reading it, and debugging is described as "rolling the dice".

### VibeGrey2026 Vibe Coding in Practice: Motivations, Challenges, and a Future Outlook – a Grey Literature Review
- Authors: Ahmed Fawzy, Amjed Tahir, Kelly Blincoe; Year: 2026; Venue: ICSE 2026 (seen in the ICSE 2026 research track list on conf.researchr.org) [track uncertain]
- URL opened: https://arxiv.org/abs/2510.00328 (arXiv abstract page)
- Status: VERIFIED
- Tier: C
- Touches: N1 (context)
- Summary: A review of 101 practitioner sources with 518 accounts of vibe coding. Users value speed, see the code as "fast but flawed", and often skip testing or hand quality checks back to the AI.

### Peng2025-PwnGPT PwnGPT: Automatic Exploit Generation Based on Large Language Models
- Authors: Wanzong Peng et al.; Year: 2025; Venue: ACL 2025 (Volume 1: Long Papers), pp. 11481-11494
- URL opened: https://aclanthology.org/2025.acl-long.562/ (ACL Anthology page)
- Status: VERIFIED
- Tier: C
- Touches: N3
- Summary: PwnGPT splits exploit generation for CTF binary-exploitation tasks into analysis, generation and verification. It raises the completion rate from 26.3% to 57.9% with o1-preview and from 21.1% to 36.8% with GPT-4o.

---

## Leads not followed

Relevant titles seen in the target venues that I could not verify (no arXiv version in DBLP's arXiv records, ACM DL or IEEE Xplore blocked, Crossref without abstract, and web search and OpenAlex budgets used up):

- "INTENTFIX: Automated Logic Vulnerability Repair via LLM-Driven Intent Modeling" (ICSE 2026; ICSE 2026 research track list on conf.researchr.org). Logic-vulnerability repair; may matter for N3 and N4.
- "PoCE: Automated Proof-of-Concept Synthesis using Large Language Models for Robust Validation" (ISSTA 2026; ISSTA 2026 research papers list). May use PoCs to validate patches (N3).
- "SecChain: Operationalizing Security Guidelines for Multi-agent Smart Contract Generation" (ASE 2026; ASE 2026 research track list). Secure Solidity generation by agents (N2).
- "SPSYN: Synthesizing DeFi Price-Manipulation Exploits via Semantic Recovery and State-Guided Search" (ASE 2026; same list). DeFi exploit synthesis (N2, N7).
- "From Vibe to Spec: An Empirical Study to Demystify Specifications in Code Generation" (ASE 2026; same list). Request wording (N5).
- "Evidence-Grounded Logic Vulnerability Detection for Smart Contracts via Runtime Context Reasoning" (ASE 2026; same list).
- "PatchAudit: Uncovering Faulty Security Patches and Lingering Zero-Days at Scale" and "From Fix to Flaw: Understanding and Revealing Incomplete Patches for Link Following Vulnerabilities" (CCS 2026; sigsac.org accepted list). Incomplete patches (N3).
- "Oracle-Guided Vulnerability Diversity and Exploit Synthesis of Smart Contracts Using LLMs", Mojtaba Eshghie and Cyrille Artho (ASE 2024; DBLP and Crossref, no abstract).
- "Do LLMs Generate Useful Test Oracles? An Empirical Study with an Unbiased Dataset", Davide Molinelli et al. (ASE 2025; DBLP and Crossref, no abstract). Tests that encode actual instead of expected behaviour (N4).
- "Make a Feint to the East While Attacking in the West: Blinding LLM-Based Code Auditors with Flashboom Attacks", Xiao Li et al. (IEEE S&P 2025; DBLP and Crossref, no abstract). Reliability of LLM auditors (N6).
- "Test Suites Guided Vulnerability Validation for Node.js Applications", Changhua Luo et al. (CCS 2024; DBLP and Crossref, no abstract). Confirming findings with executable tests (N6).
- "Should We Evaluate LLM Based Security Analysis Approaches on Open Source Systems?", Kohei Dozono et al. (ASE 2025; DBLP and Crossref, no abstract). Contamination.
- "SCAR: Mining and Structuring Smart Contract Security Audit Reports", Ilham A. Qasse et al. (FSE 2026 Companion; DBLP and Crossref, no abstract). Audit-report data (N2).
- "Lanturn: Measuring Economic Security of Smart Contracts Through Adaptive Learning", Kushal Babel et al. (CCS 2023; DBLP and Crossref, no abstract). Economic loss (N7).
- "FairChecker: Detecting Fund-Stealing Bugs in DeFi Protocols via Fairness Validation", Yi Sun et al. (ICSE 2025; DBLP and Crossref, no abstract).
- "Midas: Mining Profitable Exploits in On-Chain Smart Contracts via Feedback-Driven Fuzzing and Differential Analysis", Mingxi Ye et al. (ISSTA 2024; DBLP and Crossref, no abstract). Profit (N7).
- "AdvSCanner: Generating Adversarial Smart Contracts to Exploit Reentrancy Vulnerabilities Using LLM and Static Analysis", Yin Wu et al. (ASE 2024; DBLP and Crossref, no abstract).
- "SmartFix: Fixing Vulnerable Smart Contracts by Accelerating Generate-and-Verify Repair using Statistical Models", Sunbeom So and Hakjoo Oh (ESEC/FSE 2023; DBLP and Crossref, no abstract).
- "Leveraging Mixture-of-Experts Framework for Smart Contract Vulnerability Repair with Large Language Model", Hang Yuan et al. (ASE 2025; DBLP and Crossref, no abstract).
- "Prompt to Pwn: Automated Exploit Generation for Smart Contracts" (arXiv 2508.01371; seen in DBLP's arXiv records while matching; venue not checked).
- "Agent That Debugs: Dynamic State-Guided Vulnerability Repair" (arXiv 2504.07634; seen in web-search results; venue not checked).
- "MAS-SZZ: Multi-Agentic SZZ Algorithm for Vulnerability-Inducing Commit Identification" (arXiv 2604.24398; seen in DBLP's arXiv records; venue not checked).
- "Usability as a Weapon: Attacking the Safety of LLM-Based Code Generation via Usability Requirements" (arXiv 2605.10133; seen in DBLP's arXiv records; may bear on N5; venue not checked).
- "Securing AI-Generated Code: A Just-in-Time Vulnerability Detection and Remediation ..." (arXiv 2608.16187; title truncated in DBLP's arXiv records; venue not checked).
- Venues not swept: EMNLP 2026 (no accepted-paper list online on 2026-10-21), ICSE 2026 companion tracks beyond the 72 records in DBLP, ASE 2026 tracks other than the research track, CCS 2026 posters and workshops, and TOSEM, TSE and EMSE early-access papers not yet in DBLP.
