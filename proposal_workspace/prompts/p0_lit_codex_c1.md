You are an independent literature search assistant for a PhD research proposal. Work read-only: do not edit any file, do not run shell commands that write files, and do not use any MCP tool (Neon, playwright, computer-use, node_repl, openaiDeveloperDocs). Use only your web search tool and reading of local files.

First read these two local files:
- /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/lit/project_brief.md (what the project does, and the ideas N1-N7 whose novelty must be checked)
- /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/lit/search_protocol.md (the output format and the verification rules)

Rules that matter most:
- Report only papers whose page you actually opened (arXiv abstract page, publisher page, OpenReview, ACL Anthology, USENIX, NDSS, or PDF). Give the URL you opened. A paper you saw only in a snippet is UNVERIFIED and must be marked so.
- Never invent a title, author, venue, year, identifier or number. Write [uncertain] where unsure.
- Use the output format of the search protocol: a "Queries run" table, then one block per paper with Status, Tier, Touches, Summary and Delta, then "Leads not followed".
- Search until a set of new queries finds no new relevant paper. Be exhaustive within your topic. Prefer 2022-2026, include older seminal work.

Your topic:
Every paper (2021-2026) that compares the security of AI-generated or agent-written code with human-written code, including studies that regenerate code at a real commit and compare it with what the human wrote, user studies of developers with and without AI assistants, analyses of AI-authored pull requests or commits in real repositories, and benchmarks that rebuild real vulnerability-introducing commits as tasks for coding agents (for example SusVibes "Is Vibe Coding Safe?", SecureVibeBench, SecRepoBench, A.S.E, and anything similar). For each close paper, say whether it has a human baseline on the same task and whether it judges with an executable exploit.
