# Redactions

Files checked: `target.sol`, `context/src/types/Fungible.sol`, `context/src/types/Position.sol`, `context/src/interfaces/ILicredity.sol`, `context/src/interfaces/IUnlockCallback.sol`, `context/src/libraries/FullMath.sol`, `context/src/libraries/Locker.sol`.

Every comment was checked for text that reveals the audit (audit firm names, contest names, finding or issue numbers, the words audit, finding and fix, and the finding title). None was found.

Comment lines whose text was replaced with `// [comment removed for blind review]`. Code lines were not changed. Line numbers did not change.

| File | Line | Reason |
|---|---|---|
| `context/src/libraries/FullMath.sol` | 12 | names an individual developer (personal name, handle or email address); not audit text |
| `context/src/libraries/FullMath.sol` | 76 | names an individual developer (personal name, handle or email address); not audit text |
