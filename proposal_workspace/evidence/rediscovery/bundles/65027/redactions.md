# Redactions

Files checked: `target.sol`, `context/contracts/libraries/Math.sol`, `context/contracts/types/RiskParameters.sol`, `context/contracts/PanopticPool.sol`, `context/contracts/interfaces/IRiskEngine.sol`, `context/contracts/tokens/ERC20Minimal.sol`, `context/contracts/base/Multicall.sol`.

Every comment was checked for text that reveals the audit (audit firm names, contest names, finding or issue numbers, the words audit, finding and fix, and the finding title). None was found.

Comment lines whose text was replaced with `// [comment removed for blind review]`. Code lines were not changed. Line numbers did not change.

| File | Line | Reason |
|---|---|---|
| `context/contracts/tokens/ERC20Minimal.sol` | 6 | names an individual developer (personal name, handle or email address); not audit text |
