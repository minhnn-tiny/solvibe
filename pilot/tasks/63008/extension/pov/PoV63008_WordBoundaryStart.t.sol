// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Held-out variant P5 for finding 63008 (repair input study). Written from the security rule
// before any repair of the study was seen. Same attack as P2, at a bitmap word boundary: tick
// spacing 10, one position [2540, 2560), and a zero-for-one swap that starts exactly on its
// upper tick 2560, which is bit 0 of bitmap word 1. On the audited code the downward walk skips
// the start tick, so the hook subtracts the net liquidity of tick 2540 that it never added, the
// subtraction underflows, and the swap reverts. On a correct walk the swap goes through and
// vm.expectRevert makes this test fail. Runs only offline, against local audited code.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract PoV63008_WordBoundaryStart is AngstromL2Test {
    using TickMath for int24;

    function test_variant_swapDownFromWordBoundary() public {
        PoolKey memory key = initializePool(address(token), 10, 2560);
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, 2540, 2560, 10e21);

        bumpBlock();

        setPriorityFee(0.7 gwei);
        vm.expectRevert();
        router.swap(key, true, -1000e18, int24(2530).getSqrtPriceAtTick());
    }
}
