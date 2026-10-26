# Fix scope of the 43 pilot findings

The proposal studies one function body at a time. A High or Medium finding is left out when its fix changes more than one function body. Reviewers asked two questions:

1. Of the 43 pilot findings with public history, how many have a fix that stays inside one function body?
2. For each protocol, how many High and Medium findings are there, and how many distinct functions with a one-function fix does it give us?

## Files

- The per-finding table (`fix_scope_by_finding.csv`). One row per finding. Columns: `id`, `protocol`, `impact`, `title`, `repo`, `fix_commit`, `how_identified`, `confidence`, `classification`, `functions_changed`, `note`.
- This file (`README.md`).

## Method

**Which findings.** The 43 rows of the pipeline table (`pilot/results/findings_77_pipeline.csv`) whose *pipeline_stage* column is `history_found` (35) or `runs_complete` (8).

**Finding the fix.** I worked only in the local clones under `pilot/repos/`, with read-only git commands, and used no network. For each finding I started from the fix candidates in the task's history record (`pilot/tasks/<id>/history.json`). Then I searched the commit log after the audited commit for commits that touch the affected file. I matched commits to findings in this order:

1. The finding text cites a commit or pull request (Licredity, Sorella, Wannabet, EaseDeFi reports).
2. The project's own audit response names the pull request (Sequence, in `audits/code4rena-audit-response.md`).
3. The commit message cites the finding's submission number, such as `[S-382]` or `F-270` (Panoptic, Ekubo).
4. The commit message or the diff matches the bug the finding describes.

Some cited commits are not in the local clone. In those cases the work was squash-merged, and I used the merged commit on the main branch.

**Confidence.**
- *high*: the message or an audit response cites the finding, or the diff clearly fixes the described bug and the relevant part is easy to separate.
- *medium*: the fix sits inside a squash with other fixes, or the class depends on judging one extra edit as unrelated.
- *low*: a guess between candidates.
- *n/a*: no fix exists or none was found.

**Classifying the fix.** A small script compared each changed Solidity file before and after the fix commit. It removed comments and whitespace, split the file into functions, and reported which function bodies changed, which signatures changed, which functions were added or removed, and what changed outside functions. I then read every diff by eye. I ignored tests, scripts, comments, formatting, and edits in the same commit that belong to other findings. Each finding got one of four classes:

- **one function body**: the fix changes the body of one function only.
- **several function bodies**: the fix changes the bodies of two or more functions, with no signature or declaration change.
- **signature, storage layout, new function or other declaration**: the fix changes a function signature or visibility, the storage layout, adds or removes a function, or changes a declaration outside any function (a constant, enum, or a new contract). When a fix is both multi-function and has such a change, it goes here.
- **undetermined**: the sponsor did not fix the finding, or I could not pin down the fix commit.

The class describes the fix the developers actually wrote. It does not say whether a narrower fix was possible.

## Result 1: classification counts

| Class | Findings | High confidence |
|---|---|---|
| One function body | 17 | 14 |
| Several function bodies | 2 | 2 |
| Signature, storage layout, new function or other declaration | 15 | 14 |
| Undetermined | 9 | n/a |
| **Total** | **43** | |

- 17 of the 43 findings (40%) have a fix inside one function body. 14 of these are high confidence.
- 34 findings have an identified fix. Half of them (17 of 34) stay inside one function body.
- The 9 undetermined findings break down like this. The sponsor kept the behavior by design or acknowledged it in 3 (63764, 64692, 65041). The sponsor disputed 2 (65038, 65046). The sponsor marked 3 as informative and no fix appears in the history (65035, 65042, 65043). For 1, the sponsor says it was fixed, but I could not tie the fix to one commit (65039).

Three findings depend on a judgment call about what counts as part of the fix:

- 65025 (Panoptic H-01). The guard is inside `BuilderWallet.init`. The same commit adds a new `setBuilderAdmin` function. I counted that as an extra feature. If it is part of the fix, the finding moves to the new-function class.
- 65030 (Panoptic M-03). The fix to `twapEMA` is exactly what the finding asks for. The same commit also retunes a constant. If that retune is part of the fix, the finding moves to the declaration class.
- 65034 (Panoptic M-07). The finding names `settleBurn`. The commit makes the same change in `settleMint`. If only `settleBurn` counts, the finding moves to the one-function class.

So the one-function count lies between 15 and 18, depending on these three calls. The table above uses 17.

Five one-function findings have extra changes nearby that I did not count as part of the fix. The fix for 65025 uses a new custom error. The fixes for 64083, 64637 and 64693 sit in commits that also fix other findings. The commit for 65030 also retunes a constant.

## Result 2: per-protocol counts

The High and Medium counts come from the downloaded Solodit findings (`data_collection/downloaded_findings/batch_*_solodit_findings.json`), deduplicated by finding id. Each count covers the one audit report or contest that the pilot's findings come from. Solodit labels Cyfrin "Critical" findings as HIGH, so the two Licredity criticals count as High here.

The question mentions 11 protocols. The 43 findings come from 10 protocols. I added Megapot as the 11th, because it has local clones and 9 findings in the pipeline table, all with no usable history.

