#!/usr/bin/env python3
"""Check that an agent workspace cannot reveal the human's code through git.

Builds a workspace for one task exactly as run_task.py does (no Docker, no agent), then
asserts: the workspace repo has a single commit, `git show HEAD~1` fails, the human's
function body is absent from the workspace, and the agent diff (taken through the hidden
.git) still re-applies cleanly on the vulnerable commit, which `--from-patch` relies on.

Usage: python3 pilot/scripts/test_workspace_isolation.py [task_id]   (default 63760)
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_task as rt  # noqa: E402


def git(*args, cwd=None):
    r = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    tid = sys.argv[1] if len(sys.argv) > 1 else "63760"
    man = json.loads((rt.ROOT / f"pilot/tasks/{tid}/task/manifest.json").read_text())
    proj_rel = man.get("project_dir", "") or ""
    target = (f"{proj_rel}/" if proj_rel else "") + man["agent_edit_files"][0]
    tmp = Path(tempfile.mkdtemp(prefix="iso_"))
    try:
        run_dir = tmp / "workspace"
        rt.setup_workspace(man, run_dir, proj_rel)

        rc, out = git("rev-list", "--count", "HEAD", cwd=run_dir)
        assert rc == 0 and out.strip() == "1", f"workspace should have one commit, got: {out}"
        rc, _ = git("show", f"HEAD~1:{target}", cwd=run_dir)
        assert rc != 0, "git show HEAD~1 must fail inside the workspace"
        _, human = git(f"--git-dir={tmp / 'vuln_git'}", "show", f"HEAD:{target}")
        assert human and human != (run_dir / target).read_text(), "workspace must hold the blanked file"

        # Simulate an agent edit, then take the diff the way run_agent does.
        with open(run_dir / target, "a") as f:
            f.write("\n// agent edit\n")
        _, diff = git(f"--git-dir={tmp / 'vuln_git'}", f"--work-tree={run_dir}", "diff", "--", target)
        assert "+// agent edit" in diff and "\n-" in diff, "diff must be against the vulnerable commit"

        # The --from-patch path: fresh clone at the vulnerable commit, apply the diff.
        check = tmp / "check"
        git("clone", "--local", "--quiet", str(rt.resolve(man["clone"])), str(check))
        git("checkout", "--quiet", man["vulnerable_commit"], cwd=check)
        (tmp / "agent.patch").write_text(diff)
        rc, out = git("apply", "--check", str(tmp / "agent.patch"), cwd=check)
        assert rc == 0, f"agent.patch must apply on the vulnerable commit: {out}"
        print(f"ok: {tid} workspace has no history; agent diff re-applies on the vulnerable commit")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
