# [M-01] Vault owner is incetivized to not switch invalid collateral token, during liquidation

## Summary

*No summary available*

## GitHub Source Code

- **Link**: https://code4rena.com/audits/2025-08-flare-fasset/submissions/F-88
- **Valid**: ✓ Yes

## Content

https://github.com/code-423n4/2025-08-flare/blob/main/contracts/assetManager/library/LiquidationPaymentStrategy.sol#L37-L39

### Finding Description and Impact

A collateral token may become invalid following a governance decision. In such a case, the agent is expected to switch it to another valid collateral token. However, there is a scenario where the vault owner has no incentive to perform this switch at least temporarily.

During liquidation, if the vault collateral token is invalid, then [the collateral pool covers the entire payment](https://github.com/code-423n4/2025-08-flare/blob/main/contracts/assetManager/library/LiquidationPaymentStrategy.sol#L37-L39). If both the pool and the vault are undercollateralized, the vault’s liability is capped at [**half of the pool’s responsibility**](https://github.com/code-423n4/2025-08-flare/blob/main/contracts/assetManager/facets/LiquidationFacet.sol#L217).

This creates an incentive for the agent:

- With a valid collateral token, the vault typically pays **100%** (`vaultFactor`) while the pool pays **30%** (`poolFactor`), totaling ~115% for the agent (as vault covers half of `poolFactor`).
- With an invalid collateral token, the vault’s effective share may drop to only ~65% of responsibility, which is significantly more favorable for the agent.

As a result, agents may strategically avoid switching to a valid collateral token during liquidation, undermining the system’s design.

### Recommended Mitigation Steps

In case the collateral token becomes invalid, liquidation should still require payments from the vault based on the same `vaultFactor` logic, rather than shifting the entire burden to the pool. This ensures agents remain properly incentivized to update their collateral token when governance decisions invalidate one.

**[Flare mitigated](https://github.com/code-423n4/2025-10-flare-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**

> Token deprecation and agent vault token switching have been removed.

**Status:** Mitigation confirmed. Full details in reports from [givn](https://code4rena.com/audits/2025-10-flare-fasset-mitigation-review/submissions/S-3), [rvierdiiev](https://code4rena.com/audits/2025-10-flare-fasset-mitigation-review/submissions/S-1), and [farman1094](https://code4rena.com/audits/2025-10-flare-fasset-mitigation-review/submissions/S-7).