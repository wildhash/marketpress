"""
MarketPress Hex Cell 7: Drill-Down Details
Timeline + fact box for selected market
"""

def create_fact_box(market_id: str) -> Dict:
    """
    Create a fact box for a specific market
    
    Returns dict with:
    - implied_probability
    - delta_24h
    - delta_7d
    - volume_24h
    - attention_score
    - spread
    - confidence_score
    - last_updated
    """
    market = markets_df[markets_df['ticker'] == market_id]
    
    if market.empty:
        return {}
    
    market = market.iloc[0]
    
    # Get liquidity data
    liq = liquidity_df[liquidity_df['ticker'] == market_id]
    if not liq.empty:
        liq = liq.iloc[0]
    else:
        liq = pd.Series({'spread': 0, 'confidence_score': 0})
    
    fact_box = {
        'market_id': market_id,
        'title': market.get('title', ''),
        'implied_probability': format_percentage(market.get('yes_price')),
        'implied_probability_raw': market.get('yes_price', 0),
        'delta_24h': format_change(market.get('delta_24h')),
        'delta_24h_raw': market.get('delta_24h', 0),
        'delta_7d': format_change(market.get('delta_7d')),
        'delta_7d_raw': market.get('delta_7d', 0),
        'volume_24h': format_number(market.get('volume', 0)),
        'volume_24h_raw': market.get('volume', 0),
        'attention_score': f"{market.get('attention_score', 0):.2f}",
        'attention_score_raw': market.get('attention_score', 0),
        'spread': format_percentage(liq.get('spread', 0)),
        'spread_raw': liq.get('spread', 0),
        'confidence_score': f"{liq.get('confidence_score', 0):.2f}",
        'confidence_score_raw': liq.get('confidence_score', 0),
        'open_interest': format_number(market.get('open_interest', 0)),
        'open_interest_raw': market.get('open_interest', 0),
        'volatility': f"{market.get('volatility', 0):.3f}",
        'volatility_raw': market.get('volatility', 0),
        'newsworthiness': f"{market.get('newsworthiness', 0):.2f}",
        'newsworthiness_raw': market.get('newsworthiness', 0),
        'category': market.get('section', market.get('category', '')),
        'status': market.get('status', ''),
        'close_time': market.get('close_time', ''),
        'last_updated': datetime.now().strftime('%b %d, %I:%M %p')
    }
    
    return fact_box


def get_market_timeline(market_id: str) -> pd.DataFrame:
    """
    Get timeline of price changes for a market
    
    Returns DataFrame with timestamps and prices
    """
    timeline = snapshots_df[snapshots_df['ticker'] == market_id].copy()
    
    if not timeline.empty:
        timeline = timeline.sort_values('timestamp')
    
    return timeline


def create_sparkline_data(market_id: str, days: int = 7) -> List[float]:
    """
    Create 7-day probability sparkline data
    
    Returns list of probability values over time
    """
    timeline = get_market_timeline(market_id)
    
    if timeline.empty:
        # No historical data yet, return current price
        market = markets_df[markets_df['ticker'] == market_id]
        if not market.empty:
            return [market.iloc[0]['yes_price']]
        return []
    
    return timeline['yes_price'].tolist()


def display_fact_box(market_id: str):
    """Display a formatted fact box"""
    fact_box = create_fact_box(market_id)
    
    if not fact_box:
        print(f"Market {market_id} not found")
        return
    
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
        print(f"\n7-Day Price History: {sparkline_data}")
    
    return fact_box


# Example: Display fact box for lead story
if not lead_story.empty:
    print("\nExample Drill-Down (Lead Story):")
    lead_ticker = lead_story.iloc[0]['ticker']
    lead_fact_box = display_fact_box(lead_ticker)
else:
    print("\n✓ Drill-down module ready (no markets to display)")
    lead_fact_box = {}
