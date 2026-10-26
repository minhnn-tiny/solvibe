# Round 3, topic T2: LLMs, AI agents and smart contracts (newest work, 2026)

Search date: 21 October 2026. Agent: bibliography agent, ARS lit-review mode, round 3 saturation test.

**Result in short.** 67 queries. No new tier A paper. Eight new tier B papers that are not in the index (`master_index.tsv`, 770 titles, re-read at 07:55). Six of them are about LLMs and smart contracts. Two sit outside T2 but bear on the project (one incident dataset with losses, one PoC generator). Three of the eight had been seen as unchecked leads in earlier round files; five had never been seen. The last new paper came from query 54. Queries 55 to 67 gave nothing new, so the last five queries (63 to 67) gave nothing new.

**Tier rule used here.** I followed the tiers already in the index. LLM-reviewer reliability studies (for example ALIBI, Flashboom, Beyond F1) and datasets built from audit reports (SC-Bench, SCAR, GiAnt) are tier B there, so I rated papers of those kinds B. One rule is stricter than some index entries. A new LLM-based detection tool counts as B only if it confirms its findings by execution (N6). Otherwise it is C. GPTScan and LogicScan are B in the index, but under this rule the many 2026 detection tools of the same kind became C. They are listed by name in the tier C section below, so the orchestrator can re-tier them.

**How the arXiv listing rows were screened.** I fetched arXiv advanced-search result pages (computer science, cross-lists included, abstracts shown). For each query, "hits" is the number of records returned. "Screened" is the number whose title or abstract names both a blockchain term and an LLM or agent term; I read those titles and, for candidates, the abstracts. "Already indexed" counts screened hits whose title matches an index title with similarity of at least 0.8; a few false matches are possible. The arXiv API itself was not used for search because it stems "Solidity" to "solid" and returns physics papers.

## Queries run

