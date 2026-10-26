## V45 and the reported numbers

V45 reuses V44’s study runner, confirmation procedure, estimator, unresolved-outcome mechanisms, warning and demand calculation. The saved results support the smaller region. However, “V44 unchanged apart from the frame” needs these qualifications:

| Difference | Assessment |
|---|---|
| The remaining 187 recorded audits replace resampled frames. Inclusion probabilities use automated eligible counts rather than strict N counts. | Appropriate for the stated sampling design, subject to the frame problems below. |
| The three actual development audits are removed, rather than drawing simulated development exclusions. | Appropriate for a main-study analysis conditional on the recorded draw. |
| Strict counts are fixed from the hand count for 20 audits and imputed for the others. | Reasonable planning sensitivity, clearly identified as imputation. This does not establish the true frame composition. |
| Frame seeds change. Independent-working and linked-working variants no longer share the same underlying generated frame as they did in V44. | Does not invalidate the separate checks. It means differences between those variants are not controlled comparisons holding the generated frame fixed. |
| The development diagnostic draws hypothetical samples from the remaining 187 audits. | Useful as a generic diagnostic check. It does not validate the warning for the three development audits already selected. |
| V44’s old corners remain in the corner checks; the smaller region comes from the full grids for the three-candidate, 0.5-hour workload. | Sound as reported. It does not establish full-grid power for every other workload. The pending launch check must retain that distinction. |

The certainty unit is `sherlock-280`, with a size measure of 1,020. The largest other inclusion probability is 0.691685, correctly reported as 0.692.

I checked the following against the CSV files and saved results:

- The recorded frame has 190 rows: 87 Code4rena and 103 Sherlock; 146 from 2024 and 44 from 2025.
- Automated counts total 22,802, with median 78.5 and maximum 1,020.
- Removing the recorded development audits leaves 187 rows and a size-measure total of 22,151.
- The 20 overlapping hand counts agree with automated eligible counts. The reported strict-N ratios and Spearman correlation reproduce.
- V45’s full-grid bounds are correctly reported: error 0.0466, coverage 0.9551 and reading error 0.0351, with no recorded undefined estimates.
- The reported corner power figures, exhaustion frequencies and maximal vectors match the results.
- Intersecting the downward-closed passing regions reproduces `(0, 0, 0.0075)` and `(0.013, 0.013, 0.005)`.
- The six pooled demand percentiles—109, 217, 168, 169, 338 and 230 hours—and the largest frame-specific percentile of 386 hours match the demand file.
- The abstract has 145 words.

These are checks of the code and recorded results, not a rerun of the simulations.

## Population, region and development draw

Restricting the population to represented Code4rena and Sherlock audits with accessible audited code is defensible. It must remain a finding-derived population, rather than all public audits from those firms. The absence of links in the downloaded Cantina findings supports exclusion from this operational frame; it does not establish that those projects have no public code anywhere.

Adopting the smaller operating region is also defensible. The proposal preserves the 0.60 requirement, reports the failed corner and keeps final validation mandatory. It does not claim that development can certify these rare unresolved rates.

The development draw reproduces exactly from the saved frame and seed, including order, probabilities and output hash. The seed record states that it was fixed before frame construction. I found no evidence of an outcome-driven redraw. That record is not an independently authenticated timestamp, but this alone is not a rejection issue.

The later README-only explanation for `sherlock-858` is consistent with exclusion for unavailable audited code, rather than exclusion merely because its function count is zero. The blank exposure record remains a required step before blind work.

## Remaining issues

### R29.1 [Major] [C4, C6] Duplicate snapshots remain separate sampling units

**Section:** 5.1; frame construction; V45.

**Problem:** Section 5.1 says overlapping snapshots cannot be treated as independent protocols without accounting for dependence. Yet `code4rena-396` and `code4rena-399` both point to:

`code-423n4/2024-06-krystal-defi@f65b381b258290653fa638019a5a134c4ef90ba8`

