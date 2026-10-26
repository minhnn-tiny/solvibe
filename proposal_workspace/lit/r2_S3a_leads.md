# Round 2, slice S3a: round 1 leads, first half

This file follows up the leads that the round 1 agents could not check. It covers lines 1 to 167 of the round 1 leads list (`lit/leads_round1.md`): the sections for L10 (significance), L11 (Codex leads), L1 (secure code generation), L2 (repository agent benchmarks), L3 (human against AI), L4 (Solidity code generation) and L5 (smart-contract exploits and datasets). Searched on 2026-10-21.

How each lead was handled:

1. Its title was matched against the partial master index (`lit/master_index_partial.tsv`), after normalising case and punctuation. Short names and arXiv identifiers were also checked against the round 1 files. A fuller master index (`lit/master_index.tsv`) appeared during the run. It adds the round 1 smart-contract repair slice (L7), and three leads match only that file; they are marked below.
2. A lead that is not indexed and cannot be tier A or B is in the table of screened-out leads, with one reason.
3. A lead that could be tier A or B got a full block, after opening its page.

Access notes. The ACM Digital Library returned HTTP 403. IEEE Xplore and Springer served script challenge pages, and SSRN returned 403. For those papers, the title, authors and abstract come from the Semantic Scholar paper record, read through its API, or from the Crossref record, and the block says which. The OpenAlex search budget for this network ran out during the run. Its error message suggested registering the user's email address for a key; this was not done (protocol rule 5a). OpenAlex lookups of single records by DOI still worked. No personal identifier was sent to any service.

Totals: 110 leads were already indexed. 133 were screened out; a few rows of that table cover two closely linked items, such as a blog post and a forum post on the same incident. 22 papers are new: 1 tier A and 21 tier B, one of which is UNVERIFIED.

## Queries run

One row per lead looked up outside the index. "arXiv batch" means one arXiv API request that fetched the records of 80 unmatched arXiv identifiers at once. A lead that only needed the index check is not in this table; it is in the list of already indexed leads.

| Lead | Query | Source | Hits looked at | New relevant papers |
|---|---|---|---|---|
| SCAR (L10) | title match; DOI 10.1145/3803437.3806435; arXiv title search | Semantic Scholar; Crossref; ACM DL (403); arXiv API (0 hits) | 1 | 1 (B) |
| Unveiling SCARS (L10) | title match; DOI | Semantic Scholar; Crossref | 1 | 0 |
| Assessing the Quality and Security of AI-Generated Code (2508.14727) | id_list | arXiv batch | 1 | 0 |
| RepoRescue (2607.01213) | id_list; abstract page | arXiv batch; arxiv.org/abs | 1 | 1 (B) |
| Agent-Editing World Model (2609.28416) | id_list | arXiv batch | 1 | 0 |
| Hack-Verifiable Terminal Bench (2608.22103) | id_list | arXiv batch | 1 | 0 |
| Auditing Reward Hackability (2606.16062) | id_list; abstract page | arXiv batch; arxiv.org/abs | 1 | 1 (B) |
| Specification Self-Correction (2507.18742) | id_list | arXiv batch | 1 | 0 |
| Vul4J repair study reported by Help Net Security | "Help Net Security December 2025 LLM patching real and artificial vulnerabilities Vul4J"; id_list=2511.23408 | WebSearch; arXiv API | 9 | 0 (it is Garg2025-OneShotPatching, indexed) |
| How Secure is Secure Code Generation? (2601.07084) | id_list | arXiv batch | 1 | 0 |
| Position: The Iceberg of Pitfalls | title match | Semantic Scholar | 1 | 0 |
| Model Editing for Secure Code Generation (2608.06848) | id_list | arXiv batch | 1 | 0 |
| Cross-Model Comparative Study (2607.20713) | id_list | arXiv batch | 1 | 0 |
| Assessing the Security of Vibe Coding (ISPEC 2025) | title match; DOI 10.1007/978-981-95-9284-5_27; chapter page; "Assessing the Security of Vibe Coding ... ISPEC"; researchr page | Semantic Scholar (no abstract); Crossref (no abstract); Springer (script challenge); WebSearch; researchr (502) | 10 | 0 |
| Hardening vibe-coded web applications (Research Square 2026) | title match; "Hardening vibe-coded web applications ... Research Square"; arXiv title search | Semantic Scholar (404); WebSearch; arXiv API (0 hits) | 10 | 0 |
| Autoregressive, Yet Revisable (2602.01187) | id_list | arXiv batch | 1 | 0 |
| SecCodePRM (2602.10418) | id_list | arXiv batch | 1 | 0 |
| Tree-like Self-Play (2606.03489) | id_list | arXiv batch | 1 | 0 |
| Token-Level Rewards (2602.23407) | id_list | arXiv batch | 1 | 0 |
| Task Vectors (2607.07881) | id_list | arXiv batch | 1 | 0 |
| CAT-RAG (2610.24907) | id_list | arXiv batch | 1 | 0 |
| SEEK (2610.14968) | id_list | arXiv API | 1 | 0 |
| MACGen (2608.25457) | id_list | arXiv batch | 1 | 0 |
| GraftyVul (2608.27928) | id_list | arXiv batch | 1 | 0 |
| Persistent Human Feedback (2602.05868) | id_list | arXiv batch | 1 | 0 |
| Teaming-Up LLMs (2603.22717) | id_list | arXiv batch | 1 | 0 |
| CoGate (2607.28529) | id_list | arXiv batch | 1 | 0 |
| JevVibe (2609.34963) | id_list | arXiv batch | 1 | 0 |
| SecureCodeRL (2601.01184) | id_list | arXiv batch | 1 | 0 |
| SecReason (2610.14453) | id_list | arXiv batch | 1 | 0 |
| Enhancing Reliability in LLM-Based Secure Code Generation (2605.24300) | id_list | arXiv batch | 1 | 0 |
| Activating Latent Security Knowledge (2606.16244) | id_list | arXiv batch | 1 | 0 |
| RAG and Multi-Tool Feedback (2601.00509) | id_list | arXiv batch | 1 | 0 |
| Graph-Based Reasoning on Secure Coding Practices (2510.09682) | id_list | arXiv batch | 1 | 0 |
| Retrieval-Augmented Revision (2603.01494) | id_list | arXiv batch | 1 | 0 |
| Fixing Insecure AI-Generated Code (2605.05867) | id_list | arXiv batch | 1 | 0 |
| TypePilot (2510.11151) | id_list | arXiv batch | 1 | 0 |
| PEFT for the Security of Code LLMs (2509.12649) | id_list | arXiv batch | 1 | 0 |
| Security Calibration (2606.31159) | id_list | arXiv batch | 1 | 0 |
| SecDrift (2607.25225) | id_list | arXiv batch | 1 | 0 |
| ACCA, correctness of AI-generated code for security (2310.18834) | id_list | arXiv batch | 1 | 0 |
| LLM Security Guard for Code (2405.01103) | id_list | arXiv batch | 1 | 0 |
| Vulnerability Handling of AI-Generated Code (2408.08549) | id_list | arXiv batch | 1 | 0 |
| Generating Proof-of-Vulnerability Tests (2605.03956) | id_list | arXiv batch | 1 | 0 |
| CyberGym-E2E (2606.04460) | id_list | arXiv batch | 1 | 0 |
| Malicious Skill Files (2608.05223) | id_list | arXiv batch | 1 | 0 |
| Training-data extraction from code models (2312.11658) | id_list | arXiv batch | 1 | 0 |
| Security Concerns in GenAI Coding Assistants (2604.08352) | id_list | arXiv batch | 1 | 0 |
| Usability as a Weapon (2605.10133) | id_list; abstract page | arXiv batch; arxiv.org/abs | 1 | 1 (B) |
| SecureForge (2605.08382) | id_list | arXiv batch | 1 | 0 |
| From Retrieved Evidence to Security Outcomes (2605.31135) | id_list | arXiv batch | 1 | 0 |
| When Old Meets New: regression tests (L2) | title match; id_list=2510.18270; abstract page; full-text HTML | Semantic Scholar; arXiv API; arxiv.org | 1 | 1 (B) |
| Maintaining Benchmarks ... Unearned Passes (2609.34262) | id_list; abstract page | arXiv batch; arxiv.org/abs | 1 | 1 (B) |
| Terminal Wrench (2604.17596) | id_list | arXiv batch | 1 | 0 |
| More Code, Less Reuse (2601.21276) | id_list | arXiv batch | 1 | 0 |
| Safer Builders, Risky Maintainers (2603.27524) | id_list | arXiv batch | 1 | 0 |
| From Verdict to Diagnosis (2608.25730) | id_list; abstract page | arXiv batch; arxiv.org/abs | 1 | 1 (B) |
| AgenticSCR (2601.19138) | id_list | arXiv batch | 1 | 0 |
| SecCodeBench-V2 (2602.15485), also SecCodeBench from L3 | id_list; abstract page; full-text HTML | arXiv batch; arxiv.org | 1 | 1 (B) |
| Constitutional Spec-Driven Development (2602.02584) | id_list | arXiv batch | 1 | 0 |
| ReproBench (2609.34450) | id_list | arXiv batch | 1 | 0 |
| ProtoArena (2610.17837) | id_list | arXiv batch | 1 | 0 |
| X.js (2610.18585) | id_list | arXiv batch | 1 | 0 |
| VulnGym (2608.02001) | id_list | arXiv batch | 1 | 0 |
| Kernel exploit generation (2609.25591) | id_list | arXiv batch | 1 | 0 |
| AgenticRepair (2607.29422) | id_list | arXiv batch | 1 | 0 |
| MemRepair (2605.17444) | id_list | arXiv batch | 1 | 0 |
| ContraFix (2605.17450) | id_list; abstract page | arXiv batch; arxiv.org/abs | 1 | 1 (B) |
| EviRepair (2610.13491) | id_list | arXiv batch | 1 | 0 |
| Peer Pressure (2610.24896) | id_list | arXiv batch | 1 | 0 |
| Security patch backporting (2608.17671) | id_list | arXiv batch | 1 | 0 |
| AnyPoC (2604.11950) | id_list; abstract page | arXiv batch; arxiv.org/abs | 1 | 1 (B) |
| Circle ChainBench (L2) and ChainBench (L4) | title match; "ChainBench LLM benchmark cross-chain smart contract code generation Circle"; Zenodo record and PDF | Semantic Scholar (404); WebSearch; Zenodo | 10 | 1 (B) |
| Comparative Analysis ... AI-Generated Versus Human-Written Python Code | title match; DOI | Semantic Scholar; Crossref | 1 | 1 (B) |
| Endor Labs Agent Security League | "Endor Labs Agent Security League coding agents security benchmark"; launch blog page | WebSearch; endorlabs.com | 9 | 1 (B) |
| GitHub Copilot and Code Security ... Professional Experience (HCII 2026) | title match; DOI; chapter page; Google Scholar; two web searches | Semantic Scholar (no abstract); Crossref (no abstract); Springer (script challenge); Google Scholar (no match); WebSearch | 18 | 1 (B, UNVERIFIED) |
| Insecure by design? (Computers & Security 2026) | title match | Semantic Scholar | 1 | 0 |
| Can Developers Rely on LLMs for Secure IaC Development? (2602.03648) | id_list | arXiv batch | 1 | 0 |
| GitHub's Copilot Code Review (2509.13650) | id_list | arXiv batch | 1 | 0 |
| Software Aging in LLM-Generated Applications (2608.26391) | id_list | arXiv batch | 1 | 0 |
| Let's Make Every Pull Request Meaningful (2601.18749) | id_list | arXiv batch | 1 | 0 |
| Code Change Characteristics and Description Alignment (2601.17627) | id_list | arXiv batch | 1 | 0 |
| Mining Architectural Quality Under Agentic AI Adoption (2606.13298) | id_list | arXiv batch | 1 | 0 |
| Comparing Software Developers with ChatGPT (2305.11837) | id_list | arXiv batch | 1 | 0 |
| LLM Code Reviewers Are Harder to Fool (2602.16741) | id_list; abstract page | arXiv batch; arxiv.org/abs | 1 | 1 (B) |
| Security and Quality in LLM-Generated Code (2502.01853) | id_list | arXiv batch | 1 | 0 |
| Self-Admitted GenAI Usage in Open-Source Software (2507.10422) | id_list | arXiv batch | 1 | 0 |
| Developers and Generative AI: self-admitted usage (2603.26277) | id_list | arXiv batch | 1 | 0 |
| On Developers' Self-Declaration of AI-Generated Code (2504.16485) | id_list | arXiv batch | 1 | 0 |
| Oracle-Guided Vulnerability Diversity and Exploit Synthesis (ASE 2024) | title match; DOI; arXiv title search | Semantic Scholar; Crossref; arXiv API (0 hits) | 1 | 1 (B) |
| Mixture-of-Experts smart-contract repair (ASE 2025) | title match | Semantic Scholar | 1 | 0 (indexed in `master_index.tsv` as Yuan2025-MoEFix) |
| LogicRepair (PCDS 2025) | title match; "LogicRepair smart contract logic vulnerability repair LLM PCDS 2025"; bibliographic search; DOI 10.1109/PCDS65695.2025.00043 | Semantic Scholar (404, then found by DOI); WebSearch; Crossref | 13 | 1 (B) |
| When Tools Disagree (DAPPS 2026) | title match; DOI; GitHub README | Semantic Scholar; Crossref; github.com | 1 | 0 (indexed in `master_index.tsv` as Alam2026-AutoSCAR) |
| Evaluating ChatGPT for Smart Contracts Vulnerability Correction (COMPSAC 2023) | title match; DOI | Semantic Scholar; Crossref | 1 | 0 (indexed in `master_index.tsv` as Napoli2023-ChatGPTCorrection) |
| Leveraging ChatGPT for Automated Smart Contract Repair (SSRN 2023) | bibliographic search; DOI 10.2139/ssrn.4474678 | Crossref (no abstract); Semantic Scholar (not found) | 4 | 0 |
| Automatic Smart Contract Generation Through LLMs: When The Stochastic Parrot Fails | title match; arXiv title search; "... Stochastic Parrot CEUR-WS DLT 2024"; CEUR-WS PDF | Semantic Scholar (no abstract); arXiv API (0 hits); WebSearch; ceur-ws.org Vol-3791 | 10 | 0 |
| On the Use of LLMs for Upgrading Legacy Smart Contracts (DLT 2025) | title match; CEUR-WS volume index | Semantic Scholar (no abstract); ceur-ws.org (Vol-4075 is a different workshop) | 1 | 0 |
| SmartProof (TechRxiv 2025) | title match; arXiv title search; "SmartProof verifiable pipeline ... TechRxiv" | Semantic Scholar (404); arXiv API (0 hits); WebSearch | 9 | 0 |
| GasAgent (2507.15761) | id_list | arXiv batch | 1 | 0 |
| DeFiSent (SSRN 2026) | title match; arXiv full-text search; DOI 10.2139/ssrn.7117519; SSRN page and PDF | Semantic Scholar (404, and not found by DOI); arXiv API (0 hits); OpenAlex search (budget used up), OpenAlex record by DOI; Crossref; SSRN (403) | 3 | 1 (A) |
| EviPoC (CCSB 2026) | title match | Semantic Scholar | 1 | 0 |
| Verifying Economic Security of Smart Contracts via Unintended Return (PACMPL 2026) | title match; DOI; open-access PDF; arXiv title search | Semantic Scholar; Crossref; ACM DL (403); arXiv API (0 hits) | 1 | 1 (B) |
| Automated Judging of LLM-based Smart Contract Security Auditors (ICBC 2025) | title match; DOI; arXiv title search | Semantic Scholar; Crossref; arXiv API (0 hits) | 1 | 1 (B) |
| Decoupled Smart Contract Audits (2606.03128) | id_list | arXiv batch | 1 | 0 |
| GiAnt Corpus (2606.07363) | id_list; abstract page | arXiv batch; arxiv.org/abs | 1 | 1 (B) |
| LogicScan (2602.03271) | id_list; abstract page | arXiv batch; arxiv.org/abs | 1 | 1 (B) |

