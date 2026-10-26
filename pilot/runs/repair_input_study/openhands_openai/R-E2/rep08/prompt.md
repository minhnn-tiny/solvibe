# Fix a reported vulnerability

## Context

You are working in a Foundry project for a Uniswap V4 hook. The function `reset(TickIteratorDown memory self, int24 startTick)` in `src/libraries/TickIterator.sol` was written from the requirement below. The requirement is also in `FEATURE_REQUEST.md`.

<requirement>
# Implement `reset` for the downward tick iterator in `src/libraries/TickIterator.sol`

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
</requirement>

## Report

A security reviewer found a vulnerability in this function. This is their report.

<report>
# All rewards can be stolen due to incorrect active liquidity calculations when the current tick is an exact multiple of the tick spacing at the upper end of a liquidity range

**Description:** Consider the scenario in which the current tick, `t`, is an exact multiple of the tick spacing, `s`, residing at the upper bound of the active liquidity range `[t0, t1)`, where: `s = 10`, `t0 = 0`, and `t = t1 = 30`. Execution of a zero-for-one swap causes `TickIteratorLib::initDown` to be invoked within `AngstromL2::_zeroForOneDistributeTax`, which calls `TickIterator::reset` and ultimately `TickIterator::_advanceToNextDown`:

```solidity
function _advanceToNextDown(TickIteratorDown memory self) private view {
    do {
        (int16 wordPos, uint8 bitPos) =
@>          TickLib.position((self.currentTick - 1).compress(self.tickSpacing));

        if (bitPos == 255) {
            self.currentWord = self.manager.getPoolBitmapInfo(self.poolId, wordPos);
        }

        bool initialized;
        (initialized, bitPos) = self.currentWord.nextBitPosLte(bitPos);
@>      self.currentTick = TickLib.toTick(wordPos, bitPos, self.tickSpacing);
        if (initialized) break;
    } while (self.endTick < self.currentTick);
}
```

The expectation when swapping from the upper tick of the range, where Uniswap determines zero active liquidity, to an initialized tick with non-zero liquidity, is that this net liquidity delta of the tick crossing will increase the active liquidity. However, the above logic will incorrectly initialize the current tick as `t1 - s`. This means the liquidity delta of `t1` is ignored and can result in arithmetic underflow when decrementing the net liquidity in both `CompensationPriceFinder::getZeroForOne` and `AngstromL2::_zeroForOneCreditRewards`:

```solidity
liquidity = liquidity.sub(liquidityNet);
```

Now consider a second, overlapping liquidity position `[t0', t1')`, where `t0' = -50` and `t1 = 50`. Execution of the same zero-for-one swap again suffers from the boundary tick being skipped; however, in this scenario, if there is sufficient liquidity provided by the overlapping position then the subtraction will not revert. For simplicity, assume both positions provide equal liquidity. In this case, the liquidity of position `[t0, t1)` is not considered in the initial liquidity, but then when `t0` is crossed and the liquidity contribution of this range is subtracted, the invocation of `IUniV4::getTickLiquidity` returns the full liquidity amount. The subsequent computation is therefore left with the liquidity that should be considered active in `[t0', t0]`, but there is no next tick below this range and so the loop exits. This causes execution to fall into the excess distribution logic which updates the global accumulator.

One thing to note here is that the comment states the excess should be distributed to the last position; however, it simply increments `globalGrowthX128` and nothing else (i.e. `rewardGrowthOutsideX128` remains unchanged for the last position).

```solidity
// Distribute remainder to last range and update global accumulator.
unchecked {
    cumulativeGrowthX128 += PoolRewardsLib.getGrowthDelta(taxInEther, liquidity);
    rewards[ticks.poolId].globalGrowthX128 += cumulativeGrowthX128;
}
```

When this incorrect behavior is leveraged by an attacker, it is possible to steal all rewards. While such an attack does not depend on a specific priority fee, it must be sufficient to win the top-of-block swap if needed to move the current tick to a boundary tick and JIT taxes must also be paid on liquidity addition. These caveats combined will decrease the profit, but it can be profitable nevertheless, considering the scenario in which:

* The current tick `t` is either already at or swapped one-for-zero to boundary tick `t1`.
* Due to `rewardGrowthOutsideX128` not being correctly initialized, as reported in H-02, the entry for both `t0` and t1` will be zero.
* Liquidity `L' = L * R / swapTax` is added to `[t1 - s, t1)`, where: `L` is the current liquidity in `[t0, t1)`, and `R` is the current reward balance.
* The current tick is zero-for-one swapped back down to a price immediately below the upper boundary of the attacker's liquidity position, i.e. `t < t1`, minimizing the amount of `token1` spent.
* Upon crossing the tick boundary, `_updateTickMoveDown()` flips `t1` and stores the corresponding `rewardsGrowthOutsideX128` entry as the initial `rewardGrowthGlobalX128`, `G`.
* When `_zeroForOneCreditRewards()` is called, this bug in `TickIteratorDown` causes the subtraction of the (negative) net liquidity for this tick to be skipped, meaning the additional liquidity added to `[t1 - s, t1)` is not added to `liquidity` and is not considered in the calculation.
* This is crucial because it means that the `cumulativeGrowthX128` calculated within the excess distribution block shown above uses a smaller `liquidity` value than intended, resulting in a much larger growth delta as this value is defined as the reward growth **per unit of liquidity**.
* Assuming a `cumulativeGrowthX128` delta of `g`, then `swapTax == g * L` rather than `swapTax == g * (L + L')` such that calculation of the reward growth inside `[t1 - s, t1)` is:

```solidity
   growthInsideX128
== growthGlobalX128 - rewardsGrowthOutsideX128[T0] - rewardsGrowthOutsideX128[T1]
== (G + g) - 0 - G
== g

    g * L'
== g * L * R / swapTax
== g * L * R / (g * L)
== R
```

* Thus when the attacker finally removes their liquidity from `[t1 - s, t1)`, they receive the full `R` rewards and realize a profit.

**Impact:** The active liquidity is calculated incorrectly when the current tick is an exact multiple of the tick spacing at the upper end of a liquidity range. In certain circumstances, this can result in swaps reverting due to underflow. In others, for example if there are multiple overlapping liquidity positions, this can result in incorrect distribution of rewards. In the most impactful case, an attacker can steal all the rewards at a profit.
</report>

## Task

Fix the vulnerability in the source code. You are done when both of these hold:

1. The vulnerability is fixed.
2. The code still meets the requirement.

## Rules

- You MUST NOT edit, add or delete any file under `test/`.
- You may edit any file under `src/`.
- Do not change any function signature.
- Do not add dependencies.
- When you are done, stop. Give a short summary of what you changed and why.