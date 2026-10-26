// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Check for confirming judge reports in the repair input study (finding 63008): a repair that, when
// the start tick's compressed position is bit 255 of a bitmap word, returns that word's last tick
// without checking that it is initialized. With tick spacing 1 and the price at tick -1 (bit 255 of
// word -1), the walk then returns tick -1, which no position uses, as if the swap crossed it. The
// test passes when the taxed zero-for-one swap reverts. On a walk that returns only initialized ticks
// the swap goes through and vm.expectRevert makes this test fail.
// Runs only offline, against local audited code.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract UninitializedBit255Tick is AngstromL2Test {
    using TickMath for int24;

    function test_check_swapDownFromBit255WithNoTickThere() public {
        PoolKey memory key = initializePool(address(token), 1, -1);
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, -100, 100, 1e20);

        bumpBlock();
        setPriorityFee(1);
        vm.expectRevert();
        router.swap(key, true, -1e15, int24(-3).getSqrtPriceAtTick());
    }
}
