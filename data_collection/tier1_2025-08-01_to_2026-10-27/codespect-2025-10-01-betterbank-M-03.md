# Pausing of FavorTreasury queues outstanding epochs to be executed

## Summary

*No summary available*

## GitHub Source Code

- **Link**: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-10-01-BetterBank.md
- **Valid**: ✓ Yes

## Content

**Files:** [`FavorTreasury.sol`](https://github.com/grape-finance/BB-Custom-contracts/blob/43fba5ed6a5f47d6ae997660a7fe656c57f44b30/contracts/FavorTreasury.sol#L312)

**Description:**

The `FavorTreasury` contract implements a custom epoch checkpoint mechanism instead of using the standard `Epoch.sol`. In this mechanism, functions with the `checkEpoch` modifier increment the epoch by **one** per call, rather than calculating the current epoch based on the elapsed time.

This design introduces unpredictable behaviour if the protocol is paused for an extended period. For example, if the protocol is paused for a week, calling `allocateSeigniorage(...)` after unpausing could process all outstanding epochs (e.g., 7 days × 24 = 168 epochs). This would mint `Favor` tokens for the entire paused duration. Additionally, an attacker could exploit this by taking a flash loan, staking via `Staking.sol`, and claiming rewards for all 168 epochs, potentially draining rewards intended for long-term stakers.

**Impact:**

- Unexpected minting of `Favor` tokens for paused periods;
- Potential manipulation of staking rewards;
- Risk of reward theft from long-term stakers;

**Recommendation:** Update the epoch logic to compute the current epoch based on the elapsed time rather than incrementing by one, similar to the approach in `Epoch.sol`.

**Status:** Fixed

**Client response:** Was fixed, epoch system was reworked ([1e7747aa89f79ff8ad55e8facc0a0e3a5cc3a699](https://github.com/grape-finance/BB-Custom-contracts/commit/1e7747aa89f79ff8ad55e8facc0a0e3a5cc3a699))