| # | Query | Source | Hits looked at | Already indexed | New tier A or B |
|---|---|---|---|---|---|
| 1 | abstract: "smart contract", submitted 2026-06-01 to 2026-10-21 | arXiv advanced search (cs) | 138 hits, 54 screened | 11 | 3 (Bastet, Deception Delta, ack3 dataset) |
| 2 | abstract: smart contracts, Jun–Oct 2026 | arXiv advanced search | 145 hits, 55 screened | 11 | 0 |
| 3 | abstract: Solidity, Jun–Oct 2026 (search also matches "solid") | arXiv advanced search | 326 hits, 14 screened | 2 | 0 |
| 4 | abstract: DeFi, Jun–Oct 2026 | arXiv advanced search | 53 hits, 21 screened | 2 | 0 |
| 5 | abstract: EVM, Jun–Oct 2026 | arXiv advanced search | 33 hits, 6 screened | 1 | 0 |
| 6 | abstract: blockchain, Jun–Oct 2026 | arXiv advanced search | 361 hits, 87 screened | 3 | 0 |
| 7 | abstract: Ethereum, Jun–Oct 2026 | arXiv advanced search | 132 hits, 27 screened | 1 | 0 |
| 8 | abstract: smart contract, 2026-01-01 to 2026-05-31 | arXiv advanced search | 168 hits, 64 screened | 21 | 1 (LLM static-analysis benchmark); Neuroforger seen again |
| 9 | abstract: DeFi, Jan–May 2026 | arXiv advanced search | 60 hits, 16 screened | 3 | 0 |
| 10 | abstract: EVM, Jan–May 2026 | arXiv advanced search | 17 hits, 5 screened | 0 | 0 |
| 11 | abstract: Solidity, Jan–May 2026 | arXiv advanced search | 361 hits, 19 screened | 6 | 0 |
| 12 | abstract: blockchain, Jan–May 2026 | arXiv advanced search | 340 hits, 95 screened | 8 | 0 |
| 13 | title: smart contract, 2026 | arXiv advanced search | 125 hits, 67 screened | 26 | 0 |
| 14 | title: DeFi, 2026 | arXiv advanced search | 33 hits, 11 screened | 3 | 0 |
| 15 | title: blockchain, 2026 | arXiv advanced search | 255 hits, 62 screened | 1 | 0 |
| 16 | title: Solidity, 2026 | arXiv advanced search | 77 hits, 9 screened | 5 | 0 |
| 17 | title: EVM, 2026 | arXiv advanced search | 10 hits, 3 screened | 0 | 0 |
| 18 | title: Ethereum, 2026 | arXiv advanced search | 50 hits, 10 screened | 1 | 0 |
| 19 | title: Web3, 2026 | arXiv advanced search | 12 hits, 5 screened | 1 | 0 |
| 20 | title: on-chain, 2026 (matches "on" and "chain"; first 1,200 of 1,232) | arXiv advanced search | 1,200 hits, 19 screened | 2 | 0 |
| 21 | title: crypto, 2026 | arXiv advanced search | 37 hits, 7 screened | 0 | 0 |
| 22 | abstract: Web3, 2026 | arXiv advanced search | 34 hits, 14 screened | 1 | 0 |
| 23 | abstract: "on-chain", 2026 (first 1,200 of 7,507) | arXiv advanced search | 1,200 hits, 21 screened | 1 | 0 |
| 24 | AI-generated Solidity vulnerabilities (2025–) | Semantic Scholar keyword search API | 0 (HTTP 429 after 6 retries, tried 3 times) | – | 0 |
| 25 | "vibe-coded" smart contracts security study Solidity | WebSearch | 9 links, 7 items | 1 | 0 |
| 26 | AI-generated Solidity code vulnerabilities empirical study arXiv 2026 | WebSearch | 9 links, 4 items | 4 | 0 |
| 27 | coding agents DeFi protocol development security evaluation Claude Code Codex Solidity | WebSearch | 10 links | 1 | 0 |
| 28 | LLM agent audit contest Code4rena Sherlock AI auditor findings comparison paper | WebSearch | 9 links, 5 items | 1 | 0 |
| 29 | Solodit findings dataset LLM benchmark smart contract audit 2026 | WebSearch | 9 links, 5 items | 3 | 1 (ESEM 2026 transfer study) |
| 30 | Foundry test generation large language model smart contract unit tests Solidity | WebSearch | 9 links, 7 items | 1 | 0 |
| 31 | invariant generation LLM smart contract DeFi 2026 arXiv | WebSearch | 9 links, 4 items | 2 | 0 |
| 32 | smart contract vulnerability patch LLM agent benchmark exploit test validation 2026 | WebSearch | 10 links, 4 items | 2 | 0 |
| 33 | exploit replay patch validation DeFi hack historical attack transactions fork test patched contract | WebSearch | 9 links, 7 items | 3 | 0 |
| 34 | smart contract upgrade introduces bug AI agent LLM study proxy upgrade vulnerability 2026 | WebSearch | 9 links, 6 items | 0 | 0 |
| 35 | "Claude Code" Solidity smart contract security experiment paper | WebSearch | 9 links, 6 items | 0 | 0 |
| 36 | "Codex" agent writes Solidity smart contract vulnerabilities evaluation arXiv | WebSearch | 9 links, 8 items | 4 | 0 |
| 37 | "vibe coding" "smart contract", since 2026 (pages 1 and 2) | Google Scholar via WebFetch | 20 | 0 | 0 |
| 38 | Sherlock audit contest AI auditor LLM agent submitted findings judged valid 2026 | WebSearch | 9 links (vendor and press pages) | 0 | 0 |
| 39 | AI auditors versus human auditors smart contract audit competition empirical comparison 2026 | WebSearch | 9 links | 1 | 0 |
| 40 | "coding agent" OR "coding agents" Solidity vulnerabilities, since 2026 | Google Scholar via WebFetch | 10 | 6 | 0 |
| 41 | LLM "Code4rena" OR "Sherlock" OR "Solodit" smart contract, since 2026 | Google Scholar via WebFetch | 10 | 6 | 1 (ExploitGen) |
| 42 | AI-generated Solidity smart contract vulnerabilities agent (2025–) | Semantic Scholar API via WebFetch | 0 (HTTP 429) | – | 0 |
| 43 | coding agent Solidity smart contract security, from 2026-01-01 | OpenAlex API via WebFetch | 50 of 349 | 18 | 0 (Neuroforger seen again) |
| 44 | smart contract LLM, published 2026-06-01 or later | Crossref API | 60 (36 with a smart-contract title) | 1 | 0 |
| 45 | smart contract agent, published 2026-06-01 or later | Crossref API | 60 (47 with a smart-contract title) | 3 | 0 |
| 46 | Solidity large language model, published 2026-06-01 or later | Crossref API | 60 (none about smart contracts) | 0 | 0 |
| 47 | DeFi exploit LLM, published 2026-06-01 or later | Crossref API | 60 (22 with a DeFi title) | 0 | 0 |
| 48 | "Smart Contract Vulnerability Detection Empowered by LLM: Can It Really Work?" (exact title) | WebSearch | 9 links, 6 items | 2 | 0 (target has no abstract online; see leads) |
| 49 | held-out exploit tests smart contract repair LLM overfitting shown test proof of vulnerability Solidity 2026 | WebSearch | 9 links, 8 items | 4 | 1 (Validating Solidity Code Defects) |
| 50 | abstract: Foundry, 2026 | arXiv advanced search | 29 hits, 2 screened | 2 | 0 |
| 51 | abstract: "audit reports", 2026 | arXiv advanced search | 44 hits, 10 screened | 6 | 0 |
| 52 | abstract: "audit report", 2026 | arXiv advanced search | 44 hits, 10 screened | 6 | 0 |
| 53 | abstract: "proof of concept", 2026 | arXiv advanced search | 959 hits, 13 screened | 8 | 0 |
| 54 | LLM "smart contract" "proof-of-concept" OR "PoC" exploit validation, since 2026 | Google Scholar via WebFetch | 10 | 7 | 1 (PoCEvolve, outside T2); ExploitGen seen again |
| 55 | large language model smart contract repair exploit validation, from 2026-01-01 | OpenAlex API via WebFetch | 50 of 921 | 18 | 0 |
| 56 | AI-written versus human-written Solidity contracts security comparison same specification exploit 2026 study | WebSearch | 9 links, 6 items | 3 | 0 |
| 57 | smart contract LLM year:2026 | DBLP API via WebFetch | 0 (Anubis bot-check page) | – | 0 |
| 58 | "smart contract" LLM agent repair exploit patch "held-out" OR "hidden" tests, since 2026 | Google Scholar via WebFetch | 10 | 2 | 0 |
| 59 | abstract: "audit contest", 2025–2026 | arXiv advanced search | 6 hits, 4 screened | 2 | 0 |
| 60 | abstract: "audit competition", 2025–2026 | arXiv advanced search | 0 | – | 0 |
| 61 | abstract: "bug bounty", 2025–2026 | arXiv advanced search | 31 hits, 2 screened | 2 | 0 |
| 62 | LLM agent Solidity smart contract code generation security 2026 | Semantic Scholar keyword search API | 0 (HTTP 429 after 6 retries) | – | 0 |
| 63 | ASE 2026 research papers accepted smart contract LLM agent researchr (the researchr track page itself returned 404) | WebSearch | 9 links | 2 | 0 |
| 64 | CCS 2026 accepted papers list smart contract DeFi LLM (the CCS accepted-papers URL returned 404) | WebSearch | 9 links | 3 | 0 |
| 65 | `("smart contract" \| Solidity) + (agent \| agents \| LLM) + (Foundry \| invariant \| "proof of concept")`, 2026 | Semantic Scholar bulk search API | 27 | 6 | 0 |
| 66 | `("vibe coding" \| "coding agent" \| "coding agents" \| "Claude Code" \| Codex \| Copilot) + (Solidity \| "smart contract" \| "smart contracts" \| DeFi)`, 2026 | Semantic Scholar bulk search API | 7 | 5 | 0 |
| 67 | `("smart contract" \| "smart contracts" \| Solidity \| DeFi) + (repair \| patch \| patching \| fix) + (LLM \| agent \| agents \| "language model") + (exploit \| exploits \| PoC \| "proof of concept")`, 2026 | Semantic Scholar bulk search API | 9 | 7 | 0 |

