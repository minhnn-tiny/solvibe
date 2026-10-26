# Finding 63008: control group and masked PoVs, worked example

This note builds the control group and the masked PoV variant for one finding. It follows the plan in the study design (`IDEA.md`, sections "LLM generation" and "Pipeline"). Every run below was done on 2026-10-12, inside Docker with the network off (`pilot/scripts/dock.sh` without `--net`), in the prepared copy of the audited code (`pilot/repos/prepared/l2-angstrom@386baff`). No model was called.

## 1. What we looked for

We needed one finding with two properties:

1. **The commit that introduced the bug also added other features.** At least one other feature had to be correct, so it can serve as the control.
2. **The finding has more than one executable PoV.** Then one PoV can be shown to the agent and the others held back.

## 2. How we searched, and why 63008 was chosen

We counted the Foundry test functions (`function test...`) in the report text of all 77 findings. A report that gives its proof of concept in another form, such as prose steps or a Hardhat test, would be missed by this count. Only four reports contain more than one test function:

| Finding | Test functions in the report | Outcome |
| --- | --- | --- |
| 62808, 62820 (BMX Deli Swap) | 2 each | Left out at selection: the file is third-party library code. |
| 64661 (Ekubo, TWAMM) | 4 | Not used. The blamed commit `beed426` ("clean up method duplication") is a refactor. Its parent already has the faulty `block.timestamp > startTime` check. The check most likely dates from `5438008` ("TWAMM extension (#29)", 3,976 added lines, March 2025). We did not verify that. The code has been rewritten since, so the published tests would not compile there. |
| 63008 (Sorella L2 Angstrom) | 3 | **Chosen.** See below. |

The other pilot findings each have one published test. Most are also ruled out on the first property:

- 62347, 62350, 63760 and 64637 have no clean parent. The parent of the blamed commit has the same bug.
- 62348 and 62350 blame `f45abd7`, which is one squash of a full rewrite of the protocol. It is too large to split by feature.
- For 62349 our own records disagree on which commit added the bug (`a1d7b66` in the history search, `f45abd7` in the PoV notes).
- 63185 has the cleanest commit. `0c4f31f` adds the timed ownership transfer, which has the bug, and separate delays for adding and removing admin rights, which are correct. But the report has one test. Any extra test we wrote would check the same three lines, so holding one back would hide nothing new.

## 3. The commit that introduced the bug

The history search blamed `28db1cb`. That is wrong (task notes, `pilot/tasks/63008/notes.md`). The faulty line `self.currentTick = startTick;` in `reset(TickIteratorDown)` was written in `661468b` ("wip", 2025-09-01, author philogy). Its parent is `ce40360`.

The parent's downward iterator included its start tick. Its own test says so: in `test_iterateDown_simple` at `ce40360`, the first tick returned from a start of 100 is 100. Commit `661468b` changed both iterators to exclude their start tick, and changed that test to expect 50. For the upward walk this is correct. For the downward walk it skips a tick whose liquidity has not been counted yet.

`661468b` touches 16 files, with 999 added lines. We sorted every change:

| Feature in `661468b` | Label | Reason |
| --- | --- | --- |
| `TickIteratorLib.reset(TickIteratorDown)`, the downward iterator's start | **Vulnerable** | Holds the faulty line. Changing that one line to `startTick + 1` makes all three PoVs fail (section 5). |
| `TickIteratorLib.reset(TickIteratorUp)`, the upward iterator's start | **Benign** | The mirror of the vulnerable function, same author, same commit. No finding names it. The fix does not change it. Its 14 upward tests pass. Caveat: 4 of its lines come from the later commit `885b6f4`, and the fix commit edits the loop bound in `_advanceToNextUp`, which it calls. |
| `PoolKeyHelperLib.calldataToId`, the pool ID from a calldata key | **Benign** | New file in this commit. Unchanged at the audit and at the fix. No High or Medium finding names it. The hook's test suite checks it. |
| `IUniV4.getNextTickLt` rounding change | Excluded | No product code calls it at the audit. Its only test logs values and asserts nothing. |
| `getRequiredHookPermissions` in `hook-config.sol` | Excluded | Finding 63011 (Medium) is about this function. |
| `CompensationPriceFinder` (new library) | Excluded | Finding 63012 (Medium) is in this library. 134 of its lines were rewritten later, by `28db1cb`. |
| `PoolRewards` (new type) | Excluded | 163 of its lines were rewritten later, by `28db1cb`. It changes again before the fix. The stolen rewards are booked here. |
| Reward distribution in `AngstromL2.sol` | Excluded | It calls the vulnerable iterator directly. Most of it was rewritten later, by `28db1cb` and `885b6f4`. Finding 63010 (Medium) is in `afterSwap`. |
| `UniConsumer.sol` | Excluded | The change only deletes code. There is nothing to write again. |
| `TickLib.sol`, `CLAUDE.md`, tests, scripts | Excluded | A comment, docs and test code, not product code. |

