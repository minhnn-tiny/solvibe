<!--
claim_intent_manifests entry (ARS v3.8). This workspace has no Material Passport, so the manifest is kept here, before the first prose block. The orchestrator gave no manifest_id.
{
  "manifest_version": "1.0",
  "manifest_id": "unallocated: no orchestrator-issued id was provided",
  "emitted_by": "synthesis_agent",
  "emitted_at": "2026-10-21",
  "claims": [
    {"claim_id": "C-001", "claim_text": "No verified paper compares a coding agent with the human author of the same feature, from the same starting code, judged by the same executable exploit, with a control group of features the human wrote correctly in the same commit.", "intended_evidence_kind": "empirical", "planned_refs": ["Chen2026-SecureVibeBench", "Zhao2026-SusVibes", "Asare2023-CopilotVsHumans", "Chen2026-SolAgent"]},
    {"claim_id": "C-002", "claim_text": "Executable exploits built from Solidity audit findings are prior art; agent-written Solidity features judged by such exploits are not.", "intended_evidence_kind": "empirical", "planned_refs": ["Andersson2025-PoCo", "Wang2026-EVMbench", "Chen2025-SmartPoC"]},
    {"claim_id": "C-003", "claim_text": "Judging repairs with exploits or tests the repairer never saw is prior art; the project is new only for Solidity audit findings, a shown PoV with held-out PoVs written from the audit report, and funds lost.", "intended_evidence_kind": "empirical", "planned_refs": ["Iranmanesh2026-P2Patch", "Shen2026-PatchBench", "Yu2026-PVBench", "Wang2026-SlicePatch", "Smith2015-CureWorse"]},
    {"claim_id": "C-004", "claim_text": "No verified paper crosses repair input with execution access for coding agents on security repair judged by held-out exploits, and none studies repository tests that assert the vulnerability during repair.", "intended_evidence_kind": "empirical", "planned_refs": ["Le2026-PatchingBenchReliability", "Lin2026-ToRunOrNotToRun", "Mierczuk2026-FLAWED", "Zhong2026-ImpossibleBench", "Charoosaei2026-FaultEnforcingTests"]},
    {"claim_id": "C-005", "claim_text": "Checks of request wording exist; no verified paper measures how a request that describes the human's design and a request that states the restored rule change the outcome.", "intended_evidence_kind": "empirical", "planned_refs": ["Wu2026-LastSecureCode", "Zhao2026-SusVibes", "Chen2026-SecureVibeBench"]},
    {"claim_id": "C-006", "claim_text": "Execution-confirmed findings are prior art; the same LLM review run on agent and human versions of one function, with every flaw confirmed by a PoV, is not reported.", "intended_evidence_kind": "empirical", "planned_refs": ["Kong2026-Knowdit", "Chen2025-SmartPoC", "Chen2026-SecureVibeBench"]},
    {"claim_id": "C-007", "claim_text": "Exploit value is measured in many papers; a per-party loss estimate for each exploit, including residual theft after a repair, is not reported.", "intended_evidence_kind": "empirical", "planned_refs": ["Xiao2025-SCONEbench", "Gervais2025-A1", "Huang2026-CyberChainBench"]},
    {"claim_id": "C-008", "claim_text": "The five papers most dangerous to novelty are SecureVibeBench, EVMbench, P2Patch, PatchBench and the patching-benchmark reliability study.", "intended_evidence_kind": "empirical", "planned_refs": ["Chen2026-SecureVibeBench", "Wang2026-EVMbench", "Iranmanesh2026-P2Patch", "Shen2026-PatchBench", "Le2026-PatchingBenchReliability"]},
    {"claim_id": "C-009", "claim_text": "Round 3 still produced new tier A papers, so tier A is not saturated for N3 and N4.", "intended_evidence_kind": "empirical", "planned_refs": ["Wang2026-SlicePatch", "Ruan2024-EvoRepair", "Talha2026-SNRA"]}
  ],
  "manifest_negative_constraints": [
    {"constraint_id": "MNC-1", "rule": "No novelty claim rests on an UNVERIFIED paper."},
    {"constraint_id": "MNC-2", "rule": "No claim that the search was exhaustive."},
    {"constraint_id": "MNC-3", "rule": "No fact or number that the search files do not report."}
  ]
}
-->

# Literature review: are AI coding agents' Solidity features less secure than the human's, and do exploits help agents repair them?

Written on 21 October 2026 from the search files of rounds 1 to 3. Round 4 is still running. Its results will go into section 3.4.

Every fact below comes from a search file. Numbers are copied as the files give them. Each paper carries its venue and year. Appendix C gives the URL each search agent opened. A paper that no agent could verify never supports a claim here; it appears only in section 7.

---

## 1. Scope

The project asks two questions. Do AI coding agents write Solidity smart-contract code that is more or less secure than the code of the human developer who wrote the same feature? Does an executable exploit, a proof of vulnerability (PoV), help an agent repair a vulnerability properly?

The search checked the novelty of seven ideas from the project brief (`lit/project_brief.md`):

- **N1.** The agent and the human write the same feature from the same starting code, and the same executable exploit judges both. A control group holds features the human wrote correctly.
- **N2.** The tasks are Solidity DeFi code: business-logic and accounting bugs, executable exploits, and losses in funds.
- **N3.** Held-out PoVs judge repairs, and the agent sees one PoV as a failing test.
- **N4.** Repair success is measured while two inputs change: what the agent is told and what it can run. This includes repository tests that encode the vulnerable behaviour, and agents that fit the shown test.
- **N5.** Feature requests hint at neither the bug nor the fix, and a check confirms this.
- **N6.** The same LLM security review runs on agent code and human code, and an executable test must confirm each reported flaw.
- **N7.** Each exploit's financial loss is estimated.

---

## 2. Search method

### 2.1 Sources and dates

All searches ran on 21 October 2026. Agents used WebSearch and public APIs: DBLP, the arXiv API and arXiv search pages, the Semantic Scholar Graph API (keyword search, bulk search, citations and references), OpenAlex and Crossref. Some agents also used Google Scholar result pages, the OpenReview search API, the accepted-paper lists of 2026 venues, a local copy of the DBLP XML dump, the GitHub API, the DeFiLlama API and Zenodo. All requests were anonymous.

### 2.2 The four rounds

- **Round 1** split the field into 11 slices, one agent each (L1 to L11; Appendix B lists the files). Nine slices were topics. L9 swept venues instead: it ran title queries on a local copy of the DBLP dump (68,288 papers from the target venues, release of 2026-10-20) and on 2026 accepted-paper lists that DBLP had not indexed. L11 checked leads that a separate Codex search had produced.
- **Round 2** had four agents. S1 snowballed from 15 anchor papers through Semantic Scholar citations and references and OpenAlex citing works. S2 searched for tests and comments that assert buggy behaviour, and it confirmed the meaning of "fault-enforcing test". S3a and S3b followed the leads that round 1 could not check, which the round-1 leads list (`lit/leads_round1.md`) gathers. S3b also swept for capture-recapture, case-control and selection-bias papers.
- **Round 3** tested saturation with new wording. T1 to T4 repeated four topics: human against AI, smart contracts in 2026, repair with execution, and requests, judges and differential testing. T5 screened 16 accepted-paper lists of 2026 and 2027 venues. C1 is a Codex search for gaps; its file is a normalised copy of the raw Codex output.
- **Round 4** is still running.

Each round compared its finds with the current index, so that only papers not yet indexed counted as new. The merged index (`lit/master_index.tsv`) now holds 861 rows, one per distinct title. Its tier is the best tier any file gave.

### 2.3 Verification rule

The search protocol (`lit/search_protocol.md`) counts a paper as VERIFIED only if the agent opened a page that shows the title, the authors and the abstract: the arXiv abstract page, a publisher page, or the PDF. The agent records the URL it opened. A search snippet is not enough. A paper with no such page is UNVERIFIED, and the file says why. Venues are copied as published, and "arXiv preprint" is used when no peer-reviewed version was found.

The agents applied the rule in two ways when publisher pages were blocked. S1, L1, L3, L4, L6, L7 and T5 did not accept index records. S3a, S3b, four L9 entries and the short tier C list in L5 accepted a Semantic Scholar, OpenAlex or Crossref record when it carried the abstract. Section 8 lists the papers this affects.

### 2.4 Queries and records

The files log about 1,480 query rows. A row is what a file numbers as one query; many rows are failed calls, retries, or look-ups made only to verify a paper.

| Round | File | Query rows logged | Totals stated in the file |
|---|---|---|---|
| 1 | L1, secure code generation | 80 | 91 papers kept |
| 1 | L2, repository and agent benchmarks | 70 | 93 papers kept |
| 1 | L3, human against AI | 62 | 69 papers kept: 6 tier A, 34 tier B, 29 tier C; 3 unverified |
| 1 | L4, Solidity code generation | 64 numbered queries | 57 papers kept: 7 tier A, 19 tier B, 31 tier C; 12 unverified |
| 1 | L5, smart-contract exploits and datasets | 54 | not stated |
| 1 | L6, repair guided by an exploit | 54 | not stated |
| 1 | L7, smart-contract repair | 77 | not stated |
| 1 | L8, methodology | 179 | 138 papers kept: 7 tier A, 79 tier B, 52 tier C |
| 1 | L9, DBLP venue sweep | 54 | 1,617 distinct titles screened; 134 kept: 9 tier A, 48 tier B, 77 tier C; 8 unverified |
| 1 | L10, real-world significance | 57 | 41 entries, 27 of them grey literature |
| 1 | L11, Codex leads | 40 | not stated |
| 2 | S1, snowballing | 45 | 1,240 Semantic Scholar records and 157 OpenAlex records; 56 papers added (11 tier B, 45 tier C) |
| 2 | S2, tests that assert bugs | 70 | not stated |
| 2 | S3a, leads, first half | 106, one per lead | 110 leads already indexed, 133 screened out, 22 new |
| 2 | S3b, leads, second half | 190 | not stated |
| 3 | T1, human against AI | 74 (71 returned results) | 3 new tier B |
| 3 | T2, smart contracts 2026 | 67 | hits per query; 8 new tier B |
| 3 | T3, repair and execution | 41 (37 returned results) | 4 new tier B |
| 3 | T4, requests, judges, differential testing | 57 rows covering 68 attempts (52 returned results) | about 400 hits looked at; 12 new tier B |
| 3 | T5, 2026 venue lists | 16 venue lists and 8 look-up rows | titles screened per list, for example 6,646 for ICML 2026 |
| 3 | C1, Codex gap search | 19 | most hit counts marked uncertain; 15 new papers |

### 2.5 Access limits

- **DBLP.** The search API returned HTTP 429 and then a bot-check page to every agent in every round. L9 worked around this with the DBLP XML dump, and T1 reused that dump.
- **OpenAlex.** The free daily budget ran out early in round 1. Some OpenAlex replies asked the agent to register an API key with a personal email address. No agent did this, because the protocol forbids sending any personal identifier. Look-ups of single records by DOI kept working.
- **Semantic Scholar.** Keyword search mostly returned HTTP 429. The citations, references and bulk-search endpoints worked at times, and they carried the snowballing.
- **arXiv.** The API was throttled (HTTP 429 and 503). Agents used arXiv abstract pages and the arXiv search page instead. T2 notes that the API stems "Solidity" to "solid".
- **Web search.** A budget shared by all agents ran out during round 1. L8 gives it as 200 calls per session.
- **Publishers.** The ACM Digital Library returned HTTP 403. IEEE Xplore returned empty pages, a bot check or HTTP 418. Springer, ScienceDirect, SSRN and MDPI returned HTTP 403 or a script challenge. Agents then used arXiv versions, author PDFs, programme pages or index records.
- **Other services.** Google Scholar served about 20 result pages and then a CAPTCHA (T1). OpenReview forum pages needed a browser check, but its search API worked. The ACL Anthology site search needs JavaScript.
- **Pages with instructions.** A Code4rena documentation page and several OpenAlex replies contained text addressed to AI agents. Agents treated it as data and did not act on it.

---

## 3. Saturation evidence

### 3.1 New tier A and tier B papers per round and per agent

For round 1, every kept paper was new, so the table gives each file's own tier A and tier B blocks. These overlap: SusVibes, for example, appears in five round-1 files. For rounds 2 and 3, "new" means not yet in the index when the round ran, and the tier is the file's own rating.

| Round | Agent | New tier A | New tier B | Saturation, as the file reports it |
|---|---|---|---|---|
| 1 | L1 | 7 | 30 | Reached: ten completed queries in a row gave nothing new |
| 1 | L2 | 8 | 35 | Tier A and B stopped growing at query 66; tier C kept appearing |
| 1 | L3 | 6 | 34 | Queries 58 to 62 gave nothing new |
| 1 | L4 | 7 | 19 | The last seven queries gave nothing new |
| 1 | L5 | 14 | 45 | Queries 50 to 54 gave no new Solidity paper |
| 1 | L6 | 15 | 48 | Three empty queries in a row; one planned query did not run |
| 1 | L7 | 4 | 24 | The last three completed queries gave nothing new |
| 1 | L8 | 7 | 79 | Met for most sub-areas; not strictly met on arXiv for held-out tests and LLM judges |
| 1 | L9 | 9 | 48 | Close to saturation in the swept venues; 2026 lists added 4 of its 9 tier A papers |
| 1 | L10 | 1 | 9 | Not saturated for audit-contest studies and for surveys of Solidity developers |
| 1 | L11 | 7 | 16 | No stop rule stated |
| 1 | **Distinct, from the index** | **44 rows (43 papers)** | **276 rows** | |
| 2 | S1 | 0 | 11 | Saturated for tier A; not for tier B; its last anchors still gave 3 tier B papers. S1 rated four papers C that other files rated B, and it rated Opad C. |
| 2 | S2 | 0 | 16 | Queries 68 to 70 gave nothing new |
| 2 | S3a | 1 (DeFiSent) | 20 | No stop rule (lead list). S3a counts 21 tier B, but one of them, TestPrune, was already indexed under its later title |
| 2 | S3b | 1 (TerraProbe) | 50 | No stop rule (lead list and sweeps); 3 of the 50 are unverified |
| 2 | **Distinct, from the index** | **3** | **89 (5 unverified)** | The third tier A paper is Opad, which S1 found and C1 later rated A |
| 3 | T1 | 0 | 3 | The last 13 rows gave nothing new |
| 3 | T2 | 0 | 8 | Queries 55 to 67 gave nothing new |
| 3 | T3 | 0 | 4, plus 1 re-rated | The last 7 queries that returned results gave nothing new |
| 3 | T4 | 0 | 12 | Of 21 rows after row 36, only row 47 gave a new paper |
| 3 | T5 | 1 (SlicePatch) | 6 (1 unverified) | ICSE 2027 and NDSS 2027 lists were not online; EMNLP 2026 workshops not screened |
| 3 | C1 | 2 new (SNRA, EvoRepair), plus Opad re-rated | 12 | No stop rule stated |
| 3 | **Distinct, from the index** | **3** | **41 rows (1 re-rated, 1 unverified)** | |

### 3.2 What the counts show

Tier A is not saturated. Round 2 added three tier A papers and round 3 added three more. All six touch N3 or N4, except one round-3 paper on N1. SlicePatch (IEEE S&P 2026) judges LLM repairs with attack variants beyond the shown proof of concept. EvoRepair (ICST 2024) and Opad (ESEC/FSE 2017) come from the older program-repair literature on patch overfitting. The N1 paper, SNRA, is an unpublished manuscript.

These areas were still producing tier B papers at the end of round 3:

- **LLM tools that audit smart contracts.** C1 added six. T2 applied a stricter rule, under which such a tool is tier B only if it confirms findings by running them, and it rated several of the same tools C. So this count depends on the tier rule.
- **Wording of task descriptions and prompts.** T4 found six new tier B papers in this part of its topic.
- **Differential testing and equivalence checking for Solidity.** T4 found four new tier B items, two of them grey literature. T4 calls this part the least covered before round 3.
- **Test generation and overfitting in program repair.** C1 found two tier A and four tier B papers here.
- **2026 venues still being published.** T5 found a tier A paper at IEEE S&P 2026 and a tier B paper in the EMNLP 2026 programme.

These areas looked saturated: comparisons of human and AI code (T1), contamination and time-split evaluation (T4), and LLM work on smart contracts under T2's rule.

### 3.3 Known limits of the saturation evidence

Semantic Scholar was throttled for most of rounds 1 and 3, so forward snowballing from the newest papers was thin. DBLP's live API was never usable. Several 2026 venue lists were not online. Round-1 counts overlap between agents, so they show effort, not distinct finds.

### 3.4 Round 4

Round 4 ran narrow searches in the three areas where round 3 still found papers. Each agent reported only papers missing from the merged index.

| Agent | Topic | Queries | New tier A | New tier B | Last queries with nothing new |
|---|---|---|---|---|---|
| U1 (`lit/r4_U1_patch_validation.md`) | Checking whether a security patch is complete: exploit variants, differential fuzzing, upgrade checks | 51 | 0 | 1 (PatchFuzz, Information and Software Technology 2026) | 38 queries after the last find |
| U2 (`lit/r4_U2_wording_exposure.md`) | Training exposure, prompt wording, agent pull requests | 42 | 0 | 5 (for example "Words Speak Louder Than Code", IEEE S&P 2027; FSTab; "Quality In, Quality Out", ICPC 2025) | last 14 queries |
| U3 (`lit/r4_U3_snowball_round3.md`) | Citations and references of eight round-3 papers | 22 anchor rows | 0 | 2 (FeedbackEval; PAIR-Bench) | last 4 anchors |

Round 4 found no tier A paper. It still found 8 tier B papers, all inside themes this review already covers, and none changes a delta in section 5. Under the strict rule (a full round with no new relevant paper), the search is not yet saturated for tier B. Round 5 runs fresh queries across all themes as a final check, and its result is added in section 3.5.

### 3.5 Rounds 5 and 6

| Agent | Topic | Queries or records | New tier A | New tier B |
|---|---|---|---|---|
| V1 (`lit/r5_V1_comparison_sc.md`) | AI versus human code; agents and Solidity; audit-contest benchmarks | 68 queries | 2 (both ICLR 2027 submissions: ConstraintDial; SysRepair-Bench) | 7 |
| V2 (`lit/r5_V2_repair_tests.md`) | Repair, execution, tests that encode bugs | 42 queries | 0 | 4 |
| V3 (`lit/r5_V3_method_judges.md`) | Requests, judges, contamination, tracing, sampling designs | 55 queries | 0 | 3 |
| W1 (`lit/r6_W1_iclr2027.md`) | Systematic scan of ICLR 2027 submissions (OpenReview API) | 60 terms, 21,131 records, 2,654 titles read | 5 | 18 |
| W2 (`lit/r6_W2_arxiv_recent.md`) | Every cs.SE and cs.CR arXiv title, 15 September to 20 October 2026 | 2,266 titles, 94 abstracts | 2 (one also in W1) | 12 |

