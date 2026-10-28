# Data Collection Pipeline

This folder contains the end-to-end data preparation pipeline for collecting vulnerability reports, extracting Solidity code artifacts, and validating extracted artifacts with LLM-based checks.

## Quick Stats

| | Downloaded | Extracted (Tier 1) | Extracted (Tier 2) | Extracted (Tier 3) | Total Extracted |
|---|---|---|---|---|---|
| **Batch 1** | 100 | 80 | 0 | 15 | 95 |
| **Batch 2** | 100 | 16 | 0 | 71 | 87 |
| **Batch 3** | 100 | 16 | 8 | 63 | 87 |
| **Batch 4** | 19327 | 7714 | 137 | 5030 | 12881 |
| **Batch 5** (firm reports, see below) | 396 | 67 | 59 | 247 | 373 |
| **TOTAL** | 20023 | 7893 | 204 | 5426 | 13523 |


## Batch 5: findings from the audit firms' own reports

Solodit turned off its findings API in its September 2026 platform changes: every key, new ones included, gets
`401 Invalid API key`. Batch 5 replaces it for 2025-08-01 to 2026-10-27 by reading the reports where Solodit
used to get them:

| Source | Where | Format |
|---|---|---|
| Code4rena | `code4rena.com/reports/<contest>`, listed in the site's sitemap | HTML page |
| Cyfrin | `github.com/Cyfrin/cyfrin-audit-reports` | Markdown, PDF when there is no Markdown |
| Pashov Audit Group | `github.com/pashov/audits` (`team/` and `agentic/`) | Markdown, PDF when there is no Markdown |
| Trail of Bits | `github.com/trailofbits/publications/reviews` | PDF |
| Sherlock | `github.com/sherlock-protocol/sherlock-reports/audits` | PDF |
| Smaller firms (CODESPECT in this range) | `github.com/solodit/solodit_content/reports` | Markdown |

Steps, from the repository root:

```bash
python3 -I scripts/fetch_firm_reports.py --start 2025-08-01 --end 2026-10-27   # reports -> downloaded_findings/batch_5_raw/
python3 -I scripts/split_firm_reports.py                                        # one record per finding, duplicates removed
cd data_collection && python3 -u extract_contracts.py \
    --markdown-dir downloaded_findings/batch_5_firm_findings --output-dir batch_5_extracted_contracts && cd ..
python3 -I scripts/review_tier1.py           # review packets for the new tier 1 findings
                                             # reviewers write verdicts as batch_5_extracted_contracts/review/REVIEW.md says
python3 -I scripts/review_tier1.py --merge   # verdicts -> `validation` in each metadata JSON
python3 -I scripts/date_undated_findings.py  # dates for old findings whose links carry no date
python3 scripts/filter_tier1_after_cutoff.py --start 2025-08-01 --end 2026-10-27 \
    --out data_collection/tier1_2025-08-01_to_2026-10-27 \
    --master data_collection/tier1_master_2025-08-01_to_2026-10-27.csv \
    --lower data_collection/lower_tier_2025-08-01_to_2026-10-27.csv
python3 scripts/collection_stats.py          # counts -> tier1_2025-08-01_to_2026-10-27/stats.json
```

How the records are made:

- **Date.** The date in the report's file name. Code4rena uses the contest month in the report URL, as the
  filter did for Solodit's Code4rena findings. The page's publication date is kept in `report_published`.
- **Severity.** Only High and Medium findings are kept, as in batches 1-4. Critical counts as High, as on Solodit.
- **Solidity only.** A finding is kept when its own text points to Solidity more than to other languages
  (`.sol` files, `pragma solidity`, `msg.sender` against `.rs`, `fn`, `felt252`, `.func` and so on). A finding
  with no sign either way follows its report. This drops the Rust, Go, Cairo, Move and FunC audits.
- **Duplicates.** A finding is dropped when the old Solodit download already has it, or when an earlier report
  version has it (for example Cyfrin v2.0 and v2.1 of the same audit). Two findings match when they come from
  the same firm, from the same report or a report on the same protocol, and have the same or nearly the same
  title. Every dropped finding is listed in `batch_5_duplicates.csv` with the id it matched.
