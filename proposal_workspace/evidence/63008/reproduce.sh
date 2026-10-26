#!/bin/sh
# Reproduce the finding-63008 evidence package. Offline only. No network is used
# at any step (dock.sh is always called WITHOUT --net).
#
# Prerequisites (already present in this repository):
#   - Docker image solvibe-tools:1
#   - The named Docker volume solvibe-svm, warmed with solc 0.8.26
#   - The vulnerable clone at pilot/repos/sorellaLabs__l2-angstrom (commit 386baff)
#   - Prepared dependencies at pilot/repos/prepared/l2-angstrom@386baff/lib
#
# Run this script from anywhere. Edit REPO if your checkout lives elsewhere.
set -e

REPO=/Users/minh/Documents/workspaces/secure-solvibe
DOCK="$REPO/pilot/scripts/dock.sh"
EVID="$REPO/proposal_workspace/evidence/63008"
SRC="$REPO/pilot/repos/sorellaLabs__l2-angstrom"
PREP="$REPO/pilot/repos/prepared/l2-angstrom@386baff"

WORK=$(mktemp -d)
echo "work tree: $WORK"

# 1. Throwaway local clone at the vulnerable snapshot 386baff.
git clone --local --no-hardlinks "$SRC" "$WORK/work" >/dev/null 2>&1
git -C "$WORK/work" checkout -q 386baff
WT="$WORK/work"

# 2. Use the prepared (nested submodule) dependencies, and stop forge from
#    trying to fetch submodules.
rm -rf "$WT/lib"; cp -R "$PREP/lib" "$WT/lib"
rm -f "$WT/.gitmodules"

# 3. Drop in the two test files.
cp "$EVID/tests/Evidence63008_Entitlement.t.sol" "$WT/test/"
cp "$EVID/tests/Loss63008_AngstromL2.t.sol" "$WT/test/"

# Keep a pristine copy of src so we can restore between code states.
cp -R "$WT/src" "$WORK/src_pristine"
restore() { rm -rf "$WT/src"; cp -R "$WORK/src_pristine" "$WT/src"; }

T="--match-path test/Evidence63008_Entitlement.t.sol --match-test test_entitlement_backing -vv"
S="--no-match-path test/Evidence63008_Entitlement.t.sol --summary --fuzz-seed 1"
PRE="FOUNDRY_SHOW_PROGRESS=false forge test --offline"   # show_progress=true drops results; turn it off

echo "### vulnerable 386baff"
restore
"$DOCK" "$WT" "$PRE $T"                 # both tests PASS (violation observed)
"$DOCK" "$WT" "$PRE $S"                 # repo suite 60 pass
"$DOCK" "$WT" "$PRE --match-path test/Loss63008_AngstromL2.t.sol --match-test test_loss_stealAllRewards -vv"

echo "### function-body fix (TickIterator reset: startTick -> startTick + 1)"
restore
git -C "$WT" apply "$EVID/patches/tickiterator_function_body.patch"
"$DOCK" "$WT" "$PRE $T"                 # both tests FAIL (violation absent)
"$DOCK" "$WT" "$PRE $S"                 # repo suite 55 pass / 5 fail

echo "### H-02 fix only (commit cd0ac3c)"
restore
git -C "$WT" apply "$EVID/patches/h02_fix_cd0ac3c.patch"
"$DOCK" "$WT" "$PRE $T"                 # both tests PASS (attack still works)
"$DOCK" "$WT" "$PRE $S"                 # repo suite 60 pass

echo "### both fixes"
restore
git -C "$WT" apply "$EVID/patches/both_fixes.patch"
"$DOCK" "$WT" "$PRE $T"                 # both tests FAIL (violation absent)
"$DOCK" "$WT" "$PRE $S"                 # repo suite 55 pass / 5 fail

echo "done. throwaway tree at $WORK (safe to delete)."
