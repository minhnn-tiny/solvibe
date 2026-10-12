# Extracted Contracts JSON Guide

This folder stores extracted smart-contract artifacts and summary metadata used by the pipeline.

The two JSON files in this folder are:

1. `extraction_stats.json`
2. `shared_github_files.json`

In addition, each extracted finding also has a detailed JSON file inside:

- `tier_1_complete/*.json`
- `tier_3_snippets/*.json`

The section below documents **all fields** for that detailed per-finding format.

## 0) Per-finding JSON schema (tier files)

Applies to files such as `tier_1_complete/64837_Market.json` and `tier_3_snippets/64887_contract.json`.

### Top-level fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Vulnerability/finding identifier (for example `64837`). |
| `extraction_type` | string | Yes | Extraction method label (for example `github_complete`, `markdown_code_block`). |
| `source_url` | string | Conditional | GitHub URL to referenced line(s); usually present for `github_complete`. |
| `source` | string | Conditional | Non-GitHub source label (for example `markdown_content`); common for markdown-based extraction. |
| `block_index` | integer | Conditional | Index of markdown code block used as source when extraction comes from markdown blocks. |
| `is_combined` | boolean | Conditional | Whether multiple markdown blocks were combined into one extracted result. |
| `is_complete` | boolean | Yes | Whether the extracted code is considered complete for the finding. |
| `tier` | string | Yes | Output quality tier (`tier_1`, `tier_2`, `tier_3`). |
| `referenced_lines` | array of integer pairs | Conditional | List of line ranges from source file used to anchor extraction (for example `[[437,437]]`). |
| `filename` | string | Yes | Name of generated Solidity file stored next to JSON. |
| `has_pragma` | boolean | Yes | Whether extracted Solidity contains a pragma directive. |
| `has_contract` | boolean | Yes | Whether extracted Solidity includes a contract/interface/library declaration. |
| `has_function` | boolean | Yes | Whether extracted Solidity includes at least one function declaration. |
| `balanced_braces` | boolean | Yes | Whether extracted code has balanced `{}` braces. |
| `num_lines` | integer | Yes | Number of lines in extracted Solidity text. |
| `vulnerability_title` | string | Yes | Original finding title/summary. |
| `recommendation` | object | Yes | Extracted recommendation section and code blocks. |
| `poc` | object | Yes | Extracted proof-of-concept section and code blocks. |
| `problem_code` | object | Yes | Main vulnerable/relevant code snippets used for analysis. |
| `extraction_date` | string (ISO datetime) | Yes | Timestamp of extraction. |
| `validation` | object | Yes | Validation, tagging, classification, and generated-fix metadata. |

### `recommendation` object

| Field | Type | Required | Description |
|---|---|---|---|
| `recommendation.has_recommendation` | boolean | Yes | Whether recommendation text exists. |
| `recommendation.recommendation_text` | string | Yes | Recommendation text, may include markdown and separators. |
| `recommendation.fix_code_blocks` | array | Yes | Code blocks detected in recommendation section (may be empty). |

### `poc` object

| Field | Type | Required | Description |
|---|---|---|---|
| `poc.has_poc` | boolean | Yes | Whether PoC text exists. |
| `poc.poc_text` | string | Yes | PoC text content (empty string when absent). |
| `poc.poc_code_blocks` | array | Yes | Code blocks detected in PoC section (may be empty). |

### `problem_code` object

| Field | Type | Required | Description |
|---|---|---|---|
| `problem_code.has_problem_code` | boolean | Yes | Whether problem code snippets were extracted. |
| `problem_code.source` | string | Yes | Source strategy (for example `github_line_refs_function_scope`, `markdown_blocks`). |
| `problem_code.snippets` | array | Yes | List of extracted code snippet objects. |

`problem_code.snippets[]` fields (schema is partially source-dependent):

| Field | Type | Required | Description |
|---|---|---|---|
| `function_name` | string | Optional | Function name when snippet is function-scoped. |
| `start_line` | integer | Optional | Start line in source file for function-scoped extraction. |
| `end_line` | integer | Optional | End line in source file for function-scoped extraction. |
| `code` | string | Yes | Solidity code snippet text. |
| `confidence` | integer | Yes | Extraction confidence score (typically 0-100). |
| `reason` | string | Yes | Why this snippet was selected. |
| `matched_references` | array of integer pairs | Optional | Referenced source ranges matched to this snippet. |
| `block_index` | integer | Optional | Original markdown block index for markdown-based snippets. |

