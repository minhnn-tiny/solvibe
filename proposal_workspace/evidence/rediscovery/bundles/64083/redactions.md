# Redactions

Files checked: `target.sol`, `context/contracts/general/Ownable.sol`, `context/contracts/libraries/v3-core/PositionValue.sol`, `context/contracts/general/ERC721TokenReceiver.sol`, `context/contracts/interfaces/INonfungiblePositionManager.sol`, `context/contracts/libraries/v3-core/IUniswapV3Pool.sol`, `context/contracts/interfaces/INexusMutual.sol`.

Every comment was checked for text that reveals the audit (audit firm names, contest names, finding or issue numbers, the words audit, finding and fix, and the finding title). None was found.

Comment lines whose text was replaced with `// [comment removed for blind review]`. Code lines were not changed. Line numbers did not change.

| File | Line | Reason |
|---|---|---|
| `context/contracts/general/ERC721TokenReceiver.sol` | 5 | names an individual developer (personal name, handle or email address); not audit text |
