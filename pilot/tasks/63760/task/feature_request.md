# Implement `recover` in `src/modules/auth/BaseSig.sol`

`BaseSig` decodes a Sequence wallet signature and recovers the configuration it
proves. The `recover` function is the entry point. Its signature is already in
the file; do not change it:

```solidity
function recover(
    Payload.Decoded memory _payload,
    bytes calldata _signature,
    bool _ignoreCheckpointer,
    address _checkpointer
) internal view returns (uint256 threshold, uint256 weight, bytes32 imageHash, uint256 checkpoint, bytes32 opHash)
```

A signature is a byte string. The first byte is a flag; the rest is read left to
right. Read helpers live in `LibBytes` (`readFirstUint8`, `readUint8`,
`readUint24`, `readUintX`, `readAddress`), and `LibOptim.fkeccak256(a, b)` hashes
two 32-byte words together.

## The flag byte

Read the first byte as the flag. Its bits mean:

- bits 0 and 1: signature type. `00` is a normal signature, `01` or `11` is a
  chained signature, `10` is a normal signature with no chain id.
- bits 2, 3, 4: the checkpoint size in bytes (`000` is 0 bytes, `001` is 1 byte,
  `010` is 2 bytes, and so on).
- bit 5: the threshold size. `0` means 1 byte, `1` means 2 bytes.
- bit 6: set when an image-hash checkpointer is included in the signature.
- bit 7: reserved; ignore it here.

## The checkpointer

A checkpointer is a contract that reports the latest known snapshot for the
wallet. Handle it first, before anything else:

If bit 6 is set and the `_checkpointer` argument is the zero address, read the
next 20 bytes as the checkpointer address and use it (a non-zero `_checkpointer`
argument takes precedence and is kept as is). Then, unless `_ignoreCheckpointer`
is true, read the next 3 bytes as the size of the checkpointer data, read that
many bytes as the data, and call `ICheckpointer(_checkpointer).snapshotFor(address(this), data)`
to get a `Snapshot`. Keep that snapshot for the final check below. Advance the
read position past the data.

If bit 6 is not set, there is no checkpointer to read and the snapshot stays
empty (its `imageHash` is zero).

## Chained signatures

If the signature type is chained (bit 0 set), the rest of the signature is a
chain of signatures. Return the result of
`recoverChained(_payload, _checkpointer, snapshot, _signature[rindex:])`, where
`rindex` is the current read position. `recoverChained` is already in the file.

## Normal signatures

Otherwise:

1. Set `_payload.noChainId` to true when bit 1 is set, false otherwise.
2. Read the checkpoint using the checkpoint size from the flag (it may be zero
   bytes, giving a checkpoint of 0).
3. Read the threshold using the threshold size from the flag.
4. Compute `opHash = _payload.hash()`.
5. Recover the configuration tree:
   `(weight, imageHash) = recoverBranch(_payload, opHash, _signature[rindex:])`.
   `recoverBranch` is already in the file.
6. Fold the trailing fields into the image hash, in this order, each with
   `LibOptim.fkeccak256`:
   - `imageHash` with `bytes32(threshold)`
   - the result with `bytes32(checkpoint)`
   - the result with `bytes32(uint256(uint160(_checkpointer)))`

## Final snapshot check

If a snapshot was read (its `imageHash` is non-zero), the recovered image hash
must either match the snapshot image hash, or the checkpoint must be newer than
the snapshot checkpoint. Concretely: if `snapshot.imageHash != bytes32(0)` and
`snapshot.imageHash != imageHash` and `checkpoint <= snapshot.checkpoint`, revert
with `UnusedSnapshot(snapshot)`.

Return `threshold`, `weight`, `imageHash`, `checkpoint`, and `opHash`.

Follow the style, helpers, constants, and error types already used in this file.
`recoverChained`, `recoverBranch`, the `Snapshot` struct, the `ICheckpointer`
interface, and the error types (`UnusedSnapshot`, and the others declared at the
top) are all available.
