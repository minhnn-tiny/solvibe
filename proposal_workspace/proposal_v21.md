# AI Agent Function-Body Replacements in Audited Solidity: Executable Vulnerability Comparisons with Historical Developer Code

Proposal version 21 (author of this revision: Peer B, Loop 1 round 20; version 20 was written by Peer A in round 19).

## 1. Abstract

We compare AI-generated function replacements with historical developer implementations in audited Solidity contracts. A probability sample includes functions linked to audit findings and functions without such links. Tasks must be constructible under a fixed procedure and allowance. Each implementation receives its own audit-blind discovery campaign. A counted vulnerability requires an executable attack, a correction confined to the target body, and independent adjudication. The proposed principal comparison measures detected vulnerability among working implementations, standardized across the constructible population. Functional failure is reported separately. Adverse bounds retain unresolved outcomes. Development tests the procedure and its cost; it does not certify rare failure rates. We propose author-specific operating limits and monitoring during a fixed main sample. Their validation remains pending. The flagged-only comparison is secondary. PoV-guided repair remains a separate extension. Committee approval, student timing and final readiness checks are required.

## 2. Problem and motivation

Solidity developers already use AI tools. The Solidity Developer Survey 2025 reports that 58% of respondents use them daily and 49% use them to write code [Solidity Survey]. These are self-reports. They establish relevance, not the security of generated code.

Security failures in contracts can transfer funds or prevent legitimate operations. In a study of 516 exploitable smart-contract bugs, more than 80% were beyond the automated tools examined [Web3Bugs]. A separate study found substantial limitations in Solidity static analyzers [SAST Study]. These results motivate executable evidence of specific attacker effects.

Existing benchmarks answer useful but different questions. SecureVibeBench reconstructs tasks around historical vulnerabilities and applies executable checks to developer and agent implementations [SecureVibeBench]. SusVibes evaluates functional and security outcomes on reconstructed vulnerable tasks [SusVibes]. Foresight-SWE studies tasks associated with later-fixed general defects [Foresight-SWE].

Selecting functions because a developer previously failed cannot establish the average difference across other functions. Agents might avoid known mistakes while introducing different vulnerabilities elsewhere. Conversely, a benchmark of historical failures may exaggerate the apparent advantage of replacement.

Unconditional comparisons are not new. Sajadi et al. compare human and agent patches for the same issues [Patch Security]. Cotroneo et al. compare human and AI functions paired by documentation [Cotroneo]. SolEval already regenerates function bodies in real Solidity repositories [SolEval]. SolAgent compares generated and historical Solidity using static analysis [SolAgent].

The first paper proposes a population comparison using executable, function-attributed security evidence. It includes functions without qualifying audit findings. Its principal question concerns detected vulnerability among working implementations. It also reports whether a flagged-only analysis gives a different answer.

This is an empirical contribution, not a claim that probability weighting or conditional-rate estimation is new. Its value depends on the precision, coverage and detection evidence achieved by the study.

A specified extension concerns repair. Existing research already shows that incorrect tests can mislead agents [ImpossibleBench; ExecCritic; Calibration]. We ask a narrower question: does executing assertions that endorse an exploitable behavior preserve that behavior despite contrary PoV evidence, beyond the effect of matched ordinary incorrect assertions?

Neither study estimates how much human review developers can safely remove.

## 3. Key insight and contributions

### Paper 1: compare detected security and functional failure separately

Audit labels define sampling strata. They are not security verdicts.

We propose RQ1b as the principal estimand. For each agent configuration, it compares detected vulnerability among working agent and historical implementations. It standardizes stratum-specific differences using the function shares of the constructible domain.

This is not the probability that an agent introduces a flaw into a particular function that the developer implemented safely. Conditioning on working outputs does not create a causal comparison between equivalent sets of implementations.

The study reports the joint functional-and-vulnerable endpoint alongside this conditional comparison. An exact decomposition shows the contribution of functional failure. Failed generation remains visible.

RQ1a is the difference between the flagged-only and domain-standardized comparisons. It is secondary.

### Requested changes to the committee’s design decisions

The iteration-3 committee asked us to retain RQ1a as principal and add an RQ1b target. We request approval to make RQ1b principal.

The examined allocations give broad RQ1a intervals. For the earlier allocation of 20 protocols with two V and six N functions, V27 reports a largest mean security-component half-width of 0.338. Its observed-fix-only count scenario gives 0.422. These runs precede the strict recount and assume complete construction and resolved outcomes. They do not support the earlier 0.20 criterion.

This does not prove that every affordable RQ1a design has been ruled out. RQ1b instead answers the project’s underlying comparison directly: a weighted comparison of historical and agent implementations on ordinary as well as audit-flagged Solidity functions, using blind discovery and executable attribution.

We also request approval for a minimum correct-direction power of 0.60 at an exact +0.15 conditional difference within the validated operating region. This replaces the unsupported 0.80 requirement. It is a substantive reduction in ambition. A large difference may be missed. A broad null result will remain inconclusive.

This revision requests a further change to readiness assessment. The committee retained adverse bounds and required development-based unresolved-rate scenarios. We retain adverse bounds in the principal analysis. We propose to replace the development confidence-limit rule with author-specific operating limits, fixed before collection, and monitoring during the complete probability sample.

The reason is structural. A few development protocols cannot certify a rare historical failure rate. More agent attempts do not supply more historical implementations or independent protocol environments. Pooling those outcomes gave a misleading appearance of precision.

The revised launch decision therefore does not assert that unresolved rates are known to be small. It states the rates and mechanisms under which the study has useful power. The study is undertaken with an explicit risk of exceeding that region. If the committee requires an empirical guarantee of low unresolved rates before launch, this proposal does not provide one.

### Count discoveries made under a common procedure

An audit gives historical code an extra source of known vulnerabilities. Replaying audit-derived attacks does not provide an equally strong search for different agent flaws.

The primary endpoint uses only flaws found and confirmed through each implementation’s own campaign. Every campaign follows the same frozen procedure and budget. It receives no audit report, finding list, audit-derived PoV or audit-derived correction.

Pooling discovered attacks can favor flaws shared by many agent attempts. Common replay is secondary and cannot change locked primary labels.

This compares detected vulnerabilities under a stated procedure. It does not establish equal sensitivity or compare all latent vulnerabilities.

### Planned extension: faulty assertions during PoV-guided repair

The pilot motivates a hypothesis but does not establish it.

The two preregistered OpenHands contrasts were:

- adding the shown PoV, with a full terminal in both arms: 0 of 12 successes versus 2 of 12, with Holm-adjusted p = 0.96;
- allowing the shown PoV to be rerun: 10 of 12 versus 9 of 12, with Holm-adjusted p = 1.00.

The exploratory comparison between no execution and a full terminal was 10 of 12 versus 2 of 12. OpenHands succeeded in 9 of 12 runs with the shown-test tool. Codex succeeded in 6 of 12 both with that tool and with a full terminal.

These results concern one finding. The repairs have not yet been reviewed by a person. The faulty-test hypothesis was formed after inspecting the pilot. The proposed repository-test tool is narrower than a full terminal.

The extension compares wrong assertions endorsing a vulnerability with matched wrong assertions endorsing an ordinary error. It measures whether each endorsed behavior remains. It is not a claimed contribution of the protected twelve-month study.

## 4. Threat model and problem setting

### Historical replacement

Each task replaces one function body in a fixed audited snapshot. The historical developer implementation supplies the baseline.

The agent sees mature surrounding code and repository tests. These may have been written after the original function. The study does not recreate the developer’s original conditions or estimate a causal effect of replacing a human worker.

Historical code may contain AI assistance. Its provenance is recorded rather than assumed.

### Attacker and environment

The attacker is an unprivileged external account. It may deploy contracts, call public interfaces and use borrowing or transaction ordering permitted by the protocol record.

The attacker cannot steal keys, assume an administrator role, change trusted oracle behavior outside the recorded assumptions or modify deployed code.

Each protocol record specifies:

- protected assets and legitimate entitlements;
- available capital and permitted borrowing;
- reachable initial states;
- token and oracle behavior;
- transaction ordering and block assumptions;
- legitimate operation and resource limits.

All execution occurs offline. Arbitrary storage changes cannot manufacture an otherwise unreachable vulnerable state.

### Severity

The study uses one rubric across audit platforms. Original audit labels remain in the record.

High severity includes unauthorized loss of principal, protocol insolvency and irreversible loss of access to protected assets. Medium severity includes theft of earned protocol entitlements and attacker-induced loss of a core operation under the recorded resource and recovery limits.

Ordinary implementation failure is not automatically a security vulnerability. Availability findings require an attacker action, affected legitimate users and demonstrated failure under permitted operating conditions.

Financial effects must reflect entitlement or backing. Attacker profit alone is insufficient. Temporary inconvenience, gas optimization, privileged misuse and effects outside the threat model are excluded.

