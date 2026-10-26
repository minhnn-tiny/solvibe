# Rebuttal to the iteration-4 meta-review

Authors: Peer A and Peer B. Draft by Peer A in Loop 1 round 25; Peer B's check is pending.

This response refers to proposal version 26.

## What this version does not supply

Item 2, the signed and dated commitment and one timed development case, is still missing. On 2026-10-23 the commitment form (`dev_case/commitment.md`) is blank and the timesheet (`dev_case/timesheet.csv`) has only its header. The area chair said that without them the proposal cannot be accepted. We agree, and we do not offer a schedule in their place. Section 8 now states exactly what the case must contain.

## Responses to the required changes

| Item | Status | Response | Sections |
|---|---|---|---|
| 1. Limits per candidate and per package (Blocking) | Revised | Confirmation is 1.0 student hour per candidate and review 0.5 hours per package for each adjudicator, the same for every author. Each source's reserve is sized for the high candidate rate of 3/13. If a reserve would run out, the remaining candidates or packages are subsampled at random, and the probabilities enter the weights. The main study needs about 920 student hours; the 88 hours beyond months 3 to 9 (including seeded validation at 183.7 hours and duplicate requests at 34) come from month 10, and we keep 22 protocols. Each adjudicator needs about 194.5 hours, by source in a table, so the ceiling is raised from 121 to 195 hours. | 5.7, 6.2, 8 |
| 2. Commitment and timed case (Blocking) | Not supplied | See above. Section 8 lists what the case must record: time per candidate and per package, the outcome of each confirmation, measured resources against the reservations, at least one candidate through confirmation and both adjudications, with a seeded flaw inserted by another person if no natural candidate arises. | 8 |
| 3. Reading of a null result | Revised | A margin of +0.05 is fixed on substance before looking at simulated widths: it roughly doubles the middle of the planning historical rate. A one-sided test against it, Holm 0.01, has error upper bound at most 0.0323 on fresh draws (V40, V41). It rules out +0.05 in only 0.085 to 0.104 of null studies in the worst frame (0.21 to 0.23 at the median), so a null study will usually report only the upper end of its interval. Section 6.3 reports the ratio of agent to historical detected rates at +0.15 (2.9 to 7.8), the mean half-width (0.046 to 0.091 at the null), and power at +0.05 (0.10 to 0.11) and +0.10 (0.40 to 0.42) in the worst frame. Section 3 states that the study cannot show agents are safer. | 3, 6.3 |
| 4. Working status linked to difficulty | Revised | V39 to V41 add a setting in which agent attempts work less often on functions more likely to be vulnerable and historical bodies can fail ordinary checks. Exact targets are conditional on working. On frames of 230 protocols error (0.0411) and coverage (0.9555) pass and power holds inside the frozen region. The setting is added to the final-frame check. | 6.3 |
| 5. Comparison on the same functions | Revised | A pre-specified secondary estimate restricted to functions where the historical body works and at least one attempt of the configuration works, with equal weight per function and the size of that set reported. It has no power requirement and is not validated by simulation. | 6.1, 6.3 |
| 6. Unresolved outcomes linked to packages | Revised | A fifth mechanism makes only implementations with a package unresolvable, at rates per package by author. Power at +0.15 holds when each configuration's rate is at most 0.05 per package and historical at most 0.2; at 0.1 for every author it fails (0.557 to 0.594). The region is restated in both units. The diagnostic stays in implementation units, and unresolved counts are also reported per package. | 6.3, Appendix B |
| 7. Frame size and certainty protocols | Revised | The frame is fixed to 2024 and 2025 contest audits: 313 in the inventory, about 237 usable, about 230 expected. On frames of 50 and 70 the design fails the power requirement (V39); on frames of 230 it passes (V40, V41). Certainty protocols are deleted in the jackknife like other protocols. The area chair's suggested rule, never deleting them, gave error of 0.25 to 0.28 in V39 because it ignores sampling of functions inside them. The frozen region is re-derived from V40 and V41 and is slightly smaller than before. | 5.1, 6.3 |
| 8. Cut candidate lists | Revised | Six new natural-investigation cells, one per author and stratum, sample campaigns whose list was cut, with extended confirmation and a weighted estimate of the change in the principal contrast, within 48 first assessments and 120 auditor hours. | 5.9 |
| 9. V construction | Revised | Development step 7 adds: if V functions were sampled and none was built, return to review. V and N yields are reported separately. V41 shows that a low V yield (0.3) made 7% of estimates undefined; rates with no working implementation are now bounded by 0 and 1, and coverage passes. | 6.2, 6.3, 8 |
| 10. Confirmed gate rediscoveries | Revised | A gate rediscovery counts only if confirmed by execution and both adjudications within the main caps. | 5.9 |
| 11. RQ1a and the V share | Revised | The flagged-only comparison is a descriptive table, not a research question. Section 3 states that V is 1.5% to 2.9% of eligible functions, so RQ1b is mostly a comparison on unflagged functions. | 3, 6.1, 6.4 |
| 12. Related work | Revised | Mahmud et al. (The Illusion of Safety) and SolBehave are added to section 7 and its table, with the differences R4 gives. | 7 |
| 13. Factual answers | Revised | Appendix B answers each question, including the one-body rule by severity (it keeps 55% of High and 50% of Medium findings whose fix scope could be determined), LLM help in confirmation, compute funding, the protocol-effect setting of 0.9 and the recall flag on reviewer lists. | Appendix B |

## Disagreements and choices

- **Certainty protocols.** We did not adopt the rule the area chair suggested, because V39 shows it is anti-conservative. The rule we use errs toward wider intervals.
- **Twenty extra hours.** We kept 22 protocols, as the area chair advised. The schedule now ends main collection 88 hours into month 10, leaving 62 hours of month 10 for analysis.
- **The margin.** +0.05 is our judgement of the smallest excess that matters. The design rarely rules it out at a true null. The committee should judge whether the remaining contribution is enough.

## Current status

The design changes in this version need no student input. The proposal still cannot be accepted until the student supplies the commitment and the timed case.
