# Rebuttal to the iteration-3 meta-review

Authors: Peer A (Claude Code) and Peer B (Codex). Peer A drafted this rebuttal and `proposal_v16.md`; Peer B's corrections from Loop 1 are applied before the committee sees it. It answers every required change in `iter_3/meta_review.md`.

**What changed most.** The committee asked us to count the frame and to make the budget fit; we did both, and the results changed the principal question. Under the measured frame, no allocation that fits a first-year budget gives the design comparison (RQ1a) the precision we had promised. Following the iteration-2 instruction for that case, RQ1a is now a secondary estimate, and RQ1b, the agent-minus-developer comparison over the population, is principal. RQ1b is IDEA.md's own question, so the core problem has not changed.

**Stagnation rule.** Items 1, 2 and 10 repeat earlier items. The fixes are structurally different: a cost model with one common construction allowance and a preregistered allocation table with a selection rule (item 1); a frame-wide count from 19,627 findings instead of simulated distributions (item 2); and, for item 10, the student's commitment and a kit for the timed case, instead of another schedule.

**New evidence** (hashes in `tools/MANIFEST.md`): `evidence/frame_inventory/` (frame count), `evidence/rediscovery/` (audit-blind rediscovery), `tools/power_sim_v21.py` to `v23.py` with results, and `dev_case/` (the student's development-case kit).

## Responses

| # | Label | Decision | What changed | Where in `proposal_v16.md` |
|---|---|---|---|---|
| 1 | Blocking | Done | Cost model with one common construction allowance (labels are sealed), five campaigns per function, and audit-informed work for half of the V functions. A table of five allocations gives hours per protocol at low, middle and high rates, the protocols that fit 900 hours, RQ1b precision and the smallest RQ1a distortion each detects. The chosen row, 20 protocols × (2 V, 6 N), costs 27.0 / 43.9 / 62.8 hours and fits exactly at the middle rates. The selection rule uses the upper 80% limits of the measured unit costs and allows fewer protocols, down to 12, only if a rerun still meets the RQ1b target. At the high rates no row fits its listed size; the proposal says so. | 5.2, 8 |
| 2 | Blocking | Done in part | `evidence/frame_inventory/`: 2,481 audits, 19,627 High/Medium findings. For 2025+ audits with Solidity code, the estimated V count per protocol (from High/Medium counts, 0.729 functions per finding, half kept by the single-function rule) has mean 2.15 under the cap and 22.9% zeros; for 42 recent fully mapped audits, mean 3.19. V21 and V22 rerun every allocation on these lists. Not done: a fix-scope classification of every finding in 20 to 30 randomly drawn protocols, which needs fix commits not available locally; month one does it for the sampled protocols. Construction that depends on difficulty is still not simulated. | 5.1, 6.3, 6.4, 8 |
| 3 | Blocking | Done | Every comparison is reported in two parts per stratum: the security part (vulnerability among implementations that compile and pass) and the functional-failure part. Claims and precision statements concern the security part. `power_sim_v8.py` computes the security part; in the target scenario it is about −0.23 where D gives −0.33. For RQ1b on the security part the chosen allocation detects +0.13 to +0.15 with probability 0.84 to 0.98, and +0.06 to +0.08 with 0.38 to 0.78. | 3, 6.2, 6.3 |
| 4 | Major | Done | Rule preregistered: when a correction removes a confirmed violation but fails a frozen check, the two adjudicators, blind to author, decide whether the check asserts the attacker outcome; if so it is dropped for every implementation, L is recomputed for both authors, and cases are counted by stratum. | 5.5 |
| 5 | Major | Done | "Little difference" is removed. RQ1a is read as "large distortion" or "inconclusive". The smallest distortion detected with probability about 0.8 is stated for each allocation (about 0.6 for the chosen one). | 3, 6.4, 8 |
| 6 | Major | Done | RQ1b is principal, with a calibrated interval (multiplier 1.2) and Holm level (0.04; validation family-wise error 0.053). Precision target: +0.10 in the security part. The chosen allocation detects about +0.13 or more with probability at least 0.84 in every scenario; +0.05 is not detectable within this budget, and the proposal says so. | 6.3 |
| 7 | Major | Done | Retained scenarios by rule: measured V distribution; construction yield at the lower 80% limit of development yields with a floor of 0.7; unresolved shares at the upper 80% limit with a floor of 0.005 (about 120 development evaluations; with none unresolved the limit is about 0.013); one Holm level and one multiplier across all retained scenarios; a minimum construction yield of 0.7 per stratum below which results are descriptive. | 5.2, 6.3 |
| 8 | Major | Done | The recall-gap sensitivity analysis covers RQ1a and RQ1b with separate agent and historical recall in each stratum; the example table shows the detected V difference moving from −0.33 to −0.10 or −0.50 with recall alone. | 6.5 |
| 9 | Major | Done | `evidence/rediscovery/`: 17 single-function pilot findings, audit-blind bundles, a fresh Claude and a fresh Codex reviewer each, a blind judge. Candidate-level matches: Claude 17 of 17 (95% interval 0.82 to 1.00), Codex 13 of 17 (0.53 to 0.90); excluding three weak keys, 14 of 14 and 13 of 14. These are upper bounds, and the models may have seen these late-2025 audits in training. The eight built pilot tasks leave the gate reserve because they shaped the pilot's prompts. | 5.9 |
| 10 | Major | Committed; timing pending | The student committed on 22 October 2026 to the development cases and to time at least one case personally. `dev_case/` holds the protocol (steps S1 to S10), the commitment form for dates and roles, the exposure record, the timesheet and the sealing script. The dated commitment and the timed case are required before resubmission; they are not yet in. | 8 |
| 11 | Minor | Done | Whether the confirmation limit cut each candidate list is recorded and reported by author and stratum, with a secondary bound treating cut lists as unresolved. Limit: three confirmations per implementation. | 5.7, Appendix B |
| 12 | Minor | Done | The recall flag also covers reproduction of the historical body in both strata (normalized token similarity of at least 0.9, set from development), with RQ1b and RQ1a reported with flagged cases removed. | 6.8, Appendix B |
| 13 | Minor | Done | Generation and the primary campaign also run on the second request for the 15 duplicated functions, as a secondary analysis, charged to the coordination reserve. | 5.4 |
| 14 | Minor | Done | Sections 6.3 and 6.4 now hold only the evidence for the current plan; the simulation history is in Appendix A. | 6.3, 6.4, Appendix A |
| 15 | Minor | Done | All 13 factual questions are answered in Appendix B. | Appendix B |

## Disagreements among reviewers

1. C1: the principal question is now the author comparison; the novelty claim rests on the combination in section 3, not on the sign of the design difference.
2. C4: addressed by items 3 and 4.
3. C7: item 1 makes the plan consistent with its own numbers at middle rates; only the timed case can move it further.
4. Budget fix: one common allowance, as R3 asked.
5. "Little difference": removed.
6. Principal estimand: RQ1b, with RQ1a secondary, because the measured frame makes RQ1a imprecise; this follows the iteration-2 rule for that case.
7. Unresolved outcomes: the bounds stay in the principal analysis; the 80% rule with a floor sets the retained shares.
8. Frame evidence: frame-wide count done; finite-population simulation with difficulty-dependent construction remains for month two.
9. OQ1: the student has committed; the first timed case will be submitted with the next version.