Verification look-ups (not counted as queries): arXiv abstract pages for each tier B paper, the Dagstuhl page of the ESEM paper, the ÉTS repository record of ExploitGen, the CEUR-WS PDF of the legacy-upgrade paper, and Crossref and OpenAlex records by DOI for the IEEE and MDPI papers listed under leads.

**Saturation.** The last five queries (63 to 67) gave nothing new. The last new paper about LLMs and smart contracts came from query 49. After that, one more relevant paper came from query 54, and it is outside T2. Thirteen queries in a row (55 to 67) gave nothing new; three of them failed.

## Papers (tier A or B, not in the index)

### Hsu2026-Bastet Bastet: A Fine-Grained Expert-Labeled Dataset for DeFi Smart Contract Vulnerability Detection
- Authors: Wan-Hsuan Hsu et al. (with Kentaroh Toyoda); Year: 2026; Venue: arXiv preprint (arXiv:2606.03387)
- URL opened: https://arxiv.org/abs/2606.03387 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N2
- Found by: query 1. Never seen in earlier rounds.
- Summary: The authors say existing vulnerability datasets use old Solidity versions, labels made by tools or LLMs, and coarse labels that miss business-logic bugs. Bastet collects 4,402 findings from 394 Code4rena competitive audit reports, from April 2021 to November 2024. White-hat researchers from the DeFiHackLabs community fully annotated 849 of them. Two annotators label each finding and settle disagreements by discussion, using a two-layer taxonomy of 46 tags and 77 subtags. The dataset is meant for evaluating LLM-based vulnerability detection; the abstract reports no detector results.
- Delta: Bastet turns audit-contest findings into labels for detection benchmarks. It has no executable exploit, no fix commit and no code-writing task. The project starts from the same source, accepted audit-contest findings. It then traces each finding to the commit that introduced it and to the fix, writes a Foundry PoV, and uses the finding as a feature request and as a repair task for agents. Bastet's 46 tags could describe which kinds of business-logic bugs the project's findings cover, and could show how typical they are.

