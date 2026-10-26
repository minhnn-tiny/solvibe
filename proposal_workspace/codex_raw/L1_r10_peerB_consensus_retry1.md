## Rebuttal check

All 24 required changes and all seven disagreements have entries. The following corrections are needed to represent the amendments and v11 accurately. Unless stated otherwise, replacement text applies to the row’s “What changed” cell.

1. **Row: Opening evidence paragraph.**  
   **Problem:** “All numbers below” do not come from simulations. Some are pilot observations, allocation choices, or assumed budgets.  
   **Exact replacement text:**

   > **Evidence produced since iteration 1.** Simulation results below come from the saved code and outputs under `proposal_workspace/tools/`. Pilot observations come from the repository’s pilot reports. Allocations and person-hour budgets are planning choices and assumptions, not measured study results. Development measurements must replace the cost assumptions before main collection.

2. **Row: “Stagnation rule,” equal-search bullet.**  
   **Problem:** “Detection limits are measured” implies completed validation and overstates what seeded flaws establish.  
   **Exact replacement text:**

   > Equal search. The earlier fix matched discovery budgets and replayed PoVs across authors. The new fix changes the primary label: an implementation counts as vulnerable only if its own audit-blind campaign finds a flaw that is then confirmed. Pooled replay and audit-derived attacks become secondary views. Planned validation includes matched seeded flaws, natural audit rediscovery, and independent investigation. These provide separate evidence about detection limits; they do not establish equal recall for natural flaws.

3. **Row: 1.**  
   **Problem:** The second person’s 60–120 hours exclude additional prior-exposure cases. The development commitment also omits the required probability-selected N functions.  
   **Exact replacement text for the final two sentences:**

   > Paid work is listed separately: two adjudicators at 66 to 121 hours each, about 100 auditor hours, and 60 to 120 hours for the second person before additional prior-exposure cases. Those additional cases require a separate allocation. Month one schedules at least three development cases with people performing every designated human-review step. One case includes a probability-selected set of N functions. These measurements remain outstanding. Month two replaces the assumptions and reconciles student hours, paid work, and compute. If no useful allocation fits, main collection does not start.

4. **Row: 2.**  
   **Problem:** V11 reports four views, not three. The seeded precision range is an analytic planning approximation with specific assumptions, not demonstrated precision. The amendment’s restriction to seeded-pattern sensitivity is missing from the substantive response.  
   **Exact replacement text:**

   > Each implementation receives its own campaign, with no audit-derived properties, references, prompts, attacks, or confirmation inputs. Primary records are locked before secondary replay. Four views are reported: own-campaign discoveries, pooled common-procedure discoveries, own-campaign discoveries supplemented by audit attacks, and the union after both forms of replay. An unexposed builder freezes blind artifacts before receiving audit or mapping-review information. The core funds 60 matched seeded pairs. Their approximate pooled 95% half-width is 0.135 to 0.194 under the recorded assumptions: recall difference 0.1, discordance 0.2 to 0.4, and design effect 1.5. This is an analytic approximation, not measured precision or a guarantee for each stratum and configuration. The core cannot certify equal recall within 0.05. Seeded results describe sensitivity to those patterns, not natural-flaw recall. Natural audit rediscovery and independent investigation are reported separately. Section 6.5 gives sensitivity contours and the single-stratum sign-reversal boundary, s_A/s_H = r_A/r_H, for positive detected rates. No numerical reversal threshold is claimed before observing those rates. The development campaign must rediscover at least half of qualifying development vulnerabilities; this is a launch criterion, not proof of comparable sensitivity.

5. **Row: 5.**  
   **Problem:** The response attributes the interpretation rule only to K. V11 applies it to both D and K.  
   **Exact replacement text:**

   > One endpoint is primary: D, which requires compilation, ordinary functional success, and a vulnerability confirmed through the implementation’s own campaign. K is secondary. A lower D or K is not described as better security when working completion falls. That interpretation also requires evidence that the rate of working outputs without a confirmed flaw does not fall. Ordinary functional checks and explicit security checks are classified before generation. An ordinary functional check is not removed merely because it also detects a flaw.

