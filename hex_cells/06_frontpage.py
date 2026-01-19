"""
MarketPress Hex Cell 6: Front Page Layout
Build front page tables for Hex App layout with newspaper feel

Note: This cell requires Cell 1 (setup) to be run first for imports
"""

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


def generate_dek(market: pd.Series) -> str:
    """
    Generate a one-sentence "dek" (subheadline/deck) for a market
    
    A "dek" is newspaper terminology for a brief subheadline that provides
    additional context below the main headline.
    
    Format: "YES at XX% (+/-Y.Y pts / 24h), [volume descriptor], [spread descriptor]"
    """
    prob = market.get('yes_price', 0) * 100
    delta = market.get('delta_24h', 0) * 100
    volume = market.get('volume', 0)
    spread = market.get('spread', 0) * 100
    
    # Delta description
    if abs(delta) > 10:
        delta_desc = f"{'+' if delta > 0 else ''}{delta:.1f} pts / 24h"
    elif abs(delta) > 3:
        delta_desc = f"{'+' if delta > 0 else ''}{delta:.1f} pts / 24h"
    else:
        delta_desc = "stable"
    
    # Volume description
    if volume > 100000:
        vol_desc = "heavy volume"
    elif volume > 50000:
        vol_desc = "active trading"
    elif volume > 10000:
        vol_desc = "moderate volume"
    else:
        vol_desc = "light volume"
    
    # Spread description
    if spread < 2:
        spread_desc = "tight spread"
    elif spread < 5:
        spread_desc = "normal spread"
    else:
        spread_desc = "wide spread"
    
    return f"YES at {prob:.0f}% ({delta_desc}), {vol_desc}, {spread_desc}"


def get_sparkline_series(market_id: str, days: int = 7) -> list:
    """
    Get sparkline data for a market (7-day price history)
    
    Returns list of probability values for charting
    """
    timeline = snapshots_df[snapshots_df['ticker'] == market_id].copy()
    
    if timeline.empty:
        # No historical data, return current price
        market = markets_df[markets_df['ticker'] == market_id]
        if not market.empty:
            current_price = market.iloc[0].get('yes_price', 0)
            return [current_price] * 7  # Flat line
        return [0] * 7
    
    # Sort and get last 7 days
    timeline = timeline.sort_values('timestamp')
    prices = timeline['yes_price'].tolist()
    
    # Return last 7 points or pad if fewer
    if len(prices) >= 7:
        return prices[-7:]
    else:
        # Pad with first value to reach 7 points
        padding = [prices[0]] * (7 - len(prices))
        return padding + prices


def create_story_row(market: pd.Series) -> Dict:
    """
    Create a story row with all required fields for newspaper display
    
    Fields: market_id, headline, category, prob_now, delta_24h, delta_7d, 
            volume_24h, open_interest, spread, confidence_score, 
            newsworthiness, last_updated, dek, sparkline_series
    """
    market_id = market.get('ticker', '')
    
    # Get liquidity data
    liq = liquidity_df[liquidity_df['ticker'] == market_id]
    if not liq.empty:
        liq = liq.iloc[0]
        spread_val = liq.get('spread', 0)
        confidence_val = liq.get('confidence_score', 0)
    else:
        spread_val = 0
        confidence_val = 0
    
    return {
        'market_id': market_id,
        'headline': market.get('title', ''),
        'category': market.get('section', market.get('category', '')),
        'prob_now': format_percentage(market.get('yes_price')),
        'prob_now_raw': market.get('yes_price', 0),
        'delta_24h': format_change(market.get('delta_24h')),
        'delta_24h_raw': market.get('delta_24h', 0),
        'delta_7d': format_change(market.get('delta_7d')),
        'delta_7d_raw': market.get('delta_7d', 0),
        'volume_24h': format_number(market.get('volume', 0)),
        'volume_24h_raw': market.get('volume', 0),
        'open_interest': format_number(market.get('open_interest', 0)),
        'open_interest_raw': market.get('open_interest', 0),
        'spread': format_percentage(spread_val),
        'spread_raw': spread_val,
        'confidence_score': f"{confidence_val:.2f}",
        'confidence_score_raw': confidence_val,
        'newsworthiness': f"{market.get('newsworthiness', 0):.2f}",
        'newsworthiness_raw': market.get('newsworthiness', 0),
        'last_updated': datetime.now().strftime('%b %d, %I:%M %p'),
        'dek': generate_dek(market),
        'sparkline_series': get_sparkline_series(market_id)
    }


def section_to_display_df(section_df: pd.DataFrame) -> pd.DataFrame:
    """Convert section dataframe to display format"""
    if section_df.empty:
        return pd.DataFrame()
    
    rows = [create_story_row(row) for _, row in section_df.iterrows()]
    return pd.DataFrame(rows)


# Create display dataframes for each section
print("Building front page layout...")

# Generate all section dataframes with full newspaper columns
lead_story_df = section_to_display_df(lead_story)
top_stories_df = section_to_display_df(top_stories)
politics_df = section_to_display_df(politics)
business_df = section_to_display_df(business)
tech_df = section_to_display_df(tech)
culture_df = section_to_display_df(culture)
sports_df = section_to_display_df(sports)
developing_df = section_to_display_df(developing)
most_read_df = section_to_display_df(most_read)

# Create ticker tape (top movers - small rows)
if not markets_df.empty:
    ticker_tape = markets_df.nlargest(10, 'delta_24h') if 'delta_24h' in markets_df.columns else markets_df.head(10)
    ticker_tape_df = section_to_display_df(ticker_tape)
else:
    ticker_tape_df = pd.DataFrame()

print("✓ Front page layout ready")
print(f"  - Lead Story: {len(lead_story_df)} market")
print(f"  - Top Stories: {len(top_stories_df)} markets")
print(f"  - Politics: {len(politics_df)} markets")
print(f"  - Business: {len(business_df)} markets")
print(f"  - Tech: {len(tech_df)} markets")
print(f"  - Culture: {len(culture_df)} markets")
print(f"  - Sports: {len(sports_df)} markets")
print(f"  - Developing: {len(developing_df)} markets")
print(f"  - Most Read: {len(most_read_df)} markets")
print(f"  - Ticker Tape: {len(ticker_tape_df)} markets")

# Display sections
print("\n" + "="*80)
print("📰 MARKETPRESS - PREDICTION MARKET NEWS")
print(f"Updated: {datetime.now().strftime('%b %d, %I:%M %p')}")
print(f"📊 {banner_text}")
print("="*80)

if not lead_story_df.empty:
    print("\n🔥 LEAD STORY")
    print("-"*80)
    story = lead_story_df.iloc[0]
    print(f"  {story['headline']}")
    print(f"  {story['dek']}")
    print(f"  Newsworthiness: {story['newsworthiness']}")

if not top_stories_df.empty:
    print("\n📰 TOP STORIES")
    print("-"*80)
    for idx, story in top_stories_df.head(5).iterrows():
        print(f"  • {story['headline'][:70]}")
        print(f"    {story['dek'][:80]}")
