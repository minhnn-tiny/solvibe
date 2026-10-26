# Strict V and N counts for the 25 audits in the random sample

The frame audit one folder up (`../README.md`) counted V and N functions in 25 randomly drawn 2025 contest audits. A peer reviewer said those counts must be reconciled with the proposal's strict eligibility rules before they can serve as a sampling frame. The reviewer named three problems:

- **(a)** Some V counts rest on fixes that were classified only from the auditor's recommendation.
- **(b)** The one-function-body class allowed some changes outside the body, such as a new custom error.
- **(c)** Functions were identified by file name plus function name, so overloaded functions shared one name.

This folder recounts V and N under the proposal's rules. It does not change any file one folder up.

The proposal's rules used here come from `../../../proposal_v17.md`, sections *Attribution* and *5.1 Frame and sampling unit*:

- A function is identified by repository, snapshot, full file path, enclosing contract and signature. Overloads are distinct.
- A counted correction changes only the target function's body. "A new declaration outside the body is not permitted, even if it is an error or event used only by the correction."
- Unrelated edits in a fix commit do not show that a broader correction is needed.
- The same eligibility rule applies to V and N.
- N contains eligible functions with no link to a High or Medium finding.

## Files

- The counting script (`strict_counts.py`). It re-parses the in-scope files, gives each function a unique identity, reads the hand re-read of fix scope, and writes the two count tables. It prints every number in this file. It has a self-test (`--selftest`).
- The hand re-read of fix scope (`fix_reread.csv`). This is the script's input. One row for each of the 137 findings that the original audit put in the one-function-body class: 74 with an observed fix and 63 classified from the recommendation. Columns:
  - `slug`, `finding_id`, `evidence` (copied from the per-finding table one folder up).
  - `fix_read_now`: `yes` when the fix diff was read again for this recount, or `recommendation`.
  - `fix_source`: the commit, pull request merge or snapshot that was read, or "recommendation in finding text".
  - `target_identity`: the unique identity of the function whose body the fix (or recommendation) changes.
  - `outside_body_changes`: `none`, or a list from: new error or event, import, new or removed function, header of the changed function, other declaration, storage layout.
  - `other_bodies_changed`: `none`, or the other functions whose bodies the fix for this finding changes.
  - `strict_one_body`: `yes` when the change stays inside one body.
  - `note`: the reason in plain words, including every close call.
- The function list (`per_function_strict.csv`). One row for each of the 5,364 functions with a body in the in-scope files. Main columns:
  - `identity`: full path, contract or library, function name and parameter types, for example `src/Voter.sol::Voter.vote(uint8,bool)`.
  - `function_key`: the old name (`File.sol::name`), as used one folder up.
  - `name_shared`: `True` when the old name stands for two or more functions.
  - `eligible` and `reason`: the counting rule, unchanged from `../count_functions.py`.
  - `eligible_without_assembly_rule`: the same rule without its assembly exception (see *Strict N*).
  - `linked_findings`: the High and Medium findings that link to this function.
  - `strict_v_observed_findings` and `strict_v_recommendation_findings`: the findings that make this function a strict V function.
  - `in_strict_n`: `True` when the function counts in strict N.
- The per-audit table (`per_audit_strict.csv`). One row for each of the 25 processed audits. Main columns: `name_collisions`, `functions_sharing_a_name`, `eligible_functions`, `linked_eligible_functions`, `strict_n`, `strict_n_without_assembly_rule`, `original_n`, `findings_fix_not_read`, `findings_fix_not_read_fixed_status`, `findings_one_body_observed`, `findings_strict_observed`, `findings_strict_recommendation`, `strict_v_observed`, `strict_v_upper_bound`, `original_v_observed`, `original_v_incl_recommendation`.
- This file (`README.md`).

## How to reproduce

```bash
cd /Users/minh/Documents/workspaces/secure-solvibe
python3.12 -I proposal_workspace/evidence/frame_audit/strict/strict_counts.py --selftest
python3.12 -I proposal_workspace/evidence/frame_audit/strict/strict_counts.py --work /Users/minh/.claude/jobs/eeaa430c/tmp/frame_audit
```

