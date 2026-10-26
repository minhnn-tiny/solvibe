// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Check for a flaw that the LLM security review reported in one agent version of B1,
// reset(TickIteratorUp). It is not a flaw of the human code.
//
// The agent version (Aider with GPT-5.4-mini) returns early when the start tick equals
// the end tick, but leaves currentTick at the start tick. So hasNext() returns true for
// an empty range. The human version sets currentTick to type(int24).max, so hasNext()
// returns false.
//
// Scenario: the pool sits exactly on tick 20. One position over [10, 20) is not active at
// tick 20 and gives tick 20 a net liquidity of -2e22. Another position over [-100, 100)
// is active with 1e22. A small one-for-zero swap that stays inside tick 20 is the first
// swap of the block, so the hook distributes the tax. The tick before and after the swap
// is 20, so the hook builds an upward iterator over the empty range (20, 20].
//
// With the agent version, CompensationPriceFinder.getOneForZero receives tick 20 from the
// iterator and adds its net liquidity again: 1e22 - 2e22 underflows and the swap reverts.
// With the human version, the iterator is empty and the swap goes through.
//
// So this test PASSES when the flaw is present (the swap reverts) and FAILS on the human
// code. Runs only offline in Docker, against a local copy of the audited code 386baff.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract PoV63008_B1_SameTickSwapReverts is AngstromL2Test {
    using TickMath for int24;

    function test_oneForZeroSwapInsideStartTickReverts() public {
        PoolKey memory key = initializePool(address(token), 10, 20);
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, -100, 100, 1e22);
        addLiquidity(key, 10, 20, 2e22);

        bumpBlock();
        setPriorityFee(0.7 gwei);

        // 0.1 token1 in moves the price far less than one tick, so the pool stays on tick 20.
        vm.expectRevert();
        router.swap(key, false, -0.1e18, int24(21).getSqrtPriceAtTick());
    }
}