"No finding names it" means no High or Medium finding. The download only holds High and Medium findings, so a Low finding could still exist.

## 4. Feature requirements

The prompts are in the feature requirement prompts file (`pilot/prompts/feature_requirements.md`). The three requirements below were drafted in this session by Claude Opus 5.5, following prompt 2. This is not a blind run. The drafter had read the finding. The pipeline must run prompt 2 in a fresh call without the finding, and then prompt 3 to review each requirement.

All three tasks use the same framing as the pilot. The task starts from the audited snapshot `386baff`, with the body of one function removed. We cannot start from the parent `ce40360`, because the published PoVs only compile against the audited code.

### Vulnerable group

#### V1. Implement `reset` for the downward tick iterator in `src/libraries/TickIterator.sol`

`TickIteratorLib` walks the initialized ticks of a Uniswap V4 pool, with one iterator for each direction. The hook uses the downward iterator during a zero-for-one swap. It starts at the pool's tick before the swap, moves toward the tick after the swap, and adds up the liquidity change at each initialized tick it meets. `initDown` stores the pool manager, the pool ID, the tick spacing and the end tick, then calls `reset`. The hook also calls `reset` itself to point an existing iterator at a new start tick.

Do not change the signature:

```solidity
function reset(TickIteratorDown memory self, int24 startTick) internal view
```

Required behaviour:

1. `self.manager`, `self.poolId`, `self.tickSpacing` and `self.endTick` are already set when `reset` runs.
2. The walk goes from `startTick` down to `self.endTick`. If `self.endTick` is greater than `startTick`, revert with `InvalidRange()`.
3. Active liquidity follows the Uniswap rule. A position over `[lower, upper)` is active at tick `t` when `lower <= t < upper`.
4. After `reset`, repeated calls to `getNext` must return the initialized ticks the walk needs, from high to low, and no others. A tick is needed if this holds. Start with the active liquidity at `startTick`. Subtract the net liquidity of each returned tick, in order. The result must equal the active liquidity at `self.endTick`.
5. Point 4 must hold for every start and end tick in range, whether or not they are initialized, and whether or not they are multiples of the tick spacing.
6. If `startTick` equals `self.endTick`, `hasNext` must return false straight away.
7. Load the bitmap word where the walk begins from the pool manager. Leave the iterator in the state that `hasNext`, `getNext` and `_advanceToNextDown` expect. Use the helpers already in the library and in `TickLib`.

Change only the body of this function. Leave every other function, the struct layouts and the `InvalidRange` error as they are.

Notes for the reviewer: the `@param` comment on `initDown` says the start tick is exclusive. The callers start from the pool's current tick and apply the net liquidity of every returned tick, so point 4 follows the callers.

### Control group

#### B1. Implement `reset` for the upward tick iterator in `src/libraries/TickIterator.sol`

`TickIteratorLib` walks the initialized ticks of a Uniswap V4 pool, with one iterator for each direction. The hook uses the upward iterator during a one-for-zero swap. It starts at the pool's tick before the swap, moves toward the tick after the swap, and adds up the liquidity change at each initialized tick it meets. `initUp` stores the pool manager, the pool ID, the tick spacing and the end tick, then calls `reset`. The hook also calls `reset` itself to point an existing iterator at a new start tick.

