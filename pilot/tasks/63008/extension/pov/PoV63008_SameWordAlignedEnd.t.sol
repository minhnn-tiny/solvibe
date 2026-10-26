// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Held-out variant P4 for finding 63008 (repair input study). Written from the security rule
// before any repair of the study was seen. Same attack as P2, at other boundaries: tick
// spacing 60, one position [60, 180), and a zero-for-one swap that starts exactly on its upper
// tick (180) and stops at tick 0. The start and end ticks are in the same bitmap word, and the
// end tick is a multiple of the tick spacing. On the audited code the downward walk skips the
// start tick, so the hook subtracts the net liquidity of tick 60 that it never added, the
// subtraction underflows, and the swap reverts. On a correct walk the swap goes through and
// vm.expectRevert makes this test fail. Runs only offline, against local audited code.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract PoV63008_SameWordAlignedEnd is AngstromL2Test {
    using TickMath for int24;

    function test_variant_swapDownFromBoundarySameWord() public {
        PoolKey memory key = initializePool(address(token), 60, 180);
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, 60, 180, 10e21);

        bumpBlock();

        setPriorityFee(0.7 gwei);
        vm.expectRevert();
        router.swap(key, true, -1000e18, int24(0).getSqrtPriceAtTick());
    }
}
