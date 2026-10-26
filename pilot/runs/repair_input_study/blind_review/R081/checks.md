# R081

- Compiles: True
- Functional suite: 58 passed, 3 failed of 61
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_fuzzing_iterateDown(bytes32)`: panic: arithmetic underflow or overflow (0x11)
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_minTick()`: panic: arithmetic underflow or overflow (0x11)
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_noInitializedTicks()`: panic: arithmetic underflow or overflow (0x11)

| Attack | State | Failure reason |
|---|---|---|
| P1 | blocked | next call did not revert as expected |
| P2 | blocked | next call did not revert as expected |
| P3 | blocked | attack is not profitable: -98235537002744802 <= 0 (profit -0.098 ETH) |
| P4 | blocked | next call did not revert as expected |
| P5 | blocked | next call did not revert as expected |
