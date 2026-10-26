# Finding 63008 — executable evidence package

Protocol: Sorella L2 Angstrom. Auditor: Cyfrin. Finding: "All rewards can be
stolen due to incorrect active liquidity calculations when the current tick is
an exact multiple of the tick spacing at the upper end of a liquidity range"
(a `TickIterator` off-by-one).

The vulnerable snapshot is commit `386baff` of `sorellaLabs/l2-angstrom`. The
root cause is in `src/libraries/TickIterator.sol`: the downward tick iterator
seeds its start at `startTick` instead of `startTick + 1`, so a zero-for-one
swap that starts exactly on a position's upper boundary tick skips that tick's
liquidity change. The historical fix is commit `c01b6c7` ("fix tick iterator").

Every build and test ran inside the `solvibe-tools:1` Docker image through
`pilot/scripts/dock.sh` **without** `--net`, so the container had no network.
Solc `0.8.26` came from the warmed `solvibe-svm` volume. No live chain, RPC, or
install was used.

All amounts are in the mock chain's native coin (ether) and the mock token.
Exact wei values are in the `logs/` files named in each row.

**Version 2** (the last section of this file) replaces the function-body
correction, adds a test that asserts the fixed state, and adds a new runner,
`reproduce_v2.sh`. The version-1 sections below are kept as they were.

## What this package contains

- `tests/Evidence63008_Entitlement.t.sol` — the entitlement and backing proof of
  vulnerability. Two test functions: the main scenario and one variant at a
  different boundary tick. It asserts the four facts of the violation (it does
  not only log them).
- `tests/Loss63008_AngstromL2.t.sol` — the pilot's loss test, reused here to read
  off the attacker's capital, costs, and net profit (item 4). It logs; it does
  not assert.
- `patches/tickiterator_function_body.patch` — the function-body-only correction
  (one line).
- `patches/h02_fix_cd0ac3c.patch` — the H-02 fix, taken from commit `cd0ac3c`.
- `patches/both_fixes.patch` — the two fixes together.
- `logs/` — the full console output of every run below.
- `reproduce.sh` — the exact commands, start to finish.

## How the entitlement test reads

`Evidence63008_Entitlement.t.sol` is a violation-asserting oracle. It measures
everything first and prints it, then runs four assertions at the very end:

1. the honest LP has a positive reward entitlement before the attack;
2. the attacker's collected reward is greater than its own swap tax (so it took
   more than its own tax share);
3. the hook's ether backing for LP rewards is less than what the honest LP is
   owed (a shortfall);
4. the honest LP receives less than it is owed.

On the vulnerable code all four hold, so the test **passes** (violation
observed). On a working fix the first of these assertions fails, so the test
**fails** (violation checked and absent). Because the measurements are printed
before the assertions, the fixed-code logs still show the honest LP claiming and
removing in full. The first assertion to fail on a fix is #2, printed as
`attacker reward <= its own swap tax (no theft): 24487756121327142 <= 24500000000000000`.

## Run table

One row per run. "Violation observed" means the entitlement test passed on that
code state. "Violation checked and absent" means it failed on that code state
(the fix removed the violation). Repo-suite rows exclude the entitlement test
itself.

