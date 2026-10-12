# Finding 63008 — Sorella L2 Angstrom (Cyfrin) — PoV build notes

## The bug in one paragraph

A zero-for-one swap walks ticks downward. To do that, `TickIteratorLib.reset`
for the downward iterator sets its starting point. In the audited code
(`src/libraries/TickIterator.sol`) it sets `self.currentTick = startTick`. But
the helper that finds the next tick, `_advanceToNextDown`, looks for a tick
strictly below `currentTick`. So when a swap starts exactly on the upper
boundary tick of a liquidity range, that boundary tick is skipped. Its
liquidity change is never added. Later, when the next tick below is crossed, the
code subtracts a liquidity amount that was never added, and the subtraction
underflows. The report shows three proofs of concept for this. The fix is one
character of logic: seed the iterator at `startTick + 1`.

## Which proof of concept I used

The report has three. I used Proof of Concept number 2,
`test_cyfrin_swapBackwardsFromTickBoundaryAndRevert`. I chose it because it
already wraps the failing swap in `vm.expectRevert()`, so the pass/fail meaning
is clean on its own: on the vulnerable code the swap reverts and the test
passes; on the fixed code the swap succeeds, the expected revert never happens,
and the test fails. That is exactly the oracle we want, with no extra assertions
to tune. Proof of concept 1 shows the same underflow but on a different line and
is not wrapped in an expected revert, and proof of concept 3 is the full
reward-stealing attack, which needs far more setup. Number 2 is the smallest
thing that proves the bug.

## The build system

Angstrom is a Foundry project that pulls its dependencies as git submodules,
not soldeer and not npm. `foundry.toml` lists `libs = ["lib"]` and a set of
remappings. The submodules are nested: `lib/v4-periphery` itself contains
`lib/v4-core` and `lib/permit2`, and the remapping
`v4-core/src/=lib/v4-periphery/lib/v4-core/src/` reaches into that nested copy.
So the install is `git submodule update --init --recursive`, not a flat
checkout. The compiler is pinned by the source pragma to `=0.8.26`
(`src/AngstromL2.sol`). The profile sets `viaIR = false` and
`optimizer_runs = 21_000`.

## How I built and proved it offline

1. Made a worktree of the audited vulnerable commit `386baff` at
   `pilot/repos/prepared/l2-angstrom@386baff`.
2. Ran `git submodule update --init --recursive` on the host to fetch all
   nested submodules.
3. Warmed the solc cache once with the network on
   (`dock.sh --net ... "forge build"`). The pragma needs solc `0.8.26`, which
   was not in the shared `solvibe-svm` volume yet; the warm build downloaded it
   (and `0.8.28`) into the volume.
4. Proved the build works with the network off (`dock.sh ... "forge build"` ->
   exit 0, "No files changed, compilation skipped").
5. Wrote the PoV and ran it with the network off. It passes on the vulnerable
   commit.

The PoV reuses the project's own test harness. The report's proofs of concept
are written as methods of the contract `AngstromL2Test` in
`test/AngstromL2.t.sol`, and they call helpers that live there
(`initializePool`, `addLiquidity`, `getRewards`) and in its base
`test/_helpers/BaseTest.sol` (`bumpBlock`, `setPriorityFee`). So the PoV
contract inherits `AngstromL2Test` and adds the one test method, which is the
most faithful way to run the published code. Because inheriting that contract
also inherits its own test methods, I run the PoV scoped with `--match-test`
`test_cyfrin_swapBackwardsFromTickBoundaryAndRevert` so the parent suite's tests
do not run again.

## Challenges and how I solved each

**Challenge — the dependencies are deeply nested git submodules.** A plain
`git submodule update --init` is not enough; v4-periphery carries v4-core and
permit2 inside it, and those carry more. Solution: `--init --recursive`, run
once on the host with the network on. After that the offline build finds
everything.

**Challenge — the pinned compiler was not cached.** The source needs solc
`=0.8.26`; the shared cache only had `0.8.30`. Solution: one networked
`forge build` (`dock.sh --net`) downloads `0.8.26` into the `solvibe-svm`
volume, and every run after that is offline.