### Schefold2026-DeceptionDelta The Deception Delta: Adversarial Evaluation of LLM-Based Smart Contract Bytecode Forensics
- Authors: Timo Schefold; Year: 2026; Venue: ACM CCS 2026 (the arXiv comments say "Accepted at ACM CCS 2026" and that v2 matches the published ACM version; the ACM page was not opened); arXiv:2609.14098
- URL opened: https://arxiv.org/abs/2609.14098 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Found by: query 1. Round 2 saw the title on the CCS 2026 accepted-papers list and did not check it (`r2_S3b_leads.md`, line 960).
- Summary: The paper tests whether LLMs that read raw bytecode can find hidden fund-draining logic in contracts built to mislead them. It runs 22 frontier models on 13 purpose-built contracts (9 deception methods, 4 controls) with six prompt strategies, giving 8,528 usable runs. Deception lowers drain detection by 20.0 percentage points (95% CI [17.2, 22.8]) against matched controls, and only five models from two providers exceed 50% detection. The author also reports that models sometimes describe the drain correctly, accept the contract's misleading framing, and call it benign. Guard instructions give no overall benefit.
- Delta: The paper measures how an LLM reviewer fails on bytecode written to mislead, in one shot, with an LLM judge. The project's review reads source code. It runs the same prompt on the agent's version and the human's version of the same function, and it counts a flaw only if a new PoV confirms it. The finding that a model can explain a flaw and still call the code safe supports that choice. The paper does not compare who wrote the code, and nothing in it is confirmed by an executable test.

### Gattermayer2026-ack3 The ack3 H1 2026 DeFi Incident Dataset: Audit Scope Across 135 Security Incidents
- Authors: Josef Gattermayer et al. (with Jan Kalivoda, Arman Bašović); Year: 2026; Venue: arXiv preprint (arXiv:2608.13792); dataset DOI 10.5281/zenodo.21906487
- URL opened: https://arxiv.org/abs/2608.13792 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N2, N7 (outside T2: no LLMs)
- Found by: query 1. Never seen in earlier rounds.
- Summary: The dataset covers 135 DeFi security incidents from 1 January to 29 June 2026, with USD 939.86 million in attributed loss. Audit history was found for 68 incidents. In 46 of them the attack path was outside every public pre-incident audit scope, in 20 it was inside at least one scope, and 2 were unresolved. Outside-scope paths were 67.6% of these incidents by count and 94.4% by loss; without the two largest incidents the loss share is 72.1%.
- Delta: The paper links losses to audit scope at the level of whole projects. It does not study who wrote the code or use exploits as tests. For the project it gives 2026 loss figures and shows that "audited" often does not mean the exploited code was reviewed. The project estimates the loss of each exploit inside its PoV, per finding (N7). It is in the same family as the indexed "The Audit Gap in Blockchain Security" (tier B).

