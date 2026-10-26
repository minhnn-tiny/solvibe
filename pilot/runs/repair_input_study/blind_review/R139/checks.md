# R139

- Compiles: True
- Functional suite: 59 passed, 2 failed of 61
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_exclusiveBoundaries()`: Should include start boundary 100: 0 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_simple()`: First tick should be 100: 50 != 100

| Attack | State | Failure reason |
|---|---|---|
| P1 | blocked | next call did not revert as expected |
| P2 | blocked | next call did not revert as expected |
| P3 | blocked | attack is not profitable: -98235537002744802 <= 0 (profit -0.098 ETH) |
| P4 | blocked | next call did not revert as expected |
| P5 | blocked | next call did not revert as expected |