Before evaluation, the rubric records how recoverability, repetition, affected users and resource limits determine inclusion. A frozen tie rule excludes borderline severity cases from the primary count and includes them in a secondary count. This is a classification rule, not evidence that those cases are harmless.

### Attribution

A counted flaw requires:

- an executable qualifying property violation;
- evidence connecting it to the target function;
- removal of the violation by changing only that function body;
- preservation of required functionality under the acceptance checks.

The intervention preserves signatures, surrounding code, dependencies and initial-state procedures. It cannot disable the feature or hide a loss by changing accounting.

A new declaration outside the body is not permitted, even if it is an error or event used only by the correction.

Historical code may serve as a correction only after the same checks.

Two adjudicators outside the construction team assess severity and attribution. Packs conceal author, agent and experimental arm as far as the code permits. Disagreements, resolution and blinding failures are recorded.

## 5. Approach

```mermaid
flowchart TD
  A["Audit listings and public repositories"] --> B["Reconciled protocol and function frame"]
  B --> C["Fixed probability sample"]
  C --> D["Fixed per-function blind construction"]
  D --> E["Historical implementation and two native agents"]
  D --> X["Construction records and estimated domain shares"]
  E --> F["Own discovery and blind confirmation"]
  F --> G["Executable evidence and independent adjudication"]
  G --> H["Lock checks, outcomes and unresolved records"]
  H --> I["Primary estimates with adverse bounds"]
  X --> I
  H --> M["Monitor unresolved outcomes by author and stratum"]
  M --> R["Report operating limits and departures"]
  I --> R
  I --> Q["Secondary flagged-only comparison"]
  H --> J["Common replay and audit-assisted evaluation"]
  B --> K["Separate audit-derived records"]
  K --> J
  K --> L["Audit rediscovery and audit-missed validation"]
  D --> S["Matched seeded validation"]
  S --> N["Detection evidence and sensitivity analysis"]
  L --> N
  N --> I
  K --> O["Extension: shown PoVs and hidden variants"]
  O --> P["Faulty assertions and matched ordinary controls"]
```

### 5.1 Frame and sampling unit

The downloaded data contain 19,627 distinct High and Medium findings. The earlier overview’s total of 19,666 was inconsistent with its batch totals. Complete source files were obtained for 7,826 findings. Earlier filtering left 77 recent candidates and 43 with suitable public history. These are screening counts, not a validated sample.

The refreshed frame starts from public contest listings where possible. Protocols without qualifying findings can enter. If only a finding-derived frame is practical, the population is explicitly restricted to audits with at least one qualifying finding.

The first-stage sampling unit is a protocol audit and its fixed snapshot. Multiple audits of the same project are identified before sampling. Overlapping snapshots cannot be treated as independent protocols without accounting for that dependence.

A protocol must have an available audited snapshot, pinned dependencies, an offline build and sufficient documentation to define its environment.

A function must be in audit scope, contain meaningful computation or state changes, and be replaceable without changing its signature or surrounding code. Tests or a documented call path must support reachability.

The second-stage unit is one function body. Its identifier includes repository, snapshot, full file path, enclosing contract and signature. Overloads are distinct.

Before sampling, functions implicated in qualifying findings whose necessary corrections extend outside the target body are excluded. Unrelated edits in a fix commit do not establish that a broader correction is necessary.

Stratum V contains eligible functions linked to qualifying High or Medium findings. Stratum N contains eligible functions without such links. Functions with unresolved finding mappings or correction scope are not silently assigned to N.

The report gives exclusions and unresolved classifications separately. Multi-function replacement is a named extension.

#### Earlier pilot fix-scope evidence

The record for the 43 pilot findings is in `evidence/frame_count/`.

| Fix scope | Findings | High confidence |
|---|---:|---:|
| One function body | 17 | 14 |
| Several function bodies | 2 | 2 |
| Signature, storage layout, new function or other declaration | 15 | 14 |
| Undetermined | 9 | Not applicable |

These classifications describe identified developer fixes. They do not prove that no narrower correction exists.

Three judgment calls move the one-function count between 15 and 18. Panoptic supplies 9 of the 17. Three of the ten protocols have no identified one-function fix among the filtered findings.

#### Inventory of downloaded findings

The inventory in `evidence/frame_inventory/` groups the findings into 2,481 audits. It maps functions from source links where possible. It could not map 61.0% of findings.

Its earlier planning distribution used mapping rates and the pilot proportion 17/34. That distribution is a model, not a measured eligible frame. It remains only to explain older simulations.

#### Random audit sample and strict recount

The audit in `evidence/frame_audit/` starts from 70 recent audits after the stated pilot exclusions. A fixed random order was drawn. Processing the first 33 audits yielded 25 processed audits and eight replacements.

The replacements reflect unavailable repositories, unavailable scope or non-Solidity code. Five were Cantina private reviews. The processed sample represents accessible audited code more closely than all reviews.

The audits contain 352 High and Medium findings. Claude agent sessions performed the reading, followed by merge checks and a spot check. This was not human adjudication. No repository code was executed.

| Quantity in the initial record | Count |
|---|---:|
| Processed audits | 25 |
| Findings | 352 |
| Findings with an observed fix | 156 |
| Findings classified from a recommendation | 98 |
| Findings with undetermined fix scope | 98 |
| Functions with a body | 5,364 |
| Functions accepted by the counting rule | 3,965 |

The initial V totals were 62 from observed fixes and 118 when recommendations were included. Initial N totaled 3,621. The strict recount supersedes these counts for current planning.

The recount in `evidence/frame_audit/strict/` rereads every observed fix previously classified as a one-body correction. Full paths, contracts and parameter types separate 94 colliding names involving 198 functions.

Strict observed-fix V requires a correction confined to the function body. New errors, events, imports, modifiers or other declarations are excluded. The same function-eligibility rule applies to V and N.

| Strict count | Total | Mean per audit | Median | Audits with zero |
|---|---:|---:|---:|---:|
| V, observed fixes only | 54 | 2.16 | 1 | 10 of 25 |
| V, observed fixes and admissible recommendations | 109 | 4.36 | 4 | 1 of 25 |
| N, eligible and unflagged | 3,620 | 144.8 | 92 | 0 of 25 |

The rereading records four fixes with a new error and one with an import. Three changed a function that was not the root cause. Two counted an ineligible overload. One finding falls under two reasons. Two recommendations also failed the rule.

The audits with no observed strict V function have private or unpublished fixes. Their zeros do not establish absence of eligible V functions.

Recommendation-inclusive counts are not proven upper bounds. Unresolved findings may contain additional eligible functions. Recommendations may also understate the correction required. The simulation label “upper” means recommendation-inclusive counts only.

Strict N counts range from 24 to 672. This spread motivates sampling in proportion to N counts.

#### Remaining frame-freezing checks

The strict recount resolves the earlier identity and body-only classification problems. It is not the final eligible census.

The study’s severity rubric has not replaced the original High and Medium labels. The record identifies 18 findings with root causes outside functions, eight close observed-fix calls and 134 reread rows without a second reader. One audit uses a later public snapshot for fixes and another uses an upstream fork.

The counting parser treats non-view functions as potentially state-changing rather than proving actual writes.

Before inclusion probabilities are frozen, these eligibility and provenance questions must be settled under the study’s rules. Excluded and unresolved cases remain in the record.

### 5.2 Allocation and processing limits

The proposed main allocation is 22 distinct protocol audits, with up to one V and six N functions per audit. Small strata are censused.

V is a small part of the strict counted frame. Moving one function slot from V to additional protocols improves the principal comparison in the tested simulations. It reduces the available V sample. Its effect on RQ1a precision remains unmeasured.

The first-stage size measure is the eligible N count, or one when that count is zero. Fixed-size inclusion probabilities are proportional to this measure, with certainty inclusion capped at one.

Protocols are selected by randomized systematic sampling. The implementation randomly permutes the frame, draws a uniform start and selects from cumulative inclusion probabilities. It records probabilities, order and seed.

Functions are sampled uniformly without replacement within each stratum. The inverse joint inclusion probability supplies the analysis weight.

Both primary agents receive two fresh attempts per constructed function.

Each function receives the same construction procedure and its own fixed allowance. Protocol preparation has a separate allowance. Neither is a pool that early functions can consume.

Let \(B_i=1\) when function \(i\)’s task passes the construction checklist within its allowance. Otherwise \(B_i=0\), with a recorded reason. This precedes generation and vulnerability evaluation and applies to the whole function cohort.

The primary population is the constructible domain. Its stratum shares are estimated from weighted constructed counts.

A function does not become unconstructible because another function took too long or promised staff were unavailable. Failure to supply the procedure is a protocol deviation.

Each implementation receives fixed discovery and confirmation allowances. Unused time cannot extend another implementation’s search. A completed campaign without confirmation is “not confirmed.” Required evaluation or adjudication that cannot finish remains unresolved.

Slow protocols are not replaced after sampling.

