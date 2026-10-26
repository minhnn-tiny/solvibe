# R053

- Compiles: True
- Functional suite: 49 passed, 12 failed of 61
  - failed: `test/AngstromL2.t.sol:AngstromL2Test:test_simpleZeroForOneSwap1()`: WrappedError(0xb98C751cb4622327CdA0Fd99fF84B1C929df25CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)
  - failed: `test/AngstromL2.t.sol:AngstromL2Test:test_simpleZeroForOneSwap2()`: WrappedError(0xb98C751cb4622327CdA0Fd99fF84B1C929df25CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)
  - failed: `test/AngstromL2.t.sol:AngstromL2Test:test_simpleZeroForOneSwap3()`: WrappedError(0xb98C751cb4622327CdA0Fd99fF84B1C929df25CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)
  - failed: `test/AngstromL2.t.sol:AngstromL2Test:test_simpleZeroForOneSwap4()`: WrappedError(0xb98C751cb4622327CdA0Fd99fF84B1C929df25CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)
  - failed: `test/AngstromL2.t.sol:AngstromL2Test:test_simpleZeroForOneSwap5()`: WrappedError(0xb98C751cb4622327CdA0Fd99fF84B1C929df25CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_fuzzing_iterateDown(bytes32)`: final liquidity invalid: 20564344436900837804980 != 50406919037539351938219
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_boundaryExclusion()`: Should include start boundary 100: 0 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_exclusiveBoundaries()`: Should include start boundary 100: 0 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_simple()`: First tick should be 100: 50 != 100
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_singleTick()`: Should include start boundary 60
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_unalignedTickSpacing60()`: Should get tick 0 first: -120 != 0
  - failed: `test/libraries/TickIteratorDown.t.sol:TickIteratorDownTest:test_iterateDown_variousUnalignedCases()`: assertion failed: -50 != 0

| Attack | State | Failure reason |
|---|---|---|
| P1 | works |  |
| P2 | works |  |
| P3 | works |  (profit 48.877 ETH) |
| P4 | works |  |
| P5 | works |  |
