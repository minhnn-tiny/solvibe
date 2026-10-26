#!/usr/bin/env python3
"""Count eligible functions in an audit's in-scope Solidity files. Standard library only.
Reads files only. Never runs or builds anything from the repository.

Usage:
    python3 -I count_functions.py --repo <cloned repo> --scope <scope.txt> --out <functions.csv>
    python3 -I count_functions.py --selftest

scope.txt holds one in-scope .sol path per line, relative to --repo. Blank lines and '#' lines are skipped.

A function is a `function`, `constructor`, `fallback` or `receive` declaration with a body.
Modifiers are not counted. Declarations without a body (interfaces, abstract functions) are skipped.
A function is eligible when:
  - it is not view or pure (treated as writing state), its body is not empty, and it is not a
    single-call forwarding wrapper (one statement, no branch, no assignment, which is a call); or
  - it is view or pure and has more than one statement or any branch.
Any function whose body holds an `assembly` block is eligible.
Statements are counted as `;` in the body, minus two per `for (` header. Branches are
if, else, for, while, do, try, catch, switch, require(, assert( and the ternary `?`.
"""
import argparse, csv, re, sys
from pathlib import Path

DECL = re.compile(r"(?<![\w.])(?:(function)\s+(\w+)\s*\(|(function)\s*\(|(constructor)\s*\(|(fallback)\s*\(|"
                  r"(receive)\s*\()")
BRANCH = re.compile(r"\b(if|else|for|while|do|try|catch|switch)\b|\?|\brequire\s*\(|\bassert\s*\(")
ASSIGN = re.compile(r"(?<![=!<>])=(?![=>])|\+\+|--|\bdelete\b|\bemit\b")


def blank_comments_and_strings(src):
    """Replace comments and string literals with spaces, keeping newlines (same rule as frame_inventory)."""
    out, i, n = list(src), 0, len(src)
    while i < n:
        c, nxt = src[i], src[i + 1] if i + 1 < n else ""
        if c == "/" and nxt in "/*":
            end = src.find("\n", i) if nxt == "/" else src.find("*/", i + 2)
            end = n if end == -1 else end + (0 if nxt == "/" else 2)
        elif c in "\"'":
            end = i + 1
            while end < n and src[end] != c and src[end] != "\n":
                end += 2 if src[end] == "\\" else 1
            end = min(end + 1, n)
        else:
            i += 1
            continue
        for j in range(i, end):
            if out[j] != "\n":
                out[j] = " "
        i = end
    return "".join(out)


def functions(src):
    """[(name, kind, header, body)] for every declaration with a body, or None when braces do not balance."""
    text = blank_comments_and_strings(src)
    match, stack = {}, []
    for i, c in enumerate(text):
        if c == "{":
            stack.append(i)
        elif c == "}":
            if not stack:
                return None
            match[stack.pop()] = i
    if stack:
        return None
    out, header_end = [], -1
    for m in DECL.finditer(text):
        if m.start() < header_end:  # a function type inside the previous header
            continue
        kind = next(g for g in m.groups() if g in ("function", "constructor", "fallback", "receive"))
        name = m.group(2) or ("fallback" if kind == "function" else kind)
        brace, semi = text.find("{", m.end()), text.find(";", m.end())
        if brace == -1 or (semi != -1 and semi < brace):
            continue  # no body
        header_end = brace
        out.append((name, kind, text[m.start():brace], text[brace + 1:match[brace]]))
    return out


def after_params(header):
    """The header text after the parameter list, so a function-type parameter's `view` is not read."""
    depth, start = 0, header.find("(")
    for i in range(start, len(header)):
        depth += {"(": 1, ")": -1}.get(header[i], 0)
        if depth == 0:
            return header[i + 1:]
    return header


def classify(header, body):
    """(eligible, reason, view_pure, statements, branch)."""
    view_pure = bool(re.search(r"\b(view|pure)\b", after_params(header)))
    stmts = body.count(";") - 2 * len(re.findall(r"\bfor\s*\(", body))
    branch = bool(BRANCH.search(body))
    if re.search(r"\bassembly\b", body):
        return True, "assembly block", view_pure, stmts, branch
    if view_pure:
        if stmts > 1 or branch:
            return True, "view/pure with several statements or a branch", view_pure, stmts, branch
        return False, "simple getter (view/pure, one statement, no branch)", view_pure, stmts, branch
    if not body.strip():
        return False, "empty body", view_pure, stmts, branch
    if stmts <= 1 and not branch and not ASSIGN.search(body) and "(" in body:
        return False, "single-call forwarding wrapper", view_pure, stmts, branch
    return True, "may write state", view_pure, stmts, branch


def count(repo, scope_paths):
    rows, failures = [], []
    for rel in scope_paths:
        path = Path(repo) / rel
        if not path.is_file():
            failures.append((rel, "file missing"))
            continue
        fns = functions(path.read_text(errors="replace"))
        if fns is None:
            failures.append((rel, "braces do not balance"))
            continue
        for name, kind, header, body in fns:
            ok, why, vp, st, br = classify(header, body)
            rows.append({"path": rel, "function": "{}::{}".format(Path(rel).name, name), "kind": kind,
                         "view_or_pure": vp, "statements": st, "branch": br, "eligible": ok, "reason": why})
    return rows, failures


def selftest():
    src = """
    interface I { function f() external view returns (uint); }
    contract C {
        uint x; // function fake() { }
        string s = "function g() { }";
        function a() external view returns (uint) { return x; }
        function b(uint y) external view returns (uint) { if (y > 1) return y; return x; }
        function c() external { _c(); }
        function _c() internal { x = 1; }
        function d(function (uint) external cb) external { cb(1); x += 1; }
        function w(function (uint) internal view returns (uint) g) internal { x = 1; }
        function e() external pure returns (uint r) { assembly { r := 1 } }
        function abs() external virtual;
        receive() external payable {}
        constructor() { x = 2; }
    }"""
    got = {n: classify(h, b)[0] for n, k, h, b in functions(src)}
    assert got == {"a": False, "b": True, "c": False, "_c": True, "d": True, "e": True, "receive": False,
                   "constructor": True, "w": True}, got
    w = [h for n, k, h, b in functions(src) if n == "w"][0]
    assert not classify(w, "x = 1;")[2], "a function-type parameter's view must not make the function view"
    assert functions("contract C { function f() { ") is None
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo")
    ap.add_argument("--scope")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    scope = [ln.strip() for ln in open(a.scope) if ln.strip() and not ln.startswith("#")]
    rows, failures = count(a.repo, scope)
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["path"])
        w.writeheader()
        w.writerows(rows)
    print("scope files: {}  functions with a body: {}  eligible: {}  parse failures: {}".format(
        len(scope), len(rows), sum(r["eligible"] for r in rows), len(failures)))
    for rel, why in failures:
        print("  failure:", rel, why)


if __name__ == "__main__":
    sys.exit(main())
