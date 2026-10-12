# Finding 64637 — Active and pending bets can be cancelled by anyone (Cyfrin, Wannabet-v2)

## The bug

`Bet.cancel` in Wannabet-v2 is meant to let the maker cancel a pending bet and
let anyone cancel an expired bet. At the audited commit it only stops the maker
from cancelling an active bet. Anyone else, including the taker, can cancel a
non-expired active bet and get their stake back. In a sports bet the taker can
watch the game, and once their side is losing, call `cancel()` to unwind the bet
and walk away. The code at the audited snapshot is:

```solidity
if (b.status >= IBet.Status.RESOLVED) {
    revert InvalidStatus();
} else {
    // The maker can cancel a pending bet, so block them from cancelling an active bet
    if (b.maker == msg.sender && b.status != IBet.Status.PENDING) {
        revert InvalidStatus();
    }
}
```

The only caller it blocks is the maker. Everyone else falls straight through to
the refund.

## The build system

The repository is a pnpm monorepo. The contracts live in `contracts/`. That
package is a Hardhat 3 project (`contracts/hardhat.config.ts`) using
`hardhat-toolbox-viem`, which runs Foundry-style Solidity tests through the
`forge-std` npm dependency. There is no `foundry.toml` and no `lib/` directory
in either the vulnerable or the fixed commit. Solidity imports resolve through
`node_modules`: `forge-std`, `@openzeppelin/contracts` and
`@aave-dao/aave-v3-origin`, all declared in `contracts/package.json`. The
compiler is solc 0.8.28 with `viaIR` turned on in the hardhat config.

Our sandbox runner (`pilot/scripts/dock.sh`) runs `forge`, and the two worked
examples are `forge` projects, so the task was to make this Hardhat project build
and test under `forge`, offline, inside Docker.

## What I did