**Challenge — the reported fix commit cannot run the same PoV.** The report
names the fix as commit `c01b6c7`, and that commit really is in the main
history (I checked with `git merge-base --is-ancestor`; it returned true). This
is unlike the Licredity findings, where the reported hash was a discarded
squash-merge branch head. The trouble here is distance: `c01b6c7` sits 21
commits after the audited snapshot and carries a lot of unrelated change.
`git diff 386baff c01b6c7` touches 25 files. Among those changes, the function
`AngstromL2.setPoolLPFee` — which Proof of Concept 2 calls — was removed, the
`addLiquidity` test helper was overloaded, and the `super-sol` submodule was
bumped. So the identical PoV will not even compile at `c01b6c7`. And even if I
adapted the test to compile there, a failure could be caused by any of the 21
commits, not by the tick-iterator fix we care about.

Solution: isolate the fix. I made a second worktree, also at the audited
snapshot `386baff`, and replaced only one file —
`src/libraries/TickIterator.sol` — with that same file taken exactly from the
fix commit `c01b6c7`. `diff -rq` over `src/` confirms that this is the only file
that differs from the vulnerable worktree. The identical PoV then runs on both
worktrees, and the only thing that changed between pass and fail is the one
documented fix. The behavioural change in that file is the downward iterator's
`reset` seeding `startTick + 1` instead of `startTick` (and the upward
iterator's loop bound going from `<` to `<=`); the file also adds an unrelated
`peekNext` helper and a doc comment, which do not affect this test.

## The oracle outcome

| Commit | Role | Expected | Observed |
| --- | --- | --- | --- |
| `386baff` | audited vulnerable snapshot | swap reverts, test passes | PASS — reverts `ArithmeticOverflowUnderflow()` |
| `386baff` + `TickIterator.sol` from `c01b6c7` | the isolated fix | swap succeeds, test fails | FAIL — "next call did not revert as expected" |
| `2548adb` | parent of the blamed VIC (PVIC) | also vulnerable | not run (see below) |

The exact revert on the vulnerable commit is `ArithmeticOverflowUnderflow()`,
raised inside the swap when liquidity net is decremented in
`CompensationPriceFinder.getZeroForOne`, and it reaches the test wrapped in the
hook's error wrappers. That matches the report's note for Proof of Concept 2.

## What blocks a clean VIC/PVIC/parent framing

The blame in `pilot/tasks/63008/history.json` points at `src/AngstromL2.sol`
line 364, which is where the underflow shows up
(`liquidity = liquidity.sub(liquidityNet)`). But the real cause, and the only
file the fix changes, is `src/libraries/TickIterator.sol`. The blame landed on
the symptom, not the cause.

Because of that, the recorded VIC and PVIC do not bracket the bug. `git blame`
on the off-by-one line in `TickIterator.sol` shows it was written in commit
`661468b` ("wip") on 2025-09-01. The blamed VIC `28db1cb` ("progress") is from
2025-09-08 and the PVIC `2548adb` ("fix") is from 2025-09-06. Both are later
than `661468b`, and both already contain the off-by-one. So the PVIC is also
vulnerable, and there is no parent in this VIC/PVIC pair where the feature
exists without the bug.

This is why I did not run the PVIC. It would need its own worktree at an older
commit, where the test harness differs again, and the result is already known
from the blame: the bug is present. The real "clean parent" for this bug would
be the parent of `661468b`, not the parent of the blamed VIC. Pinning that is
per-finding work and is recorded here as the open point rather than done.

The bug kind is "added_code": the fix changes a wrong line that a developer
wrote, not a missing guard. But the standard clean story for an added-code bug —
the parent is clean because the VIC added the bad line — does not hold here,
because the blame is on the wrong file and the bad line predates the recorded
VIC and PVIC.

## Artifacts

- `pilot/tasks/63008/pov/PoV63008_AngstromL2.t.sol` — the PoV test.
- `pilot/tasks/63008/pov_result.json` — the machine-readable result.
- `pilot/tasks/63008/notes.md` — this file.

The vulnerable worktree is kept at
`pilot/repos/prepared/l2-angstrom@386baff`. The isolated-fix worktree
(`...@386baff-tickfix`) was pruned after the runs.
