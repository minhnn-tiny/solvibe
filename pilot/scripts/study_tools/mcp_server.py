#!/usr/bin/env python3
"""MCP server of the repair input study. It runs over stdio inside the agent's container.

  --test   adds run_shown_test, which runs the shared test script and returns its output (level E1).
  --files  adds read_file, list_dir, search_text, replace_in_file and write_file. Codex gets these in
           every arm: with its command tools off it has no other way to read or edit files, and
           giving them in every arm keeps its arms different only in the command and test tools.

Every path must stay inside the workspace (STUDY_PROJECT, default /work), judged by the path after
the filesystem resolves it, so `..` and symlinks that point outside are refused.
Needs fastmcp, which is in the OpenHands environment: /opt/openhands/bin/python mcp_server.py ...
"""
import argparse, os, re, subprocess
from fastmcp import FastMCP

ROOT = os.path.realpath(os.environ.get("STUDY_PROJECT", "/work"))
SKIP_DIRS = {".git", "out", "cache", "node_modules"}
MAX_MATCHES = 200
mcp = FastMCP("study")


def inside(path):
    p = os.path.realpath(os.path.join(ROOT, path))
    if os.path.commonpath([p, ROOT]) != ROOT:
        raise ValueError(f"refused: {path} is outside the workspace {ROOT}")
    return p


def run_shown_test() -> str:
    """Run the test from the report on the current code and return its output. The command is
    fixed (it is the command given in the task); this tool takes no arguments."""
    try:
        r = subprocess.run(["sh", "/opt/study/run_shown_test.sh"], capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return "The test run stopped after 900 seconds."
    return (r.stdout + r.stderr) + f"\n[exit code {r.returncode}]"


def read_file(path: str, offset: int = 1, limit: int = 400) -> str:
    """Read a text file in the workspace. Returns up to `limit` lines starting at line `offset`
    (1-based), each prefixed with its line number."""
    with open(inside(path), encoding="utf-8", errors="replace") as f:
        lines = f.read().split("\n")
    start = max(offset, 1)
    out = [f"{i}\t{lines[i - 1]}" for i in range(start, min(start + limit, len(lines) + 1))]
    more = len(lines) - (start + limit - 1)
    return "\n".join(out) + (f"\n[{more} more lines]" if more > 0 else "")


def list_dir(path: str = ".") -> str:
    """List the entries of a folder in the workspace. Folders end with '/'."""
    p = inside(path)
    return "\n".join(sorted(e.name + ("/" if e.is_dir() else "") for e in os.scandir(p)))


def search_text(pattern: str, path: str = ".", regex: bool = False) -> str:
    """Search the text files under `path` for `pattern` (plain text, or a Python regular
    expression when regex is true). Returns `file:line: text` for up to 200 matches."""
    base = inside(path)
    rx = re.compile(pattern if regex else re.escape(pattern))
    hits = []
    for d, dirs, files in os.walk(base):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for name in sorted(files):
            fp = os.path.join(d, name)
            try:
                with open(fp, encoding="utf-8") as f:
                    for n, line in enumerate(f, 1):
                        if rx.search(line):
                            hits.append(f"{os.path.relpath(fp, ROOT)}:{n}: {line.rstrip()}")
                            if len(hits) >= MAX_MATCHES:
                                return "\n".join(hits) + "\n[stopped at 200 matches]"
            except (UnicodeDecodeError, OSError):
                continue
    return "\n".join(hits) if hits else "no matches"


def replace_in_file(path: str, old: str, new: str) -> str:
    """Replace the text `old` with `new` in a workspace file. `old` must appear exactly once."""
    p = inside(path)
    with open(p, encoding="utf-8") as f:
        s = f.read()
    n = s.count(old)
    if n != 1:
        return f"not changed: the text to replace appears {n} times, it must appear exactly once"
    with open(p, "w", encoding="utf-8") as f:
        f.write(s.replace(old, new))
    return f"replaced 1 occurrence in {path}"


def write_file(path: str, content: str) -> str:
    """Write `content` to a workspace file, creating it or replacing all of its contents."""
    p = inside(path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"wrote {len(content)} characters to {path}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--files", action="store_true")
    a = ap.parse_args()
    if a.test:
        mcp.tool(run_shown_test)
    if a.files:
        for fn in (read_file, list_dir, search_text, replace_in_file, write_file):
            mcp.tool(fn)
    mcp.run(show_banner=False)
