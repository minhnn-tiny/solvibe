// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Check for the High flaw that GPT-5.4 reported in one agent version of B1,
// reset(TickIteratorUp), written by Aider with GPT-5.4-mini. It is not a flaw of the human code.
//
// The claim: when a one-for-zero swap stays inside the current tick t, the agent's iterator
// still returns t. _oneForZeroCreditRewards then treats t as crossed and adds reward growth to
// rewardGrowthOutsideX128[t]. A position [t - spacing, t) is not active at t, but its pending
// rewards are computed from rewardGrowthOutsideX128[t]. So it earns rewards it is not owed.
//
// Scenario: one active position [-100, 100) with 1e22. An untaxed swap moves the price to the
// middle of tick 20. In a later block, a second position [10, 20) with 0.9e22 is added. It sits
// below the price and is not active. In the next block, a small one-for-zero swap pays the swap
// tax and stays inside tick 20.
//
// With the human code, the iterator is empty, so the inactive position earns nothing.
// With the agent code, the inactive position earns rewards. The hook then owes more in
// rewards than the tax it took, and the extra comes out of ETH it holds for other rewards.
// The owner of the inactive position removes it and is paid in ETH.
//
// So this test PASSES when the flaw is present and FAILS on the human code.
// Runs only offline in Docker, against a local copy of the audited code 386baff.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {UniV4Inspector} from "./_mocks/UniV4Inspector.sol";
import {IUniV4} from "../src/interfaces/IUniV4.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {PoolId, PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {console2} from "forge-std/console2.sol";

contract PoV63008_B1_SameTickRewardsToInactive is AngstromL2Test {
    using PoolIdLibrary for PoolKey;
    using IUniV4 for UniV4Inspector;
    using TickMath for int24;

    function test_inactivePositionEarnsFromSameTickSwap() public {
        PoolKey memory key = initializePool(address(token), 10, 20);
        PoolId id = key.toId();
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, -100, 100, 1e22);

        // Untaxed swap: move the price to the middle of tick 20.
        uint160 p20 = int24(20).getSqrtPriceAtTick();
        uint160 p21 = int24(21).getSqrtPriceAtTick();
        bumpBlock();
        setPriorityFee(0);
        router.swap(key, false, -10_000e18, uint160((uint256(p20) + p21) / 2));
        assertEq(manager.getSlot0(id).tick(), 20, "price left tick 20 after the first swap");

        // Add the inactive position in its own block with no priority fee, so no JIT tax.
        bumpBlock();
        addLiquidity(key, 10, 20, 0.9e22);
        assertEq(getRewards(key, 10, 20), 0, "inactive position starts with rewards");

        // First taxed swap of the next block. It stays inside tick 20.
        bumpBlock();
        setPriorityFee(0.7 gwei);
        uint256 swapTax = angstrom.getSwapTaxAmount(0.7 gwei);
        router.swap(key, false, -0.01e18, p21);
        assertEq(manager.getSlot0(id).tick(), 20, "price left tick 20 after the taxed swap");

        uint256 inactiveRewards = getRewards(key, 10, 20);
        uint256 activeRewards = getRewards(key, -100, 100);
        console2.log("Swap tax:                  %s", swapTax);
        console2.log("Rewards of active [-100,100): %s", activeRewards);
        console2.log("Rewards of inactive [10,20):  %s", inactiveRewards);
        console2.log("Sum of rewards:            %s", activeRewards + inactiveRewards);

        assertGt(inactiveRewards, 0, "inactive position earned no rewards");
        assertGt(activeRewards + inactiveRewards, swapTax, "rewards owed do not exceed the tax");

        // The owner of the inactive position removes it in a later block, with no JIT tax,
        // and receives the rewards in ETH.
        bumpBlock();
        setPriorityFee(0);
        uint256 ethBefore = address(router).balance;
        router.modifyLiquidity(key, 10, 20, -int256(uint256(0.9e22)), bytes32(0));
        uint256 ethReceived = address(router).balance - ethBefore;
        console2.log("ETH paid to inactive [10,20): %s", ethReceived);
        assertEq(ethReceived, inactiveRewards, "inactive position was not paid its rewards");
    }
}
