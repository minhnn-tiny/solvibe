# Round 2, slice S3b: unchecked leads from round 1 (L6, L8 and L9 sections)

Scope: the leads from line 168 to the end of the round 1 lead list (`lit/leads_round1.md`), that is the sections "From lit/r1_L6_pov_guided_repair.md", "From lit/r1_L8_methodology.md" and "From lit/r1_L9_dblp_sweep.md". Priority went to the statistical design and the tracing method. I also searched for capture-recapture, case-control, selection bias and stratified sampling papers in software engineering, including Eick et al. 1992 and Briand et al. 2000 as asked.

Date of search: 2026-10-21. Every API call was anonymous. No email address, name or other contact detail was sent to any service.

How pages were reached. ACM Digital Library returned HTTP 403, IEEE Xplore returned an empty page or a bot check, Springer and SSRN returned a JavaScript challenge or HTTP 403, and DBLP returned a bot check. Where that happened I read the abstract in the Semantic Scholar record or the OpenAlex record of the same DOI, and I say so in the "URL opened" line. Those two records show title, authors and the full abstract. Semantic Scholar title search and OpenAlex title search were rate-limited for most of the session, so title lookups went through Crossref, and abstracts through OpenAlex lookups by DOI.

## Queries run

One row per lead, then the topic sweeps. "New relevant papers" counts blocks added to this file (any tier, including UNVERIFIED). Already-indexed and screened-out leads count 0.

| Query | Source | Hits looked at | New relevant papers |
|---|---|---|---|
| Lead: "Whose Oracle Is It? The Authority Problem in Deployed Agentic Program Repair" | Semantic Scholar batch lookup by DOI | 1 | 1 |
| Lead: "The Oracle Is Mutable: Obedient Destruction of Verification Targets ..." | Crossref title search; WebSearch; neurips.cc page | 3 + 9 + 1 | 1 |
| Lead: "LLM-Based Test Oracles: Source-of-Authority Taxonomy" (arXiv 2607.05031) | arXiv API, id_list batch | 1 | 1 |
| Lead: "TerraProbe" (arXiv 2606.26590) | arXiv API, id_list batch | 1 | 1 |
| Lead: "APR4Vul" (EMSE) | Semantic Scholar batch by DOI | 1 | 1 |
| Lead: Pinconschi et al., ISSRE 2021 | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: "An Empirical Study of APR Techniques for Injection Vulnerabilities" (ICSME 2024) | Crossref title search; OpenAlex by DOI | 3 + 1 | 0 |
| Lead: "Concolic program repair" (PLDI 2021) | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: "The patch overfitting problem in APR: practical magnitude ..." | master index check | 0 | 0 |
| Lead: "Towards Developing Effective Oracles to Reduce Patch Overfitting" (SANER 2025) | Crossref title search; OpenAlex by DOI | 3 + 1 | 0 |
| Lead: Kilgi and Bahsi, ICISSP 2026 | Crossref; OpenAlex by DOI; SciTePress page | 3 + 1 + 1 | 0 |
| Lead: "Evaluating Symbolic Feedback Granularity for LLM-Based Program Repair" (APR 2026) | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: "Catching Developers in the Flow" (ASE 2026) | title screen only | 0 | 0 |
| Lead: "Memorization in LLM-Based Program Repair" (APR 2025) | seen in Crossref results | 1 | 0 |
| Lead: "Heterogeneous Prompting and Execution Feedback for SWE Issue Test Generation" (ICSE 2026) | title screen only | 0 | 0 |
| Lead: "TDD-Bench Verified" (arXiv 2412.02883) | arXiv API, id_list batch | 1 | 0 |
| Lead: OpenAI blog "Introducing SWE-bench Verified" | title screen only | 0 | 0 |
| Lead: METR blog on reward hacking; MacDiarmid et al. 2025 | title screen only | 0 | 0 |
| Lead: AIxCC "AFC Procedures and Scoring Guide Version 2.0" | WebSearch | 9 | 0 |
| Lead: "Agent That Debugs" (arXiv 2504.07634) | arXiv API, id_list batch | 1 | 1 |
| Lead: PatchIsland (2601.17471) | arXiv API, id_list batch | 1 | 0 |
| Lead: EviRepair (2610.13491) | arXiv API, id_list batch | 1 | 0 |
| Lead: AgenticRepair (2607.29422) | arXiv API, id_list batch | 1 | 0 |
| Lead: MemRepair (2605.17444) | arXiv API, id_list batch | 1 | 0 |
| Lead: EvoRepair (2605.30105) | arXiv API, id_list batch | 1 | 0 |
| Lead: ContraFix (2605.17450) | arXiv API, id_list batch | 1 | 0 |
| Lead: Knowledge-Enhanced Agentic Vulnerability Repair (2607.00820) | arXiv API, id_list batch | 1 | 0 |
| Lead: RAVEN (2606.22647) | arXiv API, id_list batch | 1 | 0 |
| Lead: VulKey (2605.01769) | arXiv API, id_list batch | 1 | 0 |
| Lead: Vul-R2 (2510.05480) | arXiv API, id_list batch | 1 | 0 |
| Lead: LLM4CVE (2501.03446) | arXiv API, id_list batch | 1 | 0 |
| Lead: SGAgent (2602.23647) | arXiv API, id_list batch | 1 | 0 |
| Lead: VulnResolver (2601.13933) | arXiv API, id_list batch | 1 | 0 |
| Lead: Multilingual vulnerability repair evaluation (2508.03470) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Rethinking the Capability of Fine-Tuned LMs for AVR" (2512.22633) | master index check | 0 | 0 |
| Lead: "Metrics Failure in LLM-Based Code Vulnerability Repair" (2609.26749) | arXiv API, id_list batch | 1 | 0 |
| Lead: SWEPatchTest (2610.18004) | arXiv API, id_list batch | 1 | 1 |
| Lead: InfCode (2511.16004) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Independent Patch Verification for Coding Agents" (2608.08950) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Confident and Wrong" (2603.25764) | arXiv API, id_list batch | 1 | 0 |
| Lead: "AgentLens: The Lucky Pass Problem" (2605.12925) | master index check | 0 | 0 |
| Lead: "Unveiling Practical Shortcomings of Patch Overfitting Detection Techniques" (2603.11262) | arXiv API, id_list batch | 1 | 1 |
| Lead: Terminal Wrench (2604.17596) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Auditing Reward Hackability in Code RL Training Environments" (2606.16062) | arXiv API, id_list batch | 1 | 1 |
| Lead: TestJack (2610.10619) | master index check | 0 | 0 |
| Lead: BenchJack (2605.12673) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Benchmarking Reward Hack Detection in Code Environments" (2601.20103) | arXiv API, id_list batch | 1 | 0 |
| Lead: CheatBench (2609.36308) | arXiv API, id_list batch | 1 | 0 |
| Lead: Hack-Verifiable Terminal Bench (2608.22103) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Maintaining Benchmarks Against Increasingly Capable Agents" (2609.34262; listed twice) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Every Model Cheats" (2607.21763) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Specification Self-Correction" (2507.18742) | arXiv API, id_list batch | 1 | 0 |
| Lead: TestEvo-Bench (2607.02469) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Are Coding Agents Generating Over-Mocked Tests?" (2602.00409) | arXiv API, id_list batch | 1 | 0 |
| Lead: "When Automated Program Repair Meets Regression Testing" (2105.07311) | arXiv API, id_list batch | 1 | 0 |
| Lead: Active-SWE (2608.04682) | arXiv API, id_list batch | 1 | 0 |
| Lead: "How Do LLMs Read Bug Reports?" (2607.25873) | arXiv API, id_list batch | 1 | 0 |
| Lead: crash report mining industrial report (2609.04483) | arXiv API, id_list batch | 1 | 0 |
| Lead: kAgent (2504.20412) | arXiv API, id_list batch | 1 | 0 |
| Lead: KGym (2407.02680) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Beyond Crash-to-Patch" (2604.03851) | arXiv API, id_list batch | 1 | 0 |
| Lead: incomplete security bug fixes in the Linux kernel (2511.17799) | arXiv API, id_list batch | 1 | 0 |
| Lead: HCC (2203.00364) | arXiv API, id_list batch | 1 | 0 |
| Lead: LLM-BSCVM (2505.17416) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Two Timin'" (2309.07841) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Prompt to Pwn" (ReX, 2508.01371); PoCo (2511.02780) | master index check | 0 | 0 |
| Lead: Kiro blog, DEV Community post, 1Password blog, Cantina post | WebSearch (1Password only); title screen | 9 | 0 |
| Lead: Rodríguez-Pérez et al., IST 2018 (SZZ reproducibility) | Semantic Scholar batch by DOI | 1 | 1 |
| Lead: Bird et al., "Fair and Balanced?" (ESEC/FSE 2009) | Semantic Scholar batch; ACM page (403); WebSearch; author PDF | 1 + 1 + 10 + 1 | 1 |
| Lead: Herzig and Zeller, "The impact of tangled code changes" (MSR 2013) | Semantic Scholar batch; OpenAlex by DOI | 1 + 1 | 1 |
| Lead: Herzig, Just, Zeller (EMSE) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: Rezk et al., ghost commits (TSE 2022) | Semantic Scholar batch by DOI | 1 | 1 |
| Lead: Iannone et al., "The Secret Life of Software Vulnerabilities" (TSE) | Semantic Scholar batch by DOI | 1 | 1 |
| Lead: Meneely et al., "When a Patch Goes Bad" (ESEM 2013) | Semantic Scholar batch; OpenAlex by DOI | 1 + 1 | 1 |
| Lead: Bosu et al., vulnerable code changes (FSE 2014) | Semantic Scholar batch; OpenAlex by DOI | 1 + 1 | 1 |
| Lead: "Revisiting the VCCFinder approach" (EMSE 2021) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: VCCFinder (Perl et al., CCS 2015) | Crossref title search; OpenAlex by DOI; Google Scholar | 3 + 1 + 10 | 1 |
| Lead: LLM-SZZ (ICSME 2025) | Semantic Scholar batch by DOI | 1 | 1 |
| Lead: MV-SZZ (TSE 2026) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: Nguyen and Massacci, NVD vulnerable versions (ASIACCS 2013) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: Aladics et al., Java VIC dataset (ICSOFT 2022) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: CrossCommitVuln-Bench (AIware 2026) | Semantic Scholar batch; arXiv API (2604.21917) | 1 + 1 | 1 |
| Lead: "Back to the Roots" (TOSEM) | master index check | 0 | 0 |
| Lead: Wang et al., real bug fixes in Solidity projects (JSS 2023) | Semantic Scholar batch; arXiv API (2210.11990) | 1 + 1 | 1 |
| Lead: Neural SZZ (ASE 2023) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: Sem-SZZ, Tang et al. (TSE 2024) | Semantic Scholar batch by DOI | 1 | 1 |
| Lead: "Beyond the Sum of Parts" (TSE 2026) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: Wen et al., inducing and fixing commits (ESEC/FSE 2019) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: SemBIC (PACMSE 2025) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: "Estimating Uncertainty in Labeled Changes by SZZ Tools" (TOSEM) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: corner cases in bug-inducing commits (SANER 2025) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: Rani et al., SZZ with bug discussion data (EMSE 2024) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: "Hunting bugs" (EMSE 2024) | Semantic Scholar batch by DOI | 1 | 1 |
| Lead: "Precise (Un)Affected Version Analysis for Web Vulnerabilities" (ASE 2022) | Semantic Scholar batch by DOI | 1 | 1 |
| Lead: Neto et al., refactoring and SZZ (SANER 2018) | Semantic Scholar batch; OpenAlex by DOI | 1 + 1 | 0 |
| Lead: OpenSZZ (ICPC 2020) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: Bludau and Pretschner, SZZ-induced evaluation bias (Research Square 2026) | Semantic Scholar batch; OpenAlex; Research Square page | 1 + 1 + 1 | 1 |
| Lead: Rosa et al., journal extension (JSS 2023) | master index check (conference version) | 0 | 0 |
| Lead: Quach et al., SZZ for non-functional bugs (EMSE 2021) | title not recorded in lead; not looked up | 0 | 0 |
| Lead: Global-SZZ (Figshare artifact) | title screen only | 0 | 0 |
| Lead: "Harness or Model?" (arXiv 2609.11987) | arXiv API, single and batch | 2 | 1 |
| Lead: EVMbench | master index check | 0 | 0 |
| Lead: AntiLeakBench (2412.13670) | arXiv API, id_list batch | 1 | 0 |
| Lead: DiffMIA (APSEC 2025) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: "Can Prompts Rewind Time for LLMs?" (EMNLP 2025) | Semantic Scholar batch; OpenAlex by DOI | 1 + 1 | 0 |
| Lead: CodeCleaner (Internetware 2025) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: "Memorization Diagnostics for Code LLMs Should be Scale-Aware" (2608.12771) | arXiv API, id_list batch | 1 | 0 |
| Lead: Code2Bench (2508.07180) | arXiv API, id_list batch | 1 | 0 |
| Lead: Cross-Context Verification (2603.21454) | arXiv API, id_list batch | 1 | 0 |
| Lead: Al-Haque and Johnson, ESEM 2026 | OpenAlex by DOI (wrong record); Dagstuhl page | 1 + 1 | 1 |
| Lead: "SWE-Bench+: Enhanced LLM Coding Benchmark" (AIware 2026) | Semantic Scholar batch; master index check | 1 | 0 |
| Lead: "Revisiting SWE-Bench" (ICSE Companion 2025) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: SecRepoBench, DualGauge, SafeGenBench, AutoBaxBuilder, A.S.E | master index check | 0 | 0 |
| Lead: Semgrep blog on Claude Opus 5.5 and SusVibes | semgrep.dev page | 1 | 1 |
| Lead: Molison et al. (ESEM 2025) | Semantic Scholar batch; arXiv API (2508.00700) | 1 + 1 | 1 |
| Lead: Deaconu et al. (EMSE 2026) | Semantic Scholar batch; arXiv API (2608.11513) | 1 + 1 | 1 |
| Lead: BAITBENCH (2608.30724) | arXiv API, id_list batch | 1 | 1 |
| Lead: "Beyond Pass@k" (2608.14711) | master index check | 0 | 0 |
| Lead: Le et al., overfitting in semantics-based APR (EMSE 2018) | master index check | 0 | 0 |
| Lead: Al-Bataineh, "The Undecidability of Overfitting in APR" (ICSE 2026 NIER) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: Yi et al., APR and test-suite metrics (EMSE) | Semantic Scholar batch; OpenAlex; author PDF (UCL) | 1 + 1 + 1 | 1 |
| Lead: DriftBench (CAIBDA 2026) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: mutation testing of task-scoped state oracles (Research Square 2026) | OpenAlex; Research Square page and PDF | 1 + 2 | 0 |
| Lead: "Everything You Wanted to Know About LLM-based Vulnerability Detection" (2504.13474) | arXiv API, id_list batch | 1 | 0 |
| Lead: Deininger et al. (JCP 2026) | master index check | 0 | 0 |
| Lead: Solca and Balan, "Who Judges the Judges?" (IEEE Access 2026) | Semantic Scholar; OpenAlex; IEEE page and PDF (blocked); WebSearch; Google Scholar | 2 + 1 + 2 + 9 + 1 | 1 |
| Lead: Gupta, "Patchproof" (SSRN 2026) | OpenAlex; SSRN page and PDF (403); Google Scholar | 1 + 2 + 1 | 1 |
| Lead: Jang and Kim, LLM-based oracles for patch correctness (ICST 2026) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: Majumdar, "Beyond F1" (Research Square 2026) | OpenAlex; Research Square page and PDF | 1 + 2 | 1 |
| Lead: GPTLens (2310.01152) | arXiv API, id_list batch | 1 | 1 |
| Lead: "Logic Meets Magic" (2501.07058) | arXiv API, id_list batch | 1 | 0 |
| Lead: LLM-SmartAudit (2410.09381) | arXiv API, id_list batch | 1 | 0 |
| Lead: Trail of Bits blog on Codex and GPT-4 audits | title screen only | 0 | 0 |
| Lead: "Agreement Without Accuracy" (OSF 2026) | OpenAlex by DOI | 1 | 1 |
| Lead: LLM-as-a-Judge SoK (2603.29403) | arXiv API, id_list batch | 1 | 0 |
| Lead: "All Verdicts are Not Equal" (2610.12083) | arXiv API, id_list batch | 1 | 0 |
| Lead: "Context Over Content" (2604.15224) | arXiv API, id_list batch | 1 | 0 |
| Lead: "How to Trick Your AI TA" (2512.10415) | arXiv API, id_list batch | 1 | 0 |
| Lead: Nadăş, LLMs as judges review (AI Review 2026) | Semantic Scholar batch by DOI | 1 | 0 |
| Lead: Feng et al., cross-ecosystem case-control (EMSE 2026) | Semantic Scholar batch; OpenAlex; Springer page and PDF (challenge); WebSearch; arXiv title search | 1 + 1 + 2 + 9 + 30 | 1 |
| Lead: AgOSS (2609.02591) | arXiv API, id_list batch | 1 | 1 |
| Lead: INTENTFIX (ICSE 2026) | Crossref title search; OpenAlex; Semantic Scholar batch | 3 + 1 + 1 | 1 |
| Lead: PoCE (ISSTA 2026) | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: SecChain (ASE 2026) | master index check | 0 | 0 |
| Lead: SPSYN (ASE 2026) | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: "From Vibe to Spec" (ASE 2026) | Crossref; OpenAlex; Semantic Scholar batch | 3 + 1 + 1 | 1 |
| Lead: "Evidence-Grounded Logic Vulnerability Detection for Smart Contracts" (ASE 2026) | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: PatchAudit (CCS 2026) | Crossref; Semantic Scholar search; WebSearch x2; arXiv; CCS 2026 accepted-papers page | 3 + 0 + 18 + 0 + 1 | 1 |
| Lead: "From Fix to Flaw" (CCS 2026) | Crossref; WebSearch; arXiv; CCS 2026 accepted-papers page | 3 + 9 + 0 + 1 | 1 |
| Lead: Eshghie and Artho, oracle-guided exploit synthesis (ASE 2024) | Semantic Scholar search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: Molinelli et al., LLM test oracles (ASE 2025) | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: Flashboom (IEEE S&P 2025) | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: Luo et al., test-suite guided vulnerability validation for Node.js (CCS 2024) | Crossref; OpenAlex; Semantic Scholar batch | 3 + 1 + 1 | 1 |
| Lead: Dozono et al. (ASE 2025) | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: SCAR (FSE 2026 Companion) | Crossref; OpenAlex; Semantic Scholar batch | 3 + 1 + 1 | 0 |
| Lead: Lanturn (CCS 2023) | Crossref; OpenAlex; Semantic Scholar batch | 3 + 1 + 1 | 1 |
| Lead: FairChecker (ICSE 2025) | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: Midas (ISSTA 2024) | Crossref title search; OpenAlex by DOI | 3 + 1 | 1 |
| Lead: AdvSCanner (ASE 2024) | master index check | 0 | 0 |
| Lead: SmartFix (ESEC/FSE 2023) | Crossref title search; OpenAlex by DOI | 3 + 1 | 0 |
| Lead: MoE smart contract repair, MoEFix (ASE 2025) | Crossref title search; OpenAlex by DOI | 3 + 1 | 0 |
| Lead: MAS-SZZ (2604.24398) | master index check | 0 | 0 |
| Lead: "Usability as a Weapon" (2605.10133) | arXiv API, id_list batch | 1 | 1 |
| Lead: "Securing AI-Generated Code: A Just-in-Time ..." (2608.16187) | arXiv API, id_list batch | 1 | 0 |
| Requested: Eick et al. 1992, "Estimating software fault content before coding" | Crossref; OpenAlex; Semantic Scholar; IEEE page; Google Scholar; WebSearch x2; ACM page via Wayback copy | 3 + 1 + 1 + 1 + 1 + 18 + 1 | 1 |
| Requested: Briand et al., TSE 2000, capture-recapture models | Crossref; OpenAlex by DOI; Fraunhofer and Simula pages (blocked) | 3 + 1 + 2 | 1 |
| Sweep: capture-recapture software inspections defect content estimation | Crossref | 10 | 4 |
| Sweep: capture-recapture software vulnerabilities estimation | Crossref | 10 | 2 |
| Sweep: capture-recapture number of remaining defects software testing | Crossref | 10 | 1 |
| Sweep: capture recapture bug bounty vulnerabilities estimate | Crossref | 10 | 0 |
| Sweep: capture-recapture static analysis tools number of bugs | Crossref | 10 | 0 |
| Sweep: estimating the number of remaining links in traceability recovery capture-recapture | Crossref | 10 | 0 |
| Sweep: capture-recapture two inspectors evaluating models | Crossref | 10 | 2 |
| Sweep: Vander Wiel and Votta; Petersson et al. review; Walia et al. (title lookups) | Crossref | 9 | 2 |
| Sweep: capture-recapture in cs.SE, cs.CR, cs.LG, cs.AI | arXiv API, abstract search | 5 | 1 |
| Sweep: capture-recapture for undiscovered vulnerabilities, multiple tools or auditors | WebSearch; USENIX ;login: PDF | 10 + 1 | 1 |
| Sweep: case-control study software vulnerabilities | Crossref | 10 | 0 |
| Sweep: case-control study software engineering | Crossref | 10 | 0 |
| Sweep: matched case-control software defects | Crossref | 10 | 0 |
| Sweep: "case-control" in titles | arXiv API, title search | 30 | 0 |
| Sweep: "case-control" in abstracts, cs.SE or cs.CR | arXiv API, abstract search | 6 | 0 (Paul 2021 and Allodi 2014 already indexed) |
| Sweep: selection bias software engineering empirical dataset | Crossref | 10 | 1 |
| Sweep: sample selection bias defect prediction | Crossref | 10 | 1 |
| Sweep: missing links bugs and bug-fix commits | Crossref | 10 | 1 |
| Sweep: case study of bias in bug-fix datasets | Crossref | 10 | 1 |
| Sweep: stratified sampling software engineering research | Crossref | 10 | 1 |
| Sweep: sampling bias mining software repositories GitHub projects | Crossref | 10 | 0 |
| Sweep: real-world labelling of vulnerabilities; vulnerability dataset quality; latent vulnerabilities | Crossref | 12 | 2 |
| Failed: 10 Semantic Scholar title searches for the L9 leads | Semantic Scholar search API | 3 (9 of 10 calls returned HTTP 429) | 0 |
| Failed: 28 DBLP title searches | DBLP API (bot check page) | 0 | 0 |

