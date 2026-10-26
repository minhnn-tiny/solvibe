# Review task

- Protocol: Merkl
- File in the repository: `contracts/Distributor.sol`
- Function: `Distributor._claim`
- Signature: `function _claim(address[] calldata users, address[] calldata tokens, uint256[] calldata amounts, bytes32[][] calldata proofs, address[] memory recipients, bytes[] memory datas) internal nonReentrant`
- Lines in `target.sol`: 425 to 491

Review the function _claim in target.sol for High or Medium severity vulnerabilities that an unprivileged attacker could exploit.
