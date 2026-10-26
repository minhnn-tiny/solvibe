## Point status

P1: resolved  
P2: resolved  
P3: resolved  
P4: resolved  
P5: resolved  
P6: not resolved, because excluding noncompiling agent outputs while retaining population stratum weights and human rates over all sampled functions makes the primary comparison inconsistent (§§6.2–6.3).  
P7: not resolved, because “impact assertion is not reached” excludes a valid execution that reaches the assertion and demonstrates that the forbidden outcome did not occur (§5.6).  
P8: resolved  
P9: resolved  
P10: not resolved, because switching the whole terminal off changes access to non-test commands as well, so the factorial identifies an interaction with terminal access rather than specifically with permission to execute the faulty tests (§6.4).  
P11: not resolved, because the simulation changes marginal vulnerability rates without updating “True Δ” and does not simulate the stated primary tests, as detailed in N1.  
P12: not resolved, because the fixed reviewer roster addresses one asymmetry but the revised candidate search gives the human implementation more comparison opportunities than each agent implementation, as detailed in N2.  
P13: resolved  
P14: resolved  
P15: not resolved, because the expanded experiments and review budget remain materially understated: with 30 functions and four configurations, RQ2 requires 4,320 runs before location-only arms, RQ3 adds 1,440, and the stated review inputs total 120 million tokens rather than 50 million (§8).  
P16: resolved  
P17: resolved  

## New problems

### N1 [Major] [C6] The simulation reports power for larger effects than the table states

**Section:** 6.3–6.4; `tools/power_sim.py`.

**Evidence:** In [power_sim.py](/Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/tools/power_sim.py:26), agent probabilities are generated as `expit(logit(aV) + protocol_effect + function_effect)`, with analogous code for `aN`. Consequently, `aV` and `aN` are conditional probabilities at zero random effects, not the marginal rates used in the proposal’s estimand. Nevertheless, line 45 calculates “true” Δ directly from those inputs.

For the table’s `aV = 0.6`, `aN = 0.10`, and `hN = 0.02`, numerical integration of the script’s probability model gives:

| Protocol SD | Function SD | Expected marginal Δ | Reported “True Δ” |
|---|---|---|---|
| 0.5 | 1.5 | approximately +0.0931 | +0.032 |
| 1.0 | 2.0 | approximately +0.1249 | +0.032 |

Thus, the reported power does not establish sensitivity to a 3.2-point difference. The purported correlation sensitivity range also changes the underlying effect size substantially.

There are further analysis mismatches: RQ1 uses a normal test with a jackknife standard error rather than the proposed bootstrap procedure; RQ2 tests a probability-scale difference in differences rather than the primary logistic interaction. Those interaction null hypotheses are not generally equivalent.

**Required change:** Replace the power results with a validated simulation that calibrates intercepts to the intended marginal rates, implements the chosen primary estimators and tests, and checks their rejection rates under both null and alternative scenarios.

### N2 [Major] [C4] Candidate discovery gives unequal opportunities to human and agent code

**Section:** 5.10, steps 3–5.

**Evidence:** For an agent version, differential fuzzing compares it with the human implementation; for the human version, it compares against “the agent’s code from each run.” One human implementation therefore receives candidate evidence from multiple comparisons, while each agent implementation receives one comparison. The fixed budget is per candidate, not per version.

The proposal does not require every discovered PoV to be replayed across all implementations of that function. A vulnerability found through one comparison could therefore count against the human while remaining undetected in another agent version that shares it. Identical reviewer prompts do not correct this difference in discovery opportunities.

**Required change:** Adopt a function-level discovery protocol with matched per-version search budgets and common replay of every validated PoV across all compatible human and agent versions.

### N3 [Blocking] [C4] A protocol-level violation is not sufficient to blame the target function

**Section:** 4, “What counts as a vulnerability”; 5.10.

**Evidence:** The revised definition labels a function vulnerable when a PoV “drives the protocol into a state that violates one of the recorded security properties.” Every task retains the rest of the audited snapshot, including its known vulnerabilities.

This permits an exploit of an unchanged vulnerable routine to establish a property violation while the target function is an unrelated, correct helper. The sentence excluding “bugs in code the agent did not write” states the intended scope, but the confirmation procedure supplies no attribution check that enforces it. Removing the old reference-disagreement rule correctly permits shared flaws; it also makes an explicit attribution rule necessary.

**Required change:** Add a target-function attribution requirement for every counted flaw, supported by reviewed root-cause evidence and, where applicable, a target-only corrective intervention that preserves legitimate behavior and removes the demonstrated violation.

DISAGREE: [P6, P7, P10, P11, P12, P15, N1, N2, N3]