| Protocol | Audit | High | Medium | In the 77-finding table | In the 43 with history | One-function fixes | Distinct one-function functions |
|---|---|---|---|---|---|---|---|
| Panoptic | Code4rena 2025-12 next-core | 3 | 19 | 22 | 21 | 9 | 9 |
| Licredity | Cyfrin 2025-09 | 4 | 1 | 4 | 4 | 2 | 2 |
| Ekubo | Code4rena 2025-11 | 0 | 4 | 4 | 4 | 2 | 2 |
| Sequence | Code4rena 2025-10 | 2 | 4 | 6 | 6 | 0 | 0 |
| Merkl | Code4rena 2025-11 | 0 | 3 | 3 | 3 | 1 | 1 |
| Sorella L2 Angstrom | Cyfrin 2025-10 | 1 | 4 | 1 | 1 | 1 | 1 |
| stETH by EaseDeFi | Sherlock contest 1203 | 5 | 7 | 1 | 1 | 1 | 1 |
| Wannabet | Cyfrin 2025-12 | 0 | 3 | 1 | 1 | 1 | 1 |
| Ammplify | Sherlock contest 1054 | 13 | 23 | 1 | 1 | 0 | 0 |
| YuzuUSD | Pashov 2026-01-14 | 0 | 2 | 1 | 1 | 0 | 0 |
| Megapot | Code4rena 2025-11 | 3 | 8 | 9 | 0 | not assessed | not assessed |
| **Total** | | **31** | **78** | **53** | **43** | **17** | **17** |

The 17 distinct functions with a one-function fix:

- Panoptic (9): `BuilderWallet.init`, `CollateralTracker.settleBurn`, `RiskEngine.getLiquidationBonus`, `RiskEngine._getRequiredCollateralAtTickSinglePosition`, `RiskEngine.twapEMA`, `RiskEngine._getRequiredCollateralSingleLegNoPartner`, `RiskEngine._computeDelayedSwap`, `RiskEngine._borrowRate`, `RiskEngine.isSafeMode`. Seven of the nine are in one contract, `RiskEngine`.
- Licredity (2): `PositionLibrary.removeFungible`, `Licredity.decreaseDebtShare`.
- Ekubo (2): `TWAMM.getRewardRateInside`, `TWAMM.handleForwardData`.
- Merkl (1): `Distributor._claim`.
- Sorella L2 Angstrom (1): `TickIteratorLib.reset`.
- stETH by EaseDeFi (1): `StNXM.removeTokenIdAtIndex`.
- Wannabet (1): `Bet.cancel`.

One protocol, Panoptic, gives 9 of the 17 one-function findings (53%).

The downloaded data also hold other audits of some of these protocols. They are not in the table. Panoptic: Code4rena 2023-11 (2 High, 5 Medium), Code4rena 2024-04 (2 High, 9 Medium), Code4rena 2025-06 hypovault (2 High), Cantina 2024-10 (1 Medium), OpenZeppelin (7 High, 7 Medium). Sequence: two Quantstamp reports (1 High, 3 Medium together). Sorella: Spearbit 2024-10 (5 High, 3 Medium), Cantina 2024-11 (2 Medium). YuzuUSD: Pashov 2025-08-28 (3 High, 2 Medium). Megapot: Cantina 2024-01 (4 Medium), Cantina 2024-02 (1 High).

## The 8 tasks the pilot already built

Four of the 8 built tasks have a one-function fix: 62348, 62350, 63008 and 64637. The other four do not. 63185 changes two function bodies. 62347, 62349 and 63760 change a signature, the storage layout, or add a function.

## Limitations

- Only the 43 findings with history were classified. The 34 other findings in the pipeline table were not checked.
- Several fixes are squash merges that bundle many audit fixes: Wannabet 025c815, Merkl 01c99d0, YuzuUSD f63708c. The per-finding commits are not in the local clones. For these I had to pick out the part of the diff that belongs to the finding.
- The commits cited in the Licredity and Wannabet reports do not exist in the local clones. I used the commits on the main branch that carry the same pull request number or the same change.
- Two Panoptic matches (65027 and 65030) rely on commit message content. The submission number in the commit is not linked from the finding text.
- Some fixes span more than one commit (62349, 64662, 65031). The class uses all of their changes together.
- The function-splitting script is a pattern-based reader, not a Solidity compiler. I checked every diff by eye, but a function defined in unusual syntax could have been missed.
- Three classifications depend on a judgment call about unrelated edits (65025, 65030, 65034). The one-function count moves between 15 and 18 depending on them.
- "Undetermined" mixes two different cases. Eight findings were never fixed (acknowledged, disputed, or informative). One was fixed, but the fix could not be pinned to a commit (65039).
- The protocol counts reflect the downloaded Solodit snapshot (batch 4 was saved in April 2026). Findings added to Solodit later are not counted.
- The 11th protocol is my assumption. If the reviewers meant a different set, the Megapot row should be replaced.
- I did not re-check the pipeline's recorded vulnerability-introducing commits or target functions. In one case the finding names a different function from the one the fix changes: for 65040, the finding names `CollateralTracker._updateInterestRate`, but the fix is in `RiskEngine._borrowRate`. The per-protocol function list uses the function the fix changed.
