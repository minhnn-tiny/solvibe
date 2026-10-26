#!/usr/bin/env python3
"""Blinded review pack of the repair input study: one folder per run, named by a random ID, so a
reviewer can read the repairs, the attack results and the judge reports without knowing the arm.

Writes pilot/runs/repair_input_study/blind_review/<ID>/ with:
  repair.patch   the agent's change to src/
  checks.md      compile result, functional failures, and each attack's state and failure reason
  judge/         the two LLM judge replies, for the repairs the judge reviewed
and pilot/runs/repair_input_study/blind_key.json, which maps each ID to its run. Reviewers must not
open the key until their review is recorded. Building the pack again gives the same IDs (fixed seed)
and deletes everything in the pack folder, so keep reviews outside it.

Usage: study_blind_pack.py
"""
import json, random, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "pilot/runs/repair_input_study"
PACK = STUDY / "blind_review"
SEED = 63008


def main():
    runs = sorted(p.parent for p in STUDY.glob("*/*/rep*/result.json") if ".attempt" not in p.parent.name)
    ids = [f"R{i:03d}" for i in range(1, len(runs) + 1)]
    random.Random(SEED).shuffle(ids)
    shutil.rmtree(PACK, ignore_errors=True)
    key = {}
    for rid, d in zip(ids, runs):
        r = json.loads((d / "result.json").read_text())
        out = PACK / rid
        out.mkdir(parents=True)
        shutil.copy2(d / "agent.patch", out / "repair.patch")
        f = r.get("functional") or {}
        lines = [f"# {rid}", "", f"- Compiles: {r.get('compiled')}",
                 f"- Functional suite: {f.get('passed')} passed, {f.get('failed')} failed of 61"]
        lines += [f"  - failed: `{t}`: {why}" for t, why in (f.get("failures") or {}).items()]
        lines += ["", "| Attack | State | Failure reason |", "|---|---|---|"]
        for p, v in (r.get("povs") or {}).items():
            extra = f" (profit {v['profit_wei'] / 1e18:.3f} ETH)" if v.get("profit_wei") is not None else ""
            lines.append(f"| {p} | {v['state']} | {(v.get('reason') or '').replace('|', '/')}{extra} |")
        # The full forge output of the five frozen attacks only. The checks written after the runs
        # started (P6_posthoc.json and later) stay out, so a review is independent of them.
        for p in sorted((d / "judge").glob("P[1-5].json")):
            shutil.copy2(p, out / f"forge_{p.name}")
        (out / "checks.md").write_text("\n".join(lines) + "\n")
        jd = STUDY / "llm_judge" / "__".join(d.relative_to(STUDY).parts)
        if jd.is_dir():
            (out / "judge").mkdir()
            for m in jd.glob("*.json"):
                j = json.loads(m.read_text())
                (out / "judge" / m.name).write_text(json.dumps({"model": j["model"], "review": j["review"]}, indent=1))
        key[rid] = str(d.relative_to(STUDY))
    (STUDY / "blind_key.json").write_text(json.dumps(dict(sorted(key.items())), indent=1))
    print(f"{len(key)} runs packed in {PACK}")


if __name__ == "__main__":
    main()