- **Ids.** `<source>-<date>-<protocol>-<label>`, for example `c4-2025-11-sukukfi-M-03`. Labels the firm did not
  give are numbered by severity (`M-01`, `M-02`, ...).
- **Review.** New tier 1 findings are checked by Claude reviewers, not by `validate_with_openai.py`. They answer
  the same consistency questions and use the same categories. The verdicts are kept in
  `batch_5_extracted_contracts/review/verdicts_*.jsonl`, so the merge can be rerun without a new review.

### Tier 1 collection, 2025-08-01 to 2026-10-27

Built on 2026-10-27 from batches 1-5 with the commands above.

| File | What it holds |
|---|---|
| `tier1_2025-08-01_to_2026-10-27/` | The 198 selected tier 1 findings: `.sol` file, metadata `.json`, report `.md`, plus `manifest.json` and `stats.json` (all counts below) |
| `tier1_master_2025-08-01_to_2026-10-27.csv` | One row per tier 1 finding of every batch, selected or not, with the date, how it was dated, and why it was left out |
| `lower_tier_2025-08-01_to_2026-10-27.csv` | The tier 2 and tier 3 findings in the same range, kept for a closer check later |
| `batch_5_reports.csv`, `batch_5_duplicates.csv` | Every downloaded report with its finding counts, and every finding dropped as a duplicate |
| `undated_finding_dates.csv` | Dates found for old findings whose links carry no date |
| `batch_5_extracted_contracts/review/` | Review instructions, packets and the 67 verdicts for the new tier 1 findings |

- **Selected:** 198 tier 1 findings (58 High, 140 Medium). 152 come from the Solodit download (34 of them dated
  through `undated_finding_dates.csv`), 46 from the firm reports.
- **By firm:** Code4rena 124, CODESPECT 18, Shieldify 13, OpenZeppelin 11, MixBytes 10, Cyfrin 9, Sherlock 9,
  Pashov Audit Group 2, ConsenSys 1, Trail of Bits 1.
- **Left out in the range:** 29 tier 1 findings without problem code (17) or that failed the consistency check (12).
  Of the 67 new tier 1 findings, the reviewers found 11 inconsistent. In most of them the GitHub link points to the code of
  another protocol the audited contract calls (Morpho, Aerodrome, Wormhole, OpenZeppelin), not to the audited code.
- **Lower tiers kept for later:** 621 findings (71 tier 2 files, 605 tier 3 files).
- **Coverage gap:** the newest selected finding is from 2026-05. Later findings exist (89 in the lower tiers from
  2026-06 to 2026-10), but the firms that published them, mainly Cyfrin, Pashov and Sherlock, quote code without a
  GitHub link to the file, or link to repositories that are private now. They need the lower-tier check, or a step that
  fetches the audited file from the repository and commit named in the report's scope section.

Known limits:

- PDF text comes from `pdftohtml`. Code in a monospace font is rebuilt as fenced blocks, but some titles keep a
  hyphen from a line break ("config-ured").
- Most Cyfrin and Pashov findings quote code without a GitHub link, so they reach tier 2 or 3, not tier 1.
- Findings whose GitHub repository is private now (some Sherlock audits) cannot reach tier 1.
- Pashov's `agentic/` reports were written by an AI auditing agent. Their ids are kept as they are, and the
  `report_path` field shows the folder, so they can be left out.
- Old findings whose links carry no date were dated from the first git commit of their report or the blog post
  date (`undated_finding_dates.csv`). Quantstamp certificates load with JavaScript, so those stay undated.

## Overview

The usual workflow is:

1. Download findings from Solodit API.
2. Extract Solidity artifacts from report content and linked GitHub sources.
3. Validate extracted artifacts and enrich metadata with consistency checks and vulnerability classifications.

Main scripts:

- `download.py`: fetch report data and persist it as batch JSON + markdown files.
- `analyze_data.py`: inspect markdown coverage and estimate extraction quality before extraction.
- `extract_contracts.py`: produce tiered Solidity artifacts and metadata.
- `validate_with_openai.py`: validate extracted artifacts and append classification/quality fields.

## Script Details

### 1) `download.py`

Purpose:
- Pull findings from Solodit API using pagination.
- Resume safely across runs with a state file.
- Deduplicate against prior batch JSON files.
- Save findings JSON and per-finding markdown files.

Key behavior:
- Uses `.env` values like `SOLODIT_API_KEY`, `PAGE_SIZE`, `TARGET_RUNS`, `STATE_FILE`, and `OUTPUT_FILE`.
- Stops cleanly when an API page returns zero findings.
- If the run stops mid-page (target reached), marks the page as incomplete and resumes from the same page on the next run.

Outputs:
- Batch findings JSON (for example under `downloaded_findings/`).
- Markdown files in a folder named from `OUTPUT_FILE` stem.
- Updated download state JSON.

### 2) `analyze_data.py`

Purpose:
- Survey all markdown files under `downloaded_findings/`.
- Report how many files contain GitHub `.sol` links, code blocks, inline snippets, and no extractable code.

When to use:
- Run before extraction to understand expected Tier 1/2/3 yield.

### 3) `extract_contracts.py`

Purpose:
- Extract Solidity code artifacts using a 3-tier priority system.

Tier priority:

```
Tier 1: GitHub .sol files (highest quality)
    -> fallback if unavailable
Tier 2: Solidity code blocks from markdown
    -> fallback if unavailable
Tier 3: Combined snippets from remaining inline content
```

Current default configuration in this script points to batch 4 paths:
- `downloaded_findings/batch_4_solodit_findings/`
- `batch_4_extracted_contracts/`

Extraction notes:
- Tier 1 downloads full `.sol` files from GitHub, ignoring line-anchor fragments for retrieval.
- Tier 2 keeps stronger Solidity code blocks that satisfy quality checks.
- Tier 3 combines multiple snippet fragments from one finding into one output artifact.

Outputs (under output batch directory):
- `tier_1_complete/`
- `tier_2_code_blocks/`
- `tier_3_snippets/`
- `extraction_stats.json`
- `shared_github_files.json`
- `failed_extractions.log`

### 4) `validate_with_openai.py`

Purpose:
- Validate extracted artifacts against their source finding.
- Enrich each metadata JSON with consistency checks, tag checks, and vulnerability classification.

Validation responsibilities:
- Content-code consistency validation.
- Existing tag correctness checks and suggested corrections.
- Classification into MANDO categories and SCSVS categories.
- Fix-code handling (use provided recommendation fix blocks or generate when needed).

Current default configuration points to batch 4 paths:
- Input extracted dir: `batch_4_extracted_contracts`
- Output validation dir: `batch_4_extracted_contracts/validation_results`

Detailed validation flow is documented in `README_VALIDATION.md`.

## Configuration

Use `.env` to configure API, rate limits, model settings, file names, and confidence thresholds.

Common fields used across scripts:

- Solodit/API fields:
    - `SOLODIT_API_KEY`
    - `PAGE_SIZE`
    - `TARGET_RUNS`
    - `STATE_FILE`
    - `OUTPUT_FILE`
- OpenAI validation fields:
    - `OPENAI_API_KEY`
    - `OPENAI_MODEL`
    - `OPENAI_TEMPERATURE`
    - `OPENAI_RATE_LIMIT_DELAY`
    - `OPENAI_RETRY_ATTEMPTS`
    - `CONFIDENCE_HIGH`
    - `CONFIDENCE_MEDIUM`
    - `CONFIDENCE_LOW`

See `.env.example` for baseline variable names.

## Typical Run Order

From this folder:

```bash
python download.py
python analyze_data.py
python extract_contracts.py
python validate_with_openai.py
```

Optional quick validation run:

```bash
python validate_with_openai.py --test
```

## Batch-Oriented Layout

This repository uses batch folders (for example `batch_1_extracted_contracts`, `batch_2_extracted_contracts`, etc.) to keep runs isolated and reproducible.

Recommended practice:

1. Keep each download/extract/validate cycle scoped to one batch folder.
2. Avoid mixing outputs from different batches in the same extraction directory.
3. Keep `OUTPUT_FILE` and extraction/validation directories aligned to the same batch.

## Notes

- Some scripts currently hardcode batch-specific paths (especially extraction and validation scripts). Update path constants before running a different batch.
- Downloading and validation are designed to be resumable and robust to partial failures; reruns should continue from saved state and existing outputs.

