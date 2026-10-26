# Functions linked to High and Medium findings, per protocol audit

The proposal samples protocols. Within each protocol it takes up to six V functions. A V function is a function linked to a High or Medium finding whose fix stays inside one function body. How precise the study is depends on how many V functions each protocol has. So far the proposal had only the 10-protocol pilot vector `[9, 2, 2, 0, 1, 1, 1, 1, 0, 0]` and an assumed distribution, 2 + Poisson(2). A reviewer asked for a count taken from the full set of downloaded findings. This folder gives that count.

Every number below is printed by the script. Nothing was counted by hand, except the spot check described under *Checks*.

## Files

- The analysis script (`frame_inventory.py`). Python 3, standard library only. It reads the downloaded findings and the Tier 1 Solidity files, writes the per-audit table, and prints every table in this file.
- The per-audit table (`per_protocol_audit.csv`). One row per protocol audit (2,481 rows). Columns:
  - `audit_key`: the firm and the contest id or report link that defines the audit.
  - `firm`, `protocol`: the Solodit `firm_name`, and the most common `protocol_name` among the audit's findings.
  - `year`, `month`: the latest year and month found in the audit's links. Empty when no link carries a date.
  - `hm_findings`, `high`, `medium`: the number of High and Medium findings.
  - `solidity_signal`: True when at least one finding mentions a `.sol` file or has a Solidity code block.
  - `mapped`, `unmapped`, `share_unmapped`: findings that were or were not mapped to a function.
  - `well_mapped`: True when at least 80% of the audit's High and Medium findings were mapped.
  - `distinct_functions`: distinct functions reached by the first usable line link of each mapped finding. This is the upper bound on V functions before the one-function rule.
  - `distinct_functions_all_links`: the same count when every line link of every finding is used.
  - `findings_linking_several_functions`: findings whose line links reach two or more functions.
  - `unmapped_no_sol_link`, `unmapped_no_line_link`, `unmapped_no_tier1_file`, `unmapped_line_outside_function`, `unmapped_parse_failure`: why findings were not mapped.
  - `functions`: the distinct functions, written as `File.sol::functionName`.
  - `adjusted_draw`: one random draw of min(6, kept functions), where each linked function is kept with probability 17/34. Fixed seed.
  - `model_draw`: one random draw of min(6, kept functions) built from the audit's High and Medium count instead of its linked functions. See step 4.
- This file (`README.md`).

## How to reproduce

```bash
cd /Users/minh/Documents/workspaces/secure-solvibe
python3 -I proposal_workspace/evidence/frame_inventory/frame_inventory.py
```

It takes about two minutes and uses no network. It reads `data_collection/` and imports one function from the Tier 1 date filter (`scripts/filter_tier1_after_cutoff.py`). It writes only `per_protocol_audit.csv` in this folder. The seed is fixed (20261022), so the output is the same on every run.

## Data

- **Findings.** The four batch files of downloaded Solodit findings (`data_collection/downloaded_findings/batch_*_solodit_findings.json`) hold 19,627 findings with unique ids. The data overview (`data_collection/README_OVERVIEW.md`) says 19,666 in its total row, but its own batch rows add up to 19,627, and the download state file (`downloaded_findings/download_state.json`) also says 19,627.
- **Severity.** Every finding is HIGH (7,002) or MEDIUM (12,625). The download script (`data_collection/download.py`, line 197) asked the Solodit API for these two impacts only. So the High and Medium filter in this analysis removes nothing.
- **Fields used.** `id`, `kind` (GIT, MARKDOWN or PDF), `firm_name`, `protocol_name`, `impact`, `title`, `content`, `contest_id`, `contest_link`, `source_link`, `github_link`, `pdf_link`. The `report_date` field is empty for every finding.
- **Tier 1 files.** The extraction step saved a full `.sol` file from GitHub for 7,826 findings (`data_collection/batch_*_extracted_contracts/tier_1_complete/`). Each file has a metadata file next to it. Its `source_url` field gives the GitHub link the file came from. These 7,826 files cover 4,207 distinct GitHub files (same owner, repository, commit or branch, and path).

## Method

### 1. Protocol audits

