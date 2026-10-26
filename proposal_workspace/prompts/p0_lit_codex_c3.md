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
Every paper (2015-2026) on vulnerability repair or program repair guided by a proof of concept, exploit, crash input or failing test; patch overfitting to the provided tests or exploit; held-out or independent tests to judge patch correctness; and how the input given to an LLM or agent (bug report, failing test, exploit, location, ability to run tests or a terminal) changes repair results. Include LLM and agent work (for example Pearce et al. S&P 2023, SAN2PATCH, APPATCH, CodeRover-S, SEC-bench, PatchEval, VulnRepairEval) and classic work (for example Fix2Fit, VulnFix, ExtractFix, Qi et al. ISSTA 2015, Smith et al. FSE 2015). Also look for work showing that existing repository tests encode buggy behaviour and mislead repair, and work on agents fitting the visible test.
