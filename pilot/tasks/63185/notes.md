# Finding 63185 — Pending owner cannot accept ownership (Ammplify, Sherlock)

## What the bug is

The bug lives in the itos-finance/Commons library, in `src/Util/TimedAdmin.sol`, in
the abstract contract `TimedAdminFacet`. Ammplify uses this library as the base of
its `AdminFacet`, so the Sherlock report is written against the Ammplify test suite,
but the broken code is in Commons.

Ownership transfer is meant to work in two steps. The current owner calls
`transferOwnership(newOwner)`. After a delay, the new owner calls `acceptOwnership()`.

In the vulnerable code the two steps are wired wrong. `transferOwnership` only checks
the caller is the owner and records a precommit. It never sets `pendingOwner`.
`acceptOwnership`, which the pending owner calls, then calls
`AdminLib.reassignOwner(newOwner)`. That function runs `validateOwner()`, which
reverts `NotOwner` unless `msg.sender` is the current owner. The caller here is the
pending owner, not the owner, so the call always reverts. Ownership can never be
handed over.

The fix (commit `c6cb8ee`, "Fix TimedAdmin's reassign owner implementation") moves
`AdminLib.reassignOwner` into `transferOwnership`, where the current owner calls it,
and drops it from `acceptOwnership`. After the fix the pending owner can accept.

## The proof of vulnerability

The report's proof of concept is three lines of Foundry: call `transferOwnership`,
warp past the delay, then `vm.expectRevert(AdminLib.NotOwner.selector)` around the
pending owner's `acceptOwnership`. On the vulnerable code the call reverts `NotOwner`,
so the test passes. On the fixed code the call succeeds, so `expectRevert` has nothing
to catch and the test fails. That difference is the oracle.

The report's PoC uses the Ammplify `adminFacet`. The Commons repo does not have that
deployment, but it has its own harness in `test/TimedAdmin.t.sol`: a `TestTimedFacet`
that extends `TimedAdminFacet`, sets the deployer as owner with `AdminLib.initOwner`,
and returns a delay of 1 from `getDelay`. I reused that harness exactly and wrote the
report's three steps against it. The test file is `test/PoV63185_Commons.t.sol`.

One small change from the report: the report calls `makeAddr("pendingOwner")`, which
comes from forge-std's `Test` base. The Commons harness uses `PRBTest` and
`StdCheats` instead, so I used a plain literal address (`address(0xBEEF)`) for the
pending owner. The behaviour is the same.

## Build system

Commons is a Foundry project that gets its dependencies from git submodules
(`.gitmodules`), not soldeer or npm. The submodules are forge-std, prb-test,
openzeppelin-contracts, v3-core and v3-periphery. The clone had empty `lib/`
directories, so I ran `git submodule update --init --recursive` in the vulnerable
worktree with the network on. `foundry.toml` pins solc 0.8.28 and evm_version cancun.

## The three runs

All runs were inside Docker with the network off, through `pilot/scripts/dock.sh`.

| Commit | Role | Expected | Observed |
| --- | --- | --- | --- |
| `621c233` | audited vulnerable snapshot | PASS | PASS — reverts `AdminLib.NotOwner` |
| `c6cb8ee` | the fix | FAIL | FAIL — "next call did not revert as expected" |
| `bdd563a` | parent of the VIC (PVIC) | does not compile | compile fails — feature absent |

The oracle is valid: the exploit passes on the vulnerable snapshot and fails on the
fix.

## Bug kind: added_code

The commit that introduced the bug (the VIC, `0c4f31f8`, "Have Timed admin override
Admin operations with a delay") added the whole `transferOwnership` / `acceptOwnership`
override to `TimedAdminFacet`, with `reassignOwner` in the wrong place. The parent of
that commit (`bdd563a`) has no such override at all, and `getDelay` there takes no
argument. So the bug is code the VIC added, and the fix corrects the lines the VIC
wrote. This is the "added_code" kind, not "missing_code".

Because the whole feature arrived with the VIC, the parent cannot even compile the
proof of vulnerability. `getDelay(bool)` in the harness has nothing to override, and
`transferOwnership` / `acceptOwnership` do not exist to be called. The compiler says
"Function has override specified but does not override anything" and "Contract
TestTimedFacet should be marked as abstract". That is the honest parent result: the
parent is clean because the vulnerable feature is not there yet.

## Challenges and how they were solved

1. **The report targets a different repo than the one with the bug.** The PoC is
   written for Ammplify's `Admin.t.sol`, but the vulnerable code is in the Commons
   library. Solution: adapt the PoC to the Commons repo and reuse the Commons harness
   in `test/TimedAdmin.t.sol`.

2. **Sibling tests do not compile at these commits.** `test/math/Comparison.t.sol`
   and `test/math/Utils.t.sol` fail to compile, because the pinned forge-std is newer
   than the tests expect (cheat calls can no longer be `pure`). The task allows
   deleting sibling `*.t.sol` files in a disposable worktree, so I deleted every
   `*.t.sol` except the PoV in each worktree. The source tree is untouched.

3. **The report names no fix commit.** Unlike finding 62347, there is no "Fixed in ..."
   line and no PR link in the report. The fix commit `c6cb8ee` comes from the
   `fix_candidates` field in `history.json`. It is present directly in main history
   (not squash-merged and lost), confirmed by `git cat-file -t` and by reading its
   diff on `src/Util/TimedAdmin.sol`.

4. **The parent pins a solc version that was not cached.** `bdd563a` pins solc 0.8.20
   in its `foundry.toml`, while the vulnerable and fix commits use 0.8.28. The offline
   cache only had 0.8.28. I warmed 0.8.20 once with `--net` (allowed for one-time solc
   download), then ran the parent check offline. The parent's submodule pins also
   differ from the snapshot, but the compile fails on the missing feature, which is a
   source-level fact independent of the dependency versions.

## Anything that blocks a clean VIC / PVIC / parent framing

Nothing blocks the oracle. The vulnerable-versus-fixed difference is clean and valid.
The only nuance is the parent: for this added_code bug the VIC introduced an entire
feature, so the parent does not have the functions to run the proof against. The
"compile but fail on parent" form of the SusVibes check therefore does not apply here.
The honest starting point for an agent is the parent, where the agent would be asked to
implement the timed ownership transfer; the question is whether the agent wires
`reassignOwner` into `transferOwnership` (correct) or into `acceptOwnership` (the human's
bug).