### Susan2026-LLMStaticBench Benchmarking LLM-Based Static Analysis for Secure Smart Contract Development: Reliability, Limitations, and Potential Hybrid Solutions
- Authors: Stefan-Claudiu Susan et al. (with Andrei Arusoaie, Dorel Lucanu); Year: 2026; Venue: IEEE COMPSAC 2026 (the arXiv comments say "Accepted to IEEE COMPSAC 2026"; the arXiv version is extended; the IEEE page was not opened); arXiv:2605.11163
- URL opened: https://arxiv.org/abs/2605.11163 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Found by: query 8. Round 1 (`r1_L4_solidity_codegen.md`, line 633) and round 2 (`r2_S2_tests_assert_bugs.md`, line 633) passed it on as a lead for N6; nobody verified it.
- Summary: The authors ask whether LLMs can replace static analyzers as security auditors of Solidity code, or only complement them. They find a lexical bias: models rely on cues such as identifier names, which produces many false positives. Prompting techniques trade precision against recall. The results come from their own automated framework, which classifies model outputs with 92% accuracy. The abstract gives no per-model numbers.
- Delta: This bears directly on N6. The agent's version and the human's version of the same function differ in names and comments, so an LLM reviewer may report different flaws for reasons that have nothing to do with security. The project guards against this by requiring a PoV for each reported flaw. The paper does not compare code written by different authors and does not confirm findings by execution.

### Susan2025-ValidatingDefects Validating Solidity Code Defects using Symbolic and Concrete Execution powered by Large Language Models
- Authors: Ştefan-Claudiu Susan et al. (with Andrei Arusoaie, Dorel Lucanu); Year: 2025; Venue: Proceedings of FROM 2025, EPTCS 427, pp. 98–116 (journal reference on the arXiv page); arXiv:2509.13023
- URL opened: https://arxiv.org/abs/2509.13023 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Found by: query 49. Never seen in earlier rounds.
- Summary: Static tools and LLMs raise many false alarms on Solidity code. This pipeline chains custom Slither detectors, LLMs, Kontrol (symbolic execution) and Forge (concrete execution) to prove that a reported defect is real. The authors ran experiments on seven types of critical defects and present results for three: reentrancy, complex fallback, and faulty access-control policies. They report that the chain confirms true positives and cuts manual checking, and they note that LLMs are inconsistent and costly. The abstract gives no numbers.
- Delta: It applies the same rule as N6: a reported defect counts only when an execution confirms it. It applies the rule to detector output on known defect types. The project applies it to an LLM security review of agent code and human code, with PoVs adapted from audit reports, inside a comparison of agents with human developers. The paper does not study who wrote the code. Same authors as Susan2026-LLMStaticBench above.

### Aminnezhad2026-ExploitGen ExploitGen: automated smart contract vulnerability verification via taxonomy specialized multi-agent detection and proof-of-concept exploit generation
- Authors: Aysheh Aminnezhad (supervised by Kaiwen Zhang and Camille Coti); Year: 2026; Venue: master's thesis (mémoire de maîtrise), École de technologie supérieure (ÉTS), Montréal
- URL opened: https://espace.etsmtl.ca/id/eprint/4120/ (institutional repository record with the full English abstract)
- Status: VERIFIED
- Tier: B
- Touches: N6, N3
- Found by: query 41, and again by queries 54, 55 and 58. Never seen in earlier rounds.
- Summary: A LangGraph pipeline with eight detection agents, one per OpenSCV category, proposes candidates. Each candidate then goes through static graph extraction, an attempt to disprove it, attack planning, Foundry PoC writing and a counterfactual check. A vulnerability is confirmed only when its Foundry PoC passes on the vulnerable contract and fails on a patched version with the same function signatures. On SB Curated (139 ground-truth vulnerabilities) it confirms 86 exploits, with a confirmation yield of 0.741 and an F1 of 0.675. Against one attempt of the same pipeline, unconfirmed candidates fall by 23.1% and confirmed exploits rise from 73 to 86. Against detection without scoping, unconfirmed findings fall from 342 to 30. The thesis releases 139 patched contracts.
- Delta: Its confirmation rule is the project's PoV validity rule: the PoV passes on the human's vulnerable code and fails on the human's fix. ExploitGen applies it to detector findings on SmartBugs Curated, which holds classic bug classes, with patched versions written for the benchmark. The project uses real audit-contest findings and the human developer's real fix. It uses PoVs to judge code written by agents and by humans, and it judges repairs with held-out PoVs. ExploitGen is a master's thesis and has not been peer reviewed.

