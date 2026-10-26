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