### `validation` object

| Field | Type | Required | Description |
|---|---|---|---|
| `validation.content_code_consistency` | object | Yes | Checks whether extracted code matches finding summary/content. |
| `validation.report_tag_validation` | object | Yes | Tag presence/correctness and suggested tags. |
| `validation.mando_classification` | object | Yes | MANDO taxonomy classification output. |
| `validation.scsvs_classification` | object | Yes | SCSVS classification output. |
| `validation.generated_fix` | object | Yes | Auto-generated fix proposal metadata. |
| `validation.fix_code_source` | string | Yes | Source label for fix code (for example `generated`). |
| `validation.validated_at` | string (ISO datetime) | Yes | Timestamp when validation finished. |
| `validation.model` | string | Yes | Model used for validation/generation (for example `gpt-4o`). |
| `validation.code_input_source` | string | Yes | Input strategy used for code passed to validator. |

### `validation.content_code_consistency`

| Field | Type | Required | Description |
|---|---|---|---|
| `consistent` | boolean | Yes | Overall consistency verdict. |
| `confidence` | integer | Yes | Confidence score for consistency verdict. |
| `summary_matches` | boolean | Yes | Whether finding summary matches extracted evidence. |
| `content_matches` | boolean | Yes | Whether detailed content matches extracted code. |
| `summary_reasoning` | string | Yes | Reasoning for summary match verdict. |
| `content_reasoning` | string | Yes | Reasoning for content match verdict. |
| `functions_found` | array of string | Yes | Function names identified in extracted context. |
| `variables_found` | array of string | Yes | Variable names identified in extracted context. |
| `patterns_found` | array of string | Yes | Vulnerability patterns identified. |
| `issues` | array of string | Yes | Concrete issue statements extracted by validator. |

### `validation.report_tag_validation`

| Field | Type | Required | Description |
|---|---|---|---|
| `existing_tag` | string or null-like string | Yes | Existing report tag value. In some files it can be literal string `"null"`. |
| `tag_present` | boolean | Yes | Whether a tag is present in original report. |
| `tag_correct` | boolean or null | Yes | Whether existing tag is correct (`null` when no tag). |
| `confidence` | integer | Yes | Confidence score for tag validation. |
| `reasoning` | string | Yes | Explanation of tag decision. |
| `suggested_tag` | string | Yes | Proposed best tag. |
| `alternative_tags` | array of string | Yes | Other plausible tags. |
| `correction_explanation` | string | Yes | Why the suggested tag is more appropriate. |

### `validation.mando_classification`

| Field | Type | Required | Description |
|---|---|---|---|
| `primary_category` | string | Yes | Primary MANDO category. May be literal string `"null"` when not applicable. |
| `secondary_categories` | array of string | Yes | Additional MANDO categories. |
| `confidence` | integer | Yes | Confidence score for MANDO classification. |
| `mando_applicable` | boolean | Yes | Whether MANDO taxonomy is considered applicable. |
| `reasoning` | string | Yes | Rationale for MANDO classification decision. |

### `validation.scsvs_classification`

| Field | Type | Required | Description |
|---|---|---|---|
| `primary_category` | string | Yes | SCSVS category code (for example `G4`). |
| `primary_category_name` | string | Yes | Human-readable SCSVS category name. |
| `secondary_categories` | array of string | Yes | Additional SCSVS category codes. |
| `confidence` | integer | Yes | Confidence score for SCSVS classification. |
| `use_scsvs_instead` | boolean | Yes | Whether SCSVS is preferred over MANDO for this finding. |
| `reasoning` | string | Yes | Rationale for SCSVS mapping. |
| `vulnerability_type` | string | Yes | Normalized vulnerability type sentence. |

### `validation.generated_fix`

