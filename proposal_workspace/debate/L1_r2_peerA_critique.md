# Loop 1, round 2: Peer A's critique of proposal_v2.md

Critic: Peer A (Claude Code). Author for this round: Peer B (Codex).

## Strengths to keep

- The estimand split into vulnerabilities avoided and vulnerabilities added, over a defined eligible population with inclusion weights (sections 3, 5.2, 6.3).
- Property-based PoVs, so the human's code can fail the same check as the agent's (section 4).
- The per-protocol threat-model record and the per-task acceptance specification (sections 4, 5.6).
- The configuration manifest that separates experimental integrations from supported configurations (section 5.9).
- The month-2 decision gate (section 8).
- Frozen requests with diagnostics only, and the within-function wording experiment (sections 5.5, 6.5).

## Points

### Q1 [Blocking] [C4] A property violation is not attributed to the target function

Section: 4 ("What counts as a vulnerability"); 5.10.
Problem: This is Peer B's N3, which I endorse. The snapshot keeps the audit's other known vulnerabilities, so a PoV can violate a property through an unchanged routine while the target function is correct. Nothing in the procedure ties a confirmed violation to the target.
Evidence: section 4 says a version is vulnerable if a PoV "drives the protocol into a state that violates one of the recorded security properties", and section 5.10 has no attribution step.
Required change: Add an attribution rule to the definition and to the confirmation step: a flaw counts against a version only if the PoV passes with that version and fails when only the target function is replaced by a version without the flaw (the human fix for group V; for group N, the other author's version when it lacks the flaw, or a minimal target-only correction reviewed by a person), with the legitimate-behaviour suite passing in both.

### Q2 [Major] [C1] Two close papers found in literature round 5 are missing, and the repair "report" arm is not positioned against them

Section: 3, 6.4, 6.8, 7.
Problem: Round 5 found two ICLR 2027 submissions (OpenReview API records, abstracts read; `lit/r5_V1_comparison_sc.md`). SysRepair-Bench runs 313 repair scenarios twice, with and without the vulnerability report, judged by an exploit and a service-health check; the median success is 90.0% with the report and 49.4% without, and fixes that block the exploit by breaking the service are more common without the report. ConstraintDial rebuilds 203 public smart-contract cases and mutates them so the public attack fails, lowering success when the agent is given the public answer by 10.9 points. Round 5 also found Endor Labs reports (grey literature, `lit/r5_V3_method_judges.md`) that 137 of 182 cheating cases on SusVibes were recall from training, and that checking only the final diff missed 18 of 38 recall cases.
Evidence: v2's section 7 table has no row for either paper; v2's contamination check (section 6.8) looks only at whether the final code matches the human's body or the fix word for word.
Required change: Cite SysRepair-Bench and ConstraintDial in section 7 with precise deltas, state that "a report helps repair" is prior evidence and that the study's repair question is the interaction between fault-enforcing tests and test execution, and extend the memorization probe in section 6.8 to the agent's full edit history, not only the final diff.

### Q3 [Major] [C4] The primary denominator is still inconsistent

Section: 6.2, 6.3.
Problem: Peer B's P6 follow-up, which I endorse. Non-compiling agent versions leave the primary rate, but the stratum weights and the human rates still cover every sampled function. A function where an agent never compiles then has no agent rate but full weight.
Evidence: section 6.2 excludes category X from the primary rate; section 6.3 weights each function by its inverse inclusion probability.
Required change: Define the primary outcome at the run level over all runs, with a non-compiling run counted as its own outcome, and give the estimand for "a deployable vulnerable version" and the estimand for "any vulnerable compiled version" explicitly, each with a denominator that both authors share.

### Q4 [Major] [C4] The blocking rule can mislabel a valid execution

Section: 5.6.
Problem: Peer B's P7 follow-up, which I endorse. "Its impact assertion is not reached" treats a PoV that runs to the end and shows that the forbidden outcome did not happen as if it never ran.
Evidence: section 5.6, "An attack is blocked when its impact assertion is not reached and the legitimate-behaviour suite passes."
Required change: Define three PoV results explicitly (forbidden outcome observed; forbidden outcome checked and absent; could not be checked) and define "blocked" as the second result plus a passing legitimate-behaviour suite, with the third result going to the unresolved category.

### Q5 [Major] [C6] Turning the terminal off does not isolate execution of the fault-enforcing tests

Section: 6.4.
Problem: Peer B's P10 follow-up, which I endorse. With the terminal off, the agent also loses builds, scripts and search; the interaction then measures terminal access, not running the faulty tests.
Evidence: section 6.4 uses "the configurations whose terminal can be turned off".
Required change: Keep the full terminal in both execution arms and switch only the repository's test runner: in the "no test execution" arm the test command is disabled for the repository's existing tests (the agent can still build, run scripts and write its own tests), and log every attempt to run the disabled command.

### Q6 [Major] [C6] The power simulation is not calibrated and does not implement the planned tests

Section: 6.3, 6.4; `tools/power_sim.py`.
Problem: Peer B's N1 and P11 follow-up, which I endorse and checked in the code. The script draws probabilities around `logit(aV)` with random effects and then reports Δ from `aV`, so its "true Δ" is not the simulated marginal difference. It also uses a jackknife z-test instead of the planned bootstrap, and a probability-scale difference in differences instead of the planned logistic interaction.
Evidence: `power_sim.py` lines generating `fv` and `fn`, and the `true = ...` line.
Required change: Calibrate the intercepts so the simulated marginal rates equal the stated ones, implement the primary bootstrap test and the logistic interaction, report the rejection rate under the null as well as the alternatives, and update both power tables.

### Q7 [Major] [C4] Candidate discovery is not symmetric between the authors

Section: 5.10, steps 3 to 5.
Problem: Peer B's N2 and P12 follow-up, which I endorse. The human version is compared against every agent run, each agent version against the human only; and a PoV found for one version is not replayed on the others.
Evidence: section 5.10, step 3, "for the human's version it is the agent's code from each run".
Required change: Make discovery function-level: every version gets the same search budget (one differential campaign against a fixed reference set, the same reviewer calls, the same confirmation budget per candidate), and every validated PoV for a function is replayed on every compiled version of that function, human and agent.

### Q8 [Major] [C7] The workload and budget are understated, and the descoping order is missing

Section: 8, 10.
Problem: Peer B's P15 follow-up, which I endorse. RQ2 with 30 functions, a 2 x 2 design, four configurations and three runs is 1,440 runs in writing alone, and repair adds an information factor; RQ3 adds 1,440 runs; the stated review tokens are miscounted. A first-year student also needs to know what gets cut first.
Evidence: section 8 states about 2,500 runs for RQ2 and RQ3 and about 50 million input tokens for review.
Required change: Recount every experiment's runs and tokens from the design, add the expert hours, and state the order in which experiments are cut at the month-2 gate (for example: RQ3 wording first, then the repair half of RQ2, never the RQ1 core).

### Q9 [Minor] [C6] Injected fault-enforcing tests need a realism check

Section: 5.8, 6.4.
Problem: Injected tests could be easier or harder for agents to notice than natural ones, which would limit what the injected half says about natural repositories.
Evidence: section 5.8 asks only that a person check that injected tests "look like the repository's other tests".
Required change: Add a blinded check in which a person and an LLM try to pick the injected test out of a set of real tests, and report the effect separately for natural and injected tests as the primary split.

## Counts

- Blocking: 1
- Major: 7
- Minor: 1

## Most important change

Make every counted flaw attributable to the target function, and make discovery and replay identical for the two authors. Without these two changes, the estimate of vulnerabilities added by agents is not defensible, whatever the sample size.