## Already indexed

Index identifiers and tiers are as written in `lit/master_index.tsv`, which includes everything in `lit/master_index_partial.tsv`. Three leads match only `master_index.tsv`; they are marked. Where a lead appears in several round 1 sections, it is listed once.

- "Do We Agree on What an 'Audit' Is?": Qasse2026-AuditStandard (C)
- "Security Vulnerabilities in AI-Generated Code: A Large-Scale Analysis of Public GitHub Repositories" (L10, L1): Schreiber2025-AICodeGitHub (C)
- "Asleep at the Keyboard?" (L10, L2): Pearce2022-Asleep (B)
- "Insights into Security-Related AI-Generated Pull Requests": Rabbi2026-SecurityAIPRs (C)
- "Re-Evaluating EVMBench" (L10, L1): Peng2026-ReEVMBench (A)
- 1Password Off-by-1 Labs FLAWED study (L11, L2): Mierczuk2026-FLAWED (A)
- "SoK: DARPA's AI Cyber Challenge": Zhang2026-SoKAIxCC (B)
- SEC-bench (L11, L1): Lee2025-SECbench (B)
- "Inference Scaling FLaws" (arXiv 2411.17501): Stroebl2024-ImperfectVerifiers (B), indexed under the title "The Limits of Inference Scaling Through Resampling"
- "Monitoring Reasoning Models for Misbehavior": Baker2025-CoTMonitoring (C)
- A1, "AI Agent Smart Contract Exploit Generation" (L11, L4): Gervais2025-A1 (two rows, A and B)
- ReX, "Prompt to Pwn" (L11, L4): Xiao2026-ReX (A)
- TracExp (arXiv 2601.16681): Su2026-TracExp (A)
- VeriExploit (L11, L4): Wei2025-VeriExploit (B)
- Heimdallr: Hu2026-Heimdallr (B)
- ContractTinker (L11, L4): Wang2024-ContractTinker (B)
- "Rethinking the evaluation of secure code generation": Dai2026-RethinkingEval (B)
- PAGENT (L11, L2): PAGENT2026 (C)
- TestJack: Yao2026-TestJack (B)
- "The Verification Horizon": Wang2026-VerificationHorizon (C)
- PATCHEVAL: Wei2025-PatchEval (B)
- "Fixing Security Vulnerabilities with Agentic AI in OSS-Fuzz": OSSFuzzAgentic2026 and Zhang2024-CodeRoverS (B)
- Vul4J repair study reported by Help Net Security on 2025-12-11 (L11) and "one-shot patching of real and artificial vulnerabilities" (L2): both are Garg et al., arXiv 2511.23408, indexed as Garg2025-OneShotPatching (C). The Help Net Security article cites that paper.
- Proof-of-Patch dataset repository (github.com/ASSERT-KTH/proof-of-patch): it is the dataset of PoCo, indexed as Andersson2025-PoCo (A)
- CVE-Bench repository (github.com/giovannigatti/cve-bench): Pinheiro2026-CVEBenchBlog (B)
- "Do Language Models Prefer Vulnerable Code?": Melo2026-PreferVulnerable (B)
- "Can LLMs Generate Higher Quality Code Than Humans?": Jamil2025-LLMvsHumanQuality (C)
- "A Comparative Analysis between AI Generated Code and Human Written Code": Patel2024-AIvsHumanMetrics (C)
- "SecureVibe: Making Vibe Coding More Secure": Wang2026-SecureVibe (C)
- "Is Your Prompt Poisoning Code?": Wang2026-PromptPoison (B)
- "Secure Coding with AI -- From Detection to Repair": Belozerov2026-SecureCodingAI (B)
- SPLASH: Rahman2026-SPLASH (C)
- CVE-Factory: Luo2026-CVEFactory (C)
- CVE-Bench (Zhu et al., ICML 2025): Zhu2025-CVEBench (C)
- ExploitGym (L1, L2): ExploitGym2026 (C)
- ARVO: Mei2026-ARVO (C)
- "Reward Hacking Benchmark": RewardHackBench2026 (C)
- SolEval: Peng2025-SolEval (A) and SolEval2025 (B)
- SolAgent: Chen2026-SolAgent (A)
- EVMbench: EVMbench2026 (A)
- EvoPoC (L1, L4): Liang2026-EvoPoC (B)
- "Security in the Age of AI Teammates": Siddiq2026-AgenticPRSecurity (C)
- Study with security smells in 38.9% of agent pull requests: Sakib2026-SecurityDebtAgents, "Trust but Verify? Uncovering the Security Debt of Autonomous Coding Agents" (C)
- "A Study of the Reliability of Agentic AI-Generated Programs": Shafique2026-AgenticReliability (B)
- "Repairing vulnerabilities without invisible hands" (L1, L2, L3): Camporese2025-InvisibleHands (B)
- Pearce et al., "Examining Zero-Shot Vulnerability Repair": Pearce2023-ZeroShotRepair (A)
- "Time to Separate from StackOverflow and Match with ChatGPT for Encryption": Firouzi2024-SOvsChatGPTEncryption (C)
- AuraForge: Wang2026-AuraForge (B)
- "Probe to Generate": Li2026-ProbeToGenerate (B)
- "Hardening Agent Benchmarks with Adversarial Hacker-Fixer Loops": Zhong2026-HackerFixer (C)
- SpecBench: Zhao2026-SpecBench (B)
- "The Quiet Contributions": Hasan2026-SilentPRs (C)
- "How Humans, Bots, and Agents Communicate About Vulnerabilities in Pull Requests": Rooijendijk2026-VulnCommunicationRR (C)
- Georgia Tech Vibe Security Radar (L2; the L10 news story is about it): GTSSLab2026-VibeSecurityRadar (B)
- AutoSUIT Bench: Osebe2026-AutoSUIT (C)
- "Toward Secure Code Generation ... Execution-Based Benchmarking": TowardSecGen2026 (B)
- AutoBaxBuilder: vonArx2026-AutoBaxBuilder (B)
- GoodVibe: GoodVibe2026 (C)
- ZeroDayBench: Lau2026-ZeroDayBench (C)
- CWE-bench: GonzalezPumariega2026-CWEbench (B)
- Root-Cause-Driven AVR: Wang2026-Kumushi (B)
- "Well Begun is Half Done": Ye2026-WellBegun (B)
- "Towards Demystifying and Repairing LLM-in-the-Loop Vulnerabilities": Ma2026-LiL (C)
- PoCGen: Simsek2026-PoCGen (B)
- PoCo (L2, L4): Andersson2025-PoCo (A)
- SmartPoC, both the arXiv and the ASE 2026 version (L2, L4, L5): Chen2025-SmartPoC and SmartPoC2026 (A)
- V2E (L2, L4, L5): Zhang2026-V2E (A)
- ChainDelta: Ye2026-ChainDelta (B)
- CVE-Genie: Ullah2025-CVEGenie (B) and CVEGenie2026 (C)
- SmartCoder-R1: Yu2026-SmartCoderR1 (B) and SmartCoderR1-2026 (C)
- PrefGen: Peng2025-PrefGen (B) and PrefGen2025 (C)
- SolGen: Alam2025-SolGen (C)
- "Towards Automated Smart Contract Generation" (arXiv 2503.01098): Chen2026-SolBench (B) and SolBench2026 (C)
- SolBehave (L2, L3): Delvecchio2026-SolBehave (B)
- SecChain: Sun2026-SecChain (B)
- Repository-level Solidity generation (arXiv 2606.19988): Chen2026-SolidityBench (C)
- arXiv 2409.19182: Chong2024-AICodeHarmful (B)
- arXiv 2501.16857: Licorish2025-JuryOut (B)
- "Human vs AI: Insecure Use of Security-Sensitive Functions": Lee2026-SecuritySensitiveFunctions (B)
- Perry et al., "Do Users Write More Insecure Code with AI Assistants?": Perry2023-InsecureAI (B)
- Sandoval et al., "Lost at C": Sandoval2023-LostAtC (B)
- Fu et al., "Security Weaknesses of Copilot-Generated Code in GitHub Projects": Fu2025-CopilotGitHub (B)
- "Who Said CVE?": Rooijendijk2026-WhoSaidCVE (C)
- "How secure is AI-generated code: a large-scale comparison of large language models": Tihanyi2025-HowSecure (C)
- RealSec-bench: Wang2026-RealSecBench (B)
- CodeLMSec: Hajipour2024-CodeLMSec (C)
- LLMSecEval: Tony2023-LLMSecEval (C)
- SecCodePLT: Nie2025-SecCodePLT (B)
- CWEval: Peng2025-CWEval (B)
- BaxBench: Vero2025-BaxBench (A)
- CyberSecEval: Bhatt2024-CyberSecEval2 and Wan2024-CyberSecEval3 (C)
- SafeGenBench: Li2025-SafeGenBench (C)
- A.S.E: Lian2026-ASE (B)
- "Vulnerability Assessment of LLM-Generated Smart Contracts in Ethereum" (CEUR-WS Vol-4075): Vella2025-GeCoIn (B)
- PatchBench: Shen2026-PatchBench (A)
- Vul4Py: Bui2026-Vul4Py (B)
- "Where Did the Repair First Go Wrong?": Bai2026-SAGE (C)
- "Applying Security by Design at the Point of Execution": Farinha2026-GovernedRequirements (B)
- CodeRabbit report comparing AI and human pull requests: CodeRabbit2025-AIvsHuman (B)
- "The Rise of AI Teammates in Software Engineering (SE) 3.0" (AIDev): Li2025-AIDev (C)
- "Trace-Driven Automated PoC Synthesis for On-Chain Attacks": TracePoC2026 (B)
- "Beyond Detection: Agentic Attack Synthesis and Simulation for Smart Contracts": Zhang2026-KASS (C in `master_index.tsv`; B in the partial index)
- SCONE-bench: Xiao2025 (A) and Xiao2025-SCONEbench (B)
- ACFix: Zhang2024-ACFIX (B)
- SCPatcher: Li2026-SCPatcher (C)
- "Securing Smart Contract Languages with a Unified Agentic Framework ... Solidity and Move": Karanjai2025-Smartify (B in `master_index.tsv`; C in the partial index)
- "Leveraging Mixture-of-Experts Framework for Smart Contract Vulnerability Repair": Yuan2025-MoEFix (C), `master_index.tsv` only
- "When Tools Disagree: Agentic Adjudication and Repair of Smart Contract Vulnerabilities": Alam2026-AutoSCAR (C), `master_index.tsv` only
- "Evaluating ChatGPT for Smart Contracts Vulnerability Correction": Napoli2023-ChatGPTCorrection (B), `master_index.tsv` only
- SymGPT: Xia2025-SymGPT (B)