| Field | Type | Required | Description |
|---|---|---|---|
| `has_fix` | boolean | Yes | Whether a generated fix was produced. |
| `fix_approach` | string | Yes | High-level fix strategy. |
| `fixed_code_blocks` | array | Yes | Per-snippet generated replacement(s). |
| `key_changes` | array of string | Yes | Main code-level changes introduced by fix. |
| `security_improvements` | array of string | Yes | Security outcomes expected from fix. |
| `additional_recommendations` | string | Yes | Additional follow-up recommendations. |
| `confidence` | integer | Yes | Confidence score for generated fix quality. |
| `fix_code` | string | Yes | Consolidated generated fix code as a single string block. |
| `expected_fixed_blocks` | integer | Yes | Expected number of fixed blocks requested. |
| `returned_fixed_blocks` | integer | Yes | Number of fixed blocks actually returned. |
| `block_count_match` | boolean | Yes | Whether expected/returned block counts match. |
| `generated_by` | string | Yes | Generator/provider label. |
| `generation_date` | string (ISO datetime) | Yes | Timestamp when fix was generated. |

`validation.generated_fix.fixed_code_blocks[]` fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `snippet_index` | integer | Yes | 1-based index of original snippet being fixed. |
| `function_name` | string | Optional | Function name associated with this fixed snippet. |
| `fixed_function_code` | string | Yes | Generated fixed function/snippet code. |
| `reasoning` | string | Yes | Explanation of why this fix works. |

### Important notes for parsing

- Not every field appears in every file. Presence depends on `extraction_type` and source.
- Some null-like values are stored as literal strings (for example `"null"`) instead of JSON `null`.
- Arrays like `fix_code_blocks`, `poc_code_blocks`, and `issues` can be empty.
- For robust tooling, treat optional fields as nullable and fall back safely.

## 1) extraction_stats.json

Purpose:
- High-level run summary for the extraction process.
- Useful for reporting coverage, success rate, and common failure modes.

Current structure:

```json
{
  "total_processed": 100,
  "successful_extractions": 95,
  "github_attempted": 84,
  "github_successful": 80,
  "by_tier": {
    "tier_1_github_complete": 80,
    "tier_2_code_blocks": 0,
    "tier_3_snippets": 15
  },
  "by_extraction_type": {
    "github_complete": 80,
    "markdown_code_block": 15,
    "content_snippet": 0
  },
  "failed": 5,
  "failure_reasons": {
    "no_code_found_no_source": 5
  }
}
```

Field descriptions:
- `total_processed`: Total number of findings/items attempted.
- `successful_extractions`: Number of items where source content was extracted successfully.
- `github_attempted`: Number of items for which GitHub-source retrieval was attempted.
- `github_successful`: Number of successful GitHub-source retrievals.
- `by_tier`: Count split by output quality tier:
  - `tier_1_github_complete`: Full source file retrieved from GitHub.
  - `tier_2_code_blocks`: Extracted primarily from markdown code blocks.
  - `tier_3_snippets`: Partial snippet-level extraction.
- `by_extraction_type`: Same outcomes grouped by extraction method name.
- `failed`: Number of items that could not be extracted.
- `failure_reasons`: Breakdown of known failure categories and their counts.

Exhaustive field reference (`extraction_stats.json`):

| Field | Type | Required | Description |
|---|---|---|---|
| `total_processed` | integer | Yes | Number of total findings/items passed into extraction. |
| `successful_extractions` | integer | Yes | Number of items where contract content was extracted successfully (any tier). |
| `github_attempted` | integer | Yes | Number of items where GitHub retrieval was attempted as part of extraction. |
| `github_successful` | integer | Yes | Number of successful GitHub retrievals. |
| `by_tier` | object | Yes | Aggregated counts by output-quality tier. |
| `by_tier.tier_1_github_complete` | integer | Yes | Count of full-file GitHub extractions. |
| `by_tier.tier_2_code_blocks` | integer | Yes | Count of markdown code-block extractions. |
| `by_tier.tier_3_snippets` | integer | Yes | Count of snippet-level extractions. |
| `by_extraction_type` | object | Yes | Aggregated counts by extraction method label. |
| `by_extraction_type.github_complete` | integer | Yes | Method-level count for full GitHub file extraction. |
| `by_extraction_type.markdown_code_block` | integer | Yes | Method-level count for markdown code-block extraction. |
| `by_extraction_type.content_snippet` | integer | Yes | Method-level count for content-snippet extraction. |
| `failed` | integer | Yes | Number of items that failed extraction. |
| `failure_reasons` | object | Yes | Dictionary of failure reason codes to integer counts. |
| `failure_reasons.<reason_code>` | integer | Dynamic | For each reason code string (for example `no_code_found_no_source`), stores how many failures match it. |

