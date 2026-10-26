#!/bin/sh
# Finding 63008 evidence package, version 2 runner. Offline only: dock.sh is
# always called WITHOUT --net, so the container has no network.
#
# For each code state it runs three things, compares each outcome with the
# expected outcome, and writes one log per run to logs/v2_*.log:
#   violation   - tests/Evidence63008_Entitlement.t.sol (passes when the theft happens)
#   fixedstate  - tests/Fixed63008_State.t.sol (passes when the honest LP is made whole)
#   suite       - the repository's own tests, with every package test file
#                 (test/*63008*) excluded, the same way in every state
# It does not stop at an expected failure. It prints a summary table and exits
# non-zero only if some outcome differs from the expected one.
#
# Prerequisites: Docker image solvibe-tools:1, the solvibe-svm volume warmed with
# solc 0.8.26, the clone at pilot/repos/sorellaLabs__l2-angstrom, and the
# prepared dependencies at pilot/repos/prepared/l2-angstrom@386baff/lib.
# The throwaway work tree goes to $WORK (default: a new temporary directory).
set -u
export LC_ALL=C

REPO=/Users/minh/Documents/workspaces/secure-solvibe
DOCK="$REPO/pilot/scripts/dock.sh"
EVID="$REPO/proposal_workspace/evidence/63008"
SRC="$REPO/pilot/repos/sorellaLabs__l2-angstrom"
PREP="$REPO/pilot/repos/prepared/l2-angstrom@386baff"
LOGS="$EVID/logs"
WORK=${WORK:-$(mktemp -d)}
WT="$WORK/work"

# Throwaway clone at the vulnerable snapshot 386baff, with the prepared libs.
rm -rf "$WT"
git clone -q --local --no-hardlinks "$SRC" "$WT" && git -C "$WT" checkout -q 386baff || exit 2
rm -rf "$WT/lib" && cp -R "$PREP/lib" "$WT/lib" && rm -f "$WT/.gitmodules" || exit 2
cp "$EVID"/tests/*63008*.t.sol "$WT/test/" || exit 2

# show_progress=true in the repo's foundry.toml makes forge drop suites from its
# output at random, so it is turned off for every run.
FORGE="FOUNDRY_SHOW_PROGRESS=false forge test --offline --fuzz-seed 1"
VIOLATION="--match-path test/Evidence63008_Entitlement.t.sol --match-test test_entitlement_backing -vv"
FIXEDSTATE="--match-path test/Fixed63008_State.t.sol --match-test test_fixed_state -vv"
SUITE="--no-match-path 'test/*63008*' --summary"

# Expected outcomes, written the way outcome() prints them.
V_HOLDS="2 pass, 0 fail"
V_ABSENT="0 pass, 2 fail: test_entitlement_backing_stealRewards,test_entitlement_backing_variant_boundary30"
F_BROKEN="0 pass, 2 fail: test_fixed_state_main,test_fixed_state_variant_boundary30"
F_WHOLE="2 pass, 0 fail"
S_ALL="60 pass, 0 fail"
S_FOUR="56 pass, 4 fail: test_iterateDown_boundaryExclusion,test_iterateDown_exclusiveBoundaries,test_iterateDown_simple,test_iterateDown_singleTick"

# "<passed> pass, <failed> fail[: failing test names]", summed over every
# "Suite result:" line. A build error gives "0 pass, 0 fail", which never matches.
outcome() {
    awk '/Suite result:/ { for (i = 2; i <= NF; i++) { if ($i == "passed;") p += $(i-1); if ($i == "failed;") f += $(i-1) } }
         END { printf "%d pass, %d fail", p, f }' "$1"
    names=$(grep '^\[FAIL' "$1" | sed -E 's/.*\] ([A-Za-z0-9_]+)\(.*/\1/' | sort -u | paste -sd, -)
    [ -n "$names" ] && printf ": %s" "$names"
}

BAD=0
N=0
TABLE="$WORK/v2_summary.txt"
printf '%-11s %-11s %-8s %s\n' STATE RUN RESULT OUTCOME > "$TABLE"

check() { # state run args expected
    N=$((N + 1))
    log=$(printf '%s/v2_%02d_%s_%s.log' "$LOGS" "$N" "$1" "$2")
    "$DOCK" "$WT" "$FORGE $3" > "$log" 2>&1
    got=$(outcome "$log")
    if [ "$got" = "$4" ]; then r=match; else r=DIFFERS; BAD=1; fi
    printf '%-11s %-11s %-8s %s\n' "$1" "$2" "$r" "$got" >> "$TABLE"
    [ "$r" = match ] || printf '%-11s %-11s %-8s expected %s\n' "" "" "" "$4" >> "$TABLE"
    echo "$1 $2: $r ($got)"
}

state() { # name patch... ; restores src to 386baff, then applies the patches
    git -C "$WT" checkout -q -- src
    name=$1; shift
    for p in "$@"; do
        git -C "$WT" apply "$EVID/patches/$p" || { echo "$name: patch $p did not apply"; BAD=1; return 1; }
    done
}

state vulnerable &&
    { check vulnerable violation "$VIOLATION" "$V_HOLDS"
      check vulnerable fixedstate "$FIXEDSTATE" "$F_BROKEN"
      check vulnerable suite "$SUITE" "$S_ALL"; }

state v2fix tickiterator_function_body_v2.patch &&
    { check v2fix violation "$VIOLATION" "$V_ABSENT"
      check v2fix fixedstate "$FIXEDSTATE" "$F_WHOLE"
      check v2fix suite "$SUITE" "$S_FOUR"; }

state h02only h02_fix_cd0ac3c.patch &&
    { check h02only violation "$VIOLATION" "$V_HOLDS"
      check h02only fixedstate "$FIXEDSTATE" "$F_BROKEN"
      check h02only suite "$SUITE" "$S_ALL"; }

state bothv2 h02_fix_cd0ac3c.patch tickiterator_function_body_v2.patch &&
    { check bothv2 violation "$VIOLATION" "$V_ABSENT"
      check bothv2 fixedstate "$FIXEDSTATE" "$F_WHOLE"
      check bothv2 suite "$SUITE" "$S_FOUR"; }

cp "$TABLE" "$LOGS/v2_summary.log"
echo
cat "$TABLE"
echo
if [ "$BAD" -eq 0 ]; then echo "every outcome matched the expected outcome"; else echo "SOME OUTCOME DIFFERED"; fi
echo "throwaway tree: $WORK (safe to delete)"
exit "$BAD"
