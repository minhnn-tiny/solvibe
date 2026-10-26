# R108

- Compiles: True
- Functional suite: 60 passed, 1 failed of 61
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_emptyRange()`: Empty range should have no ticks

| Attack | State | Failure reason |
|---|---|---|
| P1 | blocked | next call did not revert as expected |
| P2 | blocked | next call did not revert as expected |
| P3 | blocked | attack is not profitable: -98235537002744802 <= 0 (profit -0.098 ETH) |
| P4 | blocked | next call did not revert as expected |
| P5 | blocked | next call did not revert as expected |