A protocol audit is one contest or one audit report. The script groups findings like this:

1. If the finding has a `contest_id` (Code4rena, Sherlock, Codehawks), the audit is that contest.
2. Otherwise, if the finding is a GIT finding (the Immunefi boosts), the audit is the firm plus the protocol name. Their links point to single findings, so they cannot be used.
3. Otherwise, the audit is the first non-empty link among `pdf_link`, `source_link` and `contest_link`, with any `#anchor` removed. This is the PDF report, the Markdown report, or the report page.

The year comes from dates written in the audit's links, such as `code-423n4/2025-10-...`, `security-review_2025-11-03.md` or `...-November-2025.pdf`. The script reuses the rule that built the Tier 1 master table (`linked_month` in `scripts/filter_tier1_after_cutoff.py`). An audit gets the latest month found in any of its findings' links. No audit had links pointing to two different years. When no link carries a date, the year is left empty. "2025+" means a linked date in January 2025 or later. The latest date found is March 2026.

### 2. From a finding to a function

1. **Links.** The script finds GitHub links to `.sol` files in the finding text: `https://github.com/<owner>/<repo>/blob/<ref>/<path>.sol`, optionally with `?plain=1` and a line anchor `#L<n>`. It drops links to test and script files (`.t.sol`, `.s.sol`, or a `test/`, `tests/` or `testing/` folder). A line link is a link with a line anchor.
2. **Files.** The extraction step saved only one file per finding: the first `.sol` link it could download. To use more of the saved files, the script indexes all Tier 1 files by owner, repository, ref and path. A file saved for one finding is then also used for any other finding that links the same file at the same ref.
3. **Which line.** The script walks the line links in the order they appear in the text. It takes the first one whose file exists locally and whose line falls inside a function. This is "the first linked line". It also records the functions reached by all line links, as a second count.
4. **Finding the function.** The script reads the Solidity source with a simple parser, not a compiler:
   - It blanks out comments and string literals but keeps line breaks, so line numbers do not move.
   - It matches every `{` with its `}`. If the braces do not balance, the file counts as a parse failure.
   - It looks for declarations at the start of a line: `function name(`, `function(` (the old fallback), `modifier name`, `constructor(`, `fallback(`, `receive(`.
   - A declaration whose next `;` comes before its next `{` has no body (interface, abstract function, or function-type variable), so it is skipped.
   - A function's lines run from its declaration to its closing brace. The range also takes in the comment or blank lines directly above the declaration, so a link to a function's NatSpec comment maps to that function.
   - When a line falls inside two ranges, the outer one wins. This maps a line inside an inline assembly function to the Solidity function that contains it.
5. **Function identity.** A function is the file name plus the function name, for example `RiskEngine.sol::twapEMA`. The same function linked at two commits counts once.
6. **Unmapped findings** get one reason, checked in this order: no `.sol` link at all; `.sol` links but none with a line anchor; and then, across the line links, a parse failure, a line outside any function, or no local file.

### 3. Counts per audit

For each audit the script counts the High and Medium findings, the mapped findings, and the distinct functions reached by the first linked line of each mapped finding. That last count is the upper bound on V functions before the one-function rule.

### 4. Distributions and the one-function adjustment

The script reports how many audits have 0, 1, 2, 3, 4, 5 and 6 or more distinct linked functions, with the mean and median. It does this for all audits, for audits from 2025 onward, and for two subsets of each:

- **Audits with Solidity code**: at least one finding mentions a `.sol` file or has a Solidity code block. This removes audits of Rust, Move, Go and other code.
- **Audits with at least 80% of findings mapped**: here the count of linked functions is close to complete.

**The one-function adjustment (a).** In the pilot fix-scope study (`proposal_workspace/evidence/frame_count/`), 17 of the 34 findings with an identified fix had a fix confined to one function body. The script keeps each linked function with probability 17/34 and records min(6, kept functions) for each audit. It repeats this 20,000 times with a fixed seed and reports the average share of audits at each value. The rate 17/34 comes from 34 pilot findings in 10 protocols, so it is uncertain. Its Wilson 95% interval is 0.34 to 0.66.

