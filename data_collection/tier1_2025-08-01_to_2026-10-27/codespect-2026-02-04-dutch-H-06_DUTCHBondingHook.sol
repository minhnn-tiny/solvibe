// SPDX-License-Identifier: BSL-1.1
pragma solidity 0.8.28;

// -------------------------------------------------------------------------
// Uniswap v4 Imports
// -------------------------------------------------------------------------

import {BaseHook} from "v4-periphery/src/utils/BaseHook.sol";
import {IWETH9} from "@uniswap/v4-periphery/src/interfaces/external/IWETH9.sol";
import {Hooks} from "@uniswap/v4-core/src/libraries/Hooks.sol";
import {IPoolManager} from "@uniswap/v4-core/src/interfaces/IPoolManager.sol";
import {PoolKey} from "@uniswap/v4-core/src/types/PoolKey.sol";
import {PoolId, PoolIdLibrary} from "@uniswap/v4-core/src/types/PoolId.sol";
import {Currency, CurrencyLibrary} from "@uniswap/v4-core/src/types/Currency.sol";
import {BeforeSwapDelta, BeforeSwapDeltaLibrary, toBeforeSwapDelta} from "@uniswap/v4-core/src/types/BeforeSwapDelta.sol";
import {BalanceDelta} from "@uniswap/v4-core/src/types/BalanceDelta.sol";
import {SwapParams, ModifyLiquidityParams} from "@uniswap/v4-core/src/types/PoolOperation.sol";

// -------------------------------------------------------------------------
// External Imports
// -------------------------------------------------------------------------

import {UD60x18, ud} from "@prb/math/src/UD60x18.sol";
import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";

// -------------------------------------------------------------------------
// Internal Imports
// -------------------------------------------------------------------------

import {IDUTCHToken} from "./interfaces/IDUTCHToken.sol";

