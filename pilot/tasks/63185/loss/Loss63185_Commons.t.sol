// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

// Loss check for finding 63185 (Sherlock, Ammplify -> itos-finance/Commons):
// "Pending owner cannot accept ownership because transferOwnership / acceptOwnership
//  are implemented wrong in TimedAdminFacet".
//
// No money is held or moved by TimedAdminFacet. The owner role in Commons only
// grants and removes admin rights (see the AdminRegistry comment in
// src/Util/Admin.sol). So this test does not measure a loss. It records who
// controls the contract after a failed handover, and checks that no ether moves.
// It runs unchanged on the vulnerable commit and on the fix; only the logged
// outcome differs. Runs only offline, against local code.

import { PRBTest } from "@prb/test/PRBTest.sol";
import { StdCheats } from "forge-std/StdCheats.sol";
import { console2 } from "forge-std/console2.sol";

import { TimedAdminFacet } from "../src/Util/TimedAdmin.sol";
import { AdminLib } from "../src/Util/Admin.sol";

contract Loss63185_Commons is PRBTest, StdCheats {
    TestTimedFacet public facet;

    address constant NEW_OWNER = address(0xBEEF);
    address constant SOME_ADMIN = address(0xA11CE);

    function setUp() public {
        facet = new TestTimedFacet(); // this test contract is the first owner
    }

    function test_loss_ownershipHandover() public {
        address oldOwner = address(this);
        uint256 facetEth = address(facet).balance;
        uint256 oldOwnerEth = oldOwner.balance;
        uint256 newOwnerEth = NEW_OWNER.balance;

        // Owner starts the handover, waits past the delay, new owner tries to accept.
        facet.transferOwnership(NEW_OWNER);
        skip(2);
        vm.prank(NEW_OWNER);
        (bool accepted,) = address(facet).call(abi.encodeCall(facet.acceptOwnership, ()));

        address ownerAfter = facet.owner();
        console2.log("pending owner could accept ownership:", accepted);
        console2.log("owner after the handover attempt:", ownerAfter);
        console2.log("old owner still in control:", ownerAfter == oldOwner);

        // Can whoever owns the contract now start another transfer (retry or rotate the key)?
        vm.prank(ownerAfter);
        (bool retried, bytes memory err) =
            address(facet).call(abi.encodeCall(facet.transferOwnership, (address(0xCAFE))));
        console2.log("current owner can start a new transfer:", retried);
        if (!retried) console2.logBytes(err);

        // The owner's only power in Commons: grant admin rights (time gated). Still usable?
        vm.prank(ownerAfter);
        facet.submitRights(SOME_ADMIN, 1, true);
        skip(2);
        vm.prank(ownerAfter);
        facet.acceptRights();
        console2.log("rights granted by current owner:", facet.adminRights(SOME_ADMIN));

        // No ether moved anywhere.
        console2.log("facet ether before/after (wei):", facetEth, address(facet).balance);
        assertEq(address(facet).balance, facetEth, "facet balance changed");
        assertEq(oldOwner.balance, oldOwnerEth, "old owner balance changed");
        assertEq(NEW_OWNER.balance, newOwnerEth, "new owner balance changed");
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
