# Implement `_afterSwap` in `src/Licredity.sol`

Licredity is a Uniswap V4 hook. The pool pairs the base fungible (currency0,
e.g. ETH) against the protocol's own debt fungible (currency1). The pool is
meant to trade around parity: one debt fungible is worth one base fungible, and
the square-root price at parity is the constant `ONE_SQRT_PRICE_X96` already
defined in the file.

`_afterSwap` is the Uniswap V4 `afterSwap` hook callback. The pool manager calls
it once after every swap on this pool. Implement it. The signature is already in
the file; do not change it:

```solidity
function _afterSwap(
    address sender,
    PoolKey calldata,
    IPoolManager.SwapParams calldata,
    BalanceDelta balanceDelta,
    bytes calldata
) internal override returns (bytes4, int128)
```

Required behaviour:

1. The function must return `(this.afterSwap.selector, 0)`.

2. A swap that leaves the pool price at or below parity is not acceptable. The
   protocol charges interest on debt, and interest cannot be negative, so the
   pool must never be left sitting at a price below one base fungible per debt
   fungible. By the time the call finishes for a normal user swap, the pool
   price must be at least `ONE_SQRT_PRICE_X96`. Read the current price with
   `poolManager.getSlot0(poolId)`.

3. If your implementation itself trades on the pool to carry out point 2, that
   nested action will call this hook again. The hook must recognise that it is
   being re-entered by the contract's own action (`sender == address(this)`) and
   do nothing in that case except return the selector tuple, so it does not loop.

4. Whenever base fungible is collected and debt fungible is owed as a result of
   restoring the price, the amounts that later become redeemable through
   `exchangeFungible` must be recorded. `exchangeFungible` lets anyone hand back
   debt fungible and receive base fungible from the pool at the ratio of the
   recorded amounts. Keep `baseAmountAvailable` (base fungible the contract now
   holds and can pay out) and `debtAmountOutstanding` (debt fungible that has
   been handed to the pool manager and can be redeemed) in step with each other,
   and settle any balance you move with the pool manager so the unlock accounting
   closes. The minting, `sync`, `settle`, and `take` helpers used elsewhere in
   this file are available, as is `baseFungible`.

5. After handling the price, update the oracle by calling `oracle.update()` so
   downstream price reads stay current. This only needs to happen for normal user
   swaps, not for the contract's own re-entrant calls.

Follow the style, helpers, and constants already used in this file:
`ONE_SQRT_PRICE_X96`, `MAX_SQRT_PRICE_X96`, `poolManager`, `poolId`, `poolKey`,
`baseFungible`, `oracle`, `baseAmountAvailable`, `debtAmountOutstanding`, and the
`_mint` helper are all available.