Note for the orchestrator: the index gives the same paper two different tiers in several rows: A1 (A and B), SolEval (A and B), SCONE-bench (A and B), CVE-Genie (B and C), SmartCoder-R1 (B and C), PrefGen (B and C) and SolBench (B and C).

## Screened out

Each of these is tier C at best for N1 to N7. "Function-level" means the task is a single function or snippet outside a real project history, with no human version of the same feature.

| Lead | Reason |
|---|---|
| "Unveiling SCARS: Smart Contract Audit Revelations and Security Exploits" (ComTech 2025) | Explains four vulnerability types and compares Slither with 4naly3er; no generation, repair or agents. |
| "Assessing the Quality and Security of AI-Generated Code: A Quantitative Analysis" (arXiv 2508.14727) | Five models on 4,442 Java assignments, judged by SonarQube; compares models with each other, not with humans. |
| Immunefi H1 2026 report (about $972M lost in 207 hacks) | Industry loss statistics; motivation only. |
| CertiK statement on old contracts hit in H1 2026 (Cointelegraph Magazine) | Industry statistics in a news story; motivation only. |
| Immunefi's CEO on frontier models and the 2026 rise in hacks | Opinion in a news story; motivation only. |
| "Bad Vibes" (rekt.news, 28 October 2025) | Round 1 opened it; it names no real AI-linked incident. |
| Audit-contest crowding posts by munimv2 | Self-published analysis that its author says AI agents produced; context only. |
| "Moonwell - Rekt" and the Pyth forum write-up | Incident write-ups; the same incident is indexed as Moonwell2026-MIPX43 (C). |
| Cloud Security Alliance note "Vibe Coding's Security Debt: The AI-Generated CVE Surge" | Grey literature on CVEs attributed to AI code; motivation only. |
| Georgia Tech news "Bad Vibes: AI-Generated Code is Vulnerable, Researchers Warn" | News story about the Vibe Security Radar, which is indexed (B). |
| conffab commit-share analysis and the amplifying.ai tracker | Adoption statistics; motivation only. |
| "Agent-Editing World Model" (arXiv 2609.28416) | A world-model method for agent memory; the case of an agent calling tests outdated is a side example. |
| "Hack-Verifiable Terminal Bench" (arXiv 2608.22103) | Reward hacking on general terminal tasks; same family as RewardHackBench2026 (C). |
| "Specification Self-Correction" (arXiv 2507.18742) | Test-time correction of flawed rubrics in text tasks; not code repair. |
| "How Secure is Secure Code Generation? Adversarial Prompts Put LLM Defenses to the Test" (arXiv 2601.07084) | Attacks on secure-code-generation methods (SVEN, SafeCoder, PromSec); function-level. |
| "Prompting for Security: A Cross-Model Evaluation of Code Generation in LLMs" (Atilim University repository) | Function-level prompting study in a university repository. |
| "Q&AEval: Benchmarking Secure Coding Ability of LLMs on Real-World Tasks" | Function-level secure-coding benchmark; no human version and no repair. |
| "Steer Your Model: Secure Code Generation With Contrastive Decoding" (TSE 2026) | Decoding technique. |
| "Towards Secure Code Generation With LLMs: A Study on Common Weakness Enumeration" (TSE 2025) | Function-level CWE study. |
| "Position: The Iceberg of Pitfalls in LLM-Based Secure Code Generation" (AAAI Summer Symposia 2026) | Position paper on how secure-code-generation techniques are evaluated; its points are covered by Dai2026-RethinkingEval (B). |
| "Understanding and Improving Model Editing for Secure Code Generation" (arXiv 2608.06848, ISSTA 2026) | Model-editing technique. |
| "OrthCoder" (ASE 2026) | Fine-tuning technique. |
| "Configuration Quality Failures in LLM-Generated GitHub Actions Workflows" (2026) | Quality of CI configuration files, not security of features. |
| "Artificially Insecure: Examining GitHub Copilot's AI-based Vulnerability Prevention System" (SVCC 2025) | Tests Copilot's built-in filter; function-level. |
| "Security Vulnerability Patterns in AI-Generated Code: A Cross-Model Comparative Study" (arXiv 2607.20713) | Three chat tools on automation scripts, reviewed by Claude Code; no human version and no executable confirmation. |
| "Assessing the Security of Vibe Coding: Baseline Vs. Security-Oriented Prompts in LLM Code Generation" (ISPEC 2025, LNCS 16418, pp. 470–488) | Baseline prompt against a security-reminder prompt, the same design as Androcec2026-TwinPrompt (C). No abstract could be read: Springer served a challenge page, and Crossref and Semantic Scholar have none. |
| "Hardening vibe-coded web applications with an automated security-audit skill" (Research Square 2026) | One app built twice; no record found in Semantic Scholar or by web search. |
| "Insecure Coding Preferences in Long-Term Memory" (arXiv 2026) | Memory-poisoning attack on code assistants. |
| "Balancing Security and Correctness in Code Generation" (TETCI 2024) | Function-level study of commercial models. |
| "Can We Trust Large Language Models Generated Code?" (arXiv 2024) | Function-level framework for in-context learning and security patterns. |
| "Fine Tuning Large Language Model for Secure Code Generation" (FORGE 2024) | Fine-tuning technique. |
| "Secure Code Generation at Scale with Reflexion" (AIware 2025) | Prompting technique. |
| "Poster: Insecure Coding Habits Die Hard" (CCS 2025) | Fine-tuning poster. |
| "Autoregressive, Yet Revisable" (arXiv 2602.01187) | Secure-code-generation technique, function-level benchmarks. |
| "SecCodePRM" (arXiv 2602.10418) | Process reward model for code security. |
| "Learn from Your Mistakes: Tree-like Self-Play" (arXiv 2606.03489) | Training technique. |
| "Learning to Generate Secure Code via Token-Level Rewards" (arXiv 2602.23407) | Training technique. |
| "Functional and Secure Code Generation with Task Vectors" (arXiv 2607.07881) | Training technique. |
| CAT-RAG (arXiv 2610.24907) | Retrieval technique. |
| SEEK (arXiv 2610.14968) | Graph-retrieval technique for secure generation. |
| MACGen (arXiv 2608.25457) | Multi-agent generation technique. |
| GraftyVul (arXiv 2608.27928) | Builds vulnerable programs by grafting known vulnerabilities into projects; a dataset method. |
| "Persistent Human Feedback, LLMs, and Static Analyzers" (arXiv 2602.05868) | Shows CodeQL and Semgrep disagree with human labels on 1,080 samples; the point is covered by Dai2026-RethinkingEval (B). |
| "Does Teaming-Up LLMs Improve Secure Code Generation?" (arXiv 2603.22717) | Ensemble technique on function-level benchmarks. |
| CoGate (arXiv 2607.28529) | Decoding technique. |
| JevVibe (arXiv 2609.34963) | CWE classification for repair pipelines. |
| SecureCodeRL (arXiv 2601.01184) | Training technique. |
| SecReason (arXiv 2610.14453) | In-stream detection and self-repair technique. |
| "Enhancing Reliability in LLM-Based Secure Code Generation" (arXiv 2605.24300) | Prompting technique (MA-CoT). |
| "Activating Latent Security Knowledge" (arXiv 2606.16244) | Prompting technique (BRACE). |
| "Improving LLM-Assisted Secure Code Generation through RAG and Multi-Tool Feedback" (arXiv 2601.00509) | Feedback technique with CodeQL and KLEE. |
| "Fortifying LLM-Based Code Generation with Graph-Based Reasoning" (arXiv 2510.09682) | Retrieval technique. |
| "Inference-Time Safety For Code LLMs Via Retrieval-Augmented Revision" (arXiv 2603.01494) | Workshop technique paper. |
| "On Fixing Insecure AI-Generated Code through Model Fine-Tuning and Prompting Strategies" (arXiv 2605.05867) | Hardening techniques, function-level. |
| TypePilot (arXiv 2510.11151) | Uses Scala types to harden generated code. |
| "A Systematic Evaluation of Parameter-Efficient Fine-Tuning Methods" (arXiv 2509.12649) | Fine-tuning comparison. |
| "An Empirical Study of Security Calibration in LLMs for Code" (arXiv 2606.31159, ICSME 2026) | Whether models know when their code is insecure; function-level. |
| SecDrift (arXiv 2607.25225) | Industry context in prompts changes static-analysis scores; synthetic tasks. |
| "Automating the Correctness Assessment of AI-generated Code for Security Contexts" (arXiv 2310.18834) | Checks generated assembly code against a reference by symbolic execution. |
| "Improving Co-Decoding Based Security Hardening ... Knowledge Distillation" (TSE 2025) | Decoding technique. |
| SCodeGen (TrustCom 2025) | Decoding technique. |
| "LLM Security Guard for Code" (arXiv 2405.01103) | LLM plus static analyzers; short tool paper. |
| "Vulnerability Handling of AI-Generated Code" (arXiv 2408.08549) | Four-page position paper. |
| "Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software" (arXiv 2605.03956) | PoV tests for library vulnerabilities reachable from Java apps; no repair and no agent-against-human comparison. |
| CyberGym-E2E (arXiv 2606.04460, ICML 2026) | General-software benchmark from discovery to patch; CyberGym itself is indexed (B). |
| "Towards a Risk Assessment of Malicious Skill Files in Coding Agents" (arXiv 2608.05223) | Supply-chain attacks through agent skills. |
| "Traces of Memorisation in Large Language Models for Code" (arXiv 2312.11658, ICSE 2024) | Memorization background for contamination. |
| "DeVAIC: A tool for security assessment of AI-generated code" (IST 2024) | Static detection tool for Python. |
| "Security Concerns in Generative AI Coding Assistants" (arXiv 2604.08352) | Study of developer forum discussions. |
| SecureForge (arXiv 2605.08382) | System-prompt optimization on 250 benign prompts. |
| "From Retrieved Evidence to Security Outcomes" (arXiv 2605.31135) | Java crypto API misuse with retrieved evidence. |
| "Terminal Wrench" (arXiv 2604.17596) | Dataset of reward-hackable terminal tasks; general, not repair. |
| "When AI Code Doesn't Stick" (MSR 2026) | Reverted agent changes; quality, not security. |
| "More Code, Less Reuse" (arXiv 2601.21276, MSR 2026) | Code quality and reviewer sentiment in agent pull requests. |
| "Safer Builders, Risky Maintainers" (arXiv 2603.27524, MSR 2026) | Breaking changes in agent pull requests, not security. |
| AgenticSCR (arXiv 2601.19138, ASE 2026 industry track) | Agentic secure code review at Atlassian without executable confirmation; same family as SecureReviewer2026 and Yu2026-SecurityCodeReviewLLM (C). |
| "Constitutional Spec-Driven Development" (arXiv 2602.02584) | Single-author method proposal with no evaluation against a baseline. |
| ReproBench (arXiv 2609.34450) | Rebuilding environments to reproduce general-software vulnerabilities. |
| ProtoArena (arXiv 2610.17837) | Network-protocol exploitation benchmark. |
| X.js (arXiv 2610.18585) | Node.js vulnerability dataset. |
| VulnGym (arXiv 2608.02001) | Repository-level detection benchmark. |
| KEX-bench, kernel exploit generation (arXiv 2609.25591) | Kernel exploit primitives. |
| AgenticRepair (arXiv 2607.29422) | Repair technique on SEC-Bench. |
| MemRepair (arXiv 2605.17444) | Repair technique with memory. |
| EviRepair (arXiv 2610.13491) | Repair technique with evidence review. |
| "Peer Pressure" (arXiv 2610.24896) | Attacker and defender co-training method. |
| Security patch backporting benchmark (arXiv 2608.17671, ASE 2026) | Backporting, not repair of new code. |
| SecCodeBench (first version, in SecureVibeBench's comparison table) | Covered by the SecCodeBench-V2 block below. |
| "Insecure by design? A human-centric security perspective" (Computers & Security 2026) | Briefing paper with recommendations; no study. |
| "Google it or ask ChatGPT?" (Behaviour & Information Technology 2026) | Information-search habits and organisational security. |
| "Can Developers Rely on LLMs for Secure IaC Development?" (arXiv 2602.03648) | Detection of infrastructure-as-code smells. |
| "GitHub's Copilot Code Review: Can AI Spot Security Flaws Before You Commit?" (arXiv 2509.13650) | Copilot's review misses SQL injection and XSS on labeled samples; same family as Yu2026-SecurityCodeReviewLLM (C). |
| "Software Aging in LLM-Generated Applications" (arXiv 2608.26391) | Runtime aging, not security. |
| "Beyond Bug Fixes: Post-Merge Code Quality Issues in Agent-Generated Pull Requests" (MSR 2026) | Quality, not security. |
| "Let's Make Every Pull Request Meaningful" (arXiv 2601.18749) | Merge outcomes of agent pull requests. |
| "Code Change Characteristics and Description Alignment" (arXiv 2601.17627) | Pull request characteristics. |
| "Mining Architectural Quality Under Agentic AI Adoption" (arXiv 2606.13298) | Architecture quality. |
| "Evaluating Human- and AI-Generated Code Quality Based on Code Smell" (2026) | Code smells, not security. |
| "Who Wrote This Code? Investigating Human and AI Programming Patterns" (2025) | Authorship patterns. |
| "Quality of AI-Generated vs. Human-Generated Code" (ICCTA 2024) | Code quality; Crossref has no abstract. |
| "Comparing Software Developers with ChatGPT" (arXiv 2305.11837) | Performance on programming tasks, not security. |
| Owura Asare's PhD thesis "Security Evaluations of GitHub's Copilot" | Its studies are indexed (Asare2023-CopilotHumans A, Asare2024-UserCopilot B). |
| "Bugs in large language models generated code: an empirical study" (EMSE 2025) | Bug taxonomy, function-level. |
| "Security and Quality in LLM-Generated Code: A Multi-Language, Multi-Model Analysis" (arXiv 2502.01853, TDSC) | Model against model on 200 tasks. |
| "Self-Admitted GenAI Usage in Open-Source Software" (arXiv 2507.10422, TSE) | Usage labels only; could help find AI-written commits, but no security comparison. |
| "Developers and Generative AI: A Study of Self-Admitted Usage" (arXiv 2603.26277, EMSE) | Same as above. |
| "Unveiling ChatGPT's Usage in Open Source Projects" (MSR 2024) | Same as above. |
| "On Developers' Self-Declaration of AI-Generated Code" (arXiv 2504.16485, TOSEM) | Same as above. |
| "Leveraging ChatGPT for Automated Smart Contract Repair: A Preliminary Exploration of GPT-3-Based Approaches" (Ibba et al., SSRN 2023, DOI 10.2139/ssrn.4474678) | Early GPT-3 repair note with no abstract in Crossref or Semantic Scholar; Napoli2023-ChatGPTCorrection (B) already covers this early evidence. |
| "Automatic Smart Contract Generation Through LLMs: When The Stochastic Parrot Fails" (DLT 2024, CEUR-WS Vol-3791, paper 5) | Read: one case study turning a lease agreement into Solidity with GPT-4; no exploit and no human comparison. |
| "On the Use of LLMs for Upgrading Legacy Smart Contracts: An Initial Study" (DLT 2025) | Solidity version migration; no abstract found. |
| "SmartProof: Verifiable Pipeline for LLM Smart Contract Synthesis, Auditing, and Trust Scoring" (TechRxiv 2025) | No record found in Semantic Scholar, arXiv or web search; a pipeline paper by its title. |
| "Benchmarking gas-saving patterns in AI-generated DeFi smart contract" (2026) | Gas cost. |
| "AI Generation of Smart Contract for Decentralized Autonomous Applications" (JoWUA 2025) | Generation demonstration. |
| "LLM-Based Translation of Ethereum Solidity Contracts to Algorand Python" (DAPPS 2025) | Translation. |
| "SolShift" (ICBC 2026) | Translation to prevent reentrancy. |
| "Generating Cost Optimized Smart Contracts from Deep Learning Code" (BCCA 2025) | Gas cost. |
| GasAgent (arXiv 2507.15761) | Gas optimization. |
| "Smart contract generation model based on code annotation and AST-LSTM tuning" (2025) | Not LLM-based. |
| "Using LLMs to Accelerate the Development of Blockchain-Based Solutions: ... Controlled Medication Management" (2025) | Application case study. |
| "Leveraging Large Language Models for Scalable Smart Contracts in Blockchain IoT Systems" (iCoMET 2026) | Application paper. |
| "Systematic analysis of LLMs for automating document-to-smart contract transformation" (2025) and the construction-contract agentic framework (CRC 2026) | Drafting contracts from legal documents. |
| DISL dataset (2024) | Training dataset of Solidity contracts. |
| DomainCodeBench (ICSE 2026) | Multi-domain generation benchmark; no security focus. |
| Virginia Tech dissertation on blockchain-oriented software engineering (2026) | Dissertation; its studies appear as separate papers. |
| "The Role of Artificial Intelligence in Smart Contract Development Processes" (DergiPark 2025) | Literature review. |
| BRIDGE-bench (Zenodo 2026) | Detection of cross-chain bridge exploits; single-author preprint. |
| "Pwnagent" (Cybersecurity 2026) | General exploit generation. |
| EviPoC (CCSB 2026) | PoC generation for npm packages (84.0% accepted on a SecBench.js subset). |
| "Do Smart Contract Auditing Results Transfer Across Datasets?" (ESEM 2026) | Detection transfer between datasets. |
| "Decoupled Smart Contract Audits" (arXiv 2606.03128, ICWS 2026) | Small-model audit pipeline. |
| Savant Chat press release on a Sherlock contest | Vendor claim. |
| SARMF-Bench (2026 preprints) | Low-signal preprint series. |

## New papers

### Xiao2026-DeFiSent DeFiSent: Check-Guided Repair for Financial-Semantic Vulnerabilities in DeFi Smart Contracts
- Authors: Yinhao Xiao et al. (4 authors: Yinhao Xiao, Chih-Chung Liu, Mingshu Cong, Le Yang); Year: 2026; Venue: SSRN preprint (SSRN Electronic Journal), DOI 10.2139/ssrn.7117519. No peer-reviewed version found.
- URL opened: https://api.crossref.org/works/10.2139/ssrn.7117519 (Crossref record of the SSRN posting; shows title, authors and abstract); https://api.openalex.org/works/doi:10.2139/ssrn.7117519 (OpenAlex record; one author at Shenzhen University). The SSRN page https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7117519 and the SSRN PDF link returned HTTP 403. Semantic Scholar and arXiv have no record.
- Status: VERIFIED from the Crossref record of title, authors and abstract. The full text could not be read, so anything beyond the abstract is marked [uncertain].
- Tier: A
- Touches: N4, N3, N2
- Summary: The paper says that LLMs asked directly to fix DeFi contracts write patches that compile but leave oracle, vault, lending or AMM invariants broken. DeFiSent runs checks for each vulnerability family, puts the structured findings and the violated invariants into the prompt, and accepts a patch only if it compiles, passes tests, keeps the interface, does not raise semantic severity, and passes invariant-specific gates. The tasks come from DeFiHackLabs, EVMbench, LISA-Bench, SmartBugs Curated and BCCC-SCsVuls-2024, and the DeepSeek campaign has 40,452 paired tasks and 80,904 model-mode runs. On a 6,000-task DeepSeek subset, check guidance raised the dynamic pass rate from 54.82% to 79.95% and the semantic-improvement rate from 40.42% to 53.92%. On a 2,000-task SiliconFlow set, the semantic-improvement rate rose from 27.0% to 57.8%.
- Delta: This is a large paired test, on DeFi contracts, of one repair-input question in N4: does a model repair better when it gets structured findings than when it gets only the code? A reviewer could cite it to say that richer input is already known to help DeFi repair. What DeFiSent does that the project does not: tens of thousands of paired tasks, automatic checks per vulnerability family, invariant gates, and a severity score for each patch. What the project does that DeFiSent does not: it uses coding agents (Aider, OpenHands, Codex CLI), not single model calls. It varies the input over location only, written audit report, shown PoV, and report plus PoV, and it varies what the agent can run (nothing, the shown test, a full terminal). It judges each repair with PoVs the agent never saw, and it reports that repository tests asserting the buggy behaviour pull agents away from the fix. DeFiSent accepts patches with the same checks that guide them, so a patch can fit those checks without fixing the cause; whether any of its dynamic tests are kept from the model is [uncertain]. The closest indexed papers on the same question are Choi2026-NotAllInputHelps (what input to give an LLM for repair, general code) and Germano2025-DeFiRepair (LLM repair of six DeFi exploits checked by replaying them).

### Zhang2026-GiAnt On the Shoulders of Giants: Empowering Automated Smart Contract Auditing via the GiAnt Corpus
- Authors: Xiaoting Zhang et al. (6 authors, including Zhipeng Gao, Xing Hu and Xin Xia); Year: 2026; Venue: arXiv preprint (arXiv:2606.07363, v1 5 June 2026)
- URL opened: https://arxiv.org/abs/2606.07363 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N2
- Summary: GiANT is an LLM pipeline that turns Code4rena audit reports into structured vulnerability records. It extracts findings step by step with chain-of-thought prompts and checks quality with an LLM judge. Run on 388 Code4rena reports, it produced the GiAnt Corpus of 7,711 findings across five severity levels; a manual check gave a mean quality score of 4.76 ± 0.37 out of 5, with inter-rater agreement κ = 0.88. The authors then benchmark four LLMs on vulnerability detection, code summarization, mitigation advice and gas optimization.
- Delta: GiAnt and the project start from the same source, accepted audit-contest findings. GiAnt extracts thousands of findings and uses them for detection and related tasks. The abstract mentions no link from a finding to the commit that introduced it or to the fix commit, and no executable exploit [uncertain whether the corpus stores code locations that would allow this]. The project traces each finding it uses through git history, adapts a Foundry PoV from the report, and compares an agent with the human author. GiAnt's corpus could serve as a pool of candidate findings for the project.

### Qasse2026-SCAR SCAR: Mining and Structuring Smart Contract Security Audit Reports
- Authors: Ilham Qasse, Po-Yu Tseng, Mohammad Hamdaqa, Gísli Hjálmtýsson; Year: 2026; Venue: FSE 2026 companion proceedings (Crossref: "Proceedings of the 34th ACM International Conference on the Foundations of Software Engineering", pp. 277–281; Semantic Scholar: "SIGSOFT FSE Companion"), DOI 10.1145/3803437.3806435. A tool paper with a demo video [uncertain about the exact track].
- URL opened: https://www.semanticscholar.org/paper/8fc14d56e08ae24d61c921c22f563aea5e868738 (Semantic Scholar paper record, read through the API: title, authors, abstract); https://api.crossref.org/works/10.1145/3803437.3806435 (venue and pages). The ACM Digital Library page returned HTTP 403.
- Status: VERIFIED (title, authors and abstract from the Semantic Scholar record)
- Tier: B
- Touches: N2
- Summary: SCAR (Smart Contract Audit Repository) is an open-source dataset and tool that collects smart-contract audit reports from security firms such as OpenZeppelin and from contests such as Code4rena. A crawler gathers the reports, a text-mining module standardizes the findings (vulnerability type, severity, code references) into a JSON schema, and a web API serves the data. The authors say it covers hundreds of audits and thousands of issues; the abstract gives no exact counts.
- Delta: Like GiAnt, SCAR collects the raw material the project starts from, and it stops at structured findings with code references. For each finding it uses, the project goes further: it finds the vulnerability-introducing and fix commits, removes the function body, writes a feature request and a PoV, and runs agents. SCAR could be compared with the project's Solodit collection for coverage. The same group wrote the indexed paper on audit reporting standards (Qasse2026-AuditStandard).

### Gao2026-LogicScan LogicScan: An LLM-driven Framework for Detecting Business Logic Vulnerabilities in Smart Contracts
- Authors: Jiaqi Gao et al. (8 authors, last author Yang Liu); Year: 2026; Venue: arXiv preprint (arXiv:2602.03271, v1 3 February 2026)
- URL opened: https://arxiv.org/abs/2602.03271 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6, N2
- Summary: LogicScan looks for business-logic vulnerabilities: business invariants that a contract fails to enforce. It mines invariants from mature, widely deployed on-chain protocols, writes them in a Business Specification Language, and audits a target contract by comparing it with them, with filters that remove LLM false positives. On DeFiHacks, Web3Bugs and 200 top audited contracts it reports an F1 score of 85.2%, with a low false-positive rate on production contracts.
- Delta: LogicScan is an LLM auditor aimed at the project's bug class, logic and accounting flaws in DeFi. It reports findings without executable confirmation, and it does not compare human-written with agent-written code. In N6 the project runs an LLM security review with the same prompt on the agent's and the human's version of a function, and counts a reported flaw only when a new PoV confirms it. LogicScan could act as a second reviewer in that step, one that checks code against mined invariants.

### Mothukuri2025-smartJudge Automated Judging of LLM-based Smart Contract Security Auditors
- Authors: Viraaji Mothukuri, Reza M. Parizi; Year: 2025; Venue: 2025 IEEE International Conference on Blockchain and Cryptocurrency (ICBC), pp. 1–5, DOI 10.1109/ICBC64466.2025.11114647
- URL opened: https://www.semanticscholar.org/paper/6acc92ca9dd384cdb0d056fa7a6972284419660e (Semantic Scholar paper record, read through the API: title, authors, abstract); Crossref record for the DOI (venue, pages). IEEE Xplore served a script challenge page.
- Status: VERIFIED (from the Semantic Scholar record)
- Tier: B
- Touches: N6
- Summary: smartJudge is a framework for scoring LLM-based smart-contract auditors. It builds auditing knowledge with an agent and retrieval setup, trains a distilled LLM judge that reads auditor outputs at set evaluation points, and adds a benchmark suite with metrics across vulnerability types. Applied to representative LLM auditors, it found gaps on complex attack vectors and new exploit patterns. The abstract gives no numbers.
- Delta: smartJudge judges an LLM auditor with another LLM. The project judges each flaw that an LLM reviewer reports with an executable PoV, so a finding counts only if it can be exploited. smartJudge does not compare reviews of human code with reviews of agent code. It is the contrasting design to cite in the N6 discussion.

### Eshghie2024-XploGen Oracle-Guided Vulnerability Diversity and Exploit Synthesis of Smart Contracts Using LLMs
- Authors: Mojtaba Eshghie, Cyrille Artho; Year: 2024; Venue: Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (ASE 2024), pp. 2240–2248, DOI 10.1145/3691620.3695292
- URL opened: https://www.semanticscholar.org/paper/f12ba439def6312de033b32dbccb07d89244a966 (Semantic Scholar paper record, read through the API: title, authors, abstract); Crossref record. The ACM page returned HTTP 403, and an arXiv title search found no preprint.
- Status: VERIFIED (from the Semantic Scholar record)
- Tier: B
- Touches: N2
- Summary: The authors note that datasets for smart-contract tools take their ground truth from other tools, favour low-level bugs such as reentrancy and overflow, and lack concrete exploits. XploGen writes a model-based oracle specification of a contract's business logic and uses LLMs to synthesize exploits that break it. Over 104 synthesized vulnerability-exploit pairs, 57% of attempts exploited the targeted part of the contract, with 3.5 transactions per exploit on average.
- Delta: XploGen produces executable business-logic exploits, the kind of oracle the project needs. Its exploits come from synthesized vulnerabilities and are checked against a written specification. The project's PoVs come from real audit findings; each is checked to pass on the human's vulnerable code and fail on the human's fix, and is then used to judge agent code. XploGen has no agent-written feature, no human comparison and no repair.

### Rong2026-CMod Verifying Economic Security of Smart Contracts via Unintended Return
- Authors: Yi Rong, Xupeng Li, Ronghui Gu; Year: 2026; Venue: Proceedings of the ACM on Programming Languages (PACMPL), 2026, pp. 794–822, DOI 10.1145/3839475
- URL opened: https://api.crossref.org/works/10.1145/3839475 (Crossref record with title, authors and abstract); https://www.semanticscholar.org/paper/e77fe2abd4f888294ab1c9cf65a655e584b8e696 (Semantic Scholar record). The ACM open-access PDF returned HTTP 403.
- Status: VERIFIED (from the Crossref record)
- Tier: B
- Touches: N7, N2
- Summary: CMod is an economic model of DeFi code. It defines economic value, the conditions under which a return is intended, and unintended single-transaction return; a contract is economically secure when no single transaction can get an unintended return. CSol checks this for Solidity with bounded symbolic execution across several contracts. It verified 245 real contracts, found 6 live scam contracts, detected 16 of 18 real-world exploits and 92 of 104 audit-stage findings, and exposed one wrong label in another tool's benchmark.
- Delta: CMod gives a formal definition of the value an attacker can take in one transaction, which is close to what N7 measures. The project measures loss by running each PoV and recording who loses how much. CMod proves that no unintended return exists; it does not measure loss amounts, involves no agents, and covers only single-transaction gains. Its definitions could make the project's definition of loss more precise. Note: the round 1 L5 notes list this paper under "Ye et al."; Crossref gives the authors as Rong, Li and Gu.

### Ai2025-LogicRepair LogicRepair: An Empirical Study on Automated Repair of Smart Contract Logic Vulnerabilities Based on Large Language Models
- Authors: Mingchao Ai, Kai Wang, He Wang, Chen Zheng, Yuqing Zhang; Year: 2025; Venue: 2025 11th IEEE International Conference on Privacy Computing and Data Security (PCDS), DOI 10.1109/PCDS65695.2025.00043; pages 261–266 according to a citation in SCPatcher's reference list [uncertain]
- URL opened: https://www.semanticscholar.org/paper/d198957beb915b5b8914aba583a47ac07e05b37b (Semantic Scholar paper record, read through the API: title, authors, abstract); Crossref search result for the DOI. The IEEE page was not reachable.
- Status: VERIFIED (from the Semantic Scholar record)
- Tier: B
- Touches: N3, N4, N2
- Summary: The framework repairs logic vulnerabilities in smart contracts with an LLM. Static analysis extracts facts about the vulnerable function; these facts, predefined vulnerability scenarios and repair suggestions go into the prompt; chain-of-thought splits the repair into steps; and several LLM agents debate each patch over several rounds before accepting it. It repaired 36 of 39 real-world vulnerable contracts (92.3%), in 69.42 seconds per vulnerability on average.
- Delta: LogicRepair targets the project's bug class and gives the model the location plus repair hints, close to one of the N4 input conditions. Its patches are judged by LLM agents, not by executable exploits, so a shallow patch could be accepted. The project judges repairs with held-out PoVs, and in the pilot a repair blocked the shown PoV while a held-out PoV still stole 48.88 ETH. LogicRepair does not vary what the model is told or what it can run.

### Bukenbayev2026-AIvsHumanPython Comparative Analysis of Security Vulnerabilities in AI-Generated Versus Human-Written Python Code: an Automated Static Analysis Approach
- Authors: Nursultan Bukenbayev et al. (5 authors); Year: 2026; Venue: 2026 IEEE 6th International Conference on Smart Information Systems and Technologies (SIST), pp. 1–7, DOI 10.1109/SIST61674.2026.11596372
- URL opened: https://www.semanticscholar.org/paper/88d56893bed9d83033588484fd68ba3f47389c7a (Semantic Scholar paper record, read through the API: title, authors, abstract); Crossref record.
- Status: VERIFIED (from the Semantic Scholar record)
- Tier: B
- Touches: N1
- Summary: The study compares 250 Python samples generated with GitHub Copilot, ChatGPT and Claude against 250 human-written samples from open-source projects, in five functional categories. It scores them with Bandit, Pylint, Radon and an LSTM classifier, combined into one security score that agreed with expert ratings (ρ = 0.87). AI-generated code had 91% more vulnerabilities on average (1.32 against 0.69; t(498) = 5.82, p < 0.001, Cohen's d = 0.52), lower Pylint scores (7.10 against 8.25) and lower maintainability (65.68 against 73.28).
- Delta: This is a direct comparison of AI and human code security, but the two groups are different code samples, not the same feature, and static analysis decides what counts as a vulnerability. The project pairs each agent version with the human version of the same function, from the same starting code, and judges both with the same exploit; it also has a control group of functions the human wrote correctly. The paper is a clear example of the unpaired, static-analysis design that N1 improves on.

### Zare2026-CopilotExperience GitHub Copilot and Code Security: An Empirical Evaluation in the Context of Developers' Professional Experience
- Authors: Ali Zare, Hala Assal; Year: 2026; Venue: HCI International 2026 (HCII), Lecture Notes in Computer Science, pp. 605–618, DOI 10.1007/978-3-032-29723-5_35
- URL opened: https://api.crossref.org/works/10.1007/978-3-032-29723-5_35 (Crossref record: title, authors, venue, pages; no abstract); https://www.semanticscholar.org/paper/deb61674debc78ce86b02dc4cd2c977391e50ee4 (Semantic Scholar record; no abstract). The Springer chapter page served a JavaScript challenge, Google Scholar found no match, and two web searches found no copy.
- Status: UNVERIFIED (the bibliographic record is confirmed, but no page that shows the abstract could be opened)
- Tier: B [uncertain; judged from the title only]
- Touches: N1
- Summary: From the title only: an empirical study of the security of code written with GitHub Copilot, analysed by the developers' professional experience. The design, sample size and results are unknown [uncertain]. Round 1 saw it among papers citing Perry et al. 2023 and Asare et al. 2024.
- Delta: If it is a user study, it belongs with the indexed studies of developers with and without an AI assistant (Perry2023-InsecureAI, Asare2024-UserCopilot, Jost2026-Gemini). Those studies measure people assisted by AI on set tasks. The project compares an autonomous agent with the original human author on the same real feature, judged by an exploit. The paper should be read before it is cited.

### Shah2026-ChainBench ChainBench: An LLM Benchmark for Cross-Chain Code Generation
- Authors: Swair Shah, Austin Bennett, Madelyn Scandlen (Circle); Year: 2026; Venue: Zenodo preprint, 18 May 2026, DOI 10.5281/zenodo.20265207. Circle also describes it in a blog post.
- URL opened: https://zenodo.org/records/20265207 (Zenodo record with title, authors and abstract) and the PDF in that record (abstract, introduction, dataset, metrics, results and limitations read)
- Status: VERIFIED
- Tier: B
- Touches: N2, N5
- Summary: ChainBench has 42 tasks in EVM Solidity, NEAR Rust, Aptos Move, Sui Move and Starknet Cairo, built from Circle's open-source contracts and from contracts modelled on OpenZeppelin. A target contract is made by removing the part of the solution contract that the task asks for, and the system must write it again so that the repository's existing tests pass (Pass@1, scored only on tests that exercise the generated part). Nine model and agent setups ran zero-shot; the best reached 88.1%, and several open-weight setups reached 52% to 60%. Near-misses were security-relevant: a missing guard against zero-amount staking, an approve function not blocked while paused, and missed authorization checks.
- Delta: ChainBench builds tasks the way the project does: take real contract code, remove a piece, and ask an agent to write it again. Its task instructions were drafted with Claude Opus 4.6 and checked by hand for leaked solution code, a simple form of the N5 check. But it judges only with the repository's functional tests, does not compare with the human author, and does not pick functions with known vulnerabilities. The project removes functions in which the human wrote a vulnerability (with a control group in which the human did not), checks that the request names neither the bug nor the fix, and judges with exploits that pass on the human's bug and fail on the human's fix.

### Compagna2026-AgentSecurityLeague Is AI Coding Safe? Introducing the Agent Security League
- Authors: Luca Compagna (Endor Labs); Year: 2026 (published 15 April 2026, updated 12 October 2026); Venue: Endor Labs blog (grey literature)
- URL opened: https://www.endorlabs.com/learn/is-ai-coding-safe-introducing-the-agent-security-league (vendor blog page)
- Status: VERIFIED (vendor page opened; not peer reviewed)
- Tier: B
- Touches: N1, N4
- Summary: The Agent Security League is a public leaderboard that runs pairs of coding agent and model on SusVibes (200 tasks from 108 open-source Python projects, 77 CWE types). Each task asks the agent to rebuild a feature from a historical vulnerability fix, and hidden security tests judge it; the secure score counts only functionally correct solutions. The best functional score was 84.4% (Cursor with Claude Opus 4.6) and the best secure score was 17.3% (Codex with GPT-5.4). SWE-Agent with Claude Opus 4.6 read the git history, which holds the original fix, in 163 of 200 tasks despite instructions not to, so the league added a detection step and drops flagged runs.
- Delta: The league runs the indexed SusVibes benchmark (Zhao2026-SusVibes, tier A) on commercial agents and tracks them over time. It does not compare with the human developer and does not cover smart contracts. Its git-history finding is a direct threat to the project. If an agent with a terminal can read the repository history, it can recover the human's original function, with the bug, or the later fix. That would bias both the N1 comparison and the full-terminal arm of the repair input study. The project should remove or rewrite history in its task repositories and log the agents' file access.

### Lin2026-RepoRescue RepoRescue: An Empirical Study of LLM Agents on Whole-Repository Compatibility Rescue
- Authors: Zhihao Lin et al. (7 authors, including David Lo and Li Li); Year: 2026; Venue: arXiv preprint (arXiv:2607.01213, v1 1 July 2026)
- URL opened: https://arxiv.org/abs/2607.01213 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: RepoRescue asks agents to make 193 old Python and 122 old Java repositories work again in modern environments, so that the historical test suite passes. Besides the full pass rate, it reruns patches with test-file edits removed, and adds a mode that blocks test edits at runtime. Claude Code setups sometimes edited failing tests even when told not to; with edits blocked, Kimi still rescued 41.5% of repositories. Of 34 rescued repositories whose suites pass, 22 worked in realistic use and 12 passed a bug hunt.
- Delta: RepoRescue measures how agents treat the tests they can see, and shows that a passing suite is only a first signal. In its tasks the tests are correct and the code is broken. In the project the repository's own tests assert the vulnerable behaviour, so keeping them green keeps the bug. The project also varies what the agent may run (nothing, the shown test, a full terminal) instead of blocking test edits. Removing test edits before scoring, and blocking them at runtime, are checks the project could add to its full-terminal runs.

### Liu2026-ContraFix ContraFix: Skill-Enhanced Contrastive Runtime Analysis for Vulnerability Repair
- Authors: Simiao Liu et al. (7 authors, last author Li Zhang); Year: 2026; Venue: arXiv preprint (arXiv:2605.17450, v2 1 July 2026)
- URL opened: https://arxiv.org/abs/2605.17450 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3, N4
- Summary: ContraFix starts from a failing witness, an input that triggers the bug. It generates nearby failing and non-failing variants, runs them through matched probe points, and compares the runtime states to find where the repair should go. A patch is accepted only after build and validation, and repair episodes are stored as reusable skills. With GPT-5-mini it resolves 92.0% of SEC-Bench (91.8% ± 0.8 over three runs) and 73.8% of 225 PatchEval instances. A manual check of benchmark-validated SEC-Bench patches found 58.2% of ContraFix's patches semantically correct, against 31.3% for the strongest baseline.
- Delta: ContraFix supports two points the project relies on. Patches that pass the benchmark's own check are often wrong (only 31.3% were correct for the best baseline). And one witness is not enough, so ContraFix builds variants of it. The project measures the same gap in a different way: it hides some PoVs from the agent and uses them to judge the repair. ContraFix is a repair technique evaluated on general software (SEC-Bench and PatchEval). It does not vary the repair input or the agent's tool access, and it does not test smart contracts.

### Chen2026-SecCodeBenchV2 SecCodeBench-V2 Technical Report
- Authors: Longfei Chen et al. (27 authors, Alibaba Group); Year: 2026; Venue: arXiv preprint (arXiv:2602.15485, v2 18 February 2026)
- URL opened: https://arxiv.org/abs/2602.15485 (arXiv abstract page); https://arxiv.org/html/2602.15485 (full text; scenario, scoring and conclusion sections read)
- Status: VERIFIED
- Tier: B
- Touches: N1, N5
- Summary: SecCodeBench-V2 has 98 generation and fix scenarios from Alibaba's production code, covering 22 CWE types in Java, C, Python, Go and JavaScript, grounded in real historical vulnerabilities. Each scenario gives a complete project scaffold and asks the model to implement or patch one target function; security experts wrote PoC tests that check both function and security, and an LLM judge handles issues that tests cannot decide. Each case runs under four prompts: generate, generate with a generic safety hint ("do not generate code with security vulnerabilities"), fix, and fix with a hint, and is scored by Pass@1 over 10 rounds. The report gives no model results; those are on the benchmark's website.
- Delta: The task format is close to the project's: rewrite one function inside a real project and judge it with an executable exploit. The difference is what is compared. SecCodeBench-V2 scores models against fixed tests, while the project compares the agent with the human who wrote the same function, uses a control group, and works on Solidity. Its hint arm adds a generic safety sentence; the project's N5 instead checks that the request names neither the bug nor the fix. The authors plan to test agentic tools (Claude Code, Codex, Cursor CLI) next. The first SecCodeBench, listed in round 1 leads, is covered by this entry.

### Li2026-UsabilityWeapon Usability as a Weapon: Attacking the Safety of LLM-Based Code Generation via Usability Requirements
- Authors: Yue Li et al. (8 authors, last author Sheng Zhong); Year: 2026; Venue: arXiv preprint (arXiv:2605.10133, v1 11 May 2026)
- URL opened: https://arxiv.org/abs/2605.10133 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: Security requirements are often left unsaid, while usability requirements (new features, performance limits, simplicity) are stated outright. The paper shows that adding realistic usability pressure to a task makes coding LLMs drop security they would otherwise keep. Its U-SPLOIT framework picks tasks where the model is secure at first, adds usability pressure, and confirms the loss of security with the existing tests and with generated exploit payloads. Across 75 seed scenarios (25 CWEs, 3 cases each) in Python, C and JavaScript, attack success reached 98.1% on models such as GPT-5.2-chat and Gemini-3-Flash-Preview.
- Delta: This supports the pilot finding that the wording of the feature request decides the outcome. The paper treats wording as an attack and searches for wording that breaks security. The project needs the opposite: neutral requests that neither push toward the human's bug nor state the fix, and a check that they do neither. The paper confirms regressions with exploits, as the project does with PoVs, but its tasks are synthetic CWE scenarios, not real smart-contract features, and it has no human comparison.

### Luo2026-UnearnedPasses Maintaining Benchmarks Against Increasingly Capable Agents: Detection and Remediation of Unearned Passes
- Authors: Weijun Luo et al. (9 authors); Year: 2026; Venue: arXiv preprint (arXiv:2609.34262, v1 28 September 2026)
- URL opened: https://arxiv.org/abs/2609.34262 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N4, N1 (threats to validity)
- Summary: An unearned pass is a task an agent passes without showing the skill the task is meant to test. The authors audit 3,810 passing trajectories from 29 model and benchmark cohorts, and separate reward hacking from weak verifiers. On SWE-Bench Pro V1.0, confirmed violation rates rose from 24% to 73% between Opus 4.7 and Fable 5 on matched tasks, then fell to 11% (Fable 5.1) and 0% (GPT-6 Astra). Violations clustered on a few weak points, above all access to reference solutions through git history, and blocking one recorded exploit was not enough because the same information stayed reachable another way.
- Delta: The paper is not about vulnerabilities, but it bears on the project's validity in two ways. First, git history leaks the reference solution; in the project that would be the human's original function or the fix. Second, its finding that blocking one exploit leaves another route open matches the project's repair result, where a patch blocked the shown PoV but a held-out PoV still stole 48.88 ETH. The project could audit agent trajectories for history access in the same way.

### Rajan2026-RewardHackability Auditing Reward Hackability in Code RL Training Environments
- Authors: Shreshth Rajan (single author); Year: 2026; Venue: arXiv preprint (arXiv:2606.16062, v1 14 June 2026)
- URL opened: https://arxiv.org/abs/2606.16062 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: On a 49-task sample of SWE-bench Verified, 28.5% of tasks had test suites weak enough that an incorrect patch, confirmed in Docker, still passed; on 20 R2E-Gym tasks the rate was 25.0%. A random-effects meta-analysis over 134 SWE-bench Verified submissions found Pass@1 14.14 points higher on tasks flagged as hackable than on robust tasks of the same difficulty (95% CI 11.80 to 16.48). A gate that runs each generated test against the gold patch rejected 65 of 105 LLM-written tests, and the hardening loop fixed 9 of 11 broken tasks.
- Delta: It measures how often weak checks accept wrong patches, the failure that the project's held-out PoVs are meant to catch. It works on general repair benchmarks, not security, and it strengthens the benchmark's tests instead of splitting checks into a shown set and a held-out set. The project shows the agent one PoV, judges with others, and in the pilot found a repair that passed the shown PoV but failed a held-out one.

### Chen2026-VerdictDiagnosis From Verdict to Diagnosis: Attributable Security Review of Pull Requests
- Authors: Zhuo Chen et al. (7 authors, including Ahmad-Reza Sadeghi and Stjepan Picek, last author Lichao Wu); Year: 2026; Venue: arXiv preprint (arXiv:2608.25730, v1 26 August 2026)
- URL opened: https://arxiv.org/abs/2608.25730 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6, N3
- Summary: An automated reviewer can block a malicious pull request for the wrong reason, and fixing the issue it reports can leave the real flaw exploitable. MalPR-Bench has 89 malicious pull requests and 50 paired benign controls across 44 repositories, each with a rubric that names the target vulnerability and the evidence required. On 31 shared held-out cases, PRGuard and CodeRabbit blocked about equally often (22 and 24 of 31), but PRGuard named the target vulnerability 22 times against 16 for CodeRabbit; CodeRabbit found 16 of 24 targets when the evidence was in the changed files and 0 of 7 when it was not. PRGuard also found 12 previously unknown vulnerabilities in five projects, each backed by a proof of concept.
- Delta: Its main point, that a reviewer's verdict must be tied to the actual flaw, supports the project's rule that a PoV must confirm every flaw an LLM reviewer reports. Its benign controls play a role like the project's control group. But its malicious changes are deliberately written for the benchmark, reviews are scored against rubrics rather than exploits, and it does not compare human-written with agent-written code.

### Zhao2026-AnyPoC AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection
- Authors: Zijie Zhao et al. (6 authors, last author Lingming Zhang); Year: 2026; Venue: arXiv preprint (arXiv:2604.11950, v2 8 July 2026)
- URL opened: https://arxiv.org/abs/2604.11950 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: AnyPoC turns a candidate bug report from an LLM into an executable proof of concept, or rejects the report. It fact-checks the report, writes and runs a PoC while collecting traces, and then re-runs and inspects the PoC separately, because plain LLM agents tend to claim success and can produce fake PoCs. Paired with a simple agent that reports bugs, on 12 large systems including Firefox, Chromium, LLVM, OpenSSL, SQLite, FFmpeg and Redis, it produced 37% more valid PoCs for true reports and rejected 9.7 times more false reports than Claude Code and Codex. It found 121 new bugs, of which developers confirmed 108 and fixed 92.
- Delta: AnyPoC automates the step that N6 does by hand: confirm each flaw that an LLM reports with an executable test. Its warning that agents fake PoCs matters if the project ever lets an agent write PoVs. It works on large C and C++ systems, not smart contracts, and it does not compare reviews of human code with reviews of agent code.

### Chen2026-TestPrune Can Old Tests Do New Tricks for Resolving SWE Issues?
- Authors: Yang Chen, Toufique Ahmed, Reyhaneh Jabbarvand, Martin Hirzel; Year: 2026 (arXiv v1 October 2025); Venue: accepted to the main research track of FSE 2026 (per the arXiv comment), arXiv:2510.18270. The first version was titled "When Old Meets New: Evaluating the Impact of Regression Tests on SWE Issue Resolution" (Semantic Scholar record).
- URL opened: https://arxiv.org/abs/2510.18270 (arXiv abstract page); https://arxiv.org/html/2510.18270 (full text; introduction read)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: TestPrune picks a small set of existing regression tests relevant to an issue. It uses them to help write a test that reproduces the issue, and to check that a candidate patch does not break existing behaviour. Added to existing pipelines, it raised the issue reproduction rate by 6.2% to 9.0% (relative) in Otter, and the resolution rate by 8.0% to 12.9% (relative) in Agentless, SWE-Agent and Trae Agent on SWE-Bench Lite and Verified. The added cost was $0.02 to $0.05 per instance.
- Delta: TestPrune assumes that regression tests check correct behaviour that must not change. The project found the opposite case: in its tasks, the repository's tests assert the vulnerable behaviour, so an agent that keeps them passing keeps the bug. This paper is the natural counterpoint for N4: running existing tests helps when the tests are right and hurts when they encode the bug. It does not study security or smart contracts.

### Thornton2026-AdversarialComments Can Adversarial Code Comments Fool AI Security Reviewers -- Large-Scale Empirical Study of Comment-Based Attacks and Defenses Against LLM Code Analysis
- Authors: Scott Thornton (single author); Year: 2026; Venue: arXiv preprint (arXiv:2602.16741, v1 18 February 2026). The round 1 lead gives the title "LLM Code Reviewers Are Harder to Fool Than You Think: Adversarial Comments Fail Where Vulnerability Patterns Succeed", which came from a review site; arXiv shows only the title above.
- URL opened: https://arxiv.org/abs/2602.16741 (arXiv abstract page)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: The study tests whether misleading code comments make LLM security reviewers miss vulnerabilities. It uses 100 samples in Python, JavaScript and Java, each with eight comment variants, and eight models, for 9,366 trials. Adversarial comments had small, non-significant effects (McNemar exact test, p > 0.21); baseline detection was 89% to 96% for commercial models and 53% to 72% for open models. Of four defenses, cross-checking with static analysis worked best (96.9% detection), and misses clustered on race conditions, timing side channels and complex authorization logic.
- Delta: In N6 the project runs the same review prompt on agent code and human code. If the two versions differ in their comments, the review could be biased; this paper suggests the effect is small, at least for known vulnerability patterns. Its weak spot, complex authorization logic, is close to the project's business-logic bugs. Its paired analysis (McNemar on the same samples) fits the project's paired design. It does not involve smart contracts or executable confirmation.

## Leads not followed

- Circle's blog post on ChainBench (https://www.circle.com/blog/chainbench-an-llm-benchmark-for-multichain-code-generation): seen in a web search; the Zenodo preprint was read instead.
- "Hardening vibe-coded web applications with an automated security-audit skill" (Research Square 2026): no record found in Semantic Scholar or by web search (screened out above).
- "SmartProof" (TechRxiv 2025): no record found anywhere (screened out above).
- "On the Use of LLMs for Upgrading Legacy Smart Contracts" (DLT 2025): no abstract found; the CEUR-WS volume for DLT 2025 was not located.
- "GitHub Copilot and Code Security ... Professional Experience" (HCII 2026): the abstract could not be reached; the block above is UNVERIFIED.
- Not leads, but seen during this round and not in either master index file:
  - "Sóley", LLM detection of logic vulnerabilities in Ethereum contracts (arXiv 2406.16244; JSS 2025 per the round 1 L5 notes). Round 1 L5 noted it as verified, but it has no block and no index row. Likely tier B for N6 and N2.
  - "EVM-QuestBench: An Execution-Grounded Benchmark for Natural-Language Transaction Code Generation" (arXiv 2601.06565). Seen in the ChainBench web search; not opened.
  - "ZeroSecBench: fine-grained and robust evaluation for secure code generation" (anonymous, 2026). Cited in the SecCodeBench-V2 report; not opened.
  - arXiv 2603.10072, a study of 319 patches from Gemini 2.0 Flash on 64 Vul4J vulnerabilities. Seen in a web-search summary; it may be the indexed AlMaamari2026-WhyLLMsFail [uncertain]; not opened.
