"""
MarketPress Hex Cell 7: Drill-Down Details
Timeline + fact box for selected market

Note: This cell requires Cell 1 (setup) to be run first for imports
"""

# Helper functions for formatting
def format_percentage(value: float) -> str:
    """Format a decimal as percentage"""
    if pd.isna(value):
        return "—"
    return f"{value * 100:.0f}%"


def format_change(value: float) -> str:
    """Format a change value with sign and arrow"""
    if pd.isna(value):
        return "—"
    
    arrow = "↑" if value > 0 else "↓" if value < 0 else "→"
    return f"{arrow} {abs(value) * 100:.1f}%"


def format_number(value: float) -> str:
    """Format large numbers with commas"""
    if pd.isna(value):
        return "—"
    return f"{int(value):,}"


def create_fact_box_df(market_id: str) -> pd.DataFrame:
    """
    Create a fact box dataframe for a specific market
    
    Returns DataFrame with key/value pairs or single-row dataframe
    """
    market = markets_df[markets_df['ticker'] == market_id]
    
    if market.empty:
        return pd.DataFrame()
    
    market = market.iloc[0]
    
    # Get liquidity data
    liq = liquidity_df[liquidity_df['ticker'] == market_id]
    if not liq.empty:
        liq = liq.iloc[0]
    else:
        liq = pd.Series({'spread': 0, 'confidence_score': 0, 'depth': 0})
    
    # Create fact box as single-row dataframe
    fact_box = pd.DataFrame([{
        'market_id': market_id,
        'title': market.get('title', ''),
        'category': market.get('section', market.get('category', '')),
        'status': market.get('status', ''),
        'close_time': market.get('close_time', ''),
        'implied_probability': format_percentage(market.get('yes_price')),
        'implied_probability_raw': market.get('yes_price', 0),
        'delta_24h': format_change(market.get('delta_24h')),
        'delta_24h_raw': market.get('delta_24h', 0),
        'delta_7d': format_change(market.get('delta_7d')),
        'delta_7d_raw': market.get('delta_7d', 0),
        'volume_24h': format_number(market.get('volume', 0)),
        'volume_24h_raw': market.get('volume', 0),
        'open_interest': format_number(market.get('open_interest', 0)),
        'open_interest_raw': market.get('open_interest', 0),
        'spread': format_percentage(liq.get('spread', 0)),
        'spread_raw': liq.get('spread', 0),
        'confidence_score': f"{liq.get('confidence_score', 0):.2f}",
        'confidence_score_raw': liq.get('confidence_score', 0),
        'volatility': f"{market.get('volatility', 0):.3f}",
        'volatility_raw': market.get('volatility', 0),
        'newsworthiness': f"{market.get('newsworthiness', 0):.2f}",
        'newsworthiness_raw': market.get('newsworthiness', 0),
        'attention_score': f"{market.get('attention_score', 0):.2f}",
        'attention_score_raw': market.get('attention_score', 0),
        'last_updated': datetime.now().strftime('%b %d, %I:%M %p')
    }])
    
    return fact_box


def get_timeline_df(market_id: str) -> pd.DataFrame:
    """
    Get timeline dataframe for a market (timestamp, prob, volume, oi)
    
    Returns DataFrame with historical price and volume data
    """
    timeline = snapshots_df[snapshots_df['ticker'] == market_id].copy()
    
    if timeline.empty:
        # No historical data, create single row with current data
        market = markets_df[markets_df['ticker'] == market_id]
        if not market.empty:
            market = market.iloc[0]
            return pd.DataFrame([{
                'timestamp': datetime.now().isoformat(),
                'prob': market.get('yes_price', 0),
                'volume': market.get('volume', 0),
                'open_interest': market.get('open_interest', 0)
            }])
        return pd.DataFrame()
    
    # Sort by timestamp
    timeline = timeline.sort_values('timestamp')
    
    # Rename and select columns for display
    timeline_df = pd.DataFrame({
        'timestamp': timeline['timestamp'],
        'prob': timeline['yes_price'],
        'volume': timeline.get('volume', 0),
        'open_interest': timeline.get('open_interest', 0) if 'open_interest' in timeline.columns else 0
    })
    
    return timeline_df


def get_orderbook_df(market_id: str) -> pd.DataFrame:
    """
    Get orderbook dataframe (optional - may not be available)
    
    Returns DataFrame with bid/ask levels or empty if not available
    """
    # Orderbook data is often not available via public API
    # Return empty dataframe gracefully
    return pd.DataFrame()


def create_sparkline_data(market_id: str, days: int = 7) -> list:
    """
    Create 7-day probability sparkline data
    
    Returns list of probability values over time
    """
    timeline = get_timeline_df(market_id)
    
    if timeline.empty:
        return []
    
    return timeline['prob'].tolist()


def display_fact_box(market_id: str):
    """Display a formatted fact box"""
    fact_box_df = create_fact_box_df(market_id)
    
    if fact_box_df.empty:
        print(f"Market {market_id} not found")
        return None
    
    fact_box = fact_box_df.iloc[0]
    
    print("="*80)
    print(f"📊 MARKET DETAILS: {fact_box['title']}")
    print("="*80)
    print()
    print(f"Market ID:           {fact_box['market_id']}")
    print(f"Category:            {fact_box['category']}")
    print(f"Status:              {fact_box['status']}")
    print()
    print("PRICING:")
    print(f"  Implied Probability:  {fact_box['implied_probability']}")
    print(f"  24h Change:           {fact_box['delta_24h']}")
    print(f"  7d Change:            {fact_box['delta_7d']}")
    print(f"  Spread:               {fact_box['spread']}")
    print()
    print("ACTIVITY:")
    print(f"  Volume (24h):         {fact_box['volume_24h']}")
    print(f"  Open Interest:        {fact_box['open_interest']}")
    print(f"  Attention Score:      {fact_box['attention_score']}")
    print()
    print("SIGNALS:")
    print(f"  Confidence Score:     {fact_box['confidence_score']}")
    print(f"  Volatility:           {fact_box['volatility']}")
    print(f"  Newsworthiness:       {fact_box['newsworthiness']}")
    print()
    print(f"Last Updated:         {fact_box['last_updated']}")
    print("="*80)
    
    # Show sparkline
    sparkline_data = create_sparkline_data(market_id)
    if sparkline_data:
        print(f"\n7-Day Price History: {len(sparkline_data)} data points")
    
    return fact_box_df


# Example: Display fact box for lead story
if not lead_story.empty:
    print("\nExample Drill-Down (Lead Story):")
    lead_ticker = lead_story.iloc[0]['ticker']
    fact_box_df = display_fact_box(lead_ticker)
    timeline_df = get_timeline_df(lead_ticker)
    orderbook_df = get_orderbook_df(lead_ticker)  # Will be empty if not available
    
    print(f"\nTimeline data: {len(timeline_df)} snapshots")
    if not orderbook_df.empty:
        print(f"Orderbook data: {len(orderbook_df)} levels")
    else:
        print("Orderbook data: not available (using public API)")
else:
    print("\n✓ Drill-down module ready (no markets to display)")
    fact_box_df = pd.DataFrame()
    timeline_df = pd.DataFrame()
    orderbook_df = pd.DataFrame()
