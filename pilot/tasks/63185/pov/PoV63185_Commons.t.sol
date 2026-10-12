// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

// Proof of Vulnerability for finding 63185 (Sherlock, Ammplify -> itos-finance/Commons):
// "Pending owner cannot accept ownership because transferOwnership / acceptOwnership
//  are implemented wrong in TimedAdminFacet".
//
// In the vulnerable TimedAdminFacet:
//   transferOwnership() only validates the owner and records a precommit. It never
//   sets pendingOwner.
//   acceptOwnership() is meant to be called by the pending owner. It calls
//   AdminLib.reassignOwner(_newOwner), which runs validateOwner() and requires
//   msg.sender == current owner. The caller here is the pending owner, not the
//   owner, so it reverts NotOwner and ownership can never be handed over.
//
// The fix (commit c6cb8ee) moves AdminLib.reassignOwner into transferOwnership and
// drops it from acceptOwnership, so the pending owner can accept without reverting.
//
// Source: data_collection/tier1_after_2025-08-31/63185.md (published Sherlock PoC).
// The report's PoC targets the Ammplify Admin.t.sol harness (adminFacet); here it is
// adapted to the Commons TimedAdminFacet using the project's own test harness pattern
// (see test/TimedAdmin.t.sol). Runs only offline, against the local audited commit.

import { PRBTest } from "@prb/test/PRBTest.sol";
import { StdCheats } from "forge-std/StdCheats.sol";

import { TimedAdminFacet } from "../src/Util/TimedAdmin.sol";
import { AdminLib } from "../src/Util/Admin.sol";

contract PoV63185_Commons is PRBTest, StdCheats {
    TestTimedFacet public facet;

    function setUp() public {
        // The deploying contract (this test) becomes the owner, see TestTimedFacet.
        facet = new TestTimedFacet();
    }

    function testPendingOwnerCannotAcceptOwnership() public {
        address pendingOwner = address(0xBEEF);

        // Current owner (this test contract) starts the ownership transfer.
        facet.transferOwnership(pendingOwner);

        // Wait past the required delay (getDelay returns 1 in this facet).
        skip(2);

        // The pending owner tries to accept after the delay.
        // On the vulnerable code acceptOwnership -> AdminLib.reassignOwner ->
        // validateOwner() reverts NotOwner because msg.sender is the pending owner,
        // not the current owner. So the handover is permanently blocked.
        vm.startPrank(pendingOwner);
        vm.expectRevert(AdminLib.NotOwner.selector);
        facet.acceptOwnership();
        vm.stopPrank();
    }
}

// Minimal concrete facet, copied from the project's own test/TimedAdmin.t.sol harness.
contract TestTimedFacet is TimedAdminFacet {
    constructor() {
        AdminLib.initOwner(msg.sender);
    }

    function getRightsUseID(bool add) internal pure override returns (uint256) {
        return add ? 0 : 1;
    }

    function getDelay(bool) public pure override returns (uint32) {
        return 1;
    }
}
