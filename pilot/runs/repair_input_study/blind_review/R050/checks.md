# R050

- Compiles: True
- Functional suite: 56 passed, 5 failed of 61
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_fuzzing_iterateDown(bytes32)`: final liquidity invalid: 0 != 34705804167044144048723
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_boundaryExclusion()`: Should include start boundary 100: 0 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_exclusiveBoundaries()`: Should include start boundary 100: 0 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_simple()`: First tick should be 100: 50 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_singleTick()`: Should include start boundary 60

| Attack | State | Failure reason |
|---|---|---|
| P1 | works |  |
| P2 | works |  |
| P3 | works |  (profit 48.877 ETH) |
| P4 | works |  |
| P5 | works |  |
