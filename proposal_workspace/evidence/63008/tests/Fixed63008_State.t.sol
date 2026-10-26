// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Fixed-state test for finding 63008 (version 2 of the evidence package).
//
// Evidence63008_Entitlement asserts the violation, so on fixed code it stops at
// its first failing assertion and never checks that the honest LP is made whole.
// This contract runs the same two scenarios (it reuses _build and _attack from
// that contract, unchanged) and asserts the fixed-state properties directly:
//   1. the honest LP's reward claim succeeds and pays at least what it is owed;
//   2. its full removal succeeds and returns at least its principal;
//   3. the hook's ether backing for LP rewards is at least what the honest LP is owed;
//   4. the attacker's reward is at most its own share of its own swap tax.
// It should PASS on fixed code and FAIL on the vulnerable code.
//
// Tolerance TOL = 1 wei. In the version-1 logs the only gap between amounts that
// should match is 1 wei of rounding: the honest LP was owed 48999999999999999999
// wei for 49e18 wei of tax paid in, and on the fix the hook's backing exceeded
// the honest LP's claim by 1 wei. The claim itself and the attacker's reward
// matched the expected values to the wei.

import {Evidence63008_Entitlement} from "./Evidence63008_Entitlement.t.sol";
import {IUniV4} from "../src/interfaces/IUniV4.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {SqrtPriceMath} from "v4-core/src/libraries/SqrtPriceMath.sol";
import {console} from "forge-std/console.sol";

contract Fixed63008_State is Evidence63008_Entitlement {
    using PoolIdLibrary for PoolKey;

    uint256 constant TOL = 1; // wei, see the header

    // Same parameters as test_entitlement_backing_stealRewards.
    function test_fixed_state_main() public {
        initLiquidity = 1e22;
        buildLoops = 5;
        buildPriorityFee = 1000 gwei;
        attackerPriorityFee = 5 gwei;
        tickSpacing = 10;
        initT0 = 0;
        initT1 = 50;
        startTick = 17;
        attackUpper = 20;
        attackLower = 10;
        _build();
        _attack();
        _checkFixed();
    }

    // Same parameters as test_entitlement_backing_variant_boundary30.
    function test_fixed_state_variant_boundary30() public {
        initLiquidity = 1e22;
        buildLoops = 5;
        buildPriorityFee = 1000 gwei;
        attackerPriorityFee = 5 gwei;
        tickSpacing = 10;
        initT0 = 0;
        initT1 = 50;
        startTick = 23;
        attackUpper = 30;
        attackLower = 20;
        _build();
        _attack();
        _checkFixed();
    }

    function _checkFixed() internal {
        honestPendingAfter =
            angstrom.getPendingPositionRewards(key, address(honestLp), initT0, initT1, 0);
        etherBackingLpRewards = _hookEther() - angstrom.unclaimedProtocolRevenueInEther();

        // The attacker's share of its own tax. During the taxed swap the price
        // moves from the boundary tick down by one tick, and only two positions
        // are in range there: the honest LP and the attacker.
        uint256 attackerShare = swapTax * attackLiquidity / (attackLiquidity + initLiquidity);

        // The honest LP's principal at the current price (rounded down, as on removal).
        uint160 sqrtP = IUniV4.getSlot0(IPoolManager(address(manager)), key.toId()).sqrtPriceX96();
        uint256 principal0 = SqrtPriceMath.getAmount0Delta(
            sqrtP, TickMath.getSqrtPriceAtTick(initT1), initLiquidity, false
        );
        uint256 principal1 = SqrtPriceMath.getAmount1Delta(
            TickMath.getSqrtPriceAtTick(initT0), sqrtP, initLiquidity, false
        );

        // Honest LP claims rewards only, in a later block.
        bumpBlock();
        setPriorityFee(0);
        uint256 eth0 = address(honestLp).balance;
        try honestLp.modifyLiquidity(key, initT0, initT1, 0, 0) {
            claimOk = true;
        } catch {}
        rewardsClaimed = address(honestLp).balance - eth0;

        // Honest LP removes all its liquidity.
        uint256 tok0 = token.balanceOf(address(honestLp));
        eth0 = address(honestLp).balance;
        try honestLp.modifyLiquidity(key, initT0, initT1, -int256(uint256(initLiquidity)), 0) {
            removeOk = true;
        } catch {}
        uint256 ethBack = address(honestLp).balance - eth0;
        uint256 tokBack = token.balanceOf(address(honestLp)) - tok0;

        console.log("=== FIXED-STATE CHECK ===");
        console.log("honest LP owed before attack (wei):    ", honestPendingBefore);
        console.log("honest LP owed at claim time (wei):    ", honestPendingAfter);
        console.log("hook ether backing LP rewards (wei):   ", etherBackingLpRewards);
        console.log("attacker reward (wei):                 ", attackRewards);
        console.log("attacker share of own swap tax (wei):  ", attackerShare);
        console.log("honest LP claim succeeded:             ", claimOk);
        console.log("honest LP rewards received (wei):      ", rewardsClaimed);
        console.log("honest LP removal succeeded:           ", removeOk);
        console.log("principal ether at current price (wei):", principal0);
        console.log("ether returned on removal (wei):       ", ethBack);
        console.log("principal token at current price:      ", principal1);
        console.log("token returned on removal (token wei): ", tokBack);

        assertTrue(claimOk, "honest LP reward claim reverted");
        assertGe(rewardsClaimed + TOL, honestPendingAfter, "honest LP paid less than owed at claim time");
        assertGe(rewardsClaimed + TOL, honestPendingBefore, "honest LP paid less than owed before the attack");
        assertTrue(removeOk, "honest LP removal reverted");
        assertGe(ethBack, principal0, "removal returned less ether than the principal");
        assertGe(tokBack, principal1, "removal returned less token than the principal");
        assertGe(etherBackingLpRewards + TOL, honestPendingAfter, "hook backing below what the honest LP is owed");
        assertLe(attackRewards, attackerShare + TOL, "attacker reward above its share of its own swap tax");
    }
}
