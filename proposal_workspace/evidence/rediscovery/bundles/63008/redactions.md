# Redactions

Files checked: `target.sol`, `context/src/libraries/TickLib.sol`, `context/src/interfaces/IUniV4.sol`.

Every comment was checked for text that reveals the audit (audit firm names, contest names, finding or issue numbers, the words audit, finding and fix, and the finding title). None was found.

Comment lines whose text was replaced with `// [comment removed for blind review]`. Code lines were not changed. Line numbers did not change.

| File | Line | Reason |
|---|---|---|
| `target.sol` | 30 | names an individual developer (personal name, handle or email address); not audit text |
| `context/src/libraries/TickLib.sol` | 6 | names an individual developer (personal name, handle or email address); not audit text |