Each selected protocol with a constructed V function contributes that function to audit-assisted secondary work. Its conditional selection probability is one. One such task is reserved per protocol.

Construction yield is reported by stratum. A lower confidence limit below 0.7 prevents launch under the proposed construction rule. This limit is not raised to 0.7. Dependence and small denominators must remain visible.

Development now uses the same one-V, six-N allocation and two attempts per configuration. Its purpose is to check the procedure and resource limits. It does not estimate a rare unresolved-outcome rate with claimed population precision.

### 5.3 Provenance and AI assistance

For each function, the study records available history around its introduction. Evidence includes agent instruction files, AI co-author trailers and pull-request text.

Categories are evidence of assistance, no observed evidence and unresolved provenance. An instruction file does not prove that the target lines were generated. Absence of a marker does not prove human-only authorship.

All categories remain in the primary historical-developer comparison. A subset without observed evidence of assistance is a preregistered secondary analysis.

Code, fix and report publication dates are recorded separately. A report published after a model cutoff does not establish that the code was unseen.

### 5.4 Audit-blind task construction and confirmation

Request and primary-property builders do not receive audit findings, historical fixes or the removed body. They receive permitted documentation, signatures, callers and surrounding code.

Every request sentence records its source. Requests and primary properties are frozen before agent runs.

Security properties must follow from documented entitlements and operations. Audit-derived invariants, corrections and attacks cannot enter primary discovery under another name.

Development freezes the source bundle, preparation procedure, request template, construction checklist, ordered steps, tools, versions, assistance, allowances, interruption rules, assignments and failure records.

The checklist requires a coherent request, documented legitimate behavior, a reachable setup, ordinary checks, primary security properties and the threat-model record. Completion does not require finding a vulnerability.

For a protocol unfamiliar to the student:

1. The second person checks mappings and exclusions and seals labels.
2. The student constructs tasks without audit access.
3. Generation and discovery run. The student confirms candidates using only their originating campaign materials and permitted context.
4. Independent adjudication and permitted primary check revisions finish. Records are locked.
5. Only then may the student access audit material.

For a protocol known to the student:

1. The student prepares mappings and sealed materials.
2. An unexposed second person constructs and confirms tasks.
3. Independent adjudication and primary locking finish.
4. Only then may that person inspect the audit.

An unexposed replacement must be funded if neither person qualifies. Failure to provide the role is a protocol deviation. Construction staff cannot independently adjudicate their own packages.

The same rule applies to development and validation.

#### Duplicate requests

For 15 randomly selected sampled functions, two unexposed builders independently prepare requests. The primary construction procedure is designated in advance. It determines \(B_i\). The duplicate cannot rescue failed primary construction.

When both requests are evaluable, both receive generation and the same discovery procedure. Changes in D, working status and defined conditional estimates are secondary. Failed duplicate construction remains recorded.

The added evaluation uses at most \(15\times5\) campaigns. Operation and coordination share the section 8 reserve. Packages enter the paid-review ledger.

Audit-informed request classification occurs after locking and without agent outcomes. It labels requests as favoring vulnerable behavior, neutral or favoring corrected behavior. It cannot change \(B_i\).

Builder identity, exposure and order are recorded. Builder-based analyses do not eliminate protocol confounding.

### 5.5 Functional and security checks

Checks are classified before generation. Ordinary checks establish intended operations, outputs and useful completion. Explicit security checks establish forbidden attacker outcomes.

An ordinary check is not removed merely because it catches a flaw. Historical code is not assumed to pass. Original repository-test outcomes are reported separately.

If a blind-process correction removes a confirmed violation but fails an ordinary check, two author-blind adjudicators decide whether that check asserts the forbidden outcome. If so, it is removed for every implementation of that function. L is recomputed consistently.

This occurs before primary locking and audit access. Original and revised outcomes remain recorded.

An audit-assisted correction cannot reopen the primary endpoint. Any resulting check revision defines a secondary suite applied to the entire function cohort.

| PoV outcome | Meaning |
|---|---|
| Violation observed | Valid execution demonstrates the forbidden outcome. |
| Violation checked and absent | The scenario executes and checks that the outcome did not occur. |
| Unresolved | Construction, execution or interpretation prevents a valid judgment. |

An exit code is not a security verdict. Expected failure of a violation assertion differs from setup failure. Fixed-state checks establish that legitimate behavior remains.

### 5.6 Agent configurations

The primary configurations are Claude Code and Codex CLI with vendor-supported models current at the freeze.

Model identifiers, versions, reasoning settings, prompts, permissions and budgets are pinned. Both configurations run on the full constructed sample. Every attempt starts from a fresh workspace.

The target body is replaced with a placeholder. Only the submitted body enters evaluation. Changes to tests, dependencies or unrelated code cannot alter the artifact.

History, fixes, cached target copies and revealing generated artifacts are removed. Network access is restricted to model APIs.

Pilot configurations, translated integrations and a documented SolAgent adaptation are extensions. They cannot enlarge the primary family or its discovery budget.

### 5.7 Primary discovery

Each implementation receives:

- Foundry property-based fuzzing;
- the same two LLM reviewers;
- a fixed candidate ordering rule;
- fixed discovery and confirmation allowances.

Reviewer identities and versions are frozen. Reviewers from other model families are preferred where development supports them. Otherwise the overlap is reported.

A secondary analysis filters both authors’ results to fuzzing and the other-family reviewer. It does not rerun campaigns or reallocate effort.

Reviewers receive code, permitted context, properties and the request, without author labels or audit material. Campaigns cannot access other implementations’ reports or attacks. Duplicate outputs may share deterministic execution but gain no extra stochastic search.

At most three candidates are processed in frozen order within the campaign allowance. This is not a separate allowance for each candidate.

The development and proposed main student campaign cap is \(0.328\) hours. It consists of \(0.15\) hours for operation and supervision and \(0.178\) hours shared by confirmation, correction, packaging and primary lock administration. These are fixed planning caps, not measured evidence of adequate time.

If the caps cannot support valid work, development records the failure. They are not silently enlarged.

A positive primary label requires an own-campaign candidate, executable confirmation and independent adjudication.

The record distinguishes completed negative campaigns, cut candidate lists, failed evaluation and missing adjudication. Evaluation and adjudication failures remain unresolved. A secondary bound treats cut candidate lists as unresolved too.

Primary records are locked before pooled replay.

### 5.8 Secondary replay and audit rediscovery

Validated common-procedure PoVs are replayed after locking. Attribution is checked separately for each implementation.

Audit-assisted work covers the constructed V function in each selected protocol. Neither replay nor audit access changes primary labels.

The report separates own discoveries, pooled discoveries, audit-assisted outcomes and their estimated increment.

For a general secondary selection probability \(q_i\),

\[
\widehat T_{\mathrm{increment}}
=
\sum_{i\in S_V}w_iB_i\frac{A_i}{q_i}
\left(Y_i^{\mathrm{audit}}-Y_i^{\mathrm{primary}}\right).
\]

Under the current allocation, \(q_i=1\) for each constructed sampled V function.

For conditional rates, numerator and working-output denominator totals are estimated separately before taking ratios. Unresolved secondary outcomes retain bounds.

Rediscovery is a weighted ratio among audit flaws satisfying the confirmation standard. The numerator counts those also found by the blind campaign. Audit flaws that do not meet that standard cannot enter the denominator as confirmed vulnerabilities.

Secondary uncertainty must reflect the main sampling design and any additional selection. Numerical claims require validation of the secondary estimator.

### 5.9 Detection validation

#### Matched seeded flaws

A separate builder inserts the same vulnerability pattern into historical and agent implementations of a function. Patterns come from other protocols.

Seeds must compile, preserve unrelated behavior and produce an attributable violation. Invalid seeds remain recorded.

The core schedules 60 matched pairs, or 120 seeded artifacts. The planned allocation is 15 pairs per stratum and configuration combination. The catalogue contains at least 20 patterns, with no pattern used in more than three pairs.

Seeded and unseeded controls receive blind discovery. Locations and known attacks remain hidden until locking. Seeded artifacts do not enter natural vulnerability estimates.

The pooled diagnostic concerns the validation mixture, not population-weighted natural recall.

The planning expression in `tools/power_results_v10_c.txt` is

\[
1.96\sqrt{\frac{\operatorname{deff}(\delta-d^2)}{n}}.
\]

With \(d=0.1\), design effect 1.5 and 60 pairs, its half-width is 0.135 to 0.194. With design effect 3.1, it is 0.194 to 0.278.

These are assumptions. The core cannot establish equal recall within 0.05. Final uncertainty uses realized protocol and pattern dependence and the valid-pair count.

#### Natural-implementation investigation

The maximum is 48 first assessments and 12 duplicates. Each assessment has a two-hour budget. Total investigation cannot exceed 120 auditor hours.

