# Fix a reported vulnerability

## Context

You are working in a Foundry project for a Uniswap V4 hook. The function `reset(TickIteratorDown memory self, int24 startTick)` in `src/libraries/TickIterator.sol` was written from the requirement below. The requirement is also in `FEATURE_REQUEST.md`.

<requirement>
# Implement `reset` for the downward tick iterator in `src/libraries/TickIterator.sol`

`TickIteratorLib` walks the initialized ticks of a Uniswap V4 pool, with one iterator for each direction. The hook uses the downward iterator during a zero-for-one swap. It starts at the pool's tick before the swap, moves toward the tick after the swap, and adds up the liquidity change at each initialized tick it meets. `initDown` stores the pool manager, the pool ID, the tick spacing and the end tick, then calls `reset`. The hook also calls `reset` itself to point an existing iterator at a new start tick.

Do not change the signature:

```solidity
function reset(TickIteratorDown memory self, int24 startTick) internal view
```

Required behaviour:

1. `self.manager`, `self.poolId`, `self.tickSpacing` and `self.endTick` are already set when `reset` runs.
2. The walk goes from `startTick` down to `self.endTick`. If `self.endTick` is greater than `startTick`, revert with `InvalidRange()`.
3. Active liquidity follows the Uniswap rule. A position over `[lower, upper)` is active at tick `t` when `lower <= t < upper`.
4. After `reset`, repeated calls to `getNext` must return the initialized ticks the walk needs, from high to low, and no others. A tick is needed if this holds. Start with the active liquidity at `startTick`. Subtract the net liquidity of each returned tick, in order. The result must equal the active liquidity at `self.endTick`.
5. Point 4 must hold for every start and end tick in range, whether or not they are initialized, and whether or not they are multiples of the tick spacing.
6. If `startTick` equals `self.endTick`, `hasNext` must return false straight away.
7. Load the bitmap word where the walk begins from the pool manager. Leave the iterator in the state that `hasNext`, `getNext` and `_advanceToNextDown` expect. Use the helpers already in the library and in `TickLib`.

Change only the body of this function. Leave every other function, the struct layouts and the `InvalidRange` error as they are.
</requirement>

## Report

A security reviewer found a vulnerability in the current code. They sent this test as proof. The test fails on the current code.

Test file: `test/SwapFromTickBoundary.t.sol`

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {AngstromL2Test} from "./AngstromL2.t.sol";
import {PoolKey} from "v4-core/src/types/PoolKey.sol";
import {TickMath} from "v4-core/src/libraries/TickMath.sol";

contract SwapFromTickBoundaryTest is AngstromL2Test {
    using TickMath for int24;

    function test_swapDownFromTickBoundary() public {
        uint256 PRIORITY_FEE = 0.7 gwei;
        PoolKey memory key = initializePool(address(token), 10, 20);
        angstrom.setPoolLPFee(key, 50000);

        addLiquidity(key, -10, 20, 10e21);
        assertEq(getRewards(key, -10, 20), 0);

        bumpBlock();

        setPriorityFee(PRIORITY_FEE);
        router.swap(key, true, -1000e18, int24(-10).getSqrtPriceAtTick());
    }
}
```

Command:

```sh
forge test --match-path test/SwapFromTickBoundary.t.sol --match-test test_swapDownFromTickBoundary -vvv
```

Output on the current code:

```text
Compiling 96 files with Solc 0.8.26
Solc 0.8.26 finished in 4.67s
Compiler run successful with warnings:
Warning (5574): Contract code size is 25282 bytes and exceeds 24576 bytes (a limit introduced in Spurious Dragon). This contract may not be deployable on Mainnet. Consider enabling the optimizer (with a low "runs" value!), turning off revert strings, or using libraries.
  --> test/_mocks/UniV4Inspector.sol:12:1:
   |
