# Counting V and N functions by hand in 25 randomly drawn 2025 contest audits

A reviewer asked for counts that are read from real audits, not modelled. The question was: in a random sample of recent protocol audits, how many V functions does each audit give, with no cap, and how many N functions?

- A **V function** is a function that is the root cause of a High or Medium finding, where the fix stays inside that one function body.
- An **N function** is any other eligible function in the audit's scope.

The earlier numbers were modelled from line links in the downloaded findings. They are in the per-protocol inventory (`../frame_inventory/README.md`). The manual method for the 43 pilot findings is in the pilot fix-scope study (`../frame_count/README.md`). This folder repeats that manual method on 25 randomly drawn audits.

Every number below is printed by the summary script. The reading of findings and fixes was done by hand, as described under *Method*.

## Files

- The sample script (`draw_sample.py`). It builds the list of eligible audits, draws the random order, writes the order file, and dumps each audit's findings to a work folder with finder names removed.
- The function counting script (`count_functions.py`). It counts eligible functions in a list of in-scope files. Its docstring states the eligibility rule. It has a self-test (`--selftest`).
- The summary script (`summarize.py`). It merges the per-audit work files, checks them, writes the CSV files below, and prints every table in this file.
- The random order (`sample_order.csv`). All 70 audits in the frame, in draw order. Columns: `rank`, `audit_key`, `slug` (short folder name), `firm`, `protocol`, `year_month`, `hm_findings`.
- The per-audit table (`per_audit.csv`). One row for each of the 33 drawn audits: 25 processed and 8 replaced. Main columns:
  - `status` and `reason`: processed or replaced, and why it was replaced.
  - `repo_url`, `commit`, `scope_source`, `scope_files`: where the audited code came from and how the scope was found.
  - `hm_findings`, `mapped_findings`, `distinct_root_cause_functions`.
  - `v_functions_observed`: distinct V functions, counting only fixes whose diff was read.
  - `v_functions_incl_recommendation`: the same, also counting findings classified from the finding's recommendation.
  - `findings_one_body_observed`, `findings_one_body_recommendation`, `findings_several_bodies`, `findings_signature_storage_declaration`, `findings_undetermined`: findings by fix class.
  - `findings_with_observed_fix`: findings whose fix diff was read.
  - `functions_with_body`, `eligible_functions`, `v_linked_eligible`, `n_functions`: the function counts. N is eligible functions minus `v_linked_eligible`.
  - `modelled_linked_functions`: the linked-function count for the same audit in the per-protocol inventory, for comparison.
- The per-finding table (`per_finding.csv`). One row for each of the 352 High and Medium findings of the 25 processed audits. Columns: `rank`, `slug`, `finding_id` (Solodit id), `impact`, `title`, `root_cause_functions`, `mapping_basis`, `sponsor_status`, `fix_class`, `fix_evidence`, `v_function`, `fix_reference`, `note`. Functions are written as `File.sol::functionName`, the same form as the inventory.
- The function list (`functions_in_scope.csv`). One row for each of the 5,364 functions with a body in the in-scope files. Columns: `slug`, `path`, `function`, `kind`, `view_or_pure`, `statements`, `branch`, `eligible`, `reason`.
- The scope lists (`scope_files.csv`). One row for each of the 651 in-scope Solidity files, with the repository and commit.
- This file (`README.md`).

## How to reproduce

```bash
cd /Users/minh/Documents/workspaces/secure-solvibe
python3.12 -I proposal_workspace/evidence/frame_audit/draw_sample.py --work <work folder>
python3.12 -I proposal_workspace/evidence/frame_audit/count_functions.py --selftest
python3.12 -I proposal_workspace/evidence/frame_audit/count_functions.py --repo <clone> --scope <scope.txt> --out <functions.csv>
python3.12 -I proposal_workspace/evidence/frame_audit/summarize.py --work <work folder>
```

The scripts use the standard library only. They need Python 3.8 or later, because `draw_sample.py` imports the audit grouping from the inventory script (`../frame_inventory/frame_inventory.py`). Only the sample script reads `data_collection/`, and it only reads. The work folder for this run was `/Users/minh/.claude/jobs/eeaa430c/tmp/frame_audit/`. It holds the clones, the findings dumps and the per-audit work files. It is a temporary folder, so the classifications themselves are kept in the per-finding table. To recount functions, clone each repository at the commit in the scope lists and run the counting script on that audit's files.

