# Frame of 2024 and 2025 audits, and the development draw

This folder builds the protocol frame that the proposal samples from (proposal section 5.1). It also records the draw of the three development protocols. It was run on 2026-10-26 at the student's request.

## Files

- The seed record (`SEED.txt`). The draw seed, 20261026, written before the frame was built.
- The frame list script (`list_repos.py`, no network). It lists the 2024 and 2025 Code4rena, Sherlock and Cantina audits with Solidity code from the per-protocol inventory (`../frame_inventory/per_protocol_audit.csv`). For each audit it records the GitHub repositories that the audit's findings link to. Output: `frame_list.csv`.
- The fetch-and-count script (`fetch_and_count.py`, network, read-only). For each linked repository it fetches the Solidity files at the linked commit, finds the audit scope, and counts eligible functions with the frame audit's counting rule (`../frame_audit/count_functions.py`). Outputs: `frame_counts.csv` (one row per audit, with status and scope source) and `protocol_frame.csv` (the draw input).
- The accuracy check (`compare_with_audit.py`). It compares the automated counts with the hand counts of the 25-audit study (`../frame_audit/strict/per_audit_strict.csv`).
- The unit script (`frame_units.py`, no network, added after debate round 29). It applies the repository rule, merges duplicate audits, groups audits of the same project into one sampling unit and records the exact snapshots counted. Outputs: `frame_audits.csv` (one row per audit, with status and reason), `frame_snapshots.csv` (one row per counted repository: resolved commit, scope-file hash, in-scope file list hash, eligible functions) and `protocol_units.csv` (the main frame).
- The draw output: `../../dev_case/drawn_protocols.csv`.

## How to reproduce

```bash
cd /Users/minh/Documents/workspaces/secure-solvibe
python3.12 -I proposal_workspace/evidence/frame_build/list_repos.py
python3.12 -I proposal_workspace/evidence/frame_build/fetch_and_count.py --clones <empty folder>
python3.12 -I proposal_workspace/evidence/frame_build/compare_with_audit.py
python3.12 -I proposal_workspace/evidence/frame_build/frame_units.py --clones <the same folder>
python3.12 -I proposal_workspace/dev_case/draw_protocols.py proposal_workspace/evidence/frame_build/protocol_frame.csv --count 3 --seed 20261026 --out proposal_workspace/dev_case/drawn_protocols.csv
```

The fetch step makes about 220 anonymous, read-only fetches from GitHub, one per linked repository. Nothing from the repositories is built or run. A repository that needs a login fails and is recorded as not accessible.

## First count (the input of the development draw)

This section describes the first count, `protocol_frame.csv`. The development draw used it. The corrected main frame is described further down.

- The inventory lists 313 audits from 2024 and 2025 with Solidity code: 92 Code4rena audits (69 from 2024, 23 from 2025), 118 Sherlock audits (83 and 35) and 103 Cantina audits (83 and 20).
- 106 audits have no GitHub link in their findings. 103 of them are Cantina audits, mostly private reviews. Their code cannot be found automatically, so they are not in the counted frame.
- 16 audits link only to repositories that need a login.
- 1 audit (Sherlock 2025, Burve, `sherlock-858`) is recorded in `frame_counts.csv` as having no eligible function. A later check on 2026-10-26 showed why: the linked branch of its repository holds only a README and an empty `.gitmodules` file. Its code is not accessible either, so it is outside the frame for the same reason as the 16 above. It is not a protocol with a zero count, so the rule "a zero count uses one" does not apply.
- **190 audits are counted.** They hold 22,802 eligible functions: median 78.5 per audit, largest 1,020.

So the counted frame contains Code4rena and Sherlock audits only. Cantina audits are not in it, because their code is not linked. The proposal's frame text should say so.

## Scope in the first count

For each repository, the scope comes from the first of these that exists:

1. the Code4rena `scope.txt` file (77 audits);
2. the README's scope section: "Audit scope" in Sherlock repositories, "Scope" or "Files in scope" in older Code4rena repositories, up to any "out of scope" heading (110 audits);
3. otherwise every .sol file outside test, mock, script, library and dependency folders (4 audits).

If one of an audit's repositories has an explicit scope, its other repositories are ignored.

These counts overlap: one audit (`code4rena-476`) used both a `scope.txt` file and a README scope. As mutually exclusive categories: 76 audits used `scope.txt` only, 109 the README only, 1 both and 4 the automatic rule.

## Accuracy

20 of the 25 hand-counted audits are in the counted frame. For all 20, the automated count of eligible functions equals the hand count. Against the stricter N count of the hand study (eligible functions minus those linked to findings), the automated count is 3% to 40% higher, median 7%, with Spearman's rank correlation 0.986.

