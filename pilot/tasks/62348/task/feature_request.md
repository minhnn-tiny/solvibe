# Implement `removeFungible` in `src/types/Position.sol`

A `Position` holds fungible collateral. It records the held fungibles in two
places that must always describe the same set of assets:

- `fungibles`, a compact array that lists each held fungible once, with no gaps.
- `fungibleStates`, a mapping from a fungible to its packed state. The state
  holds a 1-based index into the `fungibles` array and the balance held of that
  fungible.

The index convention is 1-based: a fungible held at `fungibles[k]` has
`fungibleStates[fungible].index() == k + 1`. An index of 0 means the fungible is
not held. The counterpart that adds a fungible, `addFungible`, is already in the
file and follows this convention.

Implement the `removeFungible` function. The signature is already in the file;
do not change it:

```solidity
function removeFungible(Position storage self, Fungible fungible, uint256 amount)
    internal
    returns (bool isRemoved)
```

Required behaviour:

1. Read the current state of `fungible` from `self.fungibleStates`. The index
   tells you whether the fungible is held and where it sits in the array. The
   balance is the amount currently held.
2. The new balance is the current balance minus `amount`. A position cannot hold
   a negative balance, so removing more than is currently held must revert.
3. If the fungible is not held, there is nothing to remove. Leave the position
   unchanged and return `false`.
4. If the fungible is held and the new balance is still positive, store the new
   balance for that fungible and keep its place in the array. Return `true`.
5. If the fungible is held and the new balance is zero, remove the fungible
   completely:
   - Clear its entry in `fungibleStates` so it reads as not held.
   - Remove it from the `fungibles` array and keep the array compact, with no
     gap left behind.
   - Return `true`.
6. Keep the two records consistent at all times. After the call returns, every
   fungible listed in `fungibles` must have a positive balance and a cached
   index equal to its 1-based position in the array, and every fungible with a
   non-zero state must appear in the array exactly once. Removing one fungible
   must not change the recorded balance of any other fungible.

The return value `isRemoved` is `true` when the fungible was held and the
removal was applied, and `false` when the fungible was not held and nothing
changed.

Follow the style, helpers, and storage layout already used in this file.
`toFungibleState`, the `index()` and `balance()` accessors on `FungibleState`,
the `FUNGIBLES_OFFSET` and `FUNGIBLE_STATES_OFFSET` constants, and the
`addFungible` counterpart are all available.