## Already indexed

These leads are already in the master index (`lit/master_index_partial.tsv`, matched on the last column, the title, after removing case and punctuation).

- "The Patch Overfitting Problem in Automated Program Repair: Practical Magnitude and a Baseline for Realistic Benchmarking" (Petke2024-PatchOverfit). Listed in both the L6 and L8 sections.
- "Rethinking the Capability of Fine-Tuned Language Models for Automated Vulnerability Repair" (Han2026-FineTunedAVR).
- "AgentLens: The Lucky Pass Problem" (AgentLens2026).
- TestJack (Yao2026-TestJack).
- "Prompt to Pwn" (Xiao2026-ReX) and PoCo (Andersson2025-PoCo). ReX is listed in both the L6 and L9 sections.
- EVMbench (EVMbench2026). The Cantina blog post about it is screened out below.
- The 1Password blog "Why AI-generated vulnerability patches still require expert human review" reports the FLAWED study, which is indexed as Mierczuk2026-FLAWED.
- "Back to the Roots: Assessing Mining Techniques for Java Vulnerability-Contributing Commits" (Hinrichs2026-VCCMining).
- "SWE-Bench+: Enhanced LLM Coding Benchmark" (AIware 2026, DOI 10.1145/3805760.3814924). The arXiv version is indexed as Aleithan2024-SWEBenchPlus. Semantic Scholar lists the AIware version's first author as "Xu Haoran" with DBLP key conf/aiware/XueAEUW26, and Reem Aleithan as second author. The orchestrator may want to add the published venue to the existing row.
- SecRepoBench (Shen2025-SecRepoBench), DualGauge (Patir2025-DualGauge), SafeGenBench (Li2025-SafeGenBench), AutoBaxBuilder (vonArx2026-AutoBaxBuilder), A.S.E (Lian2026-ASE).
- "Beyond Pass@k" (Jiang2026-BeyondPassAtK).
- "Overfitting in semantics-based automated program repair" (Le2018-OverfittingSemantics).
- "Fixing, Breaking, or Faking It?" (Deininger2026-FixingBreakingFaking).
- SecChain (Sun2026-SecChain), AdvSCanner (Wu2024-AdvSCanner), MAS-SZZ (Cao2026-MASSZZ).
- Rosa et al., journal extension of the developer-informed oracle study (JSS 2023). The conference version is indexed as Rosa2021-DevOracle. The journal version was not opened.

## Screened out

"Abstract read" means I read the abstract (arXiv, Semantic Scholar, OpenAlex or publisher page) before deciding. "Title" means I decided from the title and the lead's context.

