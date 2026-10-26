#!/usr/bin/env python3
"""Analysis of the repair input study, first experiment and its E0 follow-up (finding 63008). The methods are fixed in
IDEA.md, section "Extension: how the input given to a repair agent changes the repair", Analysis.

Reads   pilot/runs/repair_input_study/<setup>/<arm>/rep<NN>/result.json   one per run (attempts left out)
        pilot/runs/repair_input_study/llm_judge/decisions.json           every judge and review report, confirmed or rejected
        pilot/runs/repair_input_study/posthoc.json                       checks P6 to P8, written after the runs started
        pilot/runs/repair_input_study/blind_review_summary.json          the blind review's verdict on every repair
        pilot/runs/repair_input_study_calibration/...                     reported on their own
Writes  pilot/results/repair_input_study/summary.json   every number quoted in the docs and slides
        pilot/results/repair_input_study/runs.csv       one row per run with its outcome
        pilot/results/repair_input_study/arms.csv       rates per arm with 95% Wilson intervals
        pilot/results/repair_input_study/contrasts.csv  differences, Newcombe intervals, Fisher p
        pilot/results/repair_input_study/figures/*.png

Usage (scipy and matplotlib are not in the project environment):
  uv run --with matplotlib --with scipy --with numpy python pilot/analysis/stats_study.py
"""
import csv, json, math, statistics
from pathlib import Path

from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "pilot/runs/repair_input_study"
CAL = ROOT / "pilot/runs/repair_input_study_calibration"
OUT = ROOT / "pilot/results/repair_input_study"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)
Z = 1.959963984540054
NAME = {"openhands_openai": "OpenHands + GPT-5.4-mini", "codex_openai": "Codex + GPT-5.4-mini",
        "aider_openai": "Aider + GPT-5.4-mini"}
ARMS = {"openhands_openai": ["L-E2", "R-E2", "P-E2", "RP-E2", "L-E0", "R-E0", "P-E0", "RP-E0", "P-E1"],
        "codex_openai": ["L-E2", "P-E2", "P-E0", "P-E1"], "aider_openai": ["P-E0", "P-E1"]}
# (setup, first arm, second arm, what the difference measures); differences are second minus first.
PRIMARY = [("openhands_openai", "L-E2", "P-E2", "(a) adding the PoV"),
           ("openhands_openai", "P-E0", "P-E1", "(b) running the shown PoV")]
EXPLORATORY = [("openhands_openai", "L-E2", "R-E2", "adding the report"),
               ("openhands_openai", "P-E2", "RP-E2", "adding the report to the PoV"),
               ("openhands_openai", "R-E2", "RP-E2", "adding the PoV to the report"),
               ("openhands_openai", "R-E2", "P-E2", "the PoV instead of the report"),
               ("openhands_openai", "P-E1", "P-E2", "a terminal instead of the test tool"),
               ("openhands_openai", "P-E0", "P-E2", "a terminal instead of nothing"),
               ("codex_openai", "L-E2", "P-E2", "(a) adding the PoV"),
               ("codex_openai", "P-E0", "P-E1", "(b) running the shown PoV"),
               ("codex_openai", "P-E1", "P-E2", "a terminal instead of the test tool"),
               ("aider_openai", "P-E0", "P-E1", "(b) running the shown PoV")]
# The E0 follow-up (IDEA.md, section "Follow-up: the information arms without a terminal"), run on
# 2026-10-26. (c) was fixed before its runs and is the follow-up's only test, so it is not corrected.
FOLLOWUP = [("openhands_openai", "L-E0", "P-E0", "(c) adding the PoV, nothing to run")]
FOLLOWUP_EXPLORATORY = [("openhands_openai", "L-E0", "R-E0", "adding the report, nothing to run"),
                        ("openhands_openai", "R-E0", "RP-E0", "adding the PoV to the report, nothing to run"),
                        ("openhands_openai", "P-E0", "RP-E0", "adding the report to the PoV, nothing to run"),
                        ("openhands_openai", "L-E0", "L-E2", "a terminal instead of nothing, location only"),
                        ("openhands_openai", "R-E0", "R-E2", "a terminal instead of nothing, report"),
                        ("openhands_openai", "RP-E0", "RP-E2", "a terminal instead of nothing, report and PoV")]
