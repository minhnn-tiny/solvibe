## Queries run

Search date: 21 October 2026. "Already indexed" counts hits whose title is in the master index (`lit/master_index.tsv`, last column). Hits that an earlier round file had already screened out are noted in brackets. "New relevant" counts tier A or B papers that are in neither. Queries are listed in the order they were run.

| # | Query | Source | Hits looked at | Already indexed | New relevant |
|---|---|---|---|---|---|
| 1 | all:"smart contract" AND agent AND exploit | arXiv API | 15 | 9 | 0 |
| 2 | abs:"LLM-generated" AND "human-written" AND vulnerab | arXiv API | 0 | 0 | 0 |
| 3 | abs:"coding agent" AND vulnerab AND introduc | arXiv API | 0 | 0 | 0 |
| 4 | abs:Solidity AND audit AND LLM AND benchmark | arXiv API | 4 | 2 | 0 |
| 5 | abs:Foundry AND LLM | arXiv API | 19 | 2 | 0 |
| 6 | abs:"Code4rena" | arXiv API | 4 | 4 | 0 |
| 7 | abs:"Sherlock" AND contest | arXiv API | 1 | 0 | 1 (SPECA, 2604.26495) |
| 8 | abs:"Cantina" AND smart | arXiv API | 0 | 0 | 0 |
| 9 | abs:"smart contract" AND "proof of concept" AND LLM | arXiv API | 5 | 3 | 0 |
| 10 | abs:"vulnerability-introducing" AND "smart contract" | arXiv API | 1 | 0 | 0 |
| 11 | abs:"AI-generated code" AND human AND vulnerabilities | arXiv API | 9 | 8 | 0 |
| 12 | abs:"coding agents" AND security AND feature | arXiv API | 10 | 3 | 1 (Change2Task) |
| 13 | abs:"vibe coding" AND security | arXiv API | 20 | 7 [+1 screened] | 0 |
| 14 | abs:"smart contract" AND "audit reports" AND LLM | arXiv API | 10 | 6 [+2 screened] | 0 |
| 15 | abs:DeFi AND agent AND exploit | arXiv API | 4 | 3 | 0 |
| 16 | abs:Solidity AND "code generation" AND security | arXiv API | 9 | 8 | 0 |
| 17 | abs:"smart contract" AND LLM, submitted April to October 2026 | arXiv API | 40 | 14 [+12 screened] | 0 |
| 18 | "LLM code versus developer code vulnerability density same tasks" | WebSearch | 9 | 9 (incl. screened) | 0 |
| 19 | "AI pair programming security controlled comparison 2026 arXiv" | WebSearch | 10 | 1 | 0 |
| 20 | "coding agent introduces vulnerability when implementing feature request benchmark" | WebSearch | 9 | 9 | 0 |
| 21 | "EVM agent benchmark 2026 hidden exploit test arXiv" | WebSearch | 9 | 9 | 0 |
| 22 | "Foundry proof of concept LLM agent generates from audit report smart contract" | WebSearch | 9 | 7 | 0 |
| 23 | "Sherlock audit contest findings dataset LLM evaluation paper" | WebSearch | 9 | 1 | 0 |
| 24 | "Cantina findings dataset smart contract vulnerability LLM benchmark" | WebSearch | 9 | 7 | 0 |
| 25 | "smart contract vulnerability-introducing commit empirical study Solidity repositories" | WebSearch | 9 | 2 | 0 |
| 26 | decentralized finance AI generated contract audit findings | Semantic Scholar | 40 | 4 [+4 screened] | 0 |
| 27 | "smart contract" LLM agent repair audit finding held-out exploit test 2026 | WebSearch | 9 | 9 | 0 |
| 28 | LLM-written Solidity versus developer-written Solidity security comparison same specification | WebSearch | 10 | 10 | 0 |
| 29 | Code4rena reports benchmark LLM auditor recall high severity findings 2026 paper | WebSearch | 9 | 2 [+1 screened] | 0 |
| 30 | agent-authored pull requests security vulnerabilities compared to human pull requests 2026 | WebSearch | 10 | 4 | 0 |
| 31 | abs:"smart contract" AND agents, submitted July to October 2026 | arXiv API | 18 | 2 [+2 screened] | 0 |
| 32 | abs:"human-written" AND agent AND security, May to October 2026 | arXiv API | 1 | 1 | 0 |
| 33 | abs:EVM AND LLM, May to October 2026 | arXiv API | 3 | 1 [+1 screened] | 0 |
| 34 | abs:"audit contest" | arXiv API | 9 | 2 | 1 (SPECA, 2602.07513) |
| 35 | abs:exploit AND repair AND Solidity | arXiv API | 2 | 1 | 0 |
| 36 | openreview.net smart contract agent benchmark exploit Solidity ICLR 2027 submission | WebSearch | 9 | 9 | 0 |
| 37 | openreview coding agents security vulnerabilities feature implementation human developer comparison 2026 | WebSearch | 9 | 4 | 0 |
| 38 | LLM agent DeFi vulnerability patch validated by exploit Foundry test benchmark 2026 arXiv | WebSearch | 9 | 9 | 0 |
| 39 | (cs.CR OR cs.SE) AND ("smart contract" OR Solidity), September to October 2026 (listing sweep) | arXiv API | 41 | 4 [+9 screened] | 0 |
| 40 | cs.SE AND ("AI-generated code" OR "LLM-generated code" OR "agent-generated") AND security, August to October 2026 | arXiv API | 0 | 0 | 0 |
| 41 | abs:"generated code" AND security AND human, July to October 2026 | arXiv API | 12 | 4 [+1 screened] | 1 (Ansible study) |
| 42 | abs:"coding agents" AND vulnerabilities, August to October 2026 | arXiv API | 17 | 4 [+3 screened] | 0 |
| 43 | abs:"secure code generation" AND agent, July to October 2026 | arXiv API | 5 | 2 [+3 screened] | 0 |
| 44 | "vulnerability-introducing" smart contract commits SZZ Ethereum DeFi projects | WebSearch | 10 | 4 | 0 |
| 45 | LLM rewrite function from audited protocol reintroduces audit finding Solidity experiment | WebSearch | 9 | 4 | 0 |
| 46 | Solodit findings dataset large language model evaluation arXiv 2026 | WebSearch | 9 | 1 | 0 |
| 47 | smart contract vulnerability introducing commit | Semantic Scholar | 40 | 2 [+2 screened] | 0 |
| 48 | LLM agent Solidity feature implementation security human baseline | Semantic Scholar | 27 | 3 | 0 |
| 49 | Sherlock contest dataset LLM | Semantic Scholar | 40 | 1 | 0 (SPECA again) |
| 50 | Cantina audit findings dataset | Semantic Scholar | 40 | 2 | 0 |
| 51 | "smart contract agent" (all venues) | OpenReview search API | 50 | 8 [+4 screened] | 0 |
| 52 | "Solidity" (all venues) | OpenReview search API | 50 | 10 [+1 screened] | 0 |
| 53 | "vibe coding security" (all venues) | OpenReview search API | 50 | 6 [+3 screened] | 0 |
| 54 | "smart contract", ICLR 2027 submissions | OpenReview search API | 50 | 0 | 1 (ConstraintDial) |
| 55 | "DeFi exploit", ICLR 2027 submissions | OpenReview search API | 50 | 0 [+1 screened] | 0 |
| 56 | "Solidity", ICLR 2027 submissions | OpenReview search API | 2 | 0 | 0 |
| 57 | "human-written code security", ICLR 2027 submissions | OpenReview search API | 50 | 2 | 2 (VeilPRBench, multi-turn refinement study) |
| 58 | "audit report vulnerability", ICLR 2027 submissions | OpenReview search API | 50 | 3 | 2 (VulVerifyBench, SysRepair-Bench) |
| 59 | "secure coding agent benchmark feature", ICLR 2027 submissions | OpenReview search API | 50 | 6 | 0 |
| 60 | "vulnerability introducing commit agent", ICLR 2027 submissions | OpenReview search API | 50 | 3 [+3 screened] | 0 |
| 61 | "exploit test repair overfitting", ICLR 2027 submissions | OpenReview search API | 50 | 1 [+1 screened] | 0 |
| 62 | "blockchain agent security benchmark", ICLR 2027 submissions | OpenReview search API | 50 | 1 | 0 |
| 63 | abs:"human developers" AND "coding agents" AND security | arXiv API | 3 | 2 [+1 screened] | 0 |
| 64 | abs:"audit findings" AND agent | arXiv API | 16 | 1 | 0 |
| 65 | "LLM-generated code versus human-written code vulnerabilities", ICLR 2027 submissions | OpenReview search API | 50 | 2 | 0 |
| 66 | Uniswap v4 hook vulnerability LLM agent generated code audit study | WebSearch | 9 | 1 | 0 |
| 67 | LLM-generated smart contracts compared with human-written contracts exploitable vulnerabilities controlled study 2026 | WebSearch | 9 | 9 (incl. screened) | 0 |
| 68 | AI agent reimplements function removed from audited code, human developer vulnerability reproduced, proof of vulnerability test | WebSearch | 9 | 7 [+2 screened] | 0 |

