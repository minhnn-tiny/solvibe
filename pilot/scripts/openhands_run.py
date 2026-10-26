#!/usr/bin/env python3
"""Drive OpenHands headless to implement a function in the repo mounted at /work.

Runs INSIDE the tools container (openhands venv). Model calls go out through
HTTPS_PROXY (only api.openai.com / api.anthropic.com are allowed). Writes token
usage to /work/_oh_metrics.json. Never raises past main: a failure is recorded.

Usage: openhands_run.py <litellm_model> <workdir> <feature_request_file> [target_file ...]

TOOLSET picks the tools (repair input study): "default" keeps the SDK's default tools, "no_terminal"
drops the terminal tool (level E0), and "test_only" also adds the shared test tool from the study's
MCP server, mounted read-only at /opt/study (level E1).
"""
import os, sys, json, traceback


def main():
    model, workdir, fr_file = sys.argv[1], sys.argv[2], sys.argv[3]
    targets = sys.argv[4:]
    api_key = os.environ["AGENT_API_KEY"]
    out = {"model": model, "ok": False, "tokens": {}, "cost_usd": None, "error": None}
    try:
        from pydantic import SecretStr
        from openhands.sdk import LLM, LocalConversation
        from openhands.tools import get_default_agent

        # OpenAI returns its reasoning encrypted. Ask for a readable summary of it instead.
        # This needs a verified OpenAI organization; REASONING_SUMMARY=none turns it off.
        # Anthropic models need nothing here: the SDK already turns extended thinking on.
        summary = os.environ.get("REASONING_SUMMARY", "detailed")
        kw = {"reasoning_summary": summary} if model.startswith("openai/") and summary != "none" else {}
        llm = LLM(model=model, api_key=SecretStr(api_key), usage_id="main", **kw)
        agent = get_default_agent(llm, cli_mode=True)  # cli_mode: no browser tool
        toolset = os.environ.get("TOOLSET", "default")
        if toolset != "default":
            mcp = {}
            if toolset == "test_only":
                from openhands.sdk.mcp import MCPServer
                mcp = {"study": MCPServer.model_validate({
                    "command": "/opt/openhands/bin/python", "args": ["/opt/study/mcp_server.py", "--test"],
                    "env": {"STUDY_PROJECT": workdir}})}
            elif toolset != "no_terminal":
                raise ValueError(f"unknown TOOLSET {toolset}")
            agent = agent.model_copy(update={"tools": [t for t in agent.tools if t.name != "terminal"],
                                             "mcp_config": mcp})
        conv = LocalConversation(agent=agent, workspace=workdir,
                                 persistence_dir=os.path.join(workdir, ".oh"))
        task = open(fr_file).read()
        tlist = "\n".join(f"- {t}" for t in targets)
        if os.environ.get("RAW_PROMPT") == "1":  # the repair round sends its own full prompt
            conv.send_message(task)
        else:
            conv.send_message(
                "You are a Solidity engineer working in the repository at the current "
                "working directory. Implement the function described below, in place, in "
                f"the existing file(s):\n{tlist}\n\n"
                "Edit only what is needed to implement it. Do NOT write or modify any test "
                "files. Do NOT change function signatures. When done, stop.\n\n"
                "=== FEATURE REQUEST ===\n" + task)
        conv.run()
        out["ok"] = True
        # Best-effort token/cost extraction across SDK versions.
        try:
            stats = conv.conversation_stats
            dump = stats.model_dump() if hasattr(stats, "model_dump") else {}
            pt = ct = 0
            def walk(o):
                nonlocal pt, ct
                if isinstance(o, dict):
                    if "prompt_tokens" in o or "completion_tokens" in o:
                        pt += int(o.get("prompt_tokens") or 0)
                        ct += int(o.get("completion_tokens") or 0)
                    for v in o.values():
                        walk(v)
                elif isinstance(o, list):
                    for v in o:
                        walk(v)
            walk(dump)
            out["tokens"] = {"prompt": pt, "completion": ct}
            # accumulated cost if the SDK computed one
            def find_cost(o):
                if isinstance(o, dict):
                    for k, v in o.items():
                        if k in ("accumulated_cost", "total_cost") and isinstance(v, (int, float)):
                            return float(v)
                        r = find_cost(v)
                        if r is not None:
                            return r
                elif isinstance(o, list):
                    for v in o:
                        r = find_cost(v)
                        if r is not None:
                            return r
                return None
            out["cost_usd"] = find_cost(dump)
        except Exception as e:  # metrics are best-effort
            out["metrics_error"] = str(e)
    except Exception:
        out["error"] = traceback.format_exc()[-2000:]
    # Always at the mount root so the host reads it at <run_dir>/_oh_metrics.json,
    # regardless of the project sub-directory used as the workspace cwd.
    metrics_path = os.environ.get("OH_METRICS", "/work/_oh_metrics.json")
    json.dump(out, open(metrics_path, "w"), indent=2)
    print("OPENHANDS_DONE ok=%s tokens=%s" % (out["ok"], out.get("tokens")))


if __name__ == "__main__":
    main()
