# Overview

First PhD project plan - an empirical study on an executable Proof of Vulnerability (PoV) benchmark for AI coding agents on real Solidity smart contract.

## Motivation

Developers increasingly delegate coding to AI agents. Although the AI agents perform promisingly in functional completion, their security is a major concern. In Solidity the question matters, a deployed contract holds user funds, an exploit can destroy the entire user's assets, and the code is hard to change after deployment.

Current benchmarks measure how often agent-written code is secure, but not in comaprison with human-written code. Answering that requires the same feature request, the same starting code, and the same executable test of the vulnerability for both the agent and the human. Answering that question is important for the future of software engineering, when AI agents will be writing more and more code. Whether the human developers can only focus more on the system design and architecture and have less responsibilitity in coding review and leave the coding to AI agents.

Public audit contests provide exactly this: each accepted finding points to the commit where a developer introduced a bug, together with a working exploit.

This project builds an executable Proof of Vulnerability **benchmark** on top of such findings and uses it to ask whether AI coding agents write Solidity that is more or less secure than the human developer who wrote the same feature.

In addition, the project will premilarily use the PoV to faciliate the AI Agent to learn to write more secure code and fix their introduced vulnerabilities.

## Related Work

**Agent-written code works far more often than it is secure.** SusVibes (Zhao et al., 2026, ICML 2026, arXiv 2512.03262, "Is Vibe Coding Safe?") runs agents on 186 real Python feature tasks: the best setup passes the functional tests on 57.0% of tasks but the security tests on only 11.8%. SecureVibeBench (Chen et al., 2026, ACL 2026, arXiv 2509.22097) runs agents on 105 real C/C++ tasks: the best setup is both correct and secure on 23.8% of tasks. In Solidity the stakes are higher: a deployed contract holds user funds, anyone can send the exploit transaction, and the code is often hard to change after deployment.

**These rates do not say whether agents are worse than the humans they replace.** The human-versus-AI evidence points three ways, and none of it is in Solidity. Asare, Nagappan & Asokan (2023, Empirical Software Engineering, arXiv 2204.04741) found that Copilot repeated the human's vulnerable C/C++ code in about 33% of the scenarios where a human had introduced a vulnerability. In user studies, participants with an AI assistant wrote less secure code on four of five tasks (Perry et al., 2023, ACM CCS, arXiv 2211.03622), at most 10% more critical bugs than the control group (Sandoval et al., 2023, USENIX Security, arXiv 2208.09727), or more secure code on harder problems (Asare et al., 2024, ICSE, arXiv 2308.06587).

**Existing Solidity benchmarks cannot answer it.** The costly Solidity bugs are logic and accounting errors: Zhang et al. (2023, ICSE, "Demystifying Exploitable Bugs in Smart Contracts") found more than 80% of 516 exploitable Code4rena bugs beyond automated tools. Static analysers miss about 50% of labelled Solidity vulnerabilities at precision no higher than 10% (Li et al., 2024, FSE, arXiv 2404.18186). Yet Solidity generation benchmarks such as SolEval (arXiv 2502.18793) and SolAgent (arXiv 2601.23009) grade security with these analysers or a language-model judge, and none starts from a real commit history, so none compares the agent with the human who wrote the same feature.

**Public audit contests make a fair comparison possible.** Each accepted finding traces back to the commit where a developer introduced the bug. An agent starts from that commit's parent with the same feature request, and one running exploit judges both the human's code and the agent's. A two-case pilot shows the answer is not obvious: on the Caviar rounding bug (Code4rena, 2022, Medium), Codex (`gpt-5.6-sol`) wrote the human's vulnerable line almost verbatim while Claude Code (`claude-opus-5-5`) did not; on the Ajna `moveQuoteToken` bug (Sherlock, 2023, High), neither agent did. Each agent ran once per case, so these are single outcomes, not rates (`../literature_se/rq1_case_study/report.md`, 2026-09-29).

This project asks whether AI agents, given the same starting code and the same request, write Solidity that is more or less secure than what the human developer wrote and build the PoV benchmark to evaluate the capabilities of the agents in learning to write more secure code.

## Approaches

### Coding AI agents

Use these specific LLM models x agents for the experiment configuration:

### LLMs

#### OpenAI models

Set the cost limit at $100

- gpt-5.4-mini-2026-03-17

#### Anthropic models

Set the cost limit at $100

- claude-sonnet-4-5-20250929

### Agents

Use these specific agents for the project:

1. Aider.
2. Openhands.

We have 2 LLMs x 2 Agents = 4 configurations. Each configuration will be run on the same benchmark to evaluate the security of the agent-written code.

### Research Questions

1. Does the agent reproduce the human’s vulnerability?
2. Does a runnable exploit give a more trustworthy repair?
3. Does the kind of feedback effect AI-repair agents?
4. Do the three judges agree with blinded human experts?
5. Why does the agent repeat or avoid the failure?

