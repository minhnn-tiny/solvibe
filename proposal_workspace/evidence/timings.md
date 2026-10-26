# Measured times for the automated evidence work (21 to 22 October 2026)

These are wall-clock times of LLM subagents (Claude) that did the work end to end. The source is the task-completion
record that the Claude Code session reported for each subagent. They measure automated, LLM-assisted work only.
No person did any of the work, so they are not measurements of human time.

| Work | Output | Wall-clock time | Tokens | Tool calls |
|---|---|---|---|---|
| Executable evidence package for finding 63008 (entitlement PoV and variant, function-body correction, H-02 fixed independently, capital and ordering record, 10 logged runs in Docker without network) | `evidence/63008/` | 1,373 s (about 23 minutes) | 223,189 | 76 |
| Version 2 of the 63008 package (function-body correction that keeps empty-range behaviour, fixed-state assertions, runner that checks 12 expected outcomes; ran end to end and matched all 12) | `evidence/63008/` (Version 2 section) | 598 s (about 10 minutes) | 132,195 | 34 |
| Fix-scope classification of the 43 pilot findings with public history, from local clones only | `evidence/frame_count/` | 864 s (about 14 minutes) | 262,733 | 79 |

Both started from material the pilot had already prepared (local clones, the pilot's 63008 tests and notes).