**An estimate from High and Medium counts (b).** Most unmapped findings are unmapped because the report has no line links, not because the finding has no function. The number of High and Medium findings per audit is known for every audit. So the script also builds the distribution from that count:

- In audits with at least 80% of findings mapped, there are 0.729 distinct functions per mapped finding. The rest of the findings share a function with another finding in the same audit.
- Each High or Medium finding is then treated as giving a new function with probability 0.729, which is kept with probability 17/34. That is 0.365 in total. The script records min(6, kept functions) per audit and simulates as in (a).

### Checks

- **Function parser.** The script runs a small test contract through the parser before it starts. The test has a comment that looks like a function, a string holding a `}`, a function-type parameter, an inline assembly function, an interface-style declaration and a `receive` function.
- **Spot check.** I read five randomly drawn mapped findings by eye, comparing the linked line with the function found. All five were right. I also read two findings whose line fell outside any function. Both linked to the NatSpec comment above a function. This is why function ranges now include the comment lines directly above them. The change moved 172 findings from "line outside any function" to mapped.
- **Name in the text.** For 6,193 of the 7,658 mapped findings (81%), the mapped function's name appears in the finding's title or text. The other findings often name the caller, the contract or a variable instead, so this is only a loose check.
- **Text names as a substitute.** I tested whether the first function named in backticks in the title or description (`Name::fn`, `Name.fn(` or `fn(`) could replace line links for reports that have none. Of 2,931 mapped findings that also name a function this way, only 1,435 (49%) name the same function as the line link. That is too unreliable, so text names are not used for counting.
- **Simulation.** For every row of the adjustment tables, the script checks that the simulated shares are within 0.01 of the exact binomial values.

## Results

### Protocol audits

There are **2,481 protocol audits**. 2,305 of them have Solidity code. 543 have at least 80% of their findings mapped. 258 have a linked date in 2025 or later.

Protocol audits by firm or contest platform:

| Firm | Audits | With Solidity code | ≥ 80% of findings mapped | 2025+ | 2025+ and ≥ 80% mapped |
|---|---|---|---|---|---|
| Code4rena | 359 | 358 | 144 | 23 | 21 |
| Zokyo | 224 | 163 | 0 | 3 | 0 |
| Sherlock | 224 | 224 | 167 | 35 | 16 |
| Pashov Audit Group | 221 | 206 | 3 | 76 | 2 |
| OpenZeppelin | 218 | 211 | 117 | 0 | 0 |
| MixBytes | 144 | 134 | 61 | 0 | 0 |
| Cantina | 133 | 132 | 0 | 20 | 0 |
| Halborn | 122 | 91 | 8 | 0 | 0 |
| Quantstamp | 113 | 108 | 0 | 0 | 0 |
| ConsenSys | 102 | 95 | 2 | 5 | 0 |
| TrailOfBits | 101 | 94 | 0 | 10 | 0 |
| Spearbit | 98 | 97 | 0 | 24 | 0 |
| Cyfrin | 84 | 82 | 6 | 44 | 2 |
| Shieldify | 83 | 83 | 13 | 0 | 0 |
| SigmaPrime | 71 | 58 | 0 | 0 | 0 |
| OtterSec | 54 | 53 | 0 | 0 | 0 |
| Codehawks | 33 | 33 | 16 | 3 | 0 |
| Hexens | 21 | 21 | 0 | 8 | 0 |
| Trust Security | 16 | 14 | 0 | 0 | 0 |
| ZachObront | 16 | 16 | 0 | 0 | 0 |
| Guardian Audits | 9 | 2 | 0 | 0 | 0 |
| Immunefi | 7 | 5 | 1 | 0 | 0 |
| Kann | 7 | 6 | 0 | 3 | 0 |
| 0x52 | 7 | 7 | 4 | 1 | 0 |
| AuditOne | 6 | 4 | 0 | 0 | 0 |
| Recon Audits | 3 | 3 | 1 | 3 | 1 |
| Oxorio | 2 | 2 | 0 | 0 | 0 |
| Hans | 1 | 1 | 0 | 0 | 0 |
| ThreeSigma | 1 | 1 | 0 | 0 | 0 |
| Naman | 1 | 1 | 0 | 0 | 0 |
| **Total** | **2,481** | **2,305** | **543** | **258** | **42** |

