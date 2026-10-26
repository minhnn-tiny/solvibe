# Audit-blind rediscovery check: review bundles and sealed answer keys

This folder holds the inputs for one check. LLM security reviewers read the vulnerable version of a function and its nearby code, with no audit material. Later, a judge compares what each reviewer reports with the audit finding.

## Rule for reviewers

Reviewers may read only the `bundles/` folder. They must never read `sealed_key/`, and they must not read this README either, because it names the snapshot commits.

## What is here

- The review bundles (`bundles/<id>/`). One folder per finding. Each holds:
  - the full file that contains the target function, at the vulnerable snapshot (`target.sol`);
  - up to six other Solidity files from the same snapshot that the target file imports directly (`context/`, kept at their repository paths);
  - the review task: protocol, file path in the repository, function name, signature, line range in `target.sol`, and one sentence asking for a review (`task.md`);
  - the list of lines changed for blind review (`redactions.md`).
- The sealed answer keys (`sealed_key/<id>.md`). One file per finding, for the judge only. Each holds the finding id, protocol, severity, title, the finding text with its source path, the fix commit, and the diff of the target function.

## How the bundles were built

1. The list of findings is the 17 rows of the fix-scope table (`proposal_workspace/evidence/frame_count/fix_scope_by_finding.csv`) whose *classification* column is `one function body`. That table also gives the repository, the fix commit and the changed function.
2. All work used the local clones in `pilot/repos/` and read-only git commands (`git rev-parse`, `git show`, `git ls-tree`, `git log`). Nothing in the clones was changed. No network was used.
3. The vulnerable snapshot is the parent of the fix commit. Finding 64662 has two fix commits in a row (`7114e34`, then `ab4c93d`). Its snapshot is the parent of the first one.
4. `target.sol` is the whole file at the snapshot.
5. Context files. I read every import statement in the target file and resolved it with the repository's remappings (`remappings.txt` or `foundry.toml`). Imports that resolve into `lib/`, `node_modules/` or `dependencies/` are third-party code and were skipped. When more than six files were left, I kept the six whose imported names appear most often in the target function's body. Ties were broken by import order. This rule does not look at the finding.
6. The line range runs from the line with the `function` keyword to the function's closing brace. The doc comment above the function is not included in the range, but it is in the file.

The scripts are in the scratch folder of this job (`build.py`, `scan.py`, `finish_bundles.py`, `sealed_keys.py`, `readme.py`). They are not part of the evidence.

## Bundles built (17)

| Id | Protocol | Function | File in the repository | Lines in target.sol | Snapshot commit | Context files |
|---|---|---|---|---|---|---|
| 62348 | Licredity | `PositionLibrary.removeFungible` | `src/types/Position.sol` | 75 to 114 | `0d54fae86c` | 3 |
| 62350 | Licredity | `Licredity.decreaseDebtShare` | `src/Licredity.sol` | 490 to 557 | `30fc63c860` | 6 |
| 63008 | Sorella L2 Angstrom | `TickIteratorLib.reset` | `src/libraries/TickIterator.sol` | 141 to 151 | `7d9b582f32` | 2 |
| 64083 | stETH by EaseDeFi | `StNXM.removeTokenIdAtIndex` | `contracts/core/stNXM.sol` | 733 to 739 | `86decc1d35` | 6 |
| 64637 | Wannabet | `Bet.cancel` | `contracts/src/Bet.sol` | 164 to 199 | `30d6f4a79c` | 1 |
| 64661 | Ekubo | `TWAMM.getRewardRateInside` | `src/extensions/TWAMM.sol` | 84 to 111 | `ce72f5df63` | 6 |
| 64662 | Ekubo | `TWAMM.handleForwardData` | `src/extensions/TWAMM.sol` | 189 to 389 | `9ee78dbe74` | 6 |
| 64693 | Merkl | `Distributor._claim` | `contracts/Distributor.sol` | 425 to 491 | `5a4ce834a6` | 4 |
| 65025 | Panoptic | `BuilderWallet.init` | `contracts/RiskEngine.sol` | 2320 to 2322 | `4ef0998464` | 6 |
| 65027 | Panoptic | `CollateralTracker.settleBurn` | `contracts/CollateralTracker.sol` | 1614 to 1683 | `bebe915385` | 6 |
| 65028 | Panoptic | `RiskEngine.getLiquidationBonus` | `contracts/RiskEngine.sol` | 500 to 614 | `586faeee82` | 6 |
| 65029 | Panoptic | `RiskEngine._getRequiredCollateralAtTickSinglePosition` | `contracts/RiskEngine.sol` | 1315 to 1350 | `d434388bb6` | 6 |
| 65030 | Panoptic | `RiskEngine.twapEMA` | `contracts/RiskEngine.sol` | 814 to 818 | `6b154d96ba` | 6 |
| 65032 | Panoptic | `RiskEngine._getRequiredCollateralSingleLegNoPartner` | `contracts/RiskEngine.sol` | 1367 to 1529 | `069c00bd35` | 6 |
| 65036 | Panoptic | `RiskEngine._computeDelayedSwap` | `contracts/RiskEngine.sol` | 1976 to 2022 | `9acaa4e796` | 6 |
| 65040 | Panoptic | `RiskEngine._borrowRate` | `contracts/RiskEngine.sol` | 2198 to 2266 | `88ae38acad` | 6 |
| 65044 | Panoptic | `RiskEngine.isSafeMode` | `contracts/RiskEngine.sol` | 888 to 920 | `14bb7cc7ad` | 6 |

