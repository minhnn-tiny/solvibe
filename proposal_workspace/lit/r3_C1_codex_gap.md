# Derived copy of codex_raw/p0_lit_codex_gap.md (Codex gap search, round 3), field names normalised for the index. The raw file is the record.

## Queries run

All included titles were checked against the full index after removing case, punctuation, and whitespace. **15 new papers were verified.** “Verified” means the source was retrieved, not that its results were independently reproduced.

Counts marked **[uncertain]** reflect merged search results whose per-query screening counts were not retained. New-paper counts credit the discovery query, not later verification searches.

| Query | Source | Hits looked at | New relevant papers |
|---|---|---:|---:|
| `"AI-generated" "human-written" security commits benchmark` | Web search | [uncertain] | 1 |
| `Solidity LLM "audit contest" benchmark exploit` | Web search | [uncertain] | 0 |
| `program repair "buggy behavior" tests overfitting` | Web search | [uncertain] | 2 |
| `"Solidity" "LLM" "audit" benchmark arxiv 2026` | Web search | 25 | 5 |
| `"agent" "security" "human" "commits" benchmark regeneration` | Web search | [uncertain] | 0 |
| `"vulnerability repair" "exploit" "held-out" tests` | Web search | [uncertain] | 0 |
| `"program repair" "tests" "buggy behaviour"` | Web search | [uncertain] | 1 |
| `"Benchmarking LLM-Based Static Analysis for Secure Smart Contract Development"` | Web search; metadata verification | [uncertain] | 0 |
| `"Test Case Generation for Program Repair: A Study of Feasibility and Effectiveness"` | Web search; reference follow-up | [uncertain] | 1 |
| `"Test-based patch clustering for automatically-generated patches assessment"` | Web search; metadata verification | [uncertain] | 0 |
| `"No More Hidden Pitfalls?" "2025"` | Web search; metadata verification | [uncertain] | 0 |
| `"smart contract" "exploit generation" "LLM" "Code4rena"` | Web search | [uncertain] | 0 |
| `"AI-authored" "commits" "security" study` | Web search | [uncertain] | 0 |
| `"repair" "test execution" "LLM" information ablation` | Web search | [uncertain] | 2 |
| `"Automatic Generation of Test Cases based on Bug Reports" Plein venue` | Web search; publication verification | [uncertain] | 0 |
| `smart contract exploit generation LLM Code4rena benchmark` | Web search | 25 | 3 |
| `"Advanced Smart Contract Vulnerability Detection via LLM-Powered Multi-Agent Systems"` | Web search; publication verification | [uncertain] | 0 |
| `"SmartAuditFlow: A Dynamic Plan-Execute Framework"` | Web search; publication verification | [uncertain] | 0 |
| `Bastet Fine-Grained Expert-Labeled` | Semantic Scholar API through web tool | 0; inaccessible | 0 |

### Talha2026-SNRA To Vibe or Not to Vibe: An Empirical Security Analysis of AI-Generated Code Patches