Protocol audits by year of the date in their links:

| Year | Audits | With Solidity code | ≥ 80% of findings mapped |
|---|---|---|---|
| No date in links | 986 | 911 | 200 |
| 2019 | 11 | 10 | 0 |
| 2020 | 29 | 27 | 1 |
| 2021 | 137 | 108 | 5 |
| 2022 | 235 | 221 | 83 |
| 2023 | 376 | 345 | 97 |
| 2024 | 449 | 430 | 115 |
| 2025 | 248 | 243 | 42 |
| 2026 | 10 | 10 | 0 |

### What happened to each finding

| Result | Findings | Share |
|---|---|---|
| Mapped to a function | 7,658 | 39.0% |
| No GitHub `.sol` link in the text | 9,675 | 49.3% |
| `.sol` links, but none with a line anchor | 276 | 1.4% |
| Line link, but no local Tier 1 file for any linked file | 1,824 | 9.3% |
| Line falls outside any function | 194 | 1.0% |
| File could not be parsed | 0 | 0% |
| **Total** | **19,627** | |

The parser read 4,066 local files and failed on none. 3,521 of the 7,658 mapped findings (46%) have line links into two or more functions.

### Distinct linked functions per audit

Counts of audits, using the first linked line of each finding. The mean and median are of the uncapped counts. "Unmapped" is the share of the set's High and Medium findings that were not mapped.

| Audit set | Audits | 0 | 1 | 2 | 3 | 4 | 5 | 6+ | Mean | Median | H/M findings | Unmapped |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| All audits | 2,481 | 1,555 | 212 | 125 | 90 | 93 | 61 | 345 | 2.30 | 0 | 19,627 | 61.0% |
| With Solidity code | 2,305 | 1,379 | 212 | 125 | 90 | 93 | 61 | 345 | 2.48 | 0 | 19,137 | 60.0% |
| ≥ 80% of findings mapped | 543 | 0 | 90 | 65 | 46 | 61 | 41 | 240 | 7.17 | 5 | 5,686 | 6.1% |
| 2025+ | 258 | 187 | 25 | 8 | 4 | 8 | 2 | 24 | 1.64 | 0 | 1,977 | 74.4% |
| 2025+, with Solidity code | 253 | 182 | 25 | 8 | 4 | 8 | 2 | 24 | 1.67 | 0 | 1,971 | 74.3% |
| 2025+, ≥ 80% mapped | 42 | 0 | 7 | 3 | 3 | 7 | 2 | 20 | 7.86 | 5 | 418 | 3.8% |

The same count using every line link of every finding gives higher numbers. The mean is 3.82 for all audits, 11.98 (median 8) for audits with at least 80% mapped, 2.41 for 2025+ audits, and 11.76 (median 7) for 2025+ audits with at least 80% mapped.

The many zeros in the "All audits" and "2025+" rows mostly come from report format, not from the protocols. Many firms name code in the text and in code blocks, but rarely link a line on GitHub. Spearbit, Cantina, Trail of Bits, SigmaPrime and OtterSec have no mapped finding at all. Pashov (27 of 1,422 findings mapped), Zokyo (4 of 1,062), ConsenSys (4 of 707), Quantstamp (5 of 563) and Cyfrin (68 of 550) have very few. Of the 182 zeros among 2025+ audits with Solidity code, 145 are Pashov (68), Cyfrin (33), Spearbit (24) and Cantina (20) reports.

The average High and Medium count is 7.9 findings per audit overall (median 5) and 7.7 for 2025+ audits (median 4). Audits with at least 80% mapped are larger: 10.5 on average (median 6).

Distinct functions per mapped finding, in audits with at least 80% mapped, by audit size:

| Mapped findings in the audit | Audits | Distinct functions per mapped finding |
|---|---|---|
| 1 | 75 | 1.000 |
| 2 to 3 | 88 | 0.886 |
| 4 to 6 | 128 | 0.829 |
| 7 to 10 | 89 | 0.840 |
| 11 to 20 | 100 | 0.750 |
| 21 or more | 63 | 0.626 |
| **All** | **543** | **0.729** |

