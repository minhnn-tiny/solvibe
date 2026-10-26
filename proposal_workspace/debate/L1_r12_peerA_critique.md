# Loop 1, round 12: Peer A's critique of proposal_v13 and consensus vote

Proposal under critique: `proposal_v13.md` (Peer B; raw `codex_raw/L1_r12_peerB_revision.md`). Peer B's revised iteration-2 rebuttal is saved as `debate/rebuttal_iter2_peerB_r12.md`.

## Check

The v17 and v18 numbers in sections 6.3 and 6.4 match `tools/power_results_v17.txt` and `tools/power_results_v18.txt`. The 63008 Version 2 rows match `evidence/63008/logs/v2_summary.log`. The timings match `evidence/timings.md`. The per-protocol allowance is (1,050 − 120 − 30) / 20 = 45 hours.

R11.1, R11.3, R11.6 to R11.14 are resolved in v13. R11.2 and R11.5 are resolved in design; their evidence is discussed below.

## Remaining issues

### C7 (Blocking, shared with Peer B's own "Remaining concerns")

No development case has been timed with a person doing the human-review steps. Neither peer can produce this. The user has been asked and has not answered. If the next round brings no new evidence on this point, it is stalled and goes to the committee as an open question.

### P1 (Major, C4 and C7): a protocol work allowance that ends in unresolved outcomes makes the adverse-bound rule decide the study

**Problem.** Section 5.2 says that if work exceeds a protocol's allowance, "remaining outcomes are recorded as unresolved", and section 6.2 counts failure to construct a task as unresolved. Under the adverse-bound rule this is ruinous: `tools/power_results_v17.txt` shows that 2% unresolved results for both authors cut power for the larger differences from 0.65–0.97 to 0.32–0.67 at 20 protocols, and 5% to 0.04–0.14. For a function whose task was never built, both authors' outcomes are missing together, and the bounds set the pair to the extreme values, so each such function moves the bound by a full unit. The allowance also binds often at the planning rates: with the earlier V assumption, a protocol under the six-V cap has on average about 3.9 V and 8 N functions, which at the assumed unit rates costs about 43 hours at the optimistic end and about 100 hours at the pessimistic end, against a 45-hour allowance.

**Required change.** Split the allowance by stage. (a) A construction allowance per protocol: a function whose task is not built within it leaves the eligible population by a rule applied before any implementation exists, identically for both authors; the primary estimand is restated for constructible functions, the share and profile of excluded functions are reported, and the full-frame bounds are a secondary analysis. (b) Fixed per-implementation budgets for campaigns and confirmation, which always end in a completed result ("not confirmed" when the budget ends). (c) "Unresolved" only for evaluations that cannot run after the frozen reruns. Show the per-protocol cost arithmetic against the allowance at the assumed rates.

### P2 (Major, C6): the RQ1a criterion was not checked on the full interval

**Problem.** Peer B's own remaining concern. v18 checked one bound.

**Evidence produced.** `tools/power_sim_v19.py` (results `tools/power_results_v19.txt`) evaluates the full interval enclosing both identification bounds, for the fixed allocation (20 protocols, V cap 6, two attempts), with unresolved shares 0 to 0.05:

| Frame | Unresolved share | Largest mean full-interval half-width | Worst coverage | Excludes −0.10 at true −0.33 |
|---|---|---|---|---|
| Earlier V assumption | 0 | 0.167 | 0.950 | 0.83 |
| Earlier V assumption | 0.005 | 0.178 | 0.963 | 0.83 |
| Earlier V assumption | 0.01 | 0.186 | 0.975 | 0.79 |
| Earlier V assumption | 0.02 | 0.203 | 0.988 | 0.69 |
| Earlier V assumption | 0.05 | 0.253 | 0.995 | 0.35 |
| Counted spread | 0 | 0.314 | 0.953 | 0.38 |
| Counted spread | 0.05 | 0.394 | 0.988 | 0.14 |

So the criterion holds for the fixed allocation only in a frame like the earlier V assumption and only with unresolved shares of about 0.005 or less. In a frame like the counted spread it fails at any unresolved share.

**Required change.** Put these results in section 6.4 and state the conditions under which RQ1a can be principal: a refreshed frame with V counts like the earlier assumption, and an unresolved share near 0.005. Otherwise the readiness decision of section 8 applies.

## Vote

**DISAGREE: [C7 human development evidence; P1 work allowance and unresolved outcomes; P2 full-interval criterion]**
