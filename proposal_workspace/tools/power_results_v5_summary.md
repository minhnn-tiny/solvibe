# Power simulation v5: summary of results

Script: `tools/power_sim_v5.py` (seed 20261022). Raw results: `tools/power_results_v5_rq1.txt` (first RQ1 run, basic and t tests), `tools/power_results_v5b_rq1.txt` (RQ1 rerun with the jackknife test and a smaller effect), `tools/power_results_v5_rq2.txt` (RQ2). Every number below comes from those files; each RQ1 row uses 400 simulated studies, so a rate near 0.05 has a Monte Carlo standard error of about 0.011, and a rate near 0.95 of about 0.011.

## RQ1

Design simulated: 25 or 30 protocols; per protocol a group V frame of 2 + Poisson(2) functions and a group N frame of 30 to 120 functions; up to 2 V (census if fewer) and 8 N functions sampled per protocol; inclusion weights; six configurations, three attempts each; human outcome one per function. Scenarios cross the human group V rate (1.0, 0.9), dependence (shared function effects 1.0 with human correlation 0.3; or 0.5 with 0.6) and effect sizes (protocol, function standard deviations of 0.5, 1.5 or 1.0, 2.0). Effect configurations have a_V = 0.6 and a_N = h_N + 0.13 ("effect", true Δ +0.103 to +0.108 because the frame share π is about 0.05) or a_N = h_N + 0.06 ("small effect", true Δ +0.036 to +0.042). Null configurations equal the human in both strata.

Three tests, each with Holm across the six configurations:

| Test | Scenario | Per-configuration power (range over scenarios) | Lowest per-configuration coverage of the 95% interval | Highest family-wise error |
|---|---|---|---|---|
| Basic bootstrap (Rao-Wu, P - 1 draws) | all null, 25 protocols | - | 0.89 | 0.09 |
| Bootstrap SE, t(P - 1) | all null, 25 | - | 0.90 | 0.07 |
| Jackknife (delete one protocol), t(P - 1) | all null, 25 | - | 0.91 | 0.07 |
| Jackknife, t(P - 1) | all null, 30 | - | 0.92 | 0.06 |
| Jackknife, t(P - 1) | half null, 25 | 0.93 to 0.98 | 0.91 | 0.07 |
| Jackknife, t(P - 1) | half null, 30 | 0.98 to 0.99 | 0.91 | 0.07 |
| Jackknife, t(P - 1) | all effect, 25 | 0.96 to 0.99 | 0.91 | - |
| Jackknife, t(P - 1) | small effect, 25 | 0.24 to 0.48 | 0.92 | - |
| Jackknife, t(P - 1) | small effect, 30 | 0.29 to 0.59 | 0.93 | - |

Reading:
- The jackknife with a t reference is the best calibrated of the three, but it is still slightly liberal: family-wise error up to 0.07 and coverage down to 0.91, against 0.05 and 0.95.
- With 25 to 30 protocols the design detects a difference of about +0.10 per configuration with power above 0.93, and does not reliably detect +0.04 (power 0.24 to 0.59).
- Remaining simplifications: the endpoint K is simulated directly (no separate compilation and functional outcomes), configurations share protocol effects, and frame sizes are invented.

## RQ2

Declared model fitted: logistic with nested random intercepts for protocol and function, nested Gauss-Hermite quadrature (12 x 12); likelihood-ratio test against chi-square(1); writing and repair share their protocol and function effects; Holm over the two; convergence checked (bounded L-BFGS-B success, free-coordinate gradients below 1e-3, one restart; failed fits stay as non-rejections). 300 simulated studies per row.

| Functions | Protocols | Interactions (writing, repair) | Rejection, writing | Rejection, repair | Family-wise error | Failed fits |
|---|---|---|---|---|---|---|
| 40 | 20 | (0, 0) | 0.02 | 0.02 | 0.04 | 1/600 |
| 40 | 20 | (0, 1.5) | 0.02 | 0.86 | 0.02 | 3/600 |
| 40 | 20 | (1.0, 1.0) | 0.51 | 0.55 | - | 5/600 |
| 40 | 20 | (1.5, 1.5) | 0.90 | 0.91 | - | 2/600 |
| 40 | 20 | (2.0, 1.0) | 0.99 | 0.59 | - | 2/600 |
| 20 | 10 | (0, 0) | 0.04 | 0.04 | 0.08 | 0/600 |
| 20 | 10 | (1.5, 1.5) | 0.58 | 0.59 | - | 1/600 |
| 10 | 5 | (0, 0) | 0.03 | 0.03 | 0.07 | 0/600 |
| 10 | 5 | (1.5, 1.5) | 0.32 | 0.32 | - | 0/600 |

Reading:
- At the declared allocation (40 functions, 20 protocols) the test holds its level (family-wise error 0.04 under the full null) and has power about 0.90 for interactions of 1.5 on the logit scale; interactions of 1.0 have power about 0.5.
- With 10 or 20 functions the family-wise error rises to 0.07 to 0.08 and power is low, which supports treating a small natural stratum as a case series.
- The parametric bootstrap of the likelihood-ratio test was not simulated (too slow); the chi-square reference is what the simulation validates.
- Interaction sizes are scenarios. The pilot's 10 of 12 against 2 of 12 contrast is an execution-access contrast on one task, not an estimate of the interaction.
