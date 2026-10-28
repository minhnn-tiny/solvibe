# Review of batch 5 tier 1 findings

The old tier 1 findings (batches 1-4) were checked by `validate_with_openai.py`, which sent each finding and its
code to an OpenAI model. For batch 5 the same check is done by Claude reviewers instead, with no LLM API calls.
This file is the instruction every reviewer follows, so the check can be repeated.

## Input

`packets_<n>.jsonl` has one JSON object per line, one line per tier 1 finding:

- `title`, `finding_text`: the finding as the audit firm wrote it. The Recommendation and Proof of Concept parts
  are cut off, as `extract_contracts.py` does before it looks for vulnerable code.
- `problem_code`: the functions around the lines the finding links to on GitHub. This is the code
  `validate_with_openai.py` would have sent.
- `sol_file`: the whole Solidity file that was downloaded from the finding's GitHub link.
- `identifiers_found_in_file`, `identifiers_missing_from_file`: names written in backticks in the finding, and
  whether a word with that name occurs in `sol_file`. This is only a hint. A missing name often lives in another
  file of the same project.

## Questions for each finding

These are the questions `validate_with_openai.py` asks in its Task 1 and Task 3.

1. Does the title describe a problem in this code? (`summary_matches`)
2. Do the functions and variables the finding names exist in this code? (`content_matches`)
3. Is the vulnerable pattern the finding describes present in this code? (`patterns_found`)

Read `problem_code` first. If it is empty or too short to answer, open `sol_file` and search it for the
functions the finding names.

Set `consistent` to true only when the file is the code the finding is about and the described problem can be
seen in it. Set it to false when:

- the problem sits in another file, and the linked file only shows a caller, an interface or a test;
- the file is a different version of the code, where the vulnerable lines are missing or already fixed;
- the downloaded file is not the code at all (an error page, an empty file, a different project).

`confidence` is 0 to 100 and says how sure you are of `consistent`.

## Classification

`mando_primary` is one of the seven MANDO categories, or null when none fits (then `mando_applicable` is false):
access_control, arithmetic, denial_of_service, front_running, reentrancy, time_manipulation,
unchecked_low_level_calls.

`scsvs_primary` is one SCSVS code, and `scsvs_name` its name:
G1 Architecture, design and threat modeling; G2 Policies and procedures; G3 Upgradeability; G4 Business logic;
G5 Access control; G6 Communications; G7 Arithmetic; G8 Denial of service; G9 Blockchain data;
G10 Gas usage & limitations; G11 Code clarity; G12 Test coverage; C1 Token; C2 Governance; C3 Oracle; C4 Vault;
C5 Bridge; C6 NFT; C7 Liquid staking; C8 Liquidity pool; C9 Uniswap V4 Hook; I1 Basic; I2 Token; I3 Oracle;
I4 Cross-Chain.

`vulnerability_type` is a short plain description, for example "rounding error in share price".

## Output

`verdicts_<n>.jsonl`, one JSON object per line, one line per packet, with these keys:

```json
{"id": "...", "meta_json": "copied from the packet", "consistent": true, "confidence": 90,
 "summary_matches": true, "content_matches": true, "content_reasoning": "one to three sentences",
 "functions_found": ["withdraw"], "variables_found": ["balances"], "patterns_found": ["state update after external call"],
 "issues": [], "mando_primary": "reentrancy", "mando_applicable": true,
 "scsvs_primary": "G6", "scsvs_name": "Communications", "vulnerability_type": "reentrancy in withdraw"}
```

`python3 -I scripts/review_tier1.py --merge` then copies each verdict into the finding's metadata JSON as
`validation`, with the same keys `validate_with_openai.py` writes.
