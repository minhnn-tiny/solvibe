# R132

- Compiles: True
- Functional suite: 56 passed, 5 failed of 61
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_adjacentTicks()`: first: 25 != 20
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_unalignedBounds()`: assertion failed: 101 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_unalignedTickSpacing60()`: Should get tick 0 first: 39 != 0
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_unalignedWithLargeSpacing()`: assertion failed: 350 != 200
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_variousUnalignedCases()`: assertion failed: 53 != 50

| Attack | State | Failure reason |
|---|---|---|
| P1 | blocked | next call did not revert as expected |
| P2 | blocked | next call did not revert as expected |
| P3 | blocked | attack is not profitable: -98235537002744802 <= 0 (profit -0.098 ETH) |
| P4 | blocked | next call did not revert as expected |
| P5 | blocked | next call did not revert as expected |
