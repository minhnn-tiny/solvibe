# Prompts for the repair input study

These prompts start a repair run in the repair input study (`IDEA.md`, section "Extension: how the input given to a repair agent changes the repair"). The agent starts from the human's vulnerable code at the audited commit. There is one prompt for each information arm:

| Arm | Written report | Shown PoV |
|---|---|---|
| L, location only | no | no |
| R, report | yes | no |
| P, PoV | no | yes |
| RP, report and PoV | yes | yes |

They were drafted with `/prompt-master`, for Aider 0.86.2, the OpenHands SDK 1.53.0 and Codex CLI 0.160.1, all with GPT-5.4-mini. They follow the repair prompt of the first repair round (`pilot/prompts/repair_with_failing_test.md`), so arm P keeps that prompt's wording. `pilot/scripts/run_task.py --arm` fills in the prompt for the arm and sends it as the whole first message. For Codex, the offline note (`CODEX_OFFLINE_NOTE` in `run_task.py`) follows it.

## What is the same in every arm

- Every prompt names the function and its file, and gives the requirement.
- The four prompts use the same words, apart from three parts: the report, the test, and the first condition for being done.
- No prompt says where in the function the bug is, explains it, or asks for the root cause.
- No prompt says that other tests will check the repair.
- No prompt names a tool. What the agent can run changes between arms (nothing, only the shown test, or a terminal), and each tool describes itself. So the same prompt is used at every execution level.

## Placeholders

Text in `$name` form is filled in by the pipeline with Python's `string.Template`:

- `$requirement`: the V1 requirement (`pilot/tasks/63008/feature_tasks/V1/feature_request.md`).
- `$report`: the finding's title, description and impact, without its proof of concept, its recommended fix or the summary that repeats the fix (`pilot/tasks/63008/extension/report.md`).
- `$test_path`: where the shown test sits in the workspace.
- `$test_code`: the shown test (`pilot/tasks/63008/pov/P2_feedback_test.t.sol`).
- `$test_cmd`: the command that runs it.
- `$test_output`: its output on the audited code, captured offline before the agent starts.

## Prompt for arm L

````text
# Fix a reported vulnerability

## Context

You are working in a Foundry project for a Uniswap V4 hook. The function `reset(TickIteratorDown memory self, int24 startTick)` in `src/libraries/TickIterator.sol` was written from the requirement below. The requirement is also in `FEATURE_REQUEST.md`.

<requirement>
$requirement
</requirement>

## Report

A security reviewer found a vulnerability in this function.

## Task

Fix the vulnerability in the source code. You are done when both of these hold:

1. The vulnerability is fixed.
2. The code still meets the requirement.

## Rules

- You MUST NOT edit, add or delete any file under `test/`.
- You may edit any file under `src/`.
- Do not change any function signature.
- Do not add dependencies.
- When you are done, stop. Give a short summary of what you changed and why.
````

## Prompt for arm R

````text
# Fix a reported vulnerability

## Context

You are working in a Foundry project for a Uniswap V4 hook. The function `reset(TickIteratorDown memory self, int24 startTick)` in `src/libraries/TickIterator.sol` was written from the requirement below. The requirement is also in `FEATURE_REQUEST.md`.

<requirement>
$requirement
</requirement>

## Report

A security reviewer found a vulnerability in this function. This is their report.

<report>
$report
</report>

## Task

Fix the vulnerability in the source code. You are done when both of these hold:

1. The vulnerability is fixed.
2. The code still meets the requirement.

## Rules

- You MUST NOT edit, add or delete any file under `test/`.
- You may edit any file under `src/`.
- Do not change any function signature.
- Do not add dependencies.
- When you are done, stop. Give a short summary of what you changed and why.
````

## Prompt for arm P

````text
# Fix a reported vulnerability

## Context

You are working in a Foundry project for a Uniswap V4 hook. The function `reset(TickIteratorDown memory self, int24 startTick)` in `src/libraries/TickIterator.sol` was written from the requirement below. The requirement is also in `FEATURE_REQUEST.md`.

<requirement>
$requirement
</requirement>

## Report

A security reviewer found a vulnerability in this function. They sent this test as proof. The test fails on the current code.

Test file: `$test_path`

```solidity
$test_code
```

Command:

```sh
$test_cmd
```

Output on the current code:

```text
$test_output
```

## Task

Fix the vulnerability in the source code. You are done when both of these hold:

1. The test above passes.
2. The code still meets the requirement.

## Rules

- You MUST NOT edit, add or delete any file under `test/`.
- You may edit any file under `src/`.
- Do not change any function signature.
- Do not add dependencies.
- When you are done, stop. Give a short summary of what you changed and why.
````

## Prompt for arm RP

````text
# Fix a reported vulnerability

## Context

You are working in a Foundry project for a Uniswap V4 hook. The function `reset(TickIteratorDown memory self, int24 startTick)` in `src/libraries/TickIterator.sol` was written from the requirement below. The requirement is also in `FEATURE_REQUEST.md`.

<requirement>
$requirement
</requirement>

## Report

A security reviewer found a vulnerability in this function. This is their report.

<report>
$report
</report>

They sent this test as proof. The test fails on the current code.

Test file: `$test_path`

```solidity
$test_code
```

Command:

```sh
$test_cmd
```

Output on the current code:

```text
$test_output
```

## Task

Fix the vulnerability in the source code. You are done when both of these hold:

1. The test above passes.
2. The code still meets the requirement.

## Rules

- You MUST NOT edit, add or delete any file under `test/`.
- You may edit any file under `src/`.
- Do not change any function signature.
- Do not add dependencies.
- When you are done, stop. Give a short summary of what you changed and why.
````