The automated count is the size measure for drawing protocols. An error in it changes how efficient the sample is, not whether the estimates are unbiased, because the inclusion probabilities actually used are recorded. Sampled protocols still get their exact scope and V and N labels by hand (step S1 of `../../dev_case/README.md`).

## Development draw

`draw_protocols.py` drew three protocols by randomized systematic sampling with probabilities proportional to the eligible count, seed 20261026.

| Order | Protocol | Audit | Eligible functions | Inclusion probability |
|---|---|---|---:|---:|
| 1 | The Wildcat Protocol | Code4rena 2024, contest 434 | 206 | 0.0271 |
| 2 | Perennial V2 Update #3 | Sherlock 2024, contest 518 | 370 | 0.0487 |
| 3 | Fenix Finance | Code4rena 2024, contest 440 | 75 | 0.0099 |

The SHA-256 of `drawn_protocols.csv` is fecf61e6dde94435e75e666ea6a75f9509b9e0b51d650df61d99a02658e5ddfb. None of the three is a pilot protocol. The cases follow the draw order, so case 1, the timed case, is The Wildcat Protocol. These three protocols are removed from the frame before the main sample is drawn.

## Corrections after debate round 29 (the main frame)

Peer B found two defects in the first count, and Peer A found more of the same kind:

- `code4rena-396` and `code4rena-399` are the same Krystal DeFi audit. They have the same repository, commit and links.
- `sherlock-1202` (Inverse Finance) was counted only from a dependency, `transmissions11/solmate`, because its contest repository needs a login.
- `code4rena-476` (Unruggable) also counted the in-scope files of `code-423n4/2024-07-optimism`, the contest repository of another audit.
- `code4rena-443` (Coded Estate) was counted only from `code-423n4/2023-12-revolutionprotocol`, a contest ten months earlier.
- `code4rena-317` (reNFT) and `code4rena-522` (Garden) were counted from repositories outside the contest organisations.
- Several projects have more than one audit in the frame, for example Perennial V2 Updates #2, #3 and #4.

`frame_units.py` applies three rules to the first count. It uses the same clones, so nothing is fetched again.

1. **Repository rule.** A linked repository counts as an audit's code only if two things hold. It belongs to the contest organisation (`code-423n4` or `sherlock-audit`). And the year and month at the start of its name are within one month of the audit's month. In the first count, 186 linked contest repositories matched the audit's month exactly and one was one month off; the two cross-contest links were five and ten months off.
2. **Duplicates.** Audits whose counted repositories and commits are identical are one audit. The lowest-numbered record is kept.
3. **Projects.** Audits whose inventory protocol names share their first word (ignoring "The", "Audit" and "Protocol") form one sampling unit. Peer A checked the 25 groups this gives by hand on 26 October 2026. Each is one organisation's protocol, for example Panoptic, LoopFi, Perennial, Ethos, SYMMIO and Optimism.

Results:

- 185 audits are counted, with 22,322 eligible functions: 83 Code4rena and 102 Sherlock; 143 from 2024 and 42 from 2025.
- Excluded: 106 with no linked repository; 4 whose audited code is not identified (reNFT, Tapioca DAO, Coded Estate, Garden); 16 whose contest repository needs a login (now including Inverse Finance); 1 with no Solidity code at the linked version (Burve); 1 duplicate (Krystal DeFi).
- Scope, mutually exclusive: `scope.txt` 74, README scope 109, automatic 2.
- One count changed: Unruggable falls from 141 to 66 eligible functions.
- The 20 hand-counted audits are unchanged and still equal the hand counts.
- The 185 audits form 155 units. 24 units hold more than one audit.

`frame_snapshots.csv` records the commit each counted repository resolved to. Many links name a branch (`main`) rather than a commit, including all three development audits. The commit is the version that was counted, and any later work uses it.

### The development draw

The development draw was made on the first count, before these corrections. It is kept as drawn. Its three audits are not among the defective records, and their counts are unchanged. The corrections change their inclusion probabilities only slightly. Those probabilities are recorded, and development results are not used in the main estimates. Drawing again after seeing the first result would break the rule that development protocols are never replaced.

The main frame removes every unit that contains a development audit. That is Wildcat, Fenix Finance and the whole Perennial project (Updates #2, #3 and #4). Perennial Update #3 is development case 2, and the three Perennial audits share code.

**The main frame has 152 units with 21,211 eligible functions** (`protocol_units.csv`, rows with `development` = 0).