### After the one-function adjustment

**(a) Each linked function kept with probability 17/34, capped at 6.** Average share of audits at each value over 20,000 simulated runs.

| Audit set | Audits | 0 | 1 | 2 | 3 | 4 | 5 | 6 | Mean | Median |
|---|---|---|---|---|---|---|---|---|---|---|
| All audits | 2,481 | 69.0% | 9.8% | 5.8% | 4.0% | 2.8% | 2.1% | 6.5% | 0.94 | 0 |
| With Solidity code | 2,305 | 66.7% | 10.6% | 6.2% | 4.3% | 3.0% | 2.3% | 7.0% | 1.01 | 0 |
| ≥ 80% of findings mapped | 543 | 13.4% | 22.5% | 15.8% | 11.7% | 8.5% | 6.4% | 21.7% | 2.86 | 2 |
| 2025+ | 258 | 78.6% | 8.1% | 3.5% | 2.4% | 1.7% | 1.2% | 4.6% | 0.62 | 0 |
| 2025+, with Solidity code | 253 | 78.1% | 8.3% | 3.5% | 2.5% | 1.7% | 1.2% | 4.7% | 0.64 | 0 |
| 2025+, ≥ 80% mapped | 42 | 12.4% | 20.8% | 15.8% | 12.7% | 8.9% | 6.4% | 23.1% | 2.96 | 3 |

**(b) Built from the High and Medium count: each finding gives a kept function with probability 0.729 × 17/34 = 0.365, capped at 6.**

| Audit set | Audits | 0 | 1 | 2 | 3 | 4 | 5 | 6 | Mean | Median |
|---|---|---|---|---|---|---|---|---|---|---|
| With Solidity code | 2,305 | 19.4% | 24.8% | 16.7% | 11.1% | 7.4% | 5.1% | 15.5% | 2.40 | 2 |
| 2025+, with Solidity code | 253 | 22.9% | 26.5% | 15.9% | 10.2% | 6.8% | 4.7% | 13.0% | 2.17 | 2 |

Expected number of 2025+ audits at each value, out of the audits in the set:

| Audit set | Audits | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|---|
| (a) 2025+, with Solidity code | 253 | 197.7 | 20.9 | 9.0 | 6.3 | 4.4 | 3.0 | 11.8 |
| (a) 2025+, ≥ 80% mapped | 42 | 5.2 | 8.7 | 6.6 | 5.3 | 3.7 | 2.7 | 9.7 |
| (b) 2025+, with Solidity code | 253 | 58.0 | 67.1 | 40.2 | 25.7 | 17.2 | 11.8 | 32.9 |

**For comparison.** The assumed distribution, 2 + Poisson(2) capped at 6, puts 0% at 0 and 1, then 13.5%, 27.1%, 27.1%, 18.0% and 14.3% at 2 to 6. Its mean is 3.92. The pilot vector `[9, 2, 2, 0, 1, 1, 1, 1, 0, 0]` has mean 1.7, or 1.4 when capped at 6, and 3 of its 10 protocols have zero. Both data-based versions that are not dominated by missing links have a lower mean than the assumed distribution: 2.96 for 2025+ audits with at least 80% mapped, and 2.17 for the estimate from High and Medium counts. Both also put 12% to 23% of audits at zero and 21% to 27% at one, where the assumed distribution puts none.

### Comparison with the pilot

The pilot counted distinct functions with a one-function fix in the 10 pilot audits (`proposal_workspace/evidence/frame_count/README.md`). This table sets those counts beside the linked-function counts from this analysis.

| Protocol | Audit | H/M findings | Mapped | Distinct linked functions | Pilot: distinct one-function functions |
|---|---|---|---|---|---|
| Panoptic | Code4rena 2025-12 | 22 | 21 | 18 | 9 |
| Licredity | Cyfrin 2025-09 | 5 | 4 | 4 | 2 |
| Ekubo | Code4rena 2025-11 | 4 | 4 | 4 | 2 |
| Sequence | Code4rena 2025-10 | 6 | 6 | 6 | 0 |
| Merkl | Code4rena 2025-11 | 3 | 3 | 3 | 1 |
| Sorella L2 Angstrom | Cyfrin 2025-10 | 5 | 1 | 1 | 1 |
| stETH by EaseDeFi | Sherlock 2025-11 | 12 | 1 | 1 | 1 |
| Wannabet | Cyfrin 2025-12 | 3 | 1 | 1 | 1 |
| Ammplify | Sherlock 2025-09 | 36 | 1 | 1 | 0 |
| YuzuUSD | Pashov 2026-01 | 2 | 1 | 1 | 0 |

