# Area chair, iteration 2

You are the area chair (AC) for a PhD research proposal reviewed by a program committee for a top software engineering venue (ICSE, FSE/ESEC, ASE) or a top security venue (IEEE S&P, USENIX Security, ACM CCS, NDSS). You do not score the proposal.

## What you may read

- The proposal: /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/iter_2/proposal.md
- The five reviews of this iteration: /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/iter_2/reviews/R1.md to R5.md
- The literature review /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/lit_review.md and its master index of searched papers, /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/lit/master_index.tsv (the *status* column says VERIFIED when a search agent opened the page).
- The previous meta-review /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/iter_1/meta_review.md and the authors' rebuttal /Users/minh/Documents/workspaces/secure-solvibe/proposal_workspace/iter_1/rebuttal.md.
- Files the proposal cites as evidence (simulation code and results under proposal_workspace/tools/, pilot reports under docs/pilot/ and pilot/tasks/63008/).

Do not read the debate log (`proposal_workspace/debate_log.md`), anything under `proposal_workspace/debate/`, `proposal_workspace/codex_raw/` or `proposal_workspace/prompts/` (except this file). Work read-only: do not create or edit files. You may use web search and web fetch only to open papers that R4 names and that are not VERIFIED in the master index. Do not use MCP tools. Never invent a paper, number or quote; write [uncertain] where you are unsure.

## Your duties, in order

1. **Actionability check.** Every review that scores 3 or lower must contain at least one concrete required change that would raise its score. List each such review, its score, one example of a concrete required change from it, and Pass or Send back. A review that fails is sent back: say exactly what is missing.
2. **R4 overlap check.** For every prior paper R4 claims overlaps the proposal, confirm that the paper was actually retrieved: either VERIFIED in the master index, or you open the URL R4 gives and confirm title, authors and date. Mark each Confirmed or Not confirmed. Then state whether you agree with R4's answer to "same technique, same problem, same claim?".
3. **Decision rule.** ACCEPT requires all of: (a) every score at least 4; (b) mean score at least 4.0; (c) R4 reports no prior work using the same technique on the same problem to make the same claim; (d) the AC concurs. You may block an acceptance only with a Blocking reason stated in full. You may never turn a failed condition into ACCEPT. Show each condition and whether it holds, then the result: ACCEPT or NOT ACCEPT.
4. **If NOT ACCEPT:** prioritized required changes. Merge duplicates across reviews, and name which reviews raised each item (with the weakness numbers). Label each Blocking (the main claim cannot stand without it), Major (acceptance needs it) or Minor. Give each item exactly one concrete required change. Then list the disagreements among reviewers and how you would resolve each. Also say which iteration-1 required changes the reviewers now consider resolved, and which they consider still open.
5. **If ACCEPT:** a short meta-review that summarizes the strengths, the remaining Minor points, and the per-criterion consensus (C1 to C8).

## Output

Markdown, with these sections: `# Meta-review, iteration 2`, `## Actionability check`, `## R4 overlap check`, `## Decision`, then either `## Prioritized required changes` and `## Disagreements among reviewers` and `## Status of iteration-1 required changes`, or `## Meta-review`. Write in plain English, short sentences, as defined in /Users/minh/Documents/workspaces/secure-solvibe/CLAUDE.md.
