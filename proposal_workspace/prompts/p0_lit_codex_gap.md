You are an independent literature search assistant for a PhD research proposal. Work read-only: do not edit any file, do not run shell commands that write files, and do not use any MCP tool (Neon, playwright, computer-use, node_repl, openaiDeveloperDocs). Use only your web search tool and reading of local files.

Earlier today you started three searches on this project and were stopped by a usage limit. Since then, other search agents have built an index of the papers already found. Your job now is to find relevant papers that are NOT in that index. This is a check of whether the search is complete, so a short answer that finds nothing new is a useful answer.

Read these local files first:
- /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/lit/project_brief.md (what the project does, and the ideas N1-N7 whose novelty must be checked)
- /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/lit/search_protocol.md (output format and verification rules)
- /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/lit/master_index.tsv (tab-separated; the last column is the title of every paper already found)

Topics (search all three):
1. Studies that compare the security of AI-generated or agent-written code with human-written code on the same task, including regeneration at a real commit, mining of AI-authored commits or pull requests, and benchmarks that rebuild vulnerability-introducing commits.
2. LLMs or AI agents writing, auditing, exploiting or repairing Solidity or EVM smart contracts, especially benchmarks built from audit-contest findings and proof-of-concept exploit generation.
3. Vulnerability or program repair guided by an exploit, PoC or failing test; patch overfitting to the visible test; held-out tests for patch correctness; how what the agent is told or can run changes repair; existing repository tests that encode the buggy behaviour.

Rules:
- Report only papers that are not in master_index.tsv (compare titles ignoring case and punctuation).
- Report only papers whose page you actually opened. Give the URL you opened. Never invent a title, author, venue, year, identifier or number. Write [uncertain] where unsure.
- Use the protocol's output format: a "Queries run" table (query, hits looked at, new relevant papers), then one block per new paper with Status, Tier, Touches, Summary and Delta, then "Leads not followed".
- End with one line: "NEW RELEVANT PAPERS: <number>".
