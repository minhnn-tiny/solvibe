# R102

- Compiles: True
- Functional suite: 52 passed, 9 failed of 61
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_fuzzing_iterateDown(bytes32)`: panic: arithmetic underflow or overflow (0x11)
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_adjacentTicks()`: first: 10 != 20
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_boundaryExclusion()`: Should include start boundary 100: 0 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_exclusiveBoundaries()`: Should include start boundary 100: 0 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_simple()`: First tick should be 100: 50 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_singleTick()`: Should include start boundary 60
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_unalignedBounds()`: assertion failed: 0 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_unalignedWithLargeSpacing()`: assertion failed
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_variousUnalignedCases()`: assertion failed: 0 != 50

| Attack | State | Failure reason |
|---|---|---|
| P1 | works |  |
| P2 | works |  |
| P3 | works |  (profit 48.877 ETH) |
| P4 | works |  |
| P5 | blocked | next call did not revert as expected |
