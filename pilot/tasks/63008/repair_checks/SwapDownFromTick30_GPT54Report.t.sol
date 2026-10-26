// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Check of GPT-5.4's review report on the Aider + GPT-5.4-mini repair of V1 (finding 63008,
// repair round). The report says that with liquidity over [0, 30), tick spacing 10 and the
// pool on tick 30, the repaired downward reset skips tick 30, so a zero-for-one swap reverts
// or rewards use too little liquidity. This test builds exactly that state and swaps down to
// tick 0. If tick 30 is skipped, its net liquidity is never added, the subtraction at tick 0
// underflows, and the swap reverts. The test passes only if the swap goes through. Expected:
// it fails on the audited code 386baff, which has the bug. It passes on a version that walks
// tick 30. Copy it into test/ of a local copy of the code and run it offline, in Docker.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract SwapDownFromTick30_GPT54Report is AngstromL2Test {
    using TickMath for int24;

    function test_swapDownFromTick30WithLiquidityOver0To30() public {
        PoolKey memory key = initializePool(address(token), 10, 30);
        angstrom.setPoolLPFee(key, 50000);
        addLiquidity(key, 0, 30, 10e21);
        bumpBlock();
        setPriorityFee(0.7 gwei);
        router.swap(key, true, -1000e18, int24(0).getSqrtPriceAtTick());
        assertGt(getRewards(key, 0, 30), 0, "the only position earns the tax");
    }
}
