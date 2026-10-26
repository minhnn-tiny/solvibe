## Status of R22.1 and R22.2

- **R22.1: partly resolved.** Section 6.3 restores a mandatory final-frame check, separate calibration and fresh validation, and a no-launch rule. However, its stated scenario set appears to restrict error and coverage validation to the power region. That narrows the protection supplied by V37.
- **R22.2: resolved.** Section 8 explicitly removes the three development protocols, defines the main target population on the remaining frame, and recomputes main inclusion probabilities there.

The added rebuttal paragraph matches the revision. The four checked SHA-256 hashes for the V37 and V38 scripts and text results match the manifest.

The kit’s stage caps, adjudication closing rules and end-of-development checks largely match v24. Its protocol-selection instructions still conflict with the proposal.

## Remaining issues

### R23.1 [Major] [C6] Keep the error-control domain separate from the power region

**Section:** 6.3, “Final check on the frozen frame.”

**Problem:** The rerun retains “every tested vector inside the frozen region.” This does not clearly retain the outside-region scenarios for error and coverage checks.

**Evidence:** V37 checks error and coverage across all 76 ordered vectors. Only the power requirement defines the smaller operating region. Section 6.3 still promises to report inference regardless of whether monitoring flags. The diagnostic can miss substantial departures, especially under protocol-wide failures.

A replacement procedure calibrated only inside the power region would not inherit V37’s outside-region error and coverage evidence. The earlier evidence also uses different frame counts.

**Required change:** Specify that final-frame calibration and fresh validation check error and coverage across all 76 ordered vectors under all four mechanisms, while requiring the +0.15 power threshold only inside the retained region, with Bonferroni counts recomputed for the actual checks.

### R23.2 [Minor] [C4, C6] The kit still instructs manual protocol selection

**Section:** `dev_case/README.md`, “Step 0,” the closing help list, and development decision step 1.

**Problem:** The student receives contradictory instructions about selecting development protocols.

**Evidence:** Step 0 says, “Choose a protocol whose audit findings you have not read.” The help list offers to pick candidate protocols. Later, decision step 1 requires three protocols drawn by probability sampling. V24 instead assigns an unexposed worker when necessary and prohibits replacement based on exposure.

Also, `sample_and_seal.py` samples functions within one supplied protocol. It does not draw the three protocols.

**Required change:** Replace the kit’s manual-selection instructions with the three-protocol sampling procedure from v24, identifying the protocol-level draw separately from function sampling and stating that exposure changes staffing rather than sample membership.

### R23.3 [Minor] [C4] Preserve the empty-sample rule in the kit

**Section:** `dev_case/README.md`, development decision step 7.

**Problem:** The abbreviated construction-warning rule omits the proposal’s explicit treatment of \(n=0\).

**Evidence:** V24 says that \(n=0\) makes the development record inadequate. The kit instead assigns an upper value of 1 whenever \(b=n\), which also includes \(b=n=0\). The later undefined-diagnostic rule should prevent launch, but the construction step itself does not match the proposal.

**Required change:** Add “If \(n=0\), the development record is inadequate and the study does not launch” before the kit’s upper-limit formula.

I found no other Blocking or Major issue in v24. The conditional construction assumptions, limited diagnostic sensitivity and descriptive treatment of RQ1a remain explicit. Item 10 is excluded from this vote.

DISAGREE: [R23.1]