The High and Medium counts match the pilot table. In the five audits with at least 80% of findings mapped (Panoptic, Licredity, Ekubo, Sequence, Merkl), the pilot kept 14 of the 35 linked functions (0.40). This is a little below the 0.5 used for the adjustment, but within the uncertainty of 17/34. For stETH by EaseDeFi and Ammplify the reports do link lines, but the extraction saved no file for 11 of 12 and 34 of 36 findings. The pilot itself only assessed findings in its 77-finding table. So its counts for Ammplify, stETH by EaseDeFi, Sorella L2 Angstrom, Wannabet, YuzuUSD and Licredity are also partial.

### Vectors for sampling

Each list has one integer per 2025+ audit, in the row order of `per_protocol_audit.csv`. The adjusted lists are one fixed-seed random draw each, not averages. Draw again, or use the shares above, if you need more than one realization.

(a) 2025+ audits with Solidity code, one adjusted draw (`adjusted_draw` column, 253 audits). Most zeros here come from reports without line links:

```python
[3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 6, 6, 2, 1, 3, 5, 6, 0, 6, 3, 3, 0, 5, 3, 3, 4, 1, 2, 1, 5, 1, 0, 6, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 6, 0, 1, 6, 0, 6, 2, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 4, 3, 2, 6, 1, 4, 0, 4, 6, 2, 0, 6, 6, 4, 1, 0, 3, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
```

(a) 2025+ audits with at least 80% of findings mapped, one adjusted draw (`adjusted_draw` column, 42 audits):

```python
[1, 1, 6, 6, 2, 1, 3, 5, 6, 0, 6, 3, 3, 5, 3, 3, 4, 1, 2, 1, 5, 0, 3, 0, 0, 1, 6, 6, 2, 1, 1, 3, 2, 6, 4, 6, 2, 6, 6, 4, 3, 5]
```

The same 42 audits before the adjustment (`distinct_functions` column):

```python
[3, 4, 10, 26, 2, 1, 4, 8, 23, 1, 30, 6, 4, 6, 9, 4, 9, 4, 3, 3, 18, 1, 4, 1, 1, 6, 28, 11, 2, 1, 1, 7, 4, 11, 5, 21, 2, 13, 7, 5, 8, 13]
```

(b) 2025+ audits with Solidity code, one draw from the estimate built on High and Medium counts (`model_draw` column, 253 audits):

```python
[4, 0, 0, 2, 2, 1, 1, 6, 5, 3, 2, 0, 2, 1, 0, 4, 0, 1, 0, 1, 4, 2, 1, 1, 6, 6, 3, 1, 2, 3, 6, 0, 6, 4, 1, 1, 2, 2, 2, 6, 4, 1, 1, 6, 6, 1, 6, 0, 1, 1, 2, 0, 0, 2, 5, 1, 0, 2, 0, 1, 3, 0, 6, 2, 6, 6, 2, 2, 0, 2, 0, 0, 0, 1, 0, 1, 2, 2, 0, 0, 1, 6, 3, 6, 4, 1, 0, 0, 2, 1, 1, 1, 0, 0, 1, 2, 2, 3, 0, 1, 3, 2, 1, 0, 3, 1, 0, 1, 1, 1, 2, 3, 2, 0, 5, 4, 2, 4, 2, 3, 2, 4, 1, 0, 1, 1, 2, 5, 4, 1, 1, 0, 6, 4, 1, 4, 4, 1, 2, 1, 5, 6, 5, 2, 2, 0, 2, 0, 0, 6, 1, 1, 0, 1, 5, 0, 1, 2, 0, 0, 0, 6, 1, 2, 2, 0, 3, 1, 0, 2, 0, 0, 2, 2, 4, 4, 5, 6, 3, 6, 0, 6, 1, 6, 1, 0, 6, 1, 2, 2, 0, 4, 2, 0, 6, 2, 1, 6, 2, 5, 3, 6, 6, 0, 2, 5, 3, 5, 0, 0, 3, 6, 1, 0, 6, 6, 6, 5, 0, 0, 0, 1, 0, 0, 0, 2, 2, 1, 0, 1, 1, 1, 2, 4, 1, 0, 3, 5, 0, 3, 0, 0, 0, 5, 0, 6, 0, 2, 1, 6, 3, 1, 0]
```