HELD_OUT = ("P1", "P3", "P4", "P5")  # the attacks no arm shows
OUTCOMES = ["success", "flaw confirmed by the judge", "breaks the function", "invalid attack result",
            "incomplete repair", "not repaired", "does not compile"]
# not repaired: P2, the report's own attack, still works. incomplete repair: P2 is blocked, another attack works.
LEGEND = {"success": "success", "flaw confirmed by the judge": "flaw confirmed by the judge",
          "breaks the function": "attacks blocked, function broken", "invalid attack result": "invalid attack result",
          "incomplete repair": "P2 blocked, another attack works", "not repaired": "P2 still works",
          "does not compile": "does not compile"}
COLOR = {"success": "#3A6EA5", "flaw confirmed by the judge": "#7A5C99", "breaks the function": "#D9A441",
         "invalid attack result": "#A39E92", "incomplete repair": "#E07A5F", "not repaired": "#B8472F",
         "does not compile": "#44506A"}
INK, MUTED, LINE, BG = "#14213D", "#44506A", "#DDD8CB", "#FBFAF6"
plt.rcParams.update({"font.family": "Helvetica Neue", "font.size": 11, "text.color": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": INK, "axes.edgecolor": LINE, "figure.facecolor": BG,
                     "axes.facecolor": BG, "savefig.facecolor": BG, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.bbox": "tight", "savefig.pad_inches": 0.12})


def wilson(k, n):
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    c = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / (1 + Z * Z / n)
    m = (p + Z * Z / (2 * n)) / (1 + Z * Z / n)
    return (max(0.0, m - c), min(1.0, m + c))


def newcombe(k1, n1, k2, n2):
    """Difference p2 - p1 with Newcombe's hybrid score interval (method 10, 1998), 95%, unadjusted."""
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1)
    l2, u2 = wilson(k2, n2)
    d = p2 - p1
    return d, d - math.sqrt((p2 - l2) ** 2 + (u1 - p1) ** 2), d + math.sqrt((u2 - p2) ** 2 + (p1 - l1) ** 2)


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - rank) * ps[i]))
        adj[i] = run
    return adj


def confirmed(judge, rid, final):
    """(known bug confirmed, new flaw confirmed) for a run, or None if it has no decision yet.
    final=False counts only the LLM judges' reports; final=True also counts the blind review."""
    j = judge.get(rid)
    if j is None:
        return None
    reps = [x for x in j["reports"] if x["decision"] == "confirmed" and (final or x["source"] != "blind review")]
    return any(x["kind"] == "known" for x in reps), any(x["kind"] == "new" for x in reps)


def outcome(r, judge, final=True):
    """One label per run, checked in this order. A success needs every check, and every judge and
    review report on it to be confirmed or rejected."""
    if not r.get("compiled"):
        return "does not compile"
    st = {k: v["state"] for k, v in r["povs"].items()}
    if st.get("P2") == "works":
        return "not repaired"
    if "works" in st.values():
        return "incomplete repair"
    if "invalid" in st.values():
        return "invalid attack result"
    if not r["functional"]["pass"]:
        return "breaks the function"
    c = confirmed(judge, r["id"], final)
    if c is None:
        raise SystemExit(f"no judge decision for {r['id']}: run the LLM judge and confirm its reports first")
    return "flaw confirmed by the judge" if any(c) else "success"


def held_out_success(r, judge, final=True):
    if not (r.get("compiled") and r["functional"]["pass"]):
        return False
    if any(r["povs"][p]["state"] != "blocked" for p in HELD_OUT):
        return False
    c = confirmed(judge, r["id"], final)
    return c is not None and not any(c)


def load(root):
    rows = []
    for p in sorted(root.glob("*/*/rep*/result.json")):
        if ".attempt" in p.parent.name:
            continue
        r = json.loads(p.read_text())
        r["setup"] = p.parents[2].name
        rows.append(r)
    return rows


