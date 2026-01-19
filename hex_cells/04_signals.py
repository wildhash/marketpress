"""
MarketPress Hex Cell 4: Compute Signals
Compute: current_prob, Δ24h, Δ7d, volatility, attention, confidence, newsworthiness
"""

def compute_probability_changes(markets_df: pd.DataFrame, snapshots_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute probability changes (Δ24h, Δ7d)
    
    Note: For first snapshot, these will be NaN. Over time as more snapshots accumulate,
    these will show actual changes.
    """
    df = markets_df.copy()
    
    # For initial snapshot, we don't have historical data yet
    # In a real implementation, these would be computed from historical snapshots
    df['delta_24h'] = np.nan
    df['delta_7d'] = np.nan
    
    # In production, you would:
    # 1. Store snapshots_df to persistent storage
    # 2. Query snapshots from 24h and 7d ago
    # 3. Compute actual deltas
    
    return df


def compute_volatility(markets_df: pd.DataFrame, snapshots_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute volatility (standard deviation of prices)
    
    Note: Requires multiple snapshots over time
    """
    df = markets_df.copy()
    
    # For single snapshot, use a proxy based on current price
    # Markets near 50% are more volatile
    df['volatility'] = df['yes_price'].apply(lambda p: 2 * p * (1 - p))
    
    # In production with historical data:
    # df['volatility'] = df.groupby('ticker')['yes_price'].transform(lambda x: x.std())
    
    return df


def compute_attention_score(markets_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute attention score (volume + open interest weighted)
    """
    df = markets_df.copy()
    
    # Normalize volume and open interest to 0-1 range
    if df['volume'].max() > 0:
        vol_norm = df['volume'] / df['volume'].max()
    else:
        vol_norm = 0
    
    if df['open_interest'].max() > 0:
        oi_norm = df['open_interest'] / df['open_interest'].max()
    else:
        oi_norm = 0
    
    # Weighted combination
    df['attention_score'] = 0.6 * vol_norm + 0.4 * oi_norm
    
    return df


def compute_newsworthiness(markets_df: pd.DataFrame, liquidity_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute newsworthiness score (composite)
    
    Factors:
    - delta_24h (weight: 0.30)
    - volatility (weight: 0.25)
    - attention (weight: 0.25)
    - confidence (weight: 0.20)
    """
    df = markets_df.copy()
    
    # Merge confidence score
    df = df.merge(liquidity_df[['ticker', 'confidence_score']], on='ticker', how='left')
    
    # Normalize each component to 0-1 range
    components = {}
    
    # Delta 24h (absolute value)
    if 'delta_24h' in df.columns:
        delta_abs = df['delta_24h'].fillna(0).abs()
        if delta_abs.max() > 0:
            components['delta_24h'] = delta_abs / delta_abs.max()
        else:
            components['delta_24h'] = 0
    else:
        components['delta_24h'] = 0
    
    # Volatility
    if df['volatility'].max() > 0:
        components['volatility'] = df['volatility'] / df['volatility'].max()
    else:
        components['volatility'] = 0
    
    # Attention (already normalized)
    components['attention'] = df['attention_score']
    
    # Confidence
    components['confidence'] = df['confidence_score'].fillna(0.5)
    
    # Weighted sum
    newsworthiness = (
        NEWSWORTHINESS_WEIGHTS['delta_24h'] * components['delta_24h'] +
        NEWSWORTHINESS_WEIGHTS['volatility'] * components['volatility'] +
        NEWSWORTHINESS_WEIGHTS['attention'] * components['attention'] +
        NEWSWORTHINESS_WEIGHTS['confidence'] * components['confidence']
    )
    
    df['newsworthiness'] = newsworthiness
    
    return df


# Compute signals
print("Computing signals...")

# Add probability changes
markets_df = compute_probability_changes(markets_df, snapshots_df)

# Add volatility
markets_df = compute_volatility(markets_df, snapshots_df)

# Add attention score
markets_df = compute_attention_score(markets_df)

# Add newsworthiness
markets_df = compute_newsworthiness(markets_df, liquidity_df)

print(f"✓ Computed signals for {len(markets_df)} markets")
print(f"  Average attention score: {markets_df['attention_score'].mean():.3f}")
print(f"  Average volatility: {markets_df['volatility'].mean():.3f}")
print(f"  Average newsworthiness: {markets_df['newsworthiness'].mean():.3f}")

# Display sample with signals
print("\nSample with signals:")
if not markets_df.empty:
    cols = ['title', 'yes_price', 'attention_score', 'volatility', 'newsworthiness']
    print(markets_df[cols].head(3))