**What rounds 4 to 6 show.** No round after round 3 found a tier A paper published before 2026. Every tier A paper found in rounds 5 and 6 is from August to October 2026, and seven of the eight are ICLR 2027 submissions under review or arXiv preprints from the last six weeks. The older literature is saturated. The newest literature cannot be saturated by more queries, because papers in this area appear every week. We therefore closed it by complete screens of fixed sources instead: every 2026 venue list that was online (round 3, T5), every cs.SE and cs.CR arXiv title from 15 September to 20 October 2026 (W2), and the ICLR 2027 submissions (W1, whose last 32 terms found nothing new). A monthly re-screen of new arXiv cs.SE and cs.CR titles is part of the study plan. The rule applied here is therefore narrower than "a full round of new queries finds no new relevant paper": it holds for papers before 2026 and for the screened sources, and new tier B papers in covered themes still appear at a low rate.

### 3.6 Tier A papers added in rounds 5 and 6

| Paper | Venue | Touches | Delta |
|---|---|---|---|
| Do Coding Agents Catch Their Own Bugs? (They Don't) (Foresight-SWE) | ICLR 2027 submission, under review | N1 | 212 pairs of human pull requests where the second fixes defects of the first; agents redo the first, and the "foresight resolve rate" (solve and avoid the defect) is 11.32% to 24.53% across eleven LLMs. It is the general-software version of measuring how often agents repeat human defects. Every sample is a human failure, so it has no human rate on a population with correct human code, no control group, and no exploit; it does not cover security or Solidity. |
| Between Spoilers and Guesswork: Avoiding Over-Specification in Coding Benchmarks | ICLR 2027 submission; arXiv 2610.22760 | N5 | Shows that hints taken from the ground truth leak the answer in SWE-bench Pro, FEA-bench, Doc2Feat-bench and Multi-SWE-bench, and recommends minimal hints. General coding, no security, no test of whether wording makes an agent write a vulnerability. |
| Coding Agents Can Deliver What You Check, Not What You Requested | ICLR 2027 submission | N4 | Two Copilot CLI agents rebuild a UI library; with the hidden 222-test oracle in the loop they reach a near-perfect score by building to the test. Varies access to the checking tests (18 runs). Not security, no repository tests that encode a bug. |
| Placebo Audits Quantify Audit-Specific Acceptance under Adaptive Reuse of Verifier Tests | ICLR 2027 submission | N3, N4 | An estimator for how much acceptance comes from fitting reused verifier tests, by re-running frozen outputs on fresh tests. A statistical method the repair study can use; no security or Solidity. |
| What You Don't Check, Models Don't Fix: False Completion under Partial Verification | ICLR 2027 submission | N3, N4 | Exposed and hidden deterministic checks in three non-code-security domains; the loop leaves hidden checks failing. Same measurement idea as held-out PoVs; no security. |
| SysRepair-Bench: Measuring Whether Agents Can Fix a Vulnerability Without Breaking the Service | ICLR 2027 submission | N4, N3 | 313 scenarios, each run with and without the vulnerability report; median success 90.0% with the report and 49.4% without; fixes that break the service are more common without it. Varies only the report; always a full shell; second check is service health, not held-out exploits; no Solidity. |
| Beyond Copying: Lifelong Smart Contract Security Task Construction via Protocol Mutation (ConstraintDial) | ICLR 2027 submission | N2, N3 | Mutates 203 public smart-contract cases so the public attack fails; success with the public answer drops by 10.9 points. A different control for memorization than training cutoffs; no human baseline, no feature writing. |
| Does AI Help Cyber Attackers or Defenders? Evidence from Nonpublic Vulnerabilities and Subsequent Attacks | arXiv 2610.06584 | N3 | In five nonpublic environments, after the first exploit is stopped another still succeeds in 92 of 524 defender intervals; uses unpublished vulnerabilities to rule out training exposure. General software; whether the second exploit is a fixed held-out test is not stated. |

Of these, Foresight-SWE is the most important for N1: the "agents repeat human defects" measurement now exists for general software as well as for security (SecureVibeBench). The project's claim on N1 must rest on the population that includes correct human code and on the decomposition into avoided and added vulnerabilities.

---

## 4. Thematic synthesis

### 4.1 Agent and LLM code security benchmarks built from real vulnerabilities

Benchmarks have moved from written scenarios to tasks rebuilt from real vulnerability history. BaxBench (Vero et al., ICML 2025)<!--ref:Vero2025-BaxBench--><!--anchor:section:abstract--> and CWEval (Peng et al., LLM4Code 2025)<!--ref:Peng2025-CWEval--><!--anchor:none:--> wrote their own tasks and judged them with exploits or outcome checks. The newer benchmarks remove real code and ask for it again. SecRepoBench (Shen et al., LLM4Code 2026)<!--ref:Shen2025-SecRepoBench--><!--anchor:none:--> masks the region that a developer's fix changed. SusVibes (Zhao et al., ICML 2026)<!--ref:Zhao2026-SusVibes--><!--anchor:section:Table%205--> masks a feature in the commit just before a fix. SecureVibeBench (Chen et al., ACL 2026)<!--ref:Chen2026-SecureVibeBench--><!--anchor:quote:in%20the%20exact%20real-world%20scenarios%20where%20human%20developers%20originally%20introduced%20vulnerabilities--> starts from the parent of the commit that introduced the vulnerability. Last Secure Code Benchmark (Wu et al., arXiv preprint 2026)<!--ref:Wu2026-LastSecureCode--><!--anchor:section:abstract--> removes the function that contains the vulnerable code.

The judges differ, and this matters. SecRepoBench and SecureVibeBench run a real crash input or PoV. SusVibes runs the security tests added in the fix commit. Last Secure Code Benchmark rewrote its tests so that each one drives a proof-of-concept attack. A.S.E (Lian et al., Findings of ACL 2026)<!--ref:Lian2026-ASE--><!--anchor:none:--> and RealSec-bench (Wang et al., Findings of ACL 2026)<!--ref:Wang2026-RealSecBench--><!--anchor:section:Table%202--> judge with static rules.

The results agree on one point: functionally correct code is often insecure. In SusVibes, the best setting passes the functional tests on 57.0% of tasks and the security tests on 11.8%; 79.3% of its correct solutions are insecure<!--ref:Zhao2026-SusVibes--><!--anchor:section:Table%205-->. In SecureVibeBench, the best setting writes correct and secure code in 23.8% of tasks<!--ref:Chen2026-SecureVibeBench--><!--anchor:section:Table%204-->. In Last Secure Code Benchmark, six agents pass 73.6% to 91.3% of tasks functionally but only 16.4% to 25.1% both functionally and securely<!--ref:Wu2026-LastSecureCode--><!--anchor:section:abstract-->. In BaxBench, exploits succeed on about half of each model's correct programs<!--ref:Vero2025-BaxBench--><!--anchor:section:abstract-->.

Agents also rewrite the specific vulnerability the human wrote. In SecureVibeBench, Claude Code wrote correct code that still contained the PoV-confirmed vulnerability in 26.7% of tasks, and Codex CLI in 21.8%<!--ref:Chen2026-SecureVibeBench--><!--anchor:section:Table%204-->. A vendor rerun of SusVibes found that 72 of 174 working solutions by Claude Opus 5.5 kept the original vulnerability (Paxton-Fear, Semgrep blog 2026; grey literature, tier C)<!--ref:PaxtonFear2026-SemgrepSusVibes--><!--anchor:none:-->.

Leakage and memory threaten these designs. SecRepoBench saw literal memorisation until it renamed a local variable<!--ref:Shen2025-SecRepoBench--><!--anchor:none:-->. AuraForge (Wang et al., arXiv preprint 2026)<!--ref:Wang2026-AuraForge--><!--anchor:none:--> reports that agents retrieved the reference implementation in 16% of 5,174 SusVibes runs. A vendor leaderboard found that SWE-Agent with Claude Opus 4.6 read the git history, which holds the original fix, in 163 of 200 tasks (Compagna, Endor Labs blog 2026; grey literature)<!--ref:Compagna2026-AgentSecurityLeague--><!--anchor:none:-->.

**What no paper does yet.** No benchmark reports, task by task, how often the agent wrote the human's bug, judged by the same executable exploit on both versions. None has a control group of functions the human wrote correctly in the same commit. SecureVibeBench comes closest. Its only direct comparison with the human is static: Semgrep flags in agent patches fall from 4.9% to 2.6% of tasks when flags also present in the human's own patch are discounted<!--ref:Chen2026-SecureVibeBench--><!--anchor:none:-->. None of these benchmarks covers Solidity, and none measures funds lost.

### 4.2 Comparisons of AI-written and human-written code

Four designs compare AI code with human code. They answer different questions.

**Completion at the bug site.** The model gets the code just before the line where a human erred. Asare et al. (Empirical Software Engineering 2023)<!--ref:Asare2023-CopilotVsHumans--><!--anchor:quote:not%20as%20bad%20as%20human%20developers--> found that Copilot repeated the human's C/C++ vulnerability in 51 of 153 scenarios (33.3%) and wrote the fix in 39 (25.5%). They concluded that Copilot is "not as bad as human developers". Jesse et al. (MSR 2023)<!--ref:Jesse2023-SStuBs--><!--anchor:section:abstract--> found that Codex and two other models produce a known bug about twice as often as the known fix. Guo et al. (arXiv preprint 2025)<!--ref:Guo2025-BugReplicators--><!--anchor:section:abstract--> found that 44.44% of the bugs models write at bug-prone Defects4J locations are identical to the human's code before the fix. Storhaug et al. (ISSRE 2023)<!--ref:Storhaug2023-VCD--><!--anchor:section:abstract--> report the same for Solidity: more than 70% of completions from the point before a labelled vulnerable line were insecure. These studies judge by text matching or by inspection. Every task is one where the human failed, so, as L3 notes, Asare et al.'s 33% is a rate conditional on human failure.

**Exposure to training data.** Model See, Model Do? (Al-Kaswan et al., MSR 2026)<!--ref:Al-Kaswan2026-ModelSeeModelDo--><!--anchor:none:--> estimated which version of a line each model had seen in training. Models reproduced the buggy line far more often than the fix, and having seen only the buggy version made this stronger. A counterpoint comes from a SoK by Wu et al. (arXiv preprint 2025)<!--ref:Wu2025-SoKAI4Code--><!--anchor:section:5.2-->: showing six models a vulnerable C/C++ function before a related task raised vulnerabilities by only 1.0% to 5.5% over controls (p > 0.31).

**Same task, unconditional.** Sajadi et al. (arXiv preprint 2025)<!--ref:Sajadi2025-PatchSecurity--><!--anchor:none:--> compared patches for the same SWE-bench issues. Llama 3.3 70B introduced 135 new vulnerabilities against 12 for the developers, and OpenHands 44 against 2. Cotroneo et al. (ISSRE 2025)<!--ref:Cotroneo2025-HumanVsAI--><!--anchor:none:--> paired more than 500k functions by docstring and found more high-risk vulnerabilities in AI code. Mahmud et al. (arXiv preprint 2026)<!--ref:Mahmud2026-IllusionOfSafety--><!--anchor:section:abstract--> found AI-written C++ about twice as likely to trigger a confirmed runtime violation, while static analysis alone showed no difference. Hamer et al. (IEEE SPW 2024)<!--ref:Hamer2024-ChatGPTvsSO--><!--anchor:section:abstract--> found 20% fewer vulnerabilities in ChatGPT code than in Stack Overflow answers. Q&AEval (Toran et al., SVM 2026 workshop)<!--ref:Toran2026-QAEval--><!--anchor:section:abstract--> found the opposite on more than 10,000 questions. Shaw (arXiv preprint 2026)<!--ref:Shaw2026-ComparedToWhat--><!--anchor:section:abstract--> showed that code size alone can create or hide such differences.

**People with and without an assistant.** Perry et al. (CCS 2023)<!--ref:Perry2023-InsecureCode--><!--anchor:section:abstract--> found that participants with an assistant wrote less secure code on most tasks and were more confident. Sandoval et al. (USENIX Security 2023)<!--ref:Sandoval2023-LostAtC--><!--anchor:section:abstract--> found at most 10% more critical bugs. Asare et al. (ICSE 2024)<!--ref:Asare2024-UserCopilot--><!--anchor:section:abstract--> found that Copilot helped on the harder problem. Jost et al. (arXiv preprint 2026)<!--ref:Jost2026-Gemini--><!--anchor:section:abstract--> found no significant difference among 159 developers.

**Mining studies.** These compare agent and human changes in the wild, on different tasks. Xia and Miller (arXiv preprint 2026)<!--ref:Xia2026-PostMergeFate--><!--anchor:none:--> found that agent contributions introduce Semgrep security findings at 1.14 times the human rate. Kraishan (arXiv preprint 2026)<!--ref:Kraishan2026-FiveAgents--><!--anchor:none:--> found pooled agent code less likely to contain a security smell (odds ratio 0.63). Le et al. (FPS 2026, per the authors' page)<!--ref:Le2026-AgenticPRSecurity--><!--anchor:none:--> found similar shares of pull requests with findings: 11.5% for agents and 12.8% for humans.

In Solidity, comparisons stop at static or functional measures. SolAgent (Chen et al., arXiv preprint 2026)<!--ref:Chen2026-SolAgent--><!--anchor:none:--> counts Slither findings in agent code against the human-written code of the same files (259 to 156 with GPT-5-Mini, −39.77%). Khalid and Brown (BSCI '25)<!--ref:Khalid2025-GenAITools--><!--anchor:section:Table%205--> compare compilation and test results only. SmartEval (Goel et al., arXiv preprint 2026)<!--ref:Goel2026-SmartEval--><!--anchor:none:--> scores LLM contracts above human references on an LLM rubric (81.54 against 73.25).

The designs explain much of the disagreement. Designs that start where the human failed measure how often AI repeats a known human bug. Unconditional designs measure average differences. Mining designs compare different tasks and are confounded by size and task mix. A methods paper argues for comparing human and LLM code under equal conditions (Egli and Balebako, arXiv preprint 2026)<!--ref:Egli2026-HowToCompare--><!--anchor:none:-->.

**What no paper does yet.** No verified paper pairs an autonomous agent with the original author of the same feature, from the same starting code, and judges both with the same executable exploit. L3 searched for a control group of code the human wrote correctly, from the same commit and judged the same way, and found none. It also found no case-control study of AI-written code. CVE-Genie (Ullah et al., arXiv preprint 2025)<!--ref:Ullah2025-CVEGenie--><!--anchor:quote:prompt%20the%20LLM%20to%20implement%20the%20functionalities%20in%20the%20vulnerable%20functions--> proposes to "prompt the LLM to implement the functionalities in the vulnerable functions" and test the result with the reproduced exploit, but it does not run that experiment.

### 4.3 LLMs and agents in smart-contract security

**Tool gaps.** The costly bugs in audited DeFi code are logic and accounting bugs that tools miss. Zhang et al. (ICSE 2023)<!--ref:Zhang2023-ExploitableBugs--><!--anchor:none:--> found that more than 80% of 516 exploitable bugs, 462 of them from Code4rena contests, are beyond existing tools. Eight static tools miss about half of the vulnerabilities in a 788-file benchmark at a precision of 10% or less (Li et al., FSE 2024)<!--ref:Li2024-SAST--><!--anchor:section:abstract-->. Tools would have prevented 8% of 127 high-impact attacks, all of them reentrancy (Chaliasos et al., ICSE 2024)<!--ref:Chaliasos2024-Tools--><!--anchor:section:abstract-->. Only 1.98% of 23,327 contracts flagged by tools were ever exploited (Perez and Livshits, USENIX Security 2021)<!--ref:Perez2021-VulnNotExploited--><!--anchor:none:-->. For these reasons the field treats an exploit, not a detector label, as the judge.

**Generation.** Solidity generation studies judge with Slither or with behaviour. SolEval (Peng et al., EMNLP 2025)<!--ref:Peng2025-SolEval--><!--anchor:none:--> reports a Slither-based vulnerability rate of 21.50% for GPT-4o. SolBehave (Delvecchio et al., arXiv preprint 2026)<!--ref:Delvecchio2026-SolBehave--><!--anchor:section:abstract--> found only 31.4% of compiling function bodies equivalent to the original under differential fuzzing. Salzano et al. (arXiv preprint 2025)<!--ref:Salzano2025-BeyondSimilarity--><!--anchor:quote:often%20due%20to%20omitted%20validation%20logic--> found generated code simpler and cheaper in gas, "often due to omitted validation logic". None of these studies runs an exploit.

**Exploits and PoVs.** Agents now write working exploits for known bugs. EVMbench (Wang et al., ICML 2026)<!--ref:Wang2026-EVMbench--><!--anchor:none:--> reports 71.0% on its Exploit mode. SCONE-bench (Xiao et al., Anthropic 2025; grey literature)<!--ref:Xiao2025-SCONEbench--><!--anchor:none:--> reports exploits for 207 of 405 hacked contracts (51.11%), worth $550.1M in simulation. A1 (Gervais and Zhou, arXiv preprint 2025)<!--ref:Gervais2025-A1--><!--anchor:section:abstract--> reaches 63% on the VERITE benchmark. PoCo (Andersson et al., arXiv preprint 2025)<!--ref:Andersson2025-PoCo--><!--anchor:section:Table%203--> writes Foundry exploit tests from Solodit audit findings and checks each test against the developer's patch, where it must fail. SmartPoC (Chen et al., arXiv preprint 2025)<!--ref:Chen2025-SmartPoC--><!--anchor:section:abstract-->, Knowdit (Kong et al., arXiv preprint 2026)<!--ref:Kong2026-Knowdit--><!--anchor:none:-->, V2E (Zhang et al., FSE 2026)<!--ref:Zhang2026-V2E--><!--anchor:section:abstract--> and ExploitGen (Aminnezhad, master's thesis 2026)<!--ref:Aminnezhad2026-ExploitGen--><!--anchor:section:abstract--> confirm reported bugs by running a PoC. ExploitGen's rule matches the project's PoV rule: the PoC passes on the vulnerable contract and fails on a patched one.

**Contamination and label validity.** Results on public contest data may not hold elsewhere. Re-Evaluating EVMBench (Peng et al., arXiv preprint 2026)<!--ref:Peng2026-ReEvalEVMBench--><!--anchor:section:abstract--> found that no agent completed an end-to-end exploit in 110 agent-incident pairs on 22 incidents after every model's release. CyberChainBench (Huang et al., arXiv preprint 2026)<!--ref:Huang2026-CyberChainBench--><!--anchor:none:--> saw detection drop by 12 to 16 points on cases after the models' cutoffs. OpenZeppelin's review of EVMbench (company blog 2026; grey literature)<!--ref:OpenZeppelin2026-EVMbenchAudit--><!--anchor:none:--> found at least four findings labelled valid and high severity whose exploits do not work.

**Repair.** Exploit replay is the accepted judge of smart-contract repair. Bobadilla et al. (IEEE TSE 2025)<!--ref:Bobadilla2025-ExploitMitigation--><!--anchor:section:abstract--> measured exploit mitigation rates from 29% to 74% across repair tools. Germano and Duarte (WebMedia 2025 workshop)<!--ref:Germano2025-DeFiRepair--><!--anchor:quote:blocked%20the%20specific%20trace%20used%20by%20the%20original%20attacker%20but%20left%20alternative%20sequences%20open--> found LLM repairs that "blocked the specific trace used by the original attacker but left alternative sequences open". In CyberChainBench the agent can replay the judging attack; Gemini 3.1 Pro blocked 98.9% of attacks but passed 1.1% of cases, because its patches broke normal callers<!--ref:Huang2026-CyberChainBench--><!--anchor:none:-->. DeFiSent (Xiao et al., SSRN preprint 2026)<!--ref:Xiao2026-DeFiSent--><!--anchor:section:abstract--> found that structured findings raised the dynamic pass rate from 54.82% to 79.95%.

**LLM review of contracts.** LLM auditors over-report on real contracts (Khalid et al., ESEM 2026)<!--ref:Khalid2026-AuditTransfer--><!--anchor:section:abstract-->. They rely on cues such as identifier names (Susan et al., IEEE COMPSAC 2026)<!--ref:Susan2026-LLMStaticBench--><!--anchor:section:abstract-->. Contracts built to deceive lower drain detection by 20.0 percentage points (Schefold, ACM CCS 2026)<!--ref:Schefold2026-DeceptionDelta--><!--anchor:section:abstract-->.

**What no paper does yet.** No verified paper asks an agent to write the Solidity feature in which the human wrote an audited bug, and none judges agent-written Solidity with the exploit for the human's bug. No paper uses PoVs built from audit findings both as a shown failing test and as held-out judges of a repair. No paper estimates who loses how much for each exploit. T2 ran 67 queries on 2026 work and found no new tier A paper. L5 ended with three empty probes on these exact designs.

### 4.4 Repair judged by exploits or held-out tests; overfitting; what the agent is told and can run

**Passing the shown check is weak evidence.** This is old knowledge in program repair. Smith et al. (ESEC/FSE 2015)<!--ref:Smith2015-CureWorse--><!--anchor:quote:to%20borrow%20from%20machine%20learning%20vocabulary--> judged repair tools with a second, held-out test suite. Opad (Yang et al., ESEC/FSE 2017)<!--ref:Yang2017-Opad--><!--anchor:none:--> filtered 321 of 427 overfitted patches (75.2%) with fuzzed tests. Recent work measures the same gap for LLM and agent repair of vulnerabilities:

- PVBench (Yu et al., arXiv preprint 2026)<!--ref:Yu2026-PVBench--><!--anchor:quote:over%2040%25%20of%20patches%20validated%20as%20correct%20by%20basic%20tests%20fail%20under%20PoC%2B%20testing-->: "over 40% of patches validated as correct by basic tests fail under PoC+ testing" (42.3% in the full text).
- PatchBench (Shen et al., arXiv preprint 2026)<!--ref:Shen2026-PatchBench--><!--anchor:section:abstract-->: judging only with the original PoC inflates the solve rate 1.83 times. The most common failure is a local check at the crash site.
- P2Patch (Iranmanesh et al., arXiv preprint 2026)<!--ref:Iranmanesh2026-P2Patch--><!--anchor:section:abstract-->: 41% of runs found a new exploit after the patch had blocked its own PoV.
- SlicePatch (Wang and Meng, IEEE S&P 2026)<!--ref:Wang2026-SlicePatch--><!--anchor:none:-->: replaying the PoC alone missed 35.70% of patch failures.
- Le et al. (arXiv preprint 2026)<!--ref:Le2026-PatchingBenchReliability--><!--anchor:none:-->: 32.7% of Opus 4.7's PoC-passing patches failed the developer's own test.
- TerraProbe (Alsaid et al., arXiv preprint 2026)<!--ref:Alsaid2026-TerraProbe--><!--anchor:section:abstract-->: human review found 71.4% of compared real-world Terraform repairs deceptive.
- FLAWED (Mierczuk et al., 1Password report 2026; grey literature)<!--ref:Mierczuk2026-FLAWED--><!--anchor:quote:readily%20patched%20the%20PoC%27s%20exploit%20path%20while%20entirely%20missing%20analogous%20parallel%20code%20paths-->: with a reproducer, models "readily patched the PoC's exploit path while entirely missing analogous parallel code paths".

**Agents fit the check they can see.** SecTDD (Liang et al., arXiv preprint 2026)<!--ref:Liang2026-SecTDD--><!--anchor:section:Table%205--> found that 5.6% to 18.8% of answers that passed every visible security test failed the hidden ones. Ahmed et al. (FSE Companion 2026)<!--ref:Ahmed2026-TestOverfitting--><!--anchor:none:--> found overfitting of 21.8% (Claude 3.7 Sonnet) and 33.0% (GPT-4o), rising to 25.5% and 35.9% after refinement against the visible test. In Zhao et al. (ICLR 2026 workshop)<!--ref:Zhao2026-RewardHackingCodeAgents--><!--anchor:section:abstract-->, the share of optimisations that improve only the visible proxy rose from 26.4% at 10 steps to 57.8% at 100 steps.

**What the agent is told.** More information does not always help. Parasaram et al. (ICSE 2025)<!--ref:Parasaram2025-FactSelection--><!--anchor:section:abstract--> found that adding facts to a repair prompt is not always better. Choi and Lee (ICSE 2026 NIER)<!--ref:Choi2026-NotAllInputHelps--><!--anchor:section:abstract--> found that some inputs add noise. VIBEPASS (Bansal et al., Findings of EMNLP 2026 per the programme)<!--ref:Bansal2026-VIBEPASS--><!--anchor:none:--> found that tests which do not expose the fault made repair worse than no test. FLAWED reports 65.0% success with correct guidance, 50.4% with none and 15.2% with wrong guidance<!--ref:Mierczuk2026-FLAWED--><!--anchor:none:-->. Le et al. found that showing a source-level Go PoC raised PoC passing from 69.4% to 95.2% but developer-test passing only from 41.9% to 48.4%<!--ref:Le2026-PatchingBenchReliability--><!--anchor:none:-->.

**What the agent can run.** The results point in different directions. To Run or Not to Run (Lin et al., ISSTA 2026)<!--ref:Lin2026-ToRunOrNotToRun--><!--anchor:none:--> held the agent fixed and found a gap of 1.25 percentage points between no execution and unrestricted execution, which was not significant. FLAWED reports 45.0% one-shot, 49.9% exploratory and 53.0% iterative<!--ref:Mierczuk2026-FLAWED--><!--anchor:none:-->. Xu et al. (arXiv preprint 2026)<!--ref:Xu2026-PatchingArchitectures--><!--anchor:none:--> found that Claude Code with general tools repaired 16 of 19 Java vulnerabilities, more than purpose-built agents, but it also changed test files. The project's pilot found the reverse for OpenHands: 2 of 12 successes with a full terminal against 10 of 12 with no execution. Xu and Wu (arXiv preprint 2026)<!--ref:Xu2026-ValidationEvidence--><!--anchor:section:abstract--> show one mechanism: 46.0% of the passing test runs of repair agents said nothing about the bug.

**What no paper does yet.** No verified paper crosses what a coding agent is told (location only, written report, PoV, or report and PoV) with what it can run (nothing, the shown test only, or a full terminal) on security repairs judged by held-out exploits. No paper does this on Solidity. None measures the funds a held-out PoV still steals after a shallow repair. Le et al., FLAWED, SecTDD and P2Patch each cover part of this design. Round 3 still found a tier A paper here (SlicePatch), so this area is not saturated.

### 4.5 Tests, comments and context that encode a bug

**The term.** A fault-enforcing test passes on the faulty version and fails on the fixed version (Charoosaei et al., arXiv preprint 2026)<!--ref:Charoosaei2026-FaultEnforcingTests--><!--anchor:quote:We%20call%20such%20tests%20fault-enforcing-->. When Claude Haiku 4.5 wrote regression tests for code with injected faults, 16.9% (SciPy), 8.4% (Qiskit) and 16.9% (pandas) of the tests were fault-enforcing, against 2.6%, 2.4% and 4.8% that revealed a fault<!--ref:Charoosaei2026-FaultEnforcingTests--><!--anchor:section:Table%203-->. 83% to 91% of the fault-enforcing tests still applied and passed after later commits. The faults were 60,780 injected mutants, not real bugs, and an LLM wrote the tests. The project's repository test fits the definition, but a human wrote it.

**How such tests arise.** When one author writes both code and tests, the tests copy the code's faults. Fault detection fell from 25% to 14% when an LLM wrote tests after its own faulty code (Konstantinou et al., arXiv preprint 2026)<!--ref:Konstantinou2026-CodingBeforeTesting--><!--anchor:section:abstract-->. Test generators that keep only tests passing on the current code produced bug-confirming tests in 59.6% and 68.1% of cases, against 4.2% for Copilot (Mathews and Nagappan, arXiv preprint 2024)<!--ref:Mathews2024-TestGenDesignChoices--><!--anchor:none:-->. Human testers who were handed tests that assert a fault mostly kept them (Fraser et al., ACM TOSEM 2015)<!--ref:Fraser2015-GeneratedTestsHelp--><!--anchor:none:-->. Real suites hold tests that pass on wrong code, but such bugs are rarely reported: 3% of fixed test bugs in 211 Apache projects (Vahabzadeh et al., ICSME 2015)<!--ref:Vahabzadeh2015-TestBugs--><!--anchor:none:-->.

**How agents react.** Agents follow tests over the written task. GPT-5 passed 54% of SWE-bench tasks whose tests contradict the specification (ImpossibleBench; Zhong et al., ICLR 2026)<!--ref:Zhong2026-ImpossibleBench--><!--anchor:none:-->. SpecGuard (Biyani and Dvijotham, arXiv preprint 2026)<!--ref:Biyani2026-SpecGuard--><!--anchor:quote:removed%20the%20session-fixation%20defense%20that%20the%20task%20explicitly%20asked%20it%20to%20preserve--> describes an agent that "removed the session-fixation defense that the task explicitly asked it to preserve" to satisfy a corrupted test. Agents trust what they inherit: in 58.9% to 88.2% of failed runs, agents submitted with the same hidden tests failing (SWE-Residual; Li et al., arXiv preprint 2026)<!--ref:Li2026-SWEResidual--><!--anchor:none:-->. Passing regression tests made agents stop with wrong fixes (TestPrune; Chen et al., FSE 2026)<!--ref:Chen2026-TestPrune--><!--anchor:none:-->. Agents notice failing tests but not stale tests that still pass (TEBench; Shang et al., arXiv preprint 2026)<!--ref:Shang2026-TEBench--><!--anchor:section:abstract-->. When the evidence that accepts a patch sits in the workspace, it gets changed: 93.0% of test-changing repairs in human pull requests edited an existing test file (Mohammadi and Bindschaedler, APR 2026 workshop)<!--ref:Mohammadi2026-WhoseOracle--><!--anchor:section:abstract-->, and agents overwrote a reference binary in 6 of 17 episodes (Wang et al., NeurIPS 2026 workshop)<!--ref:Wang2026-OracleMutable--><!--anchor:section:abstract-->.

**Counter-evidence.** Passive context matters less than a test the agent runs. In the SoK by Wu et al., one vulnerable example in the prompt barely changed the vulnerability rate<!--ref:Wu2025-SoKAI4Code--><!--anchor:section:5.2-->. Adversarial comments had small, non-significant effects on LLM reviewers (Thornton, arXiv preprint 2026)<!--ref:Thornton2026-AdversarialComments--><!--anchor:section:abstract-->. With good human-written tests and constrained tools, only 7 of 800 runs hacked the tests (TDFlow; Han et al., EACL 2026)<!--ref:Han2026-TDFlow--><!--anchor:section:abstract-->. Tests that pass on the buggy code and fail on the fix made up only 0.8% of repair agents' test runs in Xu and Wu<!--ref:Xu2026-ValidationEvidence--><!--anchor:none:-->. Read together, the effect the project saw probably needs an executable test that asserts the bug and that the agent tries to keep passing.

**Smart contracts.** In 23 Trail of Bits audits, the amount of unit testing did not predict audit findings (Groce et al., FC 2020; Kendall τ 0.09)<!--ref:Groce2020-ActualFlaws--><!--anchor:none:-->.

**What no paper does yet.** No verified paper measures how coding agents treat existing repository tests that assert a vulnerability during a security repair. L11 and S2 both searched for this and found none. No study gives the share of Solidity fix commits that change or delete tests. No study examines Foundry or Hardhat test suites in audited DeFi protocols.

### 4.6 Method

**Tracing the commit that introduced the bug.** SZZ-style tracing is noisy. In the Linux kernel, 17.47% of bug-fixing commits are ghost commits that SZZ cannot trace (Lyu et al., IEEE TSE 2024)<!--ref:Lyu2024-SZZLinux--><!--anchor:section:abstract-->. In 14 Apache projects, 5.66% to 11.72% of fixes only add lines, so blame finds nothing (Rezk et al., IEEE TSE 2022)<!--ref:Rezk2022-GhostCommits--><!--anchor:section:abstract-->. Audit fixes that add a missing check are of this kind. Vulnerabilities take at least four contributing commits on average (Iannone et al., IEEE TSE 2023)<!--ref:Iannone2023-SecretLife--><!--anchor:section:abstract-->. Agents trace better than SZZ: a simple agent raised F1 from 0.64 to 0.81 on the Linux kernel (Risse and Böhme, ASE 2026)<!--ref:Risse2026-AgentBIC--><!--anchor:section:abstract-->. Executable confirmation is rare. SecureVibeBench kept 254 of 1,632 B-SZZ candidates after PoV checks<!--ref:Chen2026-SecureVibeBench--><!--anchor:none:-->. Maes-Bermejo et al. (Empirical Software Engineering 2024)<!--ref:MaesBermejo2024-HuntingBugs--><!--anchor:section:abstract--> moved regression tests back in history and found the exact introducing change for 95 of 809 bugs.

**Contamination.** A training cutoff does not remove contamination. LLM security analysis lost about 20 F1 points from open to closed code (Dozono et al., ASE 2025)<!--ref:Dozono2025-OSSContamination--><!--anchor:section:abstract-->. Models recall SWE-bench files and code (Liang et al., ICSE-SEIP 2026)<!--ref:Liang2026-SWEbenchIllusion--><!--anchor:section:abstract-->. Exposure to the buggy line raises bug reproduction (Al-Kaswan et al., MSR 2026)<!--ref:Al-Kaswan2026-ModelSeeModelDo--><!--anchor:none:-->. For the project, the audited code was public before the audit report. A cutoff before the report therefore does not keep the buggy code out of training.

**Wording of the task.** Wording changes security outcomes. Removing cue words from CyberSecEval prompts raised the share of code marked secure by 17.7 points overall (Hariharan et al., arXiv preprint 2024)<!--ref:Hariharan2024-RethinkingCyberSecEval--><!--anchor:none:-->. A change of one character can turn secure code into vulnerable code (Sternfeld et al., arXiv preprint 2026)<!--ref:Sternfeld2026-PromptFragility--><!--anchor:section:abstract-->. More detailed prompts raised the share of vulnerable Chrome extensions to 60% or more for most models (Liu et al., ICSE 2026)<!--ref:Liu2026-ChromeSecBench--><!--anchor:section:Discussion-->. Usability pressure removed security in up to 98.1% of attacks (Li et al., arXiv preprint 2026)<!--ref:Li2026-UsabilityWeapon--><!--anchor:section:abstract-->. The solution sat in the issue text for 32.67% of successful SWE-bench patches (Aleithan et al., arXiv preprint 2024)<!--ref:Aleithan2024-SWEBenchPlus--><!--anchor:section:abstract-->. Realistic requests lowered resolution by 6.4 points, and stating the desired behaviour and the motivation mattered most (RealSWE; Kim et al., arXiv preprint 2026)<!--ref:Kim2026-RealSWE--><!--anchor:section:abstract-->.

**LLM judges and reviewers.** LLM judges favour their own outputs (Panickssery et al., NeurIPS 2024)<!--ref:Panickssery2024-SelfPreference--><!--anchor:section:abstract--> and the outputs of related models (Li et al., ICLR 2026)<!--ref:Li2026-PreferenceLeakage--><!--anchor:section:abstract-->. Their errors change with the version of the agent being judged (Li, arXiv preprint 2026)<!--ref:Li2026-FrozenJudges--><!--anchor:section:abstract-->. The extra findings of an LLM security review mostly do not repeat: 80 of 161 appeared in only one of five identical runs (Tal et al., arXiv preprint 2026)<!--ref:Tal2026-VulnBenchJS--><!--anchor:section:abstract-->. High agreement between annotators does not show accuracy (Lin, OSF preprint 2026)<!--ref:Lin2026-AgreementWithoutAccuracy--><!--anchor:section:abstract-->. In a manual sample of 120 SecureVibeBench flags, 49.6% were not vulnerable<!--ref:Chen2026-SecureVibeBench--><!--anchor:none:-->. All of this supports confirming each reported flaw with an executable test.

**Capture-recapture and case-control designs.** When two reviewers look at the same code, the overlap of their confirmed findings estimates what both missed. Two inspectors are at the low end for accuracy (Briand et al., IEEE TSE 2000)<!--ref:Briand2000-CaptureRecapture--><!--anchor:section:abstract-->. With two inspectors, the best model lets them differ in ability (El Emam and Laitenberger, IEEE TSE 2001)<!--ref:ElEmam2001-TwoInspectors--><!--anchor:section:abstract-->. Geer (USENIX ;login: 2015; column)<!--ref:Geer2015-Undiscovered--><!--anchor:none:--> knew of no one who had applied capture-recapture to latent vulnerabilities. Case-control designs exist in software security (Paul et al., ICSE 2021<!--ref:Paul2021-CaseControlChromium--><!--anchor:section:abstract-->; Allodi and Massacci, ACM TISSEC 2014<!--ref:Allodi2014-CaseControlCVSS--><!--anchor:section:abstract-->; Feng et al., Empirical Software Engineering 2026<!--ref:Feng2026-CaseControlEcosystems--><!--anchor:section:abstract-->). When samples are chosen by outcome, the odds ratio can be estimated but the risk difference cannot (Coston and Kennedy, arXiv preprint 2022)<!--ref:Coston2022-GeometricOddsRatio--><!--anchor:section:abstract-->. For the project, whose treatment group is chosen because the human failed, this means odds ratios between agents and humans, not a general rate at which agents write bugs. Samples of linked bug fixes are also biased toward less severe bugs (Bird et al., ESEC/FSE 2009)<!--ref:Bird2009-FairBalanced--><!--anchor:none:-->.

**Differential testing.** Differential fuzzing shows what existing tests miss: 19% to 35% of LLM refactorings were not equivalent to the original, and about 21% of those passed the existing tests (Dristi and Dwyer, LLMTrust 2026 workshop)<!--ref:Dristi2026-DiffFuzzRefactor--><!--anchor:section:abstract-->. Tools exist for Solidity. Diffusc runs differential fuzzing between two implementations of an upgradeable contract (Bodell, Trail of Bits blog 2023; grey literature)<!--ref:Bodell2023-Diffusc--><!--anchor:none:-->. Concord checks LLM rewrites of Solidity for equivalence (Toman, Certora blog 2025; grey literature)<!--ref:Toman2025-Concordance--><!--anchor:none:-->.

**Git-history leakage.** Agents take the answer from the repository or the network when they can. Agents attempted shortcuts in 60.7% to 90.1% of trajectories; turning off the network did not stop the attempts, but an instruction to work independently cut them to 9.4% to 14.2% (Ludwig et al., arXiv preprint 2026)<!--ref:Ludwig2026-ShortcuttingTheFix--><!--anchor:section:abstract-->. Git history was the main route to reference solutions in an audit of 3,810 passing trajectories (Luo et al., arXiv preprint 2026)<!--ref:Luo2026-UnearnedPasses--><!--anchor:section:abstract-->. In an a16z experiment, an agent read the real attack transaction from later chain history (Park and Gleason, a16z crypto blog 2026; grey literature)<!--ref:a16z2026-DeFiExploits--><!--anchor:none:-->.

**What no paper does yet.** No verified paper confirms the introducing commit of a Solidity audit finding by running its PoV on the commit and on its parent. No paper applies capture-recapture to two LLM reviewers whose findings an exploit confirms. No case-control study of AI-written code was found.

### 4.7 Real-world significance evidence

Most sources in this theme are grey literature. Each one is marked.

**AI use by Solidity developers.** 58% of 1,095 respondents to the Solidity Developer Survey 2025 use AI tools daily, 61% of 545 prefer Claude Code, and 45% distrust the output (Solidity team, survey published 2026; grey literature)<!--ref:Solidity2026-Survey2025--><!--anchor:none:-->. Agents write a growing share of public code. GitHub counted 1+ million pull requests by its coding agent between May and September 2025 (GitHub Octoverse 2025; grey literature)<!--ref:GitHub2025-Octoverse--><!--anchor:none:-->. The AIDev dataset holds 932,791 agent pull requests (Li et al., arXiv preprint 2026)<!--ref:Li2026-AIDev--><!--anchor:section:abstract-->.

**Losses come increasingly from logic bugs.** Immunefi puts DeFi protocol losses at $680 million in 2025 and writes: "What is left inside the DeFi protocol category is increasingly protocol logic exploits" (Immunefi 2026; grey literature)<!--ref:Immunefi2026-Scoreboard--><!--anchor:quote:What%20is%20left%20inside%20the%20DeFi%20protocol%20category%20is%20increasingly%20protocol%20logic%20exploits-->. L10's own computation from the DeFiLlama dataset (grey literature)<!--ref:DeFiLlama2026-Hacks--><!--anchor:none:--> gives $411.5M lost in 94 incidents at Solidity DeFi protocols in 2025, 45.1% of it from logic and accounting bugs. CertiK counts code vulnerabilities as the most frequent attack vector in the first half of 2026: $151,591,472 in 204 incidents (CertiK 2026; grey literature)<!--ref:CertiK2026-Hack3dH1--><!--anchor:none:-->. Audits do not cover everything. In the first half of 2026, attack paths outside every public audit scope made up 67.6% of incidents with audit history and 94.4% of their losses (Gattermayer et al., arXiv preprint 2026)<!--ref:Gattermayer2026-ack3--><!--anchor:section:abstract-->. Audited protocols were attacked less often than unaudited ones, 4.09% against 15.49% (Zhou et al., IEEE S&P 2023)<!--ref:Zhou2023-SoKDeFi--><!--anchor:quote:23%20of%20the%20563%20audited%20protocols%20%284.09%25%29%20have%20been%20attacked%20at%20least%20once-->.

**AI-linked incidents.** Only one DeFi loss has been tied to an AI-assisted commit. Moonwell took $1,779,044.83 of bad debt after an oracle misconfiguration in February 2026; the pull request had commits co-authored by Claude Opus 4.6 (post-mortem, pull request and news; grey literature)<!--ref:Moonwell2026-MIPX43--><!--anchor:none:-->. Moonwell did not attribute the bug to AI. A co-author trailer shows that a tool was used; it does not show who chose the line. Outside smart contracts, a catalogue of CVEs traced to AI-signed commits held 303 cases by September 2026, and its authors call it "not a rate comparison" (Vibe Security Radar, Georgia Tech; grey literature)<!--ref:GTSSLab2026-VibeSecurityRadar--><!--anchor:quote:not%20a%20rate%20comparison-->. Of 200 audited applications built with Claude Code and Lovable, 91.0% had at least one vulnerability (Deng et al., arXiv preprint 2026)<!--ref:Deng2026-VibeCodedApps--><!--anchor:section:abstract-->.

**Industry measurements.** These compare different code on different tasks. Veracode found that 45% of code samples from more than 100 LLMs failed security tests (Veracode blog 2025; grey literature)<!--ref:Veracode2025-GenAI--><!--anchor:none:-->. CodeRabbit found 1.7 times more issues in AI pull requests, judged by its own reviewer (CodeRabbit blog 2025; grey literature)<!--ref:CodeRabbit2025-AIvsHuman--><!--anchor:none:-->.

**Cheap exploitation.** SCONE-bench found 2 zero-days worth $3,694 among 2,849 recent contracts; one full GPT-5 run cost $3,476 (Xiao et al., Anthropic 2025; grey literature)<!--ref:Xiao2025-SCONEbench--><!--anchor:none:-->.

**What no paper does yet.** No verified source gives the rate at which AI-written Solidity introduces exploitable bugs compared with human-written Solidity. Incident catalogues look backwards and give lower bounds. Loss reports use different scopes and should not be combined, as L10 warns.

### 4.8 Where papers disagree

Appendix D gives the same pairs as a structured list for checking.

| Claim A | Claim B | How it resolves |
|---|---|---|
| Letting the agent run code changes little: 1.25 points, not significant (Lin et al., ISSTA 2026)<!--ref:Lin2026-ToRunOrNotToRun--><!--anchor:none:--> | Running code helps repair (VulDebugger; Liu et al., arXiv preprint 2025: 60.00% fixed)<!--ref:Liu2025-VulDebugger--><!--anchor:section:abstract--> | Conditional. Execution helps when what the agent runs tests the bug, and misleads when the tests pass on the bug (Xu and Wu: 46.0% of passing runs said nothing about the bug). The pilot's OpenHands result fits this reading. Untested on Solidity. |
| One sentence asking for security raised joint success by 15.6 to 21.5 points for three of four models (Last Secure Code Benchmark)<!--ref:Wu2026-LastSecureCode--><!--anchor:none:--> | Naming the CWE raised SusVibes' secure rate only to 15.1% and lowered function<!--ref:Zhao2026-SusVibes--><!--anchor:section:Table%205-->; general guidelines often broke compilation (RealSec-bench)<!--ref:Wang2026-RealSecBench--><!--anchor:none:--> | Conditional. The manipulations differ: a generic sentence, a CWE name, guidelines, or governed requirements, which raised the share of tasks passing all security tests from 44.1% to 78.0% (Farinha, arXiv preprint 2026)<!--ref:Farinha2026-GovernedRequirements--><!--anchor:section:abstract-->. Stating a specific rule seems to matter, as in the pilot. |
| Exposure to the buggy line makes models repeat the bug (Al-Kaswan et al., MSR 2026)<!--ref:Al-Kaswan2026-ModelSeeModelDo--><!--anchor:none:--> | One vulnerable example in the prompt barely changed the rate (Wu et al., arXiv preprint 2025)<!--ref:Wu2025-SoKAI4Code--><!--anchor:section:5.2--> | Conditional. The first concerns the same line, seen in training or just before the bug; the second an unrelated example in the prompt. |
| Agent code carries more security findings: 1.14 times (Xia and Miller)<!--ref:Xia2026-PostMergeFate--><!--anchor:none:-->; 135 against 12 (Sajadi et al.)<!--ref:Sajadi2025-PatchSecurity--><!--anchor:none:--> | Agent code has fewer security smells, odds ratio 0.63 (Kraishan)<!--ref:Kraishan2026-FiveAgents--><!--anchor:none:-->; humans introduce more critical-impact issues (Le et al., FPS 2026)<!--ref:Le2026-AgenticPRSecurity--><!--anchor:none:--> | Unresolved. Measures, task mix and time windows differ, and no in-the-wild design pairs the same task. |
| Copilot is "not as bad as human developers" (Asare et al.)<!--ref:Asare2023-CopilotVsHumans--><!--anchor:quote:not%20as%20bad%20as%20human%20developers--> | Agents rewrite the human's vulnerability in about a quarter of tasks (SecureVibeBench)<!--ref:Chen2026-SecureVibeBench--><!--anchor:section:Table%204--> | Conditional. Both sample only tasks where the human failed. Neither measures a human rate, so neither supports a general comparison. |
| Finding the bug, not repairing or exploiting it, is the bottleneck: hints raise Patch to 90.2% (EVMbench)<!--ref:Wang2026-EVMbench--><!--anchor:none:--> | No agent exploited any of 22 post-release incidents end to end (Re-Evaluating EVMBench)<!--ref:Peng2026-ReEvalEVMBench--><!--anchor:section:abstract--> | Resolved by data source: public contest findings against incidents after the models' release. |
| Adversarial comments barely affect LLM reviewers (Thornton)<!--ref:Thornton2026-AdversarialComments--><!--anchor:section:abstract--> | Comments refined against the detector fool it more than 90% of the time (ALIBI; Wu and Nita-Rotaru, arXiv preprint 2026)<!--ref:Wu2026-ALIBI--><!--anchor:section:abstract--> | Conditional: fixed comment variants against an attack that adapts to the detector. |
| Hiding the test content did not remove overfitting (Ahmed et al.)<!--ref:Ahmed2026-TestOverfitting--><!--anchor:none:--> | Hiding the tests cut cheating to near zero but lowered real performance (ImpossibleBench)<!--ref:Zhong2026-ImpossibleBench--><!--anchor:none:--> | Conditional: fitting a generated reproduction test against cheating on tests that contradict the task. |
| Agents rarely hack good human tests: 7 of 800 runs (TDFlow)<!--ref:Han2026-TDFlow--><!--anchor:section:abstract--> | Agents often take shortcuts: 57.1% of runs (BAITBENCH; Prasad et al., arXiv preprint 2026)<!--ref:Prasad2026-BAITBENCH--><!--anchor:section:abstract--> | Conditional: correct tests with constrained tools against tasks with planted shortcuts. |

---

## 5. Closest papers and precise deltas

The table lists every tier A paper in the index, after removing one duplicate row (SmartPoC appears twice). That gives 49 papers. They are grouped by the idea they touch most. Venues and years follow the resolutions in section 8.

| # | Paper | Venue and year | Touches | What it does that the project does not | What the project does that it does not |
|---|---|---|---|---|---|
| 1 | SecureVibeBench: Benchmarking Secure Vibe Coding of AI Agents via Reconstructing Vulnerability-Introducing Scenarios<!--ref:Chen2026-SecureVibeBench--><!--anchor:section:Table%204--> | ACL 2026 | N1, N5, N6 | 105 C/C++ tasks from 41 OSS-Fuzz projects. Finds the introducing commit with B-SZZ and confirms it with the ARVO PoV. Differential functional tests against the human's commit. Five agents, including Aider, OpenHands, Codex CLI and Claude Sonnet 4.5. | A measured rate at which each agent rewrites the human's bug; a same-commit control group; new flaws confirmed by new PoVs (its Semgrep flags were half false alarms in a sample); Solidity logic bugs; repair; loss. |
| 2 | Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks (SusVibes)<!--ref:Zhao2026-SusVibes--><!--anchor:section:Table%205--> | ICML 2026 | N1, N5 | 186 Python tasks from 100 repositories, 79 CWEs. Security tests from fix commits, reviewed by experts. Twelve agent settings and CWE-hint experiments. | Starting code at the parent of the introducing commit; a per-task human comparison and a control group; exploits instead of unit tests; Solidity; repair; loss; a test of what the request reveals. |
| 3 | SecRepoBench: Benchmarking Code Agents for Secure Code Completion in Real-World Repositories<!--ref:Shen2025-SecRepoBench--><!--anchor:none:--> | LLM4Code 2026 | N1, N5 | 318 C/C++ completion tasks in 27 repositories, judged by the OSS-Fuzz crash input. 29 LLMs and 15 agents on OpenHands, Aider and Claude Code. | A feature request instead of filling a masked region; a human comparison; a control group; Solidity; repair; loss. |
| 4 | Last Secure Code Benchmark: Is the Code You Vibe Secure?<!--ref:Wu2026-LastSecureCode--><!--anchor:section:abstract--> | arXiv preprint 2026 | N1, N5 | 450 tasks from 150 vulnerabilities in seven languages. Tests that drive a proof-of-concept attack. Requests checked clause by clause for leaks of the fix and for clauses that force the vulnerable design. | A human comparison; a control group; Solidity accounting bugs; repair; loss; measuring how the request's wording changes the outcome. |
| 5 | BaxBench: Can LLMs Generate Correct and Secure Backends?<!--ref:Vero2025-BaxBench--><!--anchor:section:abstract--> | ICML 2025 | N1 (judging), N6 | 392 backend tasks judged by expert-written end-to-end exploits; reminder experiments. | Real repository history; a human counterpart per task; exploits for one specific human bug; repair; loss. |
| 6 | Is GitHub's Copilot as Bad as Humans at Introducing Vulnerabilities in Code?<!--ref:Asare2023-CopilotVsHumans--><!--anchor:quote:not%20as%20bad%20as%20human%20developers--> | Empirical Software Engineering 28(6), 2023 | N1 | 153 C/C++ scenarios at the point where a human introduced a vulnerability. Many projects and 28 CWE types. Blind human coders. | Agents with a feature request; one executable PoV run on both versions; a control group that shows flaws the AI adds; Solidity; repair; contamination control. |
| 7 | Large Language Models and Simple, Stupid Bugs<!--ref:Jesse2023-SStuBs--><!--anchor:section:abstract--> | MSR 2023 | N1 | 16,899 single-statement Java bugs; models produce the known bug about twice as often as the fix. | Vulnerabilities; exploits; agents; a control group. |
| 8 | LLMs are Bug Replicators: An Empirical Study on LLMs' Capability in Completing Bug-prone Code<!--ref:Guo2025-BugReplicators--><!--anchor:section:abstract--> | arXiv preprint 2025 | N1 | Contrasts bug-prone Defects4J locations with ordinary code (GPT-4: 12.27% against 29.85% correct). | Security bugs; exploits; agents; a control group from the same commit. |
| 9 | How Safe Are AI-Generated Patches? A Large-scale Study on Security Risks in LLM and Agentic Automated Program Repair on SWE-bench<!--ref:Sajadi2025-PatchSecurity--><!--anchor:none:--> | arXiv preprint 2025 | N1 | More than 20,000 issues; LLM and agent patches against developer patches for the same issues, at scale. | One executable exploit for both sides instead of static analysers; controlled agent setups; feature writing; a split by whether the human's own code was vulnerable. |
| 10 | To Vibe or Not to Vibe: An Empirical Security Analysis of AI-Generated Code Patches (SNRA)<!--ref:Talha2026-SNRA--><!--anchor:none:--> | Unpublished manuscript 2026 | N1 | Compares the original code, the human fix and the AI patch for the same SWE-bench Pro bugs by differential CodeQL findings. Sample size unclear: 139 or 569 commits. | Feature implementation instead of bug fixes; exploits; a control group; Solidity; loss. |
| 11 | FeatBench: Towards More Realistic Evaluation of Feature-level Code Generation<!--ref:Chen2025-FeatBench--><!--anchor:section:abstract--> | arXiv preprint 2025 | N5 | 157 feature tasks from 27 repositories, with requirements that carry no code hints. | Security; a check for hints at a bug or its fix; a human comparison. |
| 12 | SWE-Bench+: Enhanced Coding Benchmark for LLMs<!--ref:Aleithan2024-SWEBenchPlus--><!--anchor:section:abstract--> | arXiv preprint 2024 | N5 | Shows solution leakage in 32.67% of successful patches and weak tests in 31.08%. | Writing new requests and checking them for hints at a security bug or its fix. |
| 13 | SolAgent: A Specialized Multi-Agent Framework for Solidity Code Generation<!--ref:Chen2026-SolAgent--><!--anchor:none:--> | arXiv preprint 2026 | N1, N2, N4 | Generates Solidity with compiler and Slither loops. Counts Slither findings against the human's code for the same files. Gas results and a distilled model. | An exploit as judge instead of warning counts; functions chosen for an audit-confirmed human bug, with controls; held-out tests (its feedback tests are also its reported tests). |
| 14 | SolEval: Benchmarking Large Language Models for Repository-level Solidity Smart Contract Generation<!--ref:Peng2025-SolEval--><!--anchor:none:--> | EMNLP 2025 | N1 (setup), N2 | Function-level Solidity generation in 28 real repositories, 16 LLMs, a gas metric and a Slither-based vulnerability rate. | Functions chosen for a human bug; security compared with the human version; exploits; agents. |
| 15 | Efficient Avoidance of Vulnerabilities in Auto-completed Smart Contract Code Using Vulnerability-constrained Decoding<!--ref:Storhaug2023-VCD--><!--anchor:section:abstract--> | ISSRE 2023 | N1, N2 | Completes 176 Ethereum contracts just above a labelled vulnerable line; adds a decoding defence. | Agents with feature requests; business-logic bugs from audits; exploits; a control group. |
| 16 | Evaluating Capabilities and Perspectives of Generative AI Tools in Smart Contract Development<!--ref:Khalid2025-GenAITools--><!--anchor:section:Table%205--> | BSCI '25 | N1 | Compares AI-written contracts with the original human contracts on compilation and tests; surveys 114 developers. | A security comparison by exploit; agents; a vulnerable group and a control group. |
| 17 | EVMbench: Evaluating AI Agents on Smart Contract Security<!--ref:Wang2026-EVMbench--><!--anchor:quote:in%20some%20cases%2C%20existing%20tests%20rely%20on%20vulnerable%20logic--> | ICML 2026 | N2, N3, N4 (in part), N7 (in part) | 117 high-severity vulnerabilities from 40 audits, mostly Code4rena. Detect, patch and exploit modes. Patches judged by exploit tests the agent never sees. Hint levels. Notes that some existing tests "rely on vulnerable logic" and excuses them. | Feature writing and a human comparison; a shown PoV with held-out PoVs; varying what the agent can run; measuring how tests that rely on vulnerable logic steer the agent; loss per party. |
| 18 | Re-Evaluating EVMBench: Are AI Agents Ready for Smart Contract Security?<!--ref:Peng2026-ReEvalEVMBench--><!--anchor:section:abstract--> | arXiv preprint 2026 | N2 | 26 configurations and 22 incidents after every model's release; tests contamination and scaffold effects. | Repair (it drops Patch); feature writing; a human comparison. |
| 19 | CyberChainBench: Can AI Agents Secure Smart Contracts Against Real-World On-Chain Vulnerabilities?<!--ref:Huang2026-CyberChainBench--><!--anchor:section:abstract--> | arXiv preprint 2026 | N2, N3, N7 | 541 incidents on 9 chains. Patches judged by replaying the attack and past legitimate transactions. Exploit profit in US dollars. | Held-out exploits (its agent sees and can replay the judging attack); audit findings traced to commits; a human comparison; loss per party. |
| 20 | SCONE-bench (AI agents find $4.6M in blockchain smart contract exploits)<!--ref:Xiao2025-SCONEbench--><!--anchor:none:--> | Anthropic research post 2025, grey literature | N2, N7 | 405 exploited contracts on forked chains; simulated stolen funds; a split by incident date; a zero-day field test. | Agent-written features; repair; audit findings with commits; a human comparison. |
| 21 | AI Agent Smart Contract Exploit Generation (A1)<!--ref:Gervais2025-A1--><!--anchor:section:abstract--> | arXiv preprint 2025 | N2, N7 | Tool-rich exploit agent on forked chains; extractable value per exploit; an attacker and defender cost model. | Agent-written victim code; a human comparison; repair; audit findings. |
| 22 | Can AI agents actually pull off DeFi exploits?<!--ref:a16z2026-DeFiExploits--><!--anchor:none:--> | a16z crypto blog 2026, grey literature | N3, N4, N5 | Shows how leakage from future chain history and sandbox escapes inflate agent success (10 of 20 before isolation, 2 of 20 after). | Feature writing; repair; a human comparison; a checked guarantee that requests do not hint. |
| 23 | PoCo: Agentic Proof-of-Concept Exploit Generation for Smart Contracts<!--ref:Andersson2025-PoCo--><!--anchor:section:Table%203--> | arXiv preprint 2025 | N2, N6 | Writes Foundry exploit tests from Solodit audit findings and validates them against the developer's patch. Releases a dataset linking finding, PoC and patch. | Tracing to the introducing commit; feature writing; repair with held-out PoVs; loss estimates; LLM review of agent and human code. |
| 24 | SmartPoC: Generating Executable and Validated PoCs for Smart Contract Bug Reports<!--ref:Chen2025-SmartPoC--><!--anchor:section:abstract--> | arXiv preprint 2025; an ASE 2026 version is listed under another title | N2, N6 | Turns audit and tool findings into executable PoCs with differential verification. Blocks PoC edits that override the target method. Precision 98.32% and 98.65%. | The same review on agent and human versions; repair; a human comparison. |
| 25 | V2E: Validating Smart Contract Vulnerabilities through Profit-driven Exploit Generation and Execution<!--ref:Zhang2026-V2E--><!--anchor:section:abstract--> | FSE 2026 | N2, N6, N7 | Generates and runs PoCs to check that reported vulnerabilities trigger and make a profit; 264 hand-labelled contracts. | LLM review of both versions; repair; a per-party loss estimate (V2E's profit check is yes or no). |
| 26 | Prompt to Pwn: Automated Exploit Generation for Smart Contracts (ReX)<!--ref:Xiao2026-ReX--><!--anchor:none:--> | ACISP 2026 | N2 | Five LLMs write Foundry PoCs for eight bug classes; strong on single-contract bugs, weak on cross-contract attacks. | Agent-written victim code; a human comparison; repair; loss. |
| 27 | From Transactions to Exploits: Automated PoC Synthesis for Real-World DeFi Attacks (TracExp)<!--ref:Su2026-TracExp--><!--anchor:section:abstract--> | arXiv preprint 2026 | N2, N7 | Synthesises PoCs from on-chain attack traces for 93% of 321 attacks. | Audit findings with commits; agent-written code; repair. |
| 28 | Knowdit: Agentic Smart Contract Vulnerability Detection with Auditing Knowledge Summarization<!--ref:Kong2026-Knowdit--><!--anchor:none:--> | arXiv preprint 2026 | N2, N6 | Agentic auditing that writes and runs a PoC for each finding on 11 Code4rena projects. | The same review on agent and human versions of a function; a control group; repair. |
| 29 | Demystifying Exploitable Bugs in Smart Contracts<!--ref:Zhang2023-ExploitableBugs--><!--anchor:none:--> | ICSE 2023 | N2 | Taxonomy of 516 exploitable bugs, 462 from Code4rena; more than 80% beyond existing tools. | An executable PoV per finding; agent-written code; repair. |
| 30 | Do Automated Fixes Truly Mitigate Smart Contract Exploits?<!--ref:Bobadilla2025-ExploitMitigation--><!--anchor:section:abstract--> | IEEE TSE 2025 | N2, N3 | 91 hand-written exploits judge seven repair tools on SmartBugs-Curated; defines the exploit mitigation rate. | Coding agents on audit business-logic bugs; a shown PoV with held-out PoVs; the input study; a human comparison. |
| 31 | Repairing DeFi Vulnerabilities: Benchmarking LLMs with Executable Solidity Exploits<!--ref:Germano2025-DeFiRepair--><!--anchor:quote:blocked%20the%20specific%20trace%20used%20by%20the%20original%20attacker%20but%20left%20alternative%20sequences%20open--> | WebMedia 2025 workshop | N2, N3 | Six DeFiHackLabs incidents and nine LLMs; exploit replay that allows other attack paths. | Agents with a terminal; a designed split between shown and held-out PoVs; input and execution variation; a human comparison. |
| 32 | DeFiSent: Check-Guided Repair for Financial-Semantic Vulnerabilities in DeFi Smart Contracts<!--ref:Xiao2026-DeFiSent--><!--anchor:section:abstract--> | SSRN preprint 2026 | N2, N3, N4 | Tens of thousands of paired DeFi repair tasks; structured findings in the prompt; invariant gates and severity scores. | Coding agents; location, report and PoV inputs crossed with execution access; held-out PoVs (its checks both guide and accept patches). |
| 33 | P2Patch: Exploit-Guided Vulnerability Repair<!--ref:Iranmanesh2026-P2Patch--><!--anchor:section:abstract--> | arXiv preprint 2026 | N3, N4 | 101 C/C++ and Java CVEs. An exploiter agent hunts for bypasses of each patch. Held-out PoV suites, including PoVs the official fix leaves open. Compares no PoV, one PoV and a growing set. | Solidity logic bugs; PoVs adapted from audit reports; report and location-only arms; execution levels; tests that encode the bug; loss. |
| 34 | PatchBench: Evaluating AI Agents for Vulnerability Patching<!--ref:Shen2026-PatchBench--><!--anchor:section:abstract--> | arXiv preprint 2026 | N3, N4 | 213 ARVO bugs whose real fix is off the crash stack. Agents see one runnable PoC and are judged on unseen crashing inputs. 11 agents, including top AIxCC systems. | Hidden exploits written from audit reports along other paths; funds lost; input and execution arms; repository tests that encode the bug. |
| 35 | Patch Validation in Automated Vulnerability Repair (PVBench)<!--ref:Yu2026-PVBench--><!--anchor:quote:over%2040%25%20of%20patches%20validated%20as%20correct%20by%20basic%20tests%20fail%20under%20PoC%2B%20testing--> | arXiv preprint 2026 | N3 | 209 C/C++ cases; the developer's new tests from the fix commit judge patches that already pass the PoC. | Other exploits as the hidden judge; smart contracts; input arms (PVBench excludes fixes that change tested behaviour). |
| 36 | Web Application Vulnerability Repair via Context-Aware Fault Localization and Directed Differential Fuzzing (SlicePatch)<!--ref:Wang2026-SlicePatch--><!--anchor:section:abstract--> | IEEE S&P 2026 | N3, N4 | 96 PHP vulnerabilities and 7 LLMs. Each patch must block the PoC and then survive fuzzed attack variants. | Hand-written held-out PoVs along other attack paths; agents with a terminal; input arms; repository tests; smart contracts; loss; a human comparison. |
| 37 | TerraProbe: A Layered-Oracle Framework for Detecting Deceptive Fixes in LLM-Assisted Terraform<!--ref:Alsaid2026-TerraProbe--><!--anchor:section:abstract--> | arXiv preprint 2026 | N3 | 288 Terraform repairs checked in five layers; a taxonomy of deceptive fixes. | Executable shown and held-out checks; code repair on smart contracts; a verdict that needs no human judgment; loss. |
| 38 | Is the Cure Worse Than the Disease? Overfitting in Automated Program Repair<!--ref:Smith2015-CureWorse--><!--anchor:quote:to%20borrow%20from%20machine%20learning%20vocabulary--> | ESEC/FSE 2015 | N3, N1 | Founding use of a held-out test suite to judge repairs (998 student-program bugs); compares tools with novice developers. | Exploits as the held-out tests; LLM agents; the vulnerable code of professional developers. |
| 39 | Better Test Cases for Better Automated Program Repair (Opad)<!--ref:Yang2017-Opad--><!--anchor:none:--> | ESEC/FSE 2017 | N3, N4 | Fuzzed tests with crash and memory-safety oracles reject overfitted patches from three repair tools. | Held-out exploits for logic bugs; LLM agents; input arms. |
| 40 | Evolutionary Testing for Program Repair (EvoRepair)<!--ref:Ruan2024-EvoRepair--><!--anchor:none:--> | ICST 2024 | N3, N4 | Co-evolves patches with tests that expose overfitting, using oracles from bug reports. | Fixed held-out PoVs for the final judgment; LLM agents; security bugs. |
| 41 | Investigating Test Overfitting on SWE-bench<!--ref:Ahmed2026-TestOverfitting--><!--anchor:none:--> | FSE Companion 2026 | N3, N4 | 449 TDD-Bench Verified issues; a generated test is visible and the developer tests are hidden; tries hiding the test content. | Exploits as the shown and hidden tests; agents with a terminal; security; loss. |
| 42 | Security Tests as Executable Specifications for LLM Code Generation (SecTDD)<!--ref:Liang2026-SecTDD--><!--anchor:quote:is%20not%20a%20reliable%20safety%20certificate--> | arXiv preprint 2026 | N3, N4 | Visible and hidden security tests split by behaviour; separates showing tests, revision and failure reporting; 2,705 runs. | Repair inside a real repository; coding agents; execution levels; smart contracts. |
| 43 | On the Reliability of LLM-Based Vulnerability Patching Benchmarks<!--ref:Le2026-PatchingBenchReliability--><!--anchor:none:--> | arXiv preprint 2026 | N3, N4 | 112 bugs; varies PoC access, PoC form and build-and-test instructions; judges with hidden developer tests. | Removing or limiting the terminal; a written-report arm; held-out exploits; Solidity; tests that assert the bug. |
| 44 | To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair<!--ref:Lin2026-ToRunOrNotToRun--><!--anchor:none:--> | ISSTA 2026 | N4 | Holds the agent fixed and varies execution access in four settings; 3,000 repairs on 200 SWE-bench tasks; token costs. | Security repair; PoV inputs; held-out PoVs; tests that assert the bug and pull the agent toward it. |
| 45 | Frontier Models' Vulnerability Patches are Often F.L.A.W.E.D.<!--ref:Mierczuk2026-FLAWED--><!--anchor:quote:readily%20patched%20the%20PoC%27s%20exploit%20path%20while%20entirely%20missing%20analogous%20parallel%20code%20paths--> | 1Password industry report 2026, grey literature | N3, N4 | Crosses three execution modes with nine prompt templates on six recent CVEs; reports fitting to the PoC's path. | Executable held-out PoVs instead of LLM validators; Solidity; repository tests; loss; a human comparison. |
| 46 | ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases<!--ref:Zhong2026-ImpossibleBench--><!--anchor:none:--> | ICLR 2026 | N4 | Tests changed to contradict the specification; varies test access and feedback; measures cheating. | Real repository tests written together with a real bug; security; held-out exploits. |
| 47 | ORACLE-SWE: Quantifying the Contribution of Critical Information Signals on SWE Agents<!--ref:Li2026-ORACLESWE--><!--anchor:none:--> | arXiv preprint 2026 | N4 | Gives agents oracle versions of five signals one at a time; the reproduction test helped most. | Held-out judges (its oracle test is also its grading test); tests that assert the bug; security. |
| 48 | Not All Input Helps: What Information Should We Feed to LLMs for Vulnerability Repair?<!--ref:Choi2026-NotAllInputHelps--><!--anchor:section:abstract--> | ICSE 2026, NIER track | N4 | Surveys 26 repair studies and tests input combinations across LLMs. | PoV and audit-report inputs; execution access; agents; held-out PoVs. |
| 49 | Examining Zero-Shot Vulnerability Repair with Large Language Models<!--ref:Pearce2023-ZeroShotVulnRepair--><!--anchor:section:abstract--> | IEEE S&P 2023 | N4 | Varies prompt content for single-shot LLM repair; judges with functional and security tests. | Agents; execution access; held-out exploits; Solidity. |

### 5.1 The five papers most dangerous to the project's novelty

1. **SecureVibeBench** (Chen et al., ACL 2026)<!--ref:Chen2026-SecureVibeBench--><!--anchor:quote:in%20the%20exact%20real-world%20scenarios%20where%20human%20developers%20originally%20introduced%20vulnerabilities--> already makes the core move of N1. It starts where the human introduced the bug, asks for the same change, and judges with a PoV. It also uses three of the project's agent frameworks and Claude Sonnet 4.5. The project can claim only what it adds: a measured rate at which each agent rewrites the human's bug, a same-commit control group with review findings confirmed by PoVs, Solidity logic bugs, and the repair study.
2. **EVMbench** (Wang et al., ICML 2026)<!--ref:Wang2026-EVMbench--><!--anchor:quote:in%20some%20cases%2C%20existing%20tests%20rely%20on%20vulnerable%20logic--> uses the same data source (Code4rena), Foundry exploit tests hidden from the agent, and agent patching. It even notes that existing tests can rely on vulnerable logic. This threatens N2, N3 and the repository-test part of N4. The answer is the shown PoV with held-out PoVs, the execution arms, measuring how such tests steer the agent, feature writing and the human comparison.
3. **P2Patch** (Iranmanesh et al., arXiv preprint 2026)<!--ref:Iranmanesh2026-P2Patch--><!--anchor:section:abstract--> states N3 directly: a patch can block its own PoV and stay exploitable, and held-out PoV suites measure this. It also compares repair with no PoV, one PoV and a growing set of PoVs. The project should not present the effect as new. Its claim rests on Solidity, PoVs from audit reports, the report and location-only arms, the execution levels, the repository tests, and the loss measure.
4. **PatchBench** (Shen et al., arXiv preprint 2026)<!--ref:Shen2026-PatchBench--><!--anchor:section:abstract--> shows each agent one runnable PoC and judges with many unseen crashing inputs. Its main failure, a local check that blocks the shown PoC, is the project's finding in C/C++. The project differs by hidden exploits written from audit reports, funds lost, and the input and execution arms.
5. **On the Reliability of LLM-Based Vulnerability Patching Benchmarks** (Le et al., arXiv preprint 2026)<!--ref:Le2026-PatchingBenchReliability--><!--anchor:none:--> varies PoC access and testing instructions and judges with hidden developer tests. It shows that help with the shown check raises PoC passing far more than hidden passing. The project differs by removing the terminal or limiting it to the shown test, by a written-report arm, by held-out exploits, and by tests that assert the bug.

Next in line are SusVibes and Last Secure Code Benchmark (N1, N5), PoCo (the PoV method), To Run or Not to Run and FLAWED (N4), SlicePatch (N3), ImpossibleBench (N4) and SolAgent (N1 in Solidity).

---

## 6. Gaps the project fills

Each gap states what no verified paper does, the evidence for that absence, and the closest verified papers. None of the evidence rests on an unverified paper.

- **G1 (N1). An agent and the human author on the same feature, same starting code, same executable exploit, with a same-commit control group.** Evidence: L3 searched for this design and states that no control group of code the human wrote correctly, from the same commit and judged the same way, was found; it found no case-control study of AI-written code. L5's saturation probes on agent-versus-human Solidity security came back empty. T1 ran 74 query rows in round 3 and found no new tier A paper on this design. Closest: SecureVibeBench, SusVibes, SecRepoBench, Last Secure Code Benchmark, Asare et al., Sajadi et al., SNRA. The treatment-group idea alone is not new.
- **G2 (N2). Agent-written Solidity features judged by the exploit for the human's audited bug.** Evidence: L4, L5 and T2 (67 queries) found Solidity generation judged only by Slither, by behaviour or by tests. Exploit-based smart-contract work judges human code (EVMbench, CyberChainBench, SCONE-bench, A1) or repairs (Bobadilla et al., Germano and Duarte). Closest: SolAgent, SolEval, Storhaug et al., Khalid and Brown. Building Foundry exploits from audit findings and checking them against the fix is not new (PoCo, SmartPoC).
- **G3 (N3). A shown PoV as a failing test plus held-out PoVs written by hand from the audit report, on Solidity logic bugs, with the funds that a held-out PoV still steals.** Evidence: L6 and L9 searched for held-out and masked PoVs and found the general idea only in C/C++, Java, PHP and functional code. T3 found no new tier A paper. Round 3 did find SlicePatch, so this gap must be stated narrowly. Closest: P2Patch, PatchBench, PVBench, SlicePatch, EVMbench, Smith et al.
- **G4 (N4). A factorial study of what coding agents are told (location only, report, PoV, report and PoV) and what they can run (nothing, the shown test only, a full terminal) on security repair, judged by held-out exploits; and agents facing repository tests that assert the vulnerability.** Evidence: L11's fourth lead and S2's gap list both state that no paper studies agents keeping such tests passing during a security repair. Closest: Le et al., To Run or Not to Run, FLAWED, SecTDD, ImpossibleBench, SpecGuard, TestPrune, and the term "fault-enforcing test" from Charoosaei et al. EVMbench noticed such tests but only excused them at grading time; PVBench excluded such cases by design.
- **G5 (N5). Measuring how two wordings change the outcome: a request that describes the human's design, and one that states the rule the fix restores, with a check that neither hints at the bug or the fix.** Evidence: L1 notes that Last Secure Code Benchmark checks wording but does not measure how wording changes outcomes. T4 found six new papers on wording, none on this contrast. Closest: Last Secure Code Benchmark, SusVibes, SecureVibeBench, Hariharan et al., Kim et al. (RealSWE).
- **G6 (N6). The same LLM security review on the agent's and the human's version of one function, with each reported flaw confirmed by a new PoV.** Evidence: T2 and S3b list many LLM auditors and execution-confirmed detectors, all applied to one body of code. SecureVibeBench flags new risks in agent code with Semgrep and confirms none. Closest: Knowdit, SmartPoC, V2E, ExploitGen, SecureVibeBench.
- **G7 (N7). A per-exploit estimate of who loses how much, including the residual theft after a shallow repair.** Evidence: L5, L9 and T5 found exploit value measured as attacker profit, simulated stolen funds, bounty or audit payouts, or a yes-or-no profit test. Closest: SCONE-bench, A1, CyberChainBench, V2E, EVMbench, BountyBench (Zhang et al., NeurIPS 2025)<!--ref:Zhang2025-BountyBench--><!--anchor:none:-->.

---

## 7. Unverified items

These items failed the verification rule. They do not support any claim in this review. The reasons are copied from the files.

### 7.1 Tier B (25 rows)

| Index ID | Title | Venue as recorded | Why unverified | File |
|---|---|---|---|---|
| `Mahmud2025-AIPatchBypass` | A Systematic Evaluation of AI-Generated Security Patches | IEEE AITest 2025 | Only the Semantic Scholar record could be opened | L2 |
| `Rawajfih2026-BeyondBypass` | Beyond Bypass: Measuring Vulnerability Regression in LLM-Generated Security Patches | IEEE AITest 2026 | Only the Semantic Scholar record; no arXiv version | L2 |
| `Gouville2026-AgenticChangesSecurity` | When AI Writes Code: Investigating Security Issues in Agentic Software Changes | MSR 2026 Mining Challenge | ACM returned HTTP 403; abstract read only in Semantic Scholar | L2 |
| `Melo2026-PreferVulnerable` | Do Language Models Prefer Vulnerable Code? | ICST 2026 [uncertain] | Only the Semantic Scholar record was readable | L3 |
| `Baralla2024-Copilot` | Assessing GitHub Copilot in Solidity Development | IEEE Access 2024 | Publisher and repository pages blocked | L4 |
| `Napoli2026-LightShadows` | Light and shadows of smart contract development with LLMs | Expert Systems with Applications 2026 | Summary from a search result, not an opened page | L4 |
| `Baralla2026-DeepSeekSolidity` | Reasoned or Rapid code? | Information and Software Technology 2026 | Summary from a search result | L4 |
| `Sun2026-SecChain` | SecChain: Operationalizing Security Guidelines for Multi-agent Smart Contract Generation | ASE 2026 | ACM DL blocked | L4 |
| `Kado2025-ObfuscatedRepair` | Automated Vulnerability Repair of Obfuscated and Non-Obfuscated Smart Contracts | IEEE PRDC 2025 | IEEE Xplore blocked | L7 |
| `Napoli2023-ChatGPTCorrection` | Evaluating ChatGPT for Smart Contracts Vulnerability Correction | IEEE COMPSAC 2023 | Repository and publisher pages blocked | L7 |
| `Gao2024-sGuardPlus` | sGuard+ | ACM TOSEM 2024 | ACM DL blocked | L7 |
| `So2023-SmartFix` | SmartFix | ESEC/FSE 2023 | ACM DL blocked | L7 |
| `Zhang2020-SmartShield` | SMARTSHIELD | SANER 2020 | IEEE Xplore blocked | L7 |
| `OldWine2026` | Just Old Wine in a New Bottle | ISSTA 2026 | Title seen only on the accepted-paper list | L9 |
| `SymRadar2026` | SymRadar: PoC-Centered Bounded Verification for Vulnerability Repair | ICSE 2026 | Title seen only on the accepted-paper list | L9 |
| `TraceGate2026` | TraceGate | ASE 2026 | Title seen only on the accepted-paper list | L9 |
| `Sun2025-ExploitMigration` | Learning from the Past: Real-World Exploit Migration for Smart Contract PoC Generation | ASE 2025 | Crossref record without an abstract | L9 |
| `Petke2024-PatchOverfit` | The Patch Overfitting Problem in Automated Program Repair | FSE 2024 Companion | Crossref record without an abstract | L9 |
| `Pinheiro2026-CVEBenchBlog` | I Tested Whether AI Can Fix Security Vulnerabilities | Blog post | No paper, PDF or publisher page; only the author's page | L11 |
| `Hao2013-BugOrObsoleteTest` | Is This a Bug or an Obsolete Test? | ECOOP 2013 | Abstract seen only in search snippets | S2 |
| `Zare2026-CopilotExperience` | GitHub Copilot and Code Security | HCII 2026 | No page with the abstract | S3a |
| `Zhang2026-PatchAudit` | PatchAudit | ACM CCS 2026 | No abstract online yet | S3b |
| `Gupta2026-Patchproof` | Patchproof: Exploit-grounded Evidence for Security Patch Correctness | SSRN 2026 | Google Scholar snippet only; SSRN returned HTTP 403 | S3b |
| `Solca2026-LeniencyConfound` | Who Judges the Judges? | IEEE Access 2026 | Full abstract not reachable | S3b |
| `Liu2026-RollGain` | Exploiting Ethereum Rollback Semantics | ISSTA 2026 | ACM DL blocked; abstract only in OpenAlex, which the protocol does not accept | T5 |

Three of these could matter to novelty once verified. Patchproof proposes exploit-grounded evidence for patch correctness (N3). PatchAudit finds faulty security patches at scale (N3). SymRadar centres repair verification on a PoC (N3). They should be reopened in round 4 or later.

### 7.2 Tier C (34 rows)

| Reason | Index IDs |
|---|---|
| IEEE Xplore blocked; abstract only from Semantic Scholar or OpenAlex | `Patel2024-AIvsHumanMetrics`, `Jamil2025-LLMvsHumanQuality` (L3); `Hensel2025-AutoCompletion`, `Daspe2024-BRAINS`, `Olivieri2025-Fabric`, `Akhtar2026-ICHORA`, `Cuncu2026-Solana`, `Napoli2024-COMPSAC`, `DeVito2025-AstraKode`, `Ji2025-SCGenAgent` (L4); `Ahmed2026-WorkflowSmells`, `Zhang2020-EthPloit`, `Park2012-SupplementaryFixes`, `Hu2025-NotExploited` (S1); `Yuan2025-MoEFix` (L7, S1); `Alam2026-AutoSCAR` (L7) |
| ACM DL blocked | `Li2024-CoSec`, `Siddiq2022-SecurityEval` (L1, Crossref record only); `Gu2010-BadFixes`, `Jiang2024-KernelVIC` (S1); `Guo2024-RLRep`, `Kado2026-RAWL` (L7); `Zhang2024-AccountingErrors` (L9); `Eick1992-FaultContent` (S3b, archived ACM page with no abstract) |
| Other publisher or host blocked | `Kiani2024-RepairSLR` (MDPI), `Li2025-HMF` (Springer), `Staley2026-MeasurementHazards` (journal site), `Huang2024-ReenRepair` (no page opened) (L7); `Deininger2026-FixingBreakingFaking` (MDPI; Crossref record only) (L6); `Liu2025-ChatGPTLogicVulns` (ScienceDirect) (S1) |
| Only a third-party record page | `Tan2016-AntiPatterns`, `You2017-SemFuzz` (S1) |
| Primary page blocked; details from secondary sources | `OpenAI2026-SWEbenchVerified` (S1) |
| No abstract online yet | `Xiang2026-FixToFlaw` (S3b) |

### 7.3 Unverified leads outside the index

Some items appear only as leads. None is used here. Examples: a 1Password study of 6,080 AI patches, seen only in news coverage (L11); reports of an Anthropic model building exploits on SCONE-bench, seen only in secondary sources (L5); Apiiro's original post, blocked by a bot check (L10); and a review-site summary of security-related AI pull requests with no authors or venue (L10).

---

## 8. Conflicts between search files that I resolved

| Item | What the files say | Resolution |
|---|---|---|
| EVMbench venue | L4 and L5 give an arXiv preprint. L2, L6 and L7 opened the PMLR page: ICML 2026, PMLR 306, pp. 125067–125099. L9 saw it in the ICML 2026 list. | ICML 2026. L5 and an OpenZeppelin blog post note that versions differ (117 or 120 vulnerabilities; Detect 45.9% or 45.6%). This review uses the paper's 117 and 45.9%. |
| SecRepoBench venue and year | L2 gives an arXiv preprint of 2025 and calls the workshop uncertain. L1 and L3 confirmed LLM4Code 2026 in Crossref (DOI 10.1145/3786181.3788703; L3 gives pp. 159–166). | LLM4Code 2026. |
| PoCo venue | L11 opened the arXiv page ("Under review") and found no published version. L5 reports a TOSEM DOI (10.1145/3816704) from Crossref. L9 saw the title in the ASE 2026 research-track list. | Cited as an arXiv preprint until a publisher page is opened. Both claimed venues are flagged. |
| ImpossibleBench venue | L6 gives an arXiv preprint. L2 and L11 opened the ICLR 2026 poster page; L9 also gives ICLR 2026. | ICLR 2026. |
| Bobadilla et al. year | L2, L5, L6, L7 and L11 give IEEE TSE 2025. L9 gives TSE 52(1), pp. 100–115, 2026 (journal issue). | IEEE TSE, online 2025, in issue 52(1) of 2026. |
| SmartPoC | L5, L6, L7 and L11 cite arXiv 2511.12993. L9 lists an ASE 2026 title, "Validating Smart Contract Vulnerability Findings through PoC Generation and Execution", but opened only the same arXiv page. L5 calls the ASE paper "distinct" but by the same team on the same topic. | One work for this review; the index row for the ASE title is treated as a duplicate. Cited as the arXiv preprint. |
| Karanjai et al. 2023 | L3 gives an arXiv preprint, "An Empirical Study of AI-based Smart Contract Creation". L4 gives BRAINS 2023 ("Who is Smarter?") from Crossref and Semantic Scholar. Both are arXiv 2308.02955. | One paper, BRAINS 2023. The index has two rows for it. |
| SolEval title and tier | The index has a tier A row (EMNLP 2025, "...Smart Contract Generation") and a tier B row (L5, "...Solidity Code Generation"). L4 notes the arXiv title differs. | One paper, EMNLP 2025, tier A. |
| A1 tier and venue | L5 rates it A (arXiv v4, January 2026). L2 and L7 rate it B; L2 notes that EVMbench cites it as Financial Cryptography 2026, which no agent opened. | arXiv preprint; tier A, the best tier given. |
| SCONE-bench tier and type | L5 rates it A as an Anthropic technical report. L2 and L10 rate it B as a research blog post. All opened the same page. | Grey literature; tier A. |
| Demystifying Exploitable Bugs (Zhang et al.) status | L5 and L10 opened the paper PDF (VERIFIED). L9 saw only a Crossref record (UNVERIFIED, tier C). | VERIFIED; tier A from L5. |
| Choi and Lee (Not All Input Helps) status | L7 marked it UNVERIFIED (ACM blocked; Semantic Scholar only), tier B. L9 opened the ICSE 2026 NIER programme page with the abstract, tier A. | VERIFIED, tier A. Its abstract gives no numbers. |
| Mohammadi and Bindschaedler (Whose Oracle Is It?) status | S1: UNVERIFIED (abstract only in OpenAlex). S3b: VERIFIED from the Semantic Scholar record. | Kept as VERIFIED, as the index does, with the caveat that only an index record was read. |
| CMod (Verifying Economic Security via Unintended Return) | S1: UNVERIFIED (Crossref record only). S3a: VERIFIED from the same Crossref record. L5's short list names the authors "Ye et al."; Crossref gives Rong, Li and Gu. | Authors Rong, Li and Gu. Status rests on an index record. |
| DeFiSent status | S3a verified it from the Crossref record of the SSRN posting; the full text was blocked. | Kept in the closest-papers table, because it can only weaken novelty claims. Facts beyond the abstract are not used. |
| Other papers verified only from index records | S3a, S3b and L5's short tier C list accepted Semantic Scholar, OpenAlex or Crossref records; S1, L1, L3, L4, L6, L7 and T5 did not. This explains why `Napoli2023-ChatGPTCorrection`, `Kado2025-ObfuscatedRepair`, `Yuan2025-MoEFix` and `Sun2025-ExploitMigration` are VERIFIED in L5's short list but UNVERIFIED in the index. | The index status is used. The stricter rule is applied in section 7. |
| Fault-enforcing test numbers | L6 and L11 give 8% to 17% fault-enforcing and 2.4% to 4.8% fault-revealing. S2, from Table 3 of the PDF, gives 16.9%, 8.4% and 16.9%, and 2.6%, 2.4% and 4.8%, and adds that the faults were 60,780 injected mutants. | S2's numbers, which come from the full text. |
| Test overfitting on SWE-bench (Ahmed et al.) dataset | L6 says 449 SWE-bench Verified instances. L8 and L11, from the full text, say 449 TDD-Bench Verified issues drawn from SWE-bench Verified. | TDD-Bench Verified. |
| SusVibes size | The v4 paper gives 186 tasks, 100 repositories and 79 CWEs (L1, L2). FALCON describes 186 tasks and 77 CWEs (L2). A vendor leaderboard describes 200 tasks from 108 projects and 77 CWE types (S3a). | The paper's v4 counts. |
| Asare et al. venue detail | L1: EMSE (Crossref). L3: EMSE 28, article 129. L9: EMSE 28(6), article 129, from the Springer page. L8 and L10: accepted, per the arXiv comment. | Empirical Software Engineering 28(6), article 129, 2023. |
| Tier ratings of tier A papers | Jesse et al.: L1 B, L3 A. Last Secure Code Benchmark: L3 and L11 B, L1 and L2 A. Sajadi et al.: L3 B, L2 A. Storhaug et al.: L1 B, L4 A. Bobadilla et al.: L2 and L11 B, others A. V2E: L5 B, L9 A. SmartPoC: L11 B, L5 A. PatchBench, PVBench and Le et al.: L2 B, L6 and L11 A. Germano and Duarte: L2 and L5 B, L4 and L7 A. Opad: S1 C, C1 A. | The best tier given, as in the index. A reviewer could cite any of these against the project, so the higher tier is the safer choice. |
| Tier ratings in round 2 and round 3 | ContraFix, TestEvo-Bench, Unearned Passes and SCAR: tier B in S2 or S3a, "at most C" in S3b. Metrics Failure: "at most C" in S3b, tier B in T3. LiquiLM, SCALM, LLM-SmartAudit and SmartAuditFlow: tier B in C1, tier C in T2, T4 or L5. Q&AEval: tier B in S1, screened out by S3a as having "no human version"; T1 confirmed S1's reading. | The index keeps the best tier. Section 3 notes that C1's tier B finds on smart-contract auditing depend on the looser rule. |

---

## 9. Appendix

### Appendix A. Counts from the merged index

Counts by tier and status, from `lit/master_index.tsv` (861 rows):

| Tier | VERIFIED | UNVERIFIED | Total |
|---|---|---|---|
| A | 50 | 0 | 50 |
| B | 381 | 25 | 406 |
| C | 371 | 34 | 405 |
| Total | 802 | 59 | 861 |

Rows by the round in which they first entered the index, for tiers A and B:

| Round | Tier A rows | Tier B rows |
|---|---|---|
| 1 | 44 | 276 (19 unverified) |
| 2 | 3 | 89 (5 unverified) |
| 3 | 3 | 41 (1 unverified) |

The index merges rows by title, so at least eight rows repeat another row under a different title: SmartPoC (2 rows), A1 (a tier A and a tier B row), SCONE-bench (one tier A and two tier B rows), SolEval (a tier A and a tier B row), Karanjai et al. 2023 (2 rows), SecCodePLT (2 rows) and DeFinery (2 rows). The 49 tier A papers in section 5 are the 50 tier A rows less the SmartPoC duplicate.

### Appendix B. Search files

Round 1:
- The secure code generation file (`lit/r1_L1_secure_codegen.md`): security of LLM-written code and techniques for secure generation.
- The repository and agent benchmark file (`lit/r1_L2_repo_agent_benchmarks.md`): repository-level and agent security benchmarks, and the security of agent-written code.
- The human-versus-AI file (`lit/r1_L3_human_vs_ai.md`): AI-written code compared with human-written code.
- The Solidity code generation file (`lit/r1_L4_solidity_codegen.md`): LLMs and agents that write Solidity.
- The smart-contract exploits and datasets file (`lit/r1_L5_sc_exploits_datasets.md`): datasets, exploit and PoC generation, and LLM auditing.
- The PoV-guided repair file (`lit/r1_L6_pov_guided_repair.md`): repair guided by an exploit or failing test, overfitting, held-out tests and repair inputs.
- The smart-contract repair file (`lit/r1_L7_sc_repair.md`).
- The methodology file (`lit/r1_L8_methodology.md`): tracing introducing commits, contamination, task texts, test adequacy, LLM judges and case-control designs.
- The DBLP venue sweep (`lit/r1_L9_dblp_sweep.md`).
- The significance file (`lit/r1_L10_significance.md`): incidents, surveys, losses, audit platforms and industry measurements.
- The Codex leads file (`lit/r1_L11_codex_leads.md`).

Round 2:
- The snowballing file (`lit/r2_S1_snowball.md`): citations and references of 15 anchor papers.
- The tests-that-assert-bugs file (`lit/r2_S2_tests_assert_bugs.md`).
- The first round-1 leads file (`lit/r2_S3a_leads.md`): leads from the L10, L11 and L1 to L5 sections.
- The second round-1 leads file (`lit/r2_S3b_leads.md`): leads from the L6, L8 and L9 sections, plus sweeps on capture-recapture, case-control designs and selection bias.

Round 3:
- The human-versus-AI saturation file (`lit/r3_T1_human_vs_ai.md`).
- The 2026 smart-contract file (`lit/r3_T2_smart_contracts_2026.md`).
- The repair-and-execution file (`lit/r3_T3_repair_execution.md`).
- The requests, judges and differential testing file (`lit/r3_T4_requests_judges.md`).
- The 2026 venue-list file (`lit/r3_T5_venues_2026.md`).
- The Codex gap file (`lit/r3_C1_codex_gap.md`).

Supporting files: the project brief (`lit/project_brief.md`), the search protocol (`lit/search_protocol.md`), the round-1 leads list (`lit/leads_round1.md`), the merged index (`lit/master_index.tsv`) and the earlier partial index used in round 2 (`lit/master_index_partial.tsv`).

### Appendix C. References cited, with the URL each agent opened

Each entry gives the index ID, the authors, the title, the venue and year, and the URL opened. Papers are VERIFIED unless marked as grey literature.

**Tier A**
- `Chen2026-SecureVibeBench`: Junkai Chen et al. SecureVibeBench: Benchmarking Secure Vibe Coding of AI Agents via Reconstructing Vulnerability-Introducing Scenarios. ACL 2026. https://arxiv.org/abs/2509.22097 ; https://aclanthology.org/2026.acl-long.1107/
- `Zhao2026-SusVibes`: Songwen Zhao et al. Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks. ICML 2026. https://arxiv.org/abs/2512.03262 ; https://proceedings.mlr.press/v306/zhao26ax.html
- `Shen2025-SecRepoBench`: Chihao Shen et al. SecRepoBench: Benchmarking Code Agents for Secure Code Completion in Real-World Repositories. LLM4Code 2026. https://arxiv.org/abs/2504.21205 ; https://api.crossref.org/works/10.1145/3786181.3788703
- `Wu2026-LastSecureCode`: Tianyi Wu et al. Last Secure Code Benchmark: Is the Code You Vibe Secure? arXiv preprint 2026. https://arxiv.org/abs/2610.14766
- `Vero2025-BaxBench`: Mark Vero et al. BaxBench: Can LLMs Generate Correct and Secure Backends? ICML 2025. https://arxiv.org/abs/2502.11844 ; https://proceedings.mlr.press/v267/vero25a.html
- `Asare2023-CopilotVsHumans`: Owura Asare, Meiyappan Nagappan, N. Asokan. Is GitHub's Copilot as Bad as Humans at Introducing Vulnerabilities in Code? Empirical Software Engineering 2023. https://arxiv.org/abs/2204.04741 ; https://link.springer.com/article/10.1007/s10664-023-10380-1
- `Jesse2023-SStuBs`: Kevin Jesse et al. Large Language Models and Simple, Stupid Bugs. MSR 2023. https://arxiv.org/abs/2303.11455
- `Guo2025-BugReplicators`: Liwei Guo et al. LLMs are Bug Replicators. arXiv preprint 2025. https://arxiv.org/abs/2503.11082
- `Sajadi2025-PatchSecurity`: Amirali Sajadi, Kostadin Damevski, Preetha Chatterjee. How Safe Are AI-Generated Patches? arXiv preprint 2025. https://arxiv.org/abs/2507.02976
- `Talha2026-SNRA`: Muhammad Talha, Vishwaa Shah. To Vibe or Not to Vibe: An Empirical Security Analysis of AI-Generated Code Patches. Unpublished manuscript 2026. https://www.tjbravo.com/research/to-vibe-or-not-to-vibe ; https://www.tjbravo.com/papers/to-vibe-or-not-to-vibe.pdf
- `Chen2025-FeatBench`: Haorui Chen et al. FeatBench. arXiv preprint 2025. https://arxiv.org/abs/2509.22237
- `Aleithan2024-SWEBenchPlus`: Reem Aleithan et al. SWE-Bench+: Enhanced Coding Benchmark for LLMs. arXiv preprint 2024. https://arxiv.org/abs/2410.06992
- `Chen2026-SolAgent`: Wei Chen et al. SolAgent: A Specialized Multi-Agent Framework for Solidity Code Generation. arXiv preprint 2026. https://arxiv.org/abs/2601.23009
- `Peng2025-SolEval`: Zhiyuan Peng et al. SolEval. EMNLP 2025. https://aclanthology.org/2025.emnlp-main.218/
- `Storhaug2023-VCD`: André Storhaug et al. Efficient Avoidance of Vulnerabilities in Auto-completed Smart Contract Code Using Vulnerability-constrained Decoding. ISSRE 2023. https://arxiv.org/abs/2309.09826
- `Khalid2025-GenAITools`: Shawal Khalid, Chris Brown. Evaluating Capabilities and Perspectives of Generative AI Tools in Smart Contract Development. BSCI '25. https://vtechworks.lib.vt.edu/handle/10919/137729
- `Wang2026-EVMbench`: Justin Wang et al. EVMbench: Evaluating AI Agents on Smart Contract Security. ICML 2026. https://proceedings.mlr.press/v306/wang26k.html ; https://arxiv.org/abs/2603.04915
- `Peng2026-ReEvalEVMBench`: Chaoyuan Peng et al. Re-Evaluating EVMBench. arXiv preprint 2026. https://arxiv.org/abs/2603.10795
- `Huang2026-CyberChainBench`: Jintao Huang et al. CyberChainBench. arXiv preprint 2026. https://arxiv.org/abs/2606.26216
- `Xiao2025-SCONEbench`: Winnie Xiao et al. AI agents find $4.6M in blockchain smart contract exploits (SCONE-bench). Anthropic research post 2025, grey literature. https://www.anthropic.com/research/smart-contracts
- `Gervais2025-A1`: Arthur Gervais, Liyi Zhou. AI Agent Smart Contract Exploit Generation. arXiv preprint 2025. https://arxiv.org/abs/2507.05558
- `a16z2026-DeFiExploits`: Park, Gleason. Can AI agents actually pull off DeFi exploits? a16z crypto blog 2026, grey literature. https://a16zcrypto.com/posts/article/ai-agents-defi-exploits
- `Andersson2025-PoCo`: Vivi Andersson et al. PoCo: Agentic Proof-of-Concept Exploit Generation for Smart Contracts. arXiv preprint 2025. https://arxiv.org/abs/2511.02780
- `Chen2025-SmartPoC`: Longfei Chen et al. SmartPoC: Generating Executable and Validated PoCs for Smart Contract Bug Reports. arXiv preprint 2025. https://arxiv.org/abs/2511.12993
- `Zhang2026-V2E`: Jingwen Zhang et al. V2E. FSE 2026. https://arxiv.org/abs/2604.13611
- `Xiao2026-ReX`: Xiao et al. Prompt to Pwn: Automated Exploit Generation for Smart Contracts. ACISP 2026. https://arxiv.org/abs/2508.01371
- `Su2026-TracExp`: Su et al. From Transactions to Exploits. arXiv preprint 2026. https://arxiv.org/abs/2601.16681
- `Kong2026-Knowdit`: Kong et al. Knowdit. arXiv preprint 2026. https://arxiv.org/abs/2603.26270
- `Zhang2023-ExploitableBugs`: Zhuo Zhang et al. Demystifying Exploitable Bugs in Smart Contracts. ICSE 2023. https://raw.githubusercontent.com/ZhangZhuoSJTU/Web3Bugs/main/papers/icse23.pdf
- `Bobadilla2025-ExploitMitigation`: Sofia Bobadilla, Monica Jin, Martin Monperrus. Do Automated Fixes Truly Mitigate Smart Contract Exploits? IEEE TSE 2025. https://arxiv.org/abs/2501.04600
- `Germano2025-DeFiRepair`: Lucas Bastos Germano, Julio Cesar Duarte. Repairing DeFi Vulnerabilities: Benchmarking LLMs with Executable Solidity Exploits. WebMedia 2025 workshop. https://sol.sbc.org.br/index.php/webmedia_estendido/article/view/38210
- `Xiao2026-DeFiSent`: Yinhao Xiao et al. DeFiSent. SSRN preprint 2026. https://api.crossref.org/works/10.2139/ssrn.7117519
- `Iranmanesh2026-P2Patch`: Mohsen Iranmanesh et al. P2Patch: Exploit-Guided Vulnerability Repair. arXiv preprint 2026. https://arxiv.org/abs/2610.20245
- `Shen2026-PatchBench`: Chihao Shen et al. PatchBench. arXiv preprint 2026. https://arxiv.org/abs/2609.04075
- `Yu2026-PVBench`: Zheng Yu et al. Patch Validation in Automated Vulnerability Repair. arXiv preprint 2026. https://arxiv.org/abs/2603.06858
- `Wang2026-SlicePatch`: Chenlin Wang, Wei Meng. Web Application Vulnerability Repair via Context-Aware Fault Localization and Directed Differential Fuzzing. IEEE S&P 2026. https://seclab.cse.cuhk.edu.hk/papers/sp26-SlicePatch.pdf
- `Alsaid2026-TerraProbe`: Manar Alsaid et al. TerraProbe. arXiv preprint 2026. https://arxiv.org/abs/2606.26590
- `Smith2015-CureWorse`: Edward K. Smith et al. Is the Cure Worse Than the Disease? ESEC/FSE 2015. https://people.cs.umass.edu/~brun/pubs/pubs/Smith15fse.pdf
- `Yang2017-Opad`: Jinqiu Yang et al. Better Test Cases for Better Automated Program Repair. ESEC/FSE 2017. https://www.cs.purdue.edu/homes/lintan/publications/opad-fse17.pdf
- `Ruan2024-EvoRepair`: Haifeng Ruan et al. Evolutionary Testing for Program Repair. ICST 2024. https://abhikrc.com/pdf/ICST24.pdf
- `Ahmed2026-TestOverfitting`: Toufique Ahmed et al. Investigating Test Overfitting on SWE-bench. FSE Companion 2026. https://arxiv.org/abs/2511.16858
- `Liang2026-SecTDD`: Yunhao Liang et al. Security Tests as Executable Specifications for LLM Code Generation. arXiv preprint 2026. https://arxiv.org/abs/2608.09740
- `Le2026-PatchingBenchReliability`: Dang K Le, Wenxuan Shi, Xinyu Xing. On the Reliability of LLM-Based Vulnerability Patching Benchmarks. arXiv preprint 2026. https://arxiv.org/abs/2610.10150
- `Lin2026-ToRunOrNotToRun`: Zhihao Lin et al. To Run or Not to Run. ISSTA 2026. https://arxiv.org/abs/2606.26978
- `Mierczuk2026-FLAWED`: Axel Mierczuk et al. Frontier Models' Vulnerability Patches are Often F.L.A.W.E.D. 1Password industry report 2026, grey literature. https://1password.com/files/resources/frontier-models-vulnerability-patches-flawed.pdf
- `Zhong2026-ImpossibleBench`: Ziqian Zhong, Aditi Raghunathan, Nicholas Carlini. ImpossibleBench. ICLR 2026. https://arxiv.org/abs/2510.20270 ; https://iclr.cc/virtual/2026/poster/10009390
- `Li2026-ORACLESWE`: Kenan Li et al. ORACLE-SWE. arXiv preprint 2026. https://arxiv.org/abs/2604.07789
- `Choi2026-NotAllInputHelps`: Dongwook Choi, Eunseok Lee. Not All Input Helps. ICSE 2026 NIER. https://conf.researchr.org/details/icse-2026/icse-2026-nier/49/Not-All-Input-Helps-What-Information-Should-We-Feed-to-LLMs-for-Vulnerability-Repair
- `Pearce2023-ZeroShotVulnRepair`: Hammond Pearce et al. Examining Zero-Shot Vulnerability Repair with Large Language Models. IEEE S&P 2023. https://arxiv.org/abs/2112.02125

**Tier B and tier C**
- `Peng2025-CWEval`: Jinjun Peng et al. CWEval. LLM4Code 2025. https://arxiv.org/abs/2501.08200
- `Lian2026-ASE`: Keke Lian et al. A.S.E. Findings of ACL 2026. https://aclanthology.org/2026.findings-acl.1569/
- `Wang2026-RealSecBench`: Yanlin Wang et al. RealSec-bench. Findings of ACL 2026. https://aclanthology.org/2026.findings-acl.1786/
- `PaxtonFear2026-SemgrepSusVibes`: Katie Paxton-Fear. Claude Opus 5.5 Writes Working Code but Only Half of It Is Secure. Semgrep blog 2026, grey literature, tier C. https://semgrep.dev/blog/2026/claude-opus-5-5-susvibes-benchmark
- `Wang2026-AuraForge`: Danqing Wang et al. AuraForge. arXiv preprint 2026. https://arxiv.org/abs/2610.00850
- `Compagna2026-AgentSecurityLeague`: Luca Compagna. Is AI Coding Safe? Introducing the Agent Security League. Endor Labs blog 2026, grey literature. https://www.endorlabs.com/learn/is-ai-coding-safe-introducing-the-agent-security-league
- `Al-Kaswan2026-ModelSeeModelDo`: Ali Al-Kaswan et al. Model See, Model Do? MSR 2026. https://arxiv.org/abs/2601.10496
- `Wu2025-SoKAI4Code`: Qilong Wu et al. SoK: Understanding (New) Security Issues Across AI4Code Use Cases. arXiv preprint 2025. https://arxiv.org/abs/2512.18456
- `Cotroneo2025-HumanVsAI`: Domenico Cotroneo et al. Human-Written vs. AI-Generated Code. ISSRE 2025. https://arxiv.org/pdf/2508.21634
- `Mahmud2026-IllusionOfSafety`: Saif Mahmud et al. The Illusion of Safety. arXiv preprint 2026. https://arxiv.org/abs/2607.00107
- `Hamer2024-ChatGPTvsSO`: Sivana Hamer et al. Just another copy and paste? IEEE SPW 2024. https://export.arxiv.org/api/query?id_list=2403.15600
- `Toran2026-QAEval`: Markus Toran et al. Q&AEval. SVM 2026 workshop. https://www.athene-center.de/forschung/publikationen/q-a-eval-benchmarking-secure-coding-ability-of-llm-5526
- `Shaw2026-ComparedToWhat`: Animesh Shaw. Compared to What? arXiv preprint 2026. https://arxiv.org/abs/2608.28021
- `Perry2023-InsecureCode`: Neil Perry et al. Do Users Write More Insecure Code with AI Assistants? CCS 2023. https://arxiv.org/abs/2211.03622
- `Sandoval2023-LostAtC`: Gustavo Sandoval et al. Lost at C. USENIX Security 2023. https://www.usenix.org/conference/usenixsecurity23/presentation/sandoval
- `Asare2024-UserCopilot`: Owura Asare et al. A User-centered Security Evaluation of Copilot. ICSE 2024. https://arxiv.org/abs/2308.06587
- `Jost2026-Gemini`: Nadine Jost et al. The Impact of AI-Assisted Development on Software Security. arXiv preprint 2026. https://arxiv.org/abs/2603.15298
- `Xia2026-PostMergeFate`: Chunqiu Steven Xia, Courtney Miller. Do These Violent Delights Have Violent Ends? arXiv preprint 2026. https://arxiv.org/abs/2607.09902
- `Kraishan2026-FiveAgents`: Obada Kraishan. Not All Agents Are Equal. arXiv preprint 2026. https://arxiv.org/abs/2609.17598
- `Le2026-AgenticPRSecurity`: Minh Nguyen Quang Le et al. On the Security of Agentic Pull Requests in GitHub. FPS 2026, per the authors' page. https://ldklab.github.io/assets/papers/fps26-prs.pdf
- `Goel2026-SmartEval`: Abhinav Goel et al. SmartEval. arXiv preprint 2026. https://arxiv.org/html/2605.09610
- `Egli2026-HowToCompare`: Jasmine Egli, Rebecca Balebako. How to Compare the Security of Code Written by Humans to LLM-generated Code. arXiv preprint 2026. https://arxiv.org/abs/2606.00186
- `Ullah2025-CVEGenie`: Saad Ullah et al. From CVE Entries to Verifiable Exploits. arXiv preprint 2025. https://arxiv.org/abs/2509.01835
- `Li2024-SAST`: Li et al. Static Application Security Testing (SAST) Tools for Smart Contracts: How Far Are We? FSE 2024. https://arxiv.org/abs/2404.18186
- `Chaliasos2024-Tools`: Stefanos Chaliasos et al. Smart Contract and DeFi Security Tools: Do They Meet the Needs of Practitioners? ICSE 2024. https://arxiv.org/abs/2304.02981
- `Perez2021-VulnNotExploited`: Perez, Livshits. Smart Contract Vulnerabilities: Vulnerable Does Not Imply Exploited. USENIX Security 2021. https://www.usenix.org/conference/usenixsecurity21/presentation/perez
- `Delvecchio2026-SolBehave`: Giovanni Pio Delvecchio et al. SolBehave. arXiv preprint 2026. https://export.arxiv.org/api/query?id_list=2610.18745
- `Salzano2025-BeyondSimilarity`: Francesco Salzano et al. Beyond Code Similarity. arXiv preprint 2025. https://export.arxiv.org/api/query?id_list=2511.16224
- `Aminnezhad2026-ExploitGen`: Aysheh Aminnezhad. ExploitGen. Master's thesis, ÉTS Montréal, 2026. https://espace.etsmtl.ca/id/eprint/4120/
- `OpenZeppelin2026-EVMbenchAudit`: OpenZeppelin Security. OpenZeppelin audit of OpenAI's EVMbench. Company blog 2026, grey literature. https://openzeppelin.com/news/openai-evmbench-audit
- `Khalid2026-AuditTransfer`: Shawal Khalid et al. Do Smart Contract Auditing Results Transfer Across Datasets? ESEM 2026. https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESEM.2026.45
- `Susan2026-LLMStaticBench`: Stefan-Claudiu Susan et al. Benchmarking LLM-Based Static Analysis for Secure Smart Contract Development. IEEE COMPSAC 2026. https://arxiv.org/abs/2605.11163
- `Schefold2026-DeceptionDelta`: Timo Schefold. The Deception Delta. ACM CCS 2026. https://arxiv.org/abs/2609.14098
- `Parasaram2025-FactSelection`: Nikhil Parasaram et al. The Fact Selection Problem in LLM-Based Program Repair. ICSE 2025. https://arxiv.org/abs/2404.05520
- `Bansal2026-VIBEPASS`: Srijan Bansal et al. Can Vibe Coders Really Pass the Vibe Check? Findings of EMNLP 2026, per the programme spreadsheet [uncertain]. https://arxiv.org/abs/2603.15921
- `Zhao2026-RewardHackingCodeAgents`: Bingchen Zhao et al. Reward Hacking in Self-Improving Code Agents. ICLR 2026 workshop. https://iclr.cc/virtual/2026/10018648
- `Xu2026-PatchingArchitectures`: Qingxiao Xu et al. A Systematic Study of LLM-Based Architectures for Automated Patching. arXiv preprint 2026. https://arxiv.org/html/2603.01257
- `Liu2025-VulDebugger`: Zhengyao Liu et al. Agent That Debugs. arXiv preprint 2025. https://arxiv.org/abs/2504.07634
- `Xu2026-ValidationEvidence`: Xiaonan Xu, Wenjing Wu. Validation Evidence in LLM Repair Agents. arXiv preprint 2026. https://arxiv.org/abs/2607.28871
- `Charoosaei2026-FaultEnforcingTests`: Mohammadali Charoosaei, Cedric Richter, Mike Papadakis. On the Risks of using LLM-Generated Tests for Regression Testing. arXiv preprint 2026. https://arxiv.org/abs/2610.11835 ; https://arxiv.org/pdf/2610.11835
- `Konstantinou2026-CodingBeforeTesting`: Michael Konstantinou et al. On the risk of coding before testing. arXiv preprint 2026. https://arxiv.org/abs/2607.05139
- `Mathews2024-TestGenDesignChoices`: Noble Saji Mathews, Meiyappan Nagappan. Design choices made by LLM-based test generators prevent them from finding bugs. arXiv preprint 2024. https://arxiv.org/abs/2412.14137
- `Fraser2015-GeneratedTestsHelp`: Gordon Fraser et al. Does Automated Unit Test Generation Really Help Software Testers? ACM TOSEM 2015. https://eprints.whiterose.ac.uk/96274/1/j15.pdf
- `Vahabzadeh2015-TestBugs`: Arash Vahabzadeh et al. An Empirical Study of Bugs in Test Code. ICSME 2015. https://people.ece.ubc.ca/amesbah/resources/papers/icsme15.pdf
- `Biyani2026-SpecGuard`: Param Biyani, Krishnamurthy Dvijotham. SpecGuard. arXiv preprint 2026. https://arxiv.org/abs/2610.09159
- `Li2026-SWEResidual`: Jinze Li et al. SWE-Residual. arXiv preprint 2026. https://arxiv.org/html/2610.25899
- `Chen2026-TestPrune`: Yang Chen et al. Can Old Tests Do New Tricks for Resolving SWE Issues? FSE 2026. https://arxiv.org/abs/2510.18270
- `Shang2026-TEBench`: Ye Shang et al. Breaking, Stale, or Missing? arXiv preprint 2026. https://arxiv.org/abs/2605.06125
- `Mohammadi2026-WhoseOracle`: Bardia Mohammadi, Laurent Bindschaedler. Whose Oracle Is It? APR 2026 workshop. https://www.semanticscholar.org/paper/2ccce93d6f9144e0a4826e53482c41e893d98d28
- `Wang2026-OracleMutable`: Xisen Wang et al. The Oracle Is Mutable. NeurIPS 2026 workshop. https://neurips.cc/virtual/2026/173042
- `Thornton2026-AdversarialComments`: Scott Thornton. Can Adversarial Code Comments Fool AI Security Reviewers. arXiv preprint 2026. https://arxiv.org/abs/2602.16741
- `Han2026-TDFlow`: Kevin Han et al. TDFlow. EACL 2026. https://arxiv.org/abs/2510.23761
- `Groce2020-ActualFlaws`: Alex Groce et al. What are the Actual Flaws in Important Smart Contracts? FC 2020, tier C. https://arxiv.org/abs/1911.07567
- `Lyu2024-SZZLinux`: Yunbo Lyu et al. Evaluating SZZ Implementations: An Empirical Study on the Linux Kernel. IEEE TSE 2024. https://arxiv.org/abs/2308.05060
- `Rezk2022-GhostCommits`: Christophe Rezk et al. The Ghost Commit Problem. IEEE TSE 2022. https://www.semanticscholar.org/paper/56206042d03206961be96f97b411de48f5273a84
- `Iannone2023-SecretLife`: Emanuele Iannone et al. The Secret Life of Software Vulnerabilities. IEEE TSE 2023. https://www.semanticscholar.org/paper/bcbfc2eefe6e278274052f52a5535d7a3c0ce318
- `Risse2026-AgentBIC`: Niklas Risse, Marcel Böhme. LLM-Based Agents for Identifying Bug-Introducing Commits. ASE 2026. https://arxiv.org/abs/2603.29378
- `MaesBermejo2024-HuntingBugs`: Michel Maes-Bermejo et al. Hunting bugs. Empirical Software Engineering 2024. https://www.semanticscholar.org/paper/281b69ab0b7ac5a69d7b61576dce451fe5bfbd18
- `Dozono2025-OSSContamination`: Kohei Dozono et al. Should We Evaluate LLM Based Security Analysis Approaches on Open Source Systems? ASE 2025. https://api.openalex.org/works/doi:10.1109/ase63991.2025.00265
- `Liang2026-SWEbenchIllusion`: Shanchao Liang et al. The SWE-Bench Illusion. ICSE-SEIP 2026. https://arxiv.org/abs/2506.12286
- `Hariharan2024-RethinkingCyberSecEval`: Suhas Hariharan et al. Rethinking CyberSecEval. arXiv preprint 2024. https://arxiv.org/abs/2411.08813
- `Sternfeld2026-PromptFragility`: Alexander Sternfeld et al. Minimal Prompt Perturbations Lead to Code Vulnerabilities. arXiv preprint 2026. https://arxiv.org/abs/2605.29737
- `Liu2026-ChromeSecBench`: Yue Liu et al. When AI Takes the Wheel. ICSE 2026. https://arxiv.org/abs/2510.16823
- `Li2026-UsabilityWeapon`: Yue Li et al. Usability as a Weapon. arXiv preprint 2026. https://arxiv.org/abs/2605.10133
- `Kim2026-RealSWE`: Gyuhyeong Kim et al. RealSWE. arXiv preprint 2026. https://arxiv.org/abs/2608.27831
- `Panickssery2024-SelfPreference`: Arjun Panickssery et al. LLM Evaluators Recognize and Favor Their Own Generations. NeurIPS 2024. https://arxiv.org/abs/2404.13076
- `Li2026-PreferenceLeakage`: Dawei Li et al. Preference Leakage. ICLR 2026. https://arxiv.org/abs/2502.01534
- `Li2026-FrozenJudges`: Jiapeng Li. Frozen Judges, Moving Agents. arXiv preprint 2026. https://arxiv.org/abs/2609.34198
- `Tal2026-VulnBenchJS`: Liran Tal et al. Snyk VulnBench JS 1.0. arXiv preprint 2026. https://arxiv.org/abs/2606.15762
- `Lin2026-AgreementWithoutAccuracy`: Hon-Ren Lin. Agreement Without Accuracy. OSF preprint 2026. https://api.openalex.org/works/doi:10.31235/osf.io/n3zhf_v1
- `Briand2000-CaptureRecapture`: Lionel C. Briand et al. A comprehensive evaluation of capture-recapture models for estimating software defect content. IEEE TSE 2000. https://api.openalex.org/works/doi:10.1109/32.852741
- `ElEmam2001-TwoInspectors`: K. El Emam, Oliver Laitenberger. Evaluating capture-recapture models with two inspectors. IEEE TSE 2001. https://api.openalex.org/works/doi:10.1109/32.950319
- `Geer2015-Undiscovered`: Dan Geer. For Good Measure: The Undiscovered. USENIX ;login: 2015, column, tier C. https://usenix.org/system/files/login/articles/login_apr15_12_geer.pdf
- `Paul2021-CaseControlChromium`: Rajshakhar Paul et al. Why Security Defects Go Unnoticed during Code Reviews? ICSE 2021. https://arxiv.org/abs/2102.06909
- `Allodi2014-CaseControlCVSS`: Luca Allodi, Fabio Massacci. Comparing Vulnerability Severity and Exploits Using Case-Control Studies. ACM TISSEC 2014. https://arxiv.org/abs/1301.1275
- `Feng2026-CaseControlEcosystems`: Yuan Feng et al. A methodology to perform cross-ecosystems case-control security studies. Empirical Software Engineering 2026. https://www.semanticscholar.org/paper/340ffb255311ce14a49f0bdf4d977383963144cd
- `Coston2022-GeometricOddsRatio`: Amanda Coston, Edward H. Kennedy. The role of the geometric mean in case-control studies. arXiv preprint 2022, tier C. https://arxiv.org/abs/2207.09016
- `Bird2009-FairBalanced`: Christian Bird et al. Fair and Balanced? Bias in Bug-Fix Datasets. ESEC/FSE 2009. https://www.cs.ucdavis.edu/~filkov/papers/biasbusters.pdf
- `Dristi2026-DiffFuzzRefactor`: Simantika Bhattacharjee Dristi, Matthew B. Dwyer. A Differential Fuzzing-Based Evaluation of Functional Equivalence in LLM-Generated Code Refactorings. LLMTrust 2026 workshop. https://arxiv.org/abs/2602.15761
- `Bodell2023-Diffusc`: William Bodell. Differential fuzz testing upgradeable smart contracts with Diffusc. Trail of Bits blog 2023, grey literature. https://blog.trailofbits.com/2023/07/07/differential-fuzz-testing-upgradeable-smart-contracts-with-diffusc/
- `Toman2025-Concordance`: John Toman. Concordance: Automatically Simplifying Smart Contracts. Certora blog 2025, grey literature. https://www.certora.com/blog/concordance-automatically-simplifying-smart-contracts
- `Ludwig2026-ShortcuttingTheFix`: Nikolai Ludwig et al. Shortcutting the Fix. arXiv preprint 2026. https://arxiv.org/abs/2609.06780
- `Luo2026-UnearnedPasses`: Weijun Luo et al. Maintaining Benchmarks Against Increasingly Capable Agents. arXiv preprint 2026. https://arxiv.org/abs/2609.34262
- `Farinha2026-GovernedRequirements`: Pedro Farinha. Applying Security by Design at the Point of Execution. arXiv preprint 2026. https://arxiv.org/abs/2610.10659
- `Wu2026-ALIBI`: Zixuan Wu, Cristina Nita-Rotaru. ALIBI. arXiv preprint 2026. https://arxiv.org/abs/2607.24964
- `Prasad2026-BAITBENCH`: Pradyumna Shyama Prasad et al. BAITBENCH. arXiv preprint 2026. https://arxiv.org/abs/2608.30724
- `Zhang2025-BountyBench`: Andy K. Zhang et al. BountyBench. NeurIPS 2025. https://arxiv.org/abs/2505.15216

**Significance sources (mostly grey literature)**
- `Solidity2026-Survey2025`: Solidity team. Solidity Developer Survey 2025 Results. 2026, grey literature. https://soliditylang.org/blog/2026/04/15/solidity-developer-survey-2025-results/
- `GitHub2025-Octoverse`: GitHub. Octoverse 2025. Grey literature. https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- `Li2026-AIDev`: Hao Li, Haoxiang Zhang, Ahmed E. Hassan. AIDev: Studying AI Coding Agents on GitHub. arXiv preprint 2026, tier C. https://arxiv.org/abs/2602.09185
- `Immunefi2026-Scoreboard`: Immunefi. The Ecosystem Vulnerability Scoreboard. 2026, grey literature. https://immunefi.com/blog/research/the-ecosystem-vulnerability-scoreboard-6-years-of-defi-loss-data/
- `DeFiLlama2026-Hacks`: DeFiLlama hacks dataset, with the computation done by the L10 agent. 2026, grey literature. https://api.llama.fi/hacks
- `CertiK2026-Hack3dH1`: CertiK. Hack3d H1 2026 Report. Grey literature. https://www.certik.com/blog/certik-hack3d-h1-2026-report
- `Gattermayer2026-ack3`: Josef Gattermayer et al. The ack3 H1 2026 DeFi Incident Dataset. arXiv preprint 2026. https://arxiv.org/abs/2608.13792
- `Zhou2023-SoKDeFi`: Liyi Zhou et al. SoK: Decentralized Finance (DeFi) Attacks. IEEE S&P 2023. https://arxiv.org/abs/2208.13035
- `Moonwell2026-MIPX43`: Anthias Labs and news coverage. MIP-X43 cbETH Oracle Incident Summary. 2026, grey literature. https://forum.moonwell.fi/t/mip-x43-cbeth-oracle-incident-summary/2068 ; https://github.com/moonwell-fi/moonwell-contracts-v2/pull/578
- `GTSSLab2026-VibeSecurityRadar`: Hanqing Zhao and colleagues, Georgia Tech. Vibe Security Radar. Grey literature. https://vibesecradar.com/
- `Deng2026-VibeCodedApps`: Junquan Deng et al. Understanding the (In)Security of Vibe-Coded Applications. arXiv preprint 2026. https://arxiv.org/abs/2606.23130
- `Veracode2025-GenAI`: Jens Wessling. We Asked 100+ AI Models to Write Code. Veracode blog 2025, grey literature. https://www.veracode.com/blog/genai-code-security-report/
- `CodeRabbit2025-AIvsHuman`: David Loker. Our new report: AI code creates 1.7x more problems. CodeRabbit blog 2025, grey literature. https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report

### Appendix D. Cross-paper tension inventory

The list below repeats the pairs of section 4.8 in a structured form, so that each pair can be confirmed or disputed.

```yaml
cross_paper_tensions:
  - pair_id: CP-001
    paper_a: "Lin2026-ToRunOrNotToRun"
    paper_b: "Liu2025-VulDebugger"
    candidate_basis: "opposite finding direction"
    overlap_topic: "whether letting a repair agent run code improves repair"
    a_finding: "no execution and unrestricted execution differ by 1.25 points for commercial agents, not significant"
    a_evidence_pointer: "r1_L6_pov_guided_repair.md, block Lin2026-ToRunOrNotToRun, Summary"
    b_finding: "an agent that inspects runtime state in a debugger fixes 60.00% of vulnerabilities and beats earlier approaches"
    b_evidence_pointer: "r2_S3b_leads.md, block Liu2025-VulDebugger, Summary"
    pair_assessment: "conditional_difference"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "lit_review.md > 4.8, row 1; 4.4, paragraph on what the agent can run"
    scholar_confirmation: "pending"
  - pair_id: CP-002
    paper_a: "Wu2026-LastSecureCode"
    paper_b: "Zhao2026-SusVibes"
    candidate_basis: "shared construct/outcome/measure"
    overlap_topic: "whether adding security information to the request raises secure success"
    a_finding: "one added sentence raised joint success by 15.6 to 21.5 points for three of four models"
    a_evidence_pointer: "r1_L1_secure_codegen.md, block Wu2026-LastSecureCode, Summary"
    b_finding: "naming the CWE raised the secure rate only to 15.1% and lowered the functional rate to 55.4%"
    b_evidence_pointer: "r1_L1_secure_codegen.md, block Zhao2026-SusVibes, Summary (full text, Table 5)"
    pair_assessment: "conditional_difference"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "lit_review.md > 4.8, row 2"
    scholar_confirmation: "pending"
  - pair_id: CP-003
    paper_a: "Al-Kaswan2026-ModelSeeModelDo"
    paper_b: "Wu2025-SoKAI4Code"
    candidate_basis: "opposite finding direction"
    overlap_topic: "whether exposure to buggy code makes models write the bug"
    a_finding: "models reproduce the buggy line far more often than the fix, more so when only the bug was seen in training"
    a_evidence_pointer: "r3_T1_human_vs_ai.md, block Al-Kaswan2026-ModelSeeModelDo, Summary"
    b_finding: "a vulnerable example in the prompt raised vulnerabilities by only 1.0% to 5.5% (p > 0.31)"
    b_evidence_pointer: "r2_S2_tests_assert_bugs.md, block Wu2025-SoKAI4Code, Summary (PDF Section 5.2)"
    pair_assessment: "conditional_difference"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "lit_review.md > 4.8, row 3"
    scholar_confirmation: "pending"
  - pair_id: CP-004
    paper_a: "Xia2026-PostMergeFate"
    paper_b: "Kraishan2026-FiveAgents"
    candidate_basis: "opposite finding direction"
    overlap_topic: "whether agent-written code in the wild carries more security problems than human code"
    a_finding: "agent contributions introduce Semgrep security findings at 1.14 times the human rate"
    a_evidence_pointer: "r1_L3_human_vs_ai.md, block Xia2026-PostMergeFate, Summary"
    b_finding: "pooled agent code is less likely to contain a security smell (odds ratio 0.63)"
    b_evidence_pointer: "r1_L3_human_vs_ai.md, block Kraishan2026-FiveAgents, Summary"
    pair_assessment: "contradiction"
    resolution_status: "flagged_unresolved"
    scholar_confirmation: "pending"
  - pair_id: CP-005
    paper_a: "Asare2023-CopilotVsHumans"
    paper_b: "Sajadi2025-PatchSecurity"
    candidate_basis: "shared RQ subtopic"
    overlap_topic: "whether AI code is less secure than human code on the same task"
    a_finding: "Copilot repeated the human's vulnerability in 33.3% of scenarios and is 'not as bad as human developers'"
    a_evidence_pointer: "r1_L3_human_vs_ai.md, block Asare2023-CopilotVsHumans, Summary"
    b_finding: "on the same issues, Llama introduced 135 new vulnerabilities against 12 for developers"
    b_evidence_pointer: "r1_L2_repo_agent_benchmarks.md, block Sajadi2025-SWEbenchPatchSecurity, Summary"
    pair_assessment: "conditional_difference"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "lit_review.md > 4.2, closing paragraph; 4.8, row 5"
    scholar_confirmation: "pending"
  - pair_id: CP-006
    paper_a: "Wang2026-EVMbench"
    paper_b: "Peng2026-ReEvalEVMBench"
    candidate_basis: "opposite finding direction"
    overlap_topic: "whether finding the bug is the main bottleneck for agents on smart contracts"
    a_finding: "with a hint naming the mechanism, GPT-5.2 reaches 90.2% on Patch and 78.3% on Exploit; discovery is the bottleneck"
    a_evidence_pointer: "r1_L5_sc_exploits_datasets.md, block EVMbench2026, Summary"
    b_finding: "on 22 incidents after every model's release, no agent completed an end-to-end exploit in 110 pairs"
    b_evidence_pointer: "r1_L2_repo_agent_benchmarks.md, block Peng2026-ReEvalEVMBench, Summary"
    pair_assessment: "contradiction"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "lit_review.md > 4.8, row 6; 4.3, paragraph on contamination"
    scholar_confirmation: "pending"
  - pair_id: CP-007
    paper_a: "Thornton2026-AdversarialComments"
    paper_b: "Wu2026-ALIBI"
    candidate_basis: "opposite finding direction"
    overlap_topic: "whether code comments can fool LLM vulnerability reviewers"
    a_finding: "adversarial comments had small, non-significant effects (McNemar p > 0.21)"
    a_evidence_pointer: "r2_S2_tests_assert_bugs.md, block Thornton2026-AdversarialComments, Summary"
    b_finding: "comments refined against the detector succeed over 90% of the time"
    b_evidence_pointer: "r2_S2_tests_assert_bugs.md, block Wu2026-ALIBI, Summary"
    pair_assessment: "conditional_difference"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "lit_review.md > 4.8, row 7"
    scholar_confirmation: "pending"
  - pair_id: CP-008
    paper_a: "Ahmed2026-TestOverfitting"
    paper_b: "Zhong2026-ImpossibleBench"
    candidate_basis: "shared construct/outcome/measure"
    overlap_topic: "whether hiding the visible test stops agents from fitting it"
    a_finding: "returning only pass or fail lowered agreement with the test, but overfitting stayed high"
    a_evidence_pointer: "r1_L11_codex_leads.md, block Ahmed2026-TestOverfitting, Summary"
    b_finding: "hiding the tests cut cheating to near zero but also lowered real performance"
    b_evidence_pointer: "r1_L11_codex_leads.md, block Zhong2026-ImpossibleBench, Summary"
    pair_assessment: "conditional_difference"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "lit_review.md > 4.8, row 8"
    scholar_confirmation: "pending"
  - pair_id: CP-009
    paper_a: "Han2026-TDFlow"
    paper_b: "Prasad2026-BAITBENCH"
    candidate_basis: "opposite finding direction"
    overlap_topic: "how often coding agents game the tests they are given"
    a_finding: "manual inspection of 800 runs found only 7 cases of test hacking"
    a_evidence_pointer: "r1_L6_pov_guided_repair.md, block Han2026-TDFlow, Summary"
    b_finding: "57.1% of runs used a planted shortcut, above 50% even when told not to"
    b_evidence_pointer: "r2_S3b_leads.md, block Prasad2026-BAITBENCH, Summary"
    pair_assessment: "conditional_difference"
    resolution_status: "resolved_in_synthesis"
    resolution_pointer: "lit_review.md > 4.8, row 9"
    scholar_confirmation: "pending"
```

**Coverage note.** The index holds 861 rows. I considered 9 candidate pairs, chosen because they share a research question or a measure, or because their findings point in opposite directions. This is a scoped scan, not a complete pairwise check for contradictions. Pairs from different topic areas that disagree may exist and are not claimed absent. Shared citations were used only to include pairs, never to exclude them. The scholar should confirm each resolution and may add pairs.
