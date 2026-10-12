#!/usr/bin/env python3
"""Build the two pilot tracking files from whatever artifacts exist on disk.

Re-run at any time; it only reads, then overwrites the two CSVs. Safe while a batch runs.

  pilot/results/findings_77_pipeline.csv
      One row per filtered finding (all 77). How far each one has got through the
      pipeline (history search -> PoV -> agent task -> agent runs), what blocks it,
      and the next action.

  pilot/results/pilot_tasks_master.csv
      One row per processed finding (one that has a PoV). The extracted benchmark
      data (VIC, PVIC, fix, bug kind, target function, PoV) plus a roll-up of the
      agent runs for each of the four configurations.

Usage: python3 pilot/scripts/build_masters.py
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TASKS = ROOT / "pilot/tasks"
RUNS = ROOT / "pilot/runs"
OUT = ROOT / "pilot/results"
CONFIGS = ["aider_openai", "aider_anthropic", "openhands_openai", "openhands_anthropic"]


def load_json(p):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


NOT_DONE_NOTE = ("Not estimated. The loss work for this finding was stopped partway by a safety check in the "
                 "AI tooling and was not restarted.")


def loss_of(fid):
    """The finding's loss estimate (pipeline step 10), if one has been made."""
    return load_json(TASKS / fid / "loss_estimate.json")


def runs_for(fid):
    """{config: result dict} for the configurations that have a judged result."""
    out = {}
    for c in CONFIGS:
        r = load_json(RUNS / c / fid / "result.json")
        if r and ("vuln_reproduced" in r or "error" in r):
            out[c] = r
    return out


def func_str(r):
    f = (r or {}).get("functional") or {}
    if "skipped" in f:
        return "skip"
    if f.get("passed") is None:
        return ""
    return "%s/%s" % (f.get("passed", 0), (f.get("passed") or 0) + (f.get("failed") or 0))


def func_ok(r):
    f = (r or {}).get("functional") or {}
    return bool(f.get("compiled") and f.get("failed") == 0 and (f.get("passed") or 0) > 0)


def outcome(r):
    """Plain-English verdict for one agent run."""
    if r.get("error"):
        return "error"
    if not r.get("build_ok"):
        return "did not compile"
    if r.get("vuln_reproduced"):
        return "reproduced"
    if "skipped" in ((r.get("functional") or {})):
        return "avoided, not verified"
    return "avoided, verified" if func_ok(r) else "avoided, broken function"


def clean_parent(pov):
    if pov.get("parent_status"):  # set by hand per task; the text fallback below misreads some notes
        return pov["parent_status"]
    for run in pov.get("runs", []):
        role = (run.get("role") or "").lower()
        if "parent" in role or "pvic" in role:
            obs = (run.get("observed") or "").lower()
            if "compile" in obs and "fail" in obs:
                return "yes (feature absent at parent)"
            if obs.startswith("pass"):
                return "no (parent also vulnerable)"
    text = " ".join(str(pov.get(k, "")) for k in ("vulnerability_note", "parent_not_run", "parent_check")).lower()
    if pov.get("vulnerability_kind") in ("missing_code", "missing_check") or "vulnerable" in text or "predates" in text:
        return "no (parent also vulnerable)"
    return "unknown"


def stage_and_next(hist, pov, man, runs):
    method = (hist or {}).get("method", "")
    if man and len(runs) == len(CONFIGS):
        return "runs_complete", "analyse results"
    if man and runs:
        return "runs_in_progress", "finish remaining configurations"
    if man:
        return "task_built", "run the four configurations"
    if pov and pov.get("oracle_valid"):
        return "pov_built", "write feature request and blank the target function"
    if pov:
        return "pov_failed", "review notes.md; PoV did not pass on vulnerable and fail on fix"
    if method == "not searched":
        return "library_file", "blocked: bug is in protocol code not in the dataset"
    if method.startswith("history"):
        return "history_found", "build PoV (report PoC + find merged fix commit)"
    if method == "fallback":
        return "no_history", "needs a fix commit or inline fix code to validate a PoV"
    return "not_started", ""