| # | Code state | Test | Result | Key measured numbers | Log |
|---|---|---|---|---|---|
| 1 | vulnerable `386baff` | entitlement, main (boundary 20) | violation observed (PASS) | honest owed before 48.999999999999999999 eth; attacker reward 48.99999755 eth vs own tax 0.0245 eth; hook backing for LP rewards 0.024502450000000001 eth vs owed 49.0245 eth; honest claim reverts (got 0), removal reverts (got 0) | `logs/01_vulnerable_386baff_entitlement.log` |
| 2 | vulnerable `386baff` | entitlement, variant (boundary 30) | violation observed (PASS) | same magnitudes as row 1 (different boundary tick 30, attacker range [20,30)) | `logs/01_vulnerable_386baff_entitlement.log` |
| 3 | function-body fix | entitlement, main | violation checked and absent (FAIL) | attacker reward 0.024487756121327142 eth <= own tax 0.0245 eth; honest claim succeeds 49.000012243878672857 eth; removal succeeds, returns 14.978 eth + 9.9995 token | `logs/02_functionbody_fix_entitlement.log` |
| 4 | function-body fix | entitlement, variant | violation checked and absent (FAIL) | attacker reward 0.024487756121327142 eth <= own tax; honest claim 49.000012243878672857 eth; removal returns 9.9845 eth + 15.0055 token | `logs/02_functionbody_fix_entitlement.log` |
| 5 | H-02 fix only (`cd0ac3c`) | entitlement, main | violation observed (PASS) | byte-identical to row 1 (attacker reward 48.99999755 eth; honest claim and removal both revert) | `logs/04_h02_fix_only_entitlement.log` |
| 6 | H-02 fix only | entitlement, variant | violation observed (PASS) | byte-identical to row 2 | `logs/04_h02_fix_only_entitlement.log` |
| 7 | both fixes | entitlement, main | violation checked and absent (FAIL) | identical to row 3 (attacker reward 0.0244877 eth; honest made whole) | `logs/05_both_fixes_entitlement.log` |
| 8 | both fixes | entitlement, variant | violation checked and absent (FAIL) | identical to row 4 | `logs/05_both_fixes_entitlement.log` |
| 9 | vulnerable `386baff` | full repo suite | 60 pass / 0 fail | TickIteratorTest 28/0; AngstromL2Test 18/0 | `logs/00_vulnerable_386baff_full_suite.log` |
| 10 | function-body fix | full repo suite | 55 pass / 5 fail | 5 failures, all in TickIteratorTest (see below) | `logs/03_functionbody_fix_full_suite.log` |
| 11 | H-02 fix only | full repo suite | 60 pass / 0 fail | nothing breaks; the refactor is behaviour-preserving for the repo tests | `logs/07_h02_fix_only_full_suite.log` |
| 12 | both fixes | full repo suite | 55 pass / 5 fail | same 5 TickIteratorTest failures as row 10 | `logs/06_both_fixes_full_suite.log` |
| 13 | vulnerable `386baff` | loss test (capital) | attack profitable | attacker net profit +48.877274256875928055 eth; hook pays attacker 48.99999755 eth; honest LP loss 48.999999999999999999 eth (100%); principal locked 14.978 eth + 9.9995 token | `logs/08_vulnerable_loss_capital.log` |
| 14 | function-body fix | loss test | attack unprofitable, honest LP whole | attacker net profit -0.098235537002744802 eth; honest LP claims 49.000012243878672857 eth and removes full principal; loss 0 | `logs/09_functionbody_fix_loss.log` |

The repo suite has 60 tests: AngstromL2Test 18, TickIteratorTest 28, TickLibTest
6, PoolManagerStateGetterTest 5, MixedSignTest 2, IUniV4Test 1.

### The five failing tests on the fixed code (rows 10 and 12)

All five are in `test/libraries/TickIterator.t.sol`. Four fail because they
assert the old, faulty behaviour — that the downward iterator **excludes** the
start boundary tick, which is exactly the bug:

- `test_iterateDown_simple` — "First tick should be 50: 100 != 50";
- `test_iterateDown_boundaryExclusion` — "Should only get tick 0: 100 != 0";
- `test_iterateDown_exclusiveBoundaries` — "Should exclude start boundary 100: 100 != 0";
- `test_iterateDown_singleTick` — "Should have no ticks with exclusive boundaries".

The fifth, `test_iterateDown_emptyRange`, fails for a different reason. The fix
changes empty-range handling as a side effect: when `startTick == endTick` the
iterator now yields one phantom tick `startTick + 1`. The audited test still
expects an empty range to yield nothing. This is not a test of the
boundary-exclusion bug. The fix commit `c01b6c7` handled this by shipping an
**updated** version of that test (it documents the quirk and expects tick 101),
not by guarding the code. So on the audited test suite the count is five; the
four that encode the bug match the number the pilot reported.

## The function-body-only correction (item 2)

- Target function: `reset(TickIteratorDown memory self, int24 startTick)` in
  `src/libraries/TickIterator.sol`.
- The change is one line in that function's body:
  `self.currentTick = startTick;` becomes `self.currentTick = startTick + 1;`.
  Nothing else in any file changes. See `patches/tickiterator_function_body.patch`.

**Diff against `c01b6c7`'s version of the same function.** `c01b6c7`'s
`reset(TickIteratorDown)` makes the same functional change
(`self.currentTick = startTick + 1;`) and adds a three-line explanatory comment
above it. So the only difference between my change and `c01b6c7`'s version of
this function is that comment. The behaviour is identical, including the
empty-range phantom-tick quirk noted above.

