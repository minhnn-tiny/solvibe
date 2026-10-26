#!/usr/bin/env python3
"""Blind LLM security review of agent code for finding 63008.

Uses prompt 4 in the review prompt file (pilot/prompts/security_review.md). Each version of
each reviewed function (the human code and every agent version that compiles) is reviewed
once by each reviewer model. The prompt never says who wrote the code. Reviewed: the control
functions B1 and B2, and V1 after the repair round (V1-repair-P2), where the human version
is the audited code with the bug.

Steps:
  build    On the host. Writes one prompt per version to
           pilot/runs/security_review/<task>/<version>/prompt.txt.
           --report <audit report as Markdown> refreshes the saved known findings
           (pilot/tasks/63008/audit_known_findings.txt); without it the saved text is used.
  call     Inside Docker on the solvibe-internal network, so only the model APIs are
           reachable. Sends every prompt to every reviewer and saves the reply.
           Skips replies that already exist.
  summary  Prints one line per reported flaw.

Repair input study (IDEA.md, section "Extension: how the input given to a repair agent changes the
repair"): study-build, study-call and study-summary do the same for the study's repairs, with the
reviewers Claude Opus 5.5 and GPT-6.1 Sol. Only the repairs that could be a success are reviewed:
they compile, pass the functional suite and block every held-out attack. Two more versions check
the reviewers: the audited code, which has the bug, and the reference repair. Every file the repair
changed is shown in its changed form. Prompts and replies go to
pilot/runs/repair_input_study/llm_judge/<setup>__<arm>__rep<NN>/.

Usage:
  python3 pilot/scripts/security_review.py build [--report <audit_report.md>]
  docker run --rm --network solvibe-internal -e HTTPS_PROXY=http://solvibe-proxy:8888 \
    -e OPENAI_API_KEY -e ANTHROPIC_API_KEY -v "$PWD":/work -w /work solvibe-tools:1 \
    python3 pilot/scripts/security_review.py call
  python3 pilot/scripts/security_review.py summary
"""
import argparse, json, os, re, subprocess, sys, tempfile, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLONE = ROOT / "pilot/repos/sorellaLabs__l2-angstrom"
SNAPSHOT = "386baff9f903aabb48eeb813d3bd629fc740f50a"
OUT = ROOT / "pilot/runs/security_review"
PROMPT_FILE = ROOT / "pilot/prompts/security_review.md"
TASKS_DIR = ROOT / "pilot/tasks/63008/feature_tasks"
# The audit report left its download URL, so its five High and Medium findings are kept here.
FINDINGS_FILE = ROOT / "pilot/tasks/63008/audit_known_findings.txt"
SETUPS = ["aider_openai", "aider_anthropic", "openhands_openai", "openhands_anthropic", "codex_openai", "codex_anthropic"]
TASKS = {
    "B1": {"file": "src/libraries/TickIterator.sol",
           "function": "src/libraries/TickIterator.sol, library TickIteratorLib, "
                       "function reset(TickIteratorUp memory self, int24 startTick) internal view",
           "callers": ["src/AngstromL2.sol", "src/libraries/CompensationPriceFinder.sol"]},
    "B2": {"file": "src/libraries/PoolKeyHelperLib.sol",
           "function": "src/libraries/PoolKeyHelperLib.sol, library PoolKeyHelperLib, "
                       "function calldataToId(PoolKey calldata poolKey) internal pure returns (PoolId id)",
           "callers": ["src/AngstromL2.sol"]},
    # V1 after the repair round. The requirement is V1's, and the human version has the bug.
    "V1-repair-P2": {"file": "src/libraries/TickIterator.sol", "requirement": "V1",
                     "function": "src/libraries/TickIterator.sol, library TickIteratorLib, "
                                 "function reset(TickIteratorDown memory self, int24 startTick) internal view",
                     "callers": ["src/AngstromL2.sol", "src/libraries/CompensationPriceFinder.sol"]},
}
REVIEWERS = {"claude-opus-5-5": "anthropic", "gpt-5.4-2026-03-05": "openai"}
STUDY = ROOT / "pilot/runs/repair_input_study"
STUDY_OUT = STUDY / "llm_judge"
STUDY_REVIEWERS = {"claude-opus-5-5": "anthropic", "gpt-6.1-sol": "openai"}  # chosen by the user, 2026-10-20
PROVIDER = {**REVIEWERS, **STUDY_REVIEWERS}
REFERENCE_REPAIR = ROOT / "pilot/tasks/63008/extension/reference_repair.patch"
HELD_OUT = ("P1", "P3", "P4", "P5")


def git_show(path):
    return subprocess.run(["git", "-C", str(CLONE), "show", f"{SNAPSHOT}:{path}"],
                          check=True, capture_output=True, text=True).stdout


