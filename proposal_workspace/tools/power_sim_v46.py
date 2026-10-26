"""Version 46: V45 on the corrected frame of project units (round-29 points R29.1 and R29.2).

Run (from proposal_workspace/tools): uv run --offline --with numpy --with statsmodels --with scipy python power_sim_v46.py [demand]
Frame: ../evidence/frame_build/protocol_units.csv, written by frame_units.py. The repository rule removes four audits whose
linked code is not a contest repository from the audit's month and one whose contest repository needs a login; one
duplicate audit is merged; audits of the same project form one sampling unit; units containing a development audit are
removed, leaving 152 units. Everything else is power_sim_v45.py (and so V44) unchanged; see its init("units").
Outputs: power_results_v46.txt, power_results_v46_vectors.csv, power_results_v46_demand.txt.
"""
import sys
import power_sim_v45 as v45

if __name__ == "__main__":
    v45.init("units")
    v45.demand() if sys.argv[1:] == ["demand"] else v45.main()