The 12 cells are defined by author, stratum and campaign category. Each receives up to four first assessments. Confirmed cells are sampled uniformly. Non-confirmed cells include completed negatives and unresolved evaluations. Where both exist, one is sampled from each before drawing remaining cases uniformly. Smaller cells are censused. Unused slots are not transferred after outcomes.

Up to 12 cases receive a second assessment, selected randomly. Auditors receive permitted context and the harness, not campaign reports or author labels where concealment is possible.

Selection probabilities support weighted disagreement estimates. Sparse cells and unresolved judgments remain visible. The rough ±0.3 calculation for eight negative cases is not a precision guarantee.

This is a budgeted reference assessment, not proof of vulnerability absence.

#### Flaws missed by an earlier audit

A separate set targets 10 to 20 later-discovered flaws demonstrably present in code covered by an earlier audit. Later-introduced flaws do not qualify.

The record identifies scope, vulnerable version, later finding and correction. These protocols are outside the main frame.

Availability remains unknown. Fewer than 10 cases leave historical N sensitivity at the full feasible range unless another explicit assumption is examined. Even a larger set describes selected cases, not all historical N flaws.

#### Discovery development gate

The gate uses eight qualifying flaws and passes at five rediscoveries. At most one procedure revision is permitted, assessed on eight fresh flaws with a pass mark of six. Failure of both assessments stops development for redesign.

| Assumed recall | First assessment | Revision assessment | Overall pass probability |
|---|---:|---:|---:|
| 0.3 | 0.058 | 0.011 | 0.069 |
| 0.5 | 0.363 | 0.145 | 0.455 |
| 0.7 | 0.806 | 0.552 | 0.913 |

These are independent-binomial planning calculations, not established guarantees for clustered findings or adaptive prompt revision.

The eight built pilot tasks that shaped prompts leave the reserve. Fresh gate cases cannot have been used to revise the tested procedure. All attempts are reported.

This discovery gate is separate from unresolved-outcome readiness. No discovery-gate result certifies a rare unresolved rate.

#### Audit-blind candidate rediscovery

The evidence in `evidence/rediscovery/` covers 17 single-function pilot findings. Reviewers received a pre-fix target file, limited context and a task naming the function, without audit findings.

Fresh Claude and Codex reviewers assessed every bundle. A Claude judge matched candidates against sealed keys while blinded to reviewer family.

| Reviewer | All cases | Excluding three weak keys |
|---|---|---|
| Claude | 17 of 17 | 14 of 14 |
| Codex | 13 of 17 | 13 of 14 |

Reported Wilson intervals are 0.82 to 1.00 and 0.53 to 0.90 for all cases, and 0.78 to 1.00 and 0.69 to 0.99 after exclusions. These assume independent trials and are not cluster-adjusted population recall intervals.

Weak keys 64083, 64693 and 65044 involve an owner attacker, no demonstrated outside attacker, or an informational classification.

Candidate matching is not executable confirmation. It concerns those lists, not a future campaign with different tools or context. Training exposure remains possible.

The judge’s statement that the full 63008 theft depends on H-02 is superseded by executable evidence: the attack remains when H-02 alone is corrected.

### 5.10 PoV-guided repair

The extension starts from a validated vulnerable implementation. A shown PoV supplies executable evidence. Hidden attacks use different states, boundaries or call sequences.

Success requires compilation, preserved legitimate behavior, blocked frozen attacks and no confirmed new attributable vulnerability under the declared evaluation. Required unresolved checks prevent success.

Later discoveries are reported separately and replayed consistently. Passing the shown PoV is insufficient.

### 5.11 Worked example: finding 63008

The pilot concerns the downward tick iterator in Sorella L2 Angstrom. The vulnerable implementation skips a starting boundary.

Version 2 of `evidence/63008/` contains violation tests, fixed-state assertions, a body-only patch, an independent H-02 patch and an outcome-checking runner.

The correction adds `self.currentTick = startTick + 1` after the empty-range early return in `reset(TickIteratorDown)`. It preserves empty-range behavior and changes no signature, storage layout or other function.

Fixed-state checks establish that the honest provider can claim its entitlement and withdraw principal, backing covers liabilities, and attacker rewards do not exceed its share of its own swap tax. That share formula is specific to the two-position scenario.

| Code state | Violation tests | Fixed-state tests | Original suite |
|---|---|---|---|
| Vulnerable `386baff` | Violation observed in both | Both fail | 60 pass |
| Version-2 correction | Violation absent in both | Both pass | 56 pass, 4 fail |
| H-02 correction only | Violation observed in both | Both fail | 60 pass |
| Both corrections | Violation absent in both | Both pass | 56 pass, 4 fail |

The four remaining failures assert the old boundary behavior. Empty-range tests pass in every state. The runner excludes package-added tests from original-suite counts and matched all 12 expected outcomes.

On vulnerable code, the honest provider is owed about 49 ether. The attacker receives 48.99999755 ether. Remaining backing is about 0.0245 ether against about 49.0245 ether owed. Claims and withdrawal revert.

With the correction, the honest provider receives 49.000012243878672857 ether and withdraws principal. The attacker receives 0.024487756121327142 ether, its calculated share of its own swap tax.

H-02 correction `cd0ac3c` alone leaves the attack unchanged.

The capital record gives the attacker ceilings of 100 ether and \(10^9\) tokens. The attack position is about \(2\times10^{25}\) liquidity units. The scenario uses a 5 gwei priority fee and assumes the attacker wins the relevant top-of-block swap. It does not simulate a competitive auction.

The original capital run records swap tax 0.0245 ether, just-in-time tax 0.098 ether and vulnerable-code net profit 48.877274256875928055 ether. Version 2 reruns reward and withdrawal assertions, not the separate net-profit test.

Automated version-2 work took 598 seconds. This is not human construction or adjudication time.

The repository contained a `CLAUDE.md` before the faulty commit. The baseline is historical developer code.

The two added control-group flaws failed repository functional tests. They motivate reporting K but do not establish an added-flaw rate for D.

## 6. Research questions and evaluation plan

### 6.1 Research questions

**RQ1b, proposed principal:** How do agents and historical developers differ in detected vulnerability among working implementations, standardized across the constructible strata?

**RQ1a, secondary:** How much does restricting analysis to audit-flagged functions change that comparison?

**RQ4, validation:** How does discovery behave across authors, strata and known flaw patterns, and how do missed flaws affect interpretation?

**RQ2, extension:** Does executing wrong assertions affect retention of an endorsed vulnerability differently from retention of a matched ordinary error?

**RQ3, optional extension:** How does request wording affect vulnerability reproduction within a task?

### 6.2 Outcomes and unresolved results

Let \(C\) indicate compilation, \(L\) passing the final primary ordinary suite, and \(V_{\mathrm{own}}\) a vulnerability confirmed through the implementation’s own campaign.

\[
W=CL,\qquad D=WV_{\mathrm{own}},\qquad K=CV_{\mathrm{own}}.
\]

All scheduled attempts on constructed tasks remain recorded. Historical code contributes one implementation per function.

Within stratum \(s\),

\[
d^D_s
=
w_{As}v_{As}-w_{Hs}v_{Hs}
=
(v_{As}-v_{Hs})
+(w_{As}-1)v_{As}
+(1-w_{Hs})v_{Hs}.
\]

Here \(w\) is the working rate and \(v\) is detected vulnerability conditional on working. The first term is the security component. The rest is the functional-failure component.

This is a descriptive identity. Working outputs can have different function mixtures across authors. A negative D difference alone is not a better-security verdict.

Each implementation has admissible \((W,D)\) pairs:

- known functional failure: \((0,0)\);
- known working and confirmed vulnerable: \((1,1)\);
- completed working campaign without confirmation: \((1,0)\);
- working with unresolved security: \((1,0)\) or \((1,1)\);
- unknown working status: every pair consistent with observed checks.

The general set is \(\{(0,0),(1,0),(1,1)\}\). Security confirmation does not erase uncertainty about functionality.

For each author and stratum, minimize and maximize the weighted conditional rate over admissible completions. Unknown working status affects numerator and denominator.

If any admissible completion has a zero working denominator, no directional conditional-security claim is made for that comparison. D, W and their bounds are still reported.

For defined rates,

\[
d^{S,L}_s=v^L_{As}-v^U_{Hs},
\qquad
d^{S,U}_s=v^U_{As}-v^L_{Hs}.
\]

The same historical observations are shared across configurations. Inference preserves that dependence.

### 6.3 RQ1b: estimator, operating limits and inference

#### Domain and estimator

Let \(U_B=\{i\in U:B_i=1\}\) be the constructible domain in the frozen eligible frame.

Each function contributes equal total weight before conditioning on working status. Agent observations are averaged within function; historical code contributes one observation.

With inverse joint inclusion weight \(a_i\),

\[
\widehat T_{sB}=\sum_{i\in S_s}a_iB_i,
\qquad
\widehat\pi_{sB}
=
\frac{\widehat T_{sB}}{\widehat T_{VB}+\widehat T_{NB}},
\]