| Lead | Reason |
|---|---|
| Zhu et al., "An Empirical Study of APR Techniques for Injection Vulnerabilities" (ICSME 2024) | Abstract read. Traditional APR tools on injection flaws; finds the fixes are more complex than general fixes. At most C. |
| Al-Bataineh, "Towards Developing Effective Oracles to Reduce Patch Overfitting" (SANER 2025) | Abstract read. Adds a termination oracle and an assertion oracle from bug reports. At most C. |
| Kilgi and Bahsi, multi-agent LLMs for vulnerable code repair (ICISSP 2026) | Abstract read on the SciTePress page. Multi-agent setups repair more at extra cost. Does not vary inputs or execution access. At most C. |
| "Catching Developers in the Flow" (ASE 2026) | Title. Low-latency industrial repair at Google. At most C. |
| "Memorization in LLM-Based Program Repair" (APR 2025) | Title. Contamination in repair. At most C; the index already holds several memorisation papers. |
| "Heterogeneous Prompting and Execution Feedback for SWE Issue Test Generation and Selection" (ICSE 2026) | Title. Test generation for issues. At most C. |
| TDD-Bench Verified (arXiv 2412.02883) | Abstract read. LLMs write fail-to-pass tests before the fix. At most C. |
| OpenAI blog "Introducing SWE-bench Verified"; METR blog on reward hacking; MacDiarmid et al. 2025 | Title. Grey literature or RL-training safety. At most C; reward hacking on code is covered by indexed ImpossibleBench and EvilGenie. |
| PatchIsland, EviRepair, AgenticRepair, MemRepair, EvoRepair, Knowledge-Enhanced Agentic Vulnerability Repair (KeaRepair), RAVEN, VulKey, Vul-R2, LLM4CVE, SGAgent, VulnResolver, InfCode | Abstracts read. New repair systems. None holds back exploits to judge repairs or compares repair inputs as a study question. At most C. |
| ContraFix (arXiv 2605.17450) | Abstract read. Repair system. One useful number for N3: a semantic audit found only 58.2% of its benchmark-validated SEC-Bench patches and 31.3% of the strongest baseline's were semantically correct. At most C. |
| "On the Evaluation of LLMs in Multilingual Vulnerability Repair" (2508.03470) | Abstract read. Repair benchmark study across languages. At most C. |
| "Metrics Failure in LLM-Based Code Vulnerability Repair" (2609.26749) | Abstract read. Shows compile rate and CodeBLEU mislead on Big-Vul with small models and argues for execution-based evaluation. At most C. |
| "Independent Patch Verification for Coding Agents" (RETRACE, 2608.08950); "Confident and Wrong" (2603.25764) | Abstracts read. Patch self-checking by reconstruction; submit rate against resolve rate. At most C. |
| Terminal Wrench, BenchJack, TRACE reward-hack detection (2601.20103), CheatBench, Hack-Verifiable Terminal Bench, "Every Model Cheats", "Specification Self-Correction" | Abstracts read. Reward-hacking benchmarks and mitigations. At most C; the closest ones are already indexed. |
| "Maintaining Benchmarks Against Increasingly Capable Agents" (2609.34262) | Abstract read. Audits passing trajectories in benchmarks. Notes that blocking one recorded exploit is not enough because the same information stays reachable another way, which echoes N3. At most C. |
| TestEvo-Bench; "Are Coding Agents Generating Over-Mocked Tests?" (MSR 2026); "When APR Meets Regression Testing" (TOSEM); Active-SWE | Abstracts read. Test co-evolution, mocking, regression test selection for patch validation, bug fixing without reports. At most C. |
| "How Do LLMs Read Bug Reports?" (ASE 2026); crash report mining industrial report (2609.04483) | Abstracts read. Attention over bug-report sections; industrial crash analysis. At most C. |
| kAgent, KGym, "Beyond Crash-to-Patch" | Abstracts read. Linux kernel crash repair. At most C. |
| "Characteristics, Root Causes, and Detection of Incomplete Security Bug Fixes in the Linux Kernel" (2511.17799) | Abstract read (shortened on arXiv). Human incomplete security fixes. Background for N3 only. At most C. |
| HCC (2203.00364); LLM-BSCVM (2505.17416); "Two Timin'" (2309.07841) | Abstracts read. Hardening compiler, LLM vulnerability-management pipeline, classifier-based repair. At most C. |
| Kiro blog; DEV Community post; Cantina post on EVMbench | Title. Grey literature commentary. At most C. |
| Herzig, Just, Zeller, tangled changes and defect prediction (EMSE) | Journal extension of the MSR 2013 paper, aimed at defect prediction. The MSR 2013 block below covers the tracing point. |
| "Revisiting the VCCFinder approach" (EMSE 2021) | Abstract read. Replication of a commit classifier. At most C. |
| MV-SZZ (TSE 2026); Neural SZZ (ASE 2023); "Beyond the Sum of Parts" (TSE 2026); Wen et al. (ESEC/FSE 2019); SemBIC (PACMSE 2025); Guo et al. (TOSEM); Serifoglu and Tüzün (SANER 2025); Rani et al. (EMSE 2024); OpenSZZ (ICPC 2020) | Abstracts read. SZZ variants, tools and label-noise filters for defect data. At most C. SemBIC notes that one could find the introducing commit by running the failing test on old versions, which the project can do with its PoVs. |
| Neto et al., refactoring and SZZ (SANER 2018) | Abstract read. 19.9% of lines removed in fixes are refactorings, so SZZ blames wrong commits. At most C. |
| Nguyen and Massacci, NVD vulnerable versions (ASIACCS 2013); Aladics et al., Java VIC dataset (ICSOFT 2022) | Abstracts read. NVD version errors; SZZ-based Java dataset. At most C. |
| Quach et al. (EMSE 2021); Global-SZZ (Figshare artifact) | Title not recorded in the lead; artifact only, no paper. Not checked further. |
| AntiLeakBench; DiffMIA; "Can Prompts Rewind Time for LLMs?"; CodeCleaner; "Memorization Diagnostics ... Scale-Aware"; Code2Bench; Cross-Context Verification | Abstracts read. Contamination detection or contamination-free benchmark building. At most C; the index already has several. |
| "Revisiting SWE-Bench: On the Importance of Data Quality" (ICSE Companion 2025) | Abstract read. Single-author short version of the SWE-Bench+ analysis, which is indexed. |
| Al-Bataineh, "The Undecidability of Overfitting in APR" (ICSE 2026 NIER) | Abstract read. Position paper. At most C. |
| DriftBench (CAIBDA 2026) | Abstract read. Cheating detection with hidden constraints in the specification. At most C. |
| Sun, mutation testing of task-scoped state oracles (Research Square 2026) | PDF read. Benchmark evaluators rejected 100 of 110 harmful state mutations; all 10 misses were in ToolSandbox. Different domain. At most C. |
| "Everything You Wanted to Know About LLM-based Vulnerability Detection" (2504.13474) | Abstract read. Context-rich evaluation of LLM detectors. At most C for N6. |
| Jang and Kim (ICST 2026) | Abstract read. Prompt strategies for LLM-written assertions in patch assessment. At most C. |
| "Logic Meets Magic" (2501.07058); LLM-SmartAudit (2410.09381); Trail of Bits blog (2023) | Abstracts read (blog: title). LLM smart-contract detection. At most C; GPTLens is kept below as the representative. |
| LLM-as-a-Judge SoK (2603.29403); "All Verdicts are Not Equal" (2610.12083); "Context Over Content" (2604.15224); Nadăş review (AI Review 2026) | Abstracts read. General LLM-judge reliability. At most C, because the project confirms flaws with PoVs, not with a judge. |
| "How to Trick Your AI TA" (2512.10415) | Withdrawn by the authors, per its arXiv comment. |
| SCAR (FSE 2026 Companion) | Abstract read. Tool that crawls audit reports (OpenZeppelin, Code4rena). Data source only. At most C. |
| SmartFix (ESEC/FSE 2023); MoEFix (ASE 2025) | Abstracts read. Smart-contract repair with a verifier or a mixture of experts. At most C. |
| "Securing AI-Generated Code: A Just-in-Time Vulnerability Detection and Remediation Pipeline" (2608.16187) | Abstract read. Master's practicum project. At most C. |

## New entries: statistical design

### Feng2026-CaseControlEcosystems A methodology to perform cross-ecosystems case-control security studies
- Authors: Yuan Feng et al. (with Ranindya Paramitha, Carlos E. Budde, Fabio Massacci); Year: 2026; Venue: Empirical Software Engineering, vol. 32, issue 1 (online 18 July 2026)
- URL opened: https://www.semanticscholar.org/paper/340ffb255311ce14a49f0bdf4d977383963144cd (Semantic Scholar record read through the API: title, authors, full abstract); https://api.openalex.org/works/doi:10.1007/s10664-026-10873-9 (OpenAlex record, same abstract, volume and issue). The Springer page https://link.springer.com/article/10.1007/s10664-026-10873-9 and its open-access PDF returned a JavaScript challenge.
- Status: VERIFIED (abstract read in two index records; publisher page blocked)
- Tier: B
- Touches: none directly; statistical design behind N1
- Summary: The paper argues that counting vulnerabilities per ecosystem is not enough, and that case-control studies are the accepted way to estimate relative risk, provided cases and controls are comparable. It builds a human-guided protocol to carry library categories from one ecosystem to another, so that like is compared with like. It then runs a case-control study on Snyk data and GitHub Security Advisories marked "reviewed" up to 2024: 76 Java/Maven and 221 Python/PyPI libraries with a critical CVSS vulnerability are cases, and 58 and 166 libraries with only high-severity vulnerabilities are controls. The overall odds ratio of a critical vulnerability is 1.13 for Java/Maven against Python/PyPI; low attack complexity raises the odds of being critical 38.9 times in Java/Maven and 5.9 times in Python/PyPI; after 2023 the risk reverses and is 2.4 times higher for Python/PyPI. Data and protocol are released.
- Delta: The paper compares libraries across ecosystems, and both its cases and its controls are vulnerable libraries split by severity. The project compares an agent with the human on the same function, and its control group holds functions from the same commit that the human wrote correctly. The paper gives the project a recent software-engineering precedent for case-control language, for odds ratios, and for matching cases and controls on category. It does not deal with paired outcomes (human and agent on the same task), and it does not ask whether its controls hide undiscovered flaws. The project selects its treatment functions on the human's outcome, so its agent-against-human comparisons are conditioned on the human having failed; the paper's framing helps to state that design honestly.

### Bird2009-FairBalanced Fair and Balanced? Bias in Bug-Fix Datasets
- Authors: Christian Bird et al. (with Adrian Bachmann, Eirik Aune, John Duffy, Abraham Bernstein, Vladimir Filkov, Premkumar Devanbu); Year: 2009; Venue: ESEC/FSE 2009, pp. 121–130
- URL opened: https://www.cs.ucdavis.edu/~filkov/papers/biasbusters.pdf (author PDF, full text). The ACM page https://dl.acm.org/doi/10.1145/1595696.1595716 returned HTTP 403.
- Status: VERIFIED
- Tier: B
- Touches: none directly; selection bias in how tasks are chosen, and the tracing method
- Summary: Only some fixed bugs are linked to the commits that fixed them, and researchers study only the linked ones. The paper asks whether that sample is fair. Using Eclipse (two datasets), Netbeans, the Apache web server, OpenOffice, Gnome and AspectJ, it finds strong statistical evidence of two biases: linked fixes over-represent less severe bugs (in Apache, 63% of fixed minor bugs are linked but only 15% of fixed blocker bugs), and they are fixed by more experienced developers. Training the BugCache predictor on such biased subsamples changes its performance. The authors conclude that bias threatens both prediction models and the generality of hypotheses tested on these datasets.
- Delta: The paper is about defect-prediction datasets built from linked commits. The project builds its tasks only from audit findings that it can trace to an introducing commit, reproduce with a PoV, and turn into a feature request. Each of those steps can drop findings in a way that depends on severity or difficulty. Bird et al. give the standard argument and a simple test: compare the kept findings with all findings on features you can observe for both, such as severity, contest platform and size of the fix. The paper says nothing about security, audits or LLMs.

### Jimenez2019-RealWorldLabelling The importance of accounting for real-world labelling when predicting software vulnerabilities
- Authors: Matthieu Jimenez et al. (with Renaud Rwemalika, Mike Papadakis, Federica Sarro, Yves Le Traon, Mark Harman); Year: 2019; Venue: ESEC/FSE 2019, pp. 695–705
- URL opened: https://api.openalex.org/works/doi:10.1145/3338906.3338941 (OpenAlex record with title, authors, full abstract; ACM pages return 403)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: none directly; labelling of the control group (N1, N6)
- Summary: Earlier vulnerability-prediction studies trained with labels that include vulnerabilities discovered only later. This study uses 1,898 real vulnerabilities in 74 releases of the Linux kernel, OpenSSL and Wireshark, and compares three prediction approaches with and without that unrealistic labelling. With realistic labels, mean MCC drops from 0.77, 0.65 and 0.43 to 0.08, 0.22 and 0.10. The authors conclude that the labelling assumption can mislead scientific conclusions.
- Delta: The project labels its control functions as "written correctly" because no audit finding names them. Some of them may hold flaws nobody has found yet. This paper shows that ignoring flaws found later can reverse a conclusion. It studies prediction models, not human or agent code, and it does not estimate how many flaws remain. The project's LLM review with PoV confirmation checks the control functions directly, and the capture-recapture papers below show how to estimate what both reviewers miss.

### Croft2023-VulnDataQuality Data Quality for Software Vulnerability Datasets
- Authors: Roland Croft et al. (with M. Ali Babar, M. Mehdi Kholoosi); Year: 2023; Venue: ICSE 2023, pp. 121–133
- URL opened: https://api.openalex.org/works/doi:10.1109/icse48619.2023.00022 (OpenAlex record with full abstract; open copy at arXiv 2301.05456 not opened)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; label quality
- Summary: Checks five data-quality attributes of four widely used vulnerability datasets. Finds that 20–71% of vulnerability labels are inaccurate in the real-world datasets and that 17–99% of data points are duplicated, and shows that these problems hurt model training or inflate benchmark results.

### Bachmann2010-MissingLinks The missing links: bugs and bug-fix commits
- Authors: Adrian Bachmann et al. (with Christian Bird, Foyzur Rahman, Premkumar Devanbu, Abraham Bernstein); Year: 2010; Venue: FSE 2010, pp. 97–106
- URL opened: https://api.openalex.org/works/doi:10.1145/1882291.1882308 (OpenAlex record with full abstract; open copy https://www.zora.uzh.ch/id/eprint/44841/1/Bachmann-pdf.pdf not opened)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; selection bias, ground-truth sampling
- Summary: Follows up on Bird et al. 2009 by building ground truth. A core developer of the Apache web server used the Linkster tool to annotate all 493 commits from a six-week period, marking which ones fix bugs. The analysis of this complete sample shows serious and consequential problems in linked defect data.

### Nguyen2010-BiasBugFix A Case Study of Bias in Bug-Fix Datasets
- Authors: Thanh H. D. Nguyen et al. (with Bram Adams, Ahmed E. Hassan); Year: 2010; Venue: WCRE 2010, pp. 259–268
- URL opened: https://api.openalex.org/works/doi:10.1109/wcre.2010.37 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; selection bias
- Summary: Tests the bias reported by Bird et al. on a commercial project with strict rules for linking and tagging. Bias is still present even in this near-ideal dataset, so the authors suggest that bias comes from the development process itself and not only from linking heuristics.

### Rahman2013-SizeVsBias Sample size vs. bias in defect prediction
- Authors: Foyzur Rahman et al. (with Daryl Posnett, Israel Herraiz, Premkumar Devanbu); Year: 2013; Venue: ESEC/FSE 2013, pp. 147–157
- URL opened: https://api.openalex.org/works/doi:10.1145/2491411.2491418 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; selection bias against sample size
- Summary: Simulates biased samples drawn from a high-quality dataset and runs a meta-analysis. Sample size matters as much as the direction of bias, and more for AUC and F-score, so for prediction models a larger sample can sometimes offset bias.

### Furia2026-OmittedVariableBias Mitigating omitted variable bias in empirical software engineering
- Authors: Carlo A. Furia, Richard Torkar; Year: 2026; Venue: Empirical Software Engineering, vol. 31, issue 5
- URL opened: https://api.openalex.org/works/doi:10.1007/s10664-026-10851-1 (OpenAlex record with full abstract; Springer open-access PDF listed but Springer pages are behind a challenge)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: none directly; statistical design
- Summary: Omitted variable bias happens when a model leaves out a variable that affects the outcome, so its effect is wrongly given to included variables. The paper shows the problem on two software-engineering examples and gives methods to check for it, estimate its size and reduce it, based on causal structural models (diagrams of which variable affects which). It recommends doing this before running a study, because it leads to a better design.
- Delta: The project's outcome (did the agent write the bug, did the repair hold) depends on the finding, the project, the agent, the model and the wording of the request. A causal diagram drawn before the full study would show, for example, that finding difficulty affects both whether the human failed and whether the agent fails. The paper is general and has no security or LLM content.

