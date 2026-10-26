# Project brief for the literature search

This brief tells each search agent what the project does, so it can judge how close a paper is. The full idea is in `IDEA.md` at the repository root. Do not edit `IDEA.md`.

## The question

Developers now hand coding to AI agents. Do AI coding agents write Solidity smart-contract code that is more or less secure than the human developer who wrote the same feature? And does an executable exploit (a proof of vulnerability, PoV) help an agent repair a vulnerability properly?

## How the project answers it

1. **Tasks come from audit-contest findings.** Public audit contests and audit firms (Code4rena, Sherlock, Cantina, Cyfrin, and others; collected through Solodit) publish accepted findings. Each finding is traced in the project's git history to the commit that introduced the bug (the vulnerability-introducing commit) and to the fix commit.
2. **Same request, same starting code, same exploit.** The vulnerable function's body is removed from the audited code. An agent gets a feature request for that function and writes it again. A Foundry exploit test (the PoV) adapted from the audit report then judges the human's code and the agent's code the same way. The PoV passes on the human's vulnerable code and fails on the human's fix.
3. **Treatment and control groups.** The treatment group holds functions where the human wrote a vulnerability. The control group holds other functions from the same commit that the human wrote correctly. On the control group, an LLM security review (two reviewers, also run on the human version) looks for new flaws, and a new PoV must confirm each one.
4. **Six agent setups.** Aider, OpenHands and Codex CLI, each with GPT-5.4-mini and Claude Sonnet 4.5. Models were chosen so that their training data ends before the findings were published (September 2025 or later).
5. **Repair with a masked PoV.** When a finding has several PoVs, the agent is shown one as a failing test and the others are held back to judge the repair. A shallow repair can block the shown PoV and still let a held-out PoV steal funds.
6. **Repair input study.** The agent repairs the human's vulnerable code. Two inputs change: what it is told (only the function's location, the written audit report, the shown PoV, or report and PoV) and what it can run (nothing, only the shown test, or a full terminal).
7. **Loss estimate.** Each PoV is extended to measure who loses how much.

## Pilot results so far (real data from this project)

- 8 findings, 4 setups, one run each. The feature request decided the outcome: when the request described the human's design, all 13 compiled runs wrote the bug; when it stated the rule that the fix restores, 12 of 15 avoided it.
- Finding 63008 (Uniswap v4 hook, a downward tick iterator skips its start tick, rewards can be stolen): 4 of 6 setups rewrote the human's bug. On the control functions, 2 of 11 compiled agent versions added the same new vulnerability, confirmed by PoVs.
- Repair round: one repair blocked the shown PoV but a held-out PoV still stole 48.88 ETH.
- Repair input study (144 runs, GPT-5.4-mini under three agents): with a full terminal, OpenHands succeeded in 2 of 12 runs, against 10 of 12 when it could run nothing. With a terminal, the agents kept the repository's own tests passing, and those tests assert the buggy behaviour. The agents also fitted the shown test: their fixes covered only the case the shown PoV met.

## Ideas whose novelty must be checked

- N1. Comparing an agent with the human developer on the same feature, from the same starting code, judged by the same executable exploit, with a control group of features the human wrote correctly.
- N2. Smart contracts (Solidity, DeFi): business-logic and accounting bugs with executable exploits, losses measured in funds.
- N3. Held-out (masked) PoVs to judge repairs, and the shown PoV given as a failing test.
- N4. How the repair input (report, PoV, location only) and the agent's ability to run code (nothing, shown test only, full terminal) change repair success; repository tests that encode the vulnerable behaviour; agents fitting the shown test.
- N5. Writing feature requests that do not hint at the bug or the fix, and checking that they do not.
- N6. LLM security review of agent code and human code with the same prompt, with each reported flaw confirmed by an executable test.
- N7. Estimating the financial loss of each exploit.