\[
\widehat w_{as}
=
\frac{\sum_{i\in S_s}a_iB_i\overline W_{ai}}
{\widehat T_{sB}},
\qquad
\widehat v_{as}
=
\frac{\sum_{i\in S_s}a_iB_i\overline D_{ai}}
{\sum_{i\in S_s}a_iB_i\overline W_{ai}},
\]

\[
\widehat\Delta^S_{Bc}
=
\sum_s\widehat\pi_{sB}
(\widehat v_{A_cs}-\widehat v_{Hs}).
\]

This is a standardized difference between conditional rates. It is not an unstratified rate difference or a paired count of introduced flaws.

The companion D difference is

\[
\widehat\Delta^D_{Bc}
=
\sum_s\widehat\pi_{sB}
(\widehat w_{A_cs}\widehat v_{A_cs}
-\widehat w_{Hs}\widehat v_{Hs}).
\]

All totals, shares and ratios are recomputed in uncertainty replicates.

#### Directional decisions and intervals

A positive claim uses the lower identification bound. A negative claim uses the upper bound. Holm adjusts across the two configurations.

The candidate uncertainty procedure is a delete-one-protocol jackknife with inverse-inclusion weights. Calibration is needed; its factor alone does not establish validity for unequal-probability sampling.

The interval is

\[
[
\widehat L-c\,t_{0.975,P-1}\widehat{\mathrm{se}}(\widehat L)-z_H,\quad
\widehat U+c\,t_{0.975,P-1}\widehat{\mathrm{se}}(\widehat U)+z_{A_c}
].
\]

When an author has no detected flaw in a stratum, the widening term adds that stratum’s estimated constructible share times

\[
1-0.025^{1/n},
\]

where \(n\) is the number of resolved working implementations for that author and stratum.

This is a binomial-based widening adjustment. It is not an exact bound for weighted, clustered observations. Its support comes from combined simulation. The directional decision does not use these terms.

An interval is undefined if any required bound, standard error or widening term is nonfinite. Such cases count as coverage failures in validation. They receive no directional claim.

The marginal coverage target is 0.95 for each configuration’s true contrast. Directional family-wise error must be at most 0.05. Neither marginal coverage nor extension of both estimated endpoints implies simultaneous coverage of all population identification bounds.

Original-frame bounds treating unbuilt tasks as unknown remain secondary.

#### What V33 establishes

V33 uses 24 fixed simulated frames based on both strict count lists. Frames combine three recall patterns, two historical N rates and two construction settings. Each has 200 protocols.

Construction is fixed once per function and can depend on difficulty. Protocols are sampled without replacement by randomized systematic sampling. Truth is set exactly on the constructible frame.

Calibration uses 2,000 studies per frame and condition. Validation uses 4,000 fresh studies. Selection uses one-sided Clopper–Pearson bounds with Bonferroni adjustment over the actual checks. There is no fallback if no candidate passes.

For 22 protocols with one V and six N functions, V33 selects Holm level 0.03 and multiplier 1.175.

Its validation error upper bound is 0.0386 over 216 null checks. Its marginal-coverage lower bound is 0.9581 over 1,008 checks. Power bounds use 384 checks at +0.15.

| Unresolved share: agents, historical | Lowest +0.15 power | Lower bound |
|---|---:|---:|
| 0, 0 | 0.747 | 0.721 |
| 0.005, 0.005 | 0.701 | 0.674 |
| 0.0075, 0.0075 | 0.685 | 0.658 |
| 0.0075, 0 | 0.743 | 0.717 |
| 0, 0.0075 | 0.678 | 0.651 |
| 0.013, 0.013 | 0.611 | 0.583 |
| 0.013, 0 | 0.732 | 0.705 |
| 0, 0.013 | 0.644 | 0.616 |

These are minima, not typical performance. The earlier 20-protocol design fails the 0.60 requirement at 0.0075 in both authors, with lower bound 0.575.

The preferred design’s lowest +0.10 power is 0.395 without unresolved outcomes and 0.267 at 0.013 in both authors.

Negative targets are half the lowest attainable contrast in each frame, capped at −0.05. They range approximately from −0.045 to −0.011. The value −0.05 itself is attainable in eight frames, but the simulated negative targets do not reach it. Power is very low for these small negative differences.

V33’s published undefined-share diagnostic omits the widening terms. Coverage already uses them. The corrected diagnostic is **[pending]**.

#### What V34 adds

V34 keeps the V33 procedure frozen and uses 2,000 fresh studies per frame and condition. It examines higher historical unresolved rates.

| Unresolved share: agents, historical | Lowest +0.15 power | Bonferroni lower bound |
|---|---:|---:|
| 0, 0.02 | 0.595 | 0.555 |
| 0, 0.03 | 0.493 | 0.454 |
| 0, 0.065 | 0.222 | 0.190 |
| 0.0075, 0.02 | 0.563 | 0.523 |
| 0.0075, 0.065 | 0.210 | 0.179 |

The lower bounds adjust over 240 power checks.

At the exact nulls, the worst reported error point estimates range from 0.004 to 0.018, and lowest marginal coverage from 0.985 to 0.995. These are point estimates, not newly calculated confidence-bound passes. V34 does not recalibrate.

The results show why the pooled development limit was inadequate. They do not establish that historical missingness will be low.

#### Structurally different readiness rule

The development-based unresolved-rate confidence gate is withdrawn. There is no threshold of 214 or 216 resolved outcomes and no extension to 399 outcomes after a failure.

Development has a fixed set of three cases selected before their outcomes. It tests blindness, task construction, executable evaluation, adjudication, stage costs and failure recording. It does not certify population unresolved rates.

Before main sampling, the study must validate an author-specific operating region. Its axes are \(u_{A_1}\), \(u_{A_2}\) and \(u_H\). No author borrows another author’s denominator. No pooled limit is placed on an author as if it bounded that author’s rate.

The region states where the proposed minimum power of 0.60 at +0.15 holds under named unresolved-outcome mechanisms. Its boundaries are **[pending]**.

Launch requires:

- committee approval of this conditional-power approach;
- validated error and coverage across the retained robustness conditions;
- a nonempty, explicitly reported operating region meeting the approved power requirement;
- a feasible fixed reservation schedule;
- completed human development requirements.

This is a departure from the earlier requirement to derive unresolved-rate scenarios from development confidence limits. It does not depart from keeping adverse bounds primary.

The launch statement will say that useful power is conditional on the stated region. It will not say that development proves the main study will remain inside it.

#### Monitoring a fixed main sample

The full main sample is drawn before evaluation. Monitoring occurs after each protocol’s scheduled work is locked.

The record reports unresolved counts and shares separately for historical code and each configuration, and by stratum. It also reports inverse-inclusion-weighted shares with equal total weight per function. These observed shares are diagnostics, not confidence bounds for future outcomes.

A departure from the operating assumptions is flagged. It does not trigger:

- replacement of a protocol or function;
- additional agent attempts;
- transfer of another implementation’s allowance;
- selective resolution work;
- early success stopping;
- removal of adverse bounds;
- a new endpoint or target population.

Every sampled protocol retains its scheduled work and allowance. If a common resource failure prevents completion, remaining scheduled evaluations stay in the record as unresolved or as documented procedure failures. They are not replaced.

Final estimates and intervals are reported for the fixed sample whether or not monitoring flags a departure. Error and coverage validation must therefore be unconditional on the monitoring result.

If the observed process falls outside the validated operating conditions, the report states that the planned power claim no longer applies. It reports the actual bounds and uncertainty. It does not manufacture a power estimate from observed effects or reinterpret an inconclusive result as equal security.

A directional claim still requires the frozen inferential procedure and its stated error-control domain. If a departure lies outside that domain, the result is reported without a validated directional claim. It is not repaired by changing the analysis after seeing outcomes.

#### Required simulation before launch

The combined check must separate the three authors’ unresolved probabilities. The initial grid is

\[
u_{A_1},u_{A_2},u_H\in\{0,0.005,0.0075,0.013\}.
\]

Additional checks use historical rates \(0.02,0.03,0.065\), with each agent rate independently set to 0 or 0.0075.

Retain exact global nulls, both partial-null assignments of 0 and +0.10, exact +0.10 and +0.15, and the defined feasible negative alternatives.

Missingness mechanisms are:

1. independent indicators;
2. shared task-level indicators, including repeated attempts;
3. shared protocol-level indicators;
4. difficulty-dependent probabilities using link 0.6 and calibrated author-specific marginal rates.

The same strict count, construction and recall scenarios remain. The procedure must retain uncertain working status and recompute domain shares and ratios.

Assess the frozen V33 settings first. If they fail, use a separate calibration stream and select one procedure over all retained conditions. Validate on fresh draws. Save every frame and condition.

Use adjusted binomial upper bounds for error and lower bounds for coverage and power. Undefined intervals count as failures. No fallback grid endpoint is permitted.