- **Authors:** Muhammad Talha and Vishwaa Shah; **Year:** 2026; Venue: Unpublished research/course manuscript, targeting publication.
- **URL opened:** [Author’s paper page](https://www.tjbravo.com/research/to-vibe-or-not-to-vibe) and [PDF](https://www.tjbravo.com/papers/to-vibe-or-not-to-vibe.pdf).
- Status: VERIFIED
- Tier: A
- **Touches:** N1.
- **Summary:** SNRA compares the original repository, human fix, and AI patch for the same SWE-bench Pro bugs using differential CodeQL findings. It reports net finding reductions of +15 for human patches, −53 for Claude 4.5, and −114 for GPT-5. Sample size is **[uncertain]**: Table 1 and the webpage give 139 commits, while the PDF introduction says 569.
- **Delta:** Provides a closely matched human–AI comparison for bug-fix tasks and severity-weighted static findings. Your project instead compares feature implementations using executable exploits, includes human-correct controls, and measures Solidity losses.

### Hsu2026-Bastet Bastet: A Fine-Grained Expert-Labeled Dataset for DeFi Smart Contract Vulnerability Detection

- **Authors:** Wan-Hsuan Hsu et al.; **Year:** 2026; Venue: arXiv preprint.
- **URL opened:** [arXiv abstract](https://arxiv.org/abs/2606.03387).
- Status: VERIFIED
- Tier: B
- **Touches:** N2, N6.
- **Summary:** Bastet collects 4,402 findings from 394 Code4rena audit reports dated April 2021–November 2024. White-hat researchers fully annotate 849 findings through a two-annotator consensus workflow, using 46 tags and 77 subtags.
- **Delta:** Supplies expert-labelled audit-contest data and a detailed vulnerability taxonomy. Your project adds introducing-commit reconstruction, matched code generation, executable exploit validation, and repair experiments.

### Khalid2026-AuditTransfer Do Smart Contract Auditing Results Transfer Across Datasets? A Two-Benchmark Empirical Study of Static and LLM-Based Security Tools

- **Authors:** Shawal Khalid et al.; **Year:** 2026; Venue: 20th International Symposium on Empirical Software Engineering and Measurement, confirmed on the publisher page.
- **URL opened:** [Dagstuhl publisher page](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESEM.2026.45).
- Status: VERIFIED
- Tier: B
- **Touches:** N2, N6.
- **Summary:** Evaluates seven auditing tools on 143 SmartBugs Curated contracts and 173 real-world, audit-derived FORGE contracts. It finds over-prediction in both static and LLM-based auditors, alongside reliability problems on real-world contracts.
- **Delta:** Directly examines cross-dataset robustness and normalizes heterogeneous auditor outputs. Your project evaluates human and agent code under matched conditions and requires executable confirmation of newly reported flaws.

### Susan2026-StaticAudit Benchmarking LLM-Based Static Analysis for Secure Smart Contract Development: Reliability, Limitations, and Potential Hybrid Solutions

- **Authors:** Stefan-Claudiu Susan et al.; **Year:** 2026; Venue: IEEE COMPSAC 2026; acceptance stated in the arXiv comments.
- **URL opened:** [arXiv abstract](https://arxiv.org/abs/2605.11163).
- Status: VERIFIED
- Tier: B
- **Touches:** N2, N5, N6.
- **Summary:** Studies whether LLMs can replace or complement conventional smart-contract static analysis. It identifies sensitivity to identifier names and precision–recall trade-offs from prompting; its output-classification framework achieves 92% accuracy, which is distinct from vulnerability-detection accuracy.
- **Delta:** Adds evidence that lexical cues and prompting affect security judgments. Your project investigates feature-request leakage and validates security outcomes through exploits rather than auditor classifications alone.

### Liu2026-LiquiLM LiquiLM: Bridging the Semantic Gap in Liquidity Flaw Audit via DCN and LLMs

- **Authors:** Zekai Liu et al.; **Year:** 2026; Venue: arXiv preprint.
- **URL opened:** [arXiv abstract](https://arxiv.org/abs/2604.03860).
- Status: VERIFIED
- Tier: B
- **Touches:** N2, N6.
- **Summary:** Combines LLMs with a Dynamic Co-Attention Network to connect liquidity-related code with flaw descriptions. On 1,490 validation contracts, both reported backbone configurations exceed 90% F1; a separate audit of 1,380 contracts identifies 238 high-risk contracts and assists discovery of ten CVE-certified vulnerabilities.
- **Delta:** Specializes detection in liquidity and economic logic. Your project evaluates implementation and repair security through executable attacks, including held-out attacks and measured losses.

### Li2025-SCALM No More Hidden Pitfalls? Exposing Smart Contract Bad Practices with LLM-Powered Hybrid Analysis

- **Authors:** Xiaoqi Li et al.; **Year:** 2025, revised 2026; Venue: arXiv preprint; the opened PDF contains publication placeholders.
- **URL opened:** [arXiv abstract](https://arxiv.org/abs/2512.15179) and [author-hosted PDF](https://csxqli.github.io/files/TOSEM25.pdf).
- Status: VERIFIED
- Tier: B
- **Touches:** N2, N6.
- **Summary:** SCALM combines function-level slicing, retrieved patterns, and layered reasoning to detect 35 security-related and 12 quality-related bad practices. Its comparison reports 94.97% F1 for reentrancy detection.
- **Delta:** Covers maintainability and design practices as well as vulnerabilities, using a specialized auditing architecture. Your project focuses on exploitable differences between matched human and agent implementations.

### Peng2026-Synapse Thought Is All You Need: Smart Contract Vulnerability Detection with Thought-Augmented Large Language Model

- **Authors:** Chaoyuan Peng et al.; **Year:** 2026; Venue: Proceedings of the ACM on Software Engineering 3, FSE, Article FSE134; confirmed on the PDF.
- **URL opened:** [Published-paper PDF](https://yajin.org/papers/fse2026_synapse.pdf).
- Status: VERIFIED
- Tier: B
- **Touches:** N2, N6, N7.
- **Summary:** Synapse learns vulnerability-specific reasoning patterns and applies them through focused analysis and verification. The paper reports 117 previously undiscovered vulnerabilities, including a critical finding associated with safeguarding $30 million in assets.
- **Delta:** Contributes a specialized vulnerability-discovery method and real-world impact evidence. Your project studies matched code generation and repair; assets safeguarded are also a different measure from loss demonstrated by each executable exploit.

### Wei2025-LLMSmartAudit Advanced Smart Contract Vulnerability Detection via LLM-Powered Multi-Agent Systems

- **Authors:** Zhiyuan Wei et al.; **Year:** 2025; Venue: IEEE Transactions on Software Engineering 51(10), 2830–2846, confirmed through the institutional publication record.
- **URL opened:** [Author-hosted PDF](https://daoyuan14.github.io/papers/TSE25_LLM-SmartAudit.pdf) and [HKUST publication record](https://researchportal.hkust.edu.hk/en/publications/advanced-smart-contract-vulnerability-detection-via-llm-powered-m/).
- Status: VERIFIED
- Tier: B
- **Touches:** N2, N6.
- **Summary:** LLM-SmartAudit uses specialized conversational agents and a persistent reasoning buffer to refine vulnerability assessments. Across three datasets, it reports 98% accuracy on common vulnerabilities and detection of 12 of 13 CVEs.
- **Delta:** Evaluates a collaborative auditing architecture, including real-world projects. Your project uses security review within a matched authorship experiment and requires executable confirmation of newly discovered flaws.

### Wei2026-SmartAuditFlow SmartAuditFlow: A Dynamic Plan-Execute Framework for Advanced Smart Contract Security Analysis

- **Authors:** Zhiyuan Wei et al.; **Year:** 2026 publication; 2025 manuscript; Venue: ACM Transactions on Software Engineering and Methodology; final volume/issue **[uncertain]**.
- **URL opened:** [Author-hosted PDF](https://zhehou.github.io/papers/SmartAuditFlow-A-Dynamic-Plan-Execute-Framework-for-Advanced-Smart-Contract-Security-Analysis.pdf) and [Crossmark publication record](https://crossmark.crossref.org/dialog?cm_version=v2.0&doi=10.1145%2F3785364&domain=dl.acm.org&uri_scheme=https%3A).
- Status: VERIFIED Crossmark confirms publication in 2026; the manuscript’s bibliographic placeholders were not treated as final metadata.
- Tier: B
- **Touches:** N2, N4, N6.
- **Summary:** Dynamically revises audit plans using intermediate findings, static analyzers, retrieval, and prompt optimization. The manuscript reports 100% accuracy on common-vulnerability benchmarks and identification of 13 additional CVEs missed by existing methods.
- **Delta:** Investigates adaptive tool-supported auditing. Your project varies repair information and execution access, then judges repairs using separate visible and held-out exploits.

### Ruan2024-EvoRepair Evolutionary Testing for Program Repair

- **Authors:** Haifeng Ruan et al.; **Year:** 2024; Venue: 17th IEEE International Conference on Software Testing, Verification and Validation, confirmed on the author’s publication page.
- **URL opened:** [Paper PDF](https://abhikrc.com/pdf/ICST24.pdf) and [author publication page](https://yannicnoller.github.io/publications/).
- Status: VERIFIED
- Tier: A
- **Touches:** N3, N4.
- **Summary:** EvoRepair instruments programs using bug-report-derived oracles and coevolves patches with tests that expose overfitting. Across ten repetitions, it correctly repairs eight of 39 evaluated bugs; ARJA correctly repairs seven.
- **Delta:** Actively generates distinguishing tests during repair and uses explicit report-derived instrumentation. Your project studies LLM agents with fixed information/access treatments and reserves independent PoVs for final evaluation.

### Yang2017-Opad Better Test Cases for Better Automated Program Repair

- **Authors:** Jinqiu Yang et al.; **Year:** 2017; Venue: ESEC/FSE 2017, confirmed on the PDF.
- **URL opened:** [Published-paper PDF](https://www.cs.purdue.edu/homes/lintan/publications/opad-fse17.pdf).
- Status: VERIFIED
- Tier: A
- **Touches:** N3, N4.
- **Summary:** Opad augments repair tests through fuzzing and uses crash and memory-safety oracles to reject overfitted patches. Across 45 bugs in seven systems, it filters 321 of 427 overfitted patches—75.2%—and enables SPR to correctly repair one additional bug.
- **Delta:** Demonstrates concrete patch rejection through additional executable tests and safety oracles. Your project extends this concern to Solidity business logic, masked PoVs, agent access conditions, and financial consequences.

### Martinez2024-xTestCluster Test-based patch clustering for automatically-generated patches assessment

- **Authors:** Matias Martinez et al.; **Year:** 2024; Venue: Empirical Software Engineering 29, Article 116.
- **URL opened:** [Springer publisher page](https://link.springer.com/article/10.1007/s10664-024-10503-2).
- Status: VERIFIED
- Tier: B
- **Touches:** N3.
- **Summary:** Generates additional tests and groups patches according to their execution behavior, exposing differences hidden by the original repair suite. Evaluation of 902 plausible patches from 21 Java repair tools finds a median 50% reduction in patches requiring review.
- **Delta:** Uses new tests to organize human patch assessment rather than directly certify security. Your held-out PoVs provide explicit exploit-based rejection criteria.

### Plein2024-BugReportTests Automatic Generation of Test Cases based on Bug Reports: a Feasibility Study with Large Language Models

- **Authors:** Laura Plein et al.; **Year:** 2024; Venue: Proceedings of the 2024 IEEE/ACM 46th International Conference on Software Engineering: Companion Proceedings, 360–361; confirmed on the author’s publication page.
- **URL opened:** [arXiv abstract](https://arxiv.org/abs/2310.06320) and [author publication page](https://laura-plein.com/publications/).
- Status: VERIFIED
- Tier: B
- **Touches:** N3, N4.
- **Summary:** Uses ChatGPT and fine-tuned CodeGPT to turn natural-language bug reports into executable tests. The preprint reports executable-test generation for up to 50% of Defects4J bugs and demonstrates usefulness for fault localization and patch validation.
- **Delta:** Automates the conversion from reports to executable evidence. Your project compares report and PoV availability directly and keeps additional exploits hidden during repair.

### Wu2026-DebugRepair DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging

- **Authors:** Linhao Wu et al.; **Year:** 2026; Venue: arXiv preprint.
- **URL opened:** [arXiv abstract](https://arxiv.org/abs/2604.19305).
- Status: VERIFIED
- Tier: B
- **Touches:** N4.
- **Summary:** Adds targeted runtime instrumentation, test-context filtering, and conversational debugging to LLM repair. It reports 224 correctly fixed Defects4J bugs with GPT-3.5 and 295 with DeepSeek-V3, with component ablations supporting the usefulness of runtime evidence.
- **Delta:** Studies richer execution feedback and actively collected intermediate states. Your project asks when execution access harms security repair, particularly when repository tests preserve vulnerable behavior.

### Hu2025-RepairR1 Repair-R1: Better Test Before Repair

- **Authors:** Haichuan Hu et al.; **Year:** 2025; Venue: arXiv preprint.
- **URL opened:** [arXiv abstract](https://arxiv.org/abs/2507.22853).
- Status: VERIFIED
- Tier: B
- **Touches:** N3, N4.
- **Summary:** Uses reinforcement learning to train models to generate discriminating tests before producing repairs. Across three backbone models and four benchmarks, the abstract reports repair-success improvements of 2.68%–48.29% over vanilla models.
- **Delta:** Changes model training and repair ordering so tests guide diagnosis. Your project supplies selected exploit tests to existing agents and evaluates generalization to withheld exploits.

## Leads not followed

- **Do Frontier LLMs Truly Understand Smart Contract Vulnerabilities?** — found in the final smart-contract search. The [OpenReview PDF URL](https://openreview.net/pdf?id=qhHtnNnz2n) opened a browser-verification page; authors, publication status, and findings remain unverified.
- **Test Case Generation for Program Repair: A Study of Feasibility and Effectiveness** — found through the repair search. Its relationship to the already-indexed Nopol test-generation paper needs version-level checking; not counted separately.
- **Transferable Self-Evolving Playbooks for Agentic Security Auditing** — found in the commit/security search; full paper not opened.
- **Template-guided interpretable reasoning with execution feedback for LLM-based program repair** — found in the repair-feedback search; publisher page not opened.
- **Enriching automatic test case generation by extracting relevant test inputs from bug reports** — found during Plein publication verification; article not opened.

NEW RELEVANT PAPERS: 15