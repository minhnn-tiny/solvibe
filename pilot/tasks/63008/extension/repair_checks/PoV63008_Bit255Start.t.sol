// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Check for confirming judge or review reports in the repair input study (finding 63008). Not one
// of the frozen attacks: it was written after the runs started, when a repair was seen that
// handles every start tick except one whose compressed position is the last bit (255) of a bitmap
// word. Same attack as P2: tick spacing 10, one position [2530, 2550), and a zero-for-one swap that
// starts exactly on its upper tick 2550, which is bit 255 of bitmap word 0. If the downward walk
// skips the start tick, the hook subtracts the net liquidity of tick 2530 that it never added, the
// subtraction underflows, and the swap reverts, so this test passes. On a correct walk the swap goes
// through and vm.expectRevert makes this test fail. Runs only offline, against local audited code.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract PoV63008_Bit255Start is AngstromL2Test {
    using TickMath for int24;

    function test_check_swapDownFromLastBitOfWord() public {
        PoolKey memory key = initializePool(address(token), 10, 2550);
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, 2530, 2550, 10e21);

        bumpBlock();

        setPriorityFee(0.7 gwei);
        vm.expectRevert();
        router.swap(key, true, -1000e18, int24(2520).getSqrtPriceAtTick());
    }
}
