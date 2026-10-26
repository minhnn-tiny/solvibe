# R107

- Compiles: True
- Functional suite: 57 passed, 4 failed of 61
  - failed: `test/AngstromL2.t.sol:AngstromL2Test:test_zeroForOneSwapEndingOnInitializedTick()`: total rewards should match tax collected: 9800000000000000 !~= 7000622478505078 (max delta: 10, real delta: 2799377521494922)
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_adjacentTicks()`: first: 30 != 20
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_unalignedWithLargeSpacing()`: assertion failed: 400 != 200
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_variousUnalignedCases()`: No ticks between 47 and 3

| Attack | State | Failure reason |
|---|---|---|
| P1 | blocked | next call did not revert as expected |
| P2 | blocked | next call did not revert as expected |
| P3 | blocked | attack is not profitable: -98235537002744802 <= 0 (profit -0.098 ETH) |
| P4 | blocked | next call did not revert as expected |
| P5 | blocked | next call did not revert as expected |