The last five queries (64 to 68) gave no new tier A or B paper. I also ran six exact-title arXiv searches to look for preprint versions of the OpenReview papers below; none has an arXiv version yet.

Result in short: 9 new papers, 2 of them tier A. Only 4 of the 9 sit squarely in this topic (agent or human code comparison, smart-contract agents, audit-contest benchmarks): ConstraintDial (A), the two SPECA papers (B), and the Ansible comparison (B). Change2Task (B) is about building tasks from repository history. The other 4 (SysRepair-Bench, VulVerifyBench, VeilPRBench, and the multi-turn refinement study) came up in the ICLR 2027 sweep and touch N4 and N6, not this topic. I report them because no index entry or round file mentions them.

How the sources behaved:
- The arXiv API answered every query. The sweeps over 2026 listings found mostly papers that earlier rounds had already screened.
- Semantic Scholar returned HTTP 429 many times. One query needed several minutes of retries. All five queries finished in the end.
- OpenReview's search API answered without a contact address. It returned each record's title, venue line, keywords and abstract. The forum pages (openreview.net/forum) and the `/notes` endpoint showed a browser check, so I could not open them. ICLR 2027 submissions are anonymous, so no authors are shown.
- No personal identifier was sent to any service.

### Anon2027-ConstraintDial Beyond Copying: Lifelong Smart Contract Security Task Construction via Protocol Mutation
- Authors: anonymous (double-blind review); Year: 2026; Venue: ICLR 2027 Conference Submission (under review, OpenReview forum EoypgLdcmo)
- URL opened: https://api2.openreview.net/notes/search?term=smart%20contract&group=ICLR.cc/2027/Conference (OpenReview API record with title, venue line, keywords and abstract). The forum page https://openreview.net/forum?id=EoypgLdcmo showed a browser check.
- Status: VERIFIED (title and abstract from OpenReview's own record; authors hidden by double-blind review)
- Tier: A
- Touches: N2, N3 (patch tasks are judged by running the attack)
- Summary: Agent benchmarks for smart-contract security can reward memorized answers, including attack code copied from public blockchain transactions. The framework (ConstraintDial) rebuilds each contract locally and then changes the required calls or inputs, so that the original public attack fails. Execution checks make sure the changed contract can still be exploited, keeps the same security goal and still works normally. New incidents and audit findings go through the same steps. From 203 public cases it builds 3,045 task inputs covering detection, exploitation and patching. Compared with rebuilding alone, the mutation lowers success when the agent is given the public answer by 10.9 percentage points on average, and the share of tasks solved by copying online answers falls by 9.3 points.
- Delta: ConstraintDial attacks the same threat to validity as the project: a model may already know the public answer. It does this differently. It changes the contract so that the known exploit no longer works, while the project picks models whose training data ends before the findings were published. ConstraintDial scores agents on detection, exploitation and patching. It has no human baseline. It never asks an agent to write the feature from a request, it has no control group, and its abstract mentions no held-out exploits for repairs and no loss estimates. The project compares the agent's code with the human's code for the same function, from the same starting code, under the same PoV. ConstraintDial's mutation step could serve as a second check against memorized fixes in the project's repair round.

### Kamba2026-SPECA SPECA: Specification-to-Checklist Agentic Auditing for Multi-Implementation Systems -- A Case Study on Ethereum Clients
- Authors: Masato Kamba et al. (2 authors); Year: 2026; Venue: arXiv preprint (arXiv:2602.07513, v2 10 February 2026; no journal reference on the page)
- URL opened: https://arxiv.org/abs/2602.07513 (arXiv abstract page); abstract also read through the arXiv API
- Status: VERIFIED
- Tier: B
- Touches: N6; also the topic of benchmarks built from audit-contest findings
- Summary: An LLM agent turns the rules in a natural-language specification into checklists, maps them to code in several implementations, and reuses each check across implementations. It took part in a real audit contest for the Ethereum Fusaka upgrade, covering 11 production clients. Of 54 submissions, contest organizers judged 17 valid, and 13 of those 17 came from checks reused across implementations. Of the 37 invalid reports, 21 (56.8%) rested on trust or scope assumptions that contradicted the audit's rules. An improved agent, judged against the contest's ground truth, reached a strict recall of 27.3% on high-impact vulnerabilities, which put it in the top 4% of human auditors and ahead of 49 of 51 contestants on critical issues.
- Delta: SPECA audits Ethereum client software against a protocol specification. It does not audit Solidity contracts, and its agent does not write or repair code. It compares an AI auditor with human auditors in one contest, using the organizers' rulings as ground truth. The project compares an AI author with the human author of the same function and judges both with a PoV. For N6, SPECA's false-positive analysis is a useful warning. Most invalid reports came from wrong assumptions about trust and scope. The project's two LLM reviewers may need the audit's scope and trust model in the prompt, and the project already requires a PoV to confirm each reported flaw.

### Kamba2026-SPECAProtocols Beyond Code Reasoning: Specification-Anchored Auditing of Multi-Implementation Distributed Protocols
- Authors: Masato Kamba et al. (3 authors); Year: 2026; Venue: arXiv preprint (arXiv:2604.26495, v2 5 May 2026; no journal reference on the page)
- URL opened: https://arxiv.org/abs/2604.26495 (arXiv abstract page); abstract also read through the arXiv API
- Status: VERIFIED
- Tier: B
- Touches: N6; also the topic of benchmarks built from audit-contest findings
- Summary: This extends SPECA. The LLM framework derives security properties (invariants, pre- and postconditions, trust assumptions) from a specification and reuses them across client implementations. On the Sherlock Ethereum Fusaka Audit Contest (10 targets, 366 submissions), it recovers all 15 in-scope high, medium and low vulnerabilities with expert help (8 of 15 fully automated), and it finds 4 bugs whose fixes were confirmed. On the RepoAudit C/C++ benchmark it reaches 88.9% precision at 100% recall (F1 0.94). The cost is about 30 dollars and 42 minutes per high, medium or low bug.
- Delta: This version uses a Sherlock contest's adjudicated findings as a benchmark for an LLM auditor. That is the same data source as the project's tasks, but used for detection only. It audits client software, not Solidity. It does not write code from a feature request, compare against the human author, or confirm findings with executable exploits (it uses fix confirmation by maintainers). The project uses contest findings to build writing and repair tasks with PoVs. Cite the two SPECA papers together as evidence that audit contests are now used as ground truth for agent auditors.

### Qi2026-Change2Task Change2Task: From Repository Changes to Executable Coding Agent Tasks and Environments
- Authors: Haomin Qi et al. (12 authors); Year: 2026; Venue: arXiv preprint (arXiv:2607.28591, v1 30 July 2026)
- URL opened: https://arxiv.org/abs/2607.28591 (arXiv abstract page); abstract read through the arXiv API
- Status: VERIFIED
- Tier: B
- Touches: N1 (how tasks are built from repository history)
- Summary: The system turns merged pull requests into verified agent tasks on current, maintained versions of the same repository. It rebuilds the task state by reversing the patch, by mapping the old change onto newer code, or by having an agent rebuild it. It then checks the full cycle from a healthy base, to the task state, to the restored state. It covers five task families: bug fix, feature addition, test generation, API migration and security repair. From 1,130 eligible source changes, 79.6% became verified tasks. It recovers 29.2% more verified tasks than a baseline built from pull requests, historical and rebuilt cases agree on agent outcomes in up to 98.0% of cases, and reusing modern bases cuts pipeline cost by 10.8%.
- Delta: Change2Task and the project both build agent tasks by taking a real change out of the repository and asking the agent to make it again. Change2Task's "feature addition" and "security repair" families are close to the project's feature request and repair rounds. It is a general task-building tool. It does not compare the agent's code with the human's code for security, and it does not use exploits or Solidity. The project needs the human's original vulnerable version as the baseline and a PoV as the judge. Change2Task's check that the task state and the restored state both behave as expected is a method the project could cite for its own task validation.

### Konala2026-AnsibleSmells Evaluating and Preventing Security Smells in AI-Generated Ansible Code
- Authors: Pandu Ranga Reddy Konala et al. (4 authors); Year: 2026; Venue: arXiv preprint (arXiv:2608.24962, v1 25 August 2026; comments: 14 pages, dataset and prompts on figshare)
- URL opened: https://arxiv.org/abs/2608.24962 (arXiv abstract page); abstract read through the arXiv API
- Status: VERIFIED
- Tier: B
- Touches: N1 (AI-written code compared with human-written code on the same targets)
- Summary: Sixteen AI models wrote Ansible roles that deploy Apache Tomcat v10 and MongoDB v7. The authors checked 278 roles against CIS benchmarks. Without security guidance, every model produced security smells, and the generated roles did worse than roles written by human developers. With Ansible best practices and CIS rules added to the prompt (an extended CO-STAR prompt), 4 of 16 models produced compliant code. The best model reached 95% to 100% CIS compliance, against 23% to 43% for the human-written roles, and overall code quality improved by 19% to 49%.
- Delta: This is an AI-versus-human security comparison on the same deployment targets. The direction of the result flips with the prompt: AI code is worse than human code without guidance and far better with it. That matches the project's pilot, where the wording of the feature request decided whether agents wrote the bug. The study differs from the project in four ways. It covers infrastructure code, not Solidity. It judges security by a compliance checklist, not an executable exploit. It uses single prompts, not agents. The human code was not written from the same starting state. The project's comparison is tighter: same function, same starting code, same PoV, plus a control group.

### Anon2027-SysRepairBench SysRepair-Bench: Measuring Whether Agents Can Fix a Vulnerability Without Breaking the Service
- Authors: anonymous (double-blind review); Year: 2026; Venue: ICLR 2027 Conference Submission (under review, OpenReview forum tEkcE3HKIV)
- URL opened: https://api2.openreview.net/notes/search?term=audit%20report%20vulnerability&group=ICLR.cc/2027/Conference (OpenReview API record with title, venue line, keywords and abstract); the forum page showed a browser check
- Status: VERIFIED (title and abstract from OpenReview's own record; authors hidden by double-blind review)
- Tier: A
- Touches: N4 (also N3 in spirit: a fix can block the exploit and still be wrong)
- Summary: The benchmark has 313 scenarios. In each one an agent must fix a live vulnerable service through a shell. The 297 binary scenarios pass only if the exploit is blocked and the service stays healthy. Every scenario runs twice: once with the vulnerability report, and once where the agent must find the fault itself. With the report, the median model and suite reach 90.0%. Without it they reach 49.4%, a median drop of 37.4 points. The authors also count fixes that block the exploit by breaking the service. Without the report this share is higher for 7 of 8 models, and the authors treat it as specification gaming.
- Delta: This is the closest outside result to N4's question of what the agent is told. It shows, with an executable exploit as judge, that giving the report changes repair success by a large margin. A reviewer could cite it against the novelty of the report condition. It varies only one input (report or no report). It always gives a full shell. Its second check is service health, not held-out exploits. The project varies four inputs (location only, written report, shown PoV, report and PoV) and three levels of what the agent can run. It judges repairs with held-out PoVs, and it shows that the repository's own tests can assert the buggy behaviour. The project should position its N4 findings against this benchmark: the project's question is how the inputs and the ability to run code interact on Solidity business-logic bugs, not only whether a report helps.

### Anon2027-VulVerifyBench VulVerifyBench: Can and How LLM Agents Verify Vulnerability Reports?
- Authors: anonymous (double-blind review); Year: 2026; Venue: ICLR 2027 Conference Submission (under review, OpenReview forum 0AKyAPlwBm)
- URL opened: https://api2.openreview.net/notes/search?term=VulVerifyBench%20verify%20vulnerability%20reports&group=ICLR.cc/2027/Conference (OpenReview API record with title, venue line, keywords and abstract); the forum page showed a browser check
- Status: VERIFIED (title and abstract from OpenReview's own record; authors hidden by double-blind review)
- Tier: B
- Touches: N6
- Summary: The benchmark asks whether an agent can decide if a vulnerability report should be accepted. It holds 747 real reports across smart contracts, traditional software and web applications. Of these, 220 are invalid, including 45 hard negatives, where the real behaviour does not justify the claim. It also includes 88 cases that pair an unchanged report with patched code, so the right answer is known by construction. The agent gets a scrubbed report and, where available, the repository, and returns a verdict with evidence. With two frontier and two open-weight models, the best accuracies in the three domains are 84.5%, 87.5% and 78.4%. No model exceeds 77.8% recall on hard negatives, and 6.3% of verdicts were not supported by the facts the agent had gathered.
- Delta: VulVerifyBench measures how well agents judge a reported flaw, including smart-contract reports. The project's N6 does not ask an agent to judge reports. It requires a new PoV to confirm every flaw that the LLM reviewers report. VulVerifyBench gives outside evidence for that design choice: agents often accept reports that their own evidence does not support. It does not compare agent-written and human-written code, and its smart-contract reports are not tied to feature tasks.

### Anon2027-VeilPRBench VeilPRBench: Can Code Review Agents Catch Vulnerabilities in Pull Requests That Resolve Real Issues?
- Authors: anonymous (double-blind review); Year: 2026; Venue: ICLR 2027 Conference Submission (under review, OpenReview forum tNc8k7gBu3)
- URL opened: https://api2.openreview.net/notes/search?term=VeilPRBench%20code%20review%20agents%20vulnerabilities%20pull%20requests&group=ICLR.cc/2027/Conference (OpenReview API record with title, venue line, keywords and abstract); the forum page showed a browser check
- Status: VERIFIED (title and abstract from OpenReview's own record; authors hidden by double-blind review)
- Tier: B
- Touches: N6, N1
- Summary: A pull request can fix its issue and still add a logic vulnerability. The benchmark tests whether code review agents block such pull requests and accept benign fixes. It has 192 hand-built attack pull requests across 14 open-source projects and 29 issue families, plus 135 benign fixes, in Python, C and JavaScript. Functional tests confirm that each fix works, and executable security checks confirm what each attack does. Across 16 deployed review setups, review agents blocked only 25.0% of attacks on average, and the best blocked 55.2%.
- Delta: VeilPRBench studies the reviewer's side of the problem that the project's control group studies on the author's side. In the project, an agent writes a feature that works, and an LLM review plus a PoV check whether it added a flaw. In VeilPRBench, humans write the flawed pull requests by hand, and the question is whether a review agent notices. It shows that LLM review alone misses most logic flaws, which supports the project's rule that a PoV must confirm each finding. It does not cover Solidity, does not compare human and agent authors, and does not use the human's original version as a baseline.

### Anon2027-MultiTurnRefinement Promises and Pitfalls of Multi-Turn Refinement for Secure Code Generation
- Authors: anonymous (double-blind review); Year: 2026; Venue: ICLR 2027 Conference Submission (under review, OpenReview forum hSw3gkxBTC)
- URL opened: https://api2.openreview.net/notes/search?term=Promises%20and%20Pitfalls%20of%20Multi-Turn%20Refinement%20for%20Secure%20Code%20Generation&group=ICLR.cc/2027/Conference (OpenReview API record with title, venue line, keywords and abstract); the forum page showed a browser check
- Status: VERIFIED (title and abstract from OpenReview's own record; authors hidden by double-blind review)
- Tier: B
- Touches: N4
- Summary: The study asks how well models improve the security of generated code over several turns of feedback. It varies the generator and the feedback signal: test cases, static analysis and natural-language critiques. It uses four feedback types and two benchmarks. Refinement improves secure code generation, but no single feedback signal is best everywhere. The main limit is reward hacking: models make shallow changes that satisfy the critic without fixing the real correctness or security problem, and this gets worse with more turns. The abstract gives no numbers.
- Delta: The project saw the same behaviour in repair: agents fitted the shown PoV, and their fixes covered only the case the shown test met. This study shows the pattern for generation with several kinds of feedback, and gives a taxonomy of the shallow fixes. It uses existing secure-coding benchmarks, not real audited vulnerabilities, and it has no held-out exploits to expose shallow fixes. The project measures the effect with held-out PoVs on Solidity repairs, and it adds the finding that repository tests can encode the bug.

## Leads not followed

- "Building secure Uniswap v4 hooks", Trail of Bits blog, 30 July 2026 (blog.trailofbits.com/2026/07/30/building-secure-uniswap-v4-hooks/). Seen in query 66. According to the search summary, it groups dozens of audit findings on v4 hooks into seven recurring failure patterns. This is grey literature, tier C. It may be useful background for finding 63008 (a Uniswap v4 hook).
- "A Controlled Benchmark: ChatGPT-5.2 and Claude Sonnet 4.5 vs Sherlock AI on a Web3 Audit Dataset", Sherlock blog (sherlock.xyz). Seen in queries 23 and 29. A vendor post, not peer reviewed. Tier C at most.
- "AuditAgent on EVMBench: 40 Repositories, 120 Vulnerabilities", Nethermind blog. Seen in query 29. A vendor post. Tier C at most.
- SoliForge, an ETHGlobal HackMoney 2026 hackathon project (a red agent writes Foundry exploits and a blue agent patches). Seen in query 22. Not a paper.
- "AVIATOR: Towards AI-Agentic Vulnerability Injection Workflow for High-Fidelity, Large-Scale Code Security Dataset" (arXiv 2508.20866). Seen in query 68. I read only the title and the search summary. It is probably tier C (building a dataset by injecting vulnerabilities).
- "Visible Features, Hidden Flaws: Vulnerability Persistence in LLM-Generated Software" (ICLR 2027 submission, OpenReview UAsmdQsx8d). Abstract read. It has no human baseline, so tier C.
- "Smart Contracts Claimed Vulnerable by the CVE Database, with Labels and Source Locations" (arXiv 2609.01186). Abstract read. A dataset, tier C.
- "Understanding Verification Vulnerabilities in Cross-chain Bridges: An Empirical Study" (arXiv 2610.13170). Seen in queries 14 and 39. Title only. Probably tier C.
- ICLR 2027 submissions seen by title only, probably tier C (secure code generation or repair methods): PurpAgent (MugwJowgxu), Securing Agentic Code Generation with Intent Code Graph Learning (o7WvHD1nBF), SWE-RedAgent (Hw4XpEKH4C), TrapArena (R7ub0QvlFK), Harvesting SWE Benchmarks from Wild Vibe Coding Sessions, and REVIBE.
- "LLMs in Code Vulnerability Analysis: A Proof of Concept" (arXiv 2601.08691, SVM 2026 workshop at ICSE 2026). Abstract read. C/C++ detection and repair with fine-tuning. Tier C.
