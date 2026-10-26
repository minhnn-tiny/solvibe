// Regression tests for finding 63008 (repair input study). This is test/libraries/TickIterator.t.sol
// at the audited commit 386baff with its 14 downward tests removed. Those tests expect the start
// tick to be skipped, which is the bug. TickIteratorDown.t.sol replaces them.
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {
    TickIteratorLib, TickIteratorUp, TickIteratorDown
} from "../../src/libraries/TickIterator.sol";
import {IPoolManager} from "v4-core/src/interfaces/IPoolManager.sol";
import {PoolId, PoolIdLibrary} from "v4-core/src/types/PoolId.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {Currency} from "v4-core/src/types/Currency.sol";
import {IHooks} from "v4-core/src/interfaces/IHooks.sol";
import {IUniV4} from "../../src/interfaces/IUniV4.sol";
import {BaseTest} from "../_helpers/BaseTest.sol";
import {RouterActor} from "../_mocks/RouterActor.sol";
import {UniV4Inspector} from "../_mocks/UniV4Inspector.sol";
import {MockERC20} from "super-sol/mocks/MockERC20.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract TickIteratorTest is BaseTest {
    using PoolIdLibrary for PoolKey;
    using IUniV4 for IPoolManager;

    UniV4Inspector manager;
    RouterActor router;
    PoolId pid;
    PoolKey key;

    MockERC20 token0;
    MockERC20 token1;

    int24 constant TICK_SPACING = 10;
    uint160 constant INIT_SQRT_PRICE = 79228162514264337593543950336; // 1:1 price

    function setUp() public {
        // Deploy UniV4Inspector (which is a PoolManager with view functions)
        manager = new UniV4Inspector();
        router = new RouterActor(manager);

        // Deploy and sort tokens
        token0 = new MockERC20();
        token1 = new MockERC20();

        if (address(token1) < address(token0)) {
            (token0, token1) = (token1, token0);
        }

        // Set up pool key
        key = PoolKey({
            currency0: Currency.wrap(address(token0)),
            currency1: Currency.wrap(address(token1)),
            fee: 3000,
            tickSpacing: TICK_SPACING,
            hooks: IHooks(address(0))
        });

        pid = key.toId();

        // Initialize pool
        manager.initialize(key, INIT_SQRT_PRICE);

        // Fund the router with tokens for liquidity operations
        token0.mint(address(router), 1e30);
        token1.mint(address(router), 1e30);
    }

    // Helper to add liquidity at specific tick range
    function addLiquidityAtTicks(int24 tickLower, int24 tickUpper) internal {
        require(tickLower % TICK_SPACING == 0, "Lower tick not aligned");
        require(tickUpper % TICK_SPACING == 0, "Upper tick not aligned");
        require(tickLower < tickUpper, "Invalid range");

        // Calculate liquidity amount (simplified - just use a fixed amount)
        uint128 liquidity = 1e18;

        // Use RouterActor to add liquidity
        router.modifyLiquidity(key, tickLower, tickUpper, int256(uint256(liquidity)), bytes32(0));
    }

    // ============ Upward Iteration Tests ============

    function test_iterateUp_simple() public {
        // Add liquidity at specific ticks: -100, -50, 0, 50, 100
        addLiquidityAtTicks(-100, -50);
        addLiquidityAtTicks(-50, 0);
        addLiquidityAtTicks(0, 50);
        addLiquidityAtTicks(50, 100);
        addLiquidityAtTicks(100, 150);

        // Start is exclusive (-100 not included), end is inclusive (100 included)
        // Should get: -50, 0, 50, 100
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, TICK_SPACING, -100, 100);

        // Should iterate through initialized ticks
        assertTrue(iter.hasNext(), "Should have first tick");
        assertEq(iter.getNext(), -50, "First tick should be -50");

        assertTrue(iter.hasNext(), "Should have second tick");
        assertEq(iter.getNext(), 0, "Second tick should be 0");

        assertTrue(iter.hasNext(), "Should have third tick");
        assertEq(iter.getNext(), 50, "Third tick should be 50");

        assertTrue(iter.hasNext(), "Should have fourth tick");
        assertEq(iter.getNext(), 100, "Fourth tick should be 100");

        assertFalse(iter.hasNext(), "Should have no more ticks");
    }

    function test_iterateUp_exclusiveBoundaries() public {
        // Test that boundaries are exclusive
        addLiquidityAtTicks(-200, -100);
        addLiquidityAtTicks(-100, 0);
        addLiquidityAtTicks(0, 100);
        addLiquidityAtTicks(100, 200);

        // Start is exclusive (-100 not included), end is inclusive (100 included)
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, TICK_SPACING, -100, 100);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 0, "Should exclude start boundary -100");

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 100, "Should include end boundary 100");

        assertFalse(iter.hasNext());
    }

    function test_iterateUp_acrossWords() public {
        // Test iteration across word boundaries (256 ticks per word when compressed)
        // Word boundary is at compressed tick 256, which is tick 2560 with spacing 10
        addLiquidityAtTicks(-2570, -2560);
        addLiquidityAtTicks(-2560, -2550);
        addLiquidityAtTicks(-10, 0);
        addLiquidityAtTicks(0, 10);
        addLiquidityAtTicks(2550, 2560);
        addLiquidityAtTicks(2560, 2570);
        addLiquidityAtTicks(2570, 2580);

        // Exclusive bounds: (-3000, 3000)
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, TICK_SPACING, -3000, 3000);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), -2570);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), -2560);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), -2550);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), -10);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 0);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 10);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 2550);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 2560);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 2570);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 2580);

        assertFalse(iter.hasNext());
    }

    function test_iterateUp_noInitializedTicks() public view {
        // No liquidity added, so no initialized ticks
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, TICK_SPACING, -100, 100);

        assertFalse(iter.hasNext(), "Should have no ticks in empty range");
    }

    function test_iterateUp_singleTick() public {
        addLiquidityAtTicks(40, 60);

        // Test iteration over position boundaries with exclusive bounds
        // When adding liquidity from 40 to 60, ticks 40 and 60 are initialized
        // Start is exclusive (40 not included), end is inclusive (60 included)
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, TICK_SPACING, 40, 60);

        // Should have tick 60 (end boundary is included)
        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 60, "Should include end boundary 60");

        assertFalse(iter.hasNext());

        // To get the boundary ticks, need to expand range
        TickIteratorUp memory iter2 = TickIteratorLib.initUp(manager, pid, TICK_SPACING, 30, 70);

        assertTrue(iter2.hasNext());
        assertEq(iter2.getNext(), 40, "First tick should be 40");

        assertTrue(iter2.hasNext());
        assertEq(iter2.getNext(), 60, "Second tick should be 60");

        assertFalse(iter2.hasNext());
    }

    function test_iterateUp_maxTick() public view {
        // Test near maximum tick (must be aligned to tick spacing)
        /// forge-lint: disable-next-line(divide-before-multiply)
        int24 maxAlignedTick = (TickMath.MAX_TICK / TICK_SPACING) * TICK_SPACING;
        int24 nearMaxTick = maxAlignedTick - TICK_SPACING;

        // Can't actually add liquidity at MAX_TICK, so test iteration behavior
        TickIteratorUp memory iter =
            TickIteratorLib.initUp(manager, pid, TICK_SPACING, nearMaxTick, maxAlignedTick);

        // No liquidity there, so should have no ticks
        assertFalse(iter.hasNext());
    }

    // ============ Downward Iteration Tests ============

    // ============ Edge Cases ============

    function test_iterateUp_emptyRange() public view {
        // When start == end, the range includes just that point
        // Since no liquidity at tick 100, should have no ticks
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, TICK_SPACING, 100, 100);
        assertFalse(iter.hasNext(), "No initialized tick at position 100");
    }

    function test_iterateUp_partialRange() public {
        addLiquidityAtTicks(-200, -100);
        addLiquidityAtTicks(-100, 0);
        addLiquidityAtTicks(0, 100);
        addLiquidityAtTicks(100, 200);

        // Only iterate middle portion with exclusive bounds (-50, 50)
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, TICK_SPACING, -50, 50);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 0, "Should only get tick within range");

        assertFalse(iter.hasNext());
    }

    function test_iterateUp_unalignedBounds() public {
        // Test with unaligned start/end ticks
        addLiquidityAtTicks(-100, 0);
        addLiquidityAtTicks(0, 100);
        addLiquidityAtTicks(100, 200);

        // Start at -99 (unaligned), end at 101 (unaligned)
        // Exclusive bounds mean we get ticks in range (-99, 101)
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, TICK_SPACING, -99, 101);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 0, "Should get tick 0");

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 100, "Should get tick 100");

        assertFalse(iter.hasNext());
    }

    function test_iterateUp_unalignedTickSpacing60() public {
        // Change to tick spacing 60 for this test
        key = PoolKey({
            currency0: Currency.wrap(address(token0)),
            currency1: Currency.wrap(address(token1)),
            fee: 3000,
            tickSpacing: 60,
            hooks: IHooks(address(0))
        });
        pid = key.toId();
        manager.initialize(key, INIT_SQRT_PRICE);

        // Add liquidity at aligned ticks for spacing 60
        router.modifyLiquidity(key, -120, 0, int256(1e18), bytes32(0));
        router.modifyLiquidity(key, 0, 120, int256(1e18), bytes32(0));
        router.modifyLiquidity(key, 120, 240, int256(1e18), bytes32(0));

        // Test with unaligned start tick 39 (not divisible by 60)
        // With exclusive bounds (39, 180):
        // - Start is 39, so we begin searching from tick 60 (next aligned tick after 39)
        // - End is 180, so we stop before 180
        // - Initialized ticks in range: 120 (tick 60 is not initialized, only 0 and 120 are)
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, 60, 39, 180);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 120, "Should get tick 120");

        assertFalse(iter.hasNext(), "Should not have more ticks");
    }

    function test_iterateUp_boundaryExclusion() public {
        // Test that exact boundary ticks are excluded
        addLiquidityAtTicks(-100, 0);
        addLiquidityAtTicks(0, 100);
        addLiquidityAtTicks(100, 200);

        // Start is exclusive (-100 not included), end is inclusive (100 included)
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, TICK_SPACING, -100, 100);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 0, "First tick should be 0");

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 100, "Should include end boundary 100");

        assertFalse(iter.hasNext());
    }

    function test_iterateUp_adjacentTicks() public {
        // Test iteration with adjacent initialized ticks
        addLiquidityAtTicks(0, 10);
        addLiquidityAtTicks(10, 20);
        addLiquidityAtTicks(20, 30);

        // Exclusive bounds (-5, 25) should give us 0, 10, 20
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, TICK_SPACING, -5, 25);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 0);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 10);

        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 20);

        assertFalse(iter.hasNext());
    }

    // ============ Additional Unaligned Tick Tests ============

    function test_iterateUp_variousUnalignedCases() public {
        // Test various unaligned tick scenarios with tick spacing 10
        addLiquidityAtTicks(-100, -50);
        addLiquidityAtTicks(-50, 0);
        addLiquidityAtTicks(0, 50);
        addLiquidityAtTicks(50, 100);

        // Case 1: Start at 3 (unaligned), end at 47 (unaligned)
        // Should iterate through ticks in range (3, 47): none in this case since next is 50
        TickIteratorUp memory iter1 = TickIteratorLib.initUp(manager, pid, TICK_SPACING, 3, 47);
        assertFalse(iter1.hasNext(), "No ticks between 3 and 47");

        // Case 2: Start at -53 (unaligned), end at 53 (unaligned)
        // Should iterate through ticks in range (-53, 53): -50, 0, 50
        TickIteratorUp memory iter2 = TickIteratorLib.initUp(manager, pid, TICK_SPACING, -53, 53);
        assertTrue(iter2.hasNext());
        assertEq(iter2.getNext(), -50);
        assertTrue(iter2.hasNext());
        assertEq(iter2.getNext(), 0);
        assertTrue(iter2.hasNext());
        assertEq(iter2.getNext(), 50);
        assertFalse(iter2.hasNext());

        // Case 3: Start at -51 (unaligned), end at 1 (unaligned)
        // Should iterate through ticks in range (-51, 1): -50, 0
        TickIteratorUp memory iter3 = TickIteratorLib.initUp(manager, pid, TICK_SPACING, -51, 1);
        assertTrue(iter3.hasNext());
        assertEq(iter3.getNext(), -50);
        assertTrue(iter3.hasNext());
        assertEq(iter3.getNext(), 0);
        assertFalse(iter3.hasNext());
    }

    function test_iterateUp_unalignedWithLargeSpacing() public {
        // Test with tick spacing 200 and various unaligned positions
        key = PoolKey({
            currency0: Currency.wrap(address(token0)),
            currency1: Currency.wrap(address(token1)),
            fee: 10000,
            tickSpacing: 200,
            hooks: IHooks(address(0))
        });
        pid = key.toId();
        manager.initialize(key, INIT_SQRT_PRICE);

        // Add liquidity at aligned ticks for spacing 200
        router.modifyLiquidity(key, -600, -400, int256(1e18), bytes32(0));
        router.modifyLiquidity(key, -400, -200, int256(1e18), bytes32(0));
        router.modifyLiquidity(key, -200, 0, int256(1e18), bytes32(0));
        router.modifyLiquidity(key, 0, 200, int256(1e18), bytes32(0));
        router.modifyLiquidity(key, 200, 400, int256(1e18), bytes32(0));

        // Test with start tick 39 (39 % 200 = 39, heavily unaligned)
        // Exclusive bounds (39, 350)
        // Next aligned tick after 39 is 200, before 350 is 200
        // So we should only get tick 200
        TickIteratorUp memory iter = TickIteratorLib.initUp(manager, pid, 200, 39, 350);
        assertTrue(iter.hasNext());
        assertEq(iter.getNext(), 200);
        assertFalse(iter.hasNext());

        // Test with start tick -199 (just after -200)
        // Exclusive bounds (-199, 201)
        // Should get 0, 200
        TickIteratorUp memory iter2 = TickIteratorLib.initUp(manager, pid, 200, -199, 201);
        assertTrue(iter2.hasNext());
        assertEq(iter2.getNext(), 0);
        assertTrue(iter2.hasNext());
        assertEq(iter2.getNext(), 200);
        assertFalse(iter2.hasNext());
    }
}