12 | contract UniV4Inspector is PoolManager {
   | ^ (Relevant source part starts here and spans across multiple lines).

test/SwapFromTickBoundary.t.sol:SwapFromTickBoundaryTest
  ↪ Suite result: FAILED. 0 passed; 1 failed; 0 skipped; finished in 192.34ms (9.08ms CPU time)

Ran 1 test for test/SwapFromTickBoundary.t.sol:SwapFromTickBoundaryTest
[FAIL: WrappedError(0x2F4a764787704A3F250fdC267b6D228bB1E625CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)] test_swapDownFromTickBoundary() (gas: 433875)
Traces:
  [433875] SwapFromTickBoundaryTest::test_swapDownFromTickBoundary()
    ├─ [34428] UniV4Inspector::initialize(PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), 79307426338960776842885539845 [7.93e28])
    │   ├─ [1026] AngstromL2::beforeInitialize(SwapFromTickBoundaryTest: [0x7FA9385bE102ac3EAc297483Dd6233D62b3e1496], PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), 79307426338960776842885539845 [7.93e28])
    │   │   └─ ← [Return] 0xdc98354e
    │   ├─ emit Initialize(id: 0x4827e52229b38a6747ca4a003298e909eabb78a9a81df26eb989e7b9e6cf903b, currency0: 0x0000000000000000000000000000000000000000, currency1: MockERC20: [0xF62849F9A0B5Bf2913b396098F7c7019b51A820a], fee: 8388608 [8.388e6], tickSpacing: 10, hooks: AngstromL2: [0x2F4a764787704A3F250fdC267b6D228bB1E625CB], sqrtPriceX96: 79307426338960776842885539845 [7.93e28], tick: 20)
    │   └─ ← [Return] 20
    ├─ [8174] AngstromL2::setPoolLPFee(PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), 50000 [5e4])
    │   ├─ [1756] UniV4Inspector::updateDynamicLPFee(PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), 50000 [5e4])
    │   │   └─ ← [Stop]
    │   ├─ emit PoolLPFeeUpdated(key: PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), newFee: 50000 [5e4])
    │   └─ ← [Stop]
    ├─ [209122] RouterActor::modifyLiquidity(PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), -10, 20, 10000000000000000000000 [1e22], 0x0000000000000000000000000000000000000000000000000000000000000000)
    │   ├─ [204153] UniV4Inspector::unlock(0x020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f62849f9a0b5bf2913b396098f7c7019b51a820a0000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000002f4a764787704a3f250fdc267b6d228bb1e625cbfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff6000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000021e19e0c9bab24000000000000000000000000000000000000000000000000000000000000000000000)
    │   │   ├─ [201960] RouterActor::unlockCallback(0x020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f62849f9a0b5bf2913b396098f7c7019b51a820a0000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000002f4a764787704a3f250fdc267b6d228bb1e625cbfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff6000000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000021e19e0c9bab24000000000000000000000000000000000000000000000000000000000000000000000)
    │   │   │   ├─ [159921] UniV4Inspector::modifyLiquidity(PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), ModifyLiquidityParams({ tickLower: -10, tickUpper: 20, liquidityDelta: 10000000000000000000000 [1e22], salt: 0x0000000000000000000000000000000000000000000000000000000000000000 }), 0x)
    │   │   │   │   ├─ emit ModifyLiquidity(id: 0x4827e52229b38a6747ca4a003298e909eabb78a9a81df26eb989e7b9e6cf903b, sender: RouterActor: [0x2e234DAe75C793f67A35089C9d99245E1C58470b], tickLower: -10, tickUpper: 20, liquidityDelta: 10000000000000000000000 [1e22], salt: 0x0000000000000000000000000000000000000000000000000000000000000000)
    │   │   │   │   ├─ [16167] AngstromL2::afterAddLiquidity(RouterActor: [0x2e234DAe75C793f67A35089C9d99245E1C58470b], PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), ModifyLiquidityParams({ tickLower: -10, tickUpper: 20, liquidityDelta: 10000000000000000000000 [1e22], salt: 0x0000000000000000000000000000000000000000000000000000000000000000 }), 340282366920938463448371605881628173655 [3.402e38], 0, 0x)
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0xc1108968e21775cb3d744cb8fc7ecb9a74e9772a696b88ad06dad3af019a898c) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x00000000c3500000000000140000000000000001004190c48bf915addfe52805
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0x02ae49a4fdb34522637867549dbeb7a7f900bf7de03ebe415bf120d133c635c6) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x8000000000000000000000000000000000000000000000000000000000000000
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0xb9576465fb459f3ba9568b76168f55ea6b3299fe02dc54f5dc1c06005b81e228) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x0000000000000000000000000000000000000000000000000000000000000004
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0x78ce598a51bb45907b8df6a62182d04f4e345acf6ced0d1caf5ce9b25e20c62f) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x00000000000000000000000000000000000000000000021e19e0c9bab2400000
    │   │   │   │   │   └─ ← [Return] 0x9f063efc, 0
    │   │   │   │   └─ ← [Return] 340282366920938463448371605881628173655 [3.402e38], 0
    │   │   │   ├─ [6172] UniV4Inspector::sync(MockERC20: [0xF62849F9A0B5Bf2913b396098F7c7019b51A820a])
    │   │   │   │   ├─ [2527] MockERC20::balanceOf(UniV4Inspector: [0x5615dEB798BB3E4dFa0139dFa1b3D433Cc23b72f]) [staticcall]
    │   │   │   │   │   └─ ← [Return] 0
    │   │   │   │   └─ ← [Stop]
    │   │   │   ├─ [27681] MockERC20::transfer(UniV4Inspector: [0x5615dEB798BB3E4dFa0139dFa1b3D433Cc23b72f], 15003001550140037801 [1.5e19])
    │   │   │   │   ├─ emit Transfer(from: RouterActor: [0x2e234DAe75C793f67A35089C9d99245E1C58470b], to: UniV4Inspector: [0x5615dEB798BB3E4dFa0139dFa1b3D433Cc23b72f], value: 15003001550140037801 [1.5e19])
    │   │   │   │   └─ ← [Return] true
    │   │   │   ├─ [2788] UniV4Inspector::settle()
    │   │   │   │   ├─ [527] MockERC20::balanceOf(UniV4Inspector: [0x5615dEB798BB3E4dFa0139dFa1b3D433Cc23b72f]) [staticcall]
    │   │   │   │   │   └─ ← [Return] 15003001550140037801 [1.5e19]
    │   │   │   │   └─ ← [Return] 15003001550140037801 [1.5e19]
    │   │   │   └─ ← [Return] 0x00000000000000000000000000000000ffffffffffffffff2fcaa1945744a5570000000000000000000000000000000000000000000000000000000000000000
    │   │   └─ ← [Return] 0x00000000000000000000000000000000ffffffffffffffff2fcaa1945744a5570000000000000000000000000000000000000000000000000000000000000000
    │   └─ ← [Return] 340282366920938463448371605881628173655 [3.402e38], 0
    ├─ [3432] AngstromL2::getPendingPositionRewards(PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), RouterActor: [0x2e234DAe75C793f67A35089C9d99245E1C58470b], -10, 20, 0x0000000000000000000000000000000000000000000000000000000000000000) [staticcall]
    │   ├─ [393] UniV4Inspector::extsload(0xc1108968e21775cb3d744cb8fc7ecb9a74e9772a696b88ad06dad3af019a898c) [staticcall]
    │   │   └─ ← [Return] 0x00000000c3500000000000140000000000000001004190c48bf915addfe52805
    │   ├─ [393] UniV4Inspector::extsload(0x78ce598a51bb45907b8df6a62182d04f4e345acf6ced0d1caf5ce9b25e20c62f) [staticcall]
    │   │   └─ ← [Return] 0x00000000000000000000000000000000000000000000021e19e0c9bab2400000
    │   └─ ← [Return] 0
    ├─ [0] VM::roll(101)
    │   └─ ← [Return]
    ├─ [0] VM::txGasPrice(700000000 [7e8])
    │   └─ ← [Return]
    ├─ [155658] RouterActor::swap(PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), true, -1000000000000000000000 [-1e21], 79188560314459151373725315960 [7.918e28])
    │   ├─ [153556] UniV4Inspector::unlock(0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f62849f9a0b5bf2913b396098f7c7019b51a820a0000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000002f4a764787704a3f250fdc267b6d228bb1e625cb0000000000000000000000000000000000000000000000000000000000000001ffffffffffffffffffffffffffffffffffffffffffffffc9ca36523a216000000000000000000000000000000000000000000000ffdf3de87261863e03afb378)
    │   │   ├─ [152278] RouterActor::unlockCallback(0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000f62849f9a0b5bf2913b396098f7c7019b51a820a0000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000a0000000000000000000000002f4a764787704a3f250fdc267b6d228bb1e625cb0000000000000000000000000000000000000000000000000000000000000001ffffffffffffffffffffffffffffffffffffffffffffffc9ca36523a216000000000000000000000000000000000000000000000ffdf3de87261863e03afb378)
    │   │   │   ├─ [149342] UniV4Inspector::swap(PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), SwapParams({ zeroForOne: true, amountSpecified: -1000000000000000000000 [-1e21], sqrtPriceLimitX96: 79188560314459151373725315960 [7.918e28] }), 0x)
    │   │   │   │   ├─ [5689] AngstromL2::beforeSwap(RouterActor: [0x2e234DAe75C793f67A35089C9d99245E1C58470b], PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), SwapParams({ zeroForOne: true, amountSpecified: -1000000000000000000000 [-1e21], sqrtPriceLimitX96: 79188560314459151373725315960 [7.918e28] }), 0x)
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0xc1108968e21775cb3d744cb8fc7ecb9a74e9772a696b88ad06dad3af019a898c) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x00000000c3500000000000140000000000000001004190c48bf915addfe52805
    │   │   │   │   │   ├─ [2393] UniV4Inspector::extsload(0xc1108968e21775cb3d744cb8fc7ecb9a74e9772a696b88ad06dad3af019a898f) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x0000000000000000000000000000000000000000000000000000000000000000
    │   │   │   │   │   └─ ← [Return] 0x575e24b4, 1167168518538818929679374903490964965294080000000000000 [1.167e54], 0
    │   │   │   │   ├─ emit Swap(id: 0x4827e52229b38a6747ca4a003298e909eabb78a9a81df26eb989e7b9e6cf903b, sender: RouterActor: [0x2e234DAe75C793f67A35089C9d99245E1C58470b], amount0: -15784739262410737106 [-1.578e19], amount1: 15003001550140037799 [1.5e19], sqrtPriceX96: 79188560314459151373725315960 [7.918e28], liquidity: 0, tick: -11, fee: 50000 [5e4])
    │   │   │   │   ├─ [78655] AngstromL2::afterSwap(RouterActor: [0x2e234DAe75C793f67A35089C9d99245E1C58470b], PoolKey({ currency0: 0x0000000000000000000000000000000000000000, currency1: 0xF62849F9A0B5Bf2913b396098F7c7019b51A820a, fee: 8388608 [8.388e6], tickSpacing: 10, hooks: 0x2F4a764787704A3F250fdC267b6D228bB1E625CB }), SwapParams({ zeroForOne: true, amountSpecified: -1000000000000000000000 [-1e21], sqrtPriceLimitX96: 79188560314459151373725315960 [7.918e28] }), -5371268437442994008728218060229101896688448951558093448537 [-5.371e57], 0x)
    │   │   │   │   │   ├─ [5691] UniV4Inspector::mint(AngstromL2: [0x2F4a764787704A3F250fdC267b6D228bB1E625CB], 1405310203571408291950365054053061012934685786634 [1.405e48], 0)
    │   │   │   │   │   │   ├─ emit Transfer(caller: AngstromL2: [0x2F4a764787704A3F250fdC267b6D228bB1E625CB], from: 0x0000000000000000000000000000000000000000, to: AngstromL2: [0x2F4a764787704A3F250fdC267b6D228bB1E625CB], id: 1405310203571408291950365054053061012934685786634 [1.405e48], amount: 0)
    │   │   │   │   │   │   └─ ← [Stop]
    │   │   │   │   │   ├─ [26414] UniV4Inspector::mint(AngstromL2: [0x2F4a764787704A3F250fdC267b6D228bB1E625CB], 0, 3430000000000000 [3.43e15])
    │   │   │   │   │   │   ├─ emit Transfer(caller: AngstromL2: [0x2F4a764787704A3F250fdC267b6D228bB1E625CB], from: 0x0000000000000000000000000000000000000000, to: AngstromL2: [0x2F4a764787704A3F250fdC267b6D228bB1E625CB], id: 0, amount: 3430000000000000 [3.43e15])
    │   │   │   │   │   │   └─ ← [Stop]
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0xc1108968e21775cb3d744cb8fc7ecb9a74e9772a696b88ad06dad3af019a898c) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x00000000c350000000fffff50000000000000000ffdf3de87261863e03afb378
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0xb9576465fb459f3ba9568b76168f55ea6b3299fe02dc54f5dc1c06005b81e228) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x0000000000000000000000000000000000000000000000000000000000000004
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0xb9576465fb459f3ba9568b76168f55ea6b3299fe02dc54f5dc1c06005b81e228) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x0000000000000000000000000000000000000000000000000000000000000004
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0x02ae49a4fdb34522637867549dbeb7a7f900bf7de03ebe415bf120d133c635c6) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x8000000000000000000000000000000000000000000000000000000000000000
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0x02ae49a4fdb34522637867549dbeb7a7f900bf7de03ebe415bf120d133c635c6) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x8000000000000000000000000000000000000000000000000000000000000000
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0xb9576465fb459f3ba9568b76168f55ea6b3299fe02dc54f5dc1c06005b81e228) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x0000000000000000000000000000000000000000000000000000000000000004
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0x02ae49a4fdb34522637867549dbeb7a7f900bf7de03ebe415bf120d133c635c6) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x8000000000000000000000000000000000000000000000000000000000000000
    │   │   │   │   │   ├─ [393] UniV4Inspector::extsload(0x11def4ed8378c0767861466fbe7371f0afa3205126a6cf60edee623ea08c5fc6) [staticcall]
    │   │   │   │   │   │   └─ ← [Return] 0x000000000000021e19e0c9bab2400000000000000000021e19e0c9bab2400000
    │   │   │   │   │   └─ ← [Revert] ArithmeticOverflowUnderflow()
    │   │   │   │   └─ ← [Revert] WrappedError(0x2F4a764787704A3F250fdC267b6D228bB1E625CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)
    │   │   │   └─ ← [Revert] WrappedError(0x2F4a764787704A3F250fdC267b6D228bB1E625CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)
    │   │   └─ ← [Revert] WrappedError(0x2F4a764787704A3F250fdC267b6D228bB1E625CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)
    │   └─ ← [Revert] WrappedError(0x2F4a764787704A3F250fdC267b6D228bB1E625CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)
    └─ ← [Revert] WrappedError(0x2F4a764787704A3F250fdC267b6D228bB1E625CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)