## Skipped findings

None. All 18 fix commits (17 findings; 64662 has two) and all 17 target files exist in the local clones.

## Redactions

**Audit text.** I scanned every comment in every bundle file. The scan looked for audit firm and contest names (Cyfrin, Code4rena, Sherlock, C4 and other firms), finding or submission numbers (such as H-01, M-02, S-123 and F-270), the words audit, finding, fix, issue, bug, exploit and mitigation, and the key words of each finding title. I then read every match by eye, as well as every comment inside each target function and in the twenty lines above it. No comment reveals the audit. The only matches were ordinary words, such as "fixed-point", "finding the first duplicate" and "prevent underflows". So no line was changed for audit text.

**Personal identifiers.** Eight comment lines named an individual developer: two author tags with a handle, two with a full name and an email address, and four library credit links whose web address contains a person's GitHub handle. The rules for this work say no personal identifiers anywhere. So I replaced only the text of those comment lines with `// [comment removed for blind review]`. Each was a whole-line comment. No code line was changed, and no line numbers moved. The removed text is not repeated anywhere in this folder.

| Bundle | File | Line |
|---|---|---|
| 62350 | `context/src/libraries/FullMath.sol` | 12 |
| 62350 | `context/src/libraries/FullMath.sol` | 76 |
| 63008 | `target.sol` | 30 |
| 63008 | `context/src/libraries/TickLib.sol` | 6 |
| 64083 | `context/contracts/general/ERC721TokenReceiver.sol` | 5 |
| 64661 | `target.sol` | 57 |
| 64662 | `target.sol` | 57 |
| 65027 | `context/contracts/tokens/ERC20Minimal.sol` | 6 |

**Comments kept on purpose.** In bundle 64661, the target function `getRewardRateInside` holds a comment from the developers themselves: "note that we check gt because if it's equal to start time, then the reward rate inside is necessarily 0". It sits on the line the fix changes. It is part of the original code at the snapshot and says nothing about the audit, so I kept it. The judge should know that it points at the line where the bug is.

## Context files left out because of the six-file limit