### The Benchmark - Run pilot on 77 potential cases from Sept 2025 public audit reports

The benchmark is a set of Solidity commits extracted from the filtered findings, each with a feature request, a vulnerable commit, and a runnable exploit. The data in the benchmark is primarily divided into 2 main groups: the vulnerable group (treatment group) and the benign group (control group). The treatment group contains the vulnerable commits where human developers introduced the vulnerability, while the control group contains the benign commits where human successfully implemented the feature without introducing a vulnerability. The corresponding feature requirements are generated for each commit in both groups by LLMs. From the feature requirements, the LLMs are prompted to generate a new implementation for each commit in both groups. The generated implementations are then compared with the original human-written code to evaluate the security of the agent-written code.

From the vulnerable group, combining the report in the finding and the commit history, LLMs are prompted to generate the executable Proof of Vulnerability (PoV) for each vulnerable commit. The PoV is then used to evaluate the security of the agent-written code generated from the feature requirements as well as help the agent to learn to write more secure code and fix their introduced vulnerabilities.

The benchmark is designed to provide a fair comparison between human-written code and agent-written code, allowing for an assessment of whether AI agents can write Solidity that is more or less secure than human developers.

### Derive from findings

1. Vulnerable Introduced Commit (VIC) - the commit where a developer introduced a vulnerability.
2. The Parent of VIC (PVIC) - the commit immediately before the VIC, which contains the same feature request but without the vulnerability.
3. The patch that fixes the vulnerability - the commit that fixes the vulnerability introduced in the VIC.

### LLM generation

Assume: the VIC might contain multiple changes regarding the multiple feature requests, but only one of the changes directly introduces the vulnerability. The other changes are not related to the vulnerability and are kept as a control group for later comparison.

LLMs are prompted to pick the implementation from the VIC that directly introduces the vulnerability. Other changes in the same VIC that are not related to the vulnerability are kept as a control group for later comparison.

Based on the code in the PVIC + the Issue/PR description (if any) of the VIC, LLMs are prompted to generate the feature requirements for the implementation in both the vulnerable group and the benign group.

Based on the feature requirements, LLMs are prompted to generate a new implementation for both the vulnerable group and the benign group. The generated code is then compared with the original human-written code to evaluate the security and functionality of the agent-written code.

Based on the findings and the VIC, LLMs are prompted to generate the executable Proof of Vulnerability (PoV) for each vulnerable commit. If LLM can generate different harnesses for the same vulnerability or the similiar vulnerabilities appear in different functions in a smart contract, LLM will mask some harnesses or vulnerabilities to create a masked PoV version. This masked PoV version is then used to fit into the AI agent in the regeneration of the patches for their vulnerable implementation. From the masked PoV, we can assess whehter AI agent can learn to avoid introducing similar vulnerabilities in the future.

The PoV is then used to evaluate the security of the agent-written code generated from the feature requirements as well as help the agent to learn to write more secure code and fix their introduced vulnerabilities.

1. Security-neutral feature requirements:
   1. Feature requests that human's implementation introduced a vulnerability.
   2. Feature requests that human's implementation did not introduce a vulnerability.
2. The PVICs where the functionalities are not implemented yet.
3. The implementation corresponding to the feature requests in both groups, generated by LLMs.
4. The PoV for each vulnerable commit, generated by LLMs.
5. The regenerated implementation for the vulnerable implementation by AI agents, where the masked PoV is applied to help AI agents learn from their mistakes and avoid introducing similar vulnerabilities in the future.

The exploit must succeed on the vulnerable commit, fail on the fix, and compile but fail on the parent. The check is SecureVibeBench’s (Chen et al., ACL 2026) or SusVibes (Zhao et al., ICML 2026); we reuse it with a Foundry exploit.

### Pipeline

1. Get the data from the filtered findings (77 findings from Sept 2025 public audit reports).
2. For each finding, get the VICs and their corresponding PVICs.
   1. Get the vulnerable implementation and benign implementation from the VICs.
3. Generate the feature requirements for each implementation in both groups by LLMs.
4. Generate the full PoV for each VIC. Hold-out some harnesses or vulnerabilities to create masked PoV.
5. Generate the new implementation for each feature requirement in both groups by LLMs.
6. Regenerate the implementation for the vulnerable implementation by AI agents, where the masked PoV is applied to help AI agents learn from their mistakes and avoid introducing similar vulnerabilities in the future.
7. Evaluate the security of the agent-written code generated from the feature requirements in both groups by running the PoV on them.
8. Evaluate the security of the regenerated implementation for the vulnerable implementation by AI agents, where the masked PoV is applied to help AI agents learn from their mistakes and avoid introducing similar vulnerabilities in the future.
9. Analyze the results, visualize the insights, and answer the research questions.
10. Estimate the financial loss if the PoV is applied to an case. If the loss cannot be estimated in concrete amnount of money, we will estimate the loss in terms of the number of percentage of the users' funds.