Report the largest downward-closed passing regions on the tested grid. This means all tested rate vectors no larger in any coordinate also pass. It does not establish performance at untested rates or mechanisms. Choose and freeze one operating region before collection.

Operating limits, robust error and coverage bounds, and power minima are **[pending]**.

### 6.4 RQ1a: secondary design comparison

\[
G^S_c
=
d^S_{Vc}-\Delta^S_{Bc}
=
(1-\pi_{VB})(d^S_{Vc}-d^S_{Nc}).
\]

The analogous D difference and functional-failure component are reported beside it.

Bounds retain the covariance between the V-only and standardized estimates. Replicates recompute shares and ratios.

V27 gives earlier planning half-widths:

| Earlier allocation | RQ1a on D | Security component |
|---|---:|---:|
| 20 protocols, two V, six N | 0.296 | 0.338 |
| Same allocation, observed-fix counts | 0.395 | 0.422 |
| 24 protocols, two V, four N | 0.301 | 0.294 |
| 17 protocols, two V, eight N | 0.326 | 0.357 |

These are not results for the proposed allocation. They assume complete construction and resolved outcomes.

For the earlier 20-protocol allocation, the security interval excludes −0.10 in 0.81 and 0.86 of studies at displayed truths −0.56 and −0.57. At −0.46 the rate is 0.61. Observed-fix counts give rates 0.73 and 0.70 at −0.56 and −0.58.

There is no general detectable-distortion threshold of 0.5.

The proposed allocation has fewer V functions per protocol and more protocols. Its RQ1a precision is **[pending]**; no ordering relative to V27 is asserted.

A material negative distortion requires a validated interval wholly below −0.10. Positive claims require corresponding validation. Otherwise the result is inconclusive. There is no “little difference” interpretation.

### 6.5 Detection sensitivity

Let \(r_{as}\) be the detected rate among working implementations and \(\rho_{as}\) an assumed sensitivity among truly vulnerable working implementations.

With negligible false confirmations,

\[
v^{\mathrm{latent}}_{as}=r_{as}/\rho_{as},
\]

restricted to feasible rates.

\[
\Delta^{S,\mathrm{latent}}_{Bc}
=
\sum_s\pi_{sB}
\left(
\frac{r_{A_cs}}{\rho_{A_cs}}
-
\frac{r_{Hs}}{\rho_{Hs}}
\right).
\]

The latent design difference is

\[
G^{S,\mathrm{latent}}_c
=
(1-\pi_{VB})
(d^{S,\mathrm{latent}}_{Vc}-d^{S,\mathrm{latent}}_{Nc}).
\]

D sensitivity additionally includes working rates. These are distinct analyses.

For a stratum with positive detected rates, the sign-reversal boundary is \(\rho_A/\rho_H=r_A/r_H\). No numerical reversal threshold is claimed before observing rates.

The older latent difference near −0.47 concerns D, not the conditional security component.

Audit rediscovery, audit-missed cases, seeded recall and natural investigation describe different validation populations. Transfer to main-study natural sensitivity is an assumption.

The primary sensitivity display retains full feasible ranges. Restricted ranges state their assumptions. If plausible ranges reverse the latent comparison, its sign is not identified.

Challenges to positives trigger consistent re-adjudication rather than selective changes for one author.

### 6.6 Planned extension: faulty assertions and PoV-guided repair

The extension has a separate sample, budget, preregistration and validation. It receives no student hours in the protected year.

Within tasks, it varies correct versus incorrect assertions, permission to execute repository tests, and security versus matched ordinary assertions.

Within assertion type, execution arms see the same source and contrary evidence. Both receive identical read, search, edit and fixed-build tools. Only one receives the repository-test tool. There is no unrestricted terminal.

Tools restore fixed settings outside the writable workspace. Enforcement checks include scripts, renamed tests, configuration edits and instrumentation.

Security arms receive the same shown PoV and rerun tool. Ordinary arms receive a matched failing check from the specification. Hidden evaluation remains inaccessible.

The common primary outcome is retention of the behavior endorsed by the wrong assertion. Vulnerability retention remains a separate security endpoint.

Pairs require the same target function, comparable correction size and a recorded comparison of conflict with the supplied evidence. Failed admissions remain recorded.

With \(I_k\) the log-odds interaction of wrong assertions and execution for type \(k\),

\[
\theta=I_{\mathrm{security}}-I_{\mathrm{ordinary}}.
\]

Equal interactions define a modeling null, not a theorem about test-obeying agents. Conditional generating interactions and aggregated-probability interactions differ.

V14 uses 20 protocols, three attempts per cell and 1,000 studies per row. Equal-interaction rejection rates are 0.040–0.067. At 160 functions, displayed alternative rates are 0.529–0.812.

A confirmatory extension must align estimator and estimand, calibrate unequal baselines and heterogeneous effects, and choose a meaningful target. The 160-function size remains a candidate.

Availability and admission costs are unknown. Both configurations are protected. Broader claims require consistent direction and validated multiplicity control.

### 6.7 Natural tests and optional extensions

Natural faulty tests require semantic confirmation. Passing on vulnerable code and failing on a correction is only a screen.

A census is attempted only if measured costs permit. Otherwise the study estimates the weighted share in the assessed V sample, retaining unresolved cases.

Natural cases are descriptive and do not enlarge the injected experiment statistically.

Other extensions include broader request wording, pilot configurations, SolAgent and multi-function replacement. They require separate funding and cannot change primary labels.

### 6.8 Threats to validity

Historical snapshots do not recreate original development. AI provenance and exposure markers are incomplete.

Post-cutoff subsets are reported where available. The recall flag covers distinctive fixes and reproduction of historical bodies in both strata. Its planned normalized-token threshold is 0.9, frozen after development checking. Flagged-case exclusion analyses are secondary.

Equal discovery procedures do not establish equal sensitivity. Working outputs can differ in composition across authors. Blind properties may omit behavior.

Builder identity, exposure and order are recorded. First-half and second-half estimates are compared without claiming to remove protocol confounding.

Accessible audits and public fixes restrict the population. Fixed construction allowances define the domain and can select on difficulty.

V33 validates a planning model, not every real failure mechanism. V34 demonstrates substantial power loss under higher historical missingness. The revised author-specific robustness check is pending.

Monitoring does not establish that latent failure probabilities equal observed shares. Development does not certify rare failures.

The lower power requirement and changed readiness rule need committee approval. Neither passing tests nor absence of confirmed flaws establishes deployment safety.

## 7. Related work

The contribution is a probability-defined historical comparison of detected security in Solidity replacements, supported by executable attribution and explicit detection limits.

SolEval supplies a close function-body generation setup but uses Slither for vulnerability measurement [SolEval]. Sajadi et al. and Cotroneo et al. already compare human and generated code without selecting only historical failures [Patch Security; Cotroneo].

SecureVibeBench provides reconstructed tasks and common PoVs [SecureVibeBench]. EVMbench supplies executable Solidity evaluation [EVMbench]. PoCo supplies audit-derived exploit construction, which remains secondary here [PoCo].

Sampling bias itself is not the novelty. RQ1a is secondary because examined designs did not meet its earlier precision promise. The principal empirical comparison must be judged with its reduced power and conditional operating assumptions.

Fault-enforcing tests are an existing construct [Fault-Enforcing Tests]. ImpossibleBench manipulates conflicting tests and execution feedback [ImpossibleBench]. ExecCritic addresses tests encoding incorrect targets [ExecCritic]. Calibration, Not Compilation reports harmful test feedback [Calibration]. SpecGuard shows that satisfying corrupted tests can remove a defense [SpecGuard].

The repair extension must establish the matched security-versus-ordinary contrast, not rely on Solidity alone.

| Work | Closest overlap | Difference addressed here |
|---|---|---|
| SolEval | Solidity function-body generation | Historical comparison with executable attribution |
| Cotroneo et al. | Human and AI functions paired by documentation | Probability sampling and executable attacks |
| Sajadi et al. | Human and agent patches on common issues | Flagged and unflagged Solidity function replacement |
| SolAgent | Solidity generation and historical comparison | Executable outcomes rather than static warnings |
| SecureVibeBench | Historical vulnerabilities and common PoVs | Unflagged sampling and own-campaign labels |
| SusVibes | Functional and security outcomes | A domain beyond historical failures |
| Foresight-SWE | Tasks associated with historical defects | Security attribution and unflagged functions |
| EVMbench | Solidity detection, patching and exploitation | Historical replacement and population comparison |
| PoCo | Audit-derived exploit generation | Secondary audit-assisted evaluation |
| P2Patch and PatchBench | Exploit-guided repair | Matched faulty-assertion extension |
| Fault-Enforcing Tests | Tests preserving faults | Matched experimental comparison |
| ImpossibleBench | Conflicting tests and execution | Matched endorsed outcomes and contrary evidence |
| SpecGuard | Corrupted tests removing defenses | Separately calibrated matched contrast |
| ExecCritic | Incorrect tests and frozen validation | Repository assertions during PoV-guided repair |
| Calibration, Not Compilation | Harmful test feedback | Executable attacker outcomes |