### Khalid2026-AuditTransfer Do Smart Contract Auditing Results Transfer Across Datasets? A Two-Benchmark Empirical Study of Static and LLM-Based Security Tools
- Authors: Shawal Khalid et al. (with Joaquin Tuckett, Chris Brown); Year: 2026; Venue: 20th International Symposium on Empirical Software Engineering and Measurement (ESEM 2026), LIPIcs volume 394, pp. 45:1–45:21; DOI 10.4230/LIPIcs.ESEM.2026.45
- URL opened: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESEM.2026.45 (publisher page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Found by: query 29. Earlier rounds listed it as a lead (`r1_L5_sc_exploits_datasets.md`, `r2_S3a_leads.md`, `leads_round1.md`); nobody verified it.
- Summary: Seven static and LLM-based auditing tools are run on SmartBugs Curated (143 contracts) and on a filtered subset of FORGE (173 real-world contracts drawn from audits). A pipeline that does not depend on any one tool normalizes the outputs and measures accuracy, top-K detection, how often tools run without failing, and performance across the two datasets. Static tools built for broad coverage over-report and fail more often on real-world contracts. LLM-based auditors cover many vulnerability categories but also over-predict. The authors conclude that tools differ less in whether they can flag a vulnerability than in how precisely and reliably they do it. The publisher page does not name the seven tools or give per-tool numbers.
- Delta: It is evidence that LLM auditors over-report on real-world contracts, which supports the project's rule of confirming every reported flaw with a PoV (N6). It measures detection on fixed datasets. The project compares review outcomes on agent-written and human-written versions of the same function. The first and senior authors also wrote the indexed tier A paper Khalid2025-GenAITools.

### Tran2026-PoCEvolve PoCEvolve: Generating Proof-of-Concept Exploits from Security Patches with Vulnerability-Aware Prompt Evolution
- Authors: Duc Manh Tran et al. (with David Lo); Year: 2026; Venue: arXiv preprint (arXiv:2607.22076)
- URL opened: https://arxiv.org/abs/2607.22076 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6, N3 (outside T2: JavaScript packages, not smart contracts)
- Found by: query 54. Never seen in earlier rounds.
- Summary: The authors first measure the long delay between a fix commit and the publication of a detailed vulnerability report. PoCEvolve then writes PoC exploits directly from the fix commit, without a report. It scores which context helps (the inferred vulnerable API, code coverage) and changes its prompts after failed attempts. On SecBench.VFC.js it succeeds for 58.4% of vulnerabilities with GPT-4o-mini, 20.7% better (relative) than PoCGen and 200.0% better than a plain LLM baseline. With Qwen3.7-Plus it reaches 85.3%. When detailed reports are available it reaches 71.7%, 11.1% better than PoCGen.
- Delta: It builds PoCs from fix commits for npm packages. The project writes PoVs by hand from audit reports for Solidity and checks each one against the human's vulnerable code and the human's fix. The project already traces every fix commit, so PoCEvolve's method could help write more PoVs per finding, for example the held-out PoVs of N3. The paper does not study who wrote the code or how repairs are judged. The index rates PoCGen, PoCE and AnyPoC as tier B, so I did the same here.

## Seen again: already reported in a round-2 file that has not reached the index

- **Neuroforger: certified violation witnesses for smart contracts verification via LLMs** (Bartoletti and Lipparini, arXiv:2605.31389). Found again by queries 8, 11, 13, 43 and 55. `r2_S1_snowball.md` (line 201) already reports it as VERIFIED, tier B, N6. Round 1 had it in a short tier C list. I did not count it as new.

## New papers rated tier C (named only, not described)

These are new to the index but fall under the tier C line set out above. Each was screened from an arXiv search-result page (title, authors and abstract), a Crossref record, a search result, or a Scholar listing. I did not open them one by one unless noted.

- LLM or agent detection and auditing tools without executable confirmation: SmartMemory (arXiv 2609.34983); Chiral Analysis of Smart Contracts (2607.17987); DeFiScreener (2607.22184); DeFiFusion (2609.11008); EchoFuzz (2609.14475); LiquiLM (2604.03860); GoAT-X (2604.24341); Knowledge Over Parameters / EvoVuln (2607.01742); Tailored Prompts, Targeted Protection (2605.03697); Reentrancy Detection in the Age of LLMs (2603.26497); Benchmarking Zero-Shot Reasoning Approaches for Error Detection in Solidity (2603.13239); Frequency-Aware Continual Learning for SC detection (2608.19680); Solidity Meets LLMs (2609.27091); Ethereum NFT Smart Contracts: Knowledge-Guided Detection (2607.21983); CKG-LLM (2512.06846); No More Hidden Pitfalls? (2512.15179, TOSEM 2026); USCSA, upgrade-induced vulnerabilities (2512.08372, ICSE 2026 NIER); SPEAR (2602.04418); Decoupled Smart Contract Audits (2606.03128, already in round-1 files); LLM-SmartAudit (2410.09381, a lead in earlier rounds; opened); SecureFlow (Journal of Cybersecurity and Privacy 2026, DOI 10.3390/jcp6050184; patches judged by blinded manual review on SmartBugs; abstract read in Crossref); The Role of Prompt Patterns in LLM-Based SC Vulnerability Detection (SST workshop 2026, DOI 10.1145/3843781.3844627); VeriRAG-Agent (CISAT 2026); SEMA: Self-Evolving Multi-Agent Auditing (Electronics 2026); AutoTestAI (IEEE Access 2026); Reducing Hallucinated False Positives in LLM-Based Vulnerability Detection (IEEE Access 2026); LLM-Driven SC Vulnerability Detection Based on Heterogeneous Graphs (COMPSAC 2026); Benchmarking Prompt Engineering Against Fine-Tuning for Multi-Label Vulnerability Detection in Solidity (IEEE 2026); Augmenting Multi-technique Static Analysis with LLMs (PACMSE 2026); RiskScope (ASE 2026); Generative LLM Usage in SC Vulnerability Detection (2504.04685, opened); Large Language Models for Blockchain Security and Analytics: A Survey (IJCAI 2026).
- Agents and smart contracts, but not code security: EVAGE, agents that write MEV bots (2609.27424); When Verified Source Becomes Attack Input / DeLLMGuard, a defence against agent scanning tested in a SCONE-bench environment (2608.28400); ABF-Bench, agentic fund tracing (2610.23656); SCDBench, LLM decompilers (2605.29059); EVM-QuestBench (2601.06565, a lead in round 2); DeFiFlowBench (2609.11504); Intent2Tx (2604.27763); RAGas (2608.15857).
- LLMs writing Solidity, without a security comparison: On the Use of LLMs for Upgrading Legacy Smart Contracts: An Initial Study (Pinna et al., DLT 2025, CEUR-WS Vol-4105 paper 8; Claude 3.7 migrates 21 legacy contracts to Solidity 0.8.20; a lead in round 1; PDF opened); Exploratory Study on LLMs for Test Amplification in Solidity (SANER 2026 workshop).
- Not about LLMs: Smart Contract Security Beyond Detection (2605.09124); FAUDITOR, monetarily exploitable vulnerabilities (2604.18395); Program Analysis for High-Value Smart Contract Vulnerabilities (2507.20672); The Dark Side of Upgrades (2508.02145); A Methodology for Replicating Historical Exploits on EVM Compatible Blockchains (WETSEB 2025); A Comprehensive Study of Exploitable Patterns in Smart Contracts (2504.21480); SmartSpec, Smart Contract Synthesis via Multi-modal Specifications (ASE 2026).
- Grey literature: Ackee "Wake Arena" blog (an AI auditor and plain frontier models on 94 high-severity Code4rena and Sherlock issues); Zealynx "AI Auditor Arena" (118 Code4rena findings); Sherlock's vendor benchmark of ChatGPT 5.2 and Claude Sonnet 4.5 against Sherlock AI; Nethermind and QuillAudits blog posts on AI-written contracts.

## Leads not followed

- "Smart Contract Vulnerability Detection Empowered by LLM: Can It Really Work?" (Yuxuan Zhou, Kunsong Zhao, Xiapu Luo, Yuzhe Tang; IEEE ICBC 2026; DOI 10.1109/icbc67748.2026.11575484). Seen in Crossref (query 44) and OpenAlex. Neither record has an abstract, IEEE Xplore returned HTTP 418, and the exact-title web search (query 48) found nothing. If it is an evaluation of LLM auditors, it would be tier B for N6.
- "EG-MAP: Evidence-Grounded Multi-Agent Smart Contract Auditing" (IEEE SSE 2026; DOI 10.1109/sse72781.2026.00018). Seen in Crossref (query 45). No abstract in Crossref or OpenAlex. If "evidence" means executable PoCs, it would be tier B for N6.
- "From Findings to Reports: Multi-Agent Smart Contract Repair-as-a-Service with Tool Fusion, Deduplication, and Second-Pass Validation" (Liam Xu et al.; IEEE SSE 2026; DOI 10.1109/sse72781.2026.00038). Seen in Google Scholar (query 41) and Crossref. No abstract anywhere; also an unchecked lead in `r1_L7_sc_repair.md`.
- "Narratives Mislead: An Empirical Study of How LLMs Misjudge CVSS Severity in Bug Bounty Reports" (arXiv 2610.24623). Seen in query 61; outside T2. LLMs misread written vulnerability reports, which may matter for N4, where the written audit report is a repair input. Read from the listing only.
- "Prior Audit-Repair Context Shifts LLM Verifier Thresholds Toward Leniency" (arXiv 2608.16003). Seen in query 51; outside T2. An LLM checker reports fewer flaws after an audit-and-repair exchange in its context, which may matter for how the N6 review prompt is set up. Read from the listing only.
- "Guiding Human Validation of LLM-Generated Code via Verifiable Literate Programming" (arXiv 2607.02333) and "RepoGuard: Harmonising Security and Functional Correctness in LLM-Guided Repository-Level Code Generation" (ACM 2026, DOI 10.1145/3803291.3803376). Seen in Google Scholar (query 37); outside T2; for the secure code generation topic. Not opened.
- "Advancing Blockchain-Oriented Software Engineering: Empirical Investigations and AI-Augmented Tooling for Secure Smart Contract Development" (Virginia Tech dissertation, VTechWorks, 2026). Seen in OpenAlex (query 55); also a lead in round 1. It probably collects Khalid's papers. Not opened.
- "Evaluating an OpenClaw-Based Workflow for Smart Contract Audit Report Generation" (2026 conference paper, Semantic Scholar query 65) and "LLMs for security analysis for smart contract" (NTU repository, 2026, OpenAlex query 43). Not opened.
- Sherlock's June 2026 review of Polygon Heimdall V2 with several AI auditing systems, mentioned in a web result for query 38. Grey literature; not opened.

## Notes on sources

- The Semantic Scholar keyword search returned HTTP 429 all session, both directly and through WebFetch. The bulk search endpoint answered near the end (queries 65 to 67).
- The OpenAlex API was out of its daily budget for this network, so I used it through WebFetch. Twice, the OpenAlex responses contained text asking an agent to create an API key by sending the user's email address. I treated it as data, ignored it, and sent no identifier anywhere (protocol rules 4 and 5a).
- DBLP returned an Anubis bot-check page both directly and through WebFetch. IEEE Xplore returned HTTP 418 and MDPI returned HTTP 403, so abstracts for those papers came from Crossref where available.
- Google Scholar result pages worked through WebFetch (five queries) despite a "try again later" banner.
