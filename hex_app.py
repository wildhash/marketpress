"""
MarketPress Hex Application Template
Copy this code into Hex cells to create the MarketPress front page

This template provides a complete newspaper-style layout with:
- Top Stories section
- Category sections (Politics, Business, Tech, Culture, Sports)
- Developing stories
- AI Editor with summarization and Q&A
- Mini sparklines and timestamps
"""

# ============================================================================
# CELL 1: Setup and Initialization
# ============================================================================
"""
Install dependencies (run once)
"""
# !pip install requests pandas numpy plotly python-dateutil

# Import the MarketPress application
from marketpress import create_marketpress_app

# Initialize the application (fetches live Kalshi data)
app = create_marketpress_app(limit=100)

print("✓ MarketPress initialized with live Kalshi data")


# ============================================================================
# CELL 2: Front Page Display
# ============================================================================
"""
Display the complete front page in text format
"""
front_page = get_front_page_text(app)
print(front_page)


# ============================================================================
# CELL 3: Top Stories Section
# ============================================================================
"""
Top Stories - Most newsworthy markets across all categories
"""
top_stories_df = app.get_section_dataframe('Top Stories')

# Display as table
if not top_stories_df.empty:
    # Select columns that exist
    cols_to_display = []
    for col in ['title', 'yes_price', 'delta_24h', 'volume', 'attention_score']:
        if col in top_stories_df.columns:
            cols_to_display.append(col)
    
    if cols_to_display:
        display_df = top_stories_df[cols_to_display].head(10).copy()
        
        # Format columns
        col_names = {'title': 'Market', 'yes_price': 'Probability', 'delta_24h': '24h Change', 'volume': 'Volume', 'attention_score': 'Attention'}
        display_df.columns = [col_names.get(col, col) for col in cols_to_display]
        
        # Add sparklines if ticker column exists
        if 'ticker' in top_stories_df.columns:
            display_df['Trend'] = top_stories_df.head(10)['ticker'].apply(
                lambda ticker: app.get_market_sparkline(ticker) if ticker else '─────'
            )
        
        display_df
    else:
        print("No columns available to display")
else:
    print("No top stories available")


# ============================================================================
# CELL 4: Politics Section
# ============================================================================
"""
Politics - Political markets and elections
"""
politics_df = get_section_table(app, 'Politics')

if not politics_df.empty:
    display_df = politics_df[['title', 'probability', '24h_change', 'volume']].head(10).copy()
    display_df.columns = ['Market', 'Probability', '24h Change', 'Volume']
    display_df
else:
    print("No political markets available")


# ============================================================================
# CELL 5: Business Section
# ============================================================================
"""
Business - Economic and financial markets
"""
business_df = get_section_table(app, 'Business')

if not business_df.empty:
    display_df = business_df[['title', 'probability', '24h_change', 'volume']].head(10).copy()
    display_df.columns = ['Market', 'Probability', '24h Change', 'Volume']
    display_df
else:
    print("No business markets available")


# ============================================================================
# CELL 6: Tech Section
# ============================================================================
"""
Tech - Technology, AI, and innovation markets
"""
tech_df = get_section_table(app, 'Tech')

if not tech_df.empty:
    display_df = tech_df[['title', 'probability', '24h_change', 'volume']].head(10).copy()
    display_df.columns = ['Market', 'Probability', '24h Change', 'Volume']
    display_df
else:
    print("No tech markets available")


# ============================================================================
# CELL 7: Culture Section
# ============================================================================
"""
Culture - Entertainment, arts, and cultural markets
"""
culture_df = get_section_table(app, 'Culture')

if not culture_df.empty:
    display_df = culture_df[['title', 'probability', '24h_change', 'volume']].head(10).copy()
    display_df.columns = ['Market', 'Probability', '24h Change', 'Volume']
    display_df
else:
    print("No culture markets available")


# ============================================================================
# CELL 8: Sports Section
# ============================================================================
"""
Sports - Sports betting and competition markets
"""
sports_df = get_section_table(app, 'Sports')

