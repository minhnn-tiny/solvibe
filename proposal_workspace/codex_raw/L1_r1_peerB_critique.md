## Strengths to keep

- **C2:** The problem is important. The proposal connects agent use, real Solidity bugs, and financial consequences.
- **C1–C3:** Measuring both avoided human bugs and newly introduced agent bugs is a promising contribution. The faulty-test hypothesis could provide an insight that extends beyond Solidity.
- **C4–C6:** Keep executable PoV confirmation, separate functional checks, frozen held-out attacks, and explicit treatment of invalid executions.
- **C7:** The pilot exposes real construction and evaluation problems. Its limitations are useful evidence for designing the full study.
- **C5–C8:** Keep offline execution, restricted network access, honest developers and agents, paid expert review, and responsible disclosure.

## Points

### P1 [Blocking] [C4] The human control cannot fail its own reference check

**Section:** 4; 5.9; 6.2.

**Problem:** The proposed judge cannot discover a vulnerability in the human version of a group N function. This makes \(h_N\) zero by construction, despite the promise to measure it. It also excludes vulnerabilities shared by the human and agent implementations.

**Evidence:** Section 4 defines the reference for group N as “the human’s code.” Section 5.9 counts a flaw only when a PoV “passes on the version and fails on the reference.” When judging the human version, those are the same program. Section 6.2 nevertheless includes “the human’s rate in group N, found by the same checks.”

**Required change:** Replace reference disagreement as the definition of vulnerability with an independently justified security property, so the same PoV can establish a violation in either author’s code even when both implementations violate it.

### P2 [Blocking] [C4] Known group sizes do not correct task-selection bias

**Section:** 3, contribution 1; 5.1–5.2; 6.2; 8.

**Problem:** Counting every audit-scope function does not make the constructed tasks representative of those functions. Group V tasks must have usable history, a suitable fix, and a buildable PoV. Some counted functions therefore have no chance of entering the experiment. The proposed weights cannot recover their outcomes.

**Evidence:** Section 5.2 maps “every High and Medium finding … including those we do not turn into tasks.” Section 5.1 selects tasks through history and PoV construction. Section 8 may further restrict V to reports containing proofs of concept. Yet contribution 1 says the design “removes the selection problem.” The proposal also does not specify how unequal sampling across protocols enters the weights.

**Required change:** Define a fixed, task-eligible population before sampling, then specify probability sampling and inclusion weights within each protocol and stratum, with conclusions limited to that population.

### P3 [Major] [C4] The experiment does not recreate the human’s development conditions

**Section:** 1; 4; 5.4–5.5; 6.8.

**Problem:** This is a retrospective replacement experiment. It does not estimate how an agent would perform instead of the original developer under the same conditions. Removing faulty tests and comments cannot remove every consequence of later development.

**Evidence:** The abstract promises a request carrying “only what the human knew.” Section 4 says “at the same point in the codebase.” Section 5.4 instead gives the agent the audited snapshot, including later code and tests. Section 5.5 even permits surrounding code from that snapshot as a supposedly historical source. The pilot’s failed parent checks explain the practical choice, but do not establish equivalence.

**Required change:** Rewrite the title, abstract, setting, and RQ1 consistently as a comparison between agent replacements and historical human implementations in a fixed audited snapshot, without claiming equal historical conditions.

### P4 [Major] [C1] The novelty statement overclaims the shared-exploit comparison

**Section:** 2; 3; 7.

**Problem:** Running an exploit on human code and regenerated agent code is already part of the closest benchmark’s method. The defensible distinction is the broader sampling design and measurement of additional vulnerabilities, not simply using the same exploit.

