# Judge of the repair input study on known versions (2026-10-20)

Run with `run_task.py --arm P-E2 --from-patch` on each patch in `../../patches/` (the reference repair is `../../reference_repair.patch`), in Docker with the network off. Functional = tests passed / failed of the 61.

| Version | Compiles | Functional | P1 | P2 | P3 | P4 | P5 | Shown test passes | All checks pass |
|---|---|---|---|---|---|---|---|---|---|
| audited code 386baff (no change) | True | 56 / 5 | works | works | works | works | works | False | False |
| human fix (c01b6c7 TickIterator.sol) | True | 60 / 1 | blocked | blocked | blocked | blocked | blocked | True | False |
| reference repair | True | 61 / 0 | blocked | blocked | blocked | blocked | blocked | True | True |
| hand-written shallow repair | True | 56 / 5 | blocked | blocked | works | blocked | blocked | True | False |
| OpenHands + GPT-5.4-mini repair (Step 20) | True | 56 / 5 | blocked | blocked | works | blocked | works | True | False |
| reset always reverts | True | 35 / 26 | works | works | invalid | works | works | False | False |
| does not compile | False | 0 / 0 | invalid | invalid | invalid | invalid | invalid | False | False |