def ops_labels(r):
    out = []
    if r.get("error"):
        out.append("harness error")
    if r.get("stop_reason") in ("timeout",) or (r.get("duration_s") or 0) >= 2400:
        out.append("timeout")
    if r.get("agent_error") or "turn.failed" in str(r.get("stop_reason")):
        out.append("API or agent error")
    if not r.get("diff_lines"):
        out.append("no edit")
    if r.get("test_files_changed"):
        out.append("edited a test file")
    return out


def main():
    jfile = RUNS / "llm_judge/decisions.json"
    judge = json.loads(jfile.read_text()) if jfile.exists() else {}
    rows = load(RUNS)
    pfile = RUNS / "posthoc.json"
    posthoc = json.loads(pfile.read_text()) if pfile.exists() else {}
    for r in rows:
        r["outcome"] = outcome(r, judge)
        r["outcome_before_review"] = outcome(r, judge, final=False)
        r["held_out_success"] = held_out_success(r, judge)
        r["success"] = r["outcome"] == "success"
        r["success_before_review"] = r["outcome_before_review"] == "success"
        r["posthoc"] = posthoc.get(f"{r['setup']}/{r['arm']}/rep{r['rep']:02d}", {})
    S = {"runs": len(rows), "arms": {}, "primary": [], "exploratory": [], "judge_decisions": len(judge)}
    arm_rows = []
    for setup, arms in ARMS.items():
        for arm in arms:
            g = [r for r in rows if r["setup"] == setup and r["arm"] == arm]
            if not g:
                continue
            n, k = len(g), sum(r["success"] for r in g)
            h = sum(r["held_out_success"] for r in g)
            p2b = [r for r in g if r.get("povs", {}).get("P2", {}).get("state") == "blocked"]
            inc = sum(r["outcome"] == "incomplete repair" for r in g)
            kb = sum(r["success_before_review"] for r in g)
            a = dict(setup=setup, arm=arm, n=n, success=k, rate=k / n, ci=wilson(k, n), success_before_review=kb,
                     checks_pass=sum(bool(r.get("checks_pass")) for r in g),
                     kept_bug_tests=sum(r.get("bug_encoding_tests_pass") == 4 for r in g),
                     posthoc_works={c: sum(r["posthoc"].get(c) == "works" for r in g) for c in ("P6", "P7")},
                     held_out_success=h, held_out_ci=wilson(h, n),
                     incomplete=inc, incomplete_of_p2_blocked=f"{inc}/{len(p2b)}",
                     shown_test_passes=sum(bool(r.get("shown_test_passes")) for r in g) if "P" in arm.split("-")[0] else None,
                     outcomes={o: sum(r["outcome"] == o for r in g) for o in OUTCOMES},
                     attack_works={p: sum(r["povs"][p]["state"] == "works" for r in g if r.get("povs")) for p in ("P1", "P2", "P3", "P4", "P5")},
                     median_tokens=statistics.median([(r.get("tokens_prompt") or 0) + (r.get("tokens_completion") or 0) for r in g]),
                     cost_usd=round(sum(r.get("cost_usd") or 0 for r in g), 2),
                     median_minutes=round(statistics.median([(r.get("duration_s") or 0) / 60 for r in g]), 1),
                     median_test_runs=statistics.median([r.get("test_runs") or 0 for r in g]),
                     ran_a_test=sum((r.get("test_runs") or 0) > 0 for r in g),
                     stop_reasons={s: sum(r.get("stop_reason") == s for r in g) for s in {r.get("stop_reason") for r in g}},
                     ops={o: sum(o in ops_labels(r) for r in g) for o in ("harness error", "timeout", "API or agent error",
                                                                          "no edit", "edited a test file")})
            S["arms"][f"{setup}/{arm}"] = a
            arm_rows.append(a)
    def contrast(setup, a1, a2, what):
        x, y = S["arms"].get(f"{setup}/{a1}"), S["arms"].get(f"{setup}/{a2}")
        if not x or not y:
            return None
        d, lo, hi = newcombe(x["success"], x["n"], y["success"], y["n"])
        p = stats.fisher_exact([[y["success"], y["n"] - y["success"]], [x["success"], x["n"] - x["success"]]])[1]
        dh, loh, hih = newcombe(x["held_out_success"], x["n"], y["held_out_success"], y["n"])
        return dict(setup=setup, first=a1, second=a2, measures=what, first_rate=f"{x['success']}/{x['n']}",
                    second_rate=f"{y['success']}/{y['n']}", difference=d, ci_low=lo, ci_high=hi, fisher_p=p,
                    held_out_difference=dh, held_out_ci_low=loh, held_out_ci_high=hih)
    prim = [c for c in (contrast(*c) for c in PRIMARY) if c]
    for c, adj in zip(prim, holm([c["fisher_p"] for c in prim])):
        c["holm_p"] = adj
    S["primary"] = prim
    bfile = RUNS / "blind_review_summary.json"
    if bfile.exists():  # the blind review: how each repair changes the walk, and whether it agrees with the checks
        blind = json.loads(bfile.read_text())
        for k, a in S["arms"].items():
            g = [v for p, v in blind.items() if p.startswith(k + "/")]
            a["blind_approach"] = {x: sum(v["approach"] == x for v in g) for x in sorted({v["approach"] for v in g})}
        seen = [(r, blind[k]) for r in rows if (k := f"{r['setup']}/{r['arm']}/rep{r['rep']:02d}") in blind]
        agree = sum(r["success"] == (b["requirement_holds"] is True and not b["new_flaw"]) for r, b in seen)
        S["blind_review_agrees_with_outcome"] = f"{agree}/{len(seen)}"
    S["exploratory"] = [c for c in (contrast(*c) for c in EXPLORATORY) if c]
    S["followup"] = [c for c in (contrast(*c) for c in FOLLOWUP) if c]
    S["followup_exploratory"] = [c for c in (contrast(*c) for c in FOLLOWUP_EXPLORATORY) if c]
    cal = load(CAL)
    S["calibration"] = [dict(id=r["id"], checks_pass=r.get("checks_pass"),
                             povs={k: v["state"] for k, v in (r.get("povs") or {}).items()},
                             functional_pass=(r.get("functional") or {}).get("pass")) for r in cal]
    S["total_cost_usd"] = round(sum(r.get("cost_usd") or 0 for r in rows), 2)
    S["total_tokens"] = sum((r.get("tokens_prompt") or 0) + (r.get("tokens_completion") or 0) for r in rows)
    (OUT / "summary.json").write_text(json.dumps(S, indent=2, default=str))
    with open(OUT / "runs.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["setup", "arm", "rep", "outcome", "outcome_before_review", "success", "held_out_success", "compiled", "functional_pass",
                    "P1", "P2", "P3", "P4", "P5", "P3_profit_wei", "shown_test_passes", "test_runs", "bug_expecting_tests_pass",
                    "P6_posthoc", "P7_posthoc", "tokens", "cost_usd",
                    "minutes", "stop_reason", "ops"])
        for r in sorted(rows, key=lambda r: (r["setup"], r["arm"], r["rep"])):
            pv = r.get("povs") or {}
            w.writerow([r["setup"], r["arm"], r["rep"], r["outcome"], r["outcome_before_review"], r["success"], r["held_out_success"], r.get("compiled"),
                        (r.get("functional") or {}).get("pass")] + [pv.get(p, {}).get("state") for p in ("P1", "P2", "P3", "P4", "P5")]
                       + [pv.get("P3", {}).get("profit_wei"), r.get("shown_test_passes"), r.get("test_runs"), r.get("bug_encoding_tests_pass"),
                          r["posthoc"].get("P6"), r["posthoc"].get("P7"),
                          (r.get("tokens_prompt") or 0) + (r.get("tokens_completion") or 0), r.get("cost_usd"),
                          round((r.get("duration_s") or 0) / 60, 1), r.get("stop_reason"), ";".join(ops_labels(r))])
    with open(OUT / "arms.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["setup", "arm", "n", "success", "rate", "ci_low", "ci_high", "success_before_review", "checks_pass",
                    "kept_bug_expecting_tests", "held_out_success", "incomplete_repair",
                    "incomplete_of_p2_blocked", "shown_test_passes", "median_test_runs", "ran_a_test", "median_tokens", "cost_usd", "median_minutes"])
        for a in arm_rows:
            w.writerow([a["setup"], a["arm"], a["n"], a["success"], round(a["rate"], 3), round(a["ci"][0], 3), round(a["ci"][1], 3),
                        a["success_before_review"], a["checks_pass"], a["kept_bug_tests"],
                        a["held_out_success"], a["incomplete"], a["incomplete_of_p2_blocked"], a["shown_test_passes"],
                        a["median_test_runs"], a["ran_a_test"], a["median_tokens"], a["cost_usd"], a["median_minutes"]])
    with open(OUT / "contrasts.csv", "w", newline="") as f:
        cols = ["setup", "first", "second", "measures", "first_rate", "second_rate", "difference", "ci_low", "ci_high",
                "fisher_p", "holm_p", "held_out_difference", "held_out_ci_low", "held_out_ci_high"]
        w = csv.writer(f)
        w.writerow(["kind"] + cols)
        for kind, cs in (("primary", S["primary"]), ("exploratory", S["exploratory"]),
                         ("follow-up", S["followup"]), ("follow-up exploratory", S["followup_exploratory"])):
            for c in cs:
                w.writerow([kind] + [round(c[k], 4) if isinstance(c.get(k), float) else c.get(k, "") for k in cols])
    figures(arm_rows)
    print(json.dumps({"runs": S["runs"], "primary": S["primary"], "followup": S["followup"],
                      "total_cost_usd": S["total_cost_usd"]}, indent=1, default=str))


