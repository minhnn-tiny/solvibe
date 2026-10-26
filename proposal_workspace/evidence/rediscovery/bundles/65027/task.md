# Review task

- Protocol: Panoptic
- File in the repository: `contracts/CollateralTracker.sol`
- Function: `CollateralTracker.settleBurn`
- Signature: `function settleBurn(address optionOwner, int128 longAmount, int128 shortAmount, int128 ammDeltaAmount, int128 realizedPremium, RiskParameters riskParameters) external onlyPanopticPool nonReentrant returns (int128)`
- Lines in `target.sol`: 1614 to 1683

Review the function settleBurn in target.sol for High or Medium severity vulnerabilities that an unprivileged attacker could exploit.