Foresight-SWE is under review. Claims are limited to its verified abstract.

## 8. Feasibility, risks and fallback plans

### Measured evidence and student preconditions

The automated timing record is `evidence/timings.md`.

| Work | Automated wall-clock time |
|---|---:|
| Original 63008 package | 1,373 seconds |
| Version-2 package | 598 seconds |
| Classification of 43 pilot fixes | 864 seconds |

These are not measurements of human construction, confirmation, adjudication or auditing. The frame audit also used agent readers.

The student has committed to undertake development and personally time at least one case. The dated commitment and completed timed case are not yet available.

Before resubmission, the committee requires both. The case includes probability-selected N functions and retains failures. The complete three-case record remains a launch requirement.

### Fixed development design

Select three development protocols before their outcomes. Each case samples up to one V and six N functions, using the main eligibility and sampling rules. Each constructed function receives one historical implementation and two attempts from each configuration.

The initial case list is fixed. A small stratum or construction failure reduces the number evaluated. It does not authorize replacement tasks.

There is no minimum count of resolved outcomes. There is no retry or extension triggered by an unresolved outcome.

A required step performed by an exposed or otherwise ineligible person is a deviation. It cannot count as a valid demonstration of the intended blind procedure.

### One capped development schedule

This schedule replaces the allowance table in the development kit. Allowances are maximum student time, not estimates of adequate effort.

| Stage | Student cap | Included work and stopping rule |
|---|---|---|
| Protocol preparation | 9 hours per case | Threat model, environment preparation and ordinary protocol setup; failure is recorded when the cap is reached |
| Construction | 2.25 hours per sampled function | Request, properties, ordinary checks, reachable setup and checklist; includes failed construction |
| Campaign operation | 0.15 hours per scheduled implementation | Generation supervision where applicable, fuzzing and reviewer operation |
| Confirmation and primary record | 0.178 hours per scheduled implementation | All candidate confirmation, body correction, packaging and lock administration share this cap; at most three candidates |
| Audit-assisted work and secondary packaging | 3.75 hours per case | At most the one constructed V function, plus scheduled secondary replay and case packaging; incomplete secondary work is recorded |
| Case-level preparation and administration outside these stages | Within the remaining month-one reservation | Exposure records, timing setup, gate administration and coordination; no unrecorded borrowing |

Thus the maximum case allocation uses

\[
9+7\times2.25+7\times5\times0.328+3.75
\]

student hours. The three cases use three times that expression. This is within the 150-hour month-one reservation at these planning caps.

The remaining month-one time is reserved for common administration and discovery-gate work. If it is insufficient, the unfinished named activities move to the explicit month-two ledger before launch. They do not enlarge a case’s construction or campaign caps.

Paid mapping and adjudication are separate from student time. Before the first case, the paid ledger assigns fixed source budgets for development, main work, duplicate requests, seeds, controls and audit-assisted packages.

For each adjudicator, the sum cannot exceed 121 hours. Within each source, divide its reserved hours by the maximum number of scheduled implementations that can produce packages. All packages from one implementation share its review reservation. The resulting per-implementation cap is fixed before that source begins.

This formula defines a finite cap without inventing an unmeasured review cost. If the resulting cap is too small for valid decisions, the plan fails its operational check. Development cannot use a larger review allowance and then claim to have tested the main one.

The earlier 0.5-hour-per-package figure remains a workload assumption only. It is not an additional entitlement.

Paid construction and mapping use the shared 220-hour ceiling. Their source reservations must be fixed before development. The investigator ceiling remains 120 hours.

The kit must record the same caps and failure rules. Its prior per-candidate confirmation allowance and audit work on two V functions are withdrawn.

### Main allocation and cost

The preferred allocation remains 22 protocols with one V and six N functions.

| Allocation | Earlier cost per protocol: low, middle, high | Middle total |
|---|---|---:|
| 22 protocols, one V, six N | 24.7, 40.0, 57.1 hours | 880 hours |
| 20 protocols, two V, six N | 27.0, 43.9, 62.8 hours | 877 hours |
| 24 protocols, two V, four N | 22.4, 36.1, 51.4 hours | 866 hours |
| 17 protocols, two V, eight N | 31.6, 51.6, 74.3 hours | 878 hours |

These are planning calculations using V22 rates and one audit-assisted task per protocol. They do not demonstrate human adequacy.

The preferred middle expression is

\[
22(9+7\times2.25+35\times0.328+3.75),
\]

reported as 880 hours.

The student ceiling is 1,800 hours over twelve months, assuming no coursework or teaching. Reduced availability requires a revised plan.

Months 3–9 contain 1,050 hours. Seeded operation reserves 120 and duplicate-request work reserves 30, leaving 900 for main protocols.

The maximum main reservation must satisfy

\[
P[
h_{\mathrm{setup}}
+(V_{\max}+N)h_{\mathrm{build}}
+5(V_{\max}+N)h_{\mathrm{campaign}}
+h_{\mathrm{audit}}
]\leq900.
\]

Unused time is not transferred according to discovered flaws or unresolved outcomes.

### Duplicate requests and paid work

Duplicate campaigns and coordination must satisfy

\[
15\times5\times h_{\mathrm{campaign}}
+
H_{\mathrm{duplicate\ coordination}}
\leq30.
\]

Construction and adjudication enter their paid ledgers. Compute is separate.

Paid ceilings are:

- 121 hours for each of two adjudicators;
- 120 hours in total for natural investigation;
- 220 hours in total for unexposed construction, mapping and validation support.

Every potential package source must be included before work starts. Missing required decisions remain unresolved. No source may assume it can reuse another source’s reservation.

Compute requires a separate funded ceiling from measured use and current prices. Native-agent costs remain unpriced.

### Quantity ledger

| Work | Quantity |
|---|---|
| Development | Three fixed cases using the main task and attempt design |
| Main construction | All sampled V and N functions, including failures |
| Main generation | Four attempts per constructed function across the two configurations |
| Main discovery | Historical campaign and all scheduled agent campaigns |
| Confirmation | Candidates within each implementation’s fixed cap |
| Adjudication | Required independent decisions within fixed source reservations |
| Seeded validation | 60 planned pairs, controls and campaigns |
| Duplicate requests | 15 functions and up to \(15\times5\) added campaigns |
| Natural investigation | Up to 48 first assessments and 12 duplicates |
| Audit-assisted work | At most one constructed V task per selected protocol |
| Audit-missed validation | Target 10–20 cases if available |
| Replay and release | All scheduled eligible artifacts within their stage accounts |

The pilot candidate rates 8/64 and 3/13 remain workload sensitivity inputs, not guarantees of confirmation capacity.

### Monthly schedule

| Month | Work | Student limit |
|---|---|---:|
| 1 | Fixed development cases, timing, exposure records and reserved gate administration | 150 hours |
| 2 | Remaining named preparation, frame freezing, full reservation check, operating-region validation and preregistration | 150 hours |
| 3–9 | Fixed main sample, seeded operation and duplicate requests | 1,050 hours |
| 10 | Secondary analysis, validation interpretation, sensitivity and disclosure | 150 hours |
| 11 | Writing and submission preparation | 150 hours |
| 12 | Artifact release and disclosure follow-up | 150 hours |

Before launch, month two must have a task-by-task ledger within its limit. It is not an open reserve for repeated development attempts.

The repair extension receives no student hours in this year.

### Launch and completion rules

Launch requires committee approval of the principal estimand, lower power requirement and changed readiness rule.

It also requires a frozen frame, complete human development record, funded staff, feasible stage reservations, validated inference and a published author-specific operating region.

No development confidence limit on unresolved outcomes is required or claimed. Development failures may still show that a stage cannot be performed validly within its allowance. That is an operational failure and prevents launch.

A changed allowance or procedure requires review and validation before main sampling. Failed development records remain visible.

Once the main sample is drawn, it is fixed. Monitoring cannot change its size, composition, attempts, allowances or primary endpoint.

An exceeded operating region means the planned power statement may not apply. The full sample, bounds and uncertainty are still reported. An inability to complete the prescribed study is reported as such, not rebranded as a successful substitute.

### Remaining risks

| Risk | Response |
|---|---|
| Fixed stages cannot support valid work | Do not launch under those caps |
| Construction yield is uncertain or low | Retain conservative limits and failures |
| Shared failures create unresolved clusters | Validate explicit shared-failure models |
| Historical missingness exceeds agent missingness | Use separate author rates and bounds |
| Main monitoring leaves the operating region | Retain the sample and analysis; report the lost power assurance |
| Required adjudication is unavailable | Record unresolved outcomes; do not count positives |
| Frame classifications change | Settle them before freezing probabilities |
| Audit information enters primary work | Record the breach and keep audit-assisted outcomes secondary |
| Inference fails robust validation | Recalibrate before collection or do not launch |
| Committee rejects conditional readiness | Submit a different reviewed design |
| New deployed exposure is found | Follow disclosure restrictions |
| Extension resources are unavailable | Defer the extension |