### Bludau2026-SZZEvaluationBias Quantifying SZZ-Induced Evaluation Bias in Just-in-Time Defect Prediction
- Authors: Peter Bludau, Alexander Pretschner; Year: 2026; Venue: Research Square preprint (DOI 10.21203/rs.3.rs-9846265/v1)
- URL opened: https://www.researchsquare.com/article/rs-9846265/v1 (preprint page with title, authors, full abstract)
- Status: VERIFIED
- Tier: B
- Touches: none directly; tracing method and how to report its error
- Summary: Builds a manually validated sample of 420 commits from 6 open-source projects and a stratified, weighted evaluation protocol to estimate performance for the whole population. PR-SZZ labels about 12% of commits wrongly, mostly as false positives. When just-in-time defect prediction models are scored against the manual labels instead of PR-SZZ labels, mean recall drops from 0.72 to 0.64 and precision from 0.27 to 0.19. Some reported gains from feature engineering do not survive, which suggests models learn SZZ's labelling errors.
- Delta: The project traces each audit finding to the commit that introduced it. This paper gives a ready template for reporting the tracing error: a stratified sample checked by hand, with weights to recover population numbers. It studies defect prediction, not security findings or agents.

### Arjmandi2026-HarnessOrModel Harness or Model? Isolating the Harness Effect in Agentic Coding with a Contamination-Controlled Private Suite
- Authors: Mohsen Arjmandi; Year: 2026; Venue: arXiv preprint (2609.11987)
- URL opened: https://arxiv.org/abs/2609.11987 (arXiv abstract record, read through the arXiv export API)
- Status: VERIFIED
- Tier: B
- Touches: N1 (design of the agent and model comparison)
- Summary: Measures whether a vendor's own harness beats a neutral harness when the model is held fixed. The same 80 tasks from a private, contamination-controlled suite of 256 repository and post-cutoff contest tasks ran under claude-agent-sdk and deepagents on claude-opus-4-8, and under the openai-codex SDK and deepagents on gpt-5.5; 792 of 800 planned runs were graded by an isolated oracle. Neither contrast shows an average harness advantage: −1.25 points for Opus 4.8 (task-bootstrap 95% CI [−10.0, +7.5]) and +1.25 points for GPT-5.5 (CI [−4.4, +6.9]). For Opus the native harness trails by 9.0 points on 61 repository tasks and leads by 23.7 points on 19 contest tasks (permutation p = 0.003), but the split was chosen after seeing the data. 22 of 81 runs cancelled at the time limit had already produced a passing patch.
- Delta: The project crosses three agents (Aider, OpenHands, Codex CLI) with two models, so it faces the same question of how much of a difference comes from the harness and how much from the model. This paper gives a usable design: paired contrasts on the same tasks with task-level bootstrap intervals, and a warning that splitting tasks after seeing results can create effects, so strata must be fixed in advance. It measures task success only, with no human baseline, no security outcome and no exploits.

### AlHaque2026-TaskDifficulty What Makes Software Issue Resolution Tasks Difficult for Agents?
- Authors: Ebtesam Al-Haque, Brittany Johnson; Year: 2026; Venue: ESEM 2026, LIPIcs vol. 394, pp. 3:1–3:20
- URL opened: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESEM.2026.3 (Dagstuhl publisher page with full abstract). Note: OpenAlex attaches this DOI to the SWE-Bench Pro record, which is a wrong merge.
- Status: VERIFIED
- Tier: C
- Touches: none; covariates for the analysis
- Summary: Uses CoderForge-Preview, a large open dataset of coding-agent trajectories, and extracts features of the task's patch, the repository and the prompt. Task difficulty is largely predictable from static features (AUC = 0.863) and is driven mostly by how scattered the patch is and how large the repository is. Features of the prompt's wording matter for tasks of middle difficulty.

### Lin2026-AgreementWithoutAccuracy Agreement Without Accuracy: Six Systematic Defects an LLM Annotation Study Could Not See in Its Own Reliability Statistics
- Authors: Hon-Ren Lin; Year: 2026; Venue: OSF preprint (DOI 10.31235/osf.io/n3zhf_v1)
- URL opened: https://api.openalex.org/works/doi:10.31235/osf.io/n3zhf_v1 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N6
- Summary: An LLM annotated 1,902 student UML class specifications with a fixed snapshot, seed and zero temperature, under three prompt setups run twice each. A three-stage pipeline seemed to raise agreement from .647 to .845, with chance-corrected agreement rising for every code. Yet five systematic defects were present; for example, an instruction that promised an input never supplied was wrong on 64.7% of its flags at κ = .971. The author's own audit rule agreed with a blind reading on only 67.5% of cases. The paper recommends comparing how often each code fires and reading a blind random sample drawn independently of the detector.
- Delta: The paper is about LLM annotation in education, not security. For N6, it warns that agreement between the project's two LLM reviewers, or between repeated runs of one reviewer, does not show that their findings are correct. The project's rule that a PoV must confirm each reported flaw is the kind of independent check the paper asks for. The paper also suggests reading a blind random sample of reviews that reported nothing, to estimate misses.

### Dudhaiya2026-AgOSS AgOSS: A Dataset and Multi-Layer Characterization of Open-Source Agricultural Software
- Authors: Vatsal Dudhaiya et al. (with Mikhail Golovenchits, Aryan Banerjee, James C. Davis); Year: 2026; Venue: arXiv preprint (2609.02591)
- URL opened: https://arxiv.org/abs/2609.02591 (arXiv abstract record via the export API)
- Status: VERIFIED
- Tier: C
- Touches: none; matched controls
- Summary: 66 agricultural open-source repositories in six categories, compared with matched non-agricultural controls on OpenSSF Scorecard, governance, SBOM-based dependency risk and known-exploited vulnerabilities. Agricultural projects score far lower on raw Scorecard, but size and maturity confound the gap: it loses significance under matching and regression. The round 1 lead's remark that results depend on the random seed of the matching is not in the abstract; I did not read the full text.

### Podgurski1999-StratifiedSampling Estimation of software reliability by stratified sampling
- Authors: Andy Podgurski et al. (with Wassim Masri, Yolanda McCleese, Francis Wolff, Charles Yang); Year: 1999; Venue: ACM TOSEM 8(3), pp. 263–283
- URL opened: https://api.openalex.org/works/doi:10.1145/310663.310667 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; stratified sampling
- Summary: Combines operational testing with stratified sampling, using cluster analysis of execution profiles to form strata, so that fewer executions must be checked by hand to estimate reliability. Experiments suggest a large cut in cost. It is the classic software-engineering use of stratified sampling for a population estimate.

### Briand2000-CaptureRecapture A comprehensive evaluation of capture-recapture models for estimating software defect content
- Authors: Lionel C. Briand et al. (with K. El Emam, Bernd G. Freimut, Oliver Laitenberger); Year: 2000; Venue: IEEE Transactions on Software Engineering 26(6), pp. 518–540
- URL opened: https://api.openalex.org/works/doi:10.1109/32.852741 (OpenAlex record with full abstract). The IEEE page and the Fraunhofer repository copy were blocked.
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: none directly; estimating flaws that reviewers miss (N6 control group)
- Summary: Uses data from real inspections to measure how accurately capture-recapture models predict the number of defects left after an inspection. Accuracy depends strongly on the number of inspectors. With too few inspectors no model is accurate enough and the underestimate can be large. The authors recommend a model that lets defects differ in how easy they are to find (the Mh model) with the Jackknife estimator, and they calibrate predictions with relative errors from earlier inspections.
- Delta: In the control group, two LLM reviewers look for new flaws in the same code, and PoVs confirm what they report. That is the setting of capture-recapture: the overlap between the two reviewers' confirmed flaws estimates how many flaws both missed. Briand et al. show that two reviewers are at the low end, so the estimate may be biased down, and that the choice of model matters. The paper uses human inspections of documents and code, not LLM reviewers or exploits.

### ElEmam2001-TwoInspectors Evaluating capture-recapture models with two inspectors
- Authors: K. El Emam, Oliver Laitenberger; Year: 2001; Venue: IEEE Transactions on Software Engineering 27(9), pp. 851–864
- URL opened: https://api.openalex.org/works/doi:10.1109/32.950319 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: none directly; N6 control group
- Summary: A Monte Carlo simulation of code inspections with exactly two inspectors evaluates which capture-recapture model to use and how good the resulting "reinspect or not" decision is. The best model for two inspectors is one that allows the two inspectors to differ in ability. It always produces an estimate, behaves predictably when its assumptions hold, gives fairly high decision accuracy, and does better than never reinspecting.
- Delta: This is the closest classic match to the project's two LLM reviewers. It says which estimator to use when there are only two reviewers and they differ in skill (for example, two different models). It assumes the two reviewers find flaws independently, which two LLM reviewers with the same prompt may not; see Wu 2016 and Rong 2017 below.

### VanderWiel1993-DesignReviews Assessing software designs using capture-recapture methods
- Authors: Scott A. Vander Wiel, Lawrence G. Votta; Year: 1993; Venue: IEEE Transactions on Software Engineering 19(11), pp. 1045–1054
- URL opened: https://api.openalex.org/works/doi:10.1109/32.256852 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; capture-recapture
- Summary: Capture-recapture can estimate the faults a design review did not find, but its wildlife assumptions do not hold for reviews. A Monte Carlo simulation shows that the maximum likelihood estimator works well if faults are grouped into a few groups that are equally hard to find; without grouping it can do poorly, though usually better than the Jackknife estimator.

### Eick1992-FaultContent Estimating software fault content before coding
- Authors: Stephen G. Eick et al. (with Clive R. Loader, M. David Long, Lawrence G. Votta, Scott Vander Wiel); Year: 1992; Venue: ICSE 1992 (14th International Conference on Software Engineering), pp. 59–65
- URL opened: https://web.archive.org/web/20220320055507/https://dl.acm.org/doi/10.1145/143062.143090 (archived copy of the ACM page: title, authors, venue, pages and reference list, but no abstract); Crossref record https://api.crossref.org/works/10.1145/143062.143090 (no abstract); Google Scholar result (garbled snippet only). The live ACM and IEEE pages were blocked.
- Status: UNVERIFIED (the paper exists and the metadata above is confirmed, but no page I could reach shows an abstract; ACM shows none for this paper and the PDF is blocked)
- Tier: C
- Touches: none; capture-recapture
- Summary: I could not read the paper. The ACM page lists capture-recapture references (Pollock 1991 on capture, recapture and removal statistics; Otis, Burnham, White and Anderson on closed animal populations). The review by Petersson et al. (2004, below) says capture-recapture was introduced to software inspections in 1992, and its reference list includes this paper. Nothing more is claimed here.

### Petersson2004-CRCReview Capture–recapture in software inspections after 10 years research––theory, evaluation and application
- Authors: Håkan Petersson et al. (with Thomas Thelin, Per Runeson, Claes Wohlin; the Lund University page lists the first author as Håkan Ahrefors); Year: 2004; Venue: Journal of Systems and Software 72(2), pp. 249–264
- URL opened: https://www.lunduniversity.lu.se/lup/publication/282e2518-f7d2-49e0-bd9c-49934bcf9849 (university repository page with title, authors, venue and abstract)
- Status: VERIFIED
- Tier: C
- Touches: none; capture-recapture
- Summary: Reviews ten years of capture-recapture for estimating faults left after inspections, a method introduced in 1992. Sorts the work into theory, evaluation and application. Most basic theory comes from biostatistics; most software-engineering studies evaluate models and often recommend the Mh model with the Jackknife estimator; practical experience is lacking. Proposes an inspection process with decision points based on the estimates.

### Walia2008-NumberOfInspectors The effect of the number of inspectors on the defect estimates produced by capture-recapture models
- Authors: Gursimran Singh Walia et al. (with Jeffrey C. Carver, Nachiappan Nagappan); Year: 2008; Venue: ICSE 2008, pp. 331–340
- URL opened: https://api.openalex.org/works/doi:10.1145/1368088.1368134 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; capture-recapture
- Summary: With data from 73 inspectors, tests estimators from biology not used before on inspections and measures how the number of inspectors affects accuracy. Unlike earlier results that favoured the Jackknife, the sample coverage (SC) estimators suit inspections better. Gives how many inspectors are needed for estimates within 5% to 20% of the actual count.

### Wu2016-InspectorDependence How Does the Dependence between Inspectors Impact Capture-Recapture Estimation? An Empirical Study
- Authors: Ou Wu; Year: 2016; Venue: IEEE QRS 2016, pp. 398–405
- URL opened: https://api.openalex.org/works/doi:10.1109/qrs.2016.51 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; capture-recapture with dependent reviewers (N6)
- Summary: Measures the correlation between inspectors and relates it to the error and confidence interval of the Mt maximum likelihood estimate, using nine datasets from five papers. Larger correlation in absolute value goes with larger relative error, so dependence between inspectors cannot be ignored.

### Rong2017-CRCConfidence Towards Confidence with Capture-recapture Estimation
- Authors: Guoping Rong et al. (with Bohan Liu, He Zhang, Qiuping Zhang, Dong Shao); Year: 2017; Venue: EASE 2017, pp. 242–251
- URL opened: https://api.openalex.org/works/doi:10.1145/3084226.3084250 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; capture-recapture with dependent reviewers (N6)
- Summary: Uses a coefficient of covariation to measure statistical dependence between inspectors in published capture-recapture datasets. Most datasets show non-zero dependence, and the fit between dependence and relative error has R² above 0.8. Proposes a version of the measure that uses the estimated total, so the credibility of an estimate can be judged in practice.

### Scott2008-CRCUnitTesting Capture-recapture in software unit testing
- Authors: Hanna Scott, Claes Wohlin; Year: 2008; Venue: ESEM 2008, pp. 32–40
- URL opened: https://api.openalex.org/works/doi:10.1145/1414004.1414012 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; capture-recapture
- Summary: Several developers test the same unit, and capture-recapture on their results estimates the failures still left, without historical data. Evaluated in a pre-study on a large open-source project and then at a medium-sized company, where it produced a usable estimate.

### Duran1981-CRCSeeding Capture-Recapture Sampling for Estimating Software Error Content
- Authors: Joe W. Duran, John J. Wiorkowski; Year: 1981; Venue: IEEE Transactions on Software Engineering SE-7(1), pp. 147–148
- URL opened: https://api.openalex.org/works/doi:10.1109/tse.1981.230821 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; capture-recapture
- Summary: Short correspondence on Mills' method, in which known errors are inserted on purpose and testing then finds both inserted and real errors. Shows how to get correct confidence limits and maximum likelihood estimates for fixed-size and sequential testing.

