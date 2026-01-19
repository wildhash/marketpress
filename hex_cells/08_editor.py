"""
MarketPress Hex Cell 8: Editor Desk (Hex Threads)
Functions for Hex Threads "Editor Desk" prompts
"""

def summarize_front_page() -> str:
    """
    Generate executive summary of the front page
    """
    total_markets = len(markets_df)
    
    # Get section counts
    section_counts = markets_df['section'].value_counts().to_dict()
    
    # Get top headlines
    top_headlines = []
    if not top_stories.empty:
        for _, story in top_stories.head(3).iterrows():
            prob = format_percentage(story.get('yes_price'))
            top_headlines.append(f"{story.get('title', 'Unknown')}: {prob}")
    
    # Most watched
    most_watched = ""
    if not most_read.empty:
        most_watched = most_read.iloc[0].get('title', 'N/A')
    
    summary = f"""📰 MARKETPRESS EDITOR'S SUMMARY
{'='*60}

Tracking {total_markets} active prediction markets today.

TOP HEADLINES:
"""
    
    for headline in top_headlines:
        summary += f"  • {headline}\n"
    
    summary += f"\nMOST WATCHED: {most_watched}\n"
    
    summary += "\nSECTION HIGHLIGHTS:\n"
    for section in ['Politics', 'Business', 'Tech', 'Culture', 'Sports']:
        count = section_counts.get(section, 0)
        summary += f"  {section}: {count} active markets\n"
    
    summary += "\n" + "="*60
    
    return summary


def biggest_belief_shifts() -> pd.DataFrame:
    """
    Identify markets with biggest probability changes
    
    Returns DataFrame of top movers
    """
    if 'delta_24h' not in markets_df.columns:
        return pd.DataFrame()
    
    # Get absolute changes
    movers = markets_df.copy()
    movers['abs_delta'] = movers['delta_24h'].fillna(0).abs()
    
    # Top 10 movers
    top_movers = movers.nlargest(10, 'abs_delta')
    
    # Format for display
    result = top_movers[['title', 'yes_price', 'delta_24h', 'volume']].copy()
    result.columns = ['Market', 'Current Probability', '24h Change', 'Volume']
    
    return result


def most_unstable_markets() -> pd.DataFrame:
    """
    Identify markets with highest volatility
    
    Returns DataFrame of most volatile markets
    """
    unstable = markets_df.nlargest(10, 'volatility')
    
    result = unstable[['title', 'yes_price', 'volatility', 'attention_score']].copy()
    result.columns = ['Market', 'Probability', 'Volatility', 'Attention']
    
    return result


def fun_desk() -> pd.DataFrame:
    """
    "Fun Desk": weird movers with real liquidity
    
    Markets with unusual characteristics but good volume
    """
    # Markets with good volume
    min_volume = markets_df['volume'].quantile(0.5)
    liquid = markets_df[markets_df['volume'] >= min_volume].copy()
    
    if liquid.empty:
        return pd.DataFrame()
    
    # Weird = extreme probabilities (very low or very high) or high volatility
    liquid['weirdness'] = liquid.apply(
        lambda row: (
            abs(row['yes_price'] - 0.5) * 0.5 +  # Distance from 50%
            row['volatility'] * 0.5  # Volatility
        ),
        axis=1
    )
    
    fun = liquid.nlargest(10, 'weirdness')
    
    result = fun[['title', 'yes_price', 'volume', 'weirdness']].copy()
    result.columns = ['Market', 'Probability', 'Volume', 'Weirdness Score']
    
    return result


def serious_desk() -> pd.DataFrame:
    """
    "Serious Desk": high-stakes, high-confidence markets
    
    Markets with high volume, tight spreads, and significant implications
    """
    # Merge liquidity data
    serious = markets_df.merge(liquidity_df[['ticker', 'confidence_score']], on='ticker', how='left')
    
    # High volume and high confidence
    serious['seriousness'] = (
        serious['attention_score'] * 0.5 +
        serious['confidence_score'] * 0.5
    )
    
    serious = serious.nlargest(10, 'seriousness')
    
    result = serious[['title', 'yes_price', 'volume', 'confidence_score']].copy()
    result.columns = ['Market', 'Probability', 'Volume', 'Confidence']
    
    return result


def answer_query(query: str) -> str:
    """
    Answer natural language queries about markets
    
    Simple pattern matching for common questions
    """
    query_lower = query.lower()
    
    # Market count
    if 'how many' in query_lower and 'market' in query_lower:
        return f"Currently tracking {len(markets_df)} active markets."
    
    # Category-specific questions
    for section in ['politics', 'business', 'tech', 'culture', 'sports']:
        if section in query_lower:
            count = len(markets_df[markets_df['section'] == section.title()])
            return f"There are {count} active markets in {section.title()}."
    
    # Top headlines
    if 'top' in query_lower and ('headline' in query_lower or 'stories' in query_lower):
        if not top_stories.empty:
            headlines = []
            for _, story in top_stories.head(5).iterrows():
                prob = format_percentage(story.get('yes_price'))
                headlines.append(f"{story.get('title')}: {prob}")
            return "Top headlines:\n" + "\n".join(f"  • {h}" for h in headlines)
    
    # Biggest mover
    if 'biggest' in query_lower and 'mover' in query_lower:
        if 'delta_24h' in markets_df.columns:
            movers = markets_df.copy()
            movers['abs_delta'] = movers['delta_24h'].fillna(0).abs()
            if not movers.empty:
                top_mover = movers.nlargest(1, 'abs_delta').iloc[0]
                return f"Biggest mover: {top_mover['title']} ({format_change(top_mover['delta_24h'])} in 24h)"
    
    # Most attention
    if 'most attention' in query_lower or 'most watched' in query_lower:
        if not most_read.empty:
            top = most_read.iloc[0]
            return f"Most watched: {top['title']} (attention score: {top['attention_score']:.2f})"
    
    return "I can answer questions about market counts, sections, top headlines, biggest movers, and most-watched markets."


# Generate summaries
print("="*80)
print(summarize_front_page())
print()

print("\n" + "="*80)
print("📊 EDITOR DESK FUNCTIONS READY")
print("="*80)
print("\nAvailable functions:")
print("  • summarize_front_page() - Executive summary")
print("  • biggest_belief_shifts() - Top movers")
print("  • most_unstable_markets() - High volatility markets")
print("  • fun_desk() - Weird movers with liquidity")
print("  • serious_desk() - High-stakes markets")
print("  • answer_query(question) - Natural language Q&A")
print()
print("Example queries for Hex Threads:")
print("  - 'Write today's front page in 8 headlines'")
print("  - 'What's the biggest belief shift since yesterday?'")
print("  - 'Show me the fun desk: weird movers with real liquidity'")
print("  - 'Which categories are most unstable right now?'")
