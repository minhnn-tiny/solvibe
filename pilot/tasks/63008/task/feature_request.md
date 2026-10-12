# Implement `reset` for the downward tick iterator in `src/libraries/TickIterator.sol`

`TickIteratorLib` walks the initialized ticks of a Uniswap V4 pool in one
direction. A caller uses it to visit, in order, every tick that a price move
crosses, so it can add up the net-liquidity change at each tick. The library has
two iterators over the same pool. The upward one goes from a low tick to a high
tick (`TickIteratorUp`). The downward one goes from a high tick to a low tick
(`TickIteratorDown`). Each iterator is created with `initUp` / `initDown`, which
store the pool manager, the pool id, the tick spacing and the end tick, and then
call `reset` to point the iterator at its start tick. After `reset`, the caller
reads ticks with `hasNext` and `getNext`. Every tick that `getNext` returns is
an initialized tick that carries a net-liquidity change.

The reason the iterators exist: for a range from a start tick to an end tick,
the iterator must return every initialized tick in that range, so that if you
begin with the active liquidity at the start tick and apply the net liquidity of
each returned tick in turn, you end up with the active liquidity at the end
tick. Liquidity follows Uniswap's half-open convention: a position over
`[lower, upper)` is active for ticks from `lower` up to, but not including,
`upper`.

Implement `reset` for the downward iterator. The signature is already in the
file; do not change it:

```solidity
function reset(TickIteratorDown memory self, int24 startTick) internal view
```

`reset` sets up (or re-points) an already-created `TickIteratorDown` so it is
ready to return ticks from `startTick` downward. `self.endTick`,
`self.tickSpacing`, `self.manager` and `self.poolId` are already set.

Required behaviour:

1. Check the range. The downward iterator runs from the higher start tick down
   to the lower end tick, so `self.endTick` must be less than or equal to
   `startTick`. If it is not, revert with `InvalidRange()`.

2. Decide which ticks are in range. Both iterators use the same rule for their
   two bounds: the higher of the two bound ticks is included and the lower is
   excluded. For the upward iterator the higher bound is its end tick, which is
   included, and the lower bound is its start tick, which is excluded. For the
   downward iterator the higher bound is `startTick`. So the downward walk
   includes `startTick` and excludes `self.endTick`. If `startTick` is itself an
   initialized tick, it is the first tick that `getNext` returns; the walk then
   continues downward and stops before `self.endTick`.

3. Prepare the scan. Set it up the way the upward `reset` sets up its own
   direction. Find the pool's bitmap word that covers the start tick
   (`TickLib.position` of the compressed start tick), load it into
   `self.currentWord` with `self.manager.getPoolBitmapInfo`, then use
   `_advanceToNextDown` to move the cursor onto the first tick the iterator
   should return. Set the cursor before that first `_advanceToNextDown` so the
   tick it lands on is the one required by point 2.

4. End state. When `reset` returns, `hasNext` must report true exactly while
   there is still an initialized tick left in the range (start included, end
   excluded), and false once the scan has moved past `self.endTick`.

Follow the style, the helpers and the `InvalidRange` error already used by the
upward `reset` and by `_advanceToNextDown`. Change only the body of this
function; leave every other function and the struct layout unchanged.