**Evidence:** Section 2 claims no study “judges both sides with the same executable exploit.” **SecureVibeBench** validates human vulnerability-introducing commits with PoVs and uses those PoVs to evaluate agent implementations (§3.2). Its limitation is sampling human failures, not absence of a shared executable check. [SecureVibeBench](https://aclanthology.org/2026.acl-long.1107.pdf). Likewise, shown exploits and separate held-out repair oracles already appear in **P2Patch**. [P2Patch](https://arxiv.org/abs/2610.20245).

**Required change:** Rewrite the novelty claim around estimating avoided and newly introduced vulnerabilities in a defined population and testing the effect of faulty repository tests, explicitly treating shared PoVs and held-out repair evaluation as prior methods.

### P5 [Major] [C4] Capture-recapture does not justify corrected vulnerability rates

**Section:** 3, contribution 3; 5.9, steps 6–7; 6.8.

**Problem:** The audit and proposed procedure are not independent detectors. The procedure consumes audit findings and uses audit-derived seeds. Hiding the finding from an LLM reviewer does not remove those dependencies. An estimate of missed bug counts would also need another model to become an estimate of the fraction of functions containing bugs.

**Evidence:** Step 4 gives reviewers “the audit’s known findings.” Step 3 seeds fuzzing with PoVs. Step 7 nevertheless calls the audit and procedure “two independent detectors.” There is also no corresponding historical audit of agent-generated code. The cited capture-recapture literature warns that estimates depend on inspector count and defect detectability; it does not validate this correction. [Briand et al.](https://api.openalex.org/works/doi:10.1109/32.852741).

**Required change:** Replace the corrected-rate claim with observed PoV-confirmed rates and an explicit sensitivity analysis showing how different missed-vulnerability rates for human and agent code would change the conclusion.

### P6 [Major] [C6] The outcome denominator is undefined and contradicts the motivating example

**Section:** 5.11; 6.2; 8.

**Problem:** The proposal does not define whether vulnerability rates include functionally incorrect implementations. Excluding them changes the comparison’s population; including them requires security evaluation rather than treating them only as functional failures.

**Evidence:** Section 6.2 says functional failures are “reported separately and never counted as secure,” without defining their contribution to \(a_V\) and \(a_N\). Section 8 proposes reviewing only versions that pass functional tests. But the two vulnerable control implementations behind the “2 of 11” example both fail `test_iterateUp_emptyRange`. The proposed shortcut would exclude the very examples motivating the second term. See the [63008 results](../pilot/tasks/63008/feature_tasks/results.md).

**Required change:** Add an outcome table defining every denominator and the treatment of compilation failure, functional failure, confirmed vulnerability, no confirmed vulnerability, and unresolved evaluation, and derive the primary comparison from that table.

### P7 [Major] [C3] The acceptance criteria still depend too heavily on the human fix

**Section:** 5.6–5.7; 5.9–5.10.

**Problem:** Matching the human fix’s execution failure is not a general test of security. A valid defensive check can stop an attack earlier. Conversely, removing tests that fail on the fix can leave too little evidence that the feature still works. The proposal needs a semantic acceptance rule, not only a particular execution signature.

**Evidence:** Section 5.6 counts an attack as blocked only when it fails “at the same place” as the human fix. Other outcomes go to a person without a decision rule. Section 5.9 removes fault-enforcing tests but does not require replacement functional coverage. IDEA.md records that the pilot’s vulnerable iterator had no usable functional test and that the transplanted human fix had an empty-range problem.

**Required change:** Add a per-task acceptance specification stating required legitimate behavior and forbidden attacker outcomes, with rules for accepting defensive reverts and rejecting disabled functionality independently of the human fix’s exact trace.

### P8 [Major] [C4] The steering test does not establish a neutral request

**Section:** 5.5.

**Problem:** A request should change which implementation best satisfies a task. Such a change is not necessarily leakage. Conversely, unchanged LLM preferences do not show that the request will not steer a coding agent. Iterative rewriting against vulnerable and fixed versions also makes the final request depend on information withheld from its initial writer.

**Evidence:** Step 1 preserves distinguishing requirements when historical sources support them. Step 2 then rewrites requests whenever a panel moves toward either version beyond an unspecified margin. No exception preserves those legitimate requirements. The proposal offers no validation connecting panel preference changes to agent behavior.

**Required change:** Replace the panel-based acceptance gate with a protocol that freezes requests after a provenance audit and measures wording effects through randomized, within-function agent comparisons, treating panel scores only as diagnostics.

### P9 [Major] [C4] The pilot does not identify the effect of request wording

**Section:** 3, Insight 3.

**Problem:** The reported difference confounds wording with task identity. The run-level Fisher test also treats correlated runs as independent observations. It cannot support a causal interpretation of the prompt effect.

**Evidence:** The proposal highlights “13 compiled runs” against “3 of 15” and \(p=0.00002\). The [pilot report, §5.4](../docs/pilot/pilot_results.md) shows four different tasks in each wording group; no task received both wordings. The same report gives a task-level permutation result of \(p=0.029\), but task-level testing still does not remove the confounding.

**Required change:** Rewrite Insight 3 as a descriptive association across eight tasks, remove the run-level significance claim, and identify the proposed within-function experiment as the test of causation.

### P10 [Major] [C6] The controlled experiment does not isolate faulty test execution

**Section:** 6.3–6.4.

**Problem:** Removing tests and comments together cannot distinguish their effects. Comparing execution access across agent frameworks also confounds execution with other tool and prompt differences. In repair, naturally occurring faulty-test presence is only an observed moderator; it does not establish why execution helps or hurts.

**Evidence:** Section 6.3 removes “those tests and comments” together and does not specify randomized execution access within the same configuration. Section 6.4 retains P-E0 and P-E2 but moves E1 to a subset. P-E2 permits many activities beyond running faulty tests. **ImpossibleBench** already studies conflicts between specifications and tests and changes test access and feedback; this proposal needs a more specific mechanism test. [ImpossibleBench](https://arxiv.org/abs/2510.20270).

**Required change:** Specify a within-task factorial experiment that crosses faulty-test presence with permission to execute those tests, holds comments and file tools fixed, and measures the interaction in both generation and repair.

### P11 [Major] [C6] The power calculation does not match the planned analysis

**Section:** 6.2–6.4.

**Problem:** The stated power is not established for the proposed clustered, paired, multiple-comparison analysis. Repeated runs increase information about an agent’s behavior, but do not create additional human implementations or protocols.

**Evidence:** The table assumes an intraclass correlation of 0.69 from eight pilot tasks and uses unadjusted \(\alpha=0.05\) for one configuration. The planned analysis resamples protocols and applies Holm correction across six configurations. The table does not expose assumptions about protocol correlation, paired human-agent outcomes, or uncertainty in \(h_N\). “Pooling configurations” changes the quantity being estimated. RQ3 has no corresponding calculation for its interaction.

**Required change:** Replace the table with a reproducible simulation of the actual sampling and analysis plan, including plausible correlation ranges, multiplicity, and the minimum effect detectable for the repair interaction.

### P12 [Major] [C6] The measurement validation does not establish comparable detection

**Section:** 5.8–5.9; 6.5.

**Problem:** Identical-looking procedures need not have equal sensitivity on human and agent code. Here, even the reviewer roster changes with the generator’s model family. Expert agreement alone cannot establish that unflagged versions are free of vulnerabilities.

**Evidence:** Section 5.8 replaces reviewers for code from their own model family. Section 5.9 measures sensitivity using known human bugs. Section 6.5 proposes sensitivity and specificity against expert consensus, but does not specify executable confirmation, an unresolved category, review budgets, or weighting for the stratified validation sample.

**Required change:** Add one validation protocol with a common blinded reviewer roster and search budget across authors, executable adjudication of expert findings, an unresolved category, and sampling-weighted accuracy estimates with uncertainty.

### P13 [Major] [C6] The configuration plan does not ensure strong, comparable baselines

**Section:** 5.8; 6.6.

**Problem:** The six configurations are useful experimental setups, but they do not by themselves establish performance of strong supported agents. The unspecified frontier subset may also give different models different task populations.

**Evidence:** Section 5.8 promises “one frontier configuration per vendor” without naming configurations, selection rules, or a common comparison set. IDEA.md records that Codex uses fallback prompts for both selected models, that Sonnet requires API translation, and that reasoning budgets differ across frameworks. Those details materially affect interpretation.

**Required change:** Add a configuration manifest that distinguishes experimental integrations from supported configurations and specifies strong supported baselines, reasoning budgets, tool permissions, and the common task set used for direct comparisons.

### P14 [Major] [C5] Executable PoVs need enforceable attacker assumptions

**Section:** 4; 5.6; 5.11.

**Problem:** Local execution establishes a vulnerability only if the setup and attack obey the threat model. The proposal does not specify how it checks reachable states, mock behavior, attacker funding, or privileged setup actions. Its privileged-role exception also conflicts with its unprivileged-attacker definition.

**Evidence:** Section 4 excludes privileged attackers “unless the finding’s own severity assessment assumes it,” then defines every vulnerability through an “unprivileged attacker.” PoVs run with mock tokens. Section 5.11 reports profit from a chosen initial reward balance, which establishes that scenario’s outcome rather than an unrestricted loss estimate.

**Required change:** Require a threat-model record for every task that fixes attacker roles, resources, reachable initial state, permitted environmental actions, mock assumptions, and the impact assertion, with eligibility checked against that record.

### P15 [Major] [C7] The feasibility case prices generation but not the main work

**Section:** 5; 8; 10.

**Problem:** The likely bottleneck is constructing and validating tasks and judges, not the first-round API bill. The schedule lacks evidence that one student can complete that work at the proposed scale.

**Evidence:** The target includes 180 functions, 3,240 initial agent runs, additional interventions and repairs, differential harnesses, PoV variants, confirmation attempts, and about 150 versions reviewed by two auditors. Section 8 estimates roughly $850 for initial runs but gives no total labor or evaluation budget. Its fallback to reports already containing PoCs would also change the sampling population.

**Required change:** Replace the feasibility paragraph with a staged resource plan based on measured construction time, total evaluation cost, and auditor availability, with a month-two decision that fixes the attainable population and study scope before large-scale runs.

### P16 [Major] [C8] Release eligibility is assumed rather than checked

**Section:** 9.

**Problem:** A public audit report does not by itself establish that every affected deployment or fork is safe. The ethics plan also makes elapsed time sufficient for releasing a newly discovered exploit, without a stated review of remaining exposure.

**Evidence:** Section 9 asserts that known findings concern bugs “fixed before deployment,” but the selection procedure contains no corresponding check. It releases new PoVs when a bug “is fixed or 90 days pass.” The planned corpus refresh could include cases that do not meet the asserted premise.

**Required change:** Replace the blanket release rule with a per-finding release decision that records remediation evidence and disclosure status, with unresolved exposure reviewed at the disclosure deadline before exploit details are published.

### P17 [Minor] [C2] The incident headline claims more than the evidence establishes

**Section:** 2.

**Problem:** The significance argument does not need a claim about the first AI-linked Solidity loss. The evidence establishes a reported association, not chronological priority or authorship of the faulty decision.

**Evidence:** The heading states, “The first loss linked to agent-assisted Solidity has happened.” The paragraph supports this with co-author trailers and news attribution, while acknowledging that Moonwell did not blame AI. The literature review, §4.7, explicitly distinguishes evidence of tool use from evidence of who chose the line.

**Required change:** Describe Moonwell as a reported incident involving AI-assisted commits and explicitly state that the faulty line’s authorship is unestablished.

## Counts

- **Blocking:** 2
- **Major:** 14
- **Minor:** 1

## Most important change

Make the human-agent comparison identifiable before expanding the benchmark. The current design cannot detect human bugs in group N and cannot use whole-codebase weights to represent functions excluded during task construction. Fix the independent security criterion, eligible population, and outcome denominators together. Then frame the result as a retrospective comparison of implementations. This preserves the student’s core problem while giving the faulty-test and PoV-repair experiments a sound foundation.