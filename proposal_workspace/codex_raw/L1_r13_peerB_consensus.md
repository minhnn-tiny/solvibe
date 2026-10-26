## Point status

- **C7: not resolved.** No human-timed development case has been added. The proposal correctly acknowledges this, but the committee’s empirical feasibility requirement remains unmet.
- **P1: not resolved.** Separating construction from campaign budgets is sensible, but the new exclusion rule changes the population after sampling without updating the estimand, weights or stratum shares. This introduces the issue below.
- **P2: resolved as planning evidence.** V19 computes both bounds on the same simulated observations and evaluates the full interval. Its reported numbers match the results file. This does not establish readiness under the eventual frame and construction process.

## Remaining issues

### C7 [Blocking] [C7] Human feasibility evidence remains absent

**Sections:** 8 and 10.

The proposed 45-hour protocol allowance is a resource limit, not demonstrated throughput. The added estimates of about 43 optimistic hours and 100 pessimistic hours are consistent with the stated unit-cost expressions. They reinforce the dependence on favorable costs; they do not resolve it.

**Required change:** Complete and report the specified human development cases, including probability-selected N functions and failed attempts, before declaring the minimum study feasible for confirmatory collection.

### R13.1 [Major] [C4, C6] Construction exclusions do not define the population used by the estimator

**Sections:** 5.2, 6.2–6.4 and 8.

Section 5.2 now targets functions whose tasks can be constructed within a shared protocol allowance. Section 6.3 still targets:

> “the finite eligible function frame declared before sampling”

and uses its population stratum shares \(\pi_s\).

These are different populations. If construction success differs between V and N, retaining the original shares does not estimate the comparison over constructible functions. Reporting exclusion counts does not correct the weights.

There is a further problem: under a shared construction allowance, a function’s eligibility can depend on which other functions were sampled and processed before it. The same function might qualify in one draw and fail in another. A frozen processing rule does not make this a fixed function-level eligibility attribute. Applying it equally to both authors preserves pairing but does not establish the claimed population inference.

V19 does not simulate this construction-selection process. Its V and N counts describe the generated frame, with no subsequent construction exclusions. Consequently, its precision results cannot establish precision for the new target merely by checking the initial V count.

**Required change:** Replace the construction-exclusion rule with one coherent constructible-domain design: define eligibility through a fixed per-function construction procedure and allowance, and specify domain-weighted estimation—including the constructible stratum shares and their uncertainty—then include that selection process in the readiness simulation.

### R13.2 [Minor] [C6] V19’s scenario result is stated as a universal launch threshold

**Sections:** 6.4 and 8.

The sentence that the criterion “needs V counts like the earlier assumption and an unresolved share of about 0.005 or less” overgeneralizes the simulated grid.

The verified results are:

| Frame | Equal unresolved shares | Largest mean full-interval half-width | Worst coverage | Exclusion rate near −0.33 |
|---|---:|---:|---:|---:|
| Earlier assumption | 0 | 0.167 | 0.950 | 0.83 |
| Earlier assumption | 0.005 | 0.178 | 0.963 | 0.83 |
| Earlier assumption | 0.01 | 0.186 | 0.975 | 0.79 |
| Counted spread | 0 | 0.314 | 0.953 | 0.38 |
| Counted spread | 0.05 | 0.394 | 0.988 | 0.14 |

These are estimates from 400 studies per scenario. They depend on the outcome, dependence and detection assumptions, not just V counts and unresolved shares. The difference between estimated exclusion rates of 0.79 and 0.80 also needs Monte Carlo uncertainty when used for a launch decision.

Section 6.3 already says that a small development sample cannot establish a population unresolved rate below 0.005. The new wording should preserve that caution.

**Required change:** Replace the categorical threshold with a statement that these tested scenarios pass or fail the estimated criterion, while launch requires validation under the actual constructible-domain design and a prespecified treatment of simulation uncertainty.

## Overall assessment

The revision preserves the sound improvements in threat modeling, audit-blind confirmation, executable attribution, disclosure and the separation of repair into an extension. I found no further Blocking or Major issue beyond C7 and R13.1.

V19 resolves the earlier omission of the full interval. Its lower and upper calculations use matched random streams, the stratum-specific bound assignments are correct, and the reported maximum mean widths are taken across configurations and scenarios rather than averaged across them.

**C7 has no new evidence this round and is stalled as an evidence question.** It should go to the committee explicitly as unresolved. However, C7 is **not the only remaining Blocking or Major issue**: R13.1 is a methodological defect introduced by this revision and can still be addressed by the peers. Thus the round is not solely stalled on user-supplied human timings.

DISAGREE: [C7 human development evidence, R13.1 constructible population and estimator]