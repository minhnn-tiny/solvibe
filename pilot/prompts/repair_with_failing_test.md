# Prompt for the repair round

This prompt starts the repair round of the vulnerable group. The agent's own first-round code is in the workspace. The agent gets one PoV as feedback and must fix the code. The other PoVs stay held back and judge the repair afterwards. For finding 63008 the agent sees P2, and P1 and P3 are held back (control group design, `pilot/tasks/63008/control_group.md`, section 5).

It was drafted with `/prompt-master`. It is written for the coding agents Aider and OpenHands, with GPT-5.4-mini and Sonnet 4.5, and later also used for Codex. All six setups get the same text. `pilot/scripts/run_task.py --repair` fills it in and sends it as the whole first message. OpenHands and Codex get no extra text around it. Aider also gets the test command through `--test-cmd` and `--auto-test`, so it can run the test after each edit, as OpenHands and Codex can from their terminals.

## How the PoV is shown

- **As a failing test.** The published P2 passes when the attack works, because it wraps the swap in `vm.expectRevert()`. The shown copy drops that line, so it fails on vulnerable code and passes on fixed code. A failing test is the usual form of feedback for a coding agent. The attack is the same.
- **Without comments.** The PoV's own comments explain the bug and name the line to fix. The shown copy has none. It only shows that a swap reverts.
- **With its output.** The pipeline runs the test on the agent's code before the agent starts, and puts the output in the prompt.

## What the prompt does not say

- It does not say where the bug is or explain it.
- It does not ask for the root cause. That would tell the agent that a shallow fix is not enough.
- It does not say that other tests are held back.

The prompt names the function the agent wrote and gives its requirement. The agent wrote that code in the first round, so it would know this in a real session.

## Placeholders

Text in `$name` form is filled in by the pipeline with Python's `string.Template`:

- `$requirement`: the requirement from the first round.
- `$test_path`: where the shown test sits in the workspace.
- `$test_code`: the shown test.
- `$test_cmd`: the command that runs it.
- `$test_output`: its output on the agent's first-round code.

## Prompt

````text
# Fix a reported vulnerability

## Context

You are working in a Foundry project for a Uniswap V4 hook. The function `reset(TickIteratorDown memory self, int24 startTick)` in `src/libraries/TickIterator.sol` was written from the requirement below. The requirement is also in `FEATURE_REQUEST.md`.

<requirement>
$requirement
</requirement>

## Report

A security reviewer found a vulnerability in the current code. They sent this test as proof. The test fails on the current code.

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
