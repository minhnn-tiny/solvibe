// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Second Proof of Vulnerability for finding 63008 (Cyfrin, Sorella L2 Angstrom).
// Same bug as PoV63008_AngstromL2.t.sol: TickIteratorLib.reset seeds the downward
// iterator at `startTick` instead of `startTick + 1`, so a zero-for-one swap that
// starts exactly on a position's upper boundary tick skips that tick.
//
// This test is the report's Proof of Concept #1. It reaches the bug by a different
// path from PoC #2. A wide position [-50, 50) is opened, the price is pushed up to
// tick 30, and a second position [10, 30) is opened whose upper tick is the current
// tick. The swap back down skips tick 30, so the liquidity of [10, 30) is never
// added, and the subtraction at tick 10 underflows in
// AngstromL2._zeroForOneCreditRewards (AngstromL2.sol line 364 at 386baff).
// PoC #2 underflows in CompensationPriceFinder.getZeroForOne instead.
//
// One change from the report: the report's test ends with the reverting swap and
// no expectation, so it fails on the vulnerable code. Here the swap is wrapped in
// vm.expectRevert(), so the test PASSES on the vulnerable code and FAILS on the
// fix. That is the same oracle as PoC #2.
//
// Source: data_collection/tier1_after_2025-08-31/63008.md (published Cyfrin PoC #1).
// Run scoped with --match-path so the inherited AngstromL2Test suite is not re-run.
// Runs only offline, against local audited code.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {UniV4Inspector} from "./_mocks/UniV4Inspector.sol";
import {IUniV4} from "../src/interfaces/IUniV4.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {PoolId, PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract PoV63008_BoundaryAddLiquidity is AngstromL2Test {
    using PoolIdLibrary for PoolKey;
    using IUniV4 for UniV4Inspector;
    using TickMath for int24;

    function test_cyfrin_swapToBoundaryAddLiqudityAndSwapBackForRevert() public {
        uint256 PRIORITY_FEE = 0.7 gwei;
        int24 INIT_T0 = -50;
        int24 INIT_T1 = 50;
        int24 T0 = 10;
        int24 T1 = 30;

        /* Preconditions */
        assertGt(T0, INIT_T0, "precondition: T0 > INIT_T0");
        assertLt(T1, INIT_T1, "precondition: T1 < INIT_T1");

        PoolKey memory key = initializePool(address(token), 10, 3);
        PoolId id = key.toId();

        angstrom.setPoolLPFee(key, 0.005e6);
        setPriorityFee(PRIORITY_FEE);

        addLiquidity(key, INIT_T0, INIT_T1, 10e21);
        bumpBlock();
        router.swap(key, false, -1000e18, int24(T1).getSqrtPriceAtTick());
        int24 currentTick = manager.getSlot0(id).tick();
        assertEq(currentTick, T1, "precondition: After swap must be sitting on T1");

        addLiquidity(key, T0, T1, 10e21);

        // Now swap back. On the vulnerable code this underflows and reverts.
        bumpBlock();
        vm.expectRevert();
        router.swap(key, true, -1000e18, int24(INIT_T0 - 1).getSqrtPriceAtTick());
    }
}
