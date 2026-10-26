// Calls Codex through the codex plugin's own app-server runtime (openai-codex/codex 1.0.6).
// The plugin's `task --resume-last` resumes whichever task thread ran last in the repository,
// so parallel Codex roles would resume each other's threads. This wrapper passes the thread id.
//
// Usage: node codex_call.mjs --prompt-file P.md --out codex_raw/STEP.md [--resume THREAD_ID] [--model gpt-6-astra] [--effort medium]
// Defaults (user request, 21 October 2026): model gpt-6-astra, reasoning effort medium.
// Writes the final message word for word to --out, and the thread id, status, error, web
// searches and reasoning summary to the same path with .meta.json. Exit code 0 only on a completed turn.
import fs from "node:fs";
import path from "node:path";

const PLUGIN = process.env.CODEX_PLUGIN_ROOT ?? "/Users/minh/.claude/plugins/cache/openai-codex/codex/1.0.6";
// The plugin's shared broker keeps every thread it ran loaded, and Codex 0.163 then refuses to
// resume it ("already has an active writer"). A broker endpoint that does not exist makes the
// plugin fall back to its own direct app-server per call, which exits and frees the thread.
process.env.CODEX_COMPANION_APP_SERVER_ENDPOINT ??= "unix:/nonexistent/solvibe-no-broker.sock";
const { runAppServerTurn } = await import(path.join(PLUGIN, "scripts/lib/codex.mjs"));

const argv = process.argv.slice(2);
const opt = (name) => {
  const i = argv.indexOf(`--${name}`);
  return i >= 0 ? argv[i + 1] : undefined;
};
const promptFile = opt("prompt-file");
const out = opt("out");
if (!promptFile || !out) {
  console.error("need --prompt-file and --out");
  process.exit(2);
}

const progress = [];
const meta = { started: new Date().toISOString(), promptFile, resume: opt("resume") ?? null, model: opt("model") ?? "gpt-6-astra", effort: opt("effort") ?? "medium" };
let result;
try {
  result = await runAppServerTurn(opt("cwd") ?? process.cwd(), {
    resumeThreadId: opt("resume"),
    prompt: fs.readFileSync(promptFile, "utf8"),
    effort: opt("effort") ?? "medium",
    model: opt("model") ?? "gpt-6-astra",
    sandbox: "read-only",
    persistThread: true,
    threadName: `proposal ${path.basename(out, ".md")}`,
    onProgress: (p) => progress.push(typeof p === "string" ? p : p.message)
  });
} catch (error) {
  result = { status: 1, error: { message: String(error?.message ?? error) } };
}

fs.mkdirSync(path.dirname(out), { recursive: true });
if (result.finalMessage) fs.writeFileSync(out, result.finalMessage);
Object.assign(meta, {
  finished: new Date().toISOString(),
  status: result.status,
  threadId: result.threadId ?? null,
  turnId: result.turnId ?? null,
  error: result.error ?? null,
  stderr: result.stderr ?? null,
  webSearches: progress.filter((m) => m?.startsWith("Searching:")),
  progress,
  reasoningSummary: result.reasoningSummary ?? null
});
fs.writeFileSync(out.replace(/\.md$/, "") + ".meta.json", JSON.stringify(meta, null, 2));
console.log(JSON.stringify({ status: meta.status, threadId: meta.threadId, error: meta.error?.message ?? null, webSearches: meta.webSearches.length, out }));
process.exit(result.status === 0 && result.finalMessage ? 0 : 1);
