# Missing slippage protection when interacting with UniswapV2 Pair

## Summary

*No summary available*

## GitHub Source Code

- **Link**: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-10-01-BetterBank.md
- **Valid**: ✓ Yes

## Content

**Files:** [`Zapper.sol/L150`](https://github.com/grape-finance/BB-Custom-contracts/blob/43fba5ed6a5f47d6ae997660a7fe656c57f44b30/contracts/Zapper.sol#L150), [`Zapper.sol/L183`](https://github.com/grape-finance/BB-Custom-contracts/blob/43fba5ed6a5f47d6ae997660a7fe656c57f44b30/contracts/Zapper.sol#L183)

**Description:**

The `Zapper` contract allows handling of both base and Favor tokens - it manages adding liquidity on behalf of the user and can swap token to favor when needed. Both `_swap(...)` and `_addLiquidity(...)` rely on router functions but have hard-coded the minimum output parameters to `0`. In `_swap(...)`, the contract uses `router.swapExactTokensForTokensSupportingFeeOnTransferTokens(...)` with no slippage threshold, allowing execution at unfavorable exchange rates.

**Impact:** An attacker can front-run the swap with a sandwich attack. These omissions generally expose users to front-running and sandwich attacks, yet the presence of a transfer tax on Favor token reduces exploitability. Any attacker attempting to manipulate the reserves to force poor execution must pay the tax when moving Favor, which erodes profit margins and can make such attacks economically infeasible. Still, the lack of slippage protection means the system does not revert in adverse conditions, and users can unintentionally add liquidity or swap at unfavorable terms. The price could still be altered through adding liquidity which swaps half of the added tokens.

**Recommendation:** Enforce a configurable minimum token output when calling the router to ensure trades or liquidity adding reverts, if the expected rates cannot be met.

**Status:** Fixed

**Client response:** Fixed in [b9413cc025d7f7cc76daf28224b917923daf732f](https://github.com/grape-finance/BB-Custom-contracts/commit/b9413cc025d7f7cc76daf28224b917923daf732f)

**CODESPECT fix review:** Lack of slippage protection in `_zapToken(...)` acknowledged.