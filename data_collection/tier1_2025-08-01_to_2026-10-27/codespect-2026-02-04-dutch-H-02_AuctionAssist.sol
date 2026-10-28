// SPDX-License-Identifier: BSL-1.1
pragma solidity 0.8.28;

// External
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";
import {
    ReentrancyGuard
} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

// Internal
import {IDutchVault} from "./interfaces/IDutchVault.sol";
import {IDUTCHToken} from "./interfaces/IDUTCHToken.sol";
import {IAuctionAssist} from "./interfaces/IAuctionAssist.sol";

/// @title AuctionAssist
/// @notice Allows users to contribute ETH to accelerate NFT purchases.
/// @dev Users receive proportional DUTCH token rewards when NFTs are sold.
contract AuctionAssist is Ownable2Step, Pausable, ReentrancyGuard, IAuctionAssist {
    // -------------------------------------------------------------------------
    // Libraries
    // -------------------------------------------------------------------------

    using SafeERC20 for IERC20;

    // -------------------------------------------------------------------------
    // Storage
    // -------------------------------------------------------------------------

    /// @notice Contribution record for a user to a collection.
    struct ContributionRecord {
        uint256 amount;
        uint256 percentageBPS;
    }

    /// @notice The DutchVault contract address.
    address private _dutchVault;

    /// @notice The DUTCH token contract address.
    address private _dutchToken;

    /// @notice User contributions: user => collection => record.
    mapping(address user => mapping(address collection => ContributionRecord))
        private _contributions;

    /// @notice Total contributions per collection.
    mapping(address collection => uint256 total) private _totalContributions;

    /// @notice List of contributors per collection.
    mapping(address collection => address[] contributors)
        private _collectionContributors;

    /// @notice Tracks if a user has contributed to a collection.
    mapping(address collection => mapping(address user => bool hasContributed))
        private _hasContributed;

    /// @notice List of collections a user has contributed to.
    mapping(address user => address[] collections) private _userCollections;

    /// @notice NFT purchase information.
    struct NFTPurchaseInfo {
        address collection;
        uint256 tokenId;
        uint256 costETH;
        uint256 totalContributionETH;
        address[] contributors;
        bool rewardsFunded;
    }

    /// @notice User position information for a single collection.
    struct UserPosition {
        address collection;
        uint256 amountContributed;
        uint256 percentageBPS;
    }

    /// @notice Counter for purchase IDs.
    uint256 private _purchaseIdCounter;

    /// @notice Mapping from purchase ID to purchase info.
    mapping(uint256 purchaseId => NFTPurchaseInfo) private _purchases;

    /// @notice Mapping from purchase ID to contributor shares in BPS.
    mapping(uint256 purchaseId => mapping(address contributor => uint256 shareBPS))
        private _purchaseShares;

    /// @notice Total DUTCH funded for a purchase.
    mapping(uint256 purchaseId => uint256 dutchFunded) private _purchaseFunding;

    /// @notice Tracks if a contributor has claimed rewards for a purchase.
    mapping(uint256 purchaseId => mapping(address contributor => bool claimed))
        private _rewardsClaimed;

    // -------------------------------------------------------------------------
    // Constructor
    // -------------------------------------------------------------------------

    /// @notice Contract constructor.
    /// @param dutchVault_ The DutchVault contract address.
    /// @param dutchToken_ The DUTCH token contract address.
    constructor(address dutchVault_, address dutchToken_) Ownable(msg.sender) {
        if (dutchVault_ == address(0)) {
            revert InvalidDutchVaultAddress();
        }
        if (dutchToken_ == address(0)) {
            revert InvalidDUTCHTokenAddress();
        }
        _dutchVault = dutchVault_;
        _dutchToken = dutchToken_;
    }

    // -------------------------------------------------------------------------
    // Events
    // -------------------------------------------------------------------------

    /// @notice Emitted when a user contributes ETH.
    /// @param contributor_ The contributor address.
    /// @param collection_ The collection address.
    /// @param amount_ The ETH amount contributed.
    /// @param percentageBPS_ The percentage of target price in basis points.
    event ContributionReceived(
        address indexed contributor_,
        address indexed collection_,
        uint256 amount_,
        uint256 percentageBPS_
    );

    /// @notice Emitted when an NFT purchase is recorded.
    /// @param purchaseId_ The unique purchase ID.
    /// @param collection_ The NFT collection address.
    /// @param tokenId_ The NFT token ID.
    /// @param costETH_ The purchase cost in ETH.
    /// @param contributorCount_ The number of contributors.
    event PurchaseRecorded(
        uint256 indexed purchaseId_,
        address indexed collection_,
        uint256 indexed tokenId_,
        uint256 costETH_,
        uint256 contributorCount_
    );

    /// @notice Emitted when rewards are distributed to a contributor.
    /// @param purchaseId_ The purchase ID.
    /// @param contributor_ The contributor address.
    /// @param dutchAmount_ The DUTCH amount rewarded.
    event RewardDistributed(
        uint256 indexed purchaseId_,
        address indexed contributor_,
        uint256 dutchAmount_
    );

    /// @notice Emitted when a purchase is funded with DUTCH rewards.
    /// @param purchaseId_ The purchase ID.
    /// @param dutchAmount_ The total DUTCH amount funded.
    event PurchaseFunded(
        uint256 indexed purchaseId_,
        uint256 dutchAmount_
    );

    /// @notice Emitted when a contributor claims their reward.
    /// @param purchaseId_ The purchase ID.
    /// @param contributor_ The contributor address.
    /// @param dutchAmount_ The DUTCH amount claimed.
    event RewardClaimed(
        uint256 indexed purchaseId_,
        address indexed contributor_,
        uint256 dutchAmount_
    );

    /// @notice Emitted when protocol share is burned.
    /// @param purchaseId_ The purchase ID.
    /// @param dutchAmount_ The DUTCH amount burned.
    event DUTCHBurned(uint256 indexed purchaseId_, uint256 dutchAmount_);

    // -------------------------------------------------------------------------
    // Errors
    // -------------------------------------------------------------------------

    /// @notice Thrown when DutchVault address is zero.
    error InvalidDutchVaultAddress();

    /// @notice Thrown when DUTCH token address is zero.
    error InvalidDUTCHTokenAddress();

    /// @notice Thrown when collection is not configured.
    error CollectionNotConfigured();

    /// @notice Thrown when contribution amount is zero.
    error InvalidContributionAmount();

    /// @notice Thrown when caller is not authorized DutchVault contract.
    error UnauthorizedCaller();

    /// @notice Thrown when purchase ID is invalid.
    error InvalidPurchaseId();

    /// @notice Thrown when purchase cost is zero.
    error InvalidPurchaseCost();

    /// @notice Thrown when max contributors limit is exceeded.
    error MaxContributorsExceeded();

    /// @notice Thrown when rewards have already been distributed.
    error RewardsAlreadyDistributed();

    /// @notice Thrown when DUTCH amount is zero.
    error InvalidDUTCHAmount();

    /// @notice Thrown when rewards have already been claimed.
    error RewardsAlreadyClaimed();

    /// @notice Thrown when purchase has not been funded.
    error PurchaseNotFunded();

    // -------------------------------------------------------------------------
    // Constants
    // -------------------------------------------------------------------------

    /// @notice Maximum number of contributors per collection.
    /// @dev Prevents unbounded loop gas costs in recordPurchase.
    ///      ~30k gas per contributor = ~3M gas for 100 contributors.
    uint256 private constant MAX_CONTRIBUTORS = 100;

    // -------------------------------------------------------------------------
    // Owner Functions
    // -------------------------------------------------------------------------

    /// @notice Pause the contract.
    function pause() external onlyOwner {
        _pause();
    }

    /// @notice Unpause the contract.
    function unpause() external onlyOwner {
        _unpause();
    }

    // -------------------------------------------------------------------------
    // Public Functions
    // -------------------------------------------------------------------------

    /// @notice Contribute ETH to accelerate NFT purchase for a collection.
    /// @param collection_ The collection address to contribute to.
    function contribute(address collection_)
        external
        payable
        nonReentrant
        whenNotPaused
    {
        // 1. Validate contribution amount is non-zero.
        if (msg.value == 0) {
            revert InvalidContributionAmount();
        }

        // 2. Get base price (target price) from DutchVault.
        uint256 basePrice_ = IDutchVault(_dutchVault).getBasePrice(collection_);

        // 3. Validate collection is configured.
        if (basePrice_ == 0) {
            revert CollectionNotConfigured();
        }

        // 4. Calculate percentage in basis points (10000 = 100%).
        uint256 percentageBPS_ = (msg.value * 10000) / basePrice_;

        // 5. Track contributor if first time.
        if (!_hasContributed[collection_][msg.sender]) {
            // Check max contributors limit.
            if (_collectionContributors[collection_].length >= MAX_CONTRIBUTORS)
            {
                revert MaxContributorsExceeded();
            }
            _collectionContributors[collection_].push(msg.sender);
            _hasContributed[collection_][msg.sender] = true;
            
            // Track collection for this user.
            _userCollections[msg.sender].push(collection_);
        }

        // 6. Update contribution record for user.
        ContributionRecord storage record_ =
            _contributions[msg.sender][collection_];
        record_.amount += msg.value;
        record_.percentageBPS += percentageBPS_;

        // 7. Update total contributions for collection.
        _totalContributions[collection_] += msg.value;

        // 8. Forward ETH to DutchVault.
        IDutchVault(_dutchVault).receiveContribution{value: msg.value}(
            collection_, msg.sender
        );

        // 9. Emit event.
        emit ContributionReceived(
            msg.sender, collection_, msg.value, percentageBPS_
        );
    }

    /// @notice Record an NFT purchase and snapshot contributors.
    /// @dev Only callable by DutchVault contract.
    /// @param collection_ The NFT collection address.
    /// @param tokenId_ The NFT token ID.
    /// @param costETH_ The purchase cost in ETH.
    /// @return purchaseId_ The unique purchase ID.
    function recordPurchase(
        address collection_,
        uint256 tokenId_,
        uint256 costETH_
    ) external returns (uint256 purchaseId_) {
        // 1. Validate caller is DutchVault.
        if (msg.sender != _dutchVault) {
            revert UnauthorizedCaller();
        }

        // 2. Validate cost is non-zero.
        if (costETH_ == 0) {
            revert InvalidPurchaseCost();
        }

        // 3. Increment purchase counter.
        purchaseId_ = _purchaseIdCounter++;

        // 4. Get total contributions for this collection.
        uint256 totalContributionETH_ = _totalContributions[collection_];

        // 5. Get list of contributors.
        address[] memory contributors_ =
            _collectionContributors[collection_];

        // 6. Store purchase info.
        NFTPurchaseInfo storage purchase_ = _purchases[purchaseId_];
        purchase_.collection = collection_;
        purchase_.tokenId = tokenId_;
        purchase_.costETH = costETH_;
        purchase_.totalContributionETH = totalContributionETH_;
        purchase_.rewardsFunded = false;

        // 7. Calculate and store contributor shares based on actual cost.
        for (uint256 i; i < contributors_.length; ++i) {
            address contributor_ = contributors_[i];
            uint256 contributionAmount_ =
                _contributions[contributor_][collection_].amount;

            if (contributionAmount_ > 0) {
                // Calculate share as (contribution * 10000) / cost.
                uint256 shareBPS_ =
                    (contributionAmount_ * 10000) / costETH_;
                
                // Cap at 10000 BPS (100%) to prevent over-distribution.
                if (shareBPS_ > 10000) {
                    shareBPS_ = 10000;
                }
                
                _purchaseShares[purchaseId_][contributor_] = shareBPS_;
                purchase_.contributors.push(contributor_);
            }
        }

        // 8. Emit event.
        emit PurchaseRecorded(
            purchaseId_,
            collection_,
            tokenId_,
            costETH_,
            purchase_.contributors.length
        );

        return purchaseId_;
    }

    /// @notice Record an NFT settlement and pull rewards from DutchVault.
    /// @param purchaseId_ The purchase ID to record settlement for.
    /// @param dutchAmount_ The total DUTCH amount from the settlement.
    function recordAndPullRewards(
        uint256 purchaseId_,
        uint256 dutchAmount_
    ) external {
        // 1. Validate caller is DutchVault.
        if (msg.sender != _dutchVault) {
            revert UnauthorizedCaller();
        }

        // 2. Validate DUTCH amount.
        if (dutchAmount_ == 0) {
            revert InvalidDUTCHAmount();
        }

        // 3. Get purchase info.
        NFTPurchaseInfo storage purchase_ = _purchases[purchaseId_];
        
        // 4. Validate purchase exists.
        if (purchase_.costETH == 0) {
            revert InvalidPurchaseId();
        }

        // 4. Validate rewards not already funded.
        if (purchase_.rewardsFunded) {
            revert RewardsAlreadyDistributed();
        }

        // 5. Mark rewards as funded and store amount.
        purchase_.rewardsFunded = true;
        _purchaseFunding[purchaseId_] = dutchAmount_;

        // 6. Transfer DUTCH from owner to this contract.
        IERC20(_dutchToken).safeTransferFrom(
            msg.sender,
            address(this),
            dutchAmount_
        );

        // 7. Emit event.
        emit PurchaseFunded(purchaseId_, dutchAmount_);
    }

    /// @notice Allows contributor to claim their DUTCH reward for a purchase.
    /// @dev Anyone can call this to claim their own rewards.
    /// @param purchaseId_ The purchase ID to claim rewards from.
    function claimReward(uint256 purchaseId_)
        external
        nonReentrant
        whenNotPaused
    {
        // 1. Validate purchase is funded.
        uint256 totalFunded_ = _purchaseFunding[purchaseId_];
        if (totalFunded_ == 0) {
            revert PurchaseNotFunded();
        }

        // 2. Check if already claimed.
        if (_rewardsClaimed[purchaseId_][msg.sender]) {
            revert RewardsAlreadyClaimed();
        }

        // 3. Get contributor share.
        uint256 contributorShare_ = _purchaseShares[purchaseId_][msg.sender];
        if (contributorShare_ == 0) {
            revert InvalidDUTCHAmount();
        }

        // 4. Calculate reward amount.
        uint256 reward_ = (totalFunded_ * contributorShare_) / 10000;
        if (reward_ == 0) {
            revert InvalidDUTCHAmount();
        }

        // 5. Mark as claimed.
        _rewardsClaimed[purchaseId_][msg.sender] = true;

        // 6. Transfer DUTCH to contributor.
        IERC20(_dutchToken).safeTransfer(msg.sender, reward_);

        // 7. Emit event.
        emit RewardClaimed(purchaseId_, msg.sender, reward_);
    }

    /// @notice Burns unclaimed protocol share after all users claim.
    /// @dev Can be called by anyone once all contributors have claimed.
    /// @param purchaseId_ The purchase ID to burn protocol share from.
    function burnProtocolShare(uint256 purchaseId_)
        external
        nonReentrant
        whenNotPaused
    {
        // 1. Validate purchase is funded.
        uint256 totalFunded_ = _purchaseFunding[purchaseId_];
        if (totalFunded_ == 0) {
            revert PurchaseNotFunded();
        }

        // 2. Calculate total user shares.
        NFTPurchaseInfo storage purchase_ = _purchases[purchaseId_];
        address[] memory contributors_ = purchase_.contributors;
        uint256 totalUserShares_;
        
        for (uint256 i; i < contributors_.length; ++i) {
            totalUserShares_ += _purchaseShares[purchaseId_][contributors_[i]];
        }

        // 3. Calculate protocol share (remaining BPS).
        uint256 protocolShareBPS_ = 10000 - totalUserShares_;
        if (protocolShareBPS_ == 0) {
            revert InvalidDUTCHAmount();
        }

        uint256 protocolAmount_ = (totalFunded_ * protocolShareBPS_) / 10000;
        if (protocolAmount_ == 0) {
            revert InvalidDUTCHAmount();
        }

        // 4. Burn protocol share.
        IDUTCHToken(_dutchToken).userBurn(protocolAmount_);

        // 5. Emit event.
        emit DUTCHBurned(purchaseId_, protocolAmount_);
    }

    // -------------------------------------------------------------------------
    // View Functions
    // -------------------------------------------------------------------------

    /// @notice Returns the DutchVault address.
    /// @return vault_ The DutchVault address.
    function getDutchVault() external view returns (address vault_) {
        return _dutchVault;
    }

    /// @notice Returns the DUTCH token address.
    /// @return token_ The DUTCH token address.
    function getDutchToken() external view returns (address token_) {
        return _dutchToken;
    }

    /// @notice Returns a user's contribution to a collection.
    /// @param user_ The user address.
    /// @param collection_ The collection address.
    /// @return record_ The contribution record.
    function getContribution(address user_, address collection_)
        external
        view
        returns (ContributionRecord memory record_)
    {
        return _contributions[user_][collection_];
    }

    /// @notice Returns total contributions for a collection.
    /// @param collection_ The collection address.
    /// @return total_ The total ETH contributed.
    function getTotalContributions(address collection_)
        external
        view
        returns (uint256 total_)
    {
        return _totalContributions[collection_];
    }

    /// @notice Returns purchase information for a given purchase ID.
    /// @param purchaseId_ The purchase ID.
    /// @return info_ The purchase information.
    function getPurchaseInfo(uint256 purchaseId_)
        external
        view
        returns (NFTPurchaseInfo memory info_)
    {
        return _purchases[purchaseId_];
    }

    /// @notice Returns a contributor's share for a specific purchase.
    /// @param purchaseId_ The purchase ID.
    /// @param contributor_ The contributor address.
    /// @return shareBPS_ The contributor's share in basis points.
    function getPurchaseShare(uint256 purchaseId_, address contributor_)
        external
        view
        returns (uint256 shareBPS_)
    {
        return _purchaseShares[purchaseId_][contributor_];
    }

    /// @notice Returns the current purchase ID counter.
    /// @return counter_ The current purchase ID counter.
    function getPurchaseIdCounter() external view returns (uint256 counter_) {
        return _purchaseIdCounter;
    }

    /// @notice Returns all contributors for a collection.
    /// @param collection_ The collection address.
    /// @return contributors_ Array of contributor addresses.
    function getCollectionContributors(address collection_)
        external
        view
        returns (address[] memory contributors_)
    {
        return _collectionContributors[collection_];
    }

    /// @notice Returns all collections a user has contributed to.
    /// @param user_ The user address.
    /// @return collections_ Array of collection addresses.
    function getUserCollections(address user_)
        external
        view
        returns (address[] memory collections_)
    {
        return _userCollections[user_];
    }

    /// @notice Returns all active positions for a user with details.
    /// @param user_ The user address.
    /// @return positions_ Array of user position details.
    function getUserActivePositions(address user_)
        external
        view
        returns (UserPosition[] memory positions_)
    {
        address[] memory collections_ = _userCollections[user_];
        positions_ = new UserPosition[](collections_.length);

        for (uint256 i; i < collections_.length; ++i) {
            address collection_ = collections_[i];
            ContributionRecord memory record_ =
                _contributions[user_][collection_];

            positions_[i] = UserPosition({
                collection: collection_,
                amountContributed: record_.amount,
                percentageBPS: record_.percentageBPS
            });
        }

        return positions_;
    }

    /// @notice Returns claimable reward amount for a contributor.
    /// @param purchaseId_ The purchase ID.
    /// @param contributor_ The contributor address.
    /// @return claimable_ The claimable DUTCH amount (0 if claimed).
    function getClaimableReward(uint256 purchaseId_, address contributor_)
        external
        view
        returns (uint256 claimable_)
    {
        // Return 0 if already claimed.
        if (_rewardsClaimed[purchaseId_][contributor_]) {
            return 0;
        }

        // Return 0 if not funded.
        uint256 totalFunded_ = _purchaseFunding[purchaseId_];
        if (totalFunded_ == 0) {
            return 0;
        }

        // Calculate claimable amount.
        uint256 contributorShare_ = _purchaseShares[purchaseId_][contributor_];
        if (contributorShare_ == 0) {
            return 0;
        }

        return (totalFunded_ * contributorShare_) / 10000;
    }

    /// @notice Checks if a contributor has claimed their reward.
    /// @param purchaseId_ The purchase ID.
    /// @param contributor_ The contributor address.
    /// @return claimed_ True if reward has been claimed.
    function hasClaimedReward(uint256 purchaseId_, address contributor_)
        external
        view
        returns (bool claimed_)
    {
        return _rewardsClaimed[purchaseId_][contributor_];
    }
}
