"""
MarketPress Hex Cell 5: Section Organization
Assign markets into: Lead Story, Top Stories, Politics, Business, Tech, Culture, Sports, Developing, Most Read
"""

def categorize_market(title: str, category: str) -> str:
    """
    Categorize a market based on title and category
    
    Returns:
        Section name (Politics, Business, Tech, Culture, Sports, or Unknown)
    """
    title_lower = title.lower()
    category_lower = category.lower()
    
    for section, keywords in CATEGORY_MAPPINGS.items():
        for keyword in keywords:
            if keyword in title_lower or keyword in category_lower:
                return section
    
    return 'Unknown'


def assign_sections(markets_df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign each market to a section
    """
    df = markets_df.copy()
    df['section'] = df.apply(lambda row: categorize_market(row['title'], row['category']), axis=1)
    return df


def get_lead_story(markets_df: pd.DataFrame) -> pd.DataFrame:
    """Get the single most newsworthy market"""
    if markets_df.empty:
        return pd.DataFrame()
    
    lead = markets_df.nlargest(1, 'newsworthiness')
    return lead


def get_top_stories(markets_df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Get top N most newsworthy markets across all categories"""
    if markets_df.empty:
        return pd.DataFrame()
    
    top = markets_df.nlargest(n, 'newsworthiness')
    return top


def get_section_markets(markets_df: pd.DataFrame, section: str, n: int = 10) -> pd.DataFrame:
    """Get top markets for a specific section"""
    section_df = markets_df[markets_df['section'] == section].copy()
    
    if section_df.empty:
        return pd.DataFrame()
    
    # Sort by newsworthiness
    section_df = section_df.nlargest(n, 'newsworthiness')
    
    return section_df


def get_developing_stories(markets_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Get "Developing" stories (high volatility + high attention)
    """
    if markets_df.empty:
        return pd.DataFrame()
    
    # High volatility markets
    developing = markets_df[markets_df['volatility'] > DEVELOPING_THRESHOLD].copy()
    
    # Sort by combination of volatility and attention
    developing['developing_score'] = developing['volatility'] * 0.6 + developing['attention_score'] * 0.4
    developing = developing.nlargest(n, 'developing_score')
    
    return developing


def get_most_read(markets_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Get markets with highest attention (Most Read proxy)"""
    if markets_df.empty:
        return pd.DataFrame()
    
    most_read = markets_df.nlargest(n, 'attention_score')
    return most_read


# Organize into sections
print("Organizing into sections...")

# Assign section to each market
markets_df = assign_sections(markets_df)

# Create section dataframes
lead_story = get_lead_story(markets_df)
top_stories = get_top_stories(markets_df, TOP_STORIES_COUNT)
politics = get_section_markets(markets_df, 'Politics', MAX_STORIES_PER_SECTION)
business = get_section_markets(markets_df, 'Business', MAX_STORIES_PER_SECTION)
tech = get_section_markets(markets_df, 'Tech', MAX_STORIES_PER_SECTION)
culture = get_section_markets(markets_df, 'Culture', MAX_STORIES_PER_SECTION)
sports = get_section_markets(markets_df, 'Sports', MAX_STORIES_PER_SECTION)
developing = get_developing_stories(markets_df, MAX_STORIES_PER_SECTION)
most_read = get_most_read(markets_df, MAX_STORIES_PER_SECTION)

print(f"✓ Organized into sections")
print(f"  Lead Story: {len(lead_story)} market")
print(f"  Top Stories: {len(top_stories)} markets")
print(f"  Politics: {len(politics)} markets")
print(f"  Business: {len(business)} markets")
print(f"  Tech: {len(tech)} markets")
print(f"  Culture: {len(culture)} markets")
print(f"  Sports: {len(sports)} markets")
print(f"  Developing: {len(developing)} markets")
print(f"  Most Read: {len(most_read)} markets")
