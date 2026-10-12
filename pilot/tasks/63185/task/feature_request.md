# Implement `transferOwnership` and `acceptOwnership` in `src/Util/TimedAdmin.sol`

`TimedAdminFacet` is the abstract base class for admin facets whose privileged
actions are time-gated. It follows the ERC-173 ownership standard. Ownership is
handed over in two steps with a waiting period in between. The current owner
names the next owner. After a delay, that named owner accepts and becomes the
owner. Until the named owner accepts, the current owner stays in charge, and a
named owner who never accepts never gains ownership.

Implement the two functions that drive this handshake. Both signatures are
already in the file; do not change them:

```solidity
function transferOwnership(address _newOwner) external virtual override
function acceptOwnership() external virtual override
```

## Helpers you build on

These already exist and are imported:

- `AdminLib.reassignOwner(address newOwner)` — records `newOwner` as the pending
  owner. Requires the caller to be the current owner; reverts
  `AdminLib.NotOwner()` otherwise.
- `AdminLib.acceptOwnership()` — makes `msg.sender` the owner and clears the
  pending owner. Requires `msg.sender` to be the current pending owner; reverts
  `AdminLib.ImproperOwnershipAcceptance()` otherwise.
- `AdminLib.getOwner()` — returns the current owner.
- `Timed.memoryPrecommit(uint256 useId, bytes memory entry)` — records a
  time-stamped precommit under `useId`. Only one precommit may exist per `useId`
  at a time; a second one reverts `Timed.ExistingPrecommitFound(useId)`.
- `Timed.fetchPrecommit(uint256 useId, uint32 delay)` — reads and clears the
  precommit under `useId`. Reverts `Timed.NoPrecommitFound(useId)` if there is
  none, and `Timed.PrematureParamUpdate(...)` if fewer than `delay` seconds have
  passed since it was recorded.
- `OWNER_USE_ID` — the constant already declared in this contract for the
  ownership precommit.
- `getDelay(true)` — the delay that applies to this handshake.
- `IERC173.OwnershipTransferred(address previousOwner, address newOwner)` — the
  ERC-173 event to emit when ownership changes.

## `transferOwnership(address _newOwner)`

The current owner calls this to begin handing ownership to `_newOwner`.

1. Nominate `_newOwner` as the next owner. After this call, `_newOwner` is the
   one account that may accept the transfer.
2. Start the waiting period: record a precommit for this transfer under
   `OWNER_USE_ID`, with `_newOwner` as the entry, so the transfer cannot be
   accepted until the delay has passed.

Only one ownership transfer may be in progress at a time.

## `acceptOwnership()`

The account the current owner nominated calls this, after the delay, to take
ownership.

1. Consume the transfer's precommit under `OWNER_USE_ID`, enforcing the delay
   with `getDelay(true)`. This fails if no transfer is in progress or if the
   delay has not yet elapsed.
2. Make the caller the new owner. This must succeed only for the account the
   current owner nominated.
3. Emit `IERC173.OwnershipTransferred(AdminLib.getOwner(), msg.sender)`.

Follow the style, helpers, errors, and events already used elsewhere in the
contract. `AdminLib`, `Timed`, `IERC173`, the `OWNER_USE_ID` constant, and
`getDelay` are all available.