## Sample

**The frame.** I took the per-protocol inventory (`../frame_inventory/per_protocol_audit.csv`). I kept audits whose firm is Code4rena, Sherlock or Cantina and whose linked date is 2025 or later. That gives 78 audits. I removed the 8 audits of pilot protocols in this list: Panoptic (two contests), Sequence, Ekubo, Megapot, Merkl, Ammplify and stETH by EaseDeFi. Licredity, Sorella L2 Angstrom, Wannabet and YuzuUSD were audited by other firms, so they were never in the list. **70 audits remain.**

**The draw.** I sorted the 70 audits by `audit_key` and drew the order with `random.Random(20261022).sample(audits, 70)`. I then went down the order until 25 audits were processed. That took the first 33 audits in the order.

**Replacements.** 8 of the 33 drawn audits could not be processed. Each was replaced by the next audit in the same random order.

| Rank | Audit | H/M findings | Why it was replaced |
|---|---|---|---|
| 8 | Cantina private review, Clique (2025-01) | 4 | The report names the repository (clique-bera-contracts) but not its owner. No public copy was found. The one guessed location needs a login. |
| 12 | Cantina private review, Eggs (2025-02) | 6 | The report names the repository (eggs) but not its owner. No public copy was found. |
| 14 | Cantina private review, OP Labs (2025-02) | 1 | The review covers the optimism monorepo at one commit. The report does not say which part was reviewed, so the scope cannot be found. |
| 18 | Sherlock contest 1140, Fusaka Upgrade (2025-09) | 1 | The audited code is Ethereum client code in Go, Rust and TypeScript, not Solidity. |
| 19 | Sherlock contest 1073, USG Tangent (2025-08) | 16 | The contest repository needs a login. The findings link no public sponsor repository. |
| 22 | Sherlock contest 1176, Summer.fi (2025-09) | 4 | The contest repository needs a login. The public sponsor repository is a large monorepo, and the scope list is not public. |
| 24 | Cantina private review, 0xhoneyjar (2025-02) | 3 | A public repository with the same name exists, but neither the reviewed commit nor the fix commits are in it. |
| 27 | Cantina private review, PintoFarm (2025-02) | 1 | The public repository's history starts after the review, so the reviewed commit is not in it. |

The replacements were ranks 26 and 28 to 33. They are real replacements, not part of the first 25 draws.

**The 25 processed audits.** 13 Sherlock contests, 8 Code4rena contests, 2 Cantina competitions and 2 Cantina private reviews. They hold 352 High and Medium findings. Five of the eight replaced audits are Cantina private reviews, because their code is often not public. So private reviews are under-represented. Only 2 of the 7 drawn private reviews could be processed.

## Method

### Audited code and scope

- **Repositories.** For contests I cloned the public contest repository (`github.com/code-423n4/<contest>`, `github.com/sherlock-audit/<contest>`, `github.com/cantina-competitions/<name>`) with `git clone --depth 1` or `--filter=blob:none`, over HTTPS, with no credentials. Two cases differ:
  - Sherlock contest 1154 (BMX Deli Swap): the contest repository needs a login. The sponsor's public repository holds the final Sherlock report, which names the audited commit and the scope. I used that commit.
  - The two Cantina private reviews (Olas, Eco): I cloned the sponsor's public repository and checked out the commit named in the report.
- **Scope.** 23 audits have a scope list: the Code4rena `scope.txt`, the Sherlock README section "Audit scope", the Cantina competition page, or the Sherlock report for contest 1154. For the two Cantina private reviews, the report names the whole repository, so the scope is its `contracts/` folder without tests, mocks, scripts and copied third-party code. Only `.sol` files count. Rust, Move and Go files in some scopes were left out.
- **Nothing from the repositories was run.** No builds, no tests, no scripts. Files were only read.

### Eligible functions