### Wang2019-iSENSE Crowdtesting: When is The Party Over?
- Authors: Junjie Wang et al. (with Ye Yang, Zhe Yu, Tim Menzies and one more); Year: 2018 (preprint), published 2019; Venue: arXiv preprint 1805.03218; the arXiv journal reference gives the published version as "iSENSE: completion-aware crowdtesting management", ICSE 2019, pp. 912–923 (published version not opened)
- URL opened: https://arxiv.org/abs/1805.03218 (arXiv abstract record via the export API)
- Status: VERIFIED (preprint abstract)
- Tier: C
- Touches: none; capture-recapture with many independent bug finders
- Summary: Decides when to close a crowdtesting task, where many workers report bugs independently. Designs eight close-prediction methods, based on bug-trend, bug-arrival and capture-recapture models, and evaluates them on 218 tasks from a large Chinese crowdtesting platform; the results show a median of 91% of bugs detected with 49% of the cost saved. Relevant because audit contests also have many independent finders whose duplicate reports could feed a capture-recapture estimate.

### Geer2015-Undiscovered For Good Measure: The Undiscovered
- Authors: Dan Geer; Year: 2015; Venue: USENIX ;login: 40(2), April 2015, pp. 50–52 (column, grey literature)
- URL opened: https://usenix.org/system/files/login/articles/login_apr15_12_geer.pdf (full text)
- Status: VERIFIED
- Tier: C
- Touches: none; capture-recapture for vulnerabilities
- Summary: Explains the Lincoln index and its assumptions, recalls Vander Wiel and Votta (1993) and the Petersson et al. review, and says he knows of no one who has applied capture-recapture to latent zero-day vulnerabilities. Suggests a first step: three or more independent penetration tests, or three or more static-analysis firms, on the same target. It is the clearest bridge I found from inspection capture-recapture to security.

## New entries: tracing the commit that introduced the bug

### RodriguezPerez2018-SZZReproducibility Reproducibility and credibility in empirical software engineering: A case study based on a systematic literature review of the use of the SZZ algorithm
- Authors: Gema Rodríguez-Pérez et al. (with G. Robles, Jesus M. Gonzalez-Barahona); Year: 2018; Venue: Information and Software Technology
- URL opened: https://www.semanticscholar.org/paper/cf8bfcb20fe96aec32b3f12e00b9ed2eb13fb023 (Semantic Scholar record via the API with full abstract; ScienceDirect not reachable)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: none directly; tracing method
- Summary: A systematic review of 187 papers that use SZZ to find where a bug came from. Reproducibility is rare, limitations are often not reported, and improved SZZ versions are seldom used. The paper gives lessons and guidelines for authors and reviewers.
- Delta: The project's tracing of each finding to its introducing and fixing commits is a use of the same idea, so it inherits the paper's reporting duties: publish the tracing steps, the tool and version, and every manual decision. The paper is a review of SZZ use; it does not cover security findings, audit reports or LLMs.

### HerzigZeller2013-Tangled The impact of tangled code changes
- Authors: Kim Herzig, Andreas Zeller; Year: 2013; Venue: MSR 2013, pp. 121–130
- URL opened: https://api.openalex.org/works/doi:10.1109/msr.2013.6624018 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: none directly; tracing method
- Summary: Developers often commit unrelated changes together. In five open-source Java projects, up to 15% of bug fixes consist of several tangled changes, and at least 16.6% of source files are wrongly linked to bug reports on average.
- Delta: Audited projects sometimes fix several findings in one commit. The project therefore cannot treat the whole fix commit as the fix of one finding; it must separate the lines that fix each finding before tracing back. The paper studies Java defects, not smart-contract security fixes.

### Rezk2022-GhostCommits The Ghost Commit Problem When Identifying Fix-Inducing Changes: An Empirical Study of Apache Projects
- Authors: Christophe Rezk et al. (with Yasutaka Kamei, Shane McIntosh); Year: 2022; Venue: IEEE Transactions on Software Engineering
- URL opened: https://www.semanticscholar.org/paper/56206042d03206961be96f97b411de48f5273a84 (Semantic Scholar record via the API with full abstract)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: none directly; tracing method
- Summary: Some commits are invisible to SZZ. In 14 Apache projects, 5.66–11.72% of defect-fixing commits only add lines, so SZZ has nothing to trace back; 1.05–4.60% of commits only remove lines; and for 0.35–14.49% of fixes no candidate survives SZZ's filtering. Of 142 addition-only fixes, 46.5% add checks such as null or emptiness checks. A mitigation for addition-only fixes reaches precision 0.753, 39.5 points better than the baseline.
- Delta: Many audit fixes add a missing check, such as a `require` statement or a bound, so they are addition-only and plain SZZ blames nothing. The project's tracing must handle these fixes by hand or with a method that looks at the code around the added lines (see Sem-SZZ below). The paper studies Java defects, not Solidity security fixes.

### Iannone2023-SecretLife The Secret Life of Software Vulnerabilities: A Large-Scale Empirical Study
- Authors: Emanuele Iannone et al. (5 authors, with R. Guadagni, F. Ferrucci, A. De Lucia); Year: 2023; Venue: IEEE Transactions on Software Engineering
- URL opened: https://www.semanticscholar.org/paper/bcbfc2eefe6e278274052f52a5535d7a3c0ce318 (Semantic Scholar record via the API with full abstract)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: none directly; tracing method; N1 background
- Summary: Studies 3,663 NVD vulnerabilities with public patches from 1,096 GitHub projects, using an SZZ-based procedure plus manual analysis. Vulnerabilities take on average at least 4 contributing commits before they are introduced, and half stay unfixed for more than a year. Most contributions come from developers with a high workload, often during maintenance, and fixes mostly add new checks on inputs.
- Delta: The finding that a vulnerability usually builds up over several commits challenges the project's assumption that one commit introduced the bug and that one function body holds it. The project should record, for each finding, whether more than one commit contributed. The paper studies human code only.

### Meneely2013-VCC When a Patch Goes Bad: Exploring the Properties of Vulnerability-Contributing Commits
- Authors: Andrew Meneely et al. (with Harshavardhan Srinivasan, Ayemi Musa, Alberto Rodriguez Tejeda, Matthew Mokary, Brian Spates); Year: 2013; Venue: ESEM 2013, pp. 65–74
- URL opened: https://api.openalex.org/works/doi:10.1109/esem.2013.19 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: none directly; tracing method; N1 background
- Summary: Traced 68 vulnerabilities in the Apache web server by hand to 124 vulnerability-contributing commits spanning 17 years. These commits have more than twice the code churn of other commits, even after normalising for size, and a commit is twice as likely to contribute a vulnerability when its author is new to that code.
- Delta: A manual tracing precedent close to the project's. It asks what makes a human commit risky; the project asks whether an agent repeats the human's mistake when it writes the same feature.

### Bosu2014-VulnerableChanges Identifying the characteristics of vulnerable code changes: an empirical study
- Authors: Amiangshu Bosu et al. (with Jeffrey C. Carver, Munawar Hafiz, Patrick Hilley, Derek Janni); Year: 2014; Venue: FSE 2014, pp. 257–268
- URL opened: https://api.openalex.org/works/doi:10.1145/2635868.2635880 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: none directly; comparison of vulnerable and non-vulnerable changes (design of N1)
- Summary: From 267,046 code review requests in 10 open-source projects, identifies 413 vulnerable code changes. Experienced contributors wrote most of them, but changes by less experienced contributors were 1.8 to 24 times more likely to be vulnerable; the chance of a vulnerability rises with lines changed; modified files are more likely to hold vulnerabilities than new files.
- Delta: It compares vulnerable and non-vulnerable human changes, which is close to a case-control comparison. The project instead compares the agent and the human on the same change. Its risk factors (size of change, new or modified file) are candidates for the project's strata.

### Perl2015-VCCFinder VCCFinder: Finding Potential Vulnerabilities in Open-Source Projects to Assist Code Audits
- Authors: Henning Perl et al. (with Sergej Dechand, Matthew Smith, Daniel Arp, Fabian Yamaguchi, Konrad Rieck, Sascha Fahl, Yasemin Acar); Year: 2015; Venue: ACM CCS 2015, pp. 426–437
- URL opened: https://api.openalex.org/works/doi:10.1145/2810103.2813604 (OpenAlex record with full abstract; Crossref and OpenAlex store the title as just "VCCFinder"; the full title is confirmed by the Google Scholar result page)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: none; tracing method
- Summary: Made the first large-scale mapping of CVEs to GitHub commits to build a database of vulnerability-contributing commits, then trained an SVM to flag suspicious commits. At the same recall as Flawfinder, it cuts false alarms by over 99%.

### Fan2025-LLMSZZ LLM-SZZ: Novel Vulnerability-Inducing Commit Identification Driven by Large Language Model and CVE Description
- Authors: Siqi Fan et al. (9 authors); Year: 2025; Venue: ICSME 2025
- URL opened: https://www.semanticscholar.org/paper/179a16da00ee0d9b727fc22f09dbe41637eb9e57 (Semantic Scholar record via the API with full abstract)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: none directly; tracing method
- Summary: SZZ variants for vulnerabilities have low precision because they consider irrelevant lines and files, need bug discussions that many CVEs lack, and lose the trail in older versions. LLM-SZZ gives an LLM the CVE description and the fixing diff to find the true root-cause lines before tracing back. It reports over 18% higher precision than prior methods across datasets in several languages.
- Delta: The project has a written audit report for every finding, which is richer than a CVE description, so an LLM-assisted tracer of this kind fits its data. LLM-SZZ is evaluated on CVEs in general-purpose languages, not on Solidity audit findings, and it does not use an exploit to check the result. The indexed MAS-SZZ is the closest sibling.

### Majumdar2026-CrossCommitVuln CrossCommitVuln-Bench: A Dataset of Multi-commit Python Vulnerabilities Invisible to Per-Commit Static Analysis
- Authors: Arunabh Majumdar (Semantic Scholar lists "Arun Majumdar"); Year: 2026; Venue: AIware 2026 (DOI 10.1145/3805760.3814928); arXiv 2604.21917
- URL opened: https://arxiv.org/abs/2604.21917 (arXiv abstract record via the export API); https://www.semanticscholar.org/paper/9986737d584308ca7a1cebc5216322c7d90184f0 (record of the published version)
- Status: VERIFIED
- Tier: C
- Touches: none; tracing method
- Summary: Python CVEs whose exploitable condition was introduced across several commits, each harmless on its own to per-commit static analysis. The published version reports 30 CVEs, a per-commit detection rate of 7% and 13% when the whole codebase is scanned; arXiv v1 reports 15 CVEs, 13% and 27%. Supports recording multi-commit introductions when tracing.

### Wang2023-SolidityBugFixes An empirical study on real bug fixes from solidity smart contract projects
- Authors: Yilin Wang et al. (with Xiangping Chen, Yuan Huang, Hao-Nan Zhu and two more); Year: 2023; Venue: Journal of Systems and Software (article 111787); arXiv 2210.11990
- URL opened: https://arxiv.org/abs/2210.11990 (arXiv abstract record via the export API); https://www.semanticscholar.org/paper/1bd71b46b576469db3f285e13ba9608140486013 (record of the journal version)
- Status: VERIFIED
- Tier: B
- Touches: N2; tracing method
- Summary: Studies historical bug fixes in 46 real-world Solidity projects along four questions: file type and amount, fix complexity, bug distribution, and fix patches. Distils four findings and gives implications for repair techniques, analysis tools and Solidity developers.
- Delta: It is the only study I found of bug-fix history inside Solidity projects, the same kind of history the project traces. The project could report the same fix-complexity measures for its findings so that its sample can be compared with Solidity fixes in general. The abstract does not mention tracing introducing commits, separating security findings, or any LLM.

### MaesBermejo2024-HuntingBugs Hunting bugs: Towards an automated approach to identifying which change caused a bug through regression testing
- Authors: Michel Maes-Bermejo et al. (6 authors, with Alexander Serebrenik, Micael Gallego, F. Gortázar); Year: 2024; Venue: Empirical Software Engineering
- URL opened: https://www.semanticscholar.org/paper/281b69ab0b7ac5a69d7b61576dce451fe5bfbd18 (Semantic Scholar record via the API with full abstract)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: none directly; tracing method; N3
- Summary: Puts into practice the idea of a perfect test, one that fails whenever the bug is present and passes otherwise. Regression tests written with the fix are moved back onto past snapshots of the code to find the change that introduced the bug, on Defects4J. Of 809 bugs, the introducing change was found exactly for 95, and for 4 more a list of candidates including it was given; it works when the tests can be moved and run on old snapshots.
- Delta: The project has a PoV for every finding, which is a test that passes exactly when the bug is present. Running the PoV on earlier commits is this paper's method with a security test, and it would check the project's SZZ-style tracing. The paper uses Java regression tests, not exploits.

### Shi2022-AffectedVersions Precise (Un)Affected Version Analysis for Web Vulnerabilities
- Authors: You-Qun Shi et al. (5 authors, with Yuan Zhang, Tianhan Luo, Xiangyu Mao); Year: 2022; Venue: ASE 2022
- URL opened: https://www.semanticscholar.org/paper/0d6f72f7683efc2d3e211fe92e3b0b2959652436 (Semantic Scholar record via the API with full abstract)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: none directly; tracing method
- Summary: Extracts the vulnerability logic from a patch and checks it directly against each version to decide whether that version is affected, which tolerates code changes across versions. On 34 CVEs and 299 versions it reaches 98.15% precision and 85.01% recall and beats V-SZZ, ReDebug and V0Finder.
- Delta: Like the project, it decides where a vulnerability exists from the vulnerability's logic rather than from line history. The project can go one step further and run its executable PoV on each commit. The paper targets web application vulnerabilities, not smart contracts.

### Tang2024-SemSZZ Enhancing Bug-Inducing Commit Identification: A Fine-Grained Semantic Analysis Approach
- Authors: Lingxiao Tang et al. (with Chao Ni, Qiao Huang, Lingfeng Bao); Year: 2024; Venue: IEEE Transactions on Software Engineering
- URL opened: https://www.semanticscholar.org/paper/6b566e7185abca19f26096c2a2324da756891ae7 (Semantic Scholar record via the API with full abstract)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: C
- Touches: none; tracing method
- Summary: Sem-SZZ handles fixes with no deleted lines by tracing unchanged lines near the added lines, using program slicing and a comparison of data flow and control flow before and after the fix. It outperforms earlier methods whether or not the fix deletes lines. A candidate technique for addition-only audit fixes.

