# Audit-blind rediscovery check (iteration-3 meta-review, item 9)

Seventeen pilot findings with a single-function fix. For each, a fresh Claude reviewer and a fresh Codex reviewer (gpt-6-astra, medium effort, no web search recorded) reviewed only the bundle in `bundles/<id>/` (the target file at the pre-fix snapshot, up to six imported files, and a one-sentence task), copied to a folder outside the repository. A Claude judge compared each candidate list with the sealed answer key (`sealed_key/<id>.md`), blind to which list came from which family (`judge_mapping.json`). Verdicts are in `judge/batch1.md` and `judge/batch2.md`.

| Reviewer family | Candidate-level match, all 17 (95% Wilson interval) | Excluding 64083, 64693, 65044 | Matched at rank 1 | Misses |
|---|---|---|---|---|
| claude | 17 of 17 (0.82 to 1.00) | 14 of 14 (0.78 to 1.00) | 12 | none |
| codex | 13 of 17 (0.53 to 0.90) | 13 of 14 (0.69 to 0.99) | 12 | 63008, 64083, 64693, 65044 |

Both reviewers matched 13 of 17 findings; at least one matched 17 of 17.

**What this does and does not show.** A match means a candidate names the same root cause in the target function. It is not a confirmed exploit: no PoV, correction or adjudication was done, so these rates are upper bounds on confirmed rediscovery by the planned campaign. The bundles name the target function, which the real campaign also does. The audits date from late 2025, so the reviewing models may have seen the reports or fixes in training; the rates may include recall. Three keys are weak cases: 64083 needs the owner as attacker, 64693 has no outside attacker by the judge's reading, and 65044 was marked informative by the project.