6. **Row: 6.**  
   **Problem:** The response omits Monte Carlo uncertainty, combines power ranges across allocations, and drops the amendment about changing latent vulnerability rates. It also understates the remaining validation requirements.  
   **Exact replacement text:**

   > The simulation includes compilation, functional success, detection by author and stratum, and protocol-by-author variation. At 15 protocols, calibration selects Holm level 0.04, interval multiplier 1.12, and equivalence multiplier 1.34. Independent validation gives worst family-wise error 0.042 ± 0.016, minimum coverage 0.948 ± 0.018, and worst family false equivalence 0.058 ± 0.019. Equivalence uses margins of ±0.05 for detected D. Boundary studies generate true boundary differences and count a false equivalence declaration by either configuration. These checks support the tested settings, not universal error control. For differences of +0.069 to +0.090, minimum configuration-specific power ranges from 0.55 to 0.93 at 15 protocols and 0.70 to 0.98 at 20. For smaller differences of +0.022 to +0.042, the ranges are 0.13 to 0.38 and 0.13 to 0.59, respectively. Neither allocation guarantees 0.80 power across the retained larger-effect scenarios. At a true zero difference, worst-scenario minimum configuration-specific equivalence power is 0.12 at 15 protocols. This is not the probability that both configurations establish equivalence. No minimum detectable difference is claimed. Current recall scenarios change underlying vulnerability rates; they do not hold latent code quality fixed. Before collection, validation must use the actual sampling design and development evidence, include unresolved outcomes and mixed boundary configurations, and vary recall while holding latent quality fixed.

7. **Row: 7.**  
   **Problem:** “About 0.40 or larger” extrapolates beyond the simulated range. The response omits the pointwise, configuration-specific interpretation established in R9.5 and the required agent-ranking comparison.  
   **Exact replacement text:**

   > The V-only and weighted estimates are reported on the same data, with jointly computed uncertainty for their difference. Agent ordering is also reported with uncertainty. With 15 protocols and two V functions per protocol, the interval multiplier is 1.16. The minimum configuration-specific rates of excluding zero are 0.89 to 0.99 for simulated design differences of about 0.40 to 0.57 in magnitude, 0.74 at about 0.33, and 0.11 to 0.48 across the displayed scenarios of about 0.10 to 0.26. These are pointwise results without correction across configurations. They are not probabilities of joint success or ranking reversal. Month two considers up to four V functions only under the stated effect-range rule and a complete incremental budget. Unknown costs must be measured, and protected remaining work must still fit.

8. **Row: 9; disagreement 6.**  
   **Problem:** “Counted in month one” conflicts with v11’s month-one screening and later task construction. The final prevalence estimate requires semantic confirmation.  
   **Exact replacement text for row 9:**

   > Month one screens natural tests and measures construction costs. The descriptive study reports the share of V functions with semantically confirmed natural fault-enforcing tests. A full census is attempted only if measured costs permit. Otherwise the estimate uses probability-sampled V functions, sampling weights, protocol-aware uncertainty, and bounds for unresolved cases. Passing on vulnerable code and failing on a correction is only a screening signal.

   **Exact replacement text for disagreement 6:**

   > Natural fault-enforcing tests: begin screening in month one. Use a census only if measured costs permit; otherwise estimate prevalence from sampled V functions with semantic confirmation, weighted uncertainty, and unresolved-case bounds (item 9).

9. **Row: 12.**  
   **Problem:** The response does not answer the AC’s central keep-and-score versus unresolved question.  
   **Exact replacement text:**

   > Every request sentence records its source, and requests are frozen before evaluated runs. A separate diagnostic classifies each request as favoring vulnerable behavior, neutral, or favoring corrected behavior. Requests favoring vulnerable behavior are retained and scored when the acceptance specification remains coherent. Tasks lacking a coherent specification remain unresolved rather than being silently removed. Results are stratified by request classification.

10. **Row: 13.**  
    **Problem:** The zero rule lacks its exception. The response also omits admissible bounds and the requirement to survive inferential uncertainty, rather than merely retain a point-estimate sign.  
    **Exact replacement text:**

    > An unresolved attempt contributes zero to the descriptive confirmed-count statistic unless its endpoint is already established as one. This means “not confirmed,” not “safe.” Admissible bounds respect known compilation and functional outcomes. The lower difference bound assigns agent unknowns low and historical developer unknowns high; the upper bound reverses those assignments. A directional claim must survive uncertainty at its adverse bound under the final calibrated design.