I created a git worktree at the audited vulnerable commit
`d7333369548874cb99e9648ea2424ac1e67cc23f` and worked inside its `contracts/`
directory. I added a small `contracts/foundry.toml` that pins solc 0.8.28, turns
on `via_ir` (to match the project's hardhat config), and sets the remappings. I
cloned the project's declared dependency versions into `contracts/lib`:
forge-std v1.9.4 and OpenZeppelin v5.4.0.

The proof of vulnerability is the report's own proof of concept, copied into
`contracts/test/PoV64637_Wannabet.t.sol`, with two changes needed to run it
offline (explained under the challenges below). It deploys a mock USDC, mints to
the maker and the taker, deploys the `Bet` implementation and the `BetFactory`,
creates a bet with no Aave pool, has the taker accept it, warps to just before
the end time, and then has the taker cancel the active bet.

I warmed the solc 0.8.28 cache once with the network on
(`dock.sh --net ... "forge build"`), then proved the build and the test both run
with the network off. The shared solc cache (the `solvibe-svm` Docker volume)
meant the fixed commit reused the same compiler offline.

## Results

| Commit | Role | Expected | Observed |
| --- | --- | --- | --- |
| `d733336` | audited vulnerable snapshot | exploit succeeds | PASS — taker cancels the active bet, both parties refunded |
| `025c815` | the fix ("Implement feedback from audit") | exploit fails | FAIL — `Bet.cancel` reverts `Unauthorized()` |
| `680d95d` | parent of the VIC (PVIC) | — | not run (does not compile; see below) |

The exploit works on the human's vulnerable code and is stopped by the human's
fix. That pass-then-fail pair is what makes the proof a usable oracle: it fires
on vulnerable code and is silent on fixed code.

## Challenges and how I solved them

**The published proof of concept forks a live chain.** The project's own test
file `contracts/test/BetFactory.t.sol`, which the report tells you to add the
test to, starts with `vm.createSelectFork("https://base-rpc.publicnode.com")`
and uses the real Base USDC and aUSDC addresses. That breaks the hard rule that
tests run offline and never fork a live chain or use a deployed-contract address.
I rewrote `setUp` to run fully offline: a local mock ERC20 for USDC, minted to
the maker and taker, in place of the fork. The bet I attack (`betNoPool`) is
created before any Aave pool is set, so its cancel path never touches Aave and a
plain mock token is enough. I deleted `BetFactory.t.sol` in the disposable
worktrees so the live-fork test did not get compiled or run.

**The fix renames a struct field and adds an enum member, but the proof must be
one file that compiles on both commits.** The fix renames the `Bet` struct field
`resolveBy` to `endsBy` and adds a `JUDGING` member to the `Status` enum. The
report's proof reads `state.resolveBy` to compute the warp target, which would
not compile against the fix. I store the end time in `setUp` as `resolveByTs` and
warp to `resolveByTs - 1`, so the test never reads the renamed field. The test
also only names the `Status` members that exist in both commits (`PENDING`,
`ACTIVE`, `RESOLVED`, `CANCELLED`, `EXPIRED`), never `JUDGING`. The warp target
is the same instant the published proof used, so the behaviour is unchanged.

**Aave is a dependency only as a type, never as a call.** `Bet.sol` imports the
Aave V3 `IPool` interface, and at the fix commit `BetFactory.sol` also imports
`IAToken` and `IPoolAddressesProvider`. The real dependency is the whole
`aave-dao/aave-v3-origin` repository, pulled from GitHub, with its own remapping
set. For this proof the bet has no pool, so none of the Aave functions are ever
executed; the interfaces are needed only so the type references in `Bet.sol` and
`BetFactory.sol` compile. Rather than pull the full Aave repository into an
offline build, I wrote minimal local stubs of the three interfaces in
`contracts/lib/aave-stub`, declaring only the members the two contracts
reference (`IPool.supply`, `IPool.withdraw`, `IPool.getReserveAToken`,
`IAToken.UNDERLYING_ASSET_ADDRESS`, `IPoolAddressesProvider.getPool`). Because
those members are never called on the attacked bet, the compiled behaviour on
the test path is the same as with the real interfaces.

**The Aave import alias changed between the two commits.** The vulnerable commit
imports `@aave-dao/aave-v3-origin/src/contracts/interfaces/IPool.sol`. The fix
imports `@aave/v3/interfaces/IPool.sol` and adds a `contracts/remappings.txt`
that points `@aave/v3/` at `node_modules`. My `foundry.toml` carries both aliases
remapped onto the same stub directory, so one `lib/` works for both worktrees. I
removed the fix's `remappings.txt` because it points at a `node_modules` layout I
do not use.

**The reported fix hash is not in the history.** The report says the bug was
"Fixed in commit cdf3d64". That object does not exist in the cloned repository
(`git cat-file -t cdf3d64` fails). It is the head of the audit-feedback pull
request, which was squash-merged, so the branch commit was discarded. The real
merged fix is `025c815` ("Implement feedback from audit (#1)"), which is the only
commit that touches `contracts/src/Bet.sol` after the snapshot and is an ancestor
of `origin/main`. Its new `cancel` allows an active or judging bet to be
cancelled only by the judge, which is exactly what blocks the taker in the proof.

## What blocks a clean VIC / PVIC / parent framing

This is a missing-code bug, like the two Licredity pilots. The fix adds an
authorization check that never existed before, so the parent of the blame commit
is also vulnerable, and there is no parent where the feature exists without the
bug.

There is an extra wrinkle here that the Licredity findings did not have. The
blame commit (the VIC, `0c111c5`, "Organize contracts, add test") is a big rename
commit. It renamed `cancelBet` to `cancel`, `resolveBet` to `resolve` and
`deposit` to `accept`, and moved the errors into the interface. It also added the
partial guard quoted above. Before it, the function was `cancelBet()` and had no
check on who may cancel at all — only `status < RESOLVED`, with a literal
`// TODO: Can't cancel a bet that's not expired`. So the parent `680d95d` is
vulnerable too, but the proof cannot be run there without being rewritten to the
old function names, because it calls `accept()` and `cancel()` which do not exist
yet. I recorded the parent as not run for that reason, the same way finding 62348
recorded its parent.

So the honest reading for the benchmark: the vulnerability is the absence of a
who-can-cancel check, present at both the parent and the audited snapshot, and
removed only by the fix. The oracle is valid on the vulnerable-versus-fixed
difference alone.
