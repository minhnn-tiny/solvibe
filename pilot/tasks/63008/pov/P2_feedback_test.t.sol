// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract SwapFromTickBoundaryTest is AngstromL2Test {
    using TickMath for int24;

    function test_swapDownFromTickBoundary() public {
        uint256 PRIORITY_FEE = 0.7 gwei;
        PoolKey memory key = initializePool(address(token), 10, 20);
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, -10, 20, 10e21);
        assertEq(getRewards(key, -10, 20), 0);

        bumpBlock();

        setPriorityFee(PRIORITY_FEE);
        router.swap(key, true, -1000e18, int24(-10).getSqrtPriceAtTick());
    }
}