11. **Row: 14.**  
    **Problem:** “Security-specific interaction of 1.0” confuses generating-model logit parameters with the declared probability-scale contrast. “Holds its level” also overstates the finite simulation checks.  
    **Exact replacement text:**

    > The primary analysis averages function contrasts within protocols and compares protocol means. The simulation uses vulnerability retention in every arm and varying function-level interactions. Across the tested zero-contrast settings, including equal nonzero interactions, rejection rates range from 0.043 to 0.057. These support approximate calibration in those settings. At 160 functions, power is 0.805 for generating interactions of 1.0 and 0, 0.831 for 1.5 and 0.5, and 0.809 for 2.0 and 1.0. These parameters are on the logit scale; their differences are not the probability-scale contrast θ. Before confirmatory collection, paper 2 must specify its smallest effect on the probability scale and validate power for both configurations and the intended claim family. The random-slope model is secondary.

12. **Row: 16.**  
    **Problem:** Recording H-02 assumptions does not answer whether the attack survives an independent H-02 correction. The required backing assertion is also omitted.  
    **Exact replacement text:**

    > Month one schedules the full 63008 evidence package. It must assert victim entitlement and backing, validate a correction to the target function body alone, record capital and ordering assumptions, test the attack with H-02 corrected independently, and state which effects depend on H-02 or unchanged surrounding code. The package remains incomplete. If it fails the standard, 63008 is not presented as a validated showcase.

13. **Row: 23.**  
    **Problem:** The response does not explicitly explain the departure from the AC’s request for two month-two freezes.  
    **Exact replacement text:**

    > Paper 1 contains RQ1 and detection validation and targets ICSE. Paper 2 contains faulty assertions and PoV-guided repair and targets FSE or ISSTA. Month two freezes paper 1’s design and decides paper 2’s scope. Unlike the AC’s proposed schedule, paper 2 receives its own later freeze only after calibration and feasibility checks. Paper 1 is scheduled for submission in months 10 to 11. Paper 2 targets month 12 only if its evidence and funding are complete; otherwise it continues separately. Wording effects remain an extension.

14. **Row: 24.**  
    **Problem:** “The Holm test decides claims” is too broad, and “intervals are calibrated to cover the target” implies completed validation under the actual design.  
    **Exact replacement text:**

    > The target is the finite eligible function frame declared before sampling. For agents, it averages fresh runs under the frozen configuration and budget. Holm-adjusted tests determine directional significance for the two primary D comparisons. Pointwise intervals describe estimation uncertainty and do not replace that family decision. Equivalence has a separate rule. K and the sampling-design comparison remain secondary unless separately included in the preregistered multiplicity plan. Existing calibration concerns simulated populations; the actual finite sampling design must be validated before confirmatory inference.

15. **Row: Disagreement 1.**  
    **Problem:** The response again says three estimates and claims that validation evidence bounds detection differences. Natural-flaw recall is not identified by these checks.  
    **Exact replacement text:**

    > Which way detection differences bias the result: no net direction is assumed. Own-campaign labels remove the extra primary discovery opportunities caused by pooled replay. Four views separate own discovery, pooled discovery, audit supplementation, and their union. Seeded validation, audit rediscovery, and independent investigation provide separate evidence. They do not establish natural-flaw recall. Sensitivity analysis reports assumptions under which the latent difference reverses sign; if plausible ranges reverse it, prevalence is reported as not identified (item 2).

16. **Row: Disagreement 4.**  
    **Problem:** “Validated power” lacks its scenario qualification. “Additions are extensions” overlooks the permitted changes to the core allocation.  
    **Exact replacement text:**

    > Shrink or add: protect the smaller core. The minimum planning allocation is 15 protocols. Expansion to 20 protocols or up to four V functions requires the stated cost and inference checks. Power is reported for the simulated settings, with explicit limits on smaller effects and interpretation of null results. Other experiments have separate allocations and cannot consume paper 1’s protected resources (items 1, 6, and 7).

AGREE: no Blocking/Major issues remain