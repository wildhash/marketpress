"""
MarketPress Hex Cell 3: Normalize Data
Normalize into tables: markets, snapshots, liquidity/spread metrics
"""

def normalize_markets_table(raw_markets: List[Dict]) -> pd.DataFrame:
    """
    Normalize raw market data into markets table
    
    Returns:
        DataFrame with columns: ticker, title, category, status, yes_price, volume, open_interest, close_time
    """
    records = []
    
    for market in raw_markets:
        # Calculate mid price from bid/ask
        yes_bid = market.get('yes_bid', 0.5)
        yes_ask = market.get('yes_ask', 0.5)
        yes_price = (yes_bid + yes_ask) / 2.0
        
        record = {
            'ticker': market.get('ticker', ''),
            'title': market.get('title', ''),
            'category': market.get('category', 'unknown'),
            'status': market.get('status', 'unknown'),
            'yes_price': yes_price,
            'yes_bid': yes_bid,
            'yes_ask': yes_ask,
            'volume': market.get('volume', 0),
            'open_interest': market.get('open_interest', 0),
            'close_time': market.get('close_time', ''),
        }
        records.append(record)
    
    df = pd.DataFrame(records)
    
    # Parse close_time
    if 'close_time' in df.columns and not df.empty:
        try:
            df['close_time'] = pd.to_datetime(df['close_time'])
        except:
            pass
    
    return df


def normalize_snapshots_table(markets_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create snapshots table for time-series data
    
    Returns:
        DataFrame with columns: ticker, timestamp, yes_price, volume, open_interest
    """
    now = datetime.now()
    
    records = []
    for _, market in markets_df.iterrows():
        record = {
            'ticker': market['ticker'],
            'timestamp': now,
            'yes_price': market['yes_price'],
            'volume': market['volume'],
            'open_interest': market['open_interest']
        }
        records.append(record)
    
    return pd.DataFrame(records)


def normalize_liquidity_spread_table(markets_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create liquidity/spread metrics table
    
    Returns:
        DataFrame with columns: ticker, spread, depth, confidence_score
    """
    records = []
    
    for _, market in markets_df.iterrows():
        spread = market['yes_ask'] - market['yes_bid']
        
        # Confidence score: tighter spread = higher confidence
        confidence_score = 1.0 - min(spread * 10, 1.0)  # Normalize to 0-1
        
        # Depth proxy using open interest
        depth = market['open_interest']
        
        record = {
            'ticker': market['ticker'],
            'spread': spread,
            'depth': depth,
            'confidence_score': confidence_score
        }
        records.append(record)
    
    return pd.DataFrame(records)


# Normalize data
print(f"Processing {len(raw_markets)} markets...")

markets_df = normalize_markets_table(raw_markets)
snapshots_df = normalize_snapshots_table(markets_df)
liquidity_df = normalize_liquidity_spread_table(markets_df)

print(f"✓ Normalized {len(markets_df)} markets into tables")
print(f"  Markets table: {markets_df.shape}")
print(f"  Snapshots table: {snapshots_df.shape}")
print(f"  Liquidity table: {liquidity_df.shape}")

# Display sample
print("\nSample markets:")
if not markets_df.empty:
    print(markets_df[['ticker', 'title', 'category', 'yes_price']].head(3))
