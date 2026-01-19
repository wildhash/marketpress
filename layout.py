"""
Layout and Sections Module
Organizes markets into newspaper-style sections
"""
import pandas as pd
from typing import Dict
from datetime import datetime


# Category mappings for section organization
CATEGORY_MAPPINGS = {
    'Politics': ['Politics', 'Elections', 'Government', 'Policy', 'Congress', 'Senate', 'President'],
    'Business': ['Business', 'Economics', 'Finance', 'Markets', 'Stocks', 'Economy', 'Trade'],
    'Tech': ['Technology', 'Tech', 'AI', 'Crypto', 'Innovation', 'Science', 'Space'],
    'Culture': ['Culture', 'Entertainment', 'Sports', 'Arts', 'Music', 'Movies', 'TV'],
    'Sports': ['Sports', 'Football', 'Basketball', 'Baseball', 'Soccer', 'Olympics'],
}


def categorize_market(row: pd.Series) -> str:
    """
    Categorize a market into a section
    
    Args:
        row: Market data row
        
    Returns:
        Section name
    """
    category = row.get('category', '').lower()
    title = row.get('title', '').lower()
    subtitle = row.get('subtitle', '').lower()
    
    combined_text = f"{category} {title} {subtitle}"
    
    # Check each section's keywords
    for section, keywords in CATEGORY_MAPPINGS.items():
        for keyword in keywords:
            if keyword.lower() in combined_text:
                return section
    
    return 'Other'


