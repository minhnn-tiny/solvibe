# R112

- Compiles: True
- Functional suite: 57 passed, 4 failed of 61
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_boundaryExclusion()`: Should include start boundary 100: 0 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_exclusiveBoundaries()`: Should include start boundary 100: 0 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_simple()`: First tick should be 100: 50 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_singleTick()`: Should include start boundary 60

| Attack | State | Failure reason |
|---|---|---|
| P1 | works |  |
| P2 | blocked | next call did not revert as expected |
| P3 | works |  (profit 48.877 ETH) |
| P4 | works |  |
| P5 | blocked | next call did not revert as expected |
