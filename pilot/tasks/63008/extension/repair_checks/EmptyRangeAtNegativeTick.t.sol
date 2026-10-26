// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Check for confirming judge reports in the repair input study (finding 63008): when a taxed
// zero-for-one swap does not move the pool's tick, the hook walks an empty range (start tick equals
// end tick). A repair that returns early without setting the current tick leaves it at 0, so at a
// negative tick the walk returns tick 0 and the ticks below it. Here tick 0 carries the net liquidity
// of a position [0, 100) that is larger than the active liquidity, so the hook's subtraction
// underflows and the swap reverts, and the test passes. Where the empty range yields no tick that
// changes the liquidity, the swap goes through and vm.expectRevert makes this test fail.
// Runs only offline, against local audited code.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract EmptyRangeAtNegativeTick is AngstromL2Test {
    using TickMath for int24;

    function test_check_taxedSwapThatKeepsANegativeTick() public {
        PoolKey memory key = initializePool(address(token), 10, -10);
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, -100, 100, 1e20);
        addLiquidity(key, 0, 100, 2e20);

        // Move the price a little above tick -10, inside the same tick, with no tax.
        bumpBlock();
        router.swap(key, false, -1e15, int24(-9).getSqrtPriceAtTick());

        // A taxed zero-for-one swap that stops at tick -10's price, so the tick stays -10.
        bumpBlock();
        setPriorityFee(1);
        vm.expectRevert();
        router.swap(key, true, -1e15, int24(-10).getSqrtPriceAtTick());
    }
}
