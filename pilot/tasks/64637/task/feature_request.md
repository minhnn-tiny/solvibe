# Implement `cancel` in `src/Bet.sol`

Wannabet is a peer-to-peer betting protocol. Each bet is its own `Bet` contract,
created by a factory. A bet has three roles. The **maker** opens the bet and puts
up `makerStake`. The **taker** accepts the bet and puts up `takerStake`. The
**judge** is a neutral third party who decides the winner. Both stakes are held
in an ERC20 token, the bet's `asset`. If the factory has set an Aave V3 pool for
that token, the stakes are supplied to the pool while the bet is live and
withdrawn when it ends.

A bet moves through the states in `IBet.Status`:

- `PENDING`: created, waiting for the taker to accept.
- `ACTIVE`: the taker has accepted, so both stakes are held.
- `RESOLVED`: the judge has picked the winner and the payout is done.
- `CANCELLED`: the bet was called off and the stakes were returned.
- `EXPIRED`: a deadline has passed. A pending bet is expired once
  `block.timestamp > acceptBy`, meaning no one accepted in time. An active bet is
  expired once `block.timestamp > resolveBy`, meaning the judge did not resolve in
  time. `EXPIRED` is never stored. The `_status` helper computes it from the
  stored status and the current time, and the `status()` and `bet()` views return
  it.

Implement the `cancel` function. The signature is already in the file; do not
change it:

```solidity
function cancel() external
```

`cancel` returns each party's stake and marks the bet `CANCELLED`. Who may call
it depends on the bet's current status.

Required behaviour:

1. Read the bet from storage. Work out its current status with the `_status`
   helper, so that a pending bet past `acceptBy` and an active bet past
   `resolveBy` both count as expired.

2. Check who is allowed to cancel, based on that status:
   - **Pending**: only the maker may cancel. The maker opened the bet and may take
     the offer back while no one has accepted it.
   - **Active**: only the judge may cancel. While a bet is live, the maker and the
     taker are both committed to it. The judge is the neutral party, and the only
     one who may call the bet off before it is resolved or expires.
   - **Expired**: anyone may cancel. The bet can no longer go ahead, so this is
     just the path that returns the stakes, and no caller is turned away.
   - **Resolved or already cancelled**: the bet is finished. Revert with
     `InvalidStatus()`.

   If the caller is not allowed to cancel in the current status, revert with
   `Unauthorized()`.

3. Return the stakes. Send `makerStake` to the maker and `takerStake` to the
   taker. If an Aave pool is set for the bet (`_aavePool` is not the zero
   address), withdraw the stakes from the pool first, the same way `resolve` does,
   and cap each refund at the amount actually withdrawn. The contract does not
   record which party has deposited, so make the two transfers independently: wrap
   each in `try/catch` so one failing transfer does not block the other.

4. Set the stored status to `CANCELLED` and emit `BetCancelled()`.

Follow the style, helpers, errors, and events already used in the rest of the
contract. The `IBet.Status` enum, the `InvalidStatus` and `Unauthorized` errors,
the `BetCancelled` event, the `_status` and `_min` helpers, and the `_bet` and
`_aavePool` state are all present and are used by `accept`, `resolve`, and the
view functions.
