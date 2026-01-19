#!/usr/bin/env python3
"""
MarketPress Example Script
Demonstrates all major features of the MarketPress application
"""

from marketpress import create_marketpress_app
import pandas as pd

print("=" * 80)
print("MARKETPRESS DEMONSTRATION")
print("=" * 80)
print()

# Create app with demo data
print("1. Creating MarketPress instance...")
app = create_marketpress_app(limit=50, use_demo=True)
print("   ✓ App created and initialized\n")

# Show front page
print("2. Generating front page...")
front_page = app.generate_front_page()
print(front_page)
print()

# Show AI editor summary
print("3. AI Editor Summary...")
print(app.get_editor_summary())
print()

# Show specific sections as tables
print("4. Section Data Tables...\n")

sections_to_show = ['Top Stories', 'Politics', 'Business', 'Tech', 'Developing']

for section in sections_to_show:
    print(f"\n{section.upper()}:")
    print("-" * 80)
    
    df = app.get_section_dataframe(section)
    
    if not df.empty:
        # Show key columns
        cols_to_show = []
        for col in ['title', 'yes_price', 'delta_24h', 'volume', 'attention_score', 'newsworthiness']:
            if col in df.columns:
                cols_to_show.append(col)
        
        display_df = df[cols_to_show].head(5).copy()
        
        # Format for readability
        if 'yes_price' in display_df.columns:
            display_df['probability'] = display_df['yes_price'].apply(lambda x: f"{x*100:.0f}%" if pd.notna(x) else "N/A")
        
        if 'delta_24h' in display_df.columns:
            display_df['24h_change'] = display_df['delta_24h'].apply(lambda x: f"{x*100:+.0f}%" if pd.notna(x) else "—")
        
        # Show title, probability, and change
        for idx, row in display_df.iterrows():
            title = row.get('title', 'Unknown')[:65]
            prob = row.get('probability', 'N/A')
            change = row.get('24h_change', '—')
            print(f"  • {title}")
            print(f"    {prob} ({change} 24h)")
    else:
        print(f"  No {section.lower()} available")

print()

# Ask the editor questions
print("5. Ask the AI Editor...\n")

questions = [
    "How many markets are tracked?",
    "What are the top headlines?",
    "What's the biggest mover?",
    "How many political markets are active?",
    "What market has the most attention?",
]

for question in questions:
    answer = app.ask_editor(question)
    print(f"Q: {question}")
    print(f"A: {answer}")
    print()

# Show raw data tables info
print("6. Raw Data Tables...\n")
print(f"Markets table: {len(app.markets_df)} rows, {len(app.markets_df.columns)} columns")
print(f"Snapshots table: {len(app.snapshots_df)} rows, {len(app.snapshots_df.columns)} columns")
print(f"Liquidity table: {len(app.liquidity_df)} rows, {len(app.liquidity_df.columns)} columns")
print()

# Show column names
print("Markets table columns:")
print(", ".join(app.markets_df.columns.tolist()))
print()

# Show a sample market detail
if not app.markets_df.empty:
    print("7. Sample Market Detail...\n")
    sample_ticker = app.markets_df.iloc[0]['ticker']
    market = app.get_market_details(sample_ticker)
    
    if market is not None:
        print(f"Ticker: {market.get('ticker', 'N/A')}")
        print(f"Title: {market.get('title', 'N/A')}")
        print(f"Category: {market.get('category', 'N/A')}")
        print(f"Probability: {market.get('yes_price', 0)*100:.1f}%")
        print(f"24h Change: {market.get('delta_24h', 0)*100:+.1f}%")
        print(f"Volume: {market.get('volume', 0):,}")
        print(f"Open Interest: {market.get('open_interest', 0):,}")
        print(f"Attention Score: {market.get('attention_score', 0):.2f}")
        print(f"Confidence Score: {market.get('confidence_score', 0):.2f}")
        print(f"Newsworthiness: {market.get('newsworthiness', 0):.2f}")
        
        # Show sparkline if available
        sparkline = app.get_market_sparkline(sample_ticker)
        print(f"24h Trend: {sparkline}")

print()
print("=" * 80)
print("DEMONSTRATION COMPLETE")
print("=" * 80)
print()
print("Next steps:")
print("  1. Copy code to Hex notebook")
print("  2. Arrange cells in newspaper-style layout")
print("  3. Schedule auto-refresh for live updates")
print("  4. Share with your team!")