Both use `scope.txt` and report five files, 62 functions and 34 eligible functions. Their inventory entries also describe Krystal and the same linked function names. V45 generates separate protocol effects for these records. No reconciliation or dependence treatment is recorded.

This is a concrete frame defect, not merely a future simulation requirement.

**Required change:** Reconcile duplicate and overlapping audit snapshots under one explicit sampling-unit rule, including the treatment of these two records and the consequences for the archived development draw, main probabilities and simulation frame.

### R29.2 [Major] [C4, C6] A dependency repository substitutes for inaccessible audited code

**Section:** 5.1; `evidence/frame_build/fetch_and_count.py`; rebuttal item 7.

**Problem:** `sherlock-1202` is counted as eligible even though its project repository, `sherlock-audit/2025-11-inverse-finance-junior-tranche`, failed to fetch. Its 123 eligible functions come solely from `transmissions11/solmate@main`, using automatic scope.

The counting script accepts any successfully fetched listed repository. It does not establish that this repository contains the audit’s target code. This contradicts the proposal’s claim that all 190 qualifying records contain accessible audited Solidity code. It also differs from the treatment of the README-only audit.

**Required change:** Apply and document a repository-to-audit eligibility check that distinguishes audited target code from linked dependencies, resolving `sherlock-1202` and updating the frame claims under the same rule.

### R29.3 [Minor] [C4, C6] Branch names do not preserve the counted snapshots

**Section:** Frame evidence and development provenance.

**Problem:** Many `refs_used` entries record `main`, including all three development audits. The fetch script does not save the resolved commit hash. The CSV reproduces the draw, but fetching those branches later need not reproduce the code or counts used to create it.

**Required change:** Add an immutable snapshot manifest for the counted repositories, recording the resolved commit and scope-file hashes from the original checkouts, with any unavailable original snapshot explicitly identified.

### R29.4 [Minor] [C4] The population restriction remains conditional after construction

**Section:** 5.1; rebuttal item 7.

**Problem:** The sentence beginning “Public listings may permit audits without qualifying findings to enter” describes an unresolved alternative. The implemented frame is already derived from the downloaded findings. “Code4rena and Sherlock audits with public linked code” therefore overstates its coverage unless it also identifies that restriction.

**Required change:** Replace the conditional population wording with a definitive restriction to qualifying audits represented in the downloaded finding inventory.

### R29.5 [Minor] [C4] Scope counts overlap without saying so

**Section:** 5.1; frame README.

**Problem:** The reported counts of 77, 110 and four sum to 191. The CSV explains why: `code4rena-476` uses both `scope.txt` and README scope. There are 76 `scope.txt`-only audits, 109 README-only audits, one using both and four using automatic scope.

**Required change:** Report those four mutually exclusive categories, or explicitly identify the one overlapping audit.

### R29.6 [Minor] [C6] The development diagnostic is not conditional on the actual development sample

**Section:** 6.3, V45 description.

**Problem:** V45’s diagnostic samples three protocols from the remaining 187. The actual development audits have already been removed. The script states this, but the proposal’s “unchanged” description does not explain its implication.

**Required change:** State that V45’s development-warning results concern hypothetical samples from the main frame and provide no sample-specific validation for the three selected development audits.

### R29.7 [Minor] [C4] Demand comparison in the rebuttal is broader than the evidence

**Section:** Rebuttal, “What V45 changes” and “Demand selection and funding.”

**Problem:** “Demand on the real frame is within 8 hours of V44” is supported specifically for the six **pooled +0.15 95th percentiles**. Later, “The supplied demand file” gives V44’s 111–346-hour range without naming V44, although V45’s corresponding range is 109–338.

**Required change:** Identify V44 and V45 explicitly in these passages and restrict the eight-hour comparison to the six pooled +0.15 95th percentiles.

The missing timed case, selected reserve, reduced-seed precision and final-frame validation are not counted in this vote.

DISAGREE: [R29.1, R29.2]