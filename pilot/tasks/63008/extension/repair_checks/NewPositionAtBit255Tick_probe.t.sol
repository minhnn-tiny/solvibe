// SPDX-License-Identifier: UNLICENSED
// Probe used on 2026-10-20 to test a judge report on one repair in the repair input study (finding 63008):
// "the hook writes reward growth to an uninitialized bit-255 tick". It logs the pending rewards of a new
// position whose lower tick is that tick. They were 0 on the repair, on the audited code and on the
// reference repair, so the report was rejected. It has no assertion. Runs only offline.
pragma solidity ^0.8.0;
import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";
import {console2} from "forge-std/console2.sol";
contract RewardsProbe is AngstromL2Test {
    using TickMath for int24;
    function test_probe() public {
        PoolKey memory key = initializePool(address(token), 1, -1);
        angstrom.setPoolLPFee(key, 50000);
        addLiquidity(key, -100, 100, 1e20);
        bumpBlock();
        setPriorityFee(0.7 gwei);
        router.swap(key, true, -1e18, int24(-3).getSqrtPriceAtTick());
        // A new position whose lower tick is -1, the tick the walk may have returned.
        addLiquidity(key, -1, 50, 1e18);
        console2.log("pending new [-1,50):", angstrom.getPendingPositionRewards(key, address(router), -1, 50, bytes32(0)));
        bumpBlock();
        setPriorityFee(0);
        router.swap(key, false, -1e18, int24(10).getSqrtPriceAtTick());
        console2.log("pending new [-1,50) after moving into range:", angstrom.getPendingPositionRewards(key, address(router), -1, 50, bytes32(0)));
        console2.log("pending old [-100,100):", angstrom.getPendingPositionRewards(key, address(router), -100, 100, bytes32(0)));
    }
}
