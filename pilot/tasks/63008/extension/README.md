# Repair input study: task files for finding 63008

This folder holds what the repair input study (`IDEA.md`, section "Extension: how the input given to a repair agent changes the repair") needs for finding 63008, and the checks made before any data was collected. Everything here was built and checked on 2026-10-20, in Docker with the network off.

## What is in this folder

- **The study manifest (`manifest.json`).** It lists the report shown in arms R and RP, the shown test, the functional suite, and the five frozen attacks. For each attack it records the failure that attack shows on the human fix. The run script (`pilot/scripts/run_task.py --arm`) reads it.
- **The report shown in arms R and RP (`report.md`).** The finding's title, description and impact, copied from `data_collection/tier1_after_2025-08-31/63008.md`. The Solodit summary, the proof of concept, the recommended fix and the replies are left out. The summary is left out because it repeats the fix.
- **The functional suite (`functional/`).**
  - `TickIteratorDown.t.sol` is the fix commit's iterator test file (`c01b6c7`), cut to its 14 downward tests and its downward fuzz test. Four changes were needed:
    - the contract is renamed;
    - the `Random` struct, which `BaseTest.sol` gained only in `0d6d39e`, is declared in the file;
    - one log line is dropped, because the audited `FormatLib` cannot print an `int256[]`;
    - `test_iterateDown_emptyRange` follows V1 requirement 6. The fix commit expects tick 101 there. The requirement says `hasNext` must return false at once. A second case at an initialized tick was added.
  - `TickIterator.t.sol` is the audited test file without its 14 downward tests. Those expect the start tick to be skipped, which is the bug. Its 14 upward tests stay as regression tests.
  - The judge runs every test of the repository with these two files in place: 61 tests, with the fuzz seed fixed at 1.
- **Two new held-out attacks (`pov/`).** They were written from the security rule before any study repair was seen.
  - P4 (`PoV63008_SameWordAlignedEnd.t.sol`): the same attack as P2, at tick spacing 60. The swap starts on the upper tick of a position and ends at a tick in the same bitmap word, which is a multiple of the spacing.
  - P5 (`PoV63008_WordBoundaryStart.t.sol`): the same attack at a bitmap word boundary. The swap starts at tick 2560, which is bit 0 of word 1.
  - On the audited code both swaps revert with `ArithmeticOverflowUnderflow()` inside the hook's `afterSwap`. That is the same path as P2.