**Did `c01b6c7` change anything else?** The commit `c01b6c7` itself touches two
files: `src/libraries/TickIterator.sol` and `test/libraries/TickIterator.t.sol`.
Inside `TickIterator.sol`, besides the `reset` line it edits two doc comments
(the library `@dev` invariant note and the `initDown` `@param` notes); neither
changes behaviour. It changes no other source file. (The pilot's
`human_fix_c01b6c7.patch` also shows a `peekNext` helper and an upward-iterator
loop-bound change from `<` to `<=`; those came from other commits between
`386baff` and `c01b6c7`, not from `c01b6c7` itself, which is why that patch's
base blob differs from the commit's.)

## H-02, corrected independently (item 3)

**What H-02 is.** The Cyfrin report (committed in the repo at
`audit/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md`, added by commit
`1fea75d`) contains the finding
"`rewardGrowthOutsideX128` is not correctly initialized in
`PoolRewards::updateAfterLiquidityAdd`". The 63008 finding cross-references it as
"H-02". `updateAfterLiquidityAdd` runs inside the `afterAddLiquidity` hook, by
which point the position's ticks are already initialized, so `!pm.isInitialized(...)`
is always false and the seeding of `rewardGrowthOutsideX128` never runs. The
report notes the impact is mitigated by `lastGrowthInsideX128`.

**Which commit fixes it, and why.** Commit `cd0ac3c` ("simplify LP reward
logic"). The report states this directly: "Sorella Labs: Fixed in commit
cd0ac3c. Cyfrin: Verified. The Uniswap initialization convention has been
removed entirely to simplify the accumulator logic." It is also the only
post-snapshot commit that touches `src/types/PoolRewards.sol`, where
`rewardGrowthOutsideX128` is initialized. The fix removes the dead seeding block
from `updateAfterLiquidityAdd` and routes it through the existing
`getGrowthInsideX128` helper; it also drops the now-unused `tickSpacing`
argument at the one call site in `AngstromL2.sol`. `patches/h02_fix_cd0ac3c.patch`
is byte-for-byte the source change of `cd0ac3c` (its test change is not
included).

**Result of applying H-02 only, without the 63008 fix.** The attack still works,
unchanged. Rows 5 and 6 are byte-identical to the vulnerable rows 1 and 2: the
attacker still collects 48.99999755 ether, the backing shortfall is still
48.99999755 ether, and the honest LP's claim and removal still revert. So none
of the three effects — attacker gain, backing shortfall, honest-LP lock —
depends on H-02. With H-02 fixed, the full repo suite still passes 60/0 (row 11).

**Both fixes together.** Rows 7 and 8 are identical to the function-body-fix rows
3 and 4, and the full suite result (row 12) is the same 55/5 as the
function-body fix alone. Adding H-02 on top of the tick fix changes nothing in
the attack outcome. The tick fix alone resolves the violation.

## Capital and ordering record (item 4)

Main scenario, from `tests/Loss63008_AngstromL2.t.sol` and
`logs/08_vulnerable_loss_capital.log`. "Measured" means the number comes from the
run; "assumption" means it is a choice of the scenario, not a derived cost.

- **Starting funds given to the attacker (assumption; a ceiling, not a minimum).**
  The test deals the attacker 100 ether and mints it 1,000,000,000 tokens. The
  attack does not spend most of this; it is just headroom.
- **The attack position (measured).** Liquidity 19999999000000000000000000
  (about 2e25 units) in the single tick-spacing-wide range [10, 20), just below
  the boundary tick 20. The test sizes it as `L * R / swapTax`, where `L` is the
  honest LP's liquidity and `R` the pending rewards.
- **The swaps the attacker makes (measured).**
  1. One one-for-zero swap with priority fee 0, to move the price up to the
     boundary tick 20 (exact input up to 10,000 token, stopped at the boundary
     price).
  2. Add the position [10, 20).
  3. One zero-for-one swap with priority fee 5 gwei, back down to the price just
     below the boundary (tick 19), exact input up to 10 ether.
  4. Remove the position.
- **Ordering (assumption).** Steps 2 to 4 happen in one block, and the attacker's
  taxed swap must be the top-of-block swap. The test fixes the attacker's
  priority fee at 5 gwei; it does not model a competitive priority-fee auction.
  The 5 gwei value is the test's chosen figure ("as low as will win TOB because
  the JIT tax must be paid"), not a derived minimum.
- **Blocks held (measured, from the test's block bumps).** The position is added,
  used, and removed inside a single block (a just-in-time position). The earlier
  price move (step 1) is a separate block.
- **Attacker costs (measured).** Swap tax 0.0245 ether, plus just-in-time (JIT)
  tax 0.098 ether charged on the add, plus the price impact of the two swaps.
- **Outcome (measured).** On the vulnerable code the hook pays the attacker
  48.99999755 ether of rewards on removal, for a net profit of
  +48.877274256875928055 ether. On the fixed code the attacker collects only
  0.024487756121327142 ether (its share of its own swap tax) for a net profit of
  -0.098235537002744802 ether, a loss roughly equal to the JIT tax.
- **The honest LP (measured).** Owed 48.999999999999999999 ether of rewards
  before the attack. On the vulnerable code it receives 0: both its reward claim
  and its full removal revert (the hook's `afterRemoveLiquidity` panics with
  arithmetic underflow, 0x11, wrapped as a hook error; revert data begins
  `0x90bfb865`). Its principal of 14.978 ether + 9.9995 token is locked. On the
  fixed code it claims 49.000012243878672857 ether and removes its full
  principal.

## Exact commands to reproduce

Run `./reproduce.sh` (it builds a throwaway clone and runs every state), or run
the steps by hand. Set-up, matching the pilot's loss run:

```
# in a throwaway directory
git clone --local --no-hardlinks \
  /Users/minh/Documents/workspaces/secure-solvibe/pilot/repos/sorellaLabs__l2-angstrom work
cd work && git checkout 386baff && cd -
rm -rf work/lib
cp -R /Users/minh/Documents/workspaces/secure-solvibe/pilot/repos/prepared/l2-angstrom@386baff/lib work/lib
rm -f work/.gitmodules
cp tests/Evidence63008_Entitlement.t.sol tests/Loss63008_AngstromL2.t.sol work/test/
```

Then, for each code state, with `DOCK=/Users/minh/Documents/workspaces/secure-solvibe/pilot/scripts/dock.sh`:

```
# vulnerable 386baff: entitlement PoV + variant (both PASS)
$DOCK work "FOUNDRY_SHOW_PROGRESS=false forge test --offline \
  --match-path test/Evidence63008_Entitlement.t.sol --match-test test_entitlement_backing -vv"

# full repo suite (exclude the entitlement test)
$DOCK work "FOUNDRY_SHOW_PROGRESS=false forge test --offline --fuzz-seed 1 \
  --no-match-path test/Evidence63008_Entitlement.t.sol --summary"

# function-body fix, then rerun the two commands above (entitlement FAILs, suite 55/5)
git -C work apply /ABS/PATH/patches/tickiterator_function_body.patch

# H-02 fix only, then rerun (entitlement PASSes, suite 60/0)
git -C work apply /ABS/PATH/patches/h02_fix_cd0ac3c.patch

# both fixes, then rerun (entitlement FAILs, suite 55/5)
git -C work apply /ABS/PATH/patches/both_fixes.patch

# capital numbers (vulnerable and function-body fix)
$DOCK work "FOUNDRY_SHOW_PROGRESS=false forge test --offline \
  --match-path test/Loss63008_AngstromL2.t.sol --match-test test_loss_stealAllRewards -vv"
```

`dock.sh` is always called without `--net`. `FOUNDRY_SHOW_PROGRESS=false` is
required: this repo's `foundry.toml` sets `show_progress = true`, and with it on,
forge 1.5.1 drops whole test suites from its output at random. Restore `src`
from a pristine copy between patches (the patches are written against `386baff`).

## What did not work or remains uncertain

- The variant (boundary tick 30) produces economic magnitudes equal to the main
  scenario (boundary tick 20), because the reward pool and the swap tax are the
  same by construction. It is a genuinely different boundary tick and a different
  attacker range ([20, 30) instead of [10, 20)), and the honest LP's removal
  splits differently on the fix (9.9845 ether + 15.0055 token vs 14.978 ether +
  9.9995 token), but it is not a different-sized attack. A variant with a
  different magnitude would need a different reward build-up.
- The entitlement test is a violation-asserting oracle, so "violation checked and
  absent" is reported as a test **failure**, not a pass. The honest LP being made
  whole on the fix is shown in the logs (printed before the failing assertion),
  not by a passing assertion. This is deliberate: a single test gives a clean
  pass-on-vulnerable, fail-on-fix differential. It does mean the word "FAIL" in
  rows 3, 4, 7, 8 is the intended result there.
- The function-body fix is kept minimal, so it reproduces `c01b6c7`'s reset body
  exactly — including `c01b6c7`'s incidental empty-range quirk (an empty range
  yields a phantom tick). That is why `test_iterateDown_emptyRange` fails on the
  fix. I did not add the empty-range guard that the pilot's reference repair
  used, because the task asked for the smallest change that restores the fixed
  behaviour, and the fixed behaviour is `c01b6c7`'s.
- H-02 has no measured effect on this attack: rows 5 and 6 are byte-identical to
  the vulnerable rows. This matches the report's own note that
  `lastGrowthInsideX128` mitigates H-02. So the package shows that H-02 is a
  correctness cleanup here, not a second lever on the theft.
- "Attacker must win the top-of-block swap" is an assumption of the scenario, not
  something the test measures. The test sets the priority fee directly and does
  not simulate competition for the top-of-block slot.
- In the report v2.1 the H-02 finding sits in the Informational section even
  though the High finding (63008) cites it as "H-02". The numbering mismatch is
  in the source material; the fix commit (`cd0ac3c`) is unambiguous because the
  report names it.

## Version 2

A peer reviewer found three defects in version 1. Version 2 fixes them. The
version-1 files are unchanged. The new files sit beside them:

- `patches/tickiterator_function_body_v2.patch` — the new function-body
  correction (one added line).
- `tests/Fixed63008_State.t.sol` — the fixed-state test, contract
  `Fixed63008_State`. It passes when the honest LP is made whole.
- `reproduce_v2.sh` — the runner for all four code states.
- `logs/v2_01_*.log` to `logs/v2_12_*.log` — one log per run.
  `logs/v2_summary.log` — the summary table the runner printed.

The violation test (`tests/Evidence63008_Entitlement.t.sol`) and the loss test
(`tests/Loss63008_AngstromL2.t.sol`) are unchanged.

### Defect 1: the correction must keep an empty range empty

In version 1, `self.currentTick = startTick;` became `startTick + 1`. That line
runs before the empty-range early return. So when `startTick == endTick`, the
iterator kept `currentTick = startTick + 1`, `hasNext()` returned true, and it
yielded one tick outside the range. That is why `test_iterateDown_emptyRange`
failed.

Version 2 leaves the original line and the early return as they were. It adds
one line after the return:

```diff
@@ -139,6 +139,7 @@ library TickIteratorLib {
 
         if (startTick == self.endTick) return;
 
+        self.currentTick = startTick + 1;
         (int16 wordPos,) = TickLib.position(startTick.compress(self.tickSpacing));
         self.currentWord = self.manager.getPoolBitmapInfo(self.poolId, wordPos);
 
```

What this does:

- An empty range keeps `currentTick = startTick`, which equals `endTick`.
  `hasNext()` checks `currentTick > endTick`, so it is false and nothing is
  yielded. This is the same as at `386baff`.
- A non-empty range starts the search at `startTick + 1`. `_advanceToNextDown`
  looks for the next initialized tick strictly below `currentTick`, so it now
  includes `startTick` itself. For every non-empty range this is the same as
  `c01b6c7`.
- The bitmap word loaded on the next line is still the word that holds
  `startTick`. That is the word `_advanceToNextDown` reads first, because it
  reads the word of `currentTick - 1`.

Only the body of `reset(TickIteratorDown memory self, int24 startTick)` in
`src/libraries/TickIterator.sol` changes. No other function, no signature, and
no struct or storage layout changes. So the empty-range case can be handled
inside that one function body.

Upstream handled the same case later, inside the same function. In the final
commit `8e0e417` ("finished"), `reset` sets `startTick + 1` first and then, in
the empty-range branch, sets `currentTick = type(int24).min`. The only
difference from version 2 is the value left in `currentTick` for an empty range:
`endTick` here, `type(int24).min` upstream. In both, `hasNext()` is false and
`getNext()` reverts with `NoNext`. No code outside `TickIterator.sol` reads the
iterator's fields (checked with `git grep` at `386baff`), so the two behave the
same for every caller.

Result: `test_iterateDown_emptyRange` passes in all four code states
(`logs/v2_03_vulnerable_suite.log`, `logs/v2_06_v2fix_suite.log`,
`logs/v2_09_h02only_suite.log`, `logs/v2_12_bothv2_suite.log`).

### Defect 2: a test that asserts the fixed state

The violation test asserts the violation. On fixed code it fails at its first
assertion, so it never checks that the honest LP is made whole. The new contract
`Fixed63008_State` (in `tests/Fixed63008_State.t.sol`) inherits from the
violation test contract. It reuses its set-up and attack steps (`_build` and
`_attack`) without changing them, and runs the same two scenarios (boundary tick
20 and boundary tick 30). Then it asserts:

1. the honest LP's reward claim succeeds;
2. the claim pays at least what the honest LP is owed at claim time, and at
   least what it was owed before the attack;
3. the honest LP's full removal succeeds, and returns at least its principal in
   ether and in token. The principal is computed with Uniswap's `SqrtPriceMath`
   for the LP's liquidity at the current price, rounded down as on removal;
4. the hook's ether backing for LP rewards (its ether claim minus protocol
   revenue) is at least what the honest LP is owed;
5. the attacker's reward is at most its own share of its own swap tax. The share
   is `swapTax * attackerLiquidity / (attackerLiquidity + honestLiquidity)`.
   This formula is right for this scenario only: the taxed swap moves the price
   down by one tick from the boundary, and only the two positions are in range
   there.

The tolerance is 1 wei, added to the side that should be larger. It is taken
from the version-1 logs. There, the only gap between amounts that should match
is 1 wei of rounding: the honest LP was owed 48999999999999999999 wei for 49e18
wei of tax paid in, and on the fix the hook's backing was 1 wei above the
honest LP's claim. In the version-2 runs the tolerance was never needed: in
every comparison the two amounts were equal to the wei, or the side that should
be larger was larger.

Run it with `--match-test test_fixed_state`. The filter is needed because the
contract also inherits the violation test functions and the 18
`AngstromL2Test` tests.

On the vulnerable code it fails at the first assertion, "honest LP reward claim
reverted". The other broken properties show in the printed values before that
point (see the table below), but a forge test stops at its first failed
assertion, so they are not reported as separate failures.

### Defect 3: a runner that runs every state

`reproduce_v2.sh` does not use `set -e`. For each of the four code states it
restores `src` to `386baff`, applies that state's patches, and runs three
things: the violation test, the fixed-state test, and the repository suite. It
writes each run's full output to its own log. It turns each log into an outcome
of the form "N pass, M fail: names of failing tests", adding up every
`Suite result:` line. It compares that outcome, test names included, with the
expected outcome. It prints a summary table and exits 1 only if some outcome
differs (2 if the set-up fails). A build error gives "0 pass, 0 fail", which
never matches.

The repository suite excludes every file the package adds, with the same flag in
every state: `--no-match-path 'test/*63008*'`. That covers the violation test,
the loss test and the fixed-state test. No file of the repository itself has
`63008` in its name. The suite logs show exactly the six repository contracts
and 60 tests in every state.

Note on version 1: as written, `reproduce.sh` excluded only the entitlement file
from the suite, while it had also copied the loss test into `test/`. The loss
contract inherits `AngstromL2Test`, so its 18 inherited tests and the loss test
would also be counted. I did not rerun version 1 to confirm this. The version-1
suite logs show only the six repository contracts.

The "both fixes" state in version 2 is the H-02 patch
(`patches/h02_fix_cd0ac3c.patch`) followed by the version-2 correction. The two
patches touch different files. There is no separate combined patch file.

### Version 2 run table

All runs: `reproduce_v2.sh`, offline, one run end to end. It exited 0: all 12
outcomes matched the expected outcome.

| Code state | Violation test (2 tests) | Fixed-state test (2 tests) | Repository suite (60 tests) | Matches expected | Logs |
|---|---|---|---|---|---|
| vulnerable `386baff` | 2 pass, 0 fail (violation observed) | 0 pass, 2 fail, both at "honest LP reward claim reverted" | 60 pass, 0 fail | yes, all three | `logs/v2_01_vulnerable_violation.log`, `logs/v2_02_vulnerable_fixedstate.log`, `logs/v2_03_vulnerable_suite.log` |
| version-2 correction | 0 pass, 2 fail, both at "attacker reward <= its own swap tax (no theft)" (violation absent) | 2 pass, 0 fail | 56 pass, 4 fail: `test_iterateDown_boundaryExclusion`, `test_iterateDown_exclusiveBoundaries`, `test_iterateDown_simple`, `test_iterateDown_singleTick` | yes, all three | `logs/v2_04_v2fix_violation.log`, `logs/v2_05_v2fix_fixedstate.log`, `logs/v2_06_v2fix_suite.log` |
| H-02 fix only (`cd0ac3c`) | 2 pass, 0 fail (violation observed) | 0 pass, 2 fail, both at "honest LP reward claim reverted" | 60 pass, 0 fail | yes, all three | `logs/v2_07_h02only_violation.log`, `logs/v2_08_h02only_fixedstate.log`, `logs/v2_09_h02only_suite.log` |
| both fixes (`cd0ac3c` + version-2 correction) | 0 pass, 2 fail, both at "attacker reward <= its own swap tax (no theft)" (violation absent) | 2 pass, 0 fail | 56 pass, 4 fail: the same four tests | yes, all three | `logs/v2_10_bothv2_violation.log`, `logs/v2_11_bothv2_fixedstate.log`, `logs/v2_12_bothv2_suite.log` |

All four failing suite tests are in `test/libraries/TickIterator.t.sol`. Each
asserts that the downward iterator excludes its start tick, which is the bug.
There is no other failure. With the version-1 correction the suite was 55 pass,
5 fail; the fifth, `test_iterateDown_emptyRange`, now passes.

Numbers printed by the fixed-state test (wei; the main scenario at boundary 20,
and the variant at boundary 30 where it differs):

| Quantity | vulnerable, and H-02 only | version-2 correction, and both fixes |
|---|---|---|
| honest LP owed before the attack | 48999999999999999999 | 48999999999999999999 |
| honest LP owed at claim time | 49024499999999999999 | 49000012243878672857 |
| honest LP reward received | 0 (claim reverted) | 49000012243878672857 (equal to what it is owed) |
| hook ether backing for LP rewards | 24502450000000001 | 49000012243878672858 (1 wei above what is owed) |
| attacker reward | 48999997549999999999 | 24487756121327142 |
| attacker share of its own swap tax | 24487756121327142 | 24487756121327142 (equal to the reward) |
| honest LP removal, main | reverted, 0 returned | 14978012287872122069 ether + 9999505965089401322 token, equal to the principal |
| honest LP removal, variant | reverted, 0 returned | 9984507690216159807 ether + 15005504318762348377 token, equal to the principal |

The H-02-only numbers are identical to the vulnerable numbers, and the
both-fixes numbers are identical to the version-2-correction numbers.

### How to run version 2

```
./reproduce_v2.sh                 # throwaway tree in a new temporary directory
WORK=/some/dir ./reproduce_v2.sh  # or choose where the throwaway tree goes
```

It writes the logs to `logs/v2_*.log`, overwriting the ones recorded here. The
recorded run used `WORK=/Users/minh/.claude/jobs/eeaa430c/tmp/63008v2/run1`.

### What remains open in version 2

- The four failing repository tests assert the old behaviour. Any correct fix
  makes them fail. `c01b6c7` updated them; version 2 keeps the audited test
  file, so the suite shows 56 pass, 4 fail and not 60 pass.
- The attacker-share bound in the fixed-state test uses a formula that holds
  only in this scenario (two positions in range, one tick of price movement). It
  is not a general rule for how the hook splits the tax.
- I checked the runner's mismatch path only by giving its parser the version-1
  suite log (55 pass, 5 fail, with `test_iterateDown_emptyRange`). It reports an
  outcome different from the expected 56 pass, 4 fail. I did not do a full run in
  which an outcome actually differed.
- The capital record (rows 13 and 14 of the version-1 table) still comes from
  the version-1 correction. I did not rerun the loss test with the version-2
  correction. The version-2 fixed-state runs give the same attacker reward,
  honest-LP claim and removal amounts as the version-1 correction's entitlement
  log (`logs/02_functionbody_fix_entitlement.log`), to the wei.