The script uses the standard library only. It imports the original counting rule from `../count_functions.py`. It reads the clones in the work folder of the original audit, which is a temporary folder. To rerun it elsewhere, clone each repository at the commit in `../scope_files.csv` into `<work>/<slug>/repo`.

## Method

### Step 1. Unique function identities

The script parses every in-scope file again with the same parser as the original count. It also finds each `contract`, `abstract contract`, `library` and `interface` block and its braces. Each function gets the innermost block that contains it. Two functions sit outside any block (file-level functions in Superfluid's `FluidLocker.sol`). Their contract is written as `(file level)`.

The parameter types come from the function header. The script drops parameter names and the data location words (`memory`, `storage`, `calldata`). It writes `uint` as `uint256` and `int` as `int256`.

The identity is the full path, the contract, the name and the type list. The script checks three things:

- The re-parse finds exactly the same 5,364 functions, in the same order, with the same eligibility, as the original function list (`../functions_in_scope.csv`).
- No two functions in one audit share an identity.
- Every function named in the re-read file exists in the list.

### Step 2. Strict V from observed fixes

A function is a strict V function when all of these hold:

1. It is a root-cause function of a High or Medium finding.
2. The developers' fix for that finding was read as a diff.
3. The fix changes only that function's body. There is no signature, visibility, modifier or other header change. There is no new error, event, constant, state variable, struct, modifier, `using` directive or import. No function is added or removed. No other function's body changes, except for formatting or comments.
4. The function is eligible under the counting rule.

Edits in the same commit that belong to other findings were ignored, as the proposal says. Tests, scripts, comments and formatting were ignored too. Using an existing error, event, constant or function is allowed. So is a new local variable inside the body.

All 74 findings that the original audit classed as one function body with an observed fix were read again. The fix diffs were read offline from the local clones, with git's network access switched off. All 74 diffs could be read. One commit's own blob was missing, so its pull request merge diff was read instead (BMX Deli Swap finding 62817).

The rows in the other classes were not read again. They already fail the one-body test, and a stricter rule cannot move them into it.

A function counts once per audit, however many findings name it.

### Step 3. Strict V upper bound

The upper bound adds the 63 findings that the original audit classed as one function body from the finding's recommendation. Each recommendation was read again under the same rule as in Step 2:

- A recommended `revert NewError()` with an error that does not exist in the audited code is a new declaration.
- A recommendation in prose that only says "add a check" or "revert", without naming a new declaration, does not count as one.
- When a recommendation offers alternatives, the first or main one was used.

The root-cause test and the eligibility test also apply. The result is labelled an upper bound. Recommendations are narrower than real fixes, and several of them are prose without code.

### Step 4. Strict N

Strict N is the number of eligible in-scope functions, counted by unique identity, minus every function linked to any High or Medium finding of the audit. A function is linked when it is one of these:

- a root-cause function of the finding, whatever its fix class;
- the function whose body a one-body fix or recommendation changes;
- another function whose body the re-read fix changes.

So no function that a High or Medium finding names stays in N.

The eligibility rule is the original counting rule (`../count_functions.py`):

- a function that is not `view` or `pure` counts as writing state, unless its body is empty or is a single-call forwarding wrapper;
- a `view` or `pure` function counts when it has more than one statement or any branch;
- declarations without a body (interfaces, abstract functions) are skipped.

The original rule has one extra clause: any function with an `assembly` block is eligible. It is there because the parser counts statements by semicolons, and assembly code has none. The proposal's rule does not mention assembly. So the tables also give N without that clause, applied to `view` and `pure` functions only.

Seven root-cause names stand for two or more functions. Each was resolved by reading the finding's line link and text. The script lists them in `ROOT_RESOLVE`:

| Audit | Finding | Old name | Resolved to |
|---|---|---|---|
| Blackhole | 58351 | `Governor.sol::_castVote` | the five-parameter overload (line link L534 to L554) |
| DODO Cross-Chain DEX | 58593 | `GatewaySend.sol::depositAndCall` | both overloads. The link names the first. The second has the same raw `transferFrom`, and the fix changed both. |
| Notional Exponent | 62485 | `AbstractYieldStrategy.sol::price` | `price()` with no arguments (line link L118 to L120) |
| Notional Exponent | 62515 | `CurveConvex2Token.sol::TOKENS` | both copies. The link names `CurveConvexLib.TOKENS()`. The vault's `CurveConvex2Token.TOKENS()` is identical. |
| Notional Exponent | 62516 | `CurveConvex2Token.sol::constructor` | the `CurveConvexLib` constructor |
| Kinetiq | 58559 | `StakingManager.sol::processL1Operations` | `processL1Operations(uint256)` (line link L627 to L666) |
| Recall | 65100 | `LibStaking.sol::confirmChange` | `LibStaking.confirmChange(uint64)` (line link L584) |

### Which findings qualify

Every High and Medium finding in the downloaded data counts as qualifying. The proposal's own severity rubric was not applied. See *Limitations*.

### Who did the reading

Five Claude agent sessions did the re-read in parallel. Each had 4 to 9 audits and one written brief with the rules above. They used only read-only git commands, with network access switched off. They ran no code from the repositories. Two of them said they wrote temporary helper files to `/tmp` and deleted them.

I then merged their rows and checked them:

- The script asserts that the re-read file has exactly the 137 one-body findings, and that every target identity exists.
- It asserts that a row marked `yes` lists no outside change.
- I re-read three close calls myself against the diff: Malda 62733, Recall 65092 and Morpheus 62532. I agreed with all three.
- I checked the new files against the 939 finder handles of these findings. Only the ordinary word "Constant" matches, in a code note.

## Results

### Per audit

"No fix read" counts findings for which no fix diff was read, either in the original audit or in this recount. "Collisions" counts old names (`File.sol::name`) that stood for two or more functions with a body.

| Rank | Audit | H/M findings | No fix read | V observed (original) | Strict V observed | V incl. recommendation (original) | Strict V upper bound | N (original) | Strict N | Collisions resolved |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Sherlock contest 1154, BMX Deli Swap (2025-09) | 14 | 1 | 6 | 5 | 6 | 5 | 177 | 177 | 5 |
| 2 | Code4rena contest 539, Brix Money (2025-11) | 3 | 3 | 0 | 0 | 0 | 0 | 108 | 108 | 0 |
| 3 | Code4rena contest 487, IQ AI (2025-01) | 4 | 4 | 0 | 0 | 2 | 2 | 49 | 49 | 4 |
| 4 | Cantina competition, Term Structure (2025-02) | 18 | 0 | 7 | 6 | 7 | 6 | 123 | 123 | 3 |
| 5 | Code4rena contest 513, GTE (2025-08) | 35 | 35 | 0 | 0 | 11 | 11 | 327 | 327 | 6 |
| 6 | Code4rena contest 507, Blackhole (2025-05) | 24 | 4 | 10 | 9 | 10 | 9 | 672 | 672 | 12 |
| 7 | Sherlock contest 968, Superfluid Locker System (2025-06) | 8 | 3 | 2 | 2 | 2 | 2 | 139 | 139 | 24 |
| 9 | Sherlock contest 991, DODO Cross-Chain DEX (2025-05) | 17 | 2 | 6 | 6 | 6 | 6 | 63 | 62 | 1 |
| 10 | Sherlock contest 749, Peapods (2025-01) | 41 | 27 | 10 | 10 | 15 | 15 | 381 | 381 | 9 |
| 11 | Code4rena contest 526, Hybra Finance (2025-10) | 10 | 10 | 0 | 0 | 5 | 5 | 246 | 246 | 7 |
| 13 | Cantina competition, DefiApp (2025-02) | 10 | 10 | 0 | 0 | 6 | 6 | 161 | 161 | 0 |
| 15 | Sherlock contest 799, Aegis.im YUSD (2025-04) | 3 | 2 | 1 | 1 | 1 | 1 | 67 | 67 | 1 |
| 16 | Cantina private review, Olas (2025-01) | 10 | 3 | 1 | 1 | 2 | 2 | 70 | 70 | 0 |
| 17 | Sherlock contest 1051, Allbridge Core Yield (2025-07) | 2 | 2 | 0 | 0 | 1 | 1 | 46 | 46 | 0 |
| 20 | Sherlock contest 1029, Malda (2025-07) | 17 | 2 | 3 | 3 | 4 | 4 | 183 | 183 | 1 |
| 21 | Sherlock contest 977, Yearn yBOLD (2025-05) | 3 | 3 | 0 | 0 | 1 | 1 | 39 | 39 | 1 |
| 23 | Sherlock contest 791, Yieldoor (2025-02) | 17 | 17 | 0 | 0 | 7 | 7 | 92 | 92 | 3 |
| 25 | Code4rena contest 520, Morpheus (2025-08) | 4 | 0 | 1 | 1 | 1 | 1 | 67 | 67 | 0 |
| 26 | Cantina private review, Eco Inc (2025-02) | 10 | 1 | 4 | 1 | 4 | 1 | 38 | 38 | 0 |
| 28 | Sherlock contest 1001, Notional Exponent (2025-06) | 37 | 15 | 5 | 4 | 7 | 6 | 158 | 158 | 5 |
| 29 | Code4rena contest 502, Kinetiq (2025-04) | 8 | 8 | 0 | 0 | 2 | 1 | 73 | 73 | 1 |
| 30 | Sherlock contest 952, LayerEdge Staking (2025-05) | 3 | 1 | 1 | 1 | 1 | 1 | 32 | 32 | 0 |
| 31 | Sherlock contest 498, Rova (2025-02) | 2 | 0 | 1 | 1 | 1 | 1 | 24 | 24 | 0 |
| 32 | Sherlock contest 908, LEND (2025-05) | 39 | 39 | 0 | 0 | 11 | 11 | 53 | 53 | 0 |
| 33 | Code4rena contest 489, Recall (2025-02) | 13 | 4 | 4 | 3 | 5 | 4 | 233 | 233 | 11 |
| | **Total** | **352** | **196** | **62** | **54** | **118** | **109** | **3,621** | **3,620** | **94** |

Lists in the sample order above:

- Strict V observed: `[5, 0, 0, 6, 0, 9, 2, 6, 10, 0, 0, 1, 1, 0, 3, 0, 0, 1, 1, 4, 0, 1, 1, 0, 3]`
- Strict V upper bound: `[5, 0, 2, 6, 11, 9, 2, 6, 15, 5, 6, 1, 2, 1, 4, 1, 7, 1, 1, 6, 1, 1, 1, 11, 4]`
- Strict N: `[177, 108, 49, 123, 327, 672, 139, 62, 381, 246, 161, 67, 70, 46, 183, 39, 92, 67, 38, 158, 73, 32, 24, 53, 233]`

### Strict V per audit, uncapped

| Strict V count | 0 | 1 | 2 | 3 | 4 | 5 | 6 or more | Mean | Median | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| Observed fixes | 10 | 6 | 1 | 2 | 1 | 1 | 4 | 2.16 | 1 | 54 |
| Upper bound (observed plus recommendation) | 1 | 8 | 3 | 0 | 2 | 2 | 9 | 4.36 | 4 | 109 |

- Sorted, observed: 0 (ten audits), 1 (six audits), 2, 3, 3, 4, 5, 6, 6, 9, 10.
- Sorted, upper bound: 0, 1 (eight audits), 2, 2, 2, 4, 4, 5, 5, 6, 6, 6, 6, 7, 9, 11, 11, 15.
- Capped at 6, as the study design does, the mean is 1.88 (observed) and 3.44 (upper bound).
- Per finding, there are 54 strict V functions for 352 findings (0.153) from observed fixes, and 109 (0.310) for the upper bound.
- The 10 audits with zero observed strict V functions are the same 10 audits where no fix diff could be read at all. In the other 15 audits, every audit has at least one. Their counts are 5, 6, 9, 2, 6, 10, 1, 1, 3, 1, 1, 4, 1, 1 and 3 (mean 3.60).
- Blackhole's 9 observed strict V functions rest on a comparison with a public snapshot, not on the fix commits. See *Limitations*.

### Strict N per audit

| Count per audit | Min | First quartile | Median | Third quartile | Max | Mean | Total |
|---|---|---|---|---|---|---|---|
| Strict N | 24 | 53 | 92 | 177 | 672 | 144.8 | 3,620 |
| Strict N without the assembly clause | 24 | 53 | 92 | 177 | 672 | 143.2 | 3,581 |
| Original N | 24 | 53 | 92 | 177 | 672 | 144.8 | 3,621 |
| Eligible functions | 25 | 71 | 105 | 194 | 696 | 158.6 | 3,965 |

The quartiles use Python's `statistics.quantiles` with the inclusive method, as in the original audit.

### Name collisions resolved

- 94 old names stood for two or more functions with a body. Together they hold 198 functions.
- 80 of the 94 are overloads in one contract.
- 12 are the same name in different contracts of one file. They are the constructors in Blackhole's `Governor.sol`, `TOKENS` and the constructor in Notional's `CurveConvex2Token.sol`, the constructor in Notional's `Ethena.sol`, and eight names in Recall's `LibStaking.sol`, a file that holds two libraries.
- 2 are the same file name in different folders: Peapods has two copies of `VaultAccount.sol` in scope.
- In 55 of the 94, two or more of the functions are eligible.
- Per audit, from the table: Superfluid 24, Blackhole 12, Recall 11, Peapods 9, Hybra 7, GTE 6, BMX Deli Swap 5, Notional 5, IQ AI 4, Term Structure 3, Yieldoor 3, and 1 each in DODO, Aegis, Malda, yBOLD and Kinetiq. Nine audits have none.
- 7 of the 94 names are root-cause names of a finding. They are resolved in the table under *Step 4*.

### What changed relative to the original counts, and why

**Strict V observed falls from 62 to 54 functions.** Of the 74 one-body findings with an observed fix, 65 pass and 9 fail:

| Reason | Findings | Audit and function |
|---|---|---|
| The fix declares a new custom error | 4 | Term Structure 54894 (`borrowTokenFromGt`, error `GtNotOwnedBySender`); Eco 52982 (`_fulfill`, error `WrongChain`); Eco 52984 (`fill`, error `FillDeadlinePassed`); Recall 65088 (`validateActiveQuorumSignatures`, two errors and a changed import line) |
| The fix adds an import | 1 | Blackhole 58337 (`createEternalFarming`, import of `IERC20Metadata`) |
| The fixed function is not a root cause of the finding | 3 | BMX Deli Swap 62811 (fix in `vote`, root cause `_tallyAutoVotes`); Eco 52987 (fix in `_openEcoIntent`, root cause `_verifyOpenFor`, and the fix is partial); Notional 62483 (fix in `price()`, root causes `initiateWithdraw`, `_withdraw` and `effectiveSupply`) |
| The fixed function is not eligible | 2 | Notional 62483 and 62485. Both fixes add a line to `price()` with no arguments. In the audited code that function is a one-statement view. The original count merged it with the eligible `price(address)`. |

Notional 62483 fails two tests. Eight distinct functions leave the observed count. Per audit: BMX Deli Swap 6 to 5, Term Structure 7 to 6, Blackhole 10 to 9, Eco 4 to 1, Notional 5 to 4 and Recall 4 to 3.

So problem (b) removes 5 findings, those with a new error or an import. Problem (c) removes 2, through the `price()` overload. The root-cause test removes 3 more. The original audit allowed a fixed function that differs from the root cause. The task rule here does not.

**The strict V upper bound falls from 118 to 109 functions.** It loses the same 8 functions. It also loses one more from the recommendations. Of the 63 one-body findings from a recommendation, 61 pass and 2 fail:

- Peapods 52777: the change to `_calculateSpTknPerBase` also needs a change in `getPrices`, which the finding marks. Its function still counts through Peapods 52750, so the Peapods count does not change.
- Kinetiq 58555: the recommended change is in `receive()`, which is a single-call body and not eligible. Kinetiq goes from 2 to 1.

**Strict N falls by one function in total.** Only DODO changes, from 63 to 62. Its finding 58593 names one of two `depositAndCall` overloads. The other has the same flaw, so both now leave N. In Notional two changes cancel out. `price(address)` returns to N, because the findings point at `price()`. The vault's copy of `TOKENS()` leaves N, because it is identical to the linked library copy.

N hardly moves because the original count already counted each overload as its own eligible function. Only the subtraction step used names, and only 7 linked names collide. For four of the seven, the strict count removes the same number of eligible functions as the original count did. The other three are the DODO and Notional cases just described.

**Findings with no fix read stay at 196 of 352.** These are the 98 findings classed from a recommendation and the 98 undetermined ones. The recount could read every one of the 74 observed one-body fixes again, so none was added. 71 of the 196 are marked fixed by the sponsor, but the fix was private or could not be found. LEND alone has 39 of them.

### Close calls that still pass

These observed fixes pass, but a stricter reader could fail them. The notes in `fix_reread.csv` explain each one.

- BMX Deli Swap 62821: the linked fix (pull request 24) changes only `_beforeSwap`, but it was never merged. The code that reached the main branch came through a broader rework and a later review commit.
- Term Structure 54903: the same commit renames one parameter of another function, with the same types.
- Aegis 56707: the same commit also edits `mint`, a modifier and an oracle check. The reader judged those to be fixes for other issues.
- Morpheus 62532: the net fix of two commits changes only `distributeRewards`. The first attempt added a function, and the second commit took it out again.
- Notional 62496: the fix renames a parameter of `_liquidate` without changing its type or position.
- Malda 62733: the same pull request rewrites how fee parameters are decoded and adds a function for it. That concerns a different problem from this finding's `maxFee` and `ttl`.
- Peapods 52780: the fix was made after a refactor that split `callback` into two functions. It edits the new `_callback`, which holds the audited body of `callback`.
- Peapods 52747: the same commit makes the same change in another factory, which this finding does not name.

16 of the 61 recommendation rows that pass are also marked as close calls. Most are prose recommendations with no code. For example, LEND 58392 says to rewrite one condition but does not give the new condition. LEND 58382 stays in one body, but the recommended change may have no effect, because it reads a memory copy.

## Limitations

- **The rest of the original audit's limits still hold.** These include the small sample, the replaced audits, the frame and the snapshot dates. See `../README.md`.
- **Qualifying findings.** Every High and Medium finding counts. The proposal's own severity rubric was not applied, and it would exclude some findings, for example privileged misuse. That would remove some V functions and return some functions to N.
- **Blackhole's fixes are a snapshot comparison.** Its fix commits are private. Its 9 strict V functions come from comparing the audited code with the first public snapshot (commit 0aa8e51). A snapshot cannot show which edits belong to which finding. Without Blackhole, the observed total is 45.
- **Recall's fixes come from the upstream project.** Recall forked that project. Its 3 strict V functions rest on upstream commits, partly made on refactored code.
- **Other fixes are not all on the audited code.** Peapods 52780 was fixed on refactored code, and BMX Deli Swap 62821 on a branch that was never merged.
- **The other fix classes were not read again.** The 24 several-body and 93 signature or declaration findings keep the original class. A stricter rule cannot move them into the one-body class. But functions that those fixes changed, and that are not root causes, stay in N. The per-finding table records only root causes and one-body targets, not every function such a fix touched.
- **Findings with no root-cause function.** 18 findings have a root cause outside any function: a constant, a state variable, a missing function or a design issue. Any function they affect stays in N. The proposal says such functions must not be put in N silently, so these findings need a decision before the frame is frozen.
- **The upper bound is not a proven upper bound.** The 98 undetermined findings may hide more one-body fixes. And recommendations can be narrower than the correction that is really needed.
- **"Writes state" is not checked.** The counting rule treats every function that is not `view` or `pure` as writing state. A compiler-based check could give somewhat lower N.
- **The parser is a pattern parser, not a compiler.** It found the same functions as the original count, and no two functions share an identity. Parameter types are written as in the source, after dropping names and data locations. So they can differ in form from the compiler's signature, for example for struct and contract types.
- **Several readers.** Five agent sessions did the re-read with one brief. I re-checked three close calls, not all 137 rows. Readers may differ on prose recommendations most of all.