- 62350: `src/libraries/PipsMath.sol`, `src/types/InterestRate.sol`, `src/types/NonFungible.sol`, `src/BaseERC20.sol`, `src/BaseHooks.sol`, `src/Extsload.sol`, `src/NoDelegateCall.sol`, `src/RiskConfigs.sol`.
- 64083: `contracts/interfaces/IMorpho.sol`, `contracts/interfaces/IWNXM.sol`.
- 64661: `src/types/sqrtRatio.sol`, `src/interfaces/ICore.sol`, `src/interfaces/extensions/ITWAMM.sol`, `src/types/timeInfo.sol`, `src/libraries/CoreLib.sol`, `src/base/ExposedStorage.sol`, `src/types/storageSlot.sol`, `src/base/BaseExtension.sol`, `src/base/BaseForwardee.sol`, `src/types/poolState.sol`, `src/types/poolBalanceUpdate.sol`, `src/types/twammPoolState.sol`, `src/types/orderKey.sol`, `src/types/orderState.sol`, `src/math/timeBitmap.sol`, `src/types/feesPerLiquidity.sol`, `src/math/fee.sol`, `src/math/twamm.sol`, `src/math/time.sol`, `src/types/orderId.sol`, `src/types/swapParameters.sol`, `src/types/locker.sol`.
- 64662: `src/types/poolKey.sol`, `src/math/time.sol`, `src/types/poolId.sol`, `src/types/orderId.sol`, `src/math/fee.sol`, `src/types/locker.sol`, `src/types/callPoints.sol`, `src/types/positionId.sol`, `src/types/sqrtRatio.sol`, `src/interfaces/ICore.sol`, `src/interfaces/extensions/ITWAMM.sol`, `src/types/timeInfo.sol`, `src/libraries/CoreLib.sol`, `src/base/ExposedStorage.sol`, `src/base/BaseExtension.sol`, `src/base/BaseForwardee.sol`, `src/types/poolState.sol`, `src/types/poolBalanceUpdate.sol`, `src/types/orderConfig.sol`, `src/math/timeBitmap.sol`, `src/types/feesPerLiquidity.sol`, `src/types/swapParameters.sol`.
- 65025: `contracts/libraries/SafeTransferLib.sol`, `contracts/types/LeftRight.sol`, `contracts/types/LiquidityChunk.sol`, `contracts/types/PositionBalance.sol`, `contracts/types/RiskParameters.sol`, `contracts/types/TokenId.sol`, `contracts/types/OraclePack.sol`, `contracts/types/MarketState.sol`.
- 65027: `contracts/libraries/TransientReentrancyGuard.sol`, `contracts/libraries/Errors.sol`, `contracts/libraries/InteractionHelper.sol`, `contracts/libraries/SafeTransferLib.sol`, `contracts/types/LeftRight.sol`, `contracts/types/TokenId.sol`, `contracts/types/MarketState.sol`.
- 65028: `contracts/libraries/Errors.sol`, `contracts/libraries/SafeTransferLib.sol`, `contracts/types/LiquidityChunk.sol`, `contracts/types/PositionBalance.sol`, `contracts/types/RiskParameters.sol`, `contracts/types/TokenId.sol`, `contracts/types/OraclePack.sol`, `contracts/types/MarketState.sol`.
- 65029: `contracts/libraries/Errors.sol`, `contracts/libraries/Math.sol`, `contracts/libraries/SafeTransferLib.sol`, `contracts/types/LiquidityChunk.sol`, `contracts/types/PositionBalance.sol`, `contracts/types/RiskParameters.sol`, `contracts/types/OraclePack.sol`, `contracts/types/MarketState.sol`.
- 65030: `contracts/libraries/PanopticMath.sol`, `contracts/libraries/SafeTransferLib.sol`, `contracts/types/LeftRight.sol`, `contracts/types/LiquidityChunk.sol`, `contracts/types/PositionBalance.sol`, `contracts/types/RiskParameters.sol`, `contracts/types/TokenId.sol`, `contracts/types/MarketState.sol`.
- 65032: `contracts/PanopticPool.sol`, `contracts/libraries/Errors.sol`, `contracts/libraries/SafeTransferLib.sol`, `contracts/types/LiquidityChunk.sol`, `contracts/types/PositionBalance.sol`, `contracts/types/RiskParameters.sol`, `contracts/types/OraclePack.sol`, `contracts/types/MarketState.sol`.
- 65036: `contracts/libraries/Constants.sol`, `contracts/libraries/Errors.sol`, `contracts/libraries/SafeTransferLib.sol`, `contracts/types/LiquidityChunk.sol`, `contracts/types/PositionBalance.sol`, `contracts/types/RiskParameters.sol`, `contracts/types/OraclePack.sol`, `contracts/types/MarketState.sol`.
- 65040: `contracts/libraries/PanopticMath.sol`, `contracts/libraries/SafeTransferLib.sol`, `contracts/types/LeftRight.sol`, `contracts/types/LiquidityChunk.sol`, `contracts/types/PositionBalance.sol`, `contracts/types/RiskParameters.sol`, `contracts/types/TokenId.sol`, `contracts/types/OraclePack.sol`.
- 65044: `contracts/libraries/PanopticMath.sol`, `contracts/libraries/SafeTransferLib.sol`, `contracts/types/LeftRight.sol`, `contracts/types/LiquidityChunk.sol`, `contracts/types/PositionBalance.sol`, `contracts/types/RiskParameters.sol`, `contracts/types/TokenId.sol`, `contracts/types/MarketState.sol`.

## Notes for the judge

- **64083.** The target function `removeTokenIdAtIndex` has the `onlyOwner` modifier, and the finding's attacker is the owner. The task sentence asks for attacks by an unprivileged attacker. A reviewer who follows the sentence may correctly leave this bug out.
- **65044.** The finding text ends with "Panoptic marked as informative." The downloaded data still label it MEDIUM. The bug is a safety check that can never trigger. It is not a direct theft.
- **65040.** The finding names `CollateralTracker._updateInterestRate`, but the fix changed `RiskEngine._borrowRate`. The bundle targets `_borrowRate`, the function the fix changed.
- **64637 and 64693.** The fix is inside a squash commit that also fixes other findings. The diff in the sealed key shows every change to the target function in that commit, including changes for other findings.
- **65025 and 65030.** The fix-scope README marks these as judgment calls about extra edits in the fix commit. The sealed keys repeat the note.
- **Shared files.** Eight Panoptic bundles use `contracts/RiskEngine.sol` at different snapshots, and their snapshots follow one another in history. So some snapshots already contain the fixes for other findings in this list, and every snapshot may contain other known bugs outside the target function. The judge should score only the finding in the sealed key for that bundle.
- **Finding texts in the sealed keys.** These are copied from the downloaded Solodit data (`data_collection/downloaded_findings/batch_<n>_solodit_findings.json`). I removed finder names, the names of mitigation reviewers, and one repository owner's personal GitHub handle in links. Each key says what was removed from it.
