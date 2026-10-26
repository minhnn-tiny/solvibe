## Checks and point status

**R30.1: resolved at proposal stage.** The revision quantifies the additional mapping load and makes affordability a condition of proceeding. It uses the actual member-audit count after the draw, requires a named source for any transfer, and prohibits dropping audits to fit the budget. This is a conditional resource plan, not evidence that mapping will fit.

**R30.2: resolved.** Section 8 now states that about 5.6 sampled units contain several audits and that the single-audit development cases do not test their preparation. The nine-hour allowance remains an unverified cap rather than a measured estimate.

The calculation in `mapping_load_v46.py` matches the sampling design:

- It excludes development units and retains 152 units containing 180 audits.
- Of these units, 23 contain several audits.
- It uses capped inclusion probabilities proportional to the recorded size measure and the existing randomized systematic sampler.
- The expected counts are calculated directly from inclusion probabilities, rather than estimated from simulation.

My independent arithmetic gives 29.426 expected member audits and 5.573 expected multi-audit units, matching 29.4 and 5.6.

The saved 20,000-draw results report median 29, 95th percentile 33 and observed maximum 39. The code calculates those statistics as described. I did not rerun the Monte Carlo draws.

The revised budget arithmetic also checks:

| Claim | Check |
|---|---|
| Median total including development | \(29+3=32\) audits |
| 95th-percentile total including development | \(33+3=36\) audits |
| Mapping at two hours per audit | \(36\times2=72\) hours |
| Mapping at four hours per audit | \(36\times4=144\) hours |
| Spot checks | \(19\times0.5=9.5\) hours |
| Conservative common-time threshold | \((112-9.5)/36=2.8472\) hours; “about 2.8” is reasonable |
| Shortfall at four hours throughout | \(144+9.5-112=41.5\) hours; “about 42” is correct |

The rebuttal matches these figures. Its affordability statement should retain the qualification that the actual sampled audit count and recorded development expenditure govern the final calculation.

## Remaining issues

### R31.1 [Minor] [C4, C7] The preparation ceiling and transfer rule conflict

**Section:** 8, “Preparation budget”; Appendix B; rebuttal resource ledger.

Step 5 permits preparation to use other support hours, but the following sentence says preparation “retains its 112-hour ceiling.” Both cannot describe an enlarged preparation allocation. The proposal also needs to distinguish the former 100-hour mapping allowance from the combined preparation limit.

**Required change:** State that 112 hours is the initial preparation allocation, replacing the separate 100-hour mapping restriction, and that a documented transfer may raise that allocation while preserving the total 220-hour support ceiling and all other funded obligations.

### R31.2 [Minor] [C4, C7] An unfinished mapping is a censored time

**Section:** 8, six-step mapping rule, step 2.

“An unfinished mapping counts at 4 hours” is acceptable as a record of consumed allowance. It is not an estimate of the time needed to finish. Likewise, capping a measured time at four hours could conceal a recorded overrun.

The existing development requirements already prevent launch when required work cannot be completed validly within its cap. This makes the problem a clarification rather than a new Major issue.

**Required change:** Rewrite step 2 to use the largest completed, within-cap development mapping time for planning, while stating that an unfinished mapping or overrun fails the development requirement and cannot become evidence of four-hour completion through truncation.

### R31.3 [Minor] [C4] “32 to 36 audits” needs percentile labels

**Section:** 8; Appendix B; rebuttal resource ledger.

The phrase can read as a workload range. It is actually the median-to-95th-percentile interval after adding development. The saved simulation includes 39 main member audits in one draw, and the observed maximum is itself not a theoretical bound.

The six-step rule correctly substitutes the actual count after selection, so this wording does not undermine the design.

**Required change:** Replace “mapping covers about 32 to 36 audits” with “mapping covers 32 audits at the simulated median and 36 at the simulated 95th percentile, including development; the actual draw determines the required count.”

No remaining Blocking or Major issue is established by these changes. This vote does not certify the unmeasured mapping speed or multi-snapshot preparation capacity. The timed case and the other stated pre-collection checks remain pending.

AGREE: no Blocking/Major issues remain