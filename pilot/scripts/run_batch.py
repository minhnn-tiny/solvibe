#!/usr/bin/env python3
"""Run the four configurations over the pilot tasks and aggregate the results.

4 configs = {aider, openhands} x {openai (gpt-5.4-mini), anthropic (claude-sonnet-4-5}}.
One run per task per configuration (the agreed staging: five tasks first). Each run goes
through pilot/scripts/run_task.py. After each run the agent's diff and log are kept under
the run's output dir and the big workspace is deleted to save disk.

Writes pilot/results/pilot_runs.csv and prints a summary with per-provider token totals.
A soft token ceiling per provider stops further runs for that provider if crossed.

Usage: run_batch.py [--tasks 62347,62348,...] [--token-cap 40000000]
"""
import argparse, csv, json, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIGS = [("aider", "openai"), ("aider", "anthropic"), ("openhands", "openai"), ("openhands", "anthropic")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="")
    ap.add_argument("--token-cap", type=int, default=40_000_000, help="soft per-provider token ceiling")
    a = ap.parse_args()
    if a.tasks:
        tasks = a.tasks.split(",")
    else:
        tasks = sorted(p.parent.parent.name for p in ROOT.glob("pilot/tasks/*/task/manifest.json"))
    print(f"tasks: {tasks}")
    prov_tokens = {"openai": 0, "anthropic": 0}
    rows = []
    for tid in tasks:
        man = ROOT / f"pilot/tasks/{tid}/task/manifest.json"
        if not man.exists():
            print(f"skip {tid}: no manifest"); continue
        for agent, prov in CONFIGS:
            if prov_tokens[prov] >= a.token_cap:
                print(f"SKIP {tid} {agent}/{prov}: {prov} token cap reached"); continue
            t0 = time.time()
            print(f"\n=== {tid} {agent}/{prov} ===", flush=True)
            subprocess.run([sys.executable, str(ROOT / "pilot/scripts/run_task.py"),
                            "--manifest", str(man), "--agent", agent, "--provider", prov])
            outdir = ROOT / "pilot/runs" / f"{agent}_{prov}" / tid
            ws = outdir / "workspace"
            res = {}
            rp = outdir / "result.json"
            if rp.exists():
                res = json.loads(rp.read_text())
            # preserve the agent's code change + log, then drop the heavy workspace
            for f in ("agent.patch", "agent_log.txt", "_oh_metrics.json"):
                if (ws / f).exists():
                    shutil.copy2(ws / f, outdir / f)
            shutil.rmtree(ws, ignore_errors=True)
            shutil.rmtree(outdir / "vuln_git", ignore_errors=True)
            tp = res.get("tokens_prompt") or 0
            tc = res.get("tokens_completion") or 0
            prov_tokens[prov] += tp + tc
            pov = res.get("pov") or {}
            fun = res.get("functional") or {}
            rows.append(dict(
                id=tid, protocol=res.get("protocol", ""), agent=agent, provider=prov,
                build_ok=res.get("build_ok"), vuln_reproduced=res.get("vuln_reproduced"),
                pov_passed=pov.get("passed"), pov_failed=pov.get("failed"),
                func_passed=fun.get("passed"), func_failed=fun.get("failed"),
                func_skipped="skipped" in fun,
                tokens_prompt=tp, tokens_completion=tc, cost_usd=res.get("cost_usd"),
                duration_s=res.get("duration_s"), wall_s=round(time.time() - t0, 1),
                error=(res.get("error") or res.get("agent_error") or "")[:120]))
            print(f"  -> build={rows[-1]['build_ok']} vuln_reproduced={rows[-1]['vuln_reproduced']} "
                  f"func={rows[-1]['func_passed']}/{(fun.get('passed') or 0)+(fun.get('failed') or 0)} "
                  f"tok={tp}+{tc}")
    # pilot_runs.csv and both master files are rebuilt from every result.json on disk,
    # so batches run on different tasks never overwrite each other's rows.
    subprocess.run([sys.executable, str(ROOT / "pilot/scripts/build_masters.py")])
    print("per-provider tokens (this batch):", prov_tokens)
    # compact summary
    print("\nid       agent      provider   build vuln_repro func")
    for r in rows:
        print(f"{r['id']:<8} {r['agent']:<10} {r['provider']:<10} {str(r['build_ok']):<5} "
              f"{str(r['vuln_reproduced']):<10} {r['func_passed']}/{(r['func_passed'] or 0)+(r['func_failed'] or 0) if r['func_passed'] is not None else 'na'}")


if __name__ == "__main__":
    main()
