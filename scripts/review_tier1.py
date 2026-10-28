#!/usr/bin/env python3
"""Claude review of new tier 1 findings, in place of validate_with_openai.py (no LLM API calls).

Step 1 (default): write review packets, one JSON line per tier 1 finding that has no `validation` yet:
  title, finding text, the problem code the extractor took from the GitHub line references, and which
  identifiers named in the finding (`Foo::bar`, `bar()`, `baz`) occur in the downloaded .sol file.
Step 2 (by hand): reviewers answer the questions in REVIEW.md for each packet and write one verdict line each.
Step 3 (--merge): copy the verdicts into each metadata JSON as `validation`, in the structure
  validate_with_openai.py writes, so filter_tier1_after_cutoff.py treats both the same way.

Usage: python3 -I scripts/review_tier1.py [--batch batch_5] [--chunks 5]
       python3 -I scripts/review_tier1.py --merge [--batch batch_5]
Files: data_collection/<batch>_extracted_contracts/review/packets_<n>.jsonl and verdicts_<n>.jsonl
"""
import argparse, datetime, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "data_collection"
MODEL = "claude-opus-5-5 (review, no API)"
IDENT = re.compile(r"`([A-Za-z_]\w*(?:(?:::|\.)[A-Za-z_]\w*)?)(?:\(\))?`")
CUT = re.compile(r"(?:^|\n)#{1,4}\s*(?:Recommendations?|Recommended\s+Mitigation|Mitigation|Proof\s+of\s+Concept|PoC)\b"
                 r"|\n\*\*(?:Recommended Mitigation|Proof of Concept):\*\*", re.I)


def packet(meta_path, finding):
    meta, sol = json.loads(meta_path.read_text()), meta_path.with_suffix(".sol").read_text(errors="replace")
    text = finding.get("content", "")
    cut = CUT.search(text)
    names = sorted({n for n in IDENT.findall(finding.get("title", "") + "\n" + (text[:cut.start()] if cut else text))
                    if len(n.split("::")[-1].split(".")[-1]) > 2})
    found = [n for n in names if re.search(rf"\b{re.escape(n.split('::')[-1].split('.')[-1])}\b", sol)]
    snippets = [dict(lines=f"{s.get('start_line')}-{s.get('end_line')}", code="\n".join(s.get("code", "").splitlines()[:150]))
                for s in (meta.get("problem_code") or {}).get("snippets", [])[:6]]
    return dict(id=meta["id"], meta_json=str(meta_path), sol_file=str(meta_path.with_suffix(".sol")),
                source_url=meta.get("source_url"), impact=finding.get("impact"), firm=finding.get("firm_name"),
                protocol=finding.get("protocol_name"), title=finding.get("title"),
                finding_text=(text[:cut.start()] if cut else text)[:7000], problem_code=snippets,
                identifiers_in_finding=names, identifiers_found_in_file=found,
                identifiers_missing_from_file=[n for n in names if n not in found])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="batch_5")
    ap.add_argument("--chunks", type=int, default=5)
    ap.add_argument("--merge", action="store_true")
    a = ap.parse_args()
    tier1, review = ROOT / f"{a.batch}_extracted_contracts/tier_1_complete", ROOT / f"{a.batch}_extracted_contracts/review"
    if a.merge:
        merged = 0
        for vfile in sorted(review.glob("verdicts_*.jsonl")):
            for line in vfile.read_text().splitlines():
                v = json.loads(line)
                path = Path(v["meta_json"])
                meta = json.loads(path.read_text())
                meta["validation"] = dict(
                    validated_at=datetime.datetime.now().isoformat(timespec="seconds"), model=MODEL,
                    code_input_source=(meta.get("problem_code") or {}).get("source", "full_sol"),
                    content_code_consistency={k: v[k] for k in (
                        "consistent", "confidence", "summary_matches", "content_matches", "content_reasoning",
                        "functions_found", "variables_found", "patterns_found", "issues")},
                    mando_classification=dict(primary_category=v["mando_primary"], mando_applicable=v["mando_applicable"]),
                    scsvs_classification=dict(primary_category=v["scsvs_primary"], primary_category_name=v["scsvs_name"],
                                              vulnerability_type=v["vulnerability_type"]),
                    fix_code_source="provided" if (meta.get("recommendation") or {}).get("fix_code_blocks") else "none")
                path.write_text(json.dumps(meta, indent=2))
                merged += 1
        print(json.dumps(dict(merged=merged)))
        return
    findings = {str(f["id"]): f for f in json.loads((ROOT / f"downloaded_findings/{a.batch}_firm_findings.json").read_text())}
    todo = [p for p in sorted(tier1.glob("*.json")) if "validation" not in json.loads(p.read_text())]
    packets = [packet(p, findings[str(json.loads(p.read_text())["id"])]) for p in todo]
    review.mkdir(exist_ok=True)
    for n in range(a.chunks):
        part = packets[n::a.chunks]
        (review / f"packets_{n + 1}.jsonl").write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in part))
    print(json.dumps(dict(packets=len(packets), chunks=a.chunks, folder=str(review),
                          with_missing_identifiers=sum(bool(p["identifiers_missing_from_file"]) for p in packets))))


if __name__ == "__main__":
    main()
