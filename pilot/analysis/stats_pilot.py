#!/usr/bin/env python3
"""Statistical analysis of the pilot (treatment group only; the control group has not been run).

Reads   pilot/results/pilot_runs.csv          one row per agent run (automatic outcome, tokens, time)
        pilot/results/manual_code_review.csv  one row per run (does the code contain the bug; what the request describes)
Writes  pilot/results/stats/summary.json      every number quoted in the docs and slides
        pilot/results/stats/rates.csv         proportions with exact 95% confidence intervals
        pilot/results/figures/*.png           charts used in the slides

Usage (scipy and matplotlib are not in the project environment):
  uv run --with matplotlib --with scipy --with numpy python pilot/analysis/stats_pilot.py
"""
import csv, itertools, json, math
from pathlib import Path

import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "pilot/results"
OUT, FIG = RES / "stats", RES / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

# deck colours; BLUE and RUST pass the dataviz palette validator on the slide background
INK, MUTED, LINE, BG = "#14213D", "#44506A", "#DDD8CB", "#FBFAF6"
BLUE, RUST, GRAY = "#3A6EA5", "#B8472F", "#A39E92"
plt.rcParams.update({"font.family": "Helvetica Neue", "font.size": 11, "text.color": INK, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": INK, "axes.edgecolor": LINE, "figure.facecolor": BG,
                     "axes.facecolor": BG, "savefig.facecolor": BG, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.bbox": "tight", "savefig.pad_inches": 0.12})
NAME = {"aider_openai": "Aider + GPT-5.4-mini", "aider_anthropic": "Aider + Sonnet 4.5",
        "openhands_openai": "OpenHands + GPT-5.4-mini", "openhands_anthropic": "OpenHands + Sonnet 4.5"}
SHORT = {"62347": "seize", "62348": "removeFungible", "62349": "_afterSwap", "62350": "decreaseDebtShare",
         "63008": "tick reset", "63185": "ownership handover", "63760": "recover", "64637": "cancel"}


def load():
    rev = {(r["id"], r["configuration"]): r for r in csv.DictReader(open(RES / "manual_code_review.csv"))}
    rows = []
    for r in csv.DictReader(open(RES / "pilot_runs.csv")):
        cfg = f"{r['agent']}_{r['provider']}"
        v = rev[(r["id"], cfg)]
        rows.append(dict(task=r["id"], cfg=cfg, agent=r["agent"], model=r["provider"],
                         compiled=r["build_ok"] == "True", auto=r["outcome"] == "reproduced",
                         bug={"yes": True, "no": False}.get(v["code_contains_bug"]),
                         request=v["request_describes"],
                         tokens=int(r["tokens_prompt"] or 0) + int(r["tokens_completion"] or 0),
                         seconds=float(r["duration_s"] or 0)))
    assert len(rows) == 32, len(rows)
    return rows


def ci(k, n):
    lo, hi = stats.binomtest(k, n).proportion_ci(confidence_level=0.95, method="exact")
    return lo, hi


def rate(rows, label, measure="bug"):
    if measure == "bug":
        sel = [r for r in rows if r["bug"] is not None]
        k = sum(r["bug"] for r in sel)
    elif measure == "auto":
        sel, k = rows, sum(r["auto"] for r in rows)
    else:
        sel, k = rows, sum(r["compiled"] for r in rows)
    n = len(sel)
    lo, hi = ci(k, n)
    return dict(group=label, measure=measure, k=k, n=n, p=k / n, lo=lo, hi=hi)


def mcnemar(pairs):
    """Exact McNemar test on (x, y) boolean pairs: two-sided binomial test on the discordant pairs."""
    b = sum(1 for x, y in pairs if x and not y)
    c = sum(1 for x, y in pairs if y and not x)
    p = stats.binomtest(min(b, c), b + c, 0.5).pvalue if b + c else 1.0
    return dict(pairs=len(pairs), first_only=b, second_only=c, p=p)


def icc_anova(groups):
    """One-way ANOVA intraclass correlation for a binary outcome in unequal-sized groups."""
    ys = [np.array(g, float) for g in groups if len(g)]
    N, k = sum(len(g) for g in ys), len(ys)
    grand = np.concatenate(ys).mean()
    msb = sum(len(g) * (g.mean() - grand) ** 2 for g in ys) / (k - 1)
    msw = sum(((g - g.mean()) ** 2).sum() for g in ys) / (N - k)
    n0 = (N - sum(len(g) ** 2 for g in ys) / N) / (k - 1)
    return float((msb - msw) / (msb + (n0 - 1) * msw))


def n_two_props(p1, p0, alpha=0.05, power=0.8):
    """Runs per group to tell p1 from p0 (two-sided, normal approximation)."""
    za, zb = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
    pb = (p1 + p0) / 2
    return (za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p0 * (1 - p0))) ** 2 / (p1 - p0) ** 2


def main():
    rows = load()
    tasks = sorted({r["task"] for r in rows})
    S = {}

    # ---- 1. proportions with exact 95% confidence intervals ----
    rates = [rate(rows, "All runs: automatic judge says reproduced", "auto"),
             rate(rows, "All runs: code compiled", "compiled"),
             rate(rows, "All compiled runs"),
             rate([r for r in rows if r["agent"] == "aider"], "Aider"),
             rate([r for r in rows if r["agent"] == "openhands"], "OpenHands"),
             rate([r for r in rows if r["model"] == "openai"], "GPT-5.4-mini"),
             rate([r for r in rows if r["model"] == "anthropic"], "Sonnet 4.5"),
             rate([r for r in rows if r["request"] == "human's vulnerable design"], "Request describes human's design"),
             rate([r for r in rows if r["request"] == "fixed behaviour"], "Request states fixed rule"),
             rate([r for r in rows if r["agent"] == "aider"], "Aider: code compiled", "compiled"),
             rate([r for r in rows if r["agent"] == "openhands"], "OpenHands: code compiled", "compiled")]
    rates += [rate([r for r in rows if r["cfg"] == c], NAME[c]) for c in NAME]
    with open(OUT / "rates.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rates[0]))
        w.writeheader()
        w.writerows({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for r in rates)
    S["rates"] = rates

    # ---- 2. task-clustered bootstrap for the overall rate (runs in one task are not independent) ----
    rng = np.random.default_rng(20261008)
    per = {t: [r["bug"] for r in rows if r["task"] == t and r["bug"] is not None] for t in tasks}
    boots = []
    for _ in range(20000):
        pick = rng.choice(tasks, size=len(tasks), replace=True)
        k = sum(sum(per[t]) for t in pick)
        n = sum(len(per[t]) for t in pick)
        boots.append(k / n)
    S["cluster_bootstrap_overall"] = dict(p=16 / 28, lo=float(np.percentile(boots, 2.5)),
                                          hi=float(np.percentile(boots, 97.5)), resamples=20000)

    # ---- 3. request wording: run-level Fisher test and task-level exact permutation test ----
    hd = [r for r in rows if r["request"] == "human's vulnerable design" and r["bug"] is not None]
    fx = [r for r in rows if r["request"] == "fixed behaviour" and r["bug"] is not None]
    table = [[sum(r["bug"] for r in hd), sum(not r["bug"] for r in hd)],
             [sum(r["bug"] for r in fx), sum(not r["bug"] for r in fx)]]
    _, p_fisher = stats.fisher_exact(table)
    task_rate = {t: (sum(per[t]) / len(per[t])) for t in tasks if per[t]}
    hd_tasks = sorted({r["task"] for r in hd})
    obs = np.mean([task_rate[t] for t in hd_tasks]) - np.mean([task_rate[t] for t in tasks if t not in hd_tasks])
    diffs = []
    for g in itertools.combinations(tasks, 4):
        diffs.append(np.mean([task_rate[t] for t in g]) - np.mean([task_rate[t] for t in tasks if t not in g]))
    p_perm = sum(1 for d in diffs if abs(d) >= abs(obs) - 1e-12) / len(diffs)
    S["request"] = dict(table=table, fisher_p=p_fisher, task_rate=task_rate, task_level_difference=obs,
                        permutation_p=p_perm, permutations=len(diffs))

    # ---- 4. agent versus model: exact McNemar tests on paired runs ----
    by = {(r["task"], r["cfg"]): r for r in rows}
    def pairs(key, a_cfg, b_cfg, need_both_compiled=False):
        out = []
        for t in tasks:
            for a, b in zip(a_cfg, b_cfg):
                x, y = by[(t, a)], by[(t, b)]
                if need_both_compiled and (x["bug"] is None or y["bug"] is None):
                    continue
                out.append((x[key], y[key]))
        return out
    A, O = ["aider_openai", "aider_anthropic"], ["openhands_openai", "openhands_anthropic"]
    G, C = ["aider_openai", "openhands_openai"], ["aider_anthropic", "openhands_anthropic"]
    S["paired"] = {
        "agent_compiled (Aider vs OpenHands)": mcnemar(pairs("compiled", A, O)),
        "agent_auto_reproduced (Aider vs OpenHands)": mcnemar(pairs("auto", A, O)),
        "agent_code_has_bug (Aider vs OpenHands, both compiled)": mcnemar(pairs("bug", A, O, True)),
        "model_compiled (GPT vs Sonnet)": mcnemar(pairs("compiled", G, C)),
        "model_auto_reproduced (GPT vs Sonnet)": mcnemar(pairs("auto", G, C)),
        "model_code_has_bug (GPT vs Sonnet, both compiled)": mcnemar(pairs("bug", G, C, True))}

    # ---- 5. automatic judge versus code review (compiled runs) ----
    comp = [r for r in rows if r["bug"] is not None]
    tp = sum(r["auto"] and r["bug"] for r in comp)
    fn = sum((not r["auto"]) and r["bug"] for r in comp)
    fp = sum(r["auto"] and not r["bug"] for r in comp)
    tn = sum((not r["auto"]) and not r["bug"] for r in comp)
    n = len(comp)
    po = (tp + tn) / n
    pe = ((tp + fp) * (tp + fn) + (fn + tn) * (fp + tn)) / n ** 2
    sens_lo, sens_hi = ci(tp, tp + fn)
    spec_lo, spec_hi = ci(tn, tn + fp)
    S["judge"] = dict(tp=tp, fn=fn, fp=fp, tn=tn, n=n, agreement=po, kappa=(po - pe) / (1 - pe),
                      sensitivity=tp / (tp + fn), sensitivity_ci=[sens_lo, sens_hi],
                      specificity=tn / (tn + fp), specificity_ci=[spec_lo, spec_hi])

    # ---- 6. effort: tokens and time by agent ----
    tok = {a: [r["tokens"] for r in rows if r["agent"] == a] for a in ("aider", "openhands")}
    sec = {a: [r["seconds"] for r in rows if r["agent"] == a] for a in ("aider", "openhands")}
    S["effort"] = dict(
        median_tokens={a: float(np.median(v)) for a, v in tok.items()},
        median_seconds={a: float(np.median(v)) for a, v in sec.items()},
        tokens_ratio_of_medians=float(np.median(tok["openhands"]) / np.median(tok["aider"])),
        tokens_mannwhitney_p=float(stats.mannwhitneyu(tok["aider"], tok["openhands"], method="exact").pvalue),
        seconds_mannwhitney_p=float(stats.mannwhitneyu(sec["aider"], sec["openhands"], method="exact").pvalue))

    # ---- 7. clustering and planning the control group ----
    icc = icc_anova([per[t] for t in tasks])
    m = 4
    deff = 1 + (m - 1) * icc
    p1 = 16 / 28
    grid = np.round(np.arange(0.0, 0.41, 0.01), 2)
    plan = [dict(p0=float(p0), runs_per_group=n_two_props(p1, p0),
                 tasks_one_run=n_two_props(p1, p0), tasks_four_runs=n_two_props(p1, p0) * deff / m)
            for p0 in grid if p0 < p1]
    S["planning"] = dict(icc_tasks=icc, runs_per_task=m, design_effect=deff,
                         effective_n_compiled_runs=28 / deff, treatment_rate_assumed=p1, alpha=0.05, power=0.8,
                         examples={str(p0): next(round(x["tasks_four_runs"], 1) for x in plan if x["p0"] == p0)
                                   for p0 in (0.1, 0.2, 0.3)},
                         findings_with_history=43)
    S["planning_grid"] = plan
    (OUT / "summary.json").write_text(json.dumps(S, indent=2, default=float))
    figures(rows, S, per, tasks, tok)
    print(json.dumps({k: S[k] for k in ("cluster_bootstrap_overall", "request", "judge", "effort")}, indent=1,
                     default=float)[:2500])
    print("ICC", round(icc, 3), "design effect", round(deff, 2), "examples", S["planning"]["examples"])


def figures(rows, S, per, tasks, tok):
    # ---- fig 1: forest plot of the bug rate among compiled runs ----
    want = ["All compiled runs", "Aider", "OpenHands", "GPT-5.4-mini", "Sonnet 4.5",
            "Request describes human's design", "Request states fixed rule"]
    rs = {r["group"]: r for r in S["rates"]}
    fig, ax = plt.subplots(figsize=(6.6, 4.1), dpi=220)
    ys = list(range(len(want)))[::-1]
    for y, g in zip(ys, want):
        r = rs[g]
        col = RUST if g.startswith("Request") else BLUE
        ax.plot([r["lo"] * 100, r["hi"] * 100], [y, y], color=col, lw=2, solid_capstyle="round")
        ax.plot(r["p"] * 100, y, "o", color=col, ms=8, mec=BG, mew=2)
        ax.text(103, y, f"{r['k']}/{r['n']}", va="center", fontsize=10.5, color=MUTED)
    ax.axvline(rs["All compiled runs"]["p"] * 100, color=LINE, lw=1, ls="--", zorder=0)
    ax.set_yticks(ys, want)
    for lab in ax.get_yticklabels():
        if lab.get_text() == "All compiled runs":
            lab.set_fontweight("bold")
    ax.set_xlim(0, 112)
    ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    ax.set_xlabel("Compiled runs whose code has the bug, with exact 95% CI")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "fig1_bug_rate_forest.png")
    plt.close(fig)

    # ---- fig 2: per-task outcomes grouped by what the request describes ----
    order = ["62347", "62349", "62350", "63760", "62348", "63008", "63185", "64637"]
    fig, ax = plt.subplots(figsize=(6.2, 4.3), dpi=220)
    ys = [8.6, 7.6, 6.6, 5.6, 3.6, 2.6, 1.6, 0.6]
    for y, t in zip(ys, order):
        rr = [r for r in rows if r["task"] == t]
        b = sum(1 for r in rr if r["bug"] is True)
        nb = sum(1 for r in rr if r["bug"] is False)
        nc = sum(1 for r in rr if r["bug"] is None)
        x = 0
        for cnt, col, hatch in ((b, RUST, None), (nb, BLUE, None), (nc, GRAY, "///")):
            if cnt:
                ax.barh(y, cnt - 0.06, left=x + 0.03, height=0.62, color=col, hatch=hatch, edgecolor=BG, lw=0)
            x += cnt
        ax.text(-0.15, y, f"{t}  {SHORT[t]}", ha="right", va="center", fontsize=10)
    ax.text(-0.15, 9.45, "Request describes the human's design", ha="right", fontsize=10.5, fontweight="bold",
            color=RUST)
    ax.text(-0.15, 4.45, "Request states the fixed rule", ha="right", fontsize=10.5, fontweight="bold", color=BLUE)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 9.9)
    ax.set_yticks([])
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xlabel("Agent runs (4 per task)")
    ax.spines["left"].set_visible(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=RUST, label="Code has the bug"), Patch(color=BLUE, label="Code is free of it"),
                       Patch(facecolor=GRAY, hatch="///", edgecolor=BG, label="Did not compile")],
              loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=3, frameon=False, fontsize=9.5)
    fig.subplots_adjust(left=0.42, right=0.97, top=0.97, bottom=0.24)
    fig.savefig(FIG / "fig2_request_by_task.png")
    plt.close(fig)

    # ---- fig 3: automatic judge versus code review ----
    j = S["judge"]
    M = np.array([[j["tp"], j["fn"]], [j["fp"], j["tn"]]])
    fig, ax = plt.subplots(figsize=(4.6, 4.0), dpi=220)
    for i in range(2):
        for k in range(2):
            v = int(M[i, k])
            agree = i == k
            col = BLUE if agree else ("#F2D2C9" if v else "#F1EEE6")
            ax.add_patch(plt.Rectangle((k, 1 - i), 0.96, 0.96, color=col))
            ax.text(k + 0.48, 1 - i + 0.55, str(v), ha="center", va="center", fontsize=26, fontweight="bold",
                    color=BG if agree else (RUST if v else INK))
            lab = [["both say bug", "judge missed it"], ["judge false alarm", "both say no bug"]][i][k]
            ax.text(k + 0.48, 1 - i + 0.25, lab, ha="center", va="center", fontsize=9.5,
                    color=BG if agree else MUTED)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xticks([0.48, 1.48], ["Judge: reproduced", "Judge: avoided"])
    ax.set_yticks([1.48, 0.48], ["Code review:\nbug present", "Code review:\nno bug"])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.xaxis.set_ticks_position("top")
    fig.tight_layout()
    fig.savefig(FIG / "fig3_judge_vs_review.png")
    plt.close(fig)

    # ---- fig 4: tokens per run by configuration (log scale) ----
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=220)
    cfgs = list(NAME)
    for i, c in enumerate(cfgs[::-1]):
        vals = [r["tokens"] for r in rows if r["cfg"] == c]
        col = BLUE if c.startswith("aider") else RUST
        jitter = (np.arange(len(vals)) - (len(vals) - 1) / 2) * 0.045
        ax.scatter(vals, i + jitter, s=34, color=col, edgecolor=BG, lw=1, zorder=3)
        med = float(np.median(vals))
        ax.plot([med, med], [i - 0.3, i + 0.3], color=INK, lw=2, zorder=4)
    ax.set_xscale("log")
    ax.set_yticks(range(4), [NAME[c] for c in cfgs[::-1]])
    ax.set_xlabel("Tokens per run (log scale); black bar = median")
    ax.set_xlim(1e3, 1e7)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", color=LINE, lw=0.6, zorder=0)
    fig.tight_layout()
    fig.savefig(FIG / "fig4_tokens_per_run.png")
    plt.close(fig)

    # ---- fig 5: how many tasks the treatment-versus-control comparison needs ----
    P = S["planning_grid"]
    x = [p["p0"] * 100 for p in P]
    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=220)
    one = [p["tasks_one_run"] for p in P]
    four = [p["tasks_four_runs"] for p in P]
    ax.plot(x, one, color=BLUE, lw=2.2)
    ax.plot(x, four, color=RUST, lw=2.2)
    ax.axhline(43, color=GRAY, lw=1.2, ls="--")
    ax.text(1, 46, "43 findings with history today", color=MUTED, fontsize=9.5)
    ax.text(x[-1] + 0.6, one[-1], "1 run per task", color=BLUE, fontsize=10, va="center")
    ax.text(x[-1] + 0.6, four[-1], "4 runs per task\n(pilot clustering)", color=RUST, fontsize=10, va="center")
    ax.set_xlim(0, 52)
    ax.set_ylim(0, 160)
    ax.set_xticks([0, 10, 20, 30, 40], ["0%", "10%", "20%", "30%", "40%"])
    ax.set_xlabel("Assumed bug rate in the control group (treatment: 57%, from the pilot)")
    ax.set_ylabel("Tasks needed in each group")
    ax.grid(axis="y", color=LINE, lw=0.6)
    fig.tight_layout()
    fig.savefig(FIG / "fig5_control_group_size.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
