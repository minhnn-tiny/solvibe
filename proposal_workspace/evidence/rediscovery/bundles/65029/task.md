# Review task

- Protocol: Panoptic
- File in the repository: `contracts/RiskEngine.sol`
- Function: `RiskEngine._getRequiredCollateralAtTickSinglePosition`
- Signature: `function _getRequiredCollateralAtTickSinglePosition(TokenId tokenId, uint128 positionSize, int24 atTick, int16 poolUtilization, bool underlyingIsToken0) internal view returns (uint256 tokenRequired, uint256 credits)`
- Lines in `target.sol`: 1315 to 1350

Review the function _getRequiredCollateralAtTickSinglePosition in target.sol for High or Medium severity vulnerabilities that an unprivileged attacker could exploit.