def main():
    meta = {r["id"]: r for r in csv.DictReader(open(ROOT / "data_collection/tier1_master.csv"))
            if r["status"] == "selected"}
    hist = {r["id"]: r for r in csv.DictReader(open(OUT / "history_search.csv"))}
    rp = OUT / "manual_code_review.csv"
    review = {(r["id"], r["configuration"]): r for r in csv.DictReader(open(rp))} if rp.exists() else {}
    ids = sorted(meta)

    # ---------- findings_77_pipeline.csv ----------
    rows77 = []
    for fid in ids:
        m, h = meta[fid], hist.get(fid, {})
        pov = load_json(TASKS / fid / "pov_result.json")
        man = load_json(TASKS / fid / "task/manifest.json")
        runs = runs_for(fid)
        stage, nxt = stage_and_next(h, pov, man, runs)
        rows77.append(dict(
            id=fid, protocol=m["protocol"], firm=m["firm"], impact=m["impact"],
            title=m["title"][:90], linked_month=m["linked_month"], report_has_poc=m["has_poc"],
            history_method=h.get("method", ""), history_repo=h.get("history_repo", ""),
            vic=h.get("vic", ""), history_note=h.get("reason", ""),
            pov_built="yes" if pov else "no",
            pov_oracle_valid=("yes" if pov and pov.get("oracle_valid") else ("no" if pov else "")),
            bug_kind=(pov or {}).get("vulnerability_kind", ""),
            task_built="yes" if man else "no",
            target_function=(", ".join(man["target_function"]) if man and isinstance(man.get("target_function"), list)
                             else (man or {}).get("target_function", "")),
            functional_gate=("" if not man else ("yes" if man.get("functional_cmd") else "no (PoV only)")),
            runs_done="%d/%d" % (len(runs), len(CONFIGS)) if man else "",
            configs_reproduced=(str(sum(1 for r in runs.values() if r.get("vuln_reproduced"))) if runs else ""),
            in_first_batch="yes" if man else "no",
            loss_estimated="yes" if loss_of(fid) else ("not done" if man else "no"),
            loss_type=(loss_of(fid) or {}).get("loss_type", ""),
            pipeline_stage=stage, next_action=nxt))
    p77 = OUT / "findings_77_pipeline.csv"
    with open(p77, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows77[0]))
        w.writeheader()
        w.writerows(rows77)

    # ---------- pilot_tasks_master.csv (+ loss_estimates.csv) ----------
    rows, lossrows = [], []
    for fid in ids:
        pov = load_json(TASKS / fid / "pov_result.json")
        if not pov:
            continue
        man = load_json(TASKS / fid / "task/manifest.json") or {}
        c = pov.get("commits", {})
        runs = runs_for(fid)
        row = dict(
            id=fid, protocol=pov.get("protocol", ""), firm=pov.get("firm", ""),
            finding=pov.get("finding", "")[:110],
            bug_kind=pov.get("vulnerability_kind", ""), parent_commit_status=clean_parent(pov),
            vic=(c.get("vic_blame") or "")[:10], pvic=(c.get("pvic") or "")[:10],
            vulnerable_snapshot=(c.get("audited_snapshot") or "")[:10], fix=(c.get("fix") or "")[:10],
            fix_reported_as=(c.get("fix_reported_as") or "")[:10],
            pov_test=pov.get("pov_test", ""), pov_oracle_valid="yes" if pov.get("oracle_valid") else "no",
            framing=man.get("framing", ""), target_file=man.get("target_file", ""),
            target_function=(", ".join(man["target_function"]) if isinstance(man.get("target_function"), list)
                             else man.get("target_function", "")),
            functional_gate="yes" if man.get("functional_cmd") else ("no (PoV only)" if man else ""),
            solc=man.get("solc", pov.get("solc", "")))
        tok_total, cost_total, n_repro, n_func = 0, 0.0, 0, 0
        for cfg in CONFIGS:
            r = runs.get(cfg)
            if r is None:
                row[cfg + "_reproduced"] = ""
                row[cfg + "_outcome"] = ""
                row[cfg + "_functional"] = ""
                row[cfg + "_tokens"] = ""
                continue
            rep = r.get("vuln_reproduced")
            row[cfg + "_reproduced"] = "error" if r.get("error") else ("yes" if rep else "no")
            row[cfg + "_outcome"] = outcome(r)
            row[cfg + "_functional"] = func_str(r)
            t = (r.get("tokens_prompt") or 0) + (r.get("tokens_completion") or 0)
            row[cfg + "_tokens"] = t
            tok_total += t
            cost_total += r.get("cost_usd") or 0.0
            n_repro += 1 if rep else 0
            n_func += 1 if func_ok(r) else 0
        row.update(configs_run=len(runs), configs_reproduced=n_repro, configs_functional_ok=n_func,
                   configs_code_has_bug=(sum(1 for (i, _), v in review.items() if i == fid
                                             and v["code_contains_bug"] == "yes") if review else ""),
                   total_tokens=tok_total, total_cost_usd_known=round(cost_total, 4))
        ls = loss_of(fid) or {}
        meas = ls.get("measured") or {}
        row.update(loss_type=ls.get("loss_type", "not done"), loss_what_is_at_risk=ls.get("what_is_at_risk", ""),
                   loss_measured_pct_of_user_funds=meas.get("loss_pct_of_user_funds", ""),
                   loss_worst_case_pct_of_user_funds=ls.get("worst_case_pct_of_user_funds", ""),
                   loss_confidence=ls.get("confidence", ""), caveat=man.get("notes", "")[:160])
        rows.append(row)
        if man:  # every task in the pilot gets a row; "not done" where no estimate exists
            lossrows.append(dict(
                id=fid, protocol=ls.get("protocol", pov.get("protocol", "")),
                status="measured" if ls else "not done",
                loss_type=ls.get("loss_type", "") if ls else "",
                what_is_at_risk=ls.get("what_is_at_risk", ""), who_loses=ls.get("who_loses", ""),
                who_gains=ls.get("who_gains", ""), scenario=ls.get("scenario", ""), unit=meas.get("unit", ""),
                user_funds_in_scenario=meas.get("user_funds_in_scenario"), user_loss=meas.get("user_loss"),
                attacker_gain=meas.get("attacker_gain"), loss_pct_of_user_funds=meas.get("loss_pct_of_user_funds"),
                worst_case_pct_of_user_funds=ls.get("worst_case_pct_of_user_funds", ""),
                worst_case_basis=ls.get("worst_case_basis", ""), scales_with=ls.get("scales_with", ""),
                repeatable=ls.get("repeatable", ""), concrete_usd=ls.get("concrete_usd"),
                fix_check=(ls.get("fix_check") or {}).get("result", ""), confidence=ls.get("confidence", ""),
                loss_test=ls.get("loss_test", ""), agent_runs_with_bug=row["configs_code_has_bug"],
                note=ls.get("notes", "")[:300] if ls else NOT_DONE_NOTE))
    pt = OUT / "pilot_tasks_master.csv"
    if rows:
        with open(pt, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    if lossrows:  # pipeline step 10: estimated loss if the PoV is applied
        with open(OUT / "loss_estimates.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(lossrows[0]))
            w.writeheader()
            w.writerows(lossrows)

    # ---------- pilot_runs.csv (one row per judged run, rebuilt from every result.json) ----------
    runrows = []
    for fid in ids:
        for cfg, r in runs_for(fid).items():
            pov, fun = r.get("pov") or {}, r.get("functional") or {}
            runrows.append(dict(
                id=fid, agent=r.get("agent"), provider=r.get("provider"), model=r.get("model"),
                outcome=outcome(r), build_ok=r.get("build_ok"), vuln_reproduced=r.get("vuln_reproduced"),
                pov_passed=pov.get("passed"), pov_failed=pov.get("failed"),
                functional=func_str(r), tokens_prompt=r.get("tokens_prompt"),
                tokens_completion=r.get("tokens_completion"), cost_usd=r.get("cost_usd"),
                duration_s=r.get("duration_s"), diff_lines=r.get("diff_lines"),
                rejudged_from_patch="yes" if r.get("rejudged_from_patch") else "", error=r.get("error")))
    pr = OUT / "pilot_runs.csv"
    if runrows:
        with open(pr, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(runrows[0]))
            w.writeheader()
            w.writerows(runrows)

    # ---------- console summary ----------
    from collections import Counter
    print("wrote", p77.relative_to(ROOT), "(%d findings)" % len(rows77))
    print("wrote", pt.relative_to(ROOT), "(%d processed findings)" % len(rows))
    print("pipeline stages:", dict(Counter(r["pipeline_stage"] for r in rows77)))


if __name__ == "__main__":
    main()