## Limitations and biases

- **Audits with no High or Medium finding are missing.** The download asked the API for High and Medium findings only, and the data hold no contest listings. Every audit here has at least one High or Medium finding. A sampling frame built from contest listings would also hold audits with none, and each would give zero V functions. Their share cannot be estimated from these files. It is unknown.
- **Unmapped findings make the counts too low.** 61% of all findings and 74% of 2025+ findings are unmapped. The main cause is report format: 49% of findings have no GitHub `.sol` link at all. A second cause is missing files: 1,824 findings (9%) have line links, but no local file exists for any linked file. The extraction log (`failed_extractions.log`) does not give a usable reason for these. The rows for all audits and for all 2025+ audits are therefore lower bounds.
- **The 80%-mapped subset is not a random sample.** It is mostly Code4rena, Sherlock, OpenZeppelin and MixBytes audits. Among 2025+ audits it is 21 Code4rena, 16 Sherlock, 2 Pashov, 2 Cyfrin and 1 Recon. These audits have more High and Medium findings than average (10.5 against 7.9), so this subset probably overstates the count for private reviews.
- **The estimate from High and Medium counts uses one pooled rate.** The rate 0.729 is learned on the 80%-mapped audits and applied to every firm. The table by audit size shows the true rate falls from 1.0 in one-finding audits to 0.63 in audits with 21 or more. One pooled rate therefore understates small audits and overstates large ones. The cap at 6 hides most of the overstatement.
- **One finding can link to several functions.** 46% of mapped findings have line links into two or more functions. The main counts use only the first usable line link, because a finding with a one-function fix gives one V function. Counting all links raises the means by 47% to 67%, depending on the audit set.
- **Several findings can share a function.** This is why there are fewer distinct functions than mapped findings (0.729 per finding in the 80%-mapped audits). The count of distinct functions already handles it.
- **The one-function rate is uncertain.** 17/34 comes from 34 pilot findings in 10 protocols. Its Wilson 95% interval is 0.34 to 0.66. The simulation also treats each function as an independent draw. In the pilot the rate varied by protocol: 9 of the 21 Panoptic pilot findings had a one-function fix, against 0 of the 6 Sequence pilot findings.
- **Many audits have no date.** 986 audits (40%) have no date in their links. Most are OpenZeppelin (217), MixBytes (144), Halborn (120), Quantstamp (113), Shieldify (82), Pashov (76) and SigmaPrime (71) reports. They are left out of every 2025+ row. So the 2025+ rows lean toward contests and toward Pashov, Cyfrin, Spearbit and Cantina reports, which have dated links.
- **Function identity is file name plus function name.** Overloaded functions with the same name in one file count once. Links into code from other projects, such as OpenZeppelin or Uniswap libraries, count as functions of the audit.
- **Links to a branch can point to the wrong line.** Some links name a branch such as `main`, not a commit. The saved file may then differ from the audited version, and the line may fall in a different function. I did not measure how often this happens. The name check above (81% of mapped functions are named in the finding text) gives only a loose upper limit on such errors.
- **The parser is not a compiler.** It found no unbalanced files. 194 findings link to lines outside any function. These are state variables, structs, events, interface declarations, or lines past the end of a file that has changed since.
- **The Solidity flag is crude.** One mention of a `.sol` file is enough to count an audit as Solidity.
- **Snapshot.** The findings come from the Solodit download that ended in April 2026. Later findings are not included. Solodit maps firm-specific severity labels to HIGH and MEDIUM, for example Cyfrin "Critical" becomes HIGH.
