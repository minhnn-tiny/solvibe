The calibration **partly resolves the concern, but not completely**. Independent calibration and validation use separate random streams. The selected level and multiplier are implemented, and power is recomputed at the selected level. However, the offsetting scenarios are not exact nulls for the estimand used by the code.

In [power_sim_v6.py](/Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/tools/power_sim_v6.py), `null_scenarios` balances the stratum effects at a fixed reference share. `simulate` then draws a different frame share for each study and calculates `TRUE` from that share. Consequently, the offsetting configurations generally have a nonzero `TRUE`. Nevertheless, `fwer_and_cov` counts **any rejection** as a family-wise error.

For reference share \(\pi_0\), realized share \(\pi\), and avoided-vulnerability difference \(d\), the resulting difference is:

\[
\Delta=d\frac{\pi_0-\pi}{1-\pi_0},
\]

which is zero only when the shares coincide. The interval coverage calculation does use `TRUE`, so that calculation does not have the same labeling error.

**Remaining Major, C6:** the reported maximum of 0.051 mixes genuine null rejection with rejection under small nonzero effects. It cannot certify the requested offsetting-null calibration. The Monte Carlo interval containing 0.05 is not itself the problem.

**Required change:** Construct offsetting rates after drawing each frame so that the declared difference is exactly zero, assert that condition, and rerun calibration and independent validation while counting rejection only among true null configurations.

Hypothetical frames, direct simulation of \(K\), shared protocol effects, and transfer to the measured sampling design remain separate limitations. They should stay explicit even after this correction.

The following replacement reports the existing evidence accurately without presenting the unresolved calibration as complete.

===BEGIN 6.3 REPLACEMENT===

**Checked simulation evidence.** The calibration code is `tools/power_sim_v6.py`. Its results are recorded in `tools/power_results_v6_rq1_calibration.txt`. It uses the weighted estimator and delete-one-protocol jackknife described above, with a t reference distribution.

The simulation retains unequal hypothetical frames, paired human and agent outcomes, and variation in protocol effects, function effects, and dependence between configurations. It generates the endpoint \(K\) directly.

**Selected testing level and interval multiplier.** Calibration used 1,000 simulated studies per scenario across 48 scenarios. The selected nominal family level was \(\alpha^*=0.03\). This level is passed to Holm’s procedure for the configuration-specific t-test p-values. It is not a separate significance level for each configuration.

The selected interval multiplier was \(c^*=1.24\). Each pointwise interval has the form

\[
\widehat{\Delta}
\ \pm\
1.24\,q_t\,\widehat{\mathrm{SE}},
\]

where \(q_t\) is the usual critical value for a two-sided 95% interval from the declared t reference distribution. These intervals are not simultaneous intervals across configurations.

On the calibration draws, the maximum recorded family rejection rate at \(\alpha^*\) was 0.050. The minimum pointwise coverage at \(c^*\) was 0.951.

**Independent validation results.** Validation used a separate random stream and 1,000 studies per scenario.

| Quantity | Recorded result | Reported Monte Carlo interval |
|---|---:|---|
| Maximum family rejection rate across scenarios | 0.051 | 0.037 to 0.065 |
| Mean family rejection rate across scenarios | 0.028 | Not reported |
| Minimum pointwise coverage across scenarios and configurations | 0.956 | 0.943 to 0.969 |
| Mean of the scenario-specific minimum coverages | 0.973 | Not reported |

The Monte Carlo intervals describe simulation uncertainty. They are not simultaneous bounds over all scenarios.

**An offsetting-null check remains unresolved.** Some scenarios equate human and agent rates within both strata. Others make avoidance in V offset additions in N at a fixed reference stratum share. The simulated frame share varies between studies. In those offsetting scenarios, the code therefore records a true difference that is generally nonzero, but still counts every rejection as a family-wise error.

For this reason, the aggregate family rejection rates above cannot yet be interpreted as validated family-wise error rates for exact offsetting nulls. The interval calculations use each study’s recorded true difference and do not have this particular labeling problem.

The selected level and multiplier are provisional. Before confirmatory use, the offsetting rates must be constructed from each generated frame so that the declared null difference is exactly zero. Calibration and independent validation must then be repeated, with false rejections counted only for true null configurations. The measured frame and sampling design must also be checked before main data collection.

**Power at the selected level.** The simulation recomputed power at \(\alpha^*=0.03\), using 400 studies per scenario. The table reports ranges across scenarios of the minimum power among affected configurations. These are not confidence intervals.

| Protocols | Effect pattern | Mean true difference | Range of minimum configuration power |
|---|---|---|---|
| 25 | Larger effect; half the configurations null | +0.103 to +0.108 | 0.89 to 0.98 |
| 30 | Larger effect; half the configurations null | +0.103 to +0.108 | 0.97 to 0.99 |
| 25 | Middle effect; all configurations affected | +0.065 to +0.070 | 0.58 to 0.81 |
| 30 | Middle effect; all configurations affected | +0.065 to +0.070 | 0.73 to 0.91 |
| 25 | Smaller effect; all configurations affected | +0.036 to +0.042 | 0.14 to 0.40 |
| 30 | Smaller effect; all configurations affected | +0.037 to +0.042 | 0.21 to 0.51 |

Under these assumptions, the design has substantially greater power for the larger differences than for the smaller ones. It does not reliably detect differences in the smallest range. Power for the middle range remains sensitive to the scenario and protocol count.

These results describe the currently selected testing level. They must be recomputed if corrected calibration changes that level. A nonsignificant result will not establish equivalence, absence of a security difference, or safety.

===END 6.3 REPLACEMENT===

I rechecked the rest of v5 against C1–C8. I found **no additional Blocking or Major issue**. The matched evaluation, target attribution, all-attempt denominator, separate natural and injected analyses, supplementary sampling rule, resource accounting, and disclosure plan remain intact.

DISAGREE: [RQ1 offsetting-null calibration]