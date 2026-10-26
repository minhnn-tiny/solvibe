# Implement `calldataToId` in `src/libraries/PoolKeyHelperLib.sol`

The hook receives pool keys as calldata in its entry points, such as `setPoolLPFee`, `getPendingPositionRewards` and the Uniswap hook callbacks. It needs each pool's ID to find the pool's stored state. This helper computes the ID directly from a key held in calldata.

Do not change the signature:

```solidity
function calldataToId(PoolKey calldata poolKey) internal pure returns (PoolId id)
```

Required behaviour:

1. For every pool key, the result must equal the ID that Uniswap V4 core gives the same key, `PoolIdLibrary.toId`. Every lookup in `AngstromL2` depends on the two IDs matching.
2. Every field of the key counts. Two keys that differ in any field must give different IDs.
3. Read the key from calldata. Do not write storage and do not call other contracts.
4. Memory may be used as scratch space. Memory the calling function already holds must be left unchanged.
5. The function stays `internal pure`.

Change only the body of this function. Leave the rest of the library and every caller as they are.