def organize_into_sections(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Organize markets into sections
    
    Args:
        df: Market data with computed signals
        
    Returns:
        Dictionary mapping section names to DataFrames
    """
    if df.empty:
        return {section: pd.DataFrame() for section in ['Top Stories'] + list(CATEGORY_MAPPINGS.keys())}
    
    df = df.copy()
    
    # Add section column
    df['section'] = df.apply(categorize_market, axis=1)
    
    sections = {}
    
    # Top Stories (highest newsworthiness across all categories)
    if 'newsworthiness' in df.columns:
        sections['Top Stories'] = df.nlargest(10, 'newsworthiness')
    else:
        sections['Top Stories'] = df.head(10)
    
    # Category sections
    for section_name in CATEGORY_MAPPINGS.keys():
        section_data = df[df['section'] == section_name].copy()
        
        # Sort by newsworthiness or attention
        if 'newsworthiness' in section_data.columns:
            section_data = section_data.sort_values('newsworthiness', ascending=False)
        elif 'attention_score' in section_data.columns:
            section_data = section_data.sort_values('attention_score', ascending=False)
        
        sections[section_name] = section_data.head(15)
    
    return sections


def identify_developing_stories(df: pd.DataFrame, 
                                volatility_threshold: float = 0.05,
                                delta_threshold: float = 0.05) -> pd.DataFrame:
    """
    Identify "developing" stories with recent significant changes
    
    Args:
        df: Market data with signals
        volatility_threshold: Minimum volatility to be considered developing
        delta_threshold: Minimum 24h change to be considered developing
        
    Returns:
        DataFrame with developing stories
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Stories are "developing" if they have:
    # 1. High recent volatility, OR
    # 2. Large recent change (>5%), OR
    # 3. High attention with moderate change
    
    developing = df[
        (df['volatility'].fillna(0) > volatility_threshold) |
        (df['delta_24h'].fillna(0).abs() > delta_threshold) |
        ((df['attention_score'].fillna(0) > 0.7) & (df['delta_24h'].fillna(0).abs() > 0.02))
    ].copy()
    
    # Sort by recency of change (highest attention and volatility first)
    if 'attention_score' in developing.columns and 'volatility' in developing.columns:
        max_volatility = developing['volatility'].max()
        volatility_normalized = (
            developing['volatility'].fillna(0) / max_volatility 
            if max_volatility > 0 
            else 0
        )
        developing['developing_score'] = (
            0.5 * developing['attention_score'].fillna(0) + 
            0.5 * volatility_normalized
        )
        developing = developing.sort_values('developing_score', ascending=False)
    
    return developing.head(10)


def create_section_summary(section_df: pd.DataFrame, section_name: str) -> Dict:
    """
    Create a summary of a section
    
    Args:
        section_df: DataFrame for the section
        section_name: Name of the section
        
    Returns:
        Dictionary with section summary stats
    """
    if section_df.empty:
        return {
            'section': section_name,
            'story_count': 0,
            'avg_probability': None,
            'total_volume': 0,
            'top_mover': None
        }
    
    # Find biggest mover
    top_mover = None
    if 'delta_24h' in section_df.columns:
        abs_deltas = section_df['delta_24h'].fillna(0).abs()
        if abs_deltas.max() > 0:
            top_idx = abs_deltas.idxmax()
            top_mover = section_df.loc[top_idx, 'title'] if 'title' in section_df.columns else None
    
    summary = {
        'section': section_name,
        'story_count': len(section_df),
        'avg_probability': section_df['yes_price'].mean() if 'yes_price' in section_df.columns else None,
        'total_volume': section_df['volume'].sum() if 'volume' in section_df.columns else 0,
        'top_mover': top_mover
    }
    
    return summary


def format_timestamp(dt: datetime = None) -> str:
    """
    Format timestamp for display (e.g., "Updated: Jan 19, 2:30 PM EST")
    
    Args:
        dt: Datetime to format (defaults to now)
        
    Returns:
        Formatted timestamp string
    """
    if dt is None:
        dt = datetime.now()
    
    return dt.strftime("Updated: %b %d, %I:%M %p")


def create_section_layout(sections: Dict[str, pd.DataFrame]) -> str:
    """
    Create a text-based layout of all sections
    
    Args:
        sections: Dictionary of section DataFrames
        
    Returns:
        Formatted layout string
    """
    layout = []
    layout.append("=" * 80)
    layout.append("MARKETPRESS: PREDICTION MARKET NEWS")
    layout.append(format_timestamp())
    layout.append("=" * 80)
    layout.append("")
    
    # Top Stories
    layout.append("📰 TOP STORIES")
    layout.append("-" * 80)
    if 'Top Stories' in sections and not sections['Top Stories'].empty:
        for idx, row in sections['Top Stories'].head(5).iterrows():
            title = row.get('title', 'Unknown')[:70]
            prob = row.get('yes_price', 0) * 100 if row.get('yes_price') else 0
            delta = row.get('delta_24h', 0) * 100 if row.get('delta_24h') else 0
            sign = "+" if delta >= 0 else ""
            layout.append(f"  • {title}")
            layout.append(f"    {prob:.0f}% ({sign}{delta:.0f}% 24h)")
            layout.append("")
    else:
        layout.append("  No stories available")
        layout.append("")
    
    # Category sections
    section_icons = {
        'Politics': '🏛️',
        'Business': '💼',
        'Tech': '💻',
        'Culture': '🎭',
        'Sports': '⚽'
    }
    
    for section_name in ['Politics', 'Business', 'Tech', 'Culture', 'Sports']:
        icon = section_icons.get(section_name, '📌')
        layout.append(f"{icon} {section_name.upper()}")
        layout.append("-" * 80)
        
        if section_name in sections and not sections[section_name].empty:
            for idx, row in sections[section_name].head(3).iterrows():
                title = row.get('title', 'Unknown')[:70]
                prob = row.get('yes_price', 0) * 100 if row.get('yes_price') else 0
                layout.append(f"  • {title} ({prob:.0f}%)")
        else:
            layout.append(f"  No {section_name.lower()} stories")
        
        layout.append("")
    
    # Developing stories
    if 'Developing' in sections and not sections['Developing'].empty:
        layout.append("🚨 DEVELOPING STORIES")
        layout.append("-" * 80)
        for idx, row in sections['Developing'].head(3).iterrows():
            title = row.get('title', 'Unknown')[:70]
            prob = row.get('yes_price', 0) * 100 if row.get('yes_price') else 0
            layout.append(f"  • {title} ({prob:.0f}%)")
        layout.append("")
    
    layout.append("=" * 80)
    
    return "\n".join(layout)
