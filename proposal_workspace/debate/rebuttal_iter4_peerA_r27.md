# Rebuttal to the iteration-4 meta-review

Authors: Peer A and Peer B. Revised by Peer B in Loop 1 round 26.

This response refers to proposal version 28.

## What this revision does not supply

The student’s signed, dated commitment and first complete timed development case remain unsupplied. The recorded commitment form is blank and the timesheet contains only its header.

The committee requires both before acceptance. We agree. Scheduling the work does not replace the evidence.

One additional issue remains open: validation of the exact reserve-exhaustion procedure and the observable package warning. V42 validates a related missing-outcome model, but it does not simulate finite reserves or multiple candidate packages. We do not present it as doing so.

## Responses to the required changes

| Item | Status | Response | Sections |
|---|---|---|---|
| 1. Limits per candidate and package | Revised; reserve procedure simulated (V43) | Confirmation receives 1.0 student hour per candidate and each adjudicator receives 0.5 hours per package. The unsupported candidate-subsampling weights are removed. Complete implementation bundles are processed in a recorded random order within fixed source reserves. Required work left unfinished remains unresolved under adverse bounds. Whole-package review reservations total 205 hours per adjudicator. The main student ceiling is 921 hours for about 920.2 hours of planned work. V43 simulates the exact reserve procedure; power holds unless positive bundles have three candidates that each use the full hour, so launch depends on measured demand. | 5.7, 6.2, 6.3, 8 |
| 2. Commitment and timed case | Not supplied | The missing evidence is stated plainly. The timed case must use probability-selected functions, valid roles and the proposed caps. It must exercise confirmation and both adjudications. A separately budgeted seed can supply a candidate if none arises naturally. Human and machine time remain separate. | 8 |
| 3. Reading of a null result | Revised | The margin is +0.05, a stated material excess rather than a safety threshold. Holm 0.01 adjusts the two margin claims. V42 checks every retained condition with a configuration at or above the margin, including both ordered partial-margin conditions. Its largest reading-error upper bound is 0.0320. At the exact null, the lowest marginal configuration claim frequency ranges from 0.086 to 0.103 across frame groups; median-frame values range from 0.218 to 0.234. Most null studies remain inconclusive. The study does not claim that agents are safer. | 3, 6.3 |
| 4. Working status linked to difficulty | Revised | V42 uses the same final estimator in the linked-working group and the other groups. Agent working probability falls with a difficulty score linked to vulnerability. Historical bodies can fail ordinary checks. Targets are recomputed conditional on working. The linked-working group’s worst error upper bound is 0.0414 and coverage lower bound is 0.9503. | 6.3 |
| 5. Comparison on the same functions | Revised | The secondary comparison retains functions where the historical body works and at least one attempt of the configuration works. Each function has equal population weight through the sampling weights. Retained counts are reported by stratum and configuration. Unknown membership and outcomes retain bounds. Its interval is not presented as validated. | 6.1–6.3 |
| 6. Unresolved outcomes linked to packages | Revised; warning evaluated with the observable denominator (V43) | V42 adds package-dependent unresolved outcomes and evaluates a package warning. The tested package-model region is (0.05, 0.05, 0.2). Its denominator is detected-positive implementations, which is a simplifying proxy. The operational warning instead uses all registered candidate records within the three-candidate limit, including rejected and unfinished records. V43 evaluates it with the observable denominator under finite reserves: it fires in at most 6.1% of development samples and is unassessable in 1.4% to 28%; an unassessable result does not stop launch. An author with no candidate record makes development unassessable and prevents launch. | 5.7, 6.3, 8 |
| 7. Frame size and certainty protocols | Revised | The inventory contains 313 relevant firm-year records with a Solidity signal, including private reviews. About 230 usable protocols is an assumption, not a completed census. V39’s small-frame failures used older estimator rules and do not establish a universal minimum size. V42 uses frames of 230 with the final estimator. Every sampled protocol enters the jackknife, including certainty protocols, but no general conservativeness claim is made. Automated size proxies and exact mapping of sampled protocols have a separate capped preparation plan. | 5.1, 5.2, 6.3, 8 |
| 8. Cut candidate lists | Revised | Separate cells by author and stratum investigate candidates beyond the limit and work left unfinished by reserves. Extended independent assessments and recorded probabilities support a weighted sensitivity estimate within 48 first assessments and 120 auditor hours. | 5.9 |
| 9. V construction | Revised | Development returns to review if V functions were sampled but none was built. Yields and construction times are reported separately. V42 validates the final empty-stratum and empty-author-denominator rules in its low-V group. Its worst coverage lower bound is 0.9586 and undefined share is zero. | 6.2, 6.3, 8 |
| 10. Confirmed gate rediscoveries | Revised | A gate success requires execution and both adjudications within the main per-candidate and per-package allowances. The first assessment and permitted revision reserve 16 target packages, 18.4 student hours for their operation and confirmation, and 8.0 hours per adjudicator. Candidate lists are locked before matching to the known target. | 5.9, 8 |
| 11. RQ1a and the V share | Revised | The flagged-only result is descriptive, with counts and identification bounds. V accounts for 1.5% to 2.9% of the strict eligible frame, so the principal comparison is mostly about unflagged functions. No validated RQ1a confidence interval is claimed. | 3, 6.1, 6.4 |
| 12. Related work | Revised | Mahmud et al. and SolBehave remain included. The comparison distinguishes competitive-programming tasks and plain LLMs from agents in audited repositories, and behavioral equivalence from attacker violations. | 7 |
| 13. Factual answers | Revised, with costs still conditional | Appendix B reports severity exclusions, confirmation assistance, recall flags, empty-stratum rules, the package diagnostic and funding requirements. The strict body-only rule retains 50 of 119 High and 81 of 233 Medium findings; among determined scopes, 50 of 91 and 81 of 163. Human timing and current compute prices remain unsupplied. | 8, Appendix B |