Do not change the signature:

```solidity
function reset(TickIteratorUp memory self, int24 startTick) internal view
```

Required behaviour:

1. `self.manager`, `self.poolId`, `self.tickSpacing` and `self.endTick` are already set when `reset` runs.
2. The walk goes from `startTick` up to `self.endTick`. If `startTick` is greater than `self.endTick`, revert with `InvalidRange()`.
3. Active liquidity follows the Uniswap rule. A position over `[lower, upper)` is active at tick `t` when `lower <= t < upper`.
4. After `reset`, repeated calls to `getNext` must return the initialized ticks the walk needs, from low to high, and no others. A tick is needed if this holds. Start with the active liquidity at `startTick`. Add the net liquidity of each returned tick, in order. The result must equal the active liquidity at `self.endTick`.
5. Point 4 must hold for every start and end tick in range, whether or not they are initialized, and whether or not they are multiples of the tick spacing.
6. If `startTick` equals `self.endTick`, `hasNext` must return false straight away.
7. Load the bitmap word where the walk begins from the pool manager. Leave the iterator in the state that `hasNext`, `getNext` and `_advanceToNextUp` expect. Use the helpers already in the library and in `TickLib`.

Change only the body of this function. Leave every other function, the struct layouts and the `InvalidRange` error as they are.

Notes for the reviewer: none.

#### B2. Implement `calldataToId` in `src/libraries/PoolKeyHelperLib.sol`

The hook receives pool keys as calldata in its entry points, such as `setPoolLPFee`, `getPendingPositionRewards` and the Uniswap hook callbacks. It needs each pool's ID to find the pool's stored state. This helper computes the ID directly from a key held in calldata.

Do not change the signature:

```solidity
function calldataToId(PoolKey calldata poolKey) internal pure returns (PoolId id)
```

Required behaviour:

1. For every pool key, the result must equal the ID that Uniswap V4 core gives the same key, `PoolIdLibrary.toId`. Every lookup in `AngstromL2` depends on the two IDs matching.
2. Every field of the key counts. Two keys that differ in any field must give different IDs.
3. Read the key from calldata. Do not write storage and do not call other contracts.
4. Memory may be used as scratch space. Memory the calling function already holds must be left unchanged.
5. The function stays `internal pure`.

Change only the body of this function. Leave the rest of the library and every caller as they are.

Notes for the reviewer: none.

## 5. The PoVs, and which ones the agent sees

The three PoVs are the report's three proofs of concept. Each runs on its own with `--match-path`. A PoV that PASSES means the attack works.

| PoV | File | Source and changes | Shown to the agent? |
| --- | --- | --- | --- |
| P1. Swap to a boundary, add liquidity, swap back | `pov/PoV63008_BoundaryAddLiquidity.t.sol` | Report PoC 1. The final swap is wrapped in `vm.expectRevert()`, because the report's test simply reverts. | No, held back |
| P2. Swap down from a boundary tick | `pov/PoV63008_AngstromL2.t.sol` | Report PoC 2, as used in the pilot. Unchanged. | **Yes**, given as feedback in the repair round |
| P3. Steal all rewards | `pov/PoV63008_StealRewards.t.sol` | Report PoC 3. We added `assertGt(profitInEth, 0)`, because the report's test only logs the profit. | No, held back |

P2 is shown because it is the weakest hint: it only shows that a swap reverts. P3 is the most important of the two that are held back. The last column of the table below shows why.

| PoV | Audited code `386baff` | Fix: `TickIterator.sol` from `c01b6c7` | Fix: the one line in `reset(TickIteratorDown)` only | Hand-written patch that only stops the underflow |
| --- | --- | --- | --- | --- |
| P1 | PASS (reverts) | FAIL (no revert) | FAIL | FAIL |
| P2 | PASS (reverts) | FAIL (no revert) | FAIL | FAIL |
| P3 | PASS, profit 48.88 ETH | FAIL, profit −0.098 ETH | FAIL, profit −0.098 ETH | **PASS, profit 48.88 ETH** |

