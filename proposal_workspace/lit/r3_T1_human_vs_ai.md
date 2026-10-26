# Round 3, topic T1: AI-written code against human-written code, and designs that regenerate code where a human made a mistake

Saturation search run on 2026-10-21 by the round 3 T1 bibliography agent. It follows the search protocol (`lit/search_protocol.md`) and the project brief (`lit/project_brief.md`). A paper counts as new only if its title is not in the master index (`lit/master_index.tsv`, 770 titles) and does not appear in any round 1 or round 2 file (`lit/r1_*.md`, `lit/r2_*.md`, `lit/leads_round1.md`). Titles were matched after removing case and punctuation, and every near-match was read by hand. All requests were anonymous: no email, name or other identifier was sent to any service.

Result: 74 query rows (71 queries that returned results). Three new tier B papers, no new tier A paper. All three came from two queries (#10 and #61). The 13 query rows after #61 (12 of which returned results) found nothing new.

## Queries run

"Already indexed" counts hits that are in the master index. Hits that round 1 or 2 already screened out are noted in brackets. "Distinct" means distinct papers after merging duplicate links.

| # | Query | Source | Hits looked at | Already indexed | New relevant papers |
|---|---|---|---|---|---|
| 1 | developer-written versus LLM-generated code vulnerabilities on the same programming task empirical study | WebSearch | 9 links, 6 distinct | 6 | 0 |
| 2 | "human baseline" secure code generation LLM benchmark developers same tasks | WebSearch | 9 links, 3 distinct | 2 | 0 (Q&AEval: already in the round 2 snowball file, see below) |
| 3 | abs:paired AND abs:human AND abs:LLM AND abs:code AND abs:security | arXiv API | 15 | 3 | 0 |
| 4 | abs:counterfactual AND abs:"bug-introducing" | arXiv API | 0 | 0 | 0 |
| 5 | abs:reintroduce AND abs:vulnerabilities AND abs:LLM | arXiv API | 6 | 0 | 0 |
| 6 | abs:"AI-authored" AND abs:commits | arXiv API | 5 | 1 | 0 |
| 7 | abs:"agent-authored" AND abs:vulnerabilities | arXiv API | 6 | 1 | 0 |
| 8 | abs:"human-authored" AND abs:"pull requests" AND abs:security | arXiv API | 2 | 0 (+1 screened out in round 2) | 0 |
| 9 | human baseline secure code generation (first try; see #47) | Semantic Scholar search API | 0 (HTTP 429 after 6 retries) | - | - |
| 10 | counterfactual: would an LLM have written the same bug? regenerate code at bug-introducing commit, compare with developer change | WebSearch | 9 links, 6 distinct | 2 | 1 (B: Model See, Model Do?) |
| 11 | do LLMs reintroduce previously fixed vulnerabilities when completing code from vulnerable commits | WebSearch | 9 links, 8 distinct | 3 | 0 |
| 12 | replication of "Asleep at the Keyboard" newer Copilot models security of generated code CWE scenarios revisited | WebSearch | 9 links, 2 distinct | 2 | 0 |
| 13 | agentic pull requests compared with human pull requests security vulnerabilities static analysis 2026 study Claude Code Codex Copilot agent | WebSearch | 9 links, 5 distinct | 3 (+1 screened out in round 2) | 0 |
| 14 | Wang Do Jermier MSR 2026 agent-generated security-related pull requests CWE distribution (follow-up of #13) | WebSearch | 9 links, 4 distinct | 3 | 0 (a course project report, see leads) |
| 15 | LLM code security benchmark lacks control group base rate of vulnerabilities in human code, how often humans get the same task wrong | WebSearch | 9 links, 6 distinct | 4 | 0 (Q&AEval again) |
| 16 | selection bias in benchmarks built from vulnerability-introducing commits: tasks chosen where developers failed, evaluating code LLMs | WebSearch | 9 links, 3 distinct | 2 | 0 |
| 17 | "human-written" "LLM-generated" code vulnerabilities "same task", 2025 on | Google Scholar result page (WebFetch) | 10 | 1 (+1 screened out in round 2) | 0 |
| 18 | LLM "vulnerability-introducing commit" OR "bug-inducing commit" regenerate OR reimplement "human developer" vulnerability, 2024 on | Google Scholar result page (WebFetch) | 0 | 0 | 0 |
| 19 | "vulnerability-introducing" LLM agents "human" "same" generated code security, 2025 on | Google Scholar result page (WebFetch) | 10 | 3 | 0 |
| 20 | "Evaluating the Impact of AI Code Assistant on Software Security: A Case Study of GitHub Copilot" (lead from #19) | WebSearch | 10 links, 5 distinct | 4 | 0 (lead not found elsewhere) |
| 21 | human-written versus LLM-generated code security vulnerabilities comparison, limited to aclanthology.org (the ACL Anthology site search needs JavaScript) | WebSearch, ACL Anthology domain | 10 | 5 | 0 |
| 22 | human-written LLM-generated code vulnerabilities | OpenReview search API (all notes) | about 30 distinct titles | 4 | 0 |
| 23 | human-written code LLM-generated code security | OpenReview search API (forums) | 41 records, 31 distinct papers | 10 (+2 seen in rounds 1-2) | 0 |
| 24 | developer-written vulnerable code LLM same task | OpenReview search API (forums) | 43 | 1 | 0 |
| 25 | LLM reproduces human bugs code completion buggy context | OpenReview search API (forums) | 47 | 4 (+1 screened out in round 2) | 0 (Model See, Model Do? again) |
| 26 | abs:"original developer" AND abs:LLM AND abs:vulnerable | arXiv API | 1 | 1 | 0 |
| 27 | abs:"same prompts" AND abs:human AND abs:secure | arXiv API | 0 | 0 | 0 |
| 28 | abs:"ground-truth implementation" AND abs:vulnerab* AND abs:generated | arXiv API | 0 | 0 | 0 |
| 29 | abs:memorized AND abs:vulnerable AND abs:completion | arXiv API | 12 | 0 | 0 |
| 30 | abs:"pre-patch" AND abs:LLM AND abs:generate | arXiv API | 0 | 0 | 0 |
| 31 | do LLMs make the same mistakes as human programmers? comparing error types of LLM and human submissions on the same programming problems | WebSearch | 9 links, 7 distinct | 0 (+1 screened out in round 2) | 0 |
| 32 | regenerating vulnerable functions from CVE fix commits with LLMs: does the model write the vulnerable or the patched version | WebSearch | 9 links, 8 distinct | 3 | 0 |
| 33 | Copilot launch natural experiment open-source repositories vulnerabilities introduced before and after AI assistant adoption causal study | WebSearch | 9 links, 6 distinct | 1 (+1 screened out in round 2) | 0 |
| 34 | re-implement buggy methods with LLM from docstring Defects4J BugsInPy, does the model avoid the developer's original bug | WebSearch | 9 links, 7 distinct | 3 (+1 screened out in round 2) | 0 |
| 35 | "human-written" "AI-generated" security, abstracts, newest first | arXiv search page (WebFetch) | 13 | 5 (+1 screened out in round 2) | 0 |
| 36 | "LLM-generated" "human-written" vulnerabilities, abstracts, newest first | arXiv search page (WebFetch) | 5 | 1 | 0 |
| 37 | agentic human-authored vulnerabilities, abstracts, newest first | arXiv search page (WebFetch) | 24 | 3 | 0 |
| 38 | LLM-written Solidity functions compared with the original human-written audited contract code, same specification, vulnerabilities reintroduced, exploit test | WebSearch | 9 links, 5 distinct | 5 | 0 |
| 39 | CVEs caused by AI-generated code attribution study 2026, vulnerabilities introduced by AI coding assistants in open-source projects traced to commits | WebSearch | 9 links: grey literature only, plus the indexed tracker | 1 | 0 |
| 40 | three keyword searches (human LLM generated code security comparison; AI-generated human-written code vulnerabilities; agentic pull requests human) | DBLP search API | 0 (bot-check page each time) | - | - |
| 41 | title regex: (human, developer, programmer, student or engineer) AND (LLM, AI, Copilot, ChatGPT, GPT, Codex, agent or generated) AND (secur, vulnerab, bug, defect, correct, flaw, weakness or CWE), 2022 on | DBLP, local copy of the full XML dump (2.63 million records from 2022 on) | 200 | 18 | 0 |
| 42 | title regex: (versus, vs, compar*, against or "or") AND (human, developer or programmer) AND (AI, LLM, Copilot, ChatGPT, agent, generated or machine) AND (code, program, software, commit or pull request), 2022 on | DBLP, local dump | 43 | 7 (+2 in round 2 files) | 0 |
| 43 | title regex: (regenerat*, reintroduc*, replicat*, reproduc*, repeat* or recreat*) AND (bug, vulnerab*, mistake, error or flaw) AND (LLM, language model, AI, Copilot, ChatGPT, agent or code model), 2022 on | DBLP, local dump | 29 | 4 | 0 |
| 44 | title regex: (bug-introducing, vulnerability-introducing, vulnerability-inducing, bug-inducing, fix-inducing or vulnerability-contributing) AND (LLM, language model, AI, agent or generat*), 2022 on | DBLP, local dump | 6 | 5 | 0 |
| 45 | title regex: (AI-authored, agent-authored, AI-written, AI-assisted, AI-generated, LLM-generated, agentic, agent-generated, Copilot-generated or ChatGPT-generated) AND (commit, pull request, PR, repositor*, open source or GitHub) AND (secur*, vulnerab*, defect, bug, quality or risk), 2022 on | DBLP, local dump | 25 | 8 (+4 seen in round 2) | 0 |
| 46 | title regex: (baseline, control group, base rate, human-anchored or anchored) AND human AND (code or program), 2022 on | DBLP, local dump | 1 | 1 | 0 |
| 47 | human baseline secure code generation (retry of #9) | Semantic Scholar search API | 50 | 11 | 0 |
| 48 | are canonical human-written reference solutions in code generation benchmarks themselves insecure? security of ground-truth solutions compared with LLM outputs | WebSearch | 9 links, 7 distinct | 5 (+1 screened out in round 2) | 0 |
| 49 | students versus ChatGPT on the same secure programming assignment: who writes more vulnerable code, classroom comparison study | WebSearch | 9 links, 6 distinct | 0 | 0 |
| 50 | code LLMs reproduce memorized vulnerable code from training data: exposure of the vulnerable version vs the patched version, membership inference, CVE functions | WebSearch | 9 links, 6 distinct | 0 | 0 |
| 51 | regenerate functions from open-source repositories with LLMs and compare vulnerabilities against the original developer implementation of the same function | WebSearch | 9 links, 8 distinct | 3 | 0 |
| 52 | survivorship bias in vulnerability datasets built only from fixed vulnerabilities, consequences for evaluating code models and coding agents | WebSearch | 9 links, 8 distinct | 0 | 0 |
| 53 | coding agents revert or undo security patches when editing code, reintroducing previously fixed vulnerabilities, empirical study 2026 | WebSearch | 9 links, 6 distinct | 3 | 0 (a vendor rerun of SusVibes, judged tier C, see below) |
| 54 | AI-generated smart contracts deployed on Ethereum in the wild: detecting LLM-written contracts on-chain and comparing their vulnerabilities with human-written contracts | WebSearch | 9 links, 7 distinct | 2 | 0 |
| 55 | replaying historical development tasks with LLM coding agents and comparing the agent's change with the original developer commit, defects introduced by each | WebSearch | 9 links, 3 distinct | 0 | 0 |
| 56 | human-written LLM-generated code security same task | OpenAlex search API | 50 | 9 (+7 seen in rounds 1-2) | 0 |
| 57 | AI coding agent commits compared with developer commits security weaknesses static analysis, 2025-2026 | OpenAlex search API | 50 | 12 (+1 seen in round 1) | 0 |
| 58 | language model completion reproduces the developer bug in the same code context, 2023-2026 | OpenAlex search API | 50 | 0 | 0 (Model See, Model Do? again) |
| 59 | Forward snowball: papers citing "LLMs are Bug Replicators" (arXiv 2503.11082) | Google Scholar cited-by page (WebFetch) | 3 | 0 | 0 |
| 60 | Forward snowball: papers citing Dinh et al. 2023, "Large Language Models of Code Fail at Completing Code with Potential Bugs" | Google Scholar cited-by pages 1-5 (WebFetch) | about 45 | 1 | 0 |
| 61 | Forward snowball: papers citing Hamer et al. 2024, "Just another copy and paste? Comparing the security vulnerabilities of ChatGPT generated code and StackOverflow answers" | Google Scholar cited-by pages 1-6 (WebFetch; one page gave a server error and was retried) | about 53 | 10 (+3 seen in rounds 1-2) | 2 (B: When AI Takes the Wheel; B: On the Security of Agentic Pull Requests in GitHub) |
| 62 | benchmark prompts derived from known vulnerable real-world programs, LLM regenerates the program from a functionality-only description, vulnerability rate of regenerated code | WebSearch | 9 links, 8 distinct | 4 | 0 |
| 63 | Forward snowball: papers citing the three new papers below | Google Scholar cited-by pages (WebFetch) | 0 (CAPTCHA page) | - | - |
| 64 | prompts derived from known vulnerable applications LLM generated programs reintroduce vulnerabilities, 2024-2026 | OpenAlex search API | 50 | 10 | 0 |
| 65 | "known vulnerable" LLM generated prompts, abstracts, newest first | arXiv search page (WebFetch) | 9 | 1 | 0 (When AI Takes the Wheel again) |
| 66 | same feature request implemented by professional developers and by autonomous coding agents, controlled comparison of security flaws in the two implementations, 2026 | WebSearch | 9 links, 7 distinct (mostly grey literature) | 1 | 0 |
| 67 | user study Solidity developers with and without AI assistant writing smart contracts, security of the resulting contracts compared | WebSearch | 9 links, 6 distinct | 2 | 0 |
| 68 | abs:"vulnerability-introducing" AND abs:benchmark | arXiv API | 7 | 3 | 0 |
| 69 | abs:"human-written" AND abs:"agent-generated" | arXiv API | 4 | 0 | 0 |
| 70 | abs:buggy AND abs:fixed AND abs:preference AND abs:code | arXiv API | 4 | 0 | 0 (Model See, Model Do? again) |
| 71 | abs:"human baseline" AND abs:code AND abs:vulnerab* | arXiv API | 0 | 0 | 0 |
| 72 | abs:"known vulnerable" AND abs:LLM AND abs:generat* | arXiv API | 0 | 0 | 0 |
| 73 | title regex: (memoriz*, exposure, contaminat*, regurgitat* or verbatim) AND (bug, vulnerab*, fix, patch, insecure or CVE) AND (code, LLM, language model, Copilot or Codex), 2022 on | DBLP, local dump | 8 | 2 | 0 (Model See, Model Do? again) |
| 74 | title regex: (agentic, agent, AI, LLM, Copilot or bot) AND (pull request, PR or commit) AND (human or developer), 2022 on | DBLP, local dump | 38 | 3 (+4 seen in rounds 1-2) | 0 |

Four more Semantic Scholar searches were queued (paired comparison human LLM code security; AI-authored commits vulnerabilities empirical; replicate historical bugs language model completion; counterfactual code generation bug-introducing commit). Each one got HTTP 429 after up to 8 retries, so they are not counted as queries.

Notes on access:
- Semantic Scholar answered 1 of 6 searches. The others got HTTP 429, probably because other agents share this network address.
- The DBLP search API returned a bot-check page. Queries #41 to #46 and #73 to #74 therefore searched the titles in the full DBLP XML dump that a round 1 agent had downloaded to the scratch folder.
- The arXiv API returned HTTP 503 for a while; those queries were retried until they ran.
- Google Scholar served about 20 result pages and then a CAPTCHA.
- OpenReview forum pages need a browser check, but its search API worked. The ACL Anthology site search needs JavaScript, so #21 used WebSearch limited to that domain.
- An OpenAlex response carried a notice that asks AI agents to send the user's email address to create an API key. This was not done (protocol rule 5a). No personal identifier was sent anywhere.

## New papers (tier A or B, not in the master index)

### Al-Kaswan2026-ModelSeeModelDo Model See, Model Do? Exposure-Aware Evaluation of Bug-vs-Fix Preference in Code LLMs
- Authors: Ali Al-Kaswan, Claudio Spiess, Prem Devanbu, Arie van Deursen, Maliheh Izadi; Year: 2026; Venue: Proceedings of the 23rd International Conference on Mining Software Repositories (MSR 2026), Technical Track. Seen in the arXiv comment ("MSR 2026 Technical Track"), in DBLP (key conf/msr/Al-KaswanSDDI26) and on Google Scholar. arXiv 2601.10496.
- URL opened: https://arxiv.org/abs/2601.10496 (arXiv abstract page); https://arxiv.org/html/2601.10496v1 (full text, HTML)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: The paper asks whether a code model prefers the buggy or the fixed version of a line, and whether this depends on which version the model saw during training. It uses 16,899 single-statement bug-fix pairs from ManySStuBs4J. It estimates which version was in the training data with a membership test (Data Portraits) on the Stack v2 corpus. Base models (StarCoder2 3B, 7B and 15B, Mellum-4B, SmolLM3-3B) complete the line from the code above it, five samples each, judged by exact string match; the two versions are also scored by token likelihood. 67% of the pairs have neither version in the training data, and when only one version is present it is more often the fix. In generation, the models reproduce the buggy line far more often than the fixed line. Having seen the buggy line makes this stronger; having seen the fix helps only a little. The abstract gives no exact rates for this; they are in the figures.
- Delta: The paper uses the same basic move as N1: place the model exactly where a human made a mistake and see whether it repeats the mistake. But the units are one-line Java bugs completed by base models and judged by string match. There is no control group of lines the human wrote correctly and no executable test. The project has agents rewrite whole Solidity functions from a feature request, judges them with exploit tests, and adds a control group. The paper matters most for the project's contamination control. The project picks models whose training ended before each finding was published. That does not stop a model from having seen the human's buggy code itself, which was public in the repository before the audit report. This paper shows that exposure to the buggy version makes models repeat the bug more often. So when an agent rewrites the human's bug (4 of 6 setups for finding 63008), part of that may come from memory of the code, not from an independent mistake. The project could check, for each finding, whether the vulnerable code was public before each model's training cutoff.

### Liu2026-ChromeSecBench When AI Takes the Wheel: Security Analysis of Framework-Constrained Program Generation
- Authors: Yue Liu, Zhenchang Xing, Shidong Pan, Chakkrit Tantithamthavorn; Year: 2026 (arXiv v1 October 2025, v2 November 2025); Venue: Proceedings of the 2026 IEEE/ACM 48th International Conference on Software Engineering (ICSE 2026). The venue is stated in the paper itself and on Google Scholar; the DBLP copy used here lists only the arXiv version (2510.16823).
- URL opened: https://arxiv.org/abs/2510.16823 (arXiv abstract page); https://arxiv.org/html/2510.16823v2 (full text, HTML)
- Status: VERIFIED
- Tier: B
- Touches: N1, N5
- Summary: The authors take Chrome extensions that three earlier studies (Fass et al. 2021, Yu et al. 2023, Somé 2019) found to be vulnerable. For each one they write a short prompt that describes only what the extension does. This gives ChromeSecBench: 140 prompts in 10 functional categories. Nine LLMs (GPT-4o, Claude-3.5-Sonnet, Gemini-1.5-Pro, Gemini-2.0-Pro, Llama-3.1-405B, DeepSeek-V3, o3-mini, Gemini-2.0-Flash-Thinking, DeepSeek-R1) write each extension from scratch. The taint analyser CoCo finds the vulnerabilities; a manual check of 200 outputs found no false positives and two false negatives. Depending on the model, 18.6% to 50.0% of the generated extensions are vulnerable, rising to 83% in the authentication scenarios and 78% in the cookie scenarios. Most flaws expose browser data such as cookies, history or bookmarks to untrusted code. In the discussion, the authors report that more detailed prompts, for example prompts that name the APIs to use, raised the vulnerability rate to 60% or more for most models.
- Delta: Like the project, it starts from programs in which humans wrote a vulnerability, and asks a model to write the same functionality from a prompt that does not mention the flaw. But it never compares the model's program with the human's program, and it does not check whether the model repeats the human's specific vulnerability. The model writes the whole extension from nothing, not inside the existing code. The judge is a static taint analyser, and the authors say they did not try to exploit anything. There is no control group of programs the humans wrote correctly. The project gives the agent the same starting code as the human, judges both with the same exploit test, and adds a control group. The finding that more detailed prompts raise the vulnerability rate bears on N5. It matches the pilot result that the wording of the feature request decided the outcome.

### Le2026-AgenticPRSecurity On the Security of Agentic Pull Requests in GitHub: An Empirical Study
- Authors: Minh Nguyen Quang Le and Thanoshan Malavarayar Vijayanandan (equal contribution), Gouri Ginde, Benjamin Tan, Lorenzo De Carli (University of Calgary); Year: 2026; Venue: FPS 2026, as listed on the authors' publication page. I take FPS to be the Symposium on Foundations and Practice of Security [uncertain]; I could not confirm whether the proceedings have appeared.
- URL opened: https://ldklab.github.io/assets/papers/fps26-prs.pdf (author-hosted PDF, full text read); https://ldklab.github.io/publications/ (publication list that gives the venue)
- Status: VERIFIED
- Tier: B
- Touches: N1
- Summary: The study compares the security of 21,454 agent pull requests from the AIDev dataset with 8,103 human pull requests. The agent pull requests are 63.78% Codex, 16.47% Devin, 13.51% Copilot, 4.86% Cursor and 1.38% Claude Code. To get human code written without AI help, the human pull requests were sampled from June 2021 to June 2022, before Copilot, in the same six languages. Semgrep runs on the lines each patch adds. The rates are similar: 11.5% of agent pull requests and 12.8% of human pull requests contain at least one finding. Humans introduce more critical-impact vulnerabilities. Among agents, Codex has the highest share of high-severity findings (6.4%, against 2.9% for Claude Code). Security review is rare: only 2.2% of vulnerable agent pull requests and 1.2% of vulnerable human pull requests get any security discussion, and up to 96.4% and 98.6% of them are merged without it. CWE-754 (improper check for unusual conditions) is the most common weakness in both groups.
- Delta: It compares agents with humans on security, but on different tasks, in different repositories and years, judged by a static analyser. The authors themselves list the different time periods, the different language mix and the 2.6-fold size difference as threats to validity. The project compares the agent and the human on the same feature, from the same starting code, with the same exploit test, and adds a control group of functions the human wrote correctly. One design choice here is useful to the project: taking the human code from before AI assistants existed, so the human side is not partly AI-written. Its finding that humans introduced more critical vulnerabilities than agents is a counterpoint to the observational studies that find agent code worse.

## Found again, but already recorded in round 2 (not counted as new)

The round 2 snowball file (`lit/r2_S1_snowball.md`) holds some papers that are not yet in the master index. Two of them came up in this round:
- "Q&AEval: Benchmarking Secure Coding Ability of LLMs on Real-World Tasks" (Toran, Ballin, Miltenberger, Arzt; Proceedings of the 2026 IEEE/ACM 4th International Workshop on Software Vulnerability Management, pp. 1-8, DOI 10.1145/3786165.3788437). Block `Toran2026-QAEval` in that file. It came up in #2, #15 and #61. I opened https://conf.researchr.org/details/icse-2026/svm-2026-papers/1/Q-AEval-Benchmarking-Secure-Coding-Ability-of-LLMs-on-Real-World-Tasks, https://www.athene-center.de/forschung/publikationen/q-a-eval-benchmarking-secure-coding-ability-of-llm-5526 and the Crossref record. The abstract confirms the round 2 note: five LLMs answer over 10,000 security-related StackOverflow questions, three static scanners check both the LLM code and the human answers, and the LLM code is less secure.
- "GitHub Copilot AI pair programmer: Asset or Liability?" (Dakhel et al., Journal of Systems and Software 2023). Block `Dakhel2023-CopilotHumans` in that file. It came up in #42.

## Checked and judged tier C (not counted)

- "Zombie CVEs: Put to Rest by Humans, Dug Back Up by AI Agents" (Checkmarx blog, Eran Kinsbruner, 26 July 2026; study by Ilya Kabanov of The Weather Report, commissioned by Checkmarx). Opened https://checkmarx.com/blog/zombie-cves-put-to-rest-by-humans-dug-back-up-by-ai-agents/. It reruns SusVibes with Claude Opus 4.8, GPT-5.5, Gemini 3.1 Pro and Gemini 3.5 Flash, each in its own command-line agent. 83% to 95% of runs work, but only 24% to 36% are both working and secure, and 65% to 75% of working patches reintroduce the vulnerability. A threat-modelling step before coding raised the secure-and-working share to 43% to 49%. It is vendor grey literature that reruns an indexed benchmark, so it gets the same tier as the indexed Semgrep blog on SusVibes (`PaxtonFear2026-SemgrepSusVibes`, tier C). The numbers are useful motivation evidence.
- "Towards a Benchmark for Dependency Decision-Making" (Singla, Çakar, Amusuo, Davis; arXiv 2601.00205; abstract read). In 117,062 dependency changes, agents picked versions already known to be vulnerable in 2.46% of cases; net security impact was -98 for agents against +1,316 for humans. It is about dependency choices, not code the agent writes.
- "Tricky²: Towards a Benchmark for Evaluating Human and LLM Error Interactions" (arXiv 2601.18949; abstract read). It adds LLM-injected errors to human-written defects; no comparison on the same task.
- "LLM vs. Human Unit Tests: Fault Detection on Real Python Bugs" (arXiv 2606.08588; abstract read). Compares tests, not code.
- "Between the Commits: Process, Error, and Claim Reliability in a Wholly AI-Authored Codebase" (arXiv 2609.29744; abstract read). No human comparison.
- "DevIntent: How Much Does LLM-Generated Code Violate Developer Intent?" (ACL ARR 2026 August submission; abstract read through the OpenReview search API). Hidden tests for unstated constraints in HumanEval+ prompts; near N5 but a small pilot without security.
- "The Effectiveness of Security Interventions on GitHub" (Fischer, Höbenreich, Grossklags; ACM CCS 2023; first page of the PDF read). A causal time-series study of GitHub's security features over 50,000 repositories; a method precedent, not about AI code.
- "The Impact of Large Language Models on Open-source Innovation: Evidence from GitHub Copilot" (arXiv 2409.08379; abstract read). A natural experiment around Copilot's launch; it measures contributions, not security.
- "A Performance Study of LLM-Generated Code on Leetcode" (EASE 2024; abstract read through OpenAlex). Speed of LLM code against human solutions.
- "Simulating Students' Java Programming Errors with Large Language Models" (EDM 2026; abstract read from the PDF). Education; no security.

## Saturation summary

- 74 query rows, 71 of which returned results, across WebSearch, the arXiv API and search pages, Semantic Scholar, Google Scholar, OpenReview, OpenAlex, the ACL Anthology domain and a local copy of DBLP.
- New tier A: none. New tier B: 3 (Model See, Model Do?; When AI Takes the Wheel; On the Security of Agentic Pull Requests in GitHub).
- The new papers came from two queries only: #10 (a WebSearch about regenerating code where a developer introduced a bug) and #61 (a forward snowball of Hamer et al. 2024 on Google Scholar).
- The last five queries that returned results (#70 to #74) found nothing new. Nothing new appeared in any of the 13 query rows after #61.
- Most hits of the new phrasings were already indexed or had been screened out in rounds 1 and 2. The search for this topic looks close to saturated. The remaining gaps are citation lists that could not be read: Semantic Scholar was throttled, and the Google Scholar cited-by pages for the three new papers hit a CAPTCHA.

## Leads not followed

- "Deus Ex LLMs: AI vs Humans in Post-Quantum Cryptographic Hardware Code Generation" (Cornett, Magesh, Pendyala, Kavun, Aysu; VLSI-SoC 2025, DOI 10.1109/VLSI-SoC64688.2025.11421711). Seen in the DBLP dump (#42). Crossref has no abstract and IEEE Xplore was not opened. A related talk by Aysu suggests the comparison is about area and delay, not security.
- "Bug-Fixing in the Age of AI: Human vs. Agentic Pull Requests" (Domingues, Castor, Madeiral; MSR 2026, DOI 10.1145/3793302.3793570). Seen in the DBLP dump (#41). No abstract in Crossref, and the ACM Digital Library was not opened. Probably about bug-fix pull requests, not vulnerabilities.
- "Can generative AI bridge the gap? A quasi-experimental study of non-programmers with AI vs. programmers without AI" (Esnaola, Ramón, Lanzarini; Empirical Software Engineering 2026, DOI 10.1007/s10664-026-10813-7). Seen in the DBLP dump (#42). The Springer page needs a login and Crossref has no abstract.
- "Comparing Human-Written and AI-Generated Code" (Rosiene and Rosiene; Journal of Computing Sciences in Colleges 2025). Seen in the DBLP dump (#42); not opened.
- "Evaluating the Impact of AI Code Assistant on Software Security: A Case Study of GitHub Copilot" (V. O. Moranga). Seen on Google Scholar (#19) as a ResearchGate PDF; no other copy found (#20).
- "Trust But Verify: Analyzing the Trade-offs of AI-Generated Code" (A. Swaraj; IEEE Software 2026). Seen among the papers citing Hamer et al. 2024 (#61); no page found.
- "Automated vs. Human Security Patching Patterns in Pull Requests: Evidence from the AIDev Dataset" (Wang, Do, Jermier). A University of Waterloo course project report (plg.uwaterloo.ca/~migod/846/current/projects/04-FelixJacieBrian-report.pdf), seen in #13 and #14; not opened.
- "Learning to Commit" (arXiv 2603.26664). Seen only in a search summary (#55): an agent replays a repository's earlier commits and compares its attempts with the real diffs. No security angle.
- "Fine-tuning Language Models for Joint Rewriting and Completion of Code with Potential Bugs" (Findings of ACL 2024). Seen in the OpenReview listing (#25) and among the papers citing Dinh et al. 2023 (#60). A follow-up of the indexed Dinh et al. paper; probably tier C.
- "Behavioral Analysis of AI Code Generation Agents: Edit, Rewrite, and Repetition" (Abazar et al., MSR 2026 Mining Challenge). Seen on the Calgary lab's publication page; not opened.
- "Silent Implementation Shortfall in LLM-Written Trading Code" (S. Wang, He, V. Y. Wang; SSRN 2026, DOI 10.2139/ssrn.7555279). Seen in OpenAlex (#56) without an abstract. Outside T1, but it may bear on N7 (money lost through bugs in LLM-written code).
- The full Checkmarx report "Capability Without Security: Measuring the Functionality-Security Gap in AI-Generated Code", linked from the blog post above; not opened.
- The talk "Bad Vibes" at AppSec Day Israel 2026 (five agents build three web apps from identical prompts; 70 vulnerabilities in 15 code bases). Seen only as a session listing (#66).
- The papers citing the three new papers above (Google Scholar shows 3 each for Model See, Model Do? and When AI Takes the Wheel). The cited-by pages hit a CAPTCHA (#63), and Semantic Scholar was throttled.
