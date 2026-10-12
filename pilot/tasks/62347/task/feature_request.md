# Implement `seize` in `src/Licredity.sol`

`Licredity` is a lending protocol. A position holds collateral (fungibles and
non-fungibles) and a debt share. A position is *healthy* when its appraised
value covers its debt plus a margin requirement. When a position becomes
unhealthy, a liquidator may seize it.

Implement the `seize` function. The signature is already in the file; do not
change it:

```solidity
function seize(uint256 positionId, address recipient) external returns (uint256 shortfall)
```

Required behaviour:

1. If the position does not exist (its owner is the zero address), revert with
   `PositionDoesNotExist()`.
2. The owner of a position must not seize their own position. If
   `position.owner == msg.sender`, revert with `CannotSeizeOwnPosition()`.
3. Register the position with `Locker.register(bytes32(positionId))` so that its
   health is re-checked before the current `unlock` finishes.
4. Appraise the position with `_appraisePosition`. If it is healthy, revert with
   `PositionIsHealthy()`.
5. If the position is underwater (appraised value is less than its debt), top it
   up so that seizing it is still worthwhile. Compute the top-up amount with
   `_deficitToTopup(debt - value)`, mint that much debt fungible to the contract,
   add it to the position, and increase the total debt balance by the same
   amount. Recompute the position's debt afterwards. This top-up is bad debt that
   is shared across all debt holders. Emit the deposit event the same way the
   other deposit paths do.
6. Transfer ownership of the position to `recipient` with `position.setOwner`.
7. Set the return value `shortfall` to the debt fungible still needed to bring
   the position back to health: `value < debt + marginRequirement`, then
   `debt + marginRequirement - value`, otherwise `0`.
8. Emit the `SeizePosition` event with the position id, recipient, value, debt,
   margin requirement, and top-up.

Follow the style, helpers, errors, and events already used elsewhere in the
contract. The errors, the `SeizePosition` event, `_appraisePosition`,
`_deficitToTopup`, `Locker`, and the `Position` helpers are all available.
