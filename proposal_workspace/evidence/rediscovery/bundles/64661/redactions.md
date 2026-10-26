# Redactions

Files checked: `target.sol`, `context/src/libraries/TWAMMStorageLayout.sol`, `context/src/types/orderConfig.sol`, `context/src/types/poolId.sol`, `context/src/types/callPoints.sol`, `context/src/types/poolKey.sol`, `context/src/types/positionId.sol`.

Every comment was checked for text that reveals the audit (audit firm names, contest names, finding or issue numbers, the words audit, finding and fix, and the finding title). None was found.

Comment lines whose text was replaced with `// [comment removed for blind review]`. Code lines were not changed. Line numbers did not change.

| File | Line | Reason |
|---|---|---|
| `target.sol` | 57 | names an individual developer (personal name, handle or email address); not audit text |
