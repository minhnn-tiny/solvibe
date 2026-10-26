// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

// Check for confirming a judge report in the repair input study (finding 63008): "Downward reset
// scans bitmap words past endTick, so taxed zero-for-one swaps run out of gas when no initialized
// tick lies below the start" (Claude Opus 5.5 on one repair). All liquidity sits above the price,
// and a taxed (top-of-block) zero-for-one swap moves the price down. The test passes when the swap
// uses more gas than a 30,000,000-gas block holds, which is the reported flaw. On a walk that stops
// at the end tick, the swap fits in a block and the test fails at the gas assertion.
// Runs only offline, against local audited code.

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract SwapDownNoTickBelow is AngstromL2Test {
    using TickMath for int24;

    function test_check_taxedSwapDownWithNoInitializedTickBelow() public {
        PoolKey memory key = initializePool(address(token), 10, 0);
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, 100, 200, 10e21);

        bumpBlock();

        setPriorityFee(0.7 gwei);
        uint256 before = gasleft();
        router.swap(key, true, -1e18, int24(-50).getSqrtPriceAtTick());
        uint256 used = before - gasleft();
        assertGt(used, 30_000_000, "swap fits in a block");
    }
}
