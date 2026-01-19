"""
MarketPress Hex Cell 6: Front Page Layout
Build front page tables for Hex App layout with newspaper feel
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


def create_story_row(market: pd.Series) -> Dict:
    """
    Create a story row with all required fields
    
    Fields: market_id, title, category, probability, movement, attention, confidence, timestamp
    """
    return {
        'market_id': market.get('ticker', ''),
        'title': market.get('title', ''),
        'category': market.get('section', market.get('category', '')),
        'probability': format_percentage(market.get('yes_price')),
        'probability_raw': market.get('yes_price', 0),
        'delta_24h': format_change(market.get('delta_24h')),
        'delta_24h_raw': market.get('delta_24h', 0),
        'delta_7d': format_change(market.get('delta_7d')),
        'delta_7d_raw': market.get('delta_7d', 0),
        'volume': format_number(market.get('volume', 0)),
        'volume_raw': market.get('volume', 0),
        'attention': f"{market.get('attention_score', 0):.2f}",
        'attention_raw': market.get('attention_score', 0),
        'confidence': f"{market.get('confidence_score', 0):.2f}",
        'confidence_raw': market.get('confidence_score', 0),
        'volatility': f"{market.get('volatility', 0):.3f}",
        'volatility_raw': market.get('volatility', 0),
        'newsworthiness': f"{market.get('newsworthiness', 0):.2f}",
        'newsworthiness_raw': market.get('newsworthiness', 0),
        'spread': format_percentage(market.get('spread', 0)),
        'spread_raw': market.get('spread', 0),
        'last_updated': datetime.now().strftime('%b %d, %I:%M %p')
    }


def section_to_display_df(section_df: pd.DataFrame) -> pd.DataFrame:
    """Convert section dataframe to display format"""
    if section_df.empty:
        return pd.DataFrame()
    
    # Merge liquidity data if needed
    if 'spread' not in section_df.columns:
        section_df = section_df.merge(liquidity_df[['ticker', 'spread']], 
                                       left_on='ticker', right_on='ticker', how='left')
    
    rows = [create_story_row(row) for _, row in section_df.iterrows()]
    return pd.DataFrame(rows)


# Create display dataframes for each section
print("Building front page layout...")

lead_story_display = section_to_display_df(lead_story)
top_stories_display = section_to_display_df(top_stories)
politics_display = section_to_display_df(politics)
business_display = section_to_display_df(business)
tech_display = section_to_display_df(tech)
culture_display = section_to_display_df(culture)
sports_display = section_to_display_df(sports)
developing_display = section_to_display_df(developing)
most_read_display = section_to_display_df(most_read)

print("✓ Front page layout ready")

# Display sections
print("\n" + "="*80)
print("📰 MARKETPRESS - PREDICTION MARKET NEWS")
print(f"Updated: {datetime.now().strftime('%b %d, %I:%M %p')}")
print("="*80)

if not lead_story_display.empty:
    print("\n🔥 LEAD STORY")
    print("-"*80)
    story = lead_story_display.iloc[0]
    print(f"  {story['title']}")
    print(f"  Probability: {story['probability']} | 24h: {story['delta_24h']} | Attention: {story['attention']}")

if not top_stories_display.empty:
    print("\n📰 TOP STORIES")
    print("-"*80)
    for _, story in top_stories_display.iterrows():
        print(f"  • {story['title'][:70]}")
        print(f"    {story['probability']} | 24h: {story['delta_24h']}")