## 9. Ethics and responsible disclosure

All attacks run offline with local assets. Generated implementations are never deployed.

Each finding receives a release record covering public status, known fixes and deployed or forked exposure. A public audit does not establish that exposure has ended.

New findings are reported through the protocol’s security contact or bounty process. Exposure is reviewed again at 90 days. Exploit details remain embargoed while a known deployment is exposed.

Submission does not override disclosure restrictions. Aggregate methods and results may be published while affected artifacts remain withheld.

Seeds stay in local copies. Released seeds are clearly marked and never submitted as real findings.

Independent reviewers are paid. Institutional requirements are checked before recruitment. LLM assistance is recorded separately from human adjudication.

Released material excludes credentials, private endpoints and restricted material. The artifact supports research reproduction, not autonomous live exploitation.

## 10. Target venues and twelve-month timeline

Paper 1 targets ICSE, with FSE as a backup. Its proposed principal result is the conditional historical comparison, accompanied by functional outcomes, detection validation and the secondary design comparison.

A security venue is considered only if confirmed findings and evidence support a distinct security contribution.

The repair extension would target FSE or ISSTA after the protected year, with separate resources and validation.

| Months | Milestone |
|---|---|
| 1 | Complete fixed human development cases and timing |
| 2 | Freeze frame, reservations, operating limits and inference; decide launch |
| 3–9 | Execute the fixed probability sample |
| 10 | Complete secondary analysis, sensitivity and disclosure review |
| 11 | Prepare paper 1 if the required evidence is complete |
| 12 | Release eligible artifacts and continue disclosure |

Official deadlines will be checked. The schedule does not guarantee acceptance.

The study is not ready for confirmatory collection. The dated commitment and first timed case remain committee preconditions for resubmission. The pending robustness validation is a separate requirement.

## Appendix A. Simulation history

| Version | Purpose | Current interpretation |
|---|---|---|
| V10 | Earlier inference, repair power and seeded precision | Seeded precision remains relevant |
| V11–V13 | Design comparison and unresolved outcomes | Historical planning evidence |
| V14 | Matched repair outcome | Extension planning evidence |
| V15–V20 | Allocation, attempts and construction | Superseded main count assumptions |
| V21–V23 | Modeled-count allocation | Superseded principal evidence; V23 aggregation defect acknowledged |
| V24 | Exact conditional-security targets | Older counts and limited missingness model |
| V25 | Finite frame and dependent construction | Older counts and simple random sampling |
| V26–V27 | Audited count pairs and allocation | Earlier allocations with favorable completion assumptions |
| V28 | Combined check | With-replacement sampling |
| V29 | Planned sampling and combined inference | Provisional settings failed validation |
| V30 | Confidence-bound calibration | Negative alternatives omitted from calibration; coverage failed |
| V31 | Every condition calibrated | Power failed; one design lacked a passing multiplier |
| V32 | Zero-detection adjustment and design screening | Cost labels corrected; no screening design passed |
| V33 | Full calibration and fresh validation | Supports the stated independent-missingness planning conditions |
| V34 | Higher historical unresolved rates | Demonstrates loss of power with the frozen V33 procedure |

V33’s zero-detection adjustment is binomial-based, not an exact bound for the study estimand.

The corrected undefined diagnostic includes all interval quantities. Its result is pending. The previous diagnostic examined only bounds and standard errors.

The next validation must report separate configuration and historical unresolved rates and shared-failure mechanisms. Existing results cannot be relabeled as that validation.

Scripts, inputs and results must be frozen together with their hashes. Default-result reproduction is provenance evidence, not validation of a new option.

## Appendix B. Factual answers

- **Eligibility:** Strict identities and body-only correction scope are reconciled. Semantic eligibility, severity and stated provenance checks remain before frame freezing.
- **Post-cutoff cases:** Unknown until models, dates and the final frame are pinned.
- **Platforms:** The audit sample covers recent Code4rena, Sherlock and Cantina records with downloaded findings, not every audit without a finding.
- **Named people:** Must be recorded in the dated staffing and funding plan.
- **Recall threshold:** Planned normalized-token threshold 0.9, frozen after development checking.
- **Candidate limit:** At most three, sharing one confirmation allowance.
- **Audit-missed cases:** Existing leads are not verified same-version missed flaws.
- **Natural investigation:** Small cells support descriptive checks, not precise sensitivity.
- **Empty strata:** Final validation retains undefined estimates. The corrected widening-term diagnostic is pending.
- **N counts:** Strict N totals 3,620 and ranges from 24 to 672 per audit.
- **Compute:** Current native-agent cost remains unpriced.
- **Agent ordering:** A secondary contrast between the two configurations.
- **Development:** Three fixed cases use the main allocation and attempt count. No zero-unresolved gate or outcome-triggered extension remains.
- **Operating limits:** Author-specific boundaries are pending. Development does not certify them.
- **Repair extension:** A separate later study with no protected-year hours.

## References

- **[Solidity Survey]** Solidity team. *Solidity Developer Survey 2025 Results*. 2026. https://soliditylang.org/blog/2026/04/15/solidity-developer-survey-2025-results/
- **[Web3Bugs]** Zhang et al. *Demystifying Exploitable Bugs in Smart Contracts*. ICSE 2023. https://github.com/ZhangZhuoSJTU/Web3Bugs
- **[SAST Study]** Li et al. *Static Application Security Testing Tools for Smart Contracts: How Far Are We?* FSE 2024. https://arxiv.org/abs/2404.18186
- **[SecureVibeBench]** Chen et al. *SecureVibeBench: Benchmarking Secure Vibe Coding of AI Agents via Reconstructing Vulnerability-Introducing Scenarios*. ACL 2026. https://aclanthology.org/2026.acl-long.1107/
- **[SusVibes]** Zhao et al. *Is Vibe Coding Safe? Benchmarking Vulnerability of Agent-Generated Code in Real-World Tasks*. ICML 2026. https://proceedings.mlr.press/v306/zhao26ax.html
- **[Foresight-SWE]** Anonymous authors. *Do Coding Agents Catch Their Own Bugs? (They Don’t)*. ICLR 2027 submission, under review. https://openreview.net/forum?id=rtJNEHQA79
- **[Patch Security]** Sajadi, Damevski and Chatterjee. *How Safe Are AI-Generated Patches?* Preprint, 2025. https://arxiv.org/abs/2507.02976
- **[Cotroneo]** Cotroneo et al. *Human-Written vs. AI-Generated Code: A Large-Scale Study of Defects, Vulnerabilities, and Complexity*. ISSRE 2025. https://arxiv.org/pdf/2508.21634
- **[SolEval]** Peng et al. *SolEval: Benchmarking Large Language Models for Repository-level Solidity Smart Contract Generation*. EMNLP 2025. https://aclanthology.org/2025.emnlp-main.218/
- **[SolAgent]** Chen et al. *SolAgent: A Specialized Multi-Agent Framework for Solidity Code Generation*. Preprint, 2026. https://arxiv.org/abs/2601.23009
- **[EVMbench]** Wang et al. *EVMbench: Evaluating AI Agents on Smart Contract Security*. ICML 2026. https://proceedings.mlr.press/v306/wang26k.html
- **[PoCo]** Andersson et al. *PoCo: Agentic Proof-of-Concept Exploit Generation for Smart Contracts*. Preprint. https://arxiv.org/abs/2511.02780
- **[P2Patch]** Iranmanesh et al. *P2Patch: Exploit-Guided Vulnerability Repair*. Preprint, 2026. https://arxiv.org/abs/2610.20245
- **[PatchBench]** Shen et al. *PatchBench: Evaluating AI Agents for Vulnerability Patching*. Preprint, 2026. https://arxiv.org/abs/2609.04075
- **[Fault-Enforcing Tests]** Charoosaei, Richter and Papadakis. *On the Risks of using LLM-Generated Tests for Regression Testing*. Preprint, 2026. https://arxiv.org/abs/2610.11835
- **[ImpossibleBench]** Zhong, Raghunathan and Carlini. *ImpossibleBench: Measuring LLMs’ Propensity of Exploiting Test Cases*. ICLR 2026. https://arxiv.org/abs/2510.20270
- **[ExecCritic]** Tao, Peng et al. *ExecCritic: Learn to Test, Test to Improve for Coding Agents*. Preprint, 2026. https://arxiv.org/abs/2609.09133
- **[SpecGuard]** Biyani et al. *SpecGuard: Proving a Task Is Broken Before the Agent Cheats*. Preprint, 2026. https://arxiv.org/abs/2610.09159
- **[Calibration]** Xu, Zeng, Paisley and Zhao. *Calibration, Not Compilation: Detecting and Repairing Misspecified Probabilistic Programs Written by Language Models*. Preprint, 2026. https://arxiv.org/abs/2606.31630
