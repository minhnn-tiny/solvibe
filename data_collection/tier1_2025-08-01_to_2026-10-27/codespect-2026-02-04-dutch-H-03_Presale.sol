// SPDX-License-Identifier: BSL-1.1
pragma solidity 0.8.28;

import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {UD60x18, ud} from "@prb/math/src/UD60x18.sol";

// Internal Dependencies
import {IDUTCHToken} from "./interfaces/IDUTCHToken.sol";
import {DUTCHBondingHook} from "./DUTCHBondingHook.sol";

// Sablier V2 Dependencies
import {ISablierLockupLinear} from "@sablier/v2-core/interfaces/ISablierLockupLinear.sol";
import {ISablierLockup} from "@sablier/v2-core/interfaces/ISablierLockup.sol";
import {LockupLinear} from "@sablier/v2-core/types/LockupLinear.sol";
import {Lockup} from "@sablier/v2-core/types/Lockup.sol";

/**
 * @title Presale
 * @notice Presale contract for DUTCH tokens with Sablier V2 vesting integration
 * @dev Collects ETH during presale period, then converts to DUTCH via bonding curve
 *      and creates vesting streams on Sablier V2 for participants
 */
contract Presale is Ownable2Step, ReentrancyGuard, Pausable {

    // -------------------------------------------------------------------------
    // Errors
    // -------------------------------------------------------------------------

    /// @dev Thrown when presale period has not started
    error Presale__PresaleNotStarted();

    /// @dev Thrown when presale period has ended
    error Presale__PresaleEnded();

    /// @dev Thrown when vesting has already been initiated
    error Presale__VestingAlreadyStarted();

    /// @dev Thrown when invalid amount is provided
    error Presale__InvalidAmount();

    /// @dev Thrown when invalid address is provided
    error Presale__InvalidAddress();

    /// @dev Thrown when presale cap is exceeded
    error Presale__PresaleCapExceeded();

    /// @dev Thrown when conditions for upkeep are not met
    error Presale__UpkeepConditionsNotMet();

    /// @dev Thrown when user has no vesting stream
    error Presale__NoStreamFound();

    // -------------------------------------------------------------------------
    // Events
    // -------------------------------------------------------------------------

    /// @dev Emitted when ETH is deposited during presale
    event EthDeposited(address indexed user, uint256 amount);

    /// @dev Emitted when vesting is initiated
    event VestingInitiated(uint256 totalEth, uint256 totalTokens);

    /// @dev Emitted when tokens are minted from bonding curve
    event TokensMinted(uint256 ethAmount, uint256 tokenAmount);

    /// @dev Emitted when Sablier vesting streams are created
    event VestingStreamsCreated(uint256 participantCount);

    /// @dev Emitted when presale is finalized
    event PresaleFinalized(uint256 totalEth, uint256 totalTokens, uint256 participantCount);

    /// @dev Emitted when user claims vested tokens
    event TokensClaimed(address indexed user, uint256 amount);

    /// @dev Emitted when external contracts are set
    event ContractsSet(address indexed dutchToken, address indexed bondingCurve);
    
    /// @dev Emitted when Sablier V2 address is updated
    event SablierV2AddressUpdated(address indexed oldSablier, address indexed newSablier);

    /// @dev Emitted when a vesting stream creation fails for a user
    event StreamCreationFailed(address indexed user, uint256 allocation);


    // -------------------------------------------------------------------------
    // Constants (Copied from BondingCurve.sol)
    // -------------------------------------------------------------------------

    /// @notice The exponent for the bonding curve (1.5).
    UD60x18 private constant EXPONENT = UD60x18.wrap(1_500000000000000000);

    /// @notice The exponent plus one for integral calculation (2.5).
    UD60x18 private constant EXPONENT_PLUS_ONE = UD60x18.wrap(2_500000000000000000);

    /// @notice The curve constant C (determines initial price).
    /// @dev Value: 500,000,000 wei = 5.0E-10 ETH.
    UD60x18 private constant CURVE_CONSTANT = UD60x18.wrap(500_000_000);

    /// @notice Basis points denominator (100% = 10000 bps).
    uint256 private constant BPS_DENOMINATOR = 10000;

    /// @notice Buy tax rate (12% fixed for presale calculations)
    uint256 private constant PRESALE_BUY_TAX_BPS = 1200; // 12%

    /// @notice Minimum contribution amount to prevent dust attacks
    uint256 public constant MIN_CONTRIBUTION = 0.01 ether;

    // -------------------------------------------------------------------------
    // State Variables
    // -------------------------------------------------------------------------

    /// @notice External contract references (set via setContracts function)
    IDUTCHToken public dutchToken;
    DUTCHBondingHook public bondingCurve;
    ISablierLockupLinear public sablierV2;

    /// @dev Presale start timestamp
    uint256 public immutable presaleStart;

    /// @dev Maximum ETH that can be raised
    uint256 public immutable presaleCap;

    /// @dev Presale duration in seconds (7 days)
    uint256 public constant PRESALE_DURATION = 7 days;

    /// @dev Vesting cliff duration (6 months)
    uint256 public constant VESTING_CLIFF = 180 days;

    /// @dev Vesting duration (12 months after cliff)
    uint256 public constant VESTING_DURATION = 365 days;

    /// @dev Total ETH raised during presale
    uint256 public totalFundedAmount;

    /// @dev Whether vesting has been initiated
    bool public vestingInitiated;

    /// @dev Mapping of user ETH contributions
    mapping(address => uint256) public contributions;

    /// @dev Mapping to track if user is already in contributors array
    mapping(address => bool) public isContributor;

    /// @dev Array of all contributors
    address[] public contributors;

    /// @dev Mapping of user Sablier stream IDs (for claiming)
    mapping(address => uint256) public vestingStreamIds;

    // -------------------------------------------------------------------------
    // Constructor
    // -------------------------------------------------------------------------

    /**
     * @notice Constructor initializes the presale contract
     * @param presaleStart_ Timestamp when presale starts
     * @param presaleCap_ Maximum ETH that can be raised (in wei)
     */
    constructor(
        uint256 presaleStart_,
        uint256 presaleCap_,
        address sablierV2_
    ) Ownable(msg.sender) {
        if (presaleStart_ <= block.timestamp) revert Presale__InvalidAmount();
        if (presaleCap_ == 0) revert Presale__InvalidAmount();
        if (sablierV2_ == address(0)) revert Presale__InvalidAddress();

        presaleStart = presaleStart_;
        presaleCap = presaleCap_;
        sablierV2 = ISablierLockupLinear(sablierV2_);
    }

    // -------------------------------------------------------------------------
    // External Functions
    // -------------------------------------------------------------------------

    /**
     * @notice Sets the external contract addresses after deployment
     * @dev Only callable by owner, prevents execution before contracts are set
     * @param dutchToken_ Address of the DUTCH token contract
     * @param bondingCurve_ Address of the bonding curve contract
     */
    function setContracts(address dutchToken_, address bondingCurve_) external onlyOwner {
        if (dutchToken_ == address(0)) revert Presale__InvalidAddress();
        if (bondingCurve_ == address(0)) revert Presale__InvalidAddress();

        dutchToken = IDUTCHToken(dutchToken_);
        bondingCurve = DUTCHBondingHook(bondingCurve_);
        
        emit ContractsSet(dutchToken_, bondingCurve_);
    }

    /**
     * @notice Updates the Sablier V2 address
     * @dev Can only be called by owner and before vesting is initiated
     * @param sablierV2_ New Sablier V2 contract address
     */
    function setSablierV2Address(address sablierV2_) external onlyOwner {
        if (sablierV2_ == address(0)) revert Presale__InvalidAddress();
        if (vestingInitiated) revert Presale__VestingAlreadyStarted();
        
        address oldSablier = address(sablierV2);
        sablierV2 = ISablierLockupLinear(sablierV2_);
        
        emit SablierV2AddressUpdated(oldSablier, sablierV2_);
    }

    /**
     * @notice Allows users to deposit ETH during presale period
     * @dev Payable function that records user contributions
     */
    function depositEth() external payable nonReentrant whenNotPaused {
        // Validate deposit amount
        if (msg.value == 0) revert Presale__InvalidAmount();
        if (msg.value < MIN_CONTRIBUTION) revert Presale__InvalidAmount();
        
        // Check presale timing
        if (block.timestamp < presaleStart) revert Presale__PresaleNotStarted();
        if (block.timestamp >= presaleStart + PRESALE_DURATION) revert Presale__PresaleEnded();
        
        // Check presale cap
        if (totalFundedAmount + msg.value > presaleCap) revert Presale__PresaleCapExceeded();
        
        // Update total funded amount
        totalFundedAmount += msg.value;
        
        // Update user's contribution
        contributions[msg.sender] += msg.value;
        
        // Handle first-time contributor
        if (!isContributor[msg.sender]) {
            isContributor[msg.sender] = true;
            contributors.push(msg.sender);
        }
        
        emit EthDeposited(msg.sender, msg.value);
    }

    /**
     * @notice Checks if conditions are met for automated upkeep
     * @dev Used by Chainlink Automation to determine when to execute performUpkeep
     *      Can be called by anyone - admin, keeper bot, or any user
     * @return upkeepNeeded True if upkeep should be performed
     * @return performData Data to pass to performUpkeep (empty for this implementation)
     */
    function checkUpkeep(bytes memory /* checkData */) external view returns (bool upkeepNeeded, bytes memory performData) {
        // Check all conditions separately
        bool tokenSet = (address(dutchToken) != address(0));
        bool bondingCurveSet = (address(bondingCurve) != address(0));
       
        bool sablierSet = (address(sablierV2) != address(0));
        bool presaleEnded = (block.timestamp >= presaleStart + PRESALE_DURATION);
        bool notExecuted = (!vestingInitiated);
        bool isFunded = (totalFundedAmount > 0);
        
        // All conditions must be true for upkeep to be needed
        bool ready = tokenSet && bondingCurveSet && sablierSet && presaleEnded && notExecuted && isFunded;
        
        if (ready) {
            return (true, "0x0");
        }
        
        return (false, "0x0");
    }

    /**
     * @notice Executes the vesting initiation atomically
     * @dev Mints tokens via bonding curve and creates Sablier streams
     *      Can be called by anyone - admin, keeper bot, or any user once conditions are met
     */
    function performUpkeep(bytes memory /* performData */) external {
        (bool upkeepNeeded,) = this.checkUpkeep("");

        if(!upkeepNeeded) revert Presale__UpkeepConditionsNotMet();
        
        // Execute atomic sequence
        uint256 totalTokens = _mintTokens();
        _createVestingStreams();
        _finalizePresale(totalTokens);
        
        emit VestingInitiated(totalFundedAmount, totalTokens);
    }

    /**
     * @notice Manually triggers presale finalization if conditions are met
     * @dev Simple wrapper around performUpkeep() for explicit presale finalization
     *      Will revert if checkUpkeep() conditions are not met
     */
    function finalizePresale() external {
        this.performUpkeep("");
    }



    // -------------------------------------------------------------------------
    // View Functions
    // -------------------------------------------------------------------------

    /**
     * @notice Returns total ETH raised in presale
     * @return Total funded amount in wei
     */
    function checkFundedAmount() external view returns (uint256) {
        return totalFundedAmount;
    }

    /**
     * @notice Returns seconds remaining until presale ends
     * @return Seconds remaining, or type(uint256).max if presale has ended, or return 0 if presale has not started yet
     */
    function timeRemaining() external view returns (uint256) {
        // If presale hasn't started yet
        if (block.timestamp < presaleStart) {
            return 0;
        }
        
        // Calculate end time
        uint256 presaleEnd = presaleStart + PRESALE_DURATION;
        
        // If presale has ended, return max value (frontend interprets as "ended")
        if (block.timestamp >= presaleEnd) {
            return type(uint256).max;
        }
        
        // Return remaining time
        return presaleEnd - block.timestamp;
    }

    /**
     * @notice Returns user's ETH contribution
     * @param user Address to check
     * @return User's contribution in wei
     */
    function getUserContribution(address user) external view returns (uint256) {
        return contributions[user];
    }

    /**
     * @notice Calculate presale allocation for total ETH raised
     * @dev Provides frontend with real-time token estimates
     * @param totalETH_ Total ETH collected in presale
     * @return tokenAmount_ Total tokens to be minted
     * @return taxAmount_ Total tax amount deducted
     * @return curveCost_ ETH going to curve after tax
     */
    function getPresaleQuote(uint256 totalETH_) 
        public 
        pure
        returns (
            uint256 tokenAmount_, 
            uint256 taxAmount_, 
            uint256 curveCost_
        ) 
    {
        // Calculate tax first (matches mintWithETH logic).
        taxAmount_ = (totalETH_ * PRESALE_BUY_TAX_BPS) / BPS_DENOMINATOR;
        
        // Calculate curve cost (remainder after tax).
        curveCost_ = totalETH_ - taxAmount_;
        
        // Calculate tokens from curve cost.
        tokenAmount_ = _calculateAmountOfDUTCHfromETH(curveCost_);
    }

    /**
     * @notice Returns user's expected token allocation
     * @param user Address to check
     * @return Expected token allocation based on ETH contribution
     */
    function getUserAllocation(address user) external view returns (uint256) {
        if (totalFundedAmount == 0) return 0;
        
        (uint256 totalTokens,,) = getPresaleQuote(totalFundedAmount);
        return (contributions[user] * totalTokens) / totalFundedAmount;
    }

    /**
     * @notice Returns number of contributors
     * @return Total number of unique contributors
     */
    function getContributorCount() external view returns (uint256) {
        return contributors.length;
    }

    // -------------------------------------------------------------------------
    // Vesting View Functions (Frontend Helpers)
    // -------------------------------------------------------------------------

    /**
     * @notice Gets complete vesting information for a user
     * @param user Address to get vesting info for
     * @return streamId The Sablier stream ID (0 if no stream)
     * @return totalReceivable Total tokens allocated to user
     * @return unlocked Currently unlocked tokens (available to claim)
     * @return claimed Tokens already claimed by user
     * @return startTime Stream start timestamp
     * @return cliffTime Cliff end timestamp  
     * @return endTime Stream end timestamp
     * @return vestingProgress Progress percentage (0-10000 basis points)
     */
    function getUserVestingInfo(address user) 
        external 
        view 
        returns (
            uint256 streamId,
            uint256 totalReceivable,
            uint256 unlocked,
            uint256 claimed,
            uint256 startTime,
            uint256 cliffTime,
            uint256 endTime,
            uint256 vestingProgress
        ) 
    {
        streamId = vestingStreamIds[user];
        
        // If user has no stream, return zeros
        if (streamId == 0 || !vestingInitiated) {
            return (0, 0, 0, 0, 0, 0, 0, 0);
        }
        // Cast to ISablierLockup for view functions
        ISablierLockup lockupInterface = ISablierLockup(address(sablierV2));
        
        totalReceivable = lockupInterface.getDepositedAmount(streamId);
        unlocked = lockupInterface.withdrawableAmountOf(streamId);
        claimed = lockupInterface.getWithdrawnAmount(streamId);
        
        // Get timing information
        startTime = lockupInterface.getStartTime(streamId);
        cliffTime = lockupInterface.getCliffTime(streamId);
        endTime = lockupInterface.getEndTime(streamId);
        
        // Calculate vesting progress (basis points: 0-10000)
        if (block.timestamp <= startTime) {
            vestingProgress = 0;
        } else if (block.timestamp >= endTime) {
            vestingProgress = BPS_DENOMINATOR; // 100%
        } else {
            vestingProgress = ((block.timestamp - startTime) * BPS_DENOMINATOR) / (endTime - startTime);
        }
    }

    /**
     * @notice Checks if user can claim tokens (cliff period has passed)
     * @param user Address to check
     * @return canClaim Whether user can claim tokens
     * @return timeUntilCliff Seconds until cliff ends (0 if already passed)
     */
    function canUserClaim(address user) external view returns (bool canClaim, uint256 timeUntilCliff) {
        uint256 streamId = vestingStreamIds[user];
        
        if (streamId == 0 || !vestingInitiated) {
            return (false, 0);
        }

        uint256 cliffTime = ISablierLockup(address(sablierV2)).getCliffTime(streamId);
        
        if (block.timestamp >= cliffTime) {
            canClaim = true;
            timeUntilCliff = 0;
        } else {
            canClaim = false;
            timeUntilCliff = cliffTime - block.timestamp;
        }
    }

    /**
     * @notice Gets user's stream ID for direct Sablier interaction
     * @param user Address to get stream ID for
     * @return streamId The Sablier stream ID (0 if no stream)
     */
    function getUserStreamId(address user) external view returns (uint256) {
        return vestingStreamIds[user];
    }

    /**
     * @notice Convenience function to claim vested tokens via presale contract
     * @dev This is optional - users can also claim directly from Sablier
     * @param amount Amount to withdraw (0 for maximum available)
     * @return withdrawnAmount Amount actually withdrawn
     */
    function claimVestedTokens(uint256 amount) external returns (uint256 withdrawnAmount) {
        uint256 streamId = vestingStreamIds[msg.sender];
        if (streamId == 0) revert Presale__NoStreamFound();
        
        // Cast to ISablierLockup for withdrawal functions
        ISablierLockup lockupInterface = ISablierLockup(address(sablierV2));
        
        if (amount == 0) {
            // Withdraw maximum available
            withdrawnAmount = lockupInterface.withdrawMax(streamId, msg.sender);
        } else {
            // Withdraw specific amount (no return value)
            lockupInterface.withdraw(streamId, msg.sender, uint128(amount));
            withdrawnAmount = uint128(amount); // We know how much was withdrawn
        }
        
        // Emit our own event for tracking
        emit TokensClaimed(msg.sender, withdrawnAmount);
    }

    // -------------------------------------------------------------------------
    // Internal Functions
    // -------------------------------------------------------------------------

    /**
     * @notice Calculate tokens from ETH using bonding curve formula
     * @dev Copied from BondingCurve.sol - handles currentSupply as 0 for presale
     * @param ethAmount_ ETH amount (after tax deduction)
     * @return tokenAmount_ Tokens that can be minted
     */
    function _calculateAmountOfDUTCHfromETH(uint256 ethAmount_)
        private
        pure
        returns (uint256 tokenAmount_)
    {
        // For presale, assume starting from 0 supply (bonding curve hasn't launched)
        uint256 currentSupply_ = 0;
        
        // Convert to UD60x18 for PRBMath.
        UD60x18 s0_ = ud(currentSupply_);
        UD60x18 ethAmount60x18_ = ud(ethAmount_);
        
        // Calculate (cost × 2.5 / C).
        UD60x18 scaledCost_ = ethAmount60x18_.mul(EXPONENT_PLUS_ONE).div(CURVE_CONSTANT);
        
        // Calculate s0^2.5.
        UD60x18 s0Pow_ = s0_.pow(EXPONENT_PLUS_ONE);
        
        // Calculate (cost × 2.5 / C + s0^2.5).
        UD60x18 sum_ = scaledCost_.add(s0Pow_);
        
        // Calculate s1 = sum^(1/2.5).
        UD60x18 s1_ = sum_.pow(EXPONENT_PLUS_ONE.inv());
        
        // Token amount = s₁ - s₀
        tokenAmount_ = s1_.unwrap() - currentSupply_;
    }

    /**
     * @notice Internal function to mint DUTCH tokens via bonding curve
     * @dev Calls bonding curve contract to convert ETH to DUTCH
     * @return tokenAmount_ The amount of tokens minted
     */
    function _mintTokens() internal returns (uint256 tokenAmount_) {
        // Ensure we have ETH to mint with
        if (totalFundedAmount == 0) revert Presale__InvalidAmount();
        
        // Calculate tax and net ETH for bonding curve
        (uint256 expectedTokens, uint256 taxAmount_, uint256 netETH_) = getPresaleQuote(totalFundedAmount);
        
        // Get tax split configuration from bonding curve
        (uint256 vaultSplitBps_, uint256 opsSplitBps_) = bondingCurve.getBuySplitConfig();
        
        // Distribute tax to vault and ops (using bonding curve split)
        uint256 vaultTax_ = (taxAmount_ * vaultSplitBps_) / BPS_DENOMINATOR;
        uint256 opsTax_ = (taxAmount_ * opsSplitBps_) / BPS_DENOMINATOR;
        
        address vaultAddress_ = bondingCurve.getDutchVault();
        address opsAddress_ = bondingCurve.getOpsWallet();
        
        (bool vaultSuccess_,) = payable(vaultAddress_).call{value: vaultTax_}("");
        if (!vaultSuccess_) revert Presale__InvalidAmount();
        
        (bool opsSuccess_,) = payable(opsAddress_).call{value: opsTax_}("");
        if (!opsSuccess_) revert Presale__InvalidAmount();
        
        // Call bonding hook with net ETH (after tax) to mint tokens
        tokenAmount_ = bondingCurve.swapExactETHForDUTCH{value: netETH_}(
            expectedTokens,  // Minimum tokens (slippage protection)
            address(this)    // Tokens minted to this presale contract
        );
        
        emit TokensMinted(totalFundedAmount, tokenAmount_);
    }

    /**
     * @notice Internal function to create Sablier vesting streams
     * @dev Creates individual streams for each contributor
     */
    function _createVestingStreams() internal {
        uint256 contributorCount = contributors.length;
        if (contributorCount == 0) {
            emit VestingStreamsCreated(0);
            return;
        }

        // Get total token amount that was minted (should already be in this contract)
        uint256 totalTokens = IERC20(address(dutchToken)).balanceOf(address(this));
        if (totalTokens == 0) {
            revert Presale__InvalidAmount();
        }

        // Approve Sablier V2 contract to spend all tokens for stream creation
        IERC20(address(dutchToken)).approve(address(sablierV2), totalTokens);

        // Vesting parameters
        LockupLinear.Durations memory durations = LockupLinear.Durations({
            cliff: uint40(VESTING_CLIFF),  // 6 months cliff
            total: uint40(VESTING_CLIFF + VESTING_DURATION)  // 18 months total (6 cliff + 12 vesting)
        });

        uint256 streamsCreated;
        uint256 totalAllocated;
        
        // Loop through each contributor and create individual vesting streams
        for (uint256 i = 0; i < contributorCount; i++) {
            address contributor = contributors[i];
            uint256 userContribution = contributions[contributor];
            
            // Calculate user's token allocation based on their ETH contribution ratio
            uint256 userTokenAllocation = (totalTokens * userContribution) / totalFundedAmount;
            
            // Skip if user has no allocation (shouldn't happen, but safety check)
            if (userTokenAllocation == 0) continue;
            
            // Add remainder to last contributor to handle rounding dust
            if (i == contributorCount - 1) {
                userTokenAllocation = totalTokens - totalAllocated;
            } else {
                totalAllocated += userTokenAllocation;
            }
            
            // Set unlock amounts (0 at start since we have a cliff, userTokenAllocation at cliff)
            LockupLinear.UnlockAmounts memory unlockAmounts = LockupLinear.UnlockAmounts({
                start: 0,
                cliff: uint128(userTokenAllocation)
            });

            // Create stream parameters
            Lockup.CreateWithDurations memory params = Lockup.CreateWithDurations({
                sender: address(this),
                recipient: contributor,
                depositAmount: uint128(userTokenAllocation),
                token: IERC20(address(dutchToken)),
                cancelable: false,  // Non-cancelable streams
                transferable: true, // Allow recipients to transfer their stream NFTs
                shape: ""  // No custom shape metadata
            });

            try sablierV2.createWithDurationsLL(params, unlockAmounts, durations) returns (uint256 streamId) {
                // Store the stream ID for this user
                vestingStreamIds[contributor] = streamId;
                streamsCreated++;
                
                // Emit event for successful stream creation
                emit TokensClaimed(contributor, userTokenAllocation);
            } catch {
                // Emit error event but don't revert - allow other streams to be created
                emit StreamCreationFailed(contributor, userTokenAllocation);
                continue;
            }
        }

        emit VestingStreamsCreated(streamsCreated);
    }

    /**
     * @notice Internal function to finalize presale
     * @dev Sets flags and emits events
     * @param totalTokens_ Total tokens minted for presale
     */
    function _finalizePresale(uint256 totalTokens_) internal {
        vestingInitiated = true;
        emit PresaleFinalized(totalFundedAmount, totalTokens_, contributors.length);
    }

}