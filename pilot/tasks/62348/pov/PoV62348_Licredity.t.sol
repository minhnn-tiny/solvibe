// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

// Proof of Vulnerability for finding 62348 (Cyfrin C-2, Licredity v2.0):
// "Swap-and-pop without index fix-up corrupts Position's fungible array".
//
// Position.removeFungible does a swap-and-pop on the fungibles array but does
// not update the moved element's cached index in fungibleStates. The array and
// the mapping fall out of sync. This detector removes a non-last fungible and
// shows the moved element's packed FungibleState word is left unchanged (the
// index was not fixed up). On the fixed code the word changes, so the test fails.
//
// Source: data_collection/tier1_after_2025-08-31/62348.md (published Cyfrin PoC).
// Runs only offline, against local audited code.

import {Licredity} from "src/Licredity.sol";
import {Fungible} from "src/types/Fungible.sol";
import {ChainInfo} from "src/libraries/ChainInfo.sol";
import {Deployers} from "./utils/Deployer.sol";
import {StateLibrary} from "./utils/StateLibrary.sol";
import {BaseERC20Mock} from "test/mocks/BaseERC20Mock.sol";

contract PoV62348_Licredity is Deployers {
    using StateLibrary for Licredity;

    function setUp() public {
        deployETHLicredityWithUniswapV4();
        deployAndSetOracleMock();
        deployLicredityRouter();
    }

    function test_removeFungible_missingIndexFixup() public {
        BaseERC20Mock token = _newAsset(18);
        Fungible fungible = Fungible.wrap(address(token));
        // --- arrange: two fungibles in the same position ---
        token.mint(address(this), 1 ether);
        token.approve(address(licredityRouter), 1 ether);

        uint256 positionId = licredityRouter.open();

        // deposit native (will be fungibles[0])
        licredityRouter.depositFungible{value: 0.5 ether}(positionId, Fungible.wrap(ChainInfo.NATIVE), 0.5 ether);

        // deposit ERC20 (will be fungibles[1])
        licredityRouter.depositFungible(positionId, fungible, 1 ether);

        // --- discover storage slots we need (once per test is fine) ---
        (, uint256 fungibleStatesBase, uint256 fungiblesArraySlot) =
            _locatePositionFungibleStateAndArraySlots(positionId, address(licredity), address(token));

        // Sanity: array length is 2
        uint256 lenBefore = uint256(vm.load(address(licredity), bytes32(fungiblesArraySlot)));
        assertEq(lenBefore, 2, "pre: fungibles length should be 2");

        // Pre-read the packed FungibleState word for the ERC20 (index + balance)
        bytes32 stateBefore = _loadFungibleState(address(licredity), fungibleStatesBase, address(token));

        // Also read the array's first element (native) and second (ERC20)
        bytes32 dataSlot = keccak256(abi.encodePacked(bytes32(fungiblesArraySlot)));
        bytes32 arr0Before = vm.load(address(licredity), dataSlot); // [0]
        bytes32 arr1Before = vm.load(address(licredity), bytes32(uint256(dataSlot) + 1)); // [1]
        assertEq(address(uint160(uint256(arr0Before))), address(0), "pre: [0] must be native");
        assertEq(address(uint160(uint256(arr1Before))), address(token), "pre: [1] must be ERC20");

        // --- act: remove the non-last fungible (native) fully -> triggers swap-and-pop ---
        licredityRouterHelper.withdrawFungible(positionId, address(this), ChainInfo.NATIVE, 0.5 ether);

        // --- assert: array element moved down, BUT ERC20's state word did not change ---
        uint256 lenAfter = uint256(vm.load(address(licredity), bytes32(fungiblesArraySlot)));
        assertEq(lenAfter, 1, "post: fungibles length should be 1");

        bytes32 arr0After = vm.load(address(licredity), dataSlot);
        assertEq(address(uint160(uint256(arr0After))), address(token), "post: [0] must be ERC20");

        bytes32 stateAfter = _loadFungibleState(address(licredity), fungibleStatesBase, address(token));

        // A correct implementation would change only the ERC20's *index* in the word.
        // The buggy code does not fix up the index, so the word stays identical.
        assertEq(stateAfter, stateBefore, "post: ERC20 FungibleState word unchanged (index not fixed up)");
    }

    function _locatePositionFungibleStateAndArraySlots(uint256 positionId, address target, address erc20)
        internal
        view
        returns (uint256 selfSlot, uint256 fungibleStatesBase, uint256 fungiblesArraySlot)
    {
        for (uint256 S = 0; S <= 160; S++) {
            bytes32 self = keccak256(abi.encode(positionId, S));

            for (uint256 offMap = 0; offMap <= 24; offMap++) {
                uint256 candMapBase = uint256(self) + offMap;

                bytes32 nativeState = _loadFungibleState(target, candMapBase, address(0));
                bytes32 erc20State = _loadFungibleState(target, candMapBase, erc20);

                if (nativeState != bytes32(0) && erc20State != bytes32(0)) {
                    for (uint256 offArr = 0; offArr <= 24; offArr++) {
                        uint256 candArrSlot = uint256(self) + offArr;
                        if (_arrayIsNativeThen(target, candArrSlot, erc20)) {
                            return (uint256(self), candMapBase, candArrSlot);
                        }
                    }
                }
            }
        }
        revert("could not locate position/fungible storage layout");
    }

    // True when the array at `arrSlot` has length 2 and holds [native, erc20].
    function _arrayIsNativeThen(address target, uint256 arrSlot, address erc20) internal view returns (bool) {
        if (uint256(vm.load(target, bytes32(arrSlot))) != 2) return false;
        bytes32 dataSlot = keccak256(abi.encodePacked(bytes32(arrSlot)));
        address a0 = address(uint160(uint256(vm.load(target, dataSlot))));
        address a1 = address(uint160(uint256(vm.load(target, bytes32(uint256(dataSlot) + 1)))));
        return a0 == address(0) && a1 == erc20;
    }

    function _loadFungibleState(address target, uint256 mapBaseSlot, address asset) internal view returns (bytes32) {
        bytes32 key = keccak256(abi.encodePacked(bytes32(uint256(uint160(asset))), bytes32(mapBaseSlot)));
        return vm.load(target, key);
    }

    receive() external payable {}
}
