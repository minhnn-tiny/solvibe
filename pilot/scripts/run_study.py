#!/usr/bin/env python3
"""Run the first experiment of the repair input study (finding 63008) in a random order.

The runs are fixed in PLAN (IDEA.md, section "First experiment"). Their order is shuffled once with
SEED and saved in <outroot>/run_order.json, so a restart keeps the same order. Each run is one call
of run_task.py --arm ... --rep ... --prune, and `workers` runs go at a time.

Retry rule, fixed before the runs: a run is repeated only when no model call succeeded (zero
tokens), for example a Docker error or an API error on the first call. Every other run counts as it
is, including timeouts and API errors later in the run. A repeated attempt's folder is kept as
rep<NN>.attempt<k>.

Usage: run_study.py [--calibration | --followup] [--workers 3] [--limit N] [--rejudge]
  --rejudge judges every finished run again from its saved agent.patch with the current judge,
  keeping the agent's records. It calls no model.
"""
import argparse, json, os, random, shutil, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAN = "pilot/tasks/63008/extension/manifest.json"
REPS = 12
PLAN = {("openhands", "openai"): ["L-E2", "R-E2", "P-E2", "RP-E2", "P-E0", "P-E1"],
        ("codex", "openai"): ["L-E2", "P-E0", "P-E1", "P-E2"],
        ("aider", "openai"): ["P-E0", "P-E1"]}
CALIBRATION = [("openhands", "openai", "P-E2", r) for r in range(1, 5)]
SEED = 20261020
# Follow-up decided on 2026-10-26, before its runs (IDEA.md, section "Follow-up: the information arms
# without a terminal"). Same folder as the first experiment, its own order file.
FOLLOWUP = [("openhands", "openai", arm, r) for arm in ("L-E0", "R-E0", "RP-E0") for r in range(1, REPS + 1)]
FOLLOWUP_SEED = 20261026
MAX_ATTEMPTS = 3
lock = threading.Lock()


def load_env():
    """API keys come from .env (the shell's Anthropic key is stale). Values are never printed."""
    env = dict(os.environ)
    for line in (ROOT / ".env").read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def newest_change(d):
    return max([p.stat().st_mtime for p in d.rglob("*") if p.exists()] + [d.stat().st_mtime])


def one(run, outroot, env, log):
    agent, prov, arm, rep = run
    outdir = outroot / f"{agent}_{prov}" / arm / f"rep{rep:02d}"
    # A run that an earlier runner process started and that is still going: wait for it rather
    # than start it again. A folder with no change for an hour is taken as a stopped run.
    while (outdir.exists() and not (outdir / "result.json").exists()
           and time.time() - newest_change(outdir) < 3600):
        time.sleep(30)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        res_path = outdir / "result.json"
        if res_path.exists():
            r = json.loads(res_path.read_text())
            if r.get("tokens_prompt"):  # a model call succeeded: the run counts as it is
                return r
            k = 1
            while outdir.with_name(f"{outdir.name}.attempt{k}").exists():
                k += 1
            shutil.move(str(outdir), str(outdir.with_name(f"{outdir.name}.attempt{k}")))
        t0 = time.time()
        subprocess.run([sys.executable, str(ROOT / "pilot/scripts/run_task.py"), "--manifest", MAN,
                        "--agent", agent, "--provider", prov, "--arm", arm, "--rep", str(rep),
                        "--outroot", str(outroot), "--prune"], env=env, capture_output=True, text=True)
        r = json.loads(res_path.read_text()) if res_path.exists() else {}
        with lock:
            with open(log, "a") as f:
                f.write(json.dumps({"run": f"{agent}_{prov}/{arm}/rep{rep:02d}", "attempt": attempt,
                                    "minutes": round((time.time() - t0) / 60, 1), "checks_pass": r.get("checks_pass"),
                                    "povs": {k: v.get("state") for k, v in (r.get("povs") or {}).items()},
                                    "tokens": r.get("tokens_prompt"), "cost": r.get("cost_usd"),
                                    "stop": r.get("stop_reason"), "error": r.get("error")}) + "\n")
        if r.get("tokens_prompt"):
            return r
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calibration", action="store_true")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0, help="run only the first N runs of the order")
    ap.add_argument("--rejudge", action="store_true")
    ap.add_argument("--followup", action="store_true", help="the E0 follow-up runs (FOLLOWUP)")
    a = ap.parse_args()
    outroot = ROOT / ("pilot/runs/repair_input_study_calibration" if a.calibration else "pilot/runs/repair_input_study")
    outroot.mkdir(parents=True, exist_ok=True)
    order_file = outroot / ("run_order_e0.json" if a.followup else "run_order.json")
    seed = FOLLOWUP_SEED if a.followup else SEED
    if order_file.exists():
        order = [tuple(r) for r in json.loads(order_file.read_text())["order"]]
    else:
        order = CALIBRATION if a.calibration else FOLLOWUP if a.followup else [
            (ag, pr, arm, rep) for (ag, pr), arms in PLAN.items() for arm in arms for rep in range(1, REPS + 1)]
        order = list(order)
        random.Random(seed).shuffle(order)
        order_file.write_text(json.dumps({"seed": seed, "retry_rule": __doc__.split("Retry rule")[1].split("\n\n")[0],
                                          "order": order}, indent=1))
    if a.limit:
        order = order[:a.limit]
    if a.rejudge:
        def again(run):
            agent, prov, arm, rep = run
            subprocess.run([sys.executable, str(ROOT / "pilot/scripts/run_task.py"), "--manifest", MAN, "--agent", agent,
                            "--provider", prov, "--arm", arm, "--rep", str(rep), "--outroot", str(outroot),
                            "--from-patch", "--prune"], capture_output=True, text=True)
        with ThreadPoolExecutor(a.workers) as ex:
            list(ex.map(again, [r for r in order if (outroot / f"{r[0]}_{r[1]}" / r[2] / f"rep{r[3]:02d}" / "result.json").exists()]))
        print("re-judged")
        return
    env = load_env()
    log = outroot / "progress.log"
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda r: one(r, outroot, env, log), order))
    print(f"done: {len(order)} runs; see {log}")


if __name__ == "__main__":
    main()