## New entries: repairs, test oracles and held-out tests (N3, N4)

### Alsaid2026-TerraProbe TerraProbe: A Layered-Oracle Framework for Detecting Deceptive Fixes in LLM-Assisted Terraform
- Authors: Manar Alsaid et al. (with Chimdumebi Nebolisa, Faris Abbas); Year: 2026; Venue: arXiv preprint (2606.26590), submitted to Empirical Software Engineering
- URL opened: https://arxiv.org/abs/2606.26590 (arXiv abstract record via the export API)
- Status: VERIFIED
- Tier: A
- Touches: N3
- Summary: Evaluations of LLM security repair often count a repair as successful when the targeted static-analysis finding disappears. TerraProbe adds five layers of checks to 288 first-pass repairs by gemini-2.5-flash-lite, GPT-4o and Claude 3.5 Sonnet on 68 real Terraform modules and 28 modules with injected defects. For the main model, the targeted Checkov finding disappears in 83.3% of repairs, but only 10.4% pass the full scanner, 39.6% still plan, and 38.5% reach plan comparison. Human review finds that 71.4% of the plan-compared real-world repairs are deceptive: they pass automated checks but leave the vulnerability. Deceptive-fix rates of 57.1% to 71.4% do not differ across the three models (pairwise Fisher p > 0.10). The taxonomy of deceptive fixes has Cohen's κ = 0.78 and Krippendorff's α = 0.76.
- Delta: It makes the same point as the project's repair round: a repair can pass the check it was shown and still leave the flaw. A reviewer could cite it against N3's claim that this is new. The differences are concrete. TerraProbe works on Terraform configuration, its shown check is a static-analysis finding, and its deeper check needs human judgment. The project works on smart-contract code, its shown and held-out checks are both executable exploits, its verdict needs no human judgment, and it measures the funds a shallow repair still loses (48.88 ETH in the pilot).

### Mohammadi2026-WhoseOracle Whose Oracle Is It? The Authority Problem in Deployed Agentic Program Repair
- Authors: Bardia Mohammadi, Laurent Bindschaedler; Year: 2026; Venue: APR 2026 (7th International Workshop on Automated Program Repair), DOI 10.1145/3843776.3844673
- URL opened: https://www.semanticscholar.org/paper/2ccce93d6f9144e0a4826e53482c41e893d98d28 (Semantic Scholar record via the API with full abstract; ACM page blocked)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: N4, N3
- Summary: Tests are both the evidence that accepts a patch and repository files that may themselves need repair. Benchmarks make the evaluator's tests immutable, but real deployments cannot, because tests change with the code. The authors argue that deciding who may change the evidence that accepts a patch is separate from deciding whether a patch is correct, and that no diff can tell an approved change of requirements from an agent weakening its own acceptance test. They propose evidence that exists before the agent runs and that the agent cannot rewrite (their "admissible repair witness"), and a two-zone policy. In 230 merged bug-fix pull requests from nine repositories, 160 of 172 repairs that changed tests (93.0%) edited a test file that already existed; 87 deleted test lines, but only 53 deleted an assertion, a test case, an expected output or a whole test file.
- Delta: The project found that agents with a terminal kept the repository's own tests passing although those tests assert the buggy behaviour. This paper names the same tension, but it studies human pull requests and proposes a policy, with no exploits and no agents measured. The project's held-out PoVs are evidence the agent cannot see or rewrite. The paper suggests the project should also report how often agents edited existing tests or the shown PoV.

### Wang2026-OracleMutable The Oracle Is Mutable: Obedient Destruction of Verification Targets in Shared-Workspace Agent Environments
- Authors: Xisen Wang et al. (with Yu Chen, Yaqi Zhao, David Xu); Year: 2026; Venue: NeurIPS 2026 workshop "Who Verifies the Agents? Toward Reliable Agent Development" (poster)
- URL opened: https://neurips.cc/virtual/2026/173042 (conference page with title, authors and abstract)
- Status: VERIFIED
- Tier: B
- Touches: N3, N4
- Summary: When a benchmark asks the agent to put its build output at the path of the reference program, following instructions can destroy the oracle. In 17 episodes of a program-reconstruction benchmark, agents overwrote or deleted the reference binary in 6, with single and multi-agent setups. In three of these, agents kept running differential tests against their own output and logged success (one reported PASS=39 FAIL=0), while the external hidden-test scorer, which stayed intact, scored one such artifact at 10.5%. Proposed fix: keep a snapshot of the reference outside the agent's workspace.
- Delta: It shows that a check inside the agent's workspace can be destroyed without any bad intent. The project already keeps its held-out PoVs outside the agent's reach and shows only one PoV, which matches the paper's fix. The paper is a small poster on non-security tasks; the project should still report whether agents changed the shown PoV or the repository tests.

### Bui2023-APR4Vul APR4Vul: an empirical study of automatic program repair techniques on real-world Java vulnerabilities
- Authors: Quang-Cuong Bui et al. (5 authors, with Ranindya Paramitha, Duc-Ly Vu, Fabio Massacci); Year: 2023 (online December 2023; the DBLP key in the Semantic Scholar record points to a 2024 volume); Venue: Empirical Software Engineering
- URL opened: https://www.semanticscholar.org/paper/bd6990b1a10347b5fd7bd7341c0658a7bc12d780 (Semantic Scholar record via the API with full abstract)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: N3
- Summary: Nine APR tools and one vulnerability-specific tool on 79 Java vulnerabilities from Vul4J, a dataset with PoV tests. The tools produce testable patches for about 20% of the vulnerabilities. Nearly 73% of testable patches remove the vulnerability, but only 44% do so while keeping the functionality. Security fixes are short but often add method calls with input-validation words such as encode, normalize and trim.
- Delta: It judges patches by the PoV and by functional tests, and shows that closing the PoV is not enough. The project adds held-out PoVs, so it also catches repairs that close the shown PoV but leave another exploit path. APR4Vul uses traditional repair tools on Java with one PoV per vulnerability, not LLM agents.

### Pinconschi2021-APRSecurity A Comparative Study of Automatic Program Repair Techniques for Security Vulnerabilities
- Authors: Eduard Pinconschi et al. (with Rui Abreu, Pedro Adão); Year: 2021; Venue: ISSRE 2021, pp. 196–207
- URL opened: https://api.openalex.org/works/doi:10.1109/issre52982.2021.00031 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N3
- Summary: Ten test-suite-based repair tools on the DARPA Cyber Grand Challenge vulnerabilities in C/C++. Together they fix 30 of 55 vulnerable programs (54.6%). Tools with small change operators and brute-force search (AE, GenProg) and a tool that deletes functionality (Kali) do best overall; AE alone repairs 20 of 55.
- Delta: That a deletion tool scores well shows that exploit-based validation accepts repairs that remove the feature. A repair that deletes the feature also blocks every held-out PoV, since a deleted feature cannot be exploited. So the project needs functional tests that do not assert the buggy behaviour to rule such repairs out. The paper uses traditional tools on C programs, not LLM agents.

### Shariffdeen2021-CPR Concolic program repair
- Authors: Ridwan Shariffdeen et al. (with Yannic Noller, Lars Grunske, Abhik Roychoudhury); Year: 2021; Venue: PLDI 2021, pp. 390–405
- URL opened: https://api.openalex.org/works/doi:10.1145/3453483.3454051 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N3
- Summary: Repair tools change a program until it passes the given tests and cannot tell a correct patch from one that overfits them. CPR explores patches and inputs together with concolic execution, generating new inputs that rule out overfitting patches. It shrinks the pool of candidate patches by up to 74% for software vulnerabilities and 63% for SV-COMP programs; longer runs leave fewer overfitting fixes.
- Delta: CPR attacks overfitting to one exploit input by generating more inputs during repair. The project measures the same problem after the fact, with fixed held-out PoVs written from audit reports, and it judges LLM agents rather than building a repair tool.

### Yi2018-TestSuiteMetrics A correlation study between automated program repair and test-suite metrics
- Authors: Jooyong Yi et al. (with Shin Hwei Tan, Sergey Mechtaev, Marcel Böhme, Abhik Roychoudhury); Year: 2018 (online 2017); Venue: Empirical Software Engineering 23(5), pp. 2948–2979
- URL opened: https://discovery.ucl.ac.uk/10184114/1/emse17.pdf (author manuscript PDF with title, authors, abstract)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: Asks whether test-suite metrics from software testing can control the reliability of generated repairs, meaning the chance that a repair causes regressions. In large experiments on real software, reliability tends to rise with statement coverage, branch coverage and mutation score, most clearly with statement coverage.
- Delta: The project's shown PoV is a test suite of one test, which is weak by these measures. The paper motivates reporting how much of the vulnerable function the shown and held-out PoVs cover. It studies traditional repair tools, not LLM agents or exploits.

### Guo2026-FeedbackGranularity Evaluating Symbolic Feedback Granularity for LLM-Based Program Repair
- Authors: Taoer Guo; Year: 2026; Venue: APR 2026, pp. 45–50
- URL opened: https://api.openalex.org/works/doi:10.1145/3843776.3844675 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N4
- Summary: Separates the form of verifier feedback from model, task and prompting effects. Compares five kinds of feedback, from a pass or fail status to natural-language explanations, concrete counterexamples and raw symbolic traces, with four open-weight code models (7B to 480B parameters) on 540 tasks built from verification problems and contract-annotated HumanEval+ and MBPP+. Counterexample feedback repairs best. Full symbolic traces carry more information but do not help more; a padding control shows prompt length explains only part of the gap; adding a full trace to a counterexample adds nothing.
- Delta: Both this paper and the project vary what the model is told and find that more information is not always better. The paper's best input, a concrete counterexample, is the nearest thing to the project's shown PoV. The paper uses small verified programs and single-shot models, with no agents, no security bugs, no control over code execution, and no held-out checks.

### Lu2026-SWEPatchTest SWEPatchTest: Evaluating Software Tests Beyond Reproduction
- Authors: Hua Lu et al. (7 authors); Year: 2026; Venue: arXiv preprint (2610.18004)
- URL opened: https://arxiv.org/abs/2610.18004 (arXiv abstract record via the export API)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: A test suite that fails on the buggy program and passes on the reference patch can still accept wrong patches or reject correct ones. SWEPatchTest has 619 tasks from SWE-bench Pro, SWE-bench Multilingual and DeepSWE, and 82,579 candidate patches from coding-agent runs. Its Joint Validation Rate requires reproducing the issue, accepting correct patches and rejecting incorrect ones on the same task. The best setup reaches only 9.21% on this rate while it reproduces the reference transition on 59.29% of tasks.
- Delta: Each of the project's PoVs passes on the human's vulnerable code and fails on the human's fix, which is exactly the check this paper shows is not enough on its own. The project answers with several PoVs per finding and some held back. This paper answers by scoring each test on many real candidate patches. The project could do the same and replay every PoV on all agent repairs to see how well each PoV separates good from bad repairs. The paper has no security or exploit focus.

### Rajan2026-RewardHackability Auditing Reward Hackability in Code RL Training Environments
- Authors: Shreshth Rajan; Year: 2026; Venue: arXiv preprint (2606.16062)
- URL opened: https://arxiv.org/abs/2606.16062 (arXiv abstract record via the export API)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: On a 49-task sample of SWE-bench Verified, 28.5% of tasks have tests weak enough that an incorrect patch, verified in Docker, passes them; on 20 R2E-Gym tasks the rate is 25.0%. A random-effects meta-analysis over 134 SWE-bench Verified submissions finds that, within the same human-rated difficulty level, Pass@1 is 14.14 points higher on tasks flagged as weak than on robust tasks (95% CI [+11.80, +16.48]; I² = 0%; 123 of 134 models positive). A hardening loop that checks generated tests against the gold patch first finds that 65 of 105 LLM-written tests fail on the gold patch itself.
- Delta: It measures how often weak tests accept wrong patches, the problem the project's held-out PoVs address for security repairs. Its analysis, comparing pass rates on weak and robust tasks within difficulty levels with a random-effects model, could be reused to compare findings with one PoV against findings with several. It has no security content.

### Prasad2026-BAITBENCH BAITBENCH: Measuring Agent Reward Hacking with Optional Shortcuts Planted in ML Tasks
- Authors: Pradyumna Shyama Prasad et al. (6 authors); Year: 2026; Venue: arXiv preprint (2608.30724)
- URL opened: https://arxiv.org/abs/2608.30724 (arXiv abstract record via the export API)
- Status: VERIFIED
- Tier: B
- Touches: N3, N4
- Summary: Three synthetic tabular machine-learning tasks each contain an optional shortcut that raises the public test score but fails on a hidden test set. Across seven frontier agents, 57.1% of runs use the shortcut, and five of seven agents do so in more than half their runs. The rate stays above 50% even when agents are told not to.
- Delta: It uses a hidden test set to catch agents that fit the visible check, the same logic as the project's held-out PoVs. Its shortcut is planted on purpose in ML tasks. In the project the shortcut is natural (the shown PoV covers only one case) in real smart-contract repairs, and the cost of fitting the shown test is measured in stolen funds.

### Williams2026-PODShortcomings Unveiling Practical Shortcomings of Patch Overfitting Detection Techniques
- Authors: David Williams et al. (with Ioakim Avraam, Aldeida Aleti, Matias Martinez and two more); Year: 2026; Venue: arXiv preprint (2603.11262)
- URL opened: https://arxiv.org/abs/2603.11262 (arXiv abstract record via the export API)
- Status: VERIFIED
- Tier: B
- Touches: N3
- Summary: Benchmarks six patch overfitting detection methods (static, dynamic and learning-based) on datasets that reflect what repair tools really produce, against two random-sampling baselines. Simple random selection beats every detection tool in 71% to 96% of cases, depending on the tool.
- Delta: The project does not use overfitting detectors; it judges repairs by running held-out exploits. This paper supports that choice, since current detectors do not beat random choice on realistic patches. It covers general program repair, not security or agents.