def figures(arm_rows):
    """Arms grouped by agent, with the agent's name under each group."""
    xs, x, groups = [], 0, []
    for setup in ARMS:
        g = [a for a in arm_rows if a["setup"] == setup]
        groups.append((setup, x, x + len(g) - 1))
        xs += [x + i for i in range(len(g))]
        x += len(g) + 0.8
    labels = [a["arm"] for a in arm_rows]

    def frame(ax, ylabel):
        ax.set_xticks(xs)
        ax.set_xticklabels(labels, fontsize=10)
        ax.set_ylabel(ylabel)
        for setup, a, b in groups:
            ax.annotate(NAME[setup], ((a + b) / 2, 0), xycoords=("data", "axes fraction"), xytext=(0, -34),
                        textcoords="offset points", ha="center", fontsize=10.5, color=INK, fontweight="bold")
    # 1. Success rate per arm with 95% Wilson intervals.
    fig, ax = plt.subplots(figsize=(11, 4.2))
    for xi, a in zip(xs, arm_rows):
        ax.plot([xi, xi], [a["ci"][0] * 100, a["ci"][1] * 100], color="#A39E92", lw=2)
        ax.plot(xi, a["rate"] * 100, "o", color="#3A6EA5", ms=8)
        ax.annotate(f"{a['success']}/{a['n']}", (xi, a["rate"] * 100), textcoords="offset points", xytext=(9, -4), fontsize=9, color=INK)
    ax.set_ylim(-3, 103)
    ax.grid(axis="y", color=LINE, lw=0.6)
    frame(ax, "Success under the checks (%)")
    fig.savefig(FIG / "success_by_arm.png", dpi=200)
    plt.close(fig)
    # 2. Outcome of every run, per arm.
    fig, ax = plt.subplots(figsize=(11, 4.6))
    bottom = [0] * len(arm_rows)
    for o in OUTCOMES:
        vals = [a["outcomes"][o] for a in arm_rows]
        if any(vals):
            ax.bar(xs, vals, bottom=bottom, color=COLOR[o], label=LEGEND[o], width=0.72)
            bottom = [b + v for b, v in zip(bottom, vals)]
    frame(ax, "Runs (12 per arm)")
    ax.legend(fontsize=9, frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.2))
    fig.savefig(FIG / "outcomes_by_arm.png", dpi=200)
    plt.close(fig)

if __name__ == "__main__":
    main()
