# Implement `decreaseDebtShare` in `src/Licredity.sol`

Licredity lets a position borrow the protocol's debt fungible. A position's debt
is tracked in two ways that move together:

- `totalDebtShare` and `totalDebtBalance` are the protocol-wide totals. Shares
  are the unit of ownership of the debt; balance is the amount of debt fungible
  those shares currently stand for. The amount of debt fungible that one share is
  worth is `totalDebtBalance / totalDebtShare`.
- Each `Position` records its own debt share and holds collateral fungibles.

`decreaseDebtShare` repays debt: it removes `delta` shares of debt from a position
and burns the matching debt fungible. The counterpart that adds debt,
`increaseDebtShare`, is already in the file and follows the same conventions.

Implement the function. The signature is already in the file; do not change it:

```solidity
function decreaseDebtShare(uint256 positionId, uint256 delta, bool useBalance)
    external
    returns (uint256 amount)
```

Required behaviour:

1. Work out `amount`, the quantity of debt fungible to burn for `delta` shares,
   from the current totals: `amount = delta * totalDebtBalance / totalDebtShare`,
   rounded up so the position never under-pays. Use the `fullMulDivUp` helper, as
   `increaseDebtShare` does for its own rounding.

2. The `useBalance` flag chooses where the debt fungible being burned comes from:

   - `useBalance == true`: burn debt fungible that the position itself holds as
     collateral. Only the position owner may do this, so revert with
     `NotPositionOwner()` if `msg.sender` is not `position.owner`. Remove `amount`
     of the debt fungible (the contract's own token, `Fungible.wrap(address(this))`)
     from the position with `removeFungible`, then burn it from the contract.
     Emit `WithdrawFungible(positionId, address(0), Fungible.wrap(address(this)), amount)`.

   - `useBalance == false`: burn `amount` of debt fungible from `msg.sender`'s own
     balance. The position must exist, so revert with `PositionDoesNotExist()` if
     `position.owner` is the zero address.

3. Reduce the position's own recorded debt by `delta` using the position's
   `decreaseDebtShare`.

4. Reduce the protocol-wide totals: subtract `delta` from `totalDebtShare` and
   `amount` from `totalDebtBalance`.

5. Emit `DecreaseDebtShare(positionId, useBalance, delta, amount)`.

6. Return `amount`.

The existing code emits events through inline assembly with precomputed topic
hashes; keep that style, and you can copy the exact topics from the current
`increaseDebtShare` and the withdraw path. Follow the style, helpers, and storage
layout already used in this file: `positions`, `totalDebtShare`,
`totalDebtBalance`, the `fullMulDivUp` helper, `removeFungible`, `_burn`, and the
`increaseDebtShare` counterpart are all available.