### Liu2025-VulDebugger Agent That Debugs: Dynamic State-Guided Vulnerability Repair
- Authors: Zhengyao Liu et al. (7 authors); Year: 2025; Venue: arXiv preprint (2504.07634); venue of any published version not checked
- URL opened: https://arxiv.org/abs/2504.07634 (arXiv abstract record via the export API)
- Status: VERIFIED
- Tier: B
- Touches: N4
- Summary: VulDebugger is a repair agent that inspects the real program state in a debugger, infers the expected state from constraints, and compares the two to find the root cause, as a human would. It fixes 60.00% of vulnerabilities in 50 real projects and beats prior vulnerability-repair approaches.
- Delta: Here running the code helps repair. The project found the opposite for OpenHands with a full terminal (2 of 12 successes against 10 of 12 with no execution), because the repository's tests encoded the bug. Read together, the two suggest that running code helps only when what the agent runs gives a correct signal. VulDebugger targets crashes in C/C++ and does not test repairs with held-out exploits.

### Molinelli2025-TestOracles Do LLMs Generate Useful Test Oracles? An Empirical Study with an Unbiased Dataset
- Authors: Davide Molinelli et al. (with Luca Di Grazia, Alberto Martin-Lopez, Michael D. Ernst, Mauro Pezzè); Year: 2025; Venue: ASE 2025, pp. 278–290
- URL opened: https://api.openalex.org/works/doi:10.1109/ase63991.2025.00031 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: C
- Touches: N4 (background)
- Summary: Uses 13,866 test oracles from 135 Java projects, all written after the models' training cut-off dates, to avoid contamination. LLM-generated oracles reach a mean mutation score of 43%, close to the 45% of human-written oracles. The test prefix and the methods called give enough information; more code context does not help.

### Mughal2026-OracleAuthority LLM-Based Test Oracles: Source-of-Authority Taxonomy -- A Systematic Literature Review
- Authors: Ali Hassaan Mughal, Muhammad Bilal; Year: 2026; Venue: IEEE Access, vol. 14 (per the arXiv journal reference); arXiv 2607.05031
- URL opened: https://arxiv.org/abs/2607.05031 (arXiv abstract record via the export API)
- Status: VERIFIED
- Tier: C
- Touches: N4 (background)
- Summary: PRISMA review screening 2,436 records to 54 studies, extended to 83 by snowballing. Sorts LLM test oracles by where their authority comes from, their form and how they are judged. Just over half reach a verdict with no specification at all, and oracle quality is most often judged by resemblance to a known oracle rather than by catching injected faults. Useful wording for the project's finding that repository tests can encode the buggy behaviour.

### Heo2026-INTENTFIX INTENTFIX: Automated Logic Vulnerability Repair via LLM-Driven Intent Modeling
- Authors: Jinseok Heo et al. (with Dongwook Choi, Jinyoung Kim, Misoo Kim, Eunseok Lee); Year: 2026; Venue: ICSE 2026, pp. 843–854
- URL opened: https://www.semanticscholar.org/paper/262db7a844dfea8e7bb7d0786d965fa4593ded51 (Semantic Scholar record via the API with full abstract); https://api.openalex.org/works/doi:10.1145/3744916.3773260 (OpenAlex record)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: N3, N5
- Summary: Logic vulnerabilities come from gaps between what the developer meant and what the code does, and they pass ordinary tests. INTENTFIX has an LLM write down the developer's implicit intent as a structured model, compares that model with the code to find the gaps, and then writes and refines a patch. On 1,107 real CVEs across five vulnerability types and 19 languages, it reports a patch accuracy of 64.5%, 1.97 times that of chain-of-thought baselines.
- Delta: It repairs logic flaws by stating the intended rule first. The project's pilot points the same way: when the feature request stated the rule that the fix restores, 12 of 15 runs avoided the bug. INTENTFIX does not judge patches with exploits, does not hold checks back, and does not vary what the agent is told or can run.

### Tithy2026-PoCE PoCE: Automated Proof-of-Concept Synthesis using Large Language Models for Robust Validation
- Authors: Tanusree Das Tithy et al. (7 authors, last author Faysal Hossain Shezan); Year: 2026; Venue: Proceedings of the ACM on Software Engineering 3 (ISSTA 2026), pp. 986–1009
- URL opened: https://api.openalex.org/works/doi:10.1145/3832134 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N3
- Summary: Generates proof-of-concept tests with an LLM using in-context learning, retrieval and iterative reasoning, and expands one working PoC into several validated variants that are run in controlled environments. On thirteen projects including TensorFlow, Zlib, Node.js, Binutils and LibTIFF, it succeeds in 77.7% of cases, finds other trigger paths and edge conditions, produces 68 zero-day PoCs and finds 26 unknown vulnerabilities.
- Delta: Turning one PoC into several variants is a way to produce the extra PoVs the project holds back to judge repairs. PoCE uses its variants to reproduce and find vulnerabilities in native and Python libraries, not to test whether a repair closes every trigger path, and it has no smart contracts.

## New entries: LLM security review and confirming flaws (N6)

### Majumdar2026-BeyondF1 Beyond F1: A Study of LLM Reliability in Smart Contract Vulnerability Detection
- Authors: Durjoy Majumdar; Year: 2026; Venue: Research Square preprint (DOI 10.21203/rs.3.rs-10783572/v1)
- URL opened: https://www.researchsquare.com/article/rs-10783572/latest.pdf (preprint PDF with title, author, abstract)
- Status: VERIFIED
- Tier: B
- Touches: N6, N2
- Summary: Tests 14 LLMs from seven families with four prompting techniques on 54 Solidity contracts, including contracts verified to be clean. Six frontier models report no false positives on the clean contracts, while all three small open-source models report vulnerabilities in every case. Turning on extended thinking dropped one model's F1 by 11.5%. The choice of model matters more than the prompting strategy.
- Delta: It measures LLM detection on Solidity, including clean code, which is what the project's LLM review does on human and agent code in the control group. The project adds PoV confirmation of every reported flaw and compares the human and agent versions of the same function. This is a small single-author preprint with 54 contracts.

### Hu2023-GPTLens Large Language Model-Powered Smart Contract Vulnerability Detection: New Perspectives
- Authors: Sihao Hu et al. (with Tiansheng Huang, Fatih İlhan, Selim Furkan Tekin and one more); Year: 2023; Venue: IEEE TPS-ISA 2023 (per the arXiv journal reference); arXiv 2310.01152
- URL opened: https://arxiv.org/abs/2310.01152 (arXiv abstract record via the export API)
- Status: VERIFIED
- Tier: B
- Touches: N6
- Summary: Generating more answers at higher randomness raises the chance that GPT-4 finds the true vulnerability, but also adds false positives. GPTLens splits detection into two stages with the LLM in two roles: an auditor that proposes many candidate vulnerabilities and a critic that judges them to remove false positives. Reports clear gains over one-stage detection.
- Delta: GPTLens filters LLM-reported flaws with a second LLM. The project instead requires an executable PoV to confirm each reported flaw, which removes false positives that a critic may keep and gives evidence a reader can rerun.

### Li2025-Flashboom Make a Feint to the East While Attacking in the West: Blinding LLM-Based Code Auditors with Flashboom Attacks
- Authors: Xiao Li et al. (with Yue Li, Hao Wu, Yue Zhang, Kaidi Xu, Xiuzhen Cheng, Sheng Zhong, Fengyuan Xu); Year: 2025; Venue: IEEE S&P 2025, pp. 576–594
- URL opened: https://api.openalex.org/works/doi:10.1109/sp61157.2025.00125 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N6
- Summary: Inserting code snippets that draw the model's attention pulls LLM vulnerability auditors away from real vulnerable code. The automated system builds such decoys and reaches blinding success rates of up to 96.3% on CodeLlama and 83.05% on Gemma, with transfer across models and languages. In a case study, GitHub Copilot missed a critical blockchain vulnerability.
- Delta: It shows that an LLM reviewer's misses depend on what else is in the code. Agent-written and human-written versions of a function differ in style and length, so the project's LLM review might miss flaws more often in one of them. PoV confirmation removes false positives but not misses, so the project should compare miss rates using findings with known PoVs.

### Luo2024-JSGo Test Suites Guided Vulnerability Validation for Node.js Applications
- Authors: Changhua Luo et al. (with Penghui Li, Wei Meng, Chao Zhang); Year: 2024; Venue: ACM CCS 2024, pp. 570–584
- URL opened: https://www.semanticscholar.org/paper/25ed59d77f9b63b95a595cdf2110379c37fa82d9 (Semantic Scholar record via the API with full abstract)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: N6
- Summary: JSGo uses an application's existing test suites, which cover on average 85% of the code in their study, to build end-to-end inputs that validate reported vulnerabilities, with trace-guided mutation based on concolic execution. It reproduces 20 of 26 known vulnerabilities, 10 to 12 more than Restler, Miner, Witcher and Burp, and validates seven static-analysis findings in popular apps, two of which were then patched.
- Delta: It confirms reported vulnerabilities with executable inputs, which is the step the project takes when a PoV must confirm each flaw an LLM reviewer reports. JSGo automates this for Node.js web apps; the project writes PoVs by hand in Foundry for smart contracts.

### Gong2026-RcAudit Evidence-Grounded Logic Vulnerability Detection for Smart Contracts via Runtime Context Reasoning
- Authors: Guang Gong et al. (7 authors); Year: 2026; Venue: ASE 2026, pp. 2216–2228
- URL opened: https://api.openalex.org/works/doi:10.1145/3832783.3837471 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N6, N2
- Summary: Many logic flaws in smart contracts appear only in certain contract states, so code-only LLM auditing gives false positives and misses. RcAudit builds a knowledge base of contract behaviour, uses state- and intent-aware fuzzing to produce runtime contexts, and has the LLM reason over contexts where behaviour and intent seem to disagree. It finds 74 of 132 known logic vulnerabilities with 96.9% precision, 117.6% more than the strongest baseline, and 22 zero-days.
- Delta: It grounds LLM auditing of Solidity logic flaws in runtime states, an automatic relative of the project's PoV confirmation. It audits human code only and does not compare human and agent versions of the same function.

### Dozono2025-OSSContamination Should We Evaluate LLM Based Security Analysis Approaches on Open Source Systems?
- Authors: Kohei Dozono et al. (with Jonas Engesser, Benjamin Hummel, Tobias Roehm, Alexander Pretschner); Year: 2025; Venue: ASE 2025, pp. 3216–3226
- URL opened: https://api.openalex.org/works/doi:10.1109/ase63991.2025.00265 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N6; design validity of N1
- Summary: Five frontier LLMs detect vulnerabilities on CWE-Bench-Java (open source) and on TS-Vuls (a closed commercial codebase). Mean F1 drops by about 20 points from open to closed code, and precision falls from 56% to 34% (significant for four of five models). A split of the open data by CVE date is inconclusive, so a knowledge cut-off may reduce contamination but does not remove it.
- Delta: The project chooses models whose training data ends before the findings were published. This paper warns that a cut-off date alone may not remove contamination. In the project's case the audited code, including the buggy function, was public before the finding, so a model could reproduce the human's bug from memory. The project should measure how similar each agent version is to the human's code. The paper studies detection, not code writing or repair.

## New entries: smart contracts, exploits and losses (N2, N7)

### Eshghie2024-XploGen Oracle-Guided Vulnerability Diversity and Exploit Synthesis of Smart Contracts Using LLMs
- Authors: Mojtaba Eshghie, Cyrille Artho; Year: 2024; Venue: ASE 2024, pp. 2240–2248
- URL opened: https://api.openalex.org/works/doi:10.1145/3691620.3695292 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N2
- Summary: Smart-contract analysis tools are often evaluated on ground truth taken from other tools' verdicts, on low-level bugs such as reentrancy and overflow, and without concrete exploits. XploGen uses a model-based specification of the contract's business logic as an oracle and LLMs to synthesize valid exploits. On 104 synthesized vulnerability-exploit pairs it exploits the targeted aspect 57% of the time, with 3.5 transactions per exploit on average.
- Delta: It also wants exploit-based ground truth for business-logic flaws. Its vulnerabilities are synthesized variants, while the project's come from audit findings in real projects and are judged against the human's own code.

### Zhang2026-SPSYN SPSYN: Synthesizing DeFi Price-Manipulation Exploits via Semantic Recovery and State-Guided Search
- Authors: Bosi Zhang et al. (with Ningyu He, Guangdong Bai, Haoyu Wang); Year: 2026; Venue: ASE 2026, pp. 2843–2855
- URL opened: https://api.openalex.org/works/doi:10.1145/3832783.3837520 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N7, N2
- Summary: An LLM recovers the roles of victim functions, and a state-guided search on a concrete chain snapshot builds and checks price-manipulation exploits. On 29 historical incidents it finds profitable exploits for 27 (93.1%), against 11 for ItyFuzz, 19 for CPMMX and 7 for FlashSyn, with a median of 114 seconds to the first one. On Ethereum and BNB Smart Chain it finds 9 new profitable vulnerabilities with $35.1K potential profit.
- Delta: It measures exploitability as profit on a real chain state, which is close to the project's per-exploit loss estimate. SPSYN searches for exploits of one bug class; the project starts from audit-confirmed findings and extends hand-adapted PoVs to measure who loses how much.

### Babel2023-Lanturn Lanturn: Measuring Economic Security of Smart Contracts Through Adaptive Learning
- Authors: Kushal Babel et al. (with Mojan Javaheripi, Yan Ji, Mahimna Kelkar, Farinaz Koushanfar, Ari Juels); Year: 2023; Venue: ACM CCS 2023, pp. 1212–1226
- URL opened: https://www.semanticscholar.org/paper/13a6bcc5ac7d393a964b5c4bfefb286ba4aad4f8 (Semantic Scholar record via the API with full abstract)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: N7
- Summary: Lanturn treats value extraction from composed DeFi contracts as black-box optimization and learns strategies made of concrete transactions, run in a simulator on real chain state and bytecode. On Sushiswap, Uniswap V2 and V3 and Aave V2 it rediscovers known strategies, finds undocumented ones, and extracts more value than bots did in the wild.
- Delta: Lanturn estimates the most value an attacker can take; the project measures the loss caused by a given PoV and who bears it. Lanturn could serve as an upper bound check on the project's loss numbers. It has nothing on code written by agents.