The counting script reads each in-scope file with a simple parser, not a compiler. It blanks out comments and strings, matches every `{` with its `}`, and finds each `function`, `constructor`, `fallback` and `receive` declaration that has a body. A file whose braces do not balance is a parse failure. There were none.

A function is **eligible** when one of these holds:

- It is not `view` or `pure`, its body is not empty, and it is not a single-call forwarding wrapper. A forwarding wrapper is a body with one statement, no branch and no assignment, where that statement is a call.
- It is `view` or `pure` and has more than one statement or any branch.
- Its body has an `assembly` block.

Statements are the `;` in the body, minus two for each `for (` header. Branches are `if`, `else`, `for`, `while`, `do`, `try`, `catch`, `switch`, `require(`, `assert(` and the `?` operator. Modifiers are not counted. Declarations without a body (interfaces, abstract functions) are skipped. A function that is not `view` or `pure` is treated as one that writes state. The script does not check whether it really does.

Of the 5,364 functions with a body, 3,965 (74%) are eligible. The rest are 926 simple getters, 358 forwarding wrappers and 115 empty bodies.

### From a finding to its root-cause function

For each High and Medium finding, the reader used the finding's line links (Sherlock "Root Cause" links, Code4rena links, Cantina "Context" lines) and read the finding text against the code. The root-cause function is written as `File.sol::functionName`, where the file defines the function. 264 findings were mapped from a line link, and 88 by reading the text against the code. 18 findings have a root cause outside any function: a constant, a state variable, a missing function, or a design issue. 86 findings name two or more root-cause functions.

### Finding the fix

The reader looked for the fix in this order:

1. A fix link in the finding text. Sherlock findings often say "The protocol team fixed this issue in the following PRs/commits". Cantina reports say "Fixed in commit X".
2. The Sherlock judging issue page, or the Code4rena mitigation repository or report section.
3. The sponsor's public repository history after the audited commit. Commit messages often cite the issue number or describe the bug.

The fix diff was then read. Tests, scripts, comments, formatting and edits in the same commit that belong to other findings were ignored.

### Fix classes

The class describes the fix the developers actually wrote. It does not say whether a narrower fix was possible. The four classes are the same as in the pilot fix-scope study:

- **one function body**: the fix changes the body of one function only. A new custom error or event used only by that fix does not change the class. Renaming a parameter, with the same types and order, is ignored.
- **several function bodies**: the bodies of two or more functions change, with no signature or declaration change.
- **signature, storage or new declaration**: a signature, a visibility or the function header changes, the storage layout changes, a function is added or removed, or a declaration outside functions changes.
- **undetermined**: there is no fix (acknowledged, won't fix, disputed) or the fix could not be found, and the finding's recommendation is not clear enough to classify.

Adding a modifier or changing a base-constructor argument changes the function header, not the body. So such fixes go in the third class. Two rows were first classified as one function body by their reader. I moved them to the third class when merging, so that one rule holds in all audits. Their notes say "Reclassified at merge".

### Evidence

- **observed fix**: the reader read the fix diff.
- **from recommendation**: no fix diff could be read, or the issue was not fixed. But the finding's recommendation is a clear change, for example a code diff or an exact change inside one function. The class comes from that recommendation.
- **none**: the class is undetermined.

### V and N per audit

- **V (observed)** is the number of distinct functions named in `v_function` among findings with an observed fix in the one-function-body class.
- **V (including from recommendation)** adds the findings classified from the recommendation.
- One function can be the V function of several findings. It counts once. For example, five Malda findings have their fix in `EverclearBridge.sol::sendMsg`.
- **N** is the number of eligible in-scope functions, minus the eligible functions linked to any High or Medium finding of the audit. A function is linked if it is a root-cause function or a V function, whatever the fix class. Overloaded functions with the same name in one file share one name, so they are subtracted once.

### Who did the reading, and checks

The reading was split across eight Claude agent sessions that ran in parallel, each with 1 to 5 audits. All of them followed one written brief with the rules above. They only read the repositories, and they ran no code from them. Two sessions said they once wrote a temporary file to `/tmp` by mistake and deleted it at once. Otherwise they wrote only in their audits' work folders. I then merged the results and ran these checks:

- **Completeness.** Every finding id in each audit's findings dump appears exactly once in the per-finding table, and every class and evidence value is one of the allowed values. The summary script asserts this.
- **Names.** Every root-cause function name matches a function found by the counting script, except one. That function (`VaultComposerSync.sol::_depositAndSend` in Brix Money) is in a library outside the scope.
- **Spot check.** I drew 6 rows at random and checked them against the fix diff or the recommendation: Malda M-4, DODO M-6, Notional M-4, the TermMax redeem-fee finding, Hybra M-08 and GTE M-17. All 6 agreed with the recorded class.
- **One rule for header edits.** See *Fix classes*. Two rows were changed.
- **Personal names.** I checked the CSV files against the 978 finder handles in the downloaded findings for these audits. None appears, apart from one handle that is also an ordinary word ("Constant"). One sponsor repository sits under a personal GitHub account. Its links in the per-finding table are replaced by "DODO sponsor repo (linked in the findings)".

## Results

### Per audit

| Rank | Audit | H/M findings | Mapped | Root-cause functions | Findings with fix diff read | V (observed) | V (incl. recommendation) | Undetermined | Eligible functions | N |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Sherlock contest 1154, BMX Deli Swap (2025-09) | 14 | 14 | 13 | 13 | 6 | 6 | 1 | 191 | 177 |
| 2 | Code4rena contest 539, Brix Money (2025-11) | 3 | 3 | 4 | 0 | 0 | 0 | 1 | 111 | 108 |
| 3 | Code4rena contest 487, IQ AI (2025-01) | 4 | 4 | 4 | 0 | 0 | 2 | 1 | 53 | 49 |
| 4 | Cantina competition, Term Structure (2025-02) | 18 | 17 | 16 | 18 | 7 | 7 | 0 | 139 | 123 |
| 5 | Code4rena contest 513, GTE (2025-08) | 35 | 34 | 45 | 0 | 0 | 11 | 16 | 367 | 327 |
| 6 | Code4rena contest 507, Blackhole (2025-05) | 24 | 23 | 26 | 20 | 10 | 10 | 3 | 696 | 672 |
| 7 | Sherlock contest 968, Superfluid Locker System (2025-06) | 8 | 8 | 6 | 5 | 2 | 2 | 2 | 145 | 139 |
| 9 | Sherlock contest 991, DODO Cross-Chain DEX (2025-05) | 17 | 17 | 18 | 15 | 6 | 6 | 2 | 79 | 63 |
| 10 | Sherlock contest 749, Peapods (2025-01) | 41 | 39 | 40 | 14 | 10 | 15 | 18 | 421 | 381 |
| 11 | Code4rena contest 526, Hybra Finance (2025-10) | 10 | 10 | 10 | 0 | 0 | 5 | 1 | 256 | 246 |
| 13 | Cantina competition, DefiApp (2025-02) | 10 | 10 | 12 | 0 | 0 | 6 | 3 | 173 | 161 |
| 15 | Sherlock contest 799, Aegis.im YUSD (2025-04) | 3 | 2 | 4 | 1 | 1 | 1 | 2 | 71 | 67 |
| 16 | Cantina private review, Olas (2025-01) | 10 | 10 | 15 | 7 | 1 | 2 | 1 | 84 | 70 |
| 17 | Sherlock contest 1051, Allbridge Core Yield (2025-07) | 2 | 2 | 3 | 0 | 0 | 1 | 1 | 49 | 46 |
| 20 | Sherlock contest 1029, Malda (2025-07) | 17 | 13 | 11 | 15 | 3 | 4 | 1 | 194 | 183 |
| 21 | Sherlock contest 977, Yearn yBOLD (2025-05) | 3 | 2 | 3 | 0 | 0 | 1 | 2 | 41 | 39 |
| 23 | Sherlock contest 791, Yieldoor (2025-02) | 17 | 16 | 13 | 0 | 0 | 7 | 7 | 105 | 92 |
| 25 | Code4rena contest 520, Morpheus (2025-08) | 4 | 4 | 5 | 4 | 1 | 1 | 0 | 72 | 67 |
| 26 | Cantina private review, Eco Inc (2025-02) | 10 | 10 | 9 | 9 | 4 | 4 | 0 | 48 | 38 |
| 28 | Sherlock contest 1001, Notional Exponent (2025-06) | 37 | 35 | 46 | 22 | 5 | 7 | 9 | 202 | 158 |
| 29 | Code4rena contest 502, Kinetiq (2025-04) | 8 | 8 | 12 | 0 | 0 | 2 | 4 | 84 | 73 |
| 30 | Sherlock contest 952, LayerEdge Staking (2025-05) | 3 | 3 | 2 | 2 | 1 | 1 | 1 | 34 | 32 |
| 31 | Sherlock contest 498, Rova (2025-02) | 2 | 2 | 1 | 2 | 1 | 1 | 0 | 25 | 24 |
| 32 | Sherlock contest 908, LEND (2025-05) | 39 | 35 | 21 | 0 | 0 | 11 | 19 | 74 | 53 |
| 33 | Code4rena contest 489, Recall (2025-02) | 13 | 13 | 18 | 9 | 4 | 5 | 3 | 251 | 233 |
| | **Total** | **352** | **334** | **357** | **156** | **62** | **118** | **98** | **3,965** | **3,621** |

### Uncapped V functions per audit

| V count | 0 | 1 | 2 | 3 | 4 | 5 | 6 or more | Mean | Median | Audits with zero |
|---|---|---|---|---|---|---|---|---|---|---|
| Observed fixes only | 10 | 5 | 1 | 1 | 2 | 1 | 5 | 2.48 | 1 | 10 of 25 (40%) |
| Including from recommendation | 1 | 6 | 4 | 0 | 2 | 2 | 10 | 4.72 | 4 | 1 of 25 (4%) |

The uncapped values, sorted, including findings classified from the recommendation: 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 5, 5, 6, 6, 6, 7, 7, 7, 10, 11, 11, 15. The values above 6 are 7 (three audits), 10, 11 (two audits) and 15.

When capped at 6, as the study design does, the mean is 2.12 counting observed fixes only, and 3.68 including the recommendations.

**The zeros in the observed row come from private fix repositories.** The 10 audits with zero observed V functions are exactly the 10 audits where no fix diff could be read. Their sponsor repositories are private, or no public fix exists. In the other 15 audits, every audit has at least one observed V function. Their observed counts are 6, 7, 10, 2, 6, 10, 1, 1, 3, 1, 4, 5, 1, 1 and 4 (mean 4.13). Only one audit has zero V functions when the recommendations are counted: Brix Money, with 3 findings.

**V functions per finding.** Across the 25 audits there are 62 observed V functions for 352 findings (0.176 per finding). Including the recommendations, there are 118 (0.335 per finding).

### Eligible functions and N functions per audit

| Count per audit | Min | First quartile | Median | Third quartile | Max | Mean |
|---|---|---|---|---|---|---|
| Functions with a body | 36 | 88 | 125 | 263 | 927 | 214.6 |
| Eligible in-scope functions | 25 | 71 | 105 | 194 | 696 | 158.6 |
| N functions | 24 | 53 | 92 | 177 | 672 | 144.8 |

| N functions | 0 to 49 | 50 to 99 | 100 to 199 | 200 to 399 | 400 or more |
|---|---|---|---|---|---|
| Audits | 6 | 7 | 7 | 4 | 1 |

N is never small. The smallest audit (Rova) still has 24 N functions. So N functions are not the limiting resource for the study.

### Fix classes of the 352 findings

| Class | Observed fix | From recommendation | Total |
|---|---|---|---|
| One function body | 74 | 63 | 137 |
| Several function bodies | 19 | 5 | 24 |
| Signature, storage or new declaration | 63 | 30 | 93 |
| Undetermined | | | 98 |
| **Total** | **156** | **98** | **352** |

- Among the 156 findings with an observed fix, 74 (47%) have a fix inside one function body. The pilot fix-scope study found 17 of 34 (50%).
- Among the 98 findings classified from the recommendation, 63 (64%) are one function body. Recommendations are narrower than the fixes developers actually write. So the count that includes recommendations probably overstates V.
- 334 of 352 findings (95%) were mapped to at least one function. The 352 findings name 357 distinct root-cause functions in total.

### Undetermined findings

- **98 of 352 findings (27.8%) are undetermined.** Per audit, the median share is 25% and the largest is 67%.
- The share depends on whether fixes were public. In the 15 audits where at least one fix diff was read, 43 of 221 findings (19.5%) are undetermined. In the other 10 audits, 55 of 131 (42%) are.
- By sponsor status, the undetermined findings are 38 with unknown status, 27 fixed (but the fix could not be read and the recommendation was not clear), 17 disputed and 16 acknowledged.

### Compared with the modelled numbers

The per-protocol inventory modelled V functions from the High and Medium count. Each finding gave a V function with probability 0.365, with a cap of 6. For 2025 audits with Solidity code, that model gave a mean of 2.17 and 22.9% of audits at zero.

- **Per finding.** The model's 0.365 V functions per finding sits close to the count that includes recommendations (0.335). It is about twice the observed-only count (0.176). The observed-only count is a lower bound, because 10 audits had no readable fixes.
- **Mean, capped at 6.** The census gives 2.12 (observed only) and 3.68 (including recommendations). The model's 2.17 lies between them.
- **Zeros.** The census has 4% of audits at zero when recommendations are counted, against the model's 22.9%. The observed-only 40% is caused by private fix repositories, as shown above. So the model probably overstates the share of audits with zero V functions. But the census holds only audits with at least one High or Medium finding, and the same was true for the model. Audits with no such finding would add zeros to both.

## Limitations

- **Small sample.** 25 audits. Shares have wide uncertainty. For example, 1 of 25 audits at zero has a Wilson 95% interval of about 0.7% to 20%.
- **Replacements are not random.** 8 of 33 drawn audits were replaced, 5 of them Cantina private reviews. Audits whose code is not public, or whose scope is unknown, are missing. They may differ from contests, for example by having fewer findings.
- **The frame is contests and competitions with dated links.** It comes from the per-protocol inventory: 2025 or later, Code4rena, Sherlock or Cantina, and at least one High or Medium finding. Private reviews from other firms are not in it.
- **Many fixes could not be read.** In 10 audits the sponsor repository is private or no fix was published. There, every class comes from the recommendation or is undetermined. The observed counts are therefore lower bounds. The counts that include recommendations probably lean high, because recommendations were classed as one function body more often (64%) than real fixes (47%).
- **"Observed fix" is not always the commit itself.** For Blackhole, the fix commits are private. The reader compared the audited code with the first public snapshot of the sponsor's code (11 July 2025) and separated the edits per finding. For Recall, the fixes come from the upstream project that Recall forked, partly on refactored code. For TermMax, the fix commits carry private competition numbers and were matched to findings by reading their diffs.
- **Judgment calls remain.** Some fixes sit in commits that also fix other findings. The reader then had to decide which edits belong to which finding. The notes in the per-finding table name the borderline cases. Examples: Notional H-2 and H-4 share one added line in an overloaded `price` function; Eco 52987 has a partial fix in a different function from the root cause; a Kinetiq V function (`StakingManager.sol::receive`) counts as not eligible under the counting rule, because its body is a single call.
- **Several readers.** The reading was split across eight agent sessions with one brief. I re-checked 6 random rows and harmonized one rule (header edits). I did not re-read all 352 findings. Readers may still differ in how strictly they read a recommendation as clear.
- **The eligibility rule is a pattern rule.** It treats every function that is not `view` or `pure` as writing state. It counts statements by semicolons. It counts any function with an `assembly` block. A compiler-based check could give somewhat different counts. The parser found no unbalanced files.
- **Scope edges.** For the two Cantina private reviews there is no scope list, so the whole `contracts/` folder was used. That may overstate their N. Some scope lists include interface files. Those have no function bodies, so they do not change the counts.
- **Function names.** A function is identified by file name plus function name, as in the inventory. Overloads in one file share one name.
- **Snapshot.** The findings come from the Solodit download that ended in April 2026. Sponsor repositories were read on 22 October 2026. Fixes published after that date, or deleted before it, are not seen.