/// @title DUTCHBondingHook
/// @notice Uniswap v4 hook implementing DUTCH bonding curve with minting,
///         burning, and tax distribution.
/// @dev Custom accounting hook that enforces bonding curve pricing.
///      Price formula: P(supply) = C × supply^1.5
///      All trades must go through this hook to maintain curve integrity.
contract DUTCHBondingHook is BaseHook, Ownable2Step, ReentrancyGuard, Pausable {
    using PoolIdLibrary for PoolKey;
    using CurrencyLibrary for Currency;
    using SafeERC20 for IERC20;

    // -------------------------------------------------------------------------
    // Errors
    // -------------------------------------------------------------------------

    /// @notice Thrown when caller is not authorized for liquidity operations.
    error Unauthorized();

    /// @notice Thrown when swap amount is zero.
    error InvalidAmount();

    /// @notice Thrown when hook's WETH reserves are insufficient for sell.
    error InsufficientReserves();

    /// @notice Thrown when calculated output is less than minimum expected.
    error SlippageExceeded();

    /// @notice Thrown when invalid address provided (zero address).
    error InvalidAddress();

    /// @notice Thrown when invalid BPS value (exceeds 10000).
    error InvalidBPS();

    /// @notice Thrown when tax split percentages don't sum to 100%.
    error InvalidSplitConfig();

    /// @notice Thrown when insufficient excess reserve is available.
    error InsufficientExcessReserve();

    /// @notice Thrown when attempting to initialize a second pool.
    error PoolAlreadyInitialized();

    /// @notice Thrown when pool has incorrect token pair.
    error InvalidTokenPair();

    /// @notice Thrown when attempting operations before pool initialization.
    error PoolNotInitialized();

    // -------------------------------------------------------------------------
    // Events
    // -------------------------------------------------------------------------

    /// @notice Emitted when DUTCH tokens are minted via buy swap.
    /// @param wethAmount_ Amount of WETH spent (including tax).
    /// @param tokenAmount_ Amount of DUTCH tokens minted.
    /// @param taxAmount_ Amount of tax collected.
    /// @param currentPrice_ Spot price after mint.
    event Minted(
        uint256 wethAmount_,
        uint256 tokenAmount_,
        uint256 taxAmount_,
        uint256 currentPrice_
    );

    /// @notice Emitted when DUTCH tokens are burned via sell swap.
    /// @param tokenAmount_ Amount of DUTCH tokens burned.
    /// @param wethAmount_ Amount of WETH refunded (net after tax).
    /// @param taxAmount_ Amount of tax collected.
    /// @param currentPrice_ Spot price after burn.
    event Burned(
        uint256 tokenAmount_,
        uint256 wethAmount_,
        uint256 taxAmount_,
        uint256 currentPrice_
    );

    /// @notice Emitted when buy tax rate is updated.
    /// @param oldBps_ Previous buy tax in basis points.
    /// @param newBps_ New buy tax in basis points.
    event BuyTaxUpdated(uint256 oldBps_, uint256 newBps_);

    /// @notice Emitted when sell tax rate is updated.
    /// @param oldBps_ Previous sell tax in basis points.
    /// @param newBps_ New sell tax in basis points.
    event SellTaxUpdated(uint256 oldBps_, uint256 newBps_);

    /// @notice Emitted when buy tax split configuration is updated.
    /// @param vaultBps_ Vault share in basis points.
    /// @param opsBps_ Ops wallet share in basis points.
    event BuySplitUpdated(uint256 vaultBps_, uint256 opsBps_);

    /// @notice Emitted when sell tax split configuration is updated.
    /// @param vaultBps_ Vault share in basis points.
    /// @param opsBps_ Ops wallet share in basis points.
    event SellSplitUpdated(uint256 vaultBps_, uint256 opsBps_);

    /// @notice Emitted when DutchVault address is updated.
    /// @param oldVault_ Previous vault address.
    /// @param newVault_ New vault address.
    event DutchVaultUpdated(address oldVault_, address newVault_);

    /// @notice Emitted when OpsWallet address is updated.
    /// @param oldWallet_ Previous wallet address.
    /// @param newWallet_ New wallet address.
    event OpsWalletUpdated(address oldWallet_, address newWallet_);

    /// @notice Emitted when excess reserve is withdrawn.
    /// @param amount_ Amount of WETH withdrawn.
    /// @param dutchVault_ DutchVault that received the WETH.
    event ExcessReserveWithdrawn(uint256 amount_, address dutchVault_);

    /// @notice Emitted when tax exemption status changes.
    /// @param account_ Address whose exemption status changed.
    /// @param exempt_ New exemption status.
    event TaxExemptionSet(address indexed account_, bool exempt_);

    /// @notice Emitted when the pool is successfully initialized.
    /// @param poolId_ ID of the initialized pool.
    /// @param initializer_ Address that initialized the pool.
    event PoolInitialized(PoolId poolId_, address initializer_);

    // -------------------------------------------------------------------------
    // Structs
    // -------------------------------------------------------------------------

    /// @notice Slippage protection parameters passed via hookData.
    /// @dev Both fields are optional (0 = skip validation).
    ///      Only one field is checked per swap based on exact input/output.
    struct SlippageParams {
        /// @notice Minimum tokens to receive (for exact input swaps).
        uint256 minOutputAmount;
        /// @notice Maximum tokens to pay (for exact output swaps).
        uint256 maxInputAmount;
    }

    // -------------------------------------------------------------------------
    // Immutables
    // -------------------------------------------------------------------------

    /// @notice DUTCH token contract.
    IDUTCHToken public immutable dutchToken;

    /// @notice WETH currency for pool interactions.
    Currency private immutable _wethCurrency;

    /// @notice DUTCH currency for pool interactions.
    Currency private immutable _dutchCurrency;

    /// @notice True if WETH is token0 in the pool, false otherwise.
    bool private immutable _wethIsToken0;

    // -------------------------------------------------------------------------
    // Constants - Bonding Curve
    // -------------------------------------------------------------------------

    /// @notice Curve constant: 5.0E-10 ETH (500,000,000 wei).
    UD60x18 private constant CURVE_CONSTANT = UD60x18.wrap(500_000_000);

    /// @notice Price exponent: 1.5.
    UD60x18 private constant EXPONENT = UD60x18.wrap(1_500000000000000000);

    /// @notice Integral exponent: 2.5 (EXPONENT + 1).
    UD60x18 private constant EXPONENT_PLUS_ONE = UD60x18.wrap(2_500000000000000000);

    // -------------------------------------------------------------------------
    // Constants - Tax Configuration
    // -------------------------------------------------------------------------

    /// @notice Basis points denominator (100%).
    uint256 private constant BPS_DENOMINATOR = 10000;

    // -------------------------------------------------------------------------
    // State - Addresses
    // -------------------------------------------------------------------------

    /// @notice DutchVault address receiving vault share of taxes.
    address private _dutchVault;

    /// @notice Operations wallet receiving ops share of taxes.
    address private _opsWallet;

    /// @notice DutchAuctionMarketplace address (authorized to call swapETHForDUTCH).
    address private _marketplace;

    /// @notice Presale contract address (authorized to call swapExactETHForDUTCH).
    address private _presale;

    // -------------------------------------------------------------------------
    // State - Tax Configuration
    // -------------------------------------------------------------------------

    /// @notice Buy tax rate in basis points (default: 1000 = 10%).
    uint256 private _buyTaxBps;

    /// @notice Sell tax rate in basis points (default: 1000 = 10%).
    uint256 private _sellTaxBps;

    /// @notice Buy tax: Vault share in basis points (default: 7500 = 75%).
    uint256 private _buyVaultSplitBps;

    /// @notice Buy tax: Ops share in basis points (default: 2500 = 25%).
    uint256 private _buyOpsSplitBps;

    /// @notice Sell tax: Vault share in basis points (default: 7500 = 75%).
    uint256 private _sellVaultSplitBps;

    /// @notice Sell tax: Ops share in basis points (default: 2500 = 25%).
    uint256 private _sellOpsSplitBps;

    /// @notice Mapping of tax-exempt addresses (e.g., marketplace).
    mapping(address account => bool isExempt) private _taxExempt;

    // -------------------------------------------------------------------------
    // State - Accounting
    // -------------------------------------------------------------------------

    /// @notice WETH reserve balance backing bonding curve.
    uint256 private _wethReserve;

    /// @notice Cumulative DUTCH tokens minted through bonding curve.
    uint256 private _totalMinted;

    /// @notice Cumulative DUTCH tokens burned through bonding curve.
    uint256 private _totalBurned;

    /// @notice Cumulative WETH added to reserve (after buy tax).
    uint256 private _wethInflow;

    /// @notice Cumulative WETH removed from reserve (before sell tax).
    uint256 private _wethOutflow;

    /// @notice Total number of mint operations (buy swaps).
    uint256 private _totalMintOperations;

    /// @notice Total number of burn operations (sell swaps).
    uint256 private _totalBurnOperations;

    /// @notice Total excess WETH withdrawn from burned token range.
    uint256 private _totalExcessWithdrawn;

    /// @notice Flag indicating if the pool has been initialized.
    bool private _poolInitialized;

    /// @notice ID of the initialized pool.
    PoolId private _poolId;

    /// @notice The pool key for WETH/DUTCH pool.
    PoolKey private _poolKey;

    // -------------------------------------------------------------------------
    // Constructor
    // -------------------------------------------------------------------------

    /// @notice Initializes the bonding curve hook.
    /// @param poolManager_ Uniswap v4 PoolManager address.
    /// @param wethAddress_ WETH token address.
    /// @param dutchToken_ DUTCH token contract address.
    /// @param dutchVault_ DutchVault address.
    /// @param opsWallet_ Operations wallet address.
    /// @param marketplace_ DutchAuctionMarketplace address.
    /// @param presale_ Presale contract address.
    /// @param owner_ Owner address for access control.
    constructor(
        IPoolManager poolManager_,
        address wethAddress_,
        address dutchToken_,
        address dutchVault_,
        address opsWallet_,
        address marketplace_,
        address presale_,
        address owner_
    ) BaseHook(poolManager_) Ownable(owner_) {
        // Validate addresses.
        if (wethAddress_ == address(0)) revert InvalidAddress();
        if (dutchToken_ == address(0)) revert InvalidAddress();
        if (dutchVault_ == address(0)) revert InvalidAddress();
        if (opsWallet_ == address(0)) revert InvalidAddress();
        if (marketplace_ == address(0)) revert InvalidAddress();
        if (presale_ == address(0)) revert InvalidAddress();
        
        dutchToken = IDUTCHToken(dutchToken_);
        _dutchVault = dutchVault_;
        _opsWallet = opsWallet_;
        _marketplace = marketplace_;
        _presale = presale_;
        
        // Initialize currencies.
        _wethCurrency = Currency.wrap(wethAddress_);
        _dutchCurrency = Currency.wrap(dutchToken_);
        
        // Determine token ordering (smaller address = token0).
        _wethIsToken0 = wethAddress_ < dutchToken_;
        
        // Initialize tax configuration with defaults (configurable)
        _buyTaxBps = 1000;          // 10%.
        _sellTaxBps = 1000;         // 10%.
        _buyVaultSplitBps = 7500;   // 75%.
        _buyOpsSplitBps = 2500;     // 25%.
        _sellVaultSplitBps = 7500;  // 75%.
        _sellOpsSplitBps = 2500;    // 25%.
        
        // Mark marketplace and presale as tax-exempt.
        _taxExempt[marketplace_] = true;
        _taxExempt[presale_] = true;
    }

    // -------------------------------------------------------------------------
    // Hook Permissions
    // -------------------------------------------------------------------------

    /// @notice Declares which hook functions are implemented.
    /// @dev Called by PoolManager during pool creation to validate hook
    ///      address.
    /// @return Permissions struct indicating active hooks.
    function getHookPermissions()
        public
        pure
        override
        returns (Hooks.Permissions memory)
    {
        return Hooks.Permissions({
            beforeInitialize: true,          // Validate pool creation
            afterInitialize: false,
            beforeAddLiquidity: true,        // Prevent all liquidity addition
            beforeRemoveLiquidity: true,     // Restrict LP to owner
            beforeSwap: true,                // Execute bonding curve
            afterSwap: false,
            beforeDonate: false,
            afterDonate: false,
            afterAddLiquidity: false,
            afterRemoveLiquidity: false,
            beforeSwapReturnDelta: true,      // Return delta to pool for slippage validation.
            afterSwapReturnDelta: false,
            afterAddLiquidityReturnDelta: false,
            afterRemoveLiquidityReturnDelta: false
        });
    }

    // -------------------------------------------------------------------------
    // Hook Implementation - Initialize
    // -------------------------------------------------------------------------

    /// @notice Validates pool initialization.
    /// @dev Enforces single pool, correct token pair, and owner-only init.
    /// @param sender_ Address that called initialize on PoolManager.
    /// @param key_ Pool key for the pool being initialized.
    /// @return Function selector for validation.
    function _beforeInitialize(
        address sender_,
        PoolKey calldata key_,
        uint160 /* sqrtPriceX96_ */
    ) internal virtual override returns (bytes4) {
        // Only owner can initialize the pool.
        if (sender_ != owner()) revert Unauthorized();

        // Enforce single pool.
        if (_poolInitialized) revert PoolAlreadyInitialized();

        // Validate token pair matches WETH/DUTCH.
        address c0_ = Currency.unwrap(key_.currency0);
        address c1_ = Currency.unwrap(key_.currency1);
        address weth_ = Currency.unwrap(_wethCurrency);
        address dutch_ = Currency.unwrap(_dutchCurrency);

        if (_wethIsToken0) {
            if (c0_ != weth_ || c1_ != dutch_) {
                revert InvalidTokenPair();
            }
        } else {
            if (c0_ != dutch_ || c1_ != weth_) {
                revert InvalidTokenPair();
            }
        }

        // Store pool ID, key, and mark as initialized.
        _poolId = key_.toId();
        _poolKey = key_;
        _poolInitialized = true;

        emit PoolInitialized(_poolId, sender_);

        return BaseHook.beforeInitialize.selector;
    }

    // -------------------------------------------------------------------------
    // Liquidity Restrictions
    // -------------------------------------------------------------------------

    /// @notice Prevents all liquidity addition.
    /// @dev This pool uses bonding curve pricing, not AMM liquidity.
    ///      Adding liquidity would waste capital as all swaps bypass AMM.
    function _beforeAddLiquidity(
        address,
        PoolKey calldata,
        ModifyLiquidityParams calldata,
        bytes calldata
    ) internal pure virtual override returns (bytes4) {
        revert Unauthorized();
    }

    /// @notice Prevents all liquidity removal.
    /// @dev This pool uses bonding curve pricing, not AMM liquidity.
    ///      Removing liquidity would interfere with bonding curve integrity.
    function _beforeRemoveLiquidity(
        address,
        PoolKey calldata,
        ModifyLiquidityParams calldata,
        bytes calldata
    ) internal pure virtual override returns (bytes4) {
        revert Unauthorized();
    }

    // -------------------------------------------------------------------------
    // Admin Functions - Tax Configuration
    // -------------------------------------------------------------------------

    /// @notice Updates the buy tax rate.
    /// @dev Only callable by owner.
    /// @param newBps_ New buy tax in basis points (max 10000).
    function setBuyTaxBps(uint256 newBps_) external onlyOwner {
        if (newBps_ >= BPS_DENOMINATOR) revert InvalidBPS();
        
        uint256 oldBps_ = _buyTaxBps;
        _buyTaxBps = newBps_;
        
        emit BuyTaxUpdated(oldBps_, newBps_);
    }

    /// @notice Updates the sell tax rate.
    /// @dev Only callable by owner.
    /// @param newBps_ New sell tax in basis points (max 10000).
    function setSellTaxBps(uint256 newBps_) external onlyOwner {
        if (newBps_ >= BPS_DENOMINATOR) revert InvalidBPS();
        
        uint256 oldBps_ = _sellTaxBps;
        _sellTaxBps = newBps_;
        
        emit SellTaxUpdated(oldBps_, newBps_);
    }

    /// @notice Updates the buy tax split configuration.
    /// @dev Only callable by owner. Splits must sum to 100% (10000 BPS).
    /// @param vaultBps_ Vault share in basis points.
    /// @param opsBps_ Ops wallet share in basis points.
    function setBuySplitConfig(uint256 vaultBps_, uint256 opsBps_)
        external
        onlyOwner
    {
        if (vaultBps_ + opsBps_ != BPS_DENOMINATOR) {
            revert InvalidSplitConfig();
        }
        
        _buyVaultSplitBps = vaultBps_;
        _buyOpsSplitBps = opsBps_;
        
        emit BuySplitUpdated(vaultBps_, opsBps_);
    }

    /// @notice Updates the sell tax split configuration.
    /// @dev Only callable by owner. Splits must sum to 100% (10000 BPS).
    /// @param vaultBps_ Vault share in basis points.
    /// @param opsBps_ Ops wallet share in basis points.
    function setSellSplitConfig(uint256 vaultBps_, uint256 opsBps_)
        external
        onlyOwner
    {
        if (vaultBps_ + opsBps_ != BPS_DENOMINATOR) {
            revert InvalidSplitConfig();
        }
        
        _sellVaultSplitBps = vaultBps_;
        _sellOpsSplitBps = opsBps_;
        
        emit SellSplitUpdated(vaultBps_, opsBps_);
    }

    /// @notice Updates the DutchVault address.
    /// @dev Only callable by owner.
    /// @param newVault_ New vault address.
    function setDutchVault(address newVault_) external onlyOwner {
        if (newVault_ == address(0)) revert InvalidAddress();
        
        address oldVault_ = _dutchVault;
        _dutchVault = newVault_;
        
        emit DutchVaultUpdated(oldVault_, newVault_);
    }

    /// @notice Updates the OpsWallet address.
    /// @dev Only callable by owner.
    /// @param newWallet_ New wallet address.
    function setOpsWallet(address newWallet_) external onlyOwner {
        if (newWallet_ == address(0)) revert InvalidAddress();
        
        emit OpsWalletUpdated(_opsWallet, newWallet_);
        _opsWallet = newWallet_;
    }

    /// @notice Sets tax exemption status for an address.
    /// @dev Used to exempt marketplace from taxes for fee handling.
    /// @param account_ Address to update exemption status.
    /// @param exempt_ True to exempt from taxes, false otherwise.
    function setTaxExemption(
        address account_,
        bool exempt_
    ) external onlyOwner {
        if (account_ == address(0)) revert InvalidAddress();
        _taxExempt[account_] = exempt_;
        emit TaxExemptionSet(account_, exempt_);
    }

    /// @notice Checks if an address is tax-exempt.
    /// @param account_ Address to check.
    /// @return True if address is exempt from taxes.
    function isTaxExempt(address account_) external view returns (bool) {
        return _taxExempt[account_];
    }

    /// @notice Pauses all swap operations.
    /// @dev Only callable by owner. Prevents swaps in beforeSwap hook.
    function pause() external onlyOwner {
        _pause();
    }

    /// @notice Unpauses all swap operations.
    /// @dev Only callable by owner. Resumes normal swap operations.
    function unpause() external onlyOwner {
        _unpause();
    }

    // -------------------------------------------------------------------------
    // View Functions - Configuration
    // -------------------------------------------------------------------------

    /// @notice Returns the current buy tax rate.
    /// @return Buy tax in basis points.
    function getBuyTaxBps() external view returns (uint256) {
        return _buyTaxBps;
    }

    /// @notice Returns the current sell tax rate.
    /// @return Sell tax in basis points.
    function getSellTaxBps() external view returns (uint256) {
        return _sellTaxBps;
    }

    /// @notice Returns the buy tax split configuration.
    /// @return vaultBps_ Vault share in basis points.
    /// @return opsBps_ Ops wallet share in basis points.
    function getBuySplitConfig()
        external
        view
        returns (uint256 vaultBps_, uint256 opsBps_)
    {
        return (_buyVaultSplitBps, _buyOpsSplitBps);
    }

    /// @notice Returns the sell tax split configuration.
    /// @return vaultBps_ Vault share in basis points.
    /// @return opsBps_ Ops wallet share in basis points.
    function getSellSplitConfig()
        external
        view
        returns (uint256 vaultBps_, uint256 opsBps_)
    {
        return (_sellVaultSplitBps, _sellOpsSplitBps);
    }

    /// @notice Returns the DutchVault address.
    /// @return DutchVault address.
    function getDutchVault() external view returns (address) {
        return _dutchVault;
    }

    /// @notice Returns the OpsWallet address.
    /// @return OpsWallet address.
    function getOpsWallet() external view returns (address) {
        return _opsWallet;
    }

    /// @notice Returns the initialized pool ID.
    /// @return Pool ID.
    function getPoolId() external view returns (PoolId) {
        return _poolId;
    }

    /// @notice Calculates available excess reserve from burned tokens.
    /// @dev Excess reserve is the WETH value of burned tokens from bottom of
    ///      curve, minus any prior withdrawals.
    /// @return available_ Amount of excess WETH available to withdraw.
    function getExcessReserve() external view returns (uint256 available_) {
        uint256 burnedTokens_ = dutchToken.getTotalUserBurned();
        uint256 excessWeth_ = _calculateCostFromZero(burnedTokens_);

        available_ = excessWeth_ > _totalExcessWithdrawn
            ? excessWeth_ - _totalExcessWithdrawn
            : 0;
    }

    /// @notice Quotes WETH to DUTCH swap (buy operation).
    /// @dev Simulates buy operation with tax. Does not account for slippage.
    /// @param wethIn_ Amount of WETH to spend (including tax).
    /// @return dutchOut_ Gross amount of DUTCH tokens before distribution.
    /// @return taxAmount_ Amount of WETH taken as tax.
    /// @return netDutch_ Net DUTCH tokens user receives.
    function getQuoteWETHtoDUTCH(uint256 wethIn_)
        external
        view
        returns (uint256 dutchOut_, uint256 taxAmount_, uint256 netDutch_)
    {
        if (wethIn_ == 0) return (0, 0, 0);

        // Calculate net WETH after tax.
        uint256 netWeth_;
        if (_buyTaxBps > 0) {
            netWeth_ = (wethIn_ * (BPS_DENOMINATOR - _buyTaxBps)) /
                BPS_DENOMINATOR;
            taxAmount_ = wethIn_ - netWeth_;
        } else {
            netWeth_ = wethIn_;
            taxAmount_ = 0;
        }

        // Calculate tokens from net WETH.
        dutchOut_ = _calculateTokensFromWETH(netWeth_);
        netDutch_ = dutchOut_;
    }

    /// @notice Quotes DUTCH to WETH swap (sell operation).
    /// @dev Simulates sell operation with tax. Does not account for slippage.
    /// @param dutchIn_ Amount of DUTCH tokens to sell.
    /// @return wethOut_ Gross WETH refund before tax.
    /// @return taxAmount_ Amount of WETH taken as tax.
    /// @return netWeth_ Net WETH user receives.
    function getQuoteDUTCHtoWETH(uint256 dutchIn_)
        external
        view
        returns (uint256 wethOut_, uint256 taxAmount_, uint256 netWeth_)
    {
        if (dutchIn_ == 0) return (0, 0, 0);

        // Calculate gross refund.
        wethOut_ = _calculateBurnRefund(dutchIn_);

        // Apply sell tax.
        if (_sellTaxBps > 0) {
            taxAmount_ = (wethOut_ * _sellTaxBps) / BPS_DENOMINATOR;
            netWeth_ = wethOut_ - taxAmount_;
        } else {
            taxAmount_ = 0;
            netWeth_ = wethOut_;
        }
    }

    /// @notice Withdraws excess reserve from burned tokens to DutchVault.
    /// @dev Only callable by owner. Amount must not exceed available excess.
    /// @param amount_ Amount of excess WETH to withdraw.
    function withdrawExcessReserve(uint256 amount_) external onlyOwner {
        if (amount_ == 0) revert InvalidAmount();

        uint256 burnedTokens_ = dutchToken.getTotalUserBurned();
        uint256 excessWeth_ = _calculateCostFromZero(burnedTokens_);
        uint256 available_ = excessWeth_ > _totalExcessWithdrawn
            ? excessWeth_ - _totalExcessWithdrawn
            : 0;

        if (amount_ > available_) revert InsufficientExcessReserve();
        if (amount_ > _wethReserve) revert InsufficientReserves();

        _totalExcessWithdrawn += amount_;
        _wethReserve -= amount_;

        IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
            _dutchVault,
            amount_
        );
        emit ExcessReserveWithdrawn(amount_, _dutchVault);
    }

    /// @notice Swaps ETH for exact amount of DUTCH tokens.
    /// @dev Only callable by marketplace. No tax applied (marketplace is exempt).
    /// @param exactDutchAmount_ Exact amount of DUTCH tokens to receive.
    /// @param recipient_ Address to receive the DUTCH tokens.
    /// @return ethUsed_ Amount of ETH actually used for the swap.
    function swapETHForDUTCH(uint256 exactDutchAmount_, address recipient_)
        external
        payable
        whenNotPaused
        nonReentrant
        returns (uint256 ethUsed_)
    {
        if (msg.sender != _marketplace) revert Unauthorized();
        if (msg.value == 0) revert InvalidAmount();
        if (exactDutchAmount_ == 0) revert InvalidAmount();
        if (recipient_ == address(0)) revert InvalidAddress();

        // 1. Calculate ETH needed (no tax for marketplace).
        ethUsed_ = _calculateMintCost(exactDutchAmount_);

        // 2. Verify sufficient ETH sent.
        if (ethUsed_ > msg.value) revert SlippageExceeded();

        // 3. Wrap ETH to WETH before adding to reserve.
        IWETH9 weth = IWETH9(Currency.unwrap(_wethCurrency));
        weth.deposit{value: ethUsed_}();

        // 4. Update hook state.
        _wethReserve += ethUsed_;
        _wethInflow += ethUsed_;
        _totalMinted += exactDutchAmount_;
        ++_totalMintOperations;

        // 5. Mint DUTCH tokens to recipient.
        dutchToken.mint(recipient_, exactDutchAmount_);

        // 6. Emit event (no tax).
        emit Minted(ethUsed_, exactDutchAmount_, 0, getCurrentPrice());

        // 7. Refund excess ETH to marketplace.
        uint256 excess_ = msg.value - ethUsed_;
        if (excess_ > 0) {
            (bool success_, ) = payable(msg.sender).call{value: excess_}("");
            if (!success_) revert InvalidAmount();
        }
    }

    /// @notice Swaps exact amount of ETH for DUTCH tokens.
    /// @dev Only callable by presale contract. Presale handles tax collection
    ///      separately. Uses exact-input model: send ETH, receive
    ///      calculated DUTCH.
    /// @param minDutchAmount_ Minimum DUTCH tokens to receive (slippage).
    /// @param recipient_ Address to receive the DUTCH tokens.
    /// @return dutchAmount_ Actual amount of DUTCH tokens minted.
    function swapExactETHForDUTCH(
        uint256 minDutchAmount_,
        address recipient_
    )
        external
        payable
        whenNotPaused
        nonReentrant
        returns (uint256 dutchAmount_)
    {
        if (msg.sender != _presale) revert Unauthorized();
        if (msg.value == 0) revert InvalidAmount();
        if (recipient_ == address(0)) revert InvalidAddress();

        // 1. Wrap ETH to WETH before adding to reserve.
        IWETH9 weth = IWETH9(Currency.unwrap(_wethCurrency));
        weth.deposit{value: msg.value}();

        // 2. Calculate DUTCH tokens from exact WETH input.
        // Note: Presale contract handles tax separately before calling this.
        dutchAmount_ = _calculateTokensFromWETH(msg.value);

        // 3. Validate non-zero tokens (prevent rounding to zero).
        if (dutchAmount_ == 0) revert InvalidAmount();

        // 4. Slippage protection.
        if (dutchAmount_ < minDutchAmount_) revert SlippageExceeded();

        // 5. Update hook state.
        _wethReserve += msg.value;
        _wethInflow += msg.value;
        _totalMinted += dutchAmount_;
        ++_totalMintOperations;

        // 6. Mint DUTCH tokens to recipient.
        dutchToken.mint(recipient_, dutchAmount_);

        // 7. Emit event (tax handled by presale).
        emit Minted(msg.value, dutchAmount_, 0, getCurrentPrice());
    }

    // -------------------------------------------------------------------------
    // Hook Implementation - Swap
    // -------------------------------------------------------------------------

    /// @notice Executes bonding curve logic before swap, replacing AMM.
    /// @dev Implements custom pricing, minting, burning, and tax distribution.
    /// @param sender_ Address initiating the swap (used for tax exemption).
    /// @param key_ Pool key.
    /// @param params_ Swap parameters (direction, amount).
    /// @param hookData_ Optional slippage protection parameters.
    /// @return selector_ Function selector for validation.
    /// @return delta_ Delta values to cancel AMM swap.
    /// @return fee_ LP fee override (0 = no override).
    function _beforeSwap(
        address sender_,
        PoolKey calldata key_,
        SwapParams calldata params_,
        bytes calldata hookData_
    )
        internal
        override
        nonReentrant
        whenNotPaused
        returns (bytes4 selector_, BeforeSwapDelta delta_, uint24 fee_)
    {
        // Validate pool has been initialized.
        if (!_poolInitialized) revert PoolNotInitialized();

        // Validate this is the initialized pool.
        if (PoolId.unwrap(key_.toId()) != PoolId.unwrap(_poolId)) {
            revert Unauthorized();
        }

        // Validate non-zero amount.
        if (params_.amountSpecified == 0) revert InvalidAmount();

        // Determine swap direction based on token ordering.
        bool isBuy_;
        if (_wethIsToken0) {
            // WETH = Token0, DUTCH = Token1.
            // zeroForOne = true → WETH → DUTCH = BUY.
            isBuy_ = params_.zeroForOne;
        } else {
            // DUTCH = Token0, WETH = Token1.
            // zeroForOne = true → DUTCH → WETH = SELL.
            isBuy_ = !params_.zeroForOne;
        }

        // Execute buy or sell logic and get amounts for slippage validation.
        uint256 inputAmount_;
        uint256 outputAmount_;
        if (isBuy_) {
            (delta_, inputAmount_, outputAmount_) = _executeBuy(key_, params_, sender_);
        } else {
            (delta_, inputAmount_, outputAmount_) =
                _executeSell(key_, params_, sender_);
        }

        // Validate slippage if hookData provided.
        if (hookData_.length > 0) {
            SlippageParams memory slippage_ =
                abi.decode(hookData_, (SlippageParams));

            if (params_.amountSpecified > 0) {
                // Exact input: validate minimum output received.
                if (
                    slippage_.minOutputAmount > 0
                        && outputAmount_ < slippage_.minOutputAmount
                ) {
                    revert SlippageExceeded();
                }
            } else {
                // Exact output: validate maximum input required.
                if (
                    slippage_.maxInputAmount > 0
                        && inputAmount_ > slippage_.maxInputAmount
                ) {
                    revert SlippageExceeded();
                }
            }
        }

        // Return selector and delta (fee = 0, no override).
        return (BaseHook.beforeSwap.selector, delta_, 0);
    }

    /// @notice Executes buy swap (WETH → DUTCH).
    /// @dev Supports both exact input and exact output.
    ///      Unused parameter: key_ (currencies are immutables).
    /// @param params_ Swap parameters.
    /// @param sender_ Address initiating the swap.
    /// @return delta_ Before swap delta.
    /// @return inputAmount_ WETH spent (including tax).
    /// @return outputAmount_ DUTCH tokens received.
    function _executeBuy(
        PoolKey calldata, /* key_ */
        SwapParams calldata params_,
        address sender_
    )
        internal
        returns (
            BeforeSwapDelta delta_,
            uint256 inputAmount_,
            uint256 outputAmount_
        )
    {
        uint256 taxAmount_;
        uint256 netWeth_;
        bool isExempt_ = _taxExempt[sender_];

        if (params_.amountSpecified > 0) {
            // Exact Input: User specifies WETH amount to spend.
            inputAmount_ = uint256(params_.amountSpecified);
            
            // Calculate tax (skip if caller is exempt).
            taxAmount_ = isExempt_
                ? 0
                : (inputAmount_ * _buyTaxBps) / BPS_DENOMINATOR;
            netWeth_ = inputAmount_ - taxAmount_;
            
            // Calculate tokens to mint from net WETH.
            outputAmount_ = _calculateTokensFromWETH(netWeth_);
            
            // Validate non-zero output.
            if (outputAmount_ == 0) revert InvalidAmount();
        } else {
            // Exact Output: User specifies DUTCH amount desired.
            outputAmount_ = uint256(-params_.amountSpecified);
            
            // Calculate net WETH needed for tokens (without tax).
            netWeth_ = _calculateMintCost(outputAmount_);
            
            // Calculate total WETH including tax (skip if caller is exempt).
            if (isExempt_) {
                inputAmount_ = netWeth_;
                taxAmount_ = 0;
            } else {
                // Formula: netWeth = totalWeth × (1 - taxRate)
                // => totalWeth = netWeth / (1 - taxRate)
                inputAmount_ = (netWeth_ * BPS_DENOMINATOR) /
                    (BPS_DENOMINATOR - _buyTaxBps);
                taxAmount_ = inputAmount_ - netWeth_;
            }
        }

        _wethReserve += netWeth_;
        _wethInflow += netWeth_;
        _totalMinted += outputAmount_;
        ++_totalMintOperations;

        // Take WETH from pool (user already deposited it).
        poolManager.take(_wethCurrency, address(this), inputAmount_);

        // Distribute tax.
        (uint256 vaultAmount_, uint256 opsAmount_) =
            _calculateBuyTax(taxAmount_);
        IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
            _dutchVault,
            vaultAmount_
        );
        IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
            _opsWallet,
            opsAmount_
        );

        // Mint DUTCH to hook.
        dutchToken.mint(address(this), outputAmount_);

        // Settle DUTCH to pool (physical movement).
        poolManager.sync(_dutchCurrency);
        IERC20(Currency.unwrap(_dutchCurrency)).safeTransfer(
            address(poolManager),
            outputAmount_
        );
        poolManager.settle();

        // Emit event with current price.
        emit Minted(inputAmount_, outputAmount_, taxAmount_, getCurrentPrice());

        // Return delta to cancel AMM swap.
        if (params_.amountSpecified > 0) {
            // Exact input: specify input, calculated output.
            delta_ = toBeforeSwapDelta(
                int128(-params_.amountSpecified),
                int128(int256(outputAmount_))
            );
        } else {
            // Exact output: calculated input, specify output.
            delta_ = toBeforeSwapDelta(
                -int128(int256(inputAmount_)),
                int128(-params_.amountSpecified)
            );
        }
    }

    /// @notice Executes sell swap (DUTCH → WETH).
    /// @dev Supports both exact input and exact output.
    ///      Unused parameter: key_ (currencies are immutables).
    /// @param params_ Swap parameters.
    /// @param sender_ Address initiating the swap.
    /// @return delta_ Before swap delta.
    /// @return inputAmount_ DUTCH tokens sold.
    /// @return outputAmount_ WETH received (net after tax).
    function _executeSell(
        PoolKey calldata, /* key_ */
        SwapParams calldata params_,
        address sender_
    )
        internal
        returns (
            BeforeSwapDelta delta_,
            uint256 inputAmount_,
            uint256 outputAmount_
        )
    {
        uint256 wethRefund_;
        uint256 taxAmount_;
        bool isExempt_ = _taxExempt[sender_];

        if (params_.amountSpecified > 0) {
            // Exact Input: User specifies DUTCH amount to sell.
            inputAmount_ = uint256(params_.amountSpecified);
            
            // Calculate WETH refund before tax.
            wethRefund_ = _calculateBurnRefund(inputAmount_);
            
            // Validate non-zero output.
            if (wethRefund_ == 0) revert InvalidAmount();
            
            // Calculate tax (skip if caller is exempt).
            taxAmount_ = isExempt_
                ? 0
                : (wethRefund_ * _sellTaxBps) / BPS_DENOMINATOR;
            outputAmount_ = wethRefund_ - taxAmount_;
        } else {
            // Exact Output: User specifies WETH amount desired (net).
            outputAmount_ = uint256(-params_.amountSpecified);
            
            // Calculate gross WETH before tax (skip if caller is exempt).
            if (isExempt_) {
                wethRefund_ = outputAmount_;
                taxAmount_ = 0;
            } else {
                // Formula: netWeth = grossWeth × (1 - taxRate)
                // => grossWeth = netWeth / (1 - taxRate)
                wethRefund_ = (outputAmount_ * BPS_DENOMINATOR) /
                    (BPS_DENOMINATOR - _sellTaxBps);
                taxAmount_ = wethRefund_ - outputAmount_;
            }
            
            // Calculate DUTCH needed to burn for this refund.
            inputAmount_ = _calculateTokensNeededForWETH(wethRefund_);
        }

        // Validate sufficient reserves for refund.
        if (_wethReserve < wethRefund_) revert InsufficientReserves();

        _wethReserve -= wethRefund_;
        _wethOutflow += wethRefund_;
        _totalBurned += inputAmount_;
        ++_totalBurnOperations;

        // Take DUTCH from pool (user already deposited it).
        poolManager.take(_dutchCurrency, address(this), inputAmount_);

        // Burn DUTCH from hook.
        dutchToken.burn(address(this), inputAmount_);

        // Distribute tax from hook's reserves.
        (uint256 vaultAmount_, uint256 opsAmount_) =
            _calculateSellTax(taxAmount_);
        IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
            _dutchVault,
            vaultAmount_
        );
        IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
            _opsWallet,
            opsAmount_
        );

        // Settle WETH to pool for user.
        poolManager.sync(_wethCurrency);
        IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
            address(poolManager),
            outputAmount_
        );
        poolManager.settle();

        // Emit event with current price.
        emit Burned(inputAmount_, outputAmount_, taxAmount_, getCurrentPrice());

        // Return delta to cancel AMM swap and provide output.
        if (params_.amountSpecified > 0) {
            // Exact input: specify input, calculated output.
            delta_ = toBeforeSwapDelta(
                int128(-params_.amountSpecified),
                int128(int256(outputAmount_))
            );
        } else {
            // Exact output: calculated input, specify output.
            delta_ = toBeforeSwapDelta(
                -int128(int256(inputAmount_)),
                int128(-params_.amountSpecified)
            );
        }
    }

    // -------------------------------------------------------------------------
    // View Functions - Bonding Curve
    // -------------------------------------------------------------------------

    /// @notice Returns the current spot price for 1 token at current supply.
    /// @dev Price = C × supply^1.5.
    /// @return price_ The current price in WETH (18 decimals).
    function getCurrentPrice() public view returns (uint256 price_) {
        uint256 currentSupply_ = _totalMinted - _totalBurned;
        
        if (currentSupply_ == 0) {
            return 0;
        }
        
        UD60x18 supply_ = ud(currentSupply_);
        UD60x18 price60x18_ = CURVE_CONSTANT.mul(supply_.pow(EXPONENT));
        price_ = price60x18_.unwrap();
    }

    /// @notice Returns current bonding curve supply.
    /// @return supply_ Current supply (totalMinted - totalBurned).
    function getBondingCurveSupply() external view returns (uint256 supply_) {
        supply_ = _totalMinted - _totalBurned;
    }

    /// @notice Returns WETH reserve balance.
    /// @return reserve_ Current WETH reserve backing the curve.
    function getReserveBalance() external view returns (uint256 reserve_) {
        reserve_ = _wethReserve;
    }

    /// @notice Returns total minted tokens.
    /// @return total_ Cumulative DUTCH minted.
    function getTotalMinted() external view returns (uint256 total_) {
        total_ = _totalMinted;
    }

    /// @notice Returns total burned tokens.
    /// @return total_ Cumulative DUTCH burned.
    function getTotalBurned() external view returns (uint256 total_) {
        total_ = _totalBurned;
    }

    // -------------------------------------------------------------------------
    // Internal Functions - Bonding Curve Math
    // -------------------------------------------------------------------------

    /// @notice Calculates WETH cost for minting tokens at current supply.
    /// @dev Uses integral: C × ((s₁^2.5 - s₀^2.5) / 2.5).
    /// @param tokenAmount_ The amount of tokens to mint.
    /// @return cost_ The WETH cost (18 decimals).
    function _calculateMintCost(uint256 tokenAmount_)
        internal
        view
        returns (uint256 cost_)
    {
        uint256 currentSupply_ = _totalMinted - _totalBurned;

        // Convert to UD60x18 for PRBMath.
        UD60x18 s0_ = ud(currentSupply_);
        UD60x18 s1_ = ud(currentSupply_ + tokenAmount_);

        // Calculate s1^2.5 and s0^2.5.
        UD60x18 s1Pow_ = s1_.pow(EXPONENT_PLUS_ONE);
        UD60x18 s0Pow_ = s0_.pow(EXPONENT_PLUS_ONE);

        // Calculate integral: (s1^2.5 - s0^2.5) / 2.5.
        UD60x18 integral_ = (s1Pow_.sub(s0Pow_)).div(EXPONENT_PLUS_ONE);

        // Multiply by curve constant: C × integral.
        UD60x18 cost60x18_ = CURVE_CONSTANT.mul(integral_);

        // WETH uses 18 decimals, same as UD60x18, no conversion needed.
        cost_ = cost60x18_.unwrap();
    }

    /// @notice Calculates WETH refund for burning tokens.
    /// @dev Uses integral: C × ((s₀^2.5 - s₁^2.5) / 2.5).
    /// @param tokenAmount_ The amount of tokens to burn.
    /// @return refund_ The WETH refund (18 decimals).
    
    function _calculateBurnRefund(uint256 tokenAmount_)
        internal
        view
        returns (uint256 refund_)
    {
        uint256 currentSupply_ = _totalMinted - _totalBurned;

        // Convert to UD60x18 for PRBMath.
        UD60x18 s0_ = ud(currentSupply_);
        UD60x18 s1_ = ud(currentSupply_ - tokenAmount_);

        // Calculate s0^2.5 and s1^2.5.
        UD60x18 s0Pow_ = s0_.pow(EXPONENT_PLUS_ONE);
        UD60x18 s1Pow_ = s1_.pow(EXPONENT_PLUS_ONE);

        // Calculate integral: (s0^2.5 - s1^2.5) / 2.5.
        UD60x18 integral_ = (s0Pow_.sub(s1Pow_)).div(EXPONENT_PLUS_ONE);

        // Multiply by curve constant: C × integral.
        UD60x18 refund60x18_ = CURVE_CONSTANT.mul(integral_);

        // WETH uses 18 decimals, same as UD60x18, no conversion needed.
        refund_ = refund60x18_.unwrap();
    }

    /// @notice Calculates tokens that can be minted with given WETH amount.
    /// @dev Inverts the minting curve: solve for Δs given cost.
    /// @param wethAmount_ The amount of WETH to spend on the curve.
    /// @return tokenAmount_ The amount of tokens that can be minted.
    /// @dev Formula: Δs = ((cost × 2.5 / C) + s0^2.5)^(1/2.5) - s0.
    function _calculateTokensFromWETH(uint256 wethAmount_)
        internal
        view
        returns (uint256 tokenAmount_)
    {
        uint256 currentSupply_ = _totalMinted - _totalBurned;

        // Convert to UD60x18 for PRBMath.
        UD60x18 s0_ = ud(currentSupply_);
        UD60x18 wethAmount60x18_ = ud(wethAmount_);

        // Calculate (cost × 2.5 / C).
        UD60x18 scaledCost_ =
            wethAmount60x18_.mul(EXPONENT_PLUS_ONE).div(CURVE_CONSTANT);

        // Calculate s0^2.5.
        UD60x18 s0Pow_ = s0_.pow(EXPONENT_PLUS_ONE);

        // Calculate (cost × 2.5 / C + s0^2.5).
        UD60x18 sum_ = scaledCost_.add(s0Pow_);

        // Calculate s1 = sum^(1/2.5).
        UD60x18 s1_ = sum_.pow(EXPONENT_PLUS_ONE.inv());

        // Token amount = s₁ - s₀.
        tokenAmount_ = s1_.unwrap() - currentSupply_;
    }

    /// @notice Calculates tokens needed to burn for desired WETH amount.
    /// @dev Inverts the burning curve: solve for Δs given refund.
    /// @param wethAmount_ The amount of WETH desired.
    /// @return tokenAmount_ The amount of tokens that must be burned.
    /// @dev Formula: Δs = s0 - (s0^2.5 - refund×2.5/C)^(1/2.5).
    function _calculateTokensNeededForWETH(uint256 wethAmount_)
        internal
        view
        returns (uint256 tokenAmount_)
    {
        uint256 currentSupply_ = _totalMinted - _totalBurned;

        // Convert to UD60x18 for PRBMath.
        UD60x18 s0_ = ud(currentSupply_);
        UD60x18 wethAmount60x18_ = ud(wethAmount_);

        // Calculate (refund × 2.5 / C).
        UD60x18 scaledRefund_ =
            wethAmount60x18_.mul(EXPONENT_PLUS_ONE).div(CURVE_CONSTANT);

        // Calculate s0^2.5.
        UD60x18 s0Pow_ = s0_.pow(EXPONENT_PLUS_ONE);

        // Calculate (s0^2.5 - refund × 2.5 / C).
        UD60x18 diff_ = s0Pow_.sub(scaledRefund_);

        // Calculate s1 = diff^(1/2.5).
        UD60x18 s1_ = diff_.pow(EXPONENT_PLUS_ONE.inv());

        // Token amount = s₀ - s₁.
        tokenAmount_ = currentSupply_ - s1_.unwrap();
    }

    /// @notice Calculates WETH cost for tokens at bottom of curve (from 0).
    /// @dev Used for excess reserve accounting from burned token range.
    /// @param tokenAmount_ Amount of tokens from bottom of curve.
    /// @return cost_ WETH cost in 18 decimals.
    function _calculateCostFromZero(uint256 tokenAmount_)
        internal
        pure
        returns (uint256 cost_)
    {
        UD60x18 s1_ = ud(tokenAmount_);
        UD60x18 s1Pow_ = s1_.pow(EXPONENT_PLUS_ONE);
        UD60x18 integral_ = s1Pow_.div(EXPONENT_PLUS_ONE);
        UD60x18 cost60x18_ = CURVE_CONSTANT.mul(integral_);
        cost_ = cost60x18_.unwrap();
    }

    /// @notice Calculates buy tax split between Vault and Ops.
    /// @dev Due to rounding, opsAmount_ receives any remainder dust (< 1 wei
    ///      per transaction).
    /// @param taxAmount_ Total tax amount.
    /// @return vaultAmount_ Amount for DutchVault.
    /// @return opsAmount_ Amount for OpsWallet.
    function _calculateBuyTax(uint256 taxAmount_)
        internal
        view
        returns (uint256 vaultAmount_, uint256 opsAmount_)
    {
        vaultAmount_ = (taxAmount_ * _buyVaultSplitBps) / BPS_DENOMINATOR;
        opsAmount_ = taxAmount_ - vaultAmount_;
    }

    /// @notice Calculates sell tax split between Vault and Ops.
    /// @dev Due to rounding, opsAmount_ receives any remainder dust (< 1 wei
    ///      per transaction).
    /// @param taxAmount_ Total tax amount.
    /// @return vaultAmount_ Amount for DutchVault.
    /// @return opsAmount_ Amount for OpsWallet.
    function _calculateSellTax(uint256 taxAmount_)
        internal
        view
        returns (uint256 vaultAmount_, uint256 opsAmount_)
    {
        vaultAmount_ = (taxAmount_ * _sellVaultSplitBps) / BPS_DENOMINATOR;
        opsAmount_ = taxAmount_ - vaultAmount_;
    }
}