if not sports_df.empty:
    display_df = sports_df[['title', 'probability', '24h_change', 'volume']].head(10).copy()
    display_df.columns = ['Market', 'Probability', '24h Change', 'Volume']
    display_df
else:
    print("No sports markets available")


# ============================================================================
# CELL 9: Developing Stories
# ============================================================================
"""
Developing Stories - Markets with high volatility and recent significant changes
"""
developing_df = app.get_section_dataframe('Developing')

if not developing_df.empty:
    # Select available columns with fallbacks
    cols = [col for col in ['title', 'yes_price', 'delta_24h', 'volatility', 'attention_score'] if col in developing_df.columns]
    if cols:
        display_df = developing_df[cols].head(10).copy()
        # Rename columns for display
        col_map = {'title': 'Market', 'yes_price': 'Probability', 'delta_24h': '24h Change', 'volatility': 'Volatility', 'attention_score': 'Attention'}
        display_df.columns = [col_map.get(col, col) for col in cols]
        display_df
    else:
        print("No columns available")
else:
    print("No developing stories at this time")


# ============================================================================
# CELL 10: AI Editor Summary
# ============================================================================
"""
AI Editor's Summary of the Front Page
"""
editor_summary = get_editor_summary(app)
print(editor_summary)


# ============================================================================
# CELL 11: Ask the Editor (Interactive Q&A)
# ============================================================================
"""
Ask the AI Editor questions about the markets
"""
# Example questions - modify as needed
questions = [
    "What are the top headlines?",
    "What's the biggest mover today?",
    "How many political markets are active?",
    "What market has the most attention?",
]

for question in questions:
    print(f"\nQ: {question}")
    answer = ask_editor_question(app, question)
    print(f"A: {answer}")
    print("-" * 60)


# ============================================================================
# CELL 12: Data Tables (Raw Data Access)
# ============================================================================
"""
Access to raw normalized data tables
"""
print("Available data tables:")
print(f"  - Markets: {len(app.markets_df)} rows")
print(f"  - Snapshots: {len(app.snapshots_df)} rows")
print(f"  - Liquidity: {len(app.liquidity_df)} rows")

# Display raw markets table
print("\nMarkets Table (first 10 rows):")
app.markets_df.head(10)


# ============================================================================
# CELL 13: Refresh Data
# ============================================================================
"""
Refresh data from Kalshi API
Run this cell to fetch fresh market data
"""
app.refresh(limit=100)
print("✓ Data refreshed successfully")


# ============================================================================
# CELL 14: Custom Hex Thread Editor Integration
# ============================================================================
"""
Hex Thread Editor Integration
This enables semantic search and Q&A over the market data
"""

# For Hex Thread integration, expose the semantic model
semantic_model = {
    'markets': app.markets_df.to_dict('records'),
    'sections': {name: df.to_dict('records') for name, df in app.sections.items()},
    'summary': app.editor.semantic_model if app.editor else {}
}

# Thread can now query this model
print("Semantic model ready for Hex Thread queries")
print(f"Model contains {len(semantic_model['markets'])} markets across {len(semantic_model['sections'])} sections")


# ============================================================================
# NOTES FOR HEX USERS
# ============================================================================
"""
Tips for using MarketPress in Hex:

1. LAYOUT: Arrange cells in a newspaper-style layout using Hex's grid layout
2. SPARKLINES: Mini sparklines are included in the trend column
3. TIMESTAMPS: All sections show "Updated: [timestamp]" in headers
4. AUTO-REFRESH: Use Hex's scheduled runs to auto-refresh data
5. INTERACTIVITY: Add Hex input components for custom queries to the editor
6. VISUALIZATION: Use Plotly for enhanced sparkline visualizations
7. THREAD EDITOR: The semantic model is exposed for Hex Thread integration

DEPLOYMENT:
- Publish the Hex notebook to create a shareable MarketPress front page
- Schedule automatic refreshes to keep data current
- Share with teams for collaborative market analysis
"""