### Ye2024-Midas Midas: Mining Profitable Exploits in On-Chain Smart Contracts via Feedback-Driven Fuzzing and Differential Analysis
- Authors: Mingxi Ye et al. (with Xingwei Lin, Yuhong Nan, Jiajing Wu, Zibin Zheng); Year: 2024; Venue: ISSTA 2024, pp. 794–805
- URL opened: https://api.openalex.org/works/doi:10.1145/3650212.3680321 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N7, N2
- Summary: A fuzzing framework that generates valid transactions through complex call chains and uses differential analysis to decide whether a transaction is profitable for the attacker. It identifies 40 real-world exploits with 80% precision, beats ItyFuzz and Slither, and finds five unknown exploits, two confirmed by developers.
- Delta: Its differential analysis of who gains decides profitability, which is the measurement the project needs to state each exploit's loss. Midas searches for exploits; the project measures given ones.

### Sun2025-FairChecker FairChecker: Detecting Fund-Stealing Bugs in DeFi Protocols via Fairness Validation
- Authors: Yi Sun et al. (with Zhuo Zhang, Xiangyu Zhang); Year: 2025; Venue: ICSE 2025, pp. 1307–1319
- URL opened: https://api.openalex.org/works/doi:10.1109/icse55347.2025.00134 (OpenAlex record with full abstract)
- Status: VERIFIED (abstract read in the OpenAlex record)
- Tier: B
- Touches: N2
- Summary: In DeFi, the direction of change in a user's assets or debt must follow fairness rules; a bug that lets an attacker gain without cost breaks them. FairChecker detects such bugs with inter-procedural, inter-contract static analysis using symbolic execution and an SMT solver. On 113 real DeFi protocols with 34 such bugs it finds 32 (recall 94.1%, precision 46.4%).
- Delta: It targets the accounting bugs that make up much of the project's findings. It detects them statically in human code; the project asks whether agents write them and confirms each with a PoV.

## New entries: wording of the request, and human against AI (N1, N5)

### He2026-VibeToSpec From Vibe to Spec: An Empirical Study to Demystify Specifications in Code Generation
- Authors: Ruirui He et al. (8 authors); Year: 2026; Venue: ASE 2026, pp. 2780–2792
- URL opened: https://www.semanticscholar.org/paper/034a32db118dc3cd00a82cdbb756c58ba6816012 (Semantic Scholar record via the API with full abstract)
- Status: VERIFIED (abstract read in the Semantic Scholar record)
- Tier: B
- Touches: N5
- Summary: Five medium-sized projects in several languages; specifications in three forms (natural language, coarse pseudocode, fine pseudocode) and four granularities (line, function, module, project); code from GPT-5, DeepSeek-V3.1 and Qwen-3.7 scored with text similarity, tests and human-centred measures. Fine-grained structured pseudocode makes generation more stable and better; module-level specifications give the best balance of quality, stability and token cost.
- Delta: It varies how the request is written and measures functional quality. The project varies whether the request describes the human's design or states the rule the fix restores, and measures security with exploits. None of the specification forms here carries security rules.

### Deaconu2026-InfluenceTactics Do influence tactics matter? investigating prompt framing effects in LLM code generation
- Authors: Alexandrina (Alex) Deaconu et al. (with Anubhav Gupta, Manaal Basha, Nicholas Haydu and one more); Year: 2026; Venue: Empirical Software Engineering 32, article 13 (per the arXiv journal reference); arXiv 2608.11513
- URL opened: https://arxiv.org/abs/2608.11513 (arXiv abstract record via the export API); https://www.semanticscholar.org/paper/f962d4c80acd830995e4167e364f21b8bbf8cf2d (journal record)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: Turns eight influence tactics from Yukl and Falbe's taxonomy, such as rational persuasion, ingratiation and exchange, into prompt templates. Five open-weight LLMs on LiveCodeBench and SWE-bench Verified are scored on correctness, quality, maintainability and security. Framings that stress urgency go with lower correctness and security.
- Delta: It shows that wording outside the technical content can change security. The project must keep the tone of its feature requests fixed across tasks and setups, so that only the content (design described or rule stated) varies.

### Li2026-UsabilityWeapon Usability as a Weapon: Attacking the Safety of LLM-Based Code Generation via Usability Requirements
- Authors: Yue Li et al. (with Xiao Li, Hao Wu, Yue Zhang and four more); Year: 2026; Venue: arXiv preprint (2605.10133)
- URL opened: https://arxiv.org/abs/2605.10133 (arXiv abstract record via the export API)
- Status: VERIFIED
- Tier: B
- Touches: N5
- Summary: Security requirements are often implicit while usability requirements are explicit. U-SPLOIT picks tasks where a model is secure, adds realistic usability pressure (new features, performance or simplicity demands), and checks for security regressions with tests and generated exploit payloads. On 75 seed scenarios (25 CWEs, three cases each) in Python, C and JavaScript, attacks succeed up to 98.1% of the time on models such as GPT-5.2-chat and Gemini-3-Flash-Preview.
- Delta: Like the project's pilot, where the wording of the request decided the outcome, it shows that explicit feature demands can override implicit security. It builds the pressure on purpose as an attack; the project writes neutral requests from the human's feature and checks that they do not hint at the bug or the fix.

### Molison2025-LLMvsHuman Is LLM-Generated Code More Maintainable & Reliable Than Human-Written Code?
- Authors: Alfred Santa Molison et al. (with Marcia Moraes, Glaucia Melo, Fabio Santos and one more); Year: 2025; Venue: ESEM 2025; arXiv 2508.00700
- URL opened: https://arxiv.org/abs/2508.00700 (arXiv abstract record via the export API); https://www.semanticscholar.org/paper/3dddfea28ea1831157269813e6fde4f935f5facc (ESEM record)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: Compares LLM-generated and human-written Python solutions at three difficulty levels (introductory, interview, competition) under zero-shot, few-shot and fine-tuned setups, scored with SonarQube. LLM code has fewer bugs and needs less effort to fix overall; fine-tuning moves high-severity issues to lower severity but lowers performance; at competition level LLM solutions sometimes add structural issues absent from human code.
- Delta: It compares LLM and human solutions to the same tasks, as N1 does, but on standalone programming problems with static-analysis metrics. The project compares on real smart-contract features from the same starting code, judges with exploits, and has a control group of functions the human wrote correctly.

### PaxtonFear2026-SemgrepSusVibes Claude Opus 5.5 Writes Working Code but Only Half of It Is Secure
- Authors: Katie Paxton-Fear; Year: 2026 (29 September); Venue: Semgrep blog (grey literature)
- URL opened: https://semgrep.dev/blog/2026/claude-opus-5-5-susvibes-benchmark (blog page)
- Status: VERIFIED
- Tier: C
- Touches: N1, N5 (background)
- Summary: Runs Claude Opus 5.5 on the 186 SusVibes tasks (re-implement a deleted feature in a real Python project, judged on tests and on the original CVE). 93.5% of solutions work, but only 54.8% are working and secure; 72 of 174 working solutions (41%) keep the original vulnerability. About 53% of solutions are identical or nearly identical to the real project code, and those memorised solutions are secure 64% of the time against 51% for the others. The post notes that the SusVibes task text carries a one-line generic security reminder, which is already a hint. (Numbers taken from the page as read through WebFetch.)

## Unverified

### Solca2026-LeniencyConfound Who Judges the Judges? The Leniency Confound in LLM-as-Judge Evaluation of Cybersecurity Tasks
- Authors: Robert Nicolae Șolcă, Titus Bălan; Year: 2026; Venue: IEEE Access (DOI 10.1109/ACCESS.2026.3739942; IEEE document 11719568)
- URL opened: https://scholar.google.com/scholar?q=%22Who+Judges+the+Judges%3F+The+Leniency+Confound%22 (Google Scholar result with only the first sentences of the abstract). The IEEE page https://ieeexplore.ieee.org/document/11719568/ and its PDF returned a bot check; Semantic Scholar and OpenAlex have no abstract.
- Status: UNVERIFIED (full abstract not reachable)
- Tier: B (tentative)
- Touches: N6
- Summary: Only the opening is visible: LLMs increasingly score other LLMs' outputs, including in security settings, and the authors present an audit using only open-weight models on cybersecurity tasks. The title says it studies how judge leniency confounds such evaluations. Nothing more can be said without the abstract.

### Gupta2026-Patchproof Patchproof: Exploit-grounded Evidence for Security Patch Correctness
- Authors: Arnav Gupta; Year: 2026 (June); Venue: SSRN preprint (abstract ID 7254143)
- URL opened: https://scholar.google.com/scholar?q=%22Patchproof%22+exploit-grounded+evidence+security+patch+correctness (Google Scholar snippet only). The SSRN page and PDF returned HTTP 403.
- Status: UNVERIFIED (full abstract not reachable)
- Tier: B (tentative)
- Touches: N3, N6
- Summary: From the snippet only: the paper proposes an exploit-grounded benchmark and evidence standard for judging security patches, argues that common repair metrics do not show that the attacker's behaviour has been removed, and says that running it and measuring results is future work. If confirmed, it is a proposal without results, close in spirit to N3.

### Zhang2026-PatchAudit PatchAudit: Uncovering Faulty Security Patches and Lingering Zero-Days at Scale
- Authors: Zhengsong Zhang, Haipeng Cai and possibly others (University at Buffalo, SUNY; I read only the first two names on the list); Year: 2026; Venue: ACM CCS 2026 (accepted paper)
- URL opened: https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html (accepted-papers list with title and authors only)
- Status: UNVERIFIED (no abstract online yet; not on arXiv, Crossref or Semantic Scholar)
- Tier: B (tentative)
- Touches: N3
- Summary: Not available. The title says it finds faulty security patches, and vulnerabilities that remain after them, at scale. Worth reopening once the CCS 2026 proceedings are online.

### Xiang2026-FixToFlaw From Fix to Flaw: Understanding and Revealing Incomplete Patches for Link Following Vulnerabilities
- Authors: Bocheng Xiang, Yuan Zhang and possibly others (Fudan University; I read only the first two names on the list); Year: 2026; Venue: ACM CCS 2026 (accepted paper)
- URL opened: https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html (accepted-papers list with title and authors only)
- Status: UNVERIFIED (no abstract online yet)
- Tier: C (tentative)
- Touches: N3 (background)
- Summary: Not available. The title says it studies incomplete patches for link-following (symlink) vulnerabilities.

(Eick et al. 1992 is also UNVERIFIED; its block is in the statistical design section above.)

## Leads not followed

- AIxCC "AFC Procedures and Scoring Guide Version 2.0" (aicyberchallenge.com, June 2025). Seen in the L6 lead list. The official document did not come up in search. Its scoring rules are summarised in the indexed AIxCC SoK (Zhang2026-SoKAIxCC) and in the FuzzingBrain (arXiv 2509.07225) and ATLANTIS (arXiv 2509.14589) papers, seen in a WebSearch result.
- Falessi, Di Penta, Canfora, Cantone, "Estimating the number of remaining links in traceability recovery", Empirical Software Engineering 22(3), 2017 (DOI 10.1007/s10664-016-9460-6). I looked it up as a possible modern capture-recapture use. No abstract reached (Semantic Scholar and OpenAlex have none; the university page returned 403). A search snippet says it uses machine-learning estimators, not capture-recapture.
- Capture-recapture papers seen in Crossref with no abstract reached: Thelin and Runeson, "Confidence intervals for capture–recapture estimations in software inspections", IST 2002; Chun, "Estimating the number of undetected software errors via the correlated capture–recapture model", EJOR 2006 (directly about dependent reviewers); Runeson and Wohlin, experience-based capture-recapture, EMSE 1998; Wohlin, Runeson and Brantestam, STVR 1995; Miller, "Estimating the number of remaining defects after inspection", STVR 1999; Walia and Carver, ISSRE 2008 and ICST 2009; Kamel and Sorenson, log-linear models, ISESE 2003; Briand et al., ISSRE 1997; Gary and Doran, capture-recapture in IBM Jazz, 2011/2012.
- Wang et al., "Effective Automated Decision Support for Managing Crowdtesting" (arXiv 1805.02744). Companion of the crowdtesting block above; seen in the arXiv capture-recapture search.
- "An Upper Bound on the Probability That a User Encounters an Undiscovered Defect" (arXiv 2607.17061). Seen in a WebSearch result; it critiques defect counts such as capture-recapture estimates.
- Ozment and Schechter, "Milk or Wine: Does Software Security Improve with Age?", USENIX Security 2006. Cited in Geer 2015 as a removal-capture view of OpenBSD vulnerabilities.
- Alexopoulos et al., "How long do vulnerabilities live in the code?", USENIX Security 2022. Seen in a Google Scholar result page; a vulnerability-lifetime study built on contributing commits, relevant to tracing.
- A University of Texas at Dallas study of 1,646 open-source CVEs with more than one linked patch (641 incomplete fixes), reported by Help Net Security on 23 July 2026. Paper not identified.
- Herzig, Just and Zeller, "It's not a bug, it's a feature: how misclassification impacts bug prediction" (ICSE 2013) and Croft et al., "Data Preparation for Software Vulnerability Prediction: A Systematic Literature Review" (TSE 2023). Known label-quality papers that came up while searching; not looked up.
- Dabic et al., "Sampling Projects in GitHub for MSR Studies" (MSR 2021). Seen in the stratified-sampling sweep; at most C.
- "Directing the Machine: A Single-Case Study of Verification When an AI Agent Cannot Reach the Oracle" (SSRN 2026). Seen in Crossref while looking for "The Oracle Is Mutable".
- EvoPoC (arXiv 2605.02868), DeFi exploit synthesis. Seen in a Semantic Scholar search result; belongs to the exploit-generation slice.
- CCS 2026 accepted papers seen on the accepted-papers list and not checked: "The Deception Delta: Adversarial Evaluation of LLM-Based Smart Contract Bytecode Forensics" (N6-adjacent); "Reproducing Web Application Vulnerabilities with Patch-Guided Routing Inference and Sink Exploration"; "SPFUZZ: Validating Secretly Patched Vulnerabilities by Patch Guided Fuzzing".
