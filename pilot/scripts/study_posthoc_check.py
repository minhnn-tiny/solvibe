#!/usr/bin/env python3
"""Run checks written after the repair input study's runs started on the repairs the LLM judge
reviews. These checks are not part of the frozen attack set. They are reported on their own, and
they are used to confirm or reject judge and review reports.

- P6 (repair_checks/PoV63008_Bit255Start.t.sol) is P2's attack with a start tick whose compressed
  position is bit 255 of a bitmap word. Written on 2026-10-20, after one repair was seen that handles
  every start tick except that one.
- P7 (repair_checks/SwapDownNoTickBelow.t.sol) passes when a taxed zero-for-one swap with no
  initialized tick below the price needs more gas than a 30,000,000-gas block. Written on 2026-10-20
  to check a judge report on one repair.
- P8 (repair_checks/EmptyRangeAtNegativeTick.t.sol) passes when a taxed zero-for-one swap that keeps
  the pool at a negative tick reverts, because the empty range returns a tick that changes the
  liquidity. Written on 2026-10-20 to check a judge report on one repair. The human fix's
  TickIterator.sol on the audited code also fails it, by a different path; the audited code and the
  reference repair pass it.
The folder is pilot/tasks/63008/extension/. "works" means the flaw is present.

Writes <run>/judge/<check>_posthoc.json (forge's full output) and pilot/runs/repair_input_study/posthoc.json.
Usage: study_posthoc_check.py [--all]   (--all: every run that compiles, not only the judge's set)
"""
import argparse, json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_task as rt
from security_review import study_needs_judge

STUDY = rt.ROOT / "pilot/runs/repair_input_study"
CHECKS = [{"name": "P6", "src": "pilot/tasks/63008/extension/repair_checks/PoV63008_Bit255Start.t.sol",
           "dest": "test/PoV63008_Bit255Start.t.sol", "contract": "PoV63008_Bit255Start",
           "test": "test_check_swapDownFromLastBitOfWord()", "blocked_reason": "next call did not revert as expected"},
          {"name": "P7", "src": "pilot/tasks/63008/extension/repair_checks/SwapDownNoTickBelow.t.sol",
           "dest": "test/SwapDownNoTickBelow.t.sol", "contract": "SwapDownNoTickBelow",
           "test": "test_check_taxedSwapDownWithNoInitializedTickBelow()",
           "blocked_reason": "swap fits in a block: [0-9]+ <= 30000000"},
          {"name": "P8", "src": "pilot/tasks/63008/extension/repair_checks/EmptyRangeAtNegativeTick.t.sol",
           "dest": "test/EmptyRangeAtNegativeTick.t.sol", "contract": "EmptyRangeAtNegativeTick",
           "test": "test_check_taxedSwapThatKeepsANegativeTick()", "blocked_reason": "next call did not revert as expected"}]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    man = json.loads((rt.ROOT / "pilot/tasks/63008/extension/manifest.json").read_text())
    out_file = STUDY / "posthoc.json"
    done = json.loads(out_file.read_text()) if out_file.exists() else {}
    for rp in sorted(STUDY.glob("*/*/rep*/result.json")):
        d = rp.parent
        key = str(d.relative_to(STUDY))
        r = json.loads(rp.read_text())
        todo = [c for c in CHECKS if c["name"] not in done.get(key, {})]
        if ".attempt" in d.name or not todo or not r.get("compiled"):
            continue
        if not (a.all or study_needs_judge(r)):
            continue
        ws = d / "posthoc_ws"
        rt.setup_workspace(man, ws, "", blank=False)
        if (d / "agent.patch").read_text().strip():
            rt.run(["git", "-C", str(ws), "apply", str(d / "agent.patch")])
        for c in todo:
            rt.copy_into(rt.resolve(c["src"]), ws / c["dest"])
            data = rt.forge_json(ws, "/work", f"forge test --match-path {c['dest']} --match-test '^{c['test'][:-2]}\\('",
                                 f"{c['name']}_posthoc", d / "judge")
            state, why = rt.pov_state(c, data)
            done.setdefault(key, {})[c["name"]] = state
            done[key][c["name"] + "_reason"] = why
            print(key, c["name"], state, why, flush=True)
        shutil.rmtree(ws, ignore_errors=True)
        out_file.write_text(json.dumps(dict(sorted(done.items())), indent=1))


if __name__ == "__main__":
    main()