## Interpretation of the new evidence

V42 uses one estimator across all three frame groups and five unresolved-outcome mechanisms. It retains the empty-stratum rule, bounds an undefined author-stratum conditional rate by 0 and 1, and deletes every sampled protocol in the jackknife.

Its reported worst directional-error upper bound is 0.0426. Its lowest coverage bound is 0.9503. Its worst reading-error upper bound is 0.0320.

The retained implementation-rate region is the tested downward-closed set with maximal vectors:

- (0.0075, 0.0075, 0.0075);
- (0.013, 0.013, 0.005).

The separate package-model region is (0.05, 0.05, 0.2). Continuous extension is a planning assumption. These are not a validated joint region for simultaneous causes.

The smaller symmetric implementation region avoids relying on configuration-specific boundary fluctuations between runs. V42 is the current common-estimator evidence. V40 and V41 supply corroborating earlier results, not a second complete validation of the identical procedure.

Without unresolved outcomes, V42’s lowest power at +0.10 ranges from 0.406 to 0.415. At +0.05 it ranges from 0.104 to 0.115. Mean half-widths range from 0.046 to 0.091 at the null and from 0.088 to 0.115 at +0.15.

The package warning is weak in development. In V42’s proxy model, development is unassessable in 0.331, 0.347 and 0.634 of samples across its three groups. These are pooled results, not worst-frame guarantees.

## Decisions that differ from Peer A’s preliminary suggestions

**Reserve exhaustion is not equated with V42’s package mechanism.** V42 independently masks detected-positive implementations. A shared reserve with multiple candidates can create different dependence and can leave rejected or unfinished candidate packages. The proposal keeps the suggested random ordering and adverse bounds, but requests direct validation.

**The package warning uses observable records.** Its denominator includes registered candidate records, not a latent count of implementations that would eventually have confirmed flaws. V42’s diagnostic therefore remains supporting proxy evidence. The practical warning must be checked in the reserve simulation.

**Size measures are distinguished from exact eligibility.** Automated counts supply positive first-stage size measures. Exact V and N mapping occurs in sampled protocols before function sampling. Recorded probabilities protect the design only if frame coverage and positive selection probabilities are preserved.

## Resource reconciliation

The revised adjudicator ledger is:

| Source | Hours per adjudicator |
|---|---:|
| Main | 89.0 |
| Development | 12.5 |
| Development audit-assisted work | 1.5 |
| Gate and permitted revision | 8.0 |
| Duplicate requests | 9.0 |
| Seeded artifacts | 60.0 |
| Controls | 14.0 |
| Main audit-assisted work | 11.0 |
| Total | 205.0 |

The main student work remains about 920.2 hours, within a 921-hour ceiling. Main work, seeded operation and duplicate requests total about 1,137.9 hours. Approximately 88 hours therefore extend into month 10.

Gate operation and confirmation add 18.4 student hours in months 1 and 2. They do not silently consume the main-study reserve.

Frame preparation uses automated enumeration, a random human spot check and full mapping of the 25 sampled protocols. The preparation ceiling is 112 paid hours within the shared 220-hour support ceiling. The remaining named work must fit a pre-development ledger.

These are planning reservations. Funding, staffing and the student’s timed case remain necessary.

## Final validation and current status

The final-frame check now has one explicit matrix. It covers all four implementation mechanisms on 76 vectors, the package mechanism on 64 vectors, all ten conditions for coverage, all applicable margin-null conditions, and the exact reserve procedure.

Outside-region error and coverage remain mandatory. The +0.15 power requirement applies only inside the retained operating scenarios. Replacement calibration and fresh validation use the same scope and recomputed multiplicity counts.

This revision still cannot be accepted as complete evidence: the student commitment and timed case remain missing. V43 now simulates the reserve stopping rule. Power holds inside the region unless every positive implementation has three candidates that each use the full hour; in that case the reserve runs out in 44% of studies at +0.15 and power falls to 0.25 to 0.34. Launch therefore depends on rerunning V43 with the candidate demand measured in development. An unassessable development warning is recorded but does not stop launch; a firing warning does.
