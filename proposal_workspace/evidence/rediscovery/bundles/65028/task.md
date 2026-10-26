# Review task

- Protocol: Panoptic
- File in the repository: `contracts/RiskEngine.sol`
- Function: `RiskEngine.getLiquidationBonus`
- Signature: `function getLiquidationBonus(LeftRightUnsigned tokenData0, LeftRightUnsigned tokenData1, uint160 atSqrtPriceX96, LeftRightSigned netPaid, LeftRightUnsigned shortPremium) external pure returns (LeftRightSigned, LeftRightSigned)`
- Lines in `target.sol`: 500 to 614

Review the function getLiquidationBonus in target.sol for High or Medium severity vulnerabilities that an unprivileged attacker could exploit.