Backtrace:
  at AngstromL2.afterSwap
  at UniV4Inspector.swap
  at RouterActor.unlockCallback
  at UniV4Inspector.unlock
  at RouterActor.swap
  at SwapFromTickBoundaryTest.test_swapDownFromTickBoundary

Suite result: FAILED. 0 passed; 1 failed; 0 skipped; finished in 192.34ms (9.08ms CPU time)

Ran 1 test suite in 217.77ms (192.34ms CPU time): 0 tests passed, 1 failed, 0 skipped (1 total tests)

Failing tests:
Encountered 1 failing test in test/SwapFromTickBoundary.t.sol:SwapFromTickBoundaryTest
[FAIL: WrappedError(0x2F4a764787704A3F250fdC267b6D228bB1E625CB, 0xb47b2fb1, 0xc9654ed4, 0xa9e35b2f)] test_swapDownFromTickBoundary() (gas: 433875)

Encountered a total of 1 failing tests, 0 tests succeeded

Tip: Run `forge test --rerun` to retry only the 1 failed test
```

## Task

Fix the vulnerability in the source code. You are done when both of these hold:

1. The test above passes.
2. The code still meets the requirement.

## Rules

- You MUST NOT edit, add or delete any file under `test/`.
- You may edit any file under `src/`.
- Do not change any function signature.
- Do not add dependencies.
- When you are done, stop. Give a short summary of what you changed and why.