Consistency checks (expected relationships):
- `successful_extractions + failed = total_processed`
- `github_successful <= github_attempted`
- `files_with_multiple_refs + files_with_single_ref = total_github_files` (in `shared_github_files.json`)

How to use for reporting:
- Coverage = `successful_extractions / total_processed`.
- GitHub success rate = `github_successful / github_attempted`.
- Tier distribution indicates data quality mix for downstream modeling.

## 2) shared_github_files.json

Purpose:
- Maps contract filenames to all vulnerability findings that reference the same file.
- Helps identify high-frequency target files (for prioritization and deduplication).

Top-level structure:

```json
{
  "total_github_files": 34,
  "files_with_multiple_refs": 16,
  "files_with_single_ref": 18,
  "files": {
    "RiskEngine.sol": {
      "reference_count": 10,
      "vulnerabilities": [
        {
          "id": "65025",
          "title": "...",
          "file_key": "owner/repo/commit/path/to/file.sol"
        }
      ]
    }
  }
}
```

Field descriptions:
- `total_github_files`: Number of distinct contract filenames found in GitHub-based extraction.
- `files_with_multiple_refs`: Number of filenames linked to more than one vulnerability finding.
- `files_with_single_ref`: Number of filenames linked to exactly one finding.
- `files`: Dictionary keyed by contract filename (for example, `RiskEngine.sol`).
  - `reference_count`: Number of findings that point to this filename.
  - `vulnerabilities`: List of linked findings.
    - `id`: Finding identifier (matches markdown filename in `data_collection/markdown_files`).
    - `title`: Finding title/summary.
    - `file_key`: Canonical source locator in the format `owner/repo/revision/path`.

Exhaustive field reference (`shared_github_files.json`):

| Field | Type | Required | Description |
|---|---|---|---|
| `total_github_files` | integer | Yes | Total count of unique contract filenames tracked in `files`. |
| `files_with_multiple_refs` | integer | Yes | Number of filenames whose `reference_count > 1`. |
| `files_with_single_ref` | integer | Yes | Number of filenames whose `reference_count = 1`. |
| `files` | object | Yes | Dictionary keyed by contract filename (for example `RiskEngine.sol`). |
| `files.<contract_filename>` | object | Dynamic | Per-file aggregate object for one contract filename. |
| `files.<contract_filename>.reference_count` | integer | Yes (per file) | Number of findings attached to this filename. |
| `files.<contract_filename>.vulnerabilities` | array | Yes (per file) | List of finding objects referencing this contract filename. |
| `files.<contract_filename>.vulnerabilities[].id` | string | Yes | Finding ID (also used as markdown filename in `data_collection/markdown_files`). |
| `files.<contract_filename>.vulnerabilities[].title` | string | Yes | Human-readable finding title. |
| `files.<contract_filename>.vulnerabilities[].file_key` | string | Yes | Canonical source locator in format `owner/repo/revision/path/to/file`. |

Notes on dynamic keys:
- `files` keys are not fixed; each key is a discovered filename (for example `Launchpad.sol`, `RiskEngine.sol`).
- `failure_reasons` keys are not fixed; each key is a discovered failure-code label.

How to use for reporting:
- Use `reference_count` to rank which contracts appear most frequently in findings.
- Use `vulnerabilities` to trace each contract to concrete finding IDs and titles.
- Use `file_key` for reproducibility (which repository and revision the source came from).

## Related output folders

- `tier_1_complete/`: Full files retrieved from source repositories.
- `tier_2_code_blocks/`: Markdown-derived code blocks.
- `tier_3_snippets/`: Smaller extracted snippets.

Interpretation:
- Tier 1 generally offers the best context for model training/analysis.
- Tier 2 and Tier 3 are useful fallback data when full source is unavailable.

## Note on stability

Field names are expected to stay stable for pipeline compatibility, but counts will change as extraction is rerun on new data.