def agent_version(task, setup):
    """The target file at the snapshot with the agent's patch applied. The patch is a diff against the snapshot."""
    rel = TASKS[task]["file"]
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / rel
        f.parent.mkdir(parents=True)
        f.write_text(git_show(rel))
        subprocess.run(["git", "apply", str(ROOT / f"pilot/runs/{setup}/63008-{task}/agent.patch")], cwd=d, check=True)
        return f.read_text()


def known_findings(report):
    """Title, severity, description and impact of every High and Medium finding in the report."""
    text = Path(report).read_text()
    out = []
    for sev, section in (("High", "## High Risk"), ("Medium", "## Medium Risk")):
        body = text.split(section, 1)[1].split("\n## ", 1)[0]
        for block in body.split("\n### ")[1:]:
            title, rest = block.split("\n", 1)
            desc = re.split(r"\*\*(?:Proof of Concept|Recommended Mitigation):\*\*", rest)[0].strip()
            out.append(f"<finding severity=\"{sev}\">\n<title>{title.strip()}</title>\n{desc}\n</finding>")
    return "\n".join(out)


def template():
    md = PROMPT_FILE.read_text()
    return md.split("## Prompt 4", 1)[1].split("```text\n", 1)[1].split("\n```", 1)[0]


def fill(tpl, tag, value):
    # The template holds exactly one <tag ...>{{...}}</tag> for each input.
    new, n = re.subn(rf"(<{tag}[^>]*>)\{{\{{.*?\}}\}}(</{tag}>)", lambda m: m[1] + value + m[2], tpl, flags=re.S)
    assert n == 1, tag
    return new


def build(report):
    if report:
        FINDINGS_FILE.write_text(known_findings(report))
    tpl, findings = template(), FINDINGS_FILE.read_text()
    for task, t in TASKS.items():
        callers = "\n".join(f'<source path="{p}">\n{git_show(p)}</source>' for p in t["callers"])
        versions = {"human": git_show(t["file"])}
        for s in SETUPS:
            rp = ROOT / f"pilot/runs/{s}/63008-{task}/result.json"
            if not rp.exists():  # e.g. no repair run: that setup's V1 already blocked the shown PoV
                print(f"skip {task} {s}: no run")
                continue
            res = json.loads(rp.read_text())
            if res["functional"].get("compiled") is False:
                print(f"skip {task} {s}: did not compile")
                continue
            versions[s] = agent_version(task, s)
        for name, code in versions.items():
            p = tpl.replace("{{target_file}}", t["file"])
            p = fill(p, "requirement", (TASKS_DIR / t.get("requirement", task) / "feature_request.md").read_text().strip())
            p = fill(p, "target_function", t["function"])
            p = fill(p, "file", code)
            p = fill(p, "callers", callers)
            p = fill(p, "known_findings", findings)
            d = OUT / f"63008-{task}" / name
            d.mkdir(parents=True, exist_ok=True)
            (d / "prompt.txt").write_text(p)
            print(f"built {task} {name}: {len(p)} chars")


def patched_files(patch, paths):
    """The snapshot's version of `paths` and of every file the patch touches, with the patch applied."""
    touched = re.findall(r"^\+\+\+ b/(\S+)", patch.read_text(), re.M) if patch else []
    with tempfile.TemporaryDirectory() as d:
        for rel in dict.fromkeys(list(paths) + touched):
            f = Path(d) / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(git_show(rel))
        if patch and patch.read_text().strip():
            subprocess.run(["git", "apply", str(patch)], cwd=d, check=True)
        return {rel: (Path(d) / rel).read_text() for rel in dict.fromkeys(list(paths) + touched)}


def study_needs_judge(r):
    """The judge can change the outcome only of a repair that compiles, passes the functional suite
    and blocks every held-out attack."""
    return bool(r.get("compiled") and (r.get("functional") or {}).get("pass")
                and all(r["povs"][p]["state"] == "blocked" for p in HELD_OUT))


def study_build():
    tpl, findings = template(), FINDINGS_FILE.read_text()
    t = TASKS["V1-repair-P2"]
    versions = {"audited": None, "reference": REFERENCE_REPAIR}
    for rp in sorted(STUDY.glob("*/*/rep*/result.json")):
        if ".attempt" not in rp.parent.name and study_needs_judge(json.loads(rp.read_text())):
            versions["__".join(rp.parent.relative_to(STUDY).parts)] = rp.parent / "agent.patch"
    for name, patch in versions.items():
        files = patched_files(patch, [t["file"]] + t["callers"])
        others = [p for p in files if p != t["file"]]
        p = tpl.replace("{{target_file}}", t["file"])
        p = fill(p, "requirement", (TASKS_DIR / "V1" / "feature_request.md").read_text().strip())
        p = fill(p, "target_function", t["function"])
        p = fill(p, "file", files[t["file"]])
        p = fill(p, "callers", "\n".join(f'<source path="{q}">\n{files[q]}</source>' for q in others))
        p = fill(p, "known_findings", findings)
        d = STUDY_OUT / name
        d.mkdir(parents=True, exist_ok=True)
        if (d / "prompt.txt").exists() and (d / "prompt.txt").read_text() != p:
            sys.exit(f"{d} already has a different prompt")
        (d / "prompt.txt").write_text(p)
        print(f"built {name}: {len(p)} chars")


def study_call():
    jobs = [(p, m) for p in sorted(STUDY_OUT.glob("*/prompt.txt")) for m in STUDY_REVIEWERS]
    with ThreadPoolExecutor(6) as ex:
        for f in [ex.submit(call_one, p, m, STUDY_OUT) for p, m in jobs]:
            try:
                print(f.result(), flush=True)
            except Exception as e:
                print(f"error: {e}", flush=True)


def study_summary():
    for f in sorted(STUDY_OUT.glob("*/*.json")):
        d = json.loads(f.read_text())
        flaws = (d["review"] or {}).get("flaws", [])
        if not flaws:
            print(f"{f.parent.name}\t{d['model']}\tno flaws")
        for x in flaws:
            print(f"{f.parent.name}\t{d['model']}\t{x['severity']}\t{x['known_finding']}\t{x['title']}")


def post(url, headers, body):
    req = urllib.request.Request(url, json.dumps(body).encode(), {"content-type": "application/json", **headers})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=1800) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:500]
            if e.code not in (429, 500, 502, 503, 529) or attempt == 3:
                raise RuntimeError(f"HTTP {e.code}: {msg}")
        time.sleep(30 * (attempt + 1))


def ask(model, prompt):
    """Returns (reply text, raw response)."""
    if PROVIDER[model] == "anthropic":
        raw = post("https://api.anthropic.com/v1/messages",
                   {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
                   {"model": model, "max_tokens": 32000, "thinking": {"type": "adaptive"},
                    "messages": [{"role": "user", "content": prompt}]})
        text = "".join(b["text"] for b in raw["content"] if b["type"] == "text")
    else:
        raw = post("https://api.openai.com/v1/responses",
                   {"authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
                   {"model": model, "input": prompt, "reasoning": {"effort": "high"}})
        text = "".join(c["text"] for o in raw["output"] if o["type"] == "message"
                       for c in o["content"] if c["type"] == "output_text")
    return text, raw


def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m[0]) if m else None


def call_one(prompt_path, model, base=OUT):
    out = prompt_path.parent / f"{model}.json"
    if out.exists():
        return f"exists {out.relative_to(base)}"
    t0 = time.time()
    text, raw = ask(model, prompt_path.read_text())
    try:
        review = parse(text)
    except json.JSONDecodeError:
        review = None
    out.write_text(json.dumps({"model": model, "seconds": round(time.time() - t0), "review": review,
                               "text": text, "usage": raw.get("usage"), "raw": raw}, indent=1))
    n = len(review["flaws"]) if review else "unparsed"
    return f"done {out.relative_to(base)}: {n} flaws, {round(time.time() - t0)} s"


def call():
    jobs = [(p, m) for p in sorted(OUT.glob("63008-*/*/prompt.txt")) for m in REVIEWERS]
    with ThreadPoolExecutor(6) as ex:
        for f in [ex.submit(call_one, p, m) for p, m in jobs]:
            try:
                print(f.result(), flush=True)
            except Exception as e:
                print(f"error: {e}", flush=True)


def summary():
    for f in sorted(OUT.glob("63008-*/*/*.json")):
        d = json.loads(f.read_text())
        task, version = f.parts[-3], f.parts[-2]
        flaws = (d["review"] or {}).get("flaws", [])
        if not flaws:
            print(f"{task}\t{version}\t{d['model']}\tno flaws")
        for x in flaws:
            print(f"{task}\t{version}\t{d['model']}\t{x['severity']}\t{x['known_finding']}\t{x['title']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["build", "call", "summary", "study-build", "study-call", "study-summary"])
    ap.add_argument("--report")
    a = ap.parse_args()
    if a.step.startswith("study-"):
        {"study-build": study_build, "study-call": study_call, "study-summary": study_summary}[a.step]()
    elif a.step == "build":
        if not a.report and not FINDINGS_FILE.exists():
            sys.exit("build needs --report the first time")
        build(a.report)
    elif a.step == "call":
        call()
    else:
        summary()