- **The reference repair (`reference_repair.patch`).** It is the human fix (`c01b6c7`'s `TickIterator.sol`), plus one change: when the start tick equals the end tick, the iterator yields no ticks. It shows that a repair can pass every check.
- **The patches used to check the judge (`patches/`).**
  - the human fix;
  - the hand-written shallow repair from the control group design, which clamps the liquidity at zero instead of fixing the walk;
  - the shallow repair that OpenHands + GPT-5.4-mini wrote in Step 20;
  - two versions that turn the feature off: `reset` always reverts, or the walk yields nothing;
  - a version that does not compile.
- **The checks (`checks/`).** They are described in the next section.

## Checks made before any data was collected

**The judge, on known versions (`checks/judge_validation/summary.md`).** Each version was judged with `run_task.py --arm P-E2 --from-patch`.

| Version | Compiles | Functional (pass / fail) | P1 | P2 | P3 | P4 | P5 | All checks pass |
|---|---|---|---|---|---|---|---|---|
| audited code | yes | 56 / 5 | works | works | works | works | works | no |
| human fix | yes | 60 / 1 | blocked | blocked | blocked | blocked | blocked | no (empty range) |
| reference repair | yes | 61 / 0 | blocked | blocked | blocked | blocked | blocked | **yes** |
| hand-written shallow repair | yes | 56 / 5 | blocked | blocked | works | blocked | blocked | no |
| OpenHands shallow repair (Step 20) | yes | 56 / 5 | blocked | blocked | works | blocked | works | no |
| `reset` always reverts | yes | 35 / 26 | works | works | invalid | works | works | no |
| does not compile | no | 0 / 0 | invalid | invalid | invalid | invalid | invalid | no |

This shows the following:
- Every attack passes on the audited code.
- On the human fix, every attack fails at the place recorded in the manifest. P1, P2, P4 and P5 fail at "next call did not revert as expected". P3 fails at "attack is not profitable", with a loss of 0.098 ETH.
- The attacks together catch both known shallow repairs. P3 catches both, and P5 also catches the OpenHands one.
- The functional suite rejects both versions that turn the feature off: 26 and 18 failures.
- A failure at another place is marked invalid, not blocked. When `reset` always reverts, P3 fails with the hook's `WrappedError`, and the judge marks it invalid.

**Forge drops test results when its progress display is on.** With `show_progress = true`, which this repository's `foundry.toml` sets, forge 1.5.1 left whole suites out of its JSON output and its summary, at random. In one run, the 18 hook tests were missing. With `FOUNDRY_SHOW_PROGRESS=false`, all 61 tests were reported in three runs out of three. The run script now sets it in every container. The control group notes saw the same thing earlier: "the full run reported only 10 of the 18 tests".

**The tools each level offers.** Each tool list was recorded from the agent's first request to a stand-in API server, so no model was called:
- `checks/codex_tools_E0.json`, `checks/codex_tools_E1.json` and `checks/codex_tools_E2.json` for Codex;
- `checks/openhands_tools_E0.json`, `checks/openhands_tools_E1.json` and `checks/openhands_tools_E2.json` for OpenHands.

The lists are these:
- **OpenHands:**
  - E0: the file editor, task tracker, finish and think tools.
  - E1: the same, plus `run_shown_test`.
  - E2: the same as E0, plus the terminal.
- **Codex:**
  - E0: the study file tools, plus Codex's tools that cannot run commands: resource listing, user input, image viewing, sub-agents and goals.
  - E1: the same, plus `run_shown_test`.
  - E2: the same as E0, plus `exec_command` and `write_stdin`.
- **Codex at first started its first turn without the MCP server.** The server was still starting, and Codex left out its tools ("omitting pending optional MCP server"). `required = true` in the server's settings makes Codex wait for it.

**The file tools refuse paths outside the workspace (`checks/mcp_file_tools_check.txt`).** These were checked through a real MCP client: `..` paths, absolute paths, a symlink to a file outside, a symlink to `/etc`, and a write through a symlink. Each one was refused, and the file outside was not changed.

**Short runs with each agent at each level.** These used GPT-5.4-mini, cost about $0.40 in all, and are in `pilot/runs/repair_input_study_checks/`. All 11 passed.
- **Basic check, every agent and level:**
  - The agent read a file, searched the code, added a comment to `src/`, and tried one shell command.
  - At E0 and E1 the command did not run. This held for OpenHands, Codex and Aider.
  - At E2 it ran, for OpenHands and Codex.
  - The comment reached `agent.patch` at every level.
  - Codex at E0 and E1 read, searched and edited only through the study file tools.
- **Tamper check, every agent at E1:**
  - The agent emptied the shown test, turned `ffi` on in `foundry.toml`, added a `vm.ffi` call, and reran the test.
  - The shared test script still ran the original test, which failed with the swap's revert.
  - The `ffi` command did not run.
  - The same tampering, done by hand afterwards, gave the same result.

## Checks written after the runs started (`repair_checks/`)

These were written on 2026-10-20 to confirm or reject reports from the LLM judge. They are not part of the frozen attack set, and they are reported on their own. Each one passes on the flawed repair it was written for, and fails on the audited code and on the reference repair.

| Check | File | What it shows when it passes |
|---|---|---|
| P6 | `PoV63008_Bit255Start.t.sol` | P2's attack starting at tick 2550, bit 255 of word 0: the start tick is still skipped there |
| P7 | `SwapDownNoTickBelow.t.sol` | with all liquidity above the price, a taxed zero-for-one swap needs more than a 30,000,000-gas block |
| P8 | `EmptyRangeAtNegativeTick.t.sol` | a taxed zero-for-one swap that keeps the pool at a negative tick reverts, because the empty range returns ticks |

- **P8 also passes on the human fix's `TickIterator.sol` placed on the audited code.** It does so by another path: the fix returns the tick above the start for an empty range. The full fix commit was not tested.
- **Two more files tested reports that were then rejected.** Each scenario failed, so no flaw was shown:
  - `UninitializedBit255Tick.t.sol`: the claimed revert does not happen;
  - `NewPositionAtBit255Tick_probe.t.sol`: it logs pending rewards and has no assertion.
- **All three checks were run on the 64 repairs the judge reviewed** (`pilot/scripts/study_posthoc_check.py`, results in `pilot/runs/repair_input_study/posthoc.json`).
