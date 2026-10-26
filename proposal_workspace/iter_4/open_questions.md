# Open questions for the committee, iteration 4

The two authors agreed on this version (proposal version 25). The questions below are decisions that only the committee can make, or facts the committee should weigh. Please answer each one in your review.

## OQ1. The student's commitment and timed case (iteration-3 meta-review, item 10)

The iteration-3 area chair required, before acceptance, a written commitment from the student with dates, and one development case timed by the student.

Status on 2026-10-23: the student has said they will do the timed case (an answer given on 2026-10-22). The written commitment with dates (`proposal_workspace/dev_case/commitment.md`) and the timesheet (`proposal_workspace/dev_case/timesheet.csv`) are still empty. The kit for the case is in `proposal_workspace/dev_case/` (instructions in `README.md`; protocol draw in `draw_protocols.py`; function draw in `sample_and_seal.py`).

Question: apart from item 10, does the proposal meet the bar for your score? If item 10 were supplied and showed the stated caps to be workable, what score would you give?

## OQ2. Changes the authors request to earlier committee decisions

The proposal asks the committee to approve four changes to decisions made in iterations 2 and 3. Section 3 ("Requested changes to the committee's design decisions") states each one and its reason.

1. **Principal estimand.** RQ1b (the standardized difference in detected vulnerability among working implementations, agents minus historical code) becomes principal. RQ1a (the flagged-only comparison) becomes secondary and descriptive. The iteration-3 area chair had kept RQ1a principal.
2. **Power requirement.** The minimum is correct-direction power of 0.60 at an exact +0.15 difference, inside a stated region of unresolved-outcome rates, in place of 0.80.
3. **Readiness for unresolved outcomes.** Development no longer certifies low unresolved rates with a confidence limit. Instead, simulations fix a region of author-specific unresolved rates in which the power requirement holds, and a fixed diagnostic reports evidence of leaving it. Adverse bounds stay in the principal analysis, as the iteration-3 area chair required.
4. **Construction yield.** The launch gate based on a lower confidence limit for construction yield is replaced by descriptive yields and a warning rule, because three development cases cannot certify a yield.

Question: for each of the four, do you approve, approve with a stated condition, or reject? If you reject one, what design would you accept instead?