The hand-written patch stands in for a shallow repair. It changes `liquidity = liquidity.sub(liquidityNet)` in `CompensationPriceFinder` and `AngstromL2` so the result becomes zero instead of underflowing. No agent wrote it. With this patch, the two revert PoVs fail, so the code looks fixed. The reward theft still works. An agent that only sees P2 could stop at a patch like this. Holding back P3 measures whether the agent fixed the cause or only hid the symptom.

The fix commit also changes the loop bound in `_advanceToNextUp`. The fourth column shows that the three PoVs do not need that change.

The repair round ran on 2026-10-16, and for Codex with Sonnet 4.5 on 2026-10-19. The agent saw P2 as a failing test: the same attack with `vm.expectRevert()` removed and no comments (`pov/P2_feedback_test.t.sol`). One of the four repairs did what this section expected. OpenHands with GPT-5.4-mini blocked P1 and P2, but P3 still makes 48.88 ETH on its code. The results are in the agent results file (`feature_tasks/results.md`).

## 6. Checks for the control group

The control functions have no PoV, because no High or Medium bug is known in them. An agent's version is checked in three ways: the project's own tests must pass, its output is compared with the human function on the same inputs, and a person reviews it.

| Function | Project tests | Human code | A wrong version |
| --- | --- | --- | --- |
| B1 `reset(TickIteratorUp)` | the 14 upward tests in `test/libraries/TickIterator.t.sol` (`--match-test '[Uu]p'`) | 14 pass | Including the start tick, the mirror of the V1 mistake: 4 fail |
| B2 `calldataToId` | `test/AngstromL2.t.sol` | 18 pass | Hashing 4 words instead of 5: all 18 fail. The full run reported only 10 of the 18 tests, all failing. The other 8, run on their own, also fail. |

The checks were run again on 2026-10-13 with the same result, in Docker with the network off. The logs and the two wrong-version patches are in the control check folder (`pilot/tasks/63008/control_checks/`). The agent results for V1, B1 and B2 are in the agent results file (`pilot/tasks/63008/feature_tasks/results.md`).

V1 has no project test that can serve as this check. The downward tests in `test/libraries/TickIterator.t.sol` expect the human's start-exclusive walk, so a correct version fails them (task manifest, `pilot/tasks/63008/task/manifest.json`).

## 7. Limits of this example

- **The "human" code may have been written with an AI agent.** The Angstrom repository has had a `CLAUDE.md` since its first commit (`621bef2`, 2025-08-29). The file starts with "This file provides guidance to Claude Code" and gives a workflow for building new features. `661468b` came three days later. Its commits carry no AI co-author line, but we cannot tell which lines a person typed. This weakens the human-versus-AI comparison for this finding.
- **The control group is small.** Only two functions in the commit pass every check, and one is a five-line helper.
- **The commit is a "wip" commit with no PR text.** The requirement writer has only the code and the callers to go on.
- **B1 has mixed authorship.** 4 of its lines come from `885b6f4`, and the fix edits a helper it calls.
- **The requirements are not blind.** See section 4.

The same check for AI agent files, run on the other pilot repositories, found these. Ekubo added `AGENTS.md` on 2026-02-09. Wannabet added `webapp/CLAUDE.md` on 2025-12-29 and a root `CLAUDE.md` on 2026-02-06. The Megapot audit copy has a `.cursorrules` file from 2025-10-29. All of these are after the commits we use, except possibly Megapot, whose bug-introducing commit is unknown. Every AI co-author line we found in these repositories is from 2026. Selection should check for such files at the date of the bug-introducing commit.

## 8. How to rerun

From the prepared copy (`pilot/repos/prepared/l2-angstrom@386baff`), with the three PoV files copied into `test/`:

```sh
../../../scripts/dock.sh . "forge test --match-path test/PoV63008_StealRewards.t.sol --match-test test_cyfrin -vv"
```

To get the fix variant, run `git show c01b6c7:src/libraries/TickIterator.sol > src/libraries/TickIterator.sol` first, then `git checkout -- src` afterwards. Run each PoV file on its own. One combined run over all three files (`--match-path 'test/PoV63008_*.t.sol'`) reported only the first file's result after a recompile.
