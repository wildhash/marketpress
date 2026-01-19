# MarketPress 📰

A BBC/Yahoo-style newspaper front page for prediction markets. MarketPress transforms live Kalshi market data into a clean, organized news layout with AI-powered insights.

## Features

### 🔄 Live Data Ingestion
- Fetches real-time market data from Kalshi's public API
- Enriches data with orderbook and trade information
- Automatic rate limiting and error handling

### 📊 Data Normalization
Three core tables:
- **Markets**: Core market information (ticker, title, category, status, prices)
- **Snapshots**: Time-series price and volume data for trend analysis
- **Liquidity/Spread**: Orderbook depth, spreads, and confidence metrics

### 📈 Signal Computation
Computes key trading signals:
- **Probability Changes**: Δ24h and Δ7d price movements
- **Volatility**: Standard deviation of prices over time windows
- **Attention**: Volume and open interest-based engagement scores
- **Confidence**: Spread-based market confidence metrics
- **Newsworthiness**: Composite score ranking market importance

### 📰 Newspaper Layout
Organized sections like a real newspaper:
- **Top Stories**: Highest newsworthiness across all categories
- **Politics**: Elections, government, policy markets
- **Business**: Economics, finance, trade markets
- **Tech**: Technology, AI, innovation markets
- **Culture**: Entertainment, arts, cultural events
- **Sports**: Sports betting and competition markets
- **Developing**: High-volatility markets with recent changes

### 📉 Mini Sparklines
- ASCII/Unicode sparklines for 24h price trends
- SVG sparklines for richer visualizations
- Trend arrows (↑/↓/→) and color coding

### 🤖 AI Editor
Intelligent summarization and Q&A:
- Generates executive summaries of the front page
- Identifies biggest movers and most-watched markets
- Answers natural language queries about market data
- Semantic model for deep market understanding

### ⏰ Timestamps
All sections include "Updated: [time]" timestamps for freshness

## Installation

```bash
# Clone the repository
git clone https://github.com/wildhash/marketpress.git
cd marketpress

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Standalone Python

```python
from marketpress import create_marketpress_app

# Initialize and fetch data
app = create_marketpress_app(limit=100)

# Display the front page
print(app.generate_front_page())

# Get AI editor summary
print(app.get_editor_summary())

# Ask questions
print(app.ask_editor("What's the biggest mover today?"))

# Access specific sections
politics_df = app.get_section_dataframe('Politics')
print(politics_df.head())
```

### In Hex

1. Create a new Hex notebook
2. Upload all `.py` files from this repository
3. Copy the code from `hex_app.py` into separate Hex cells
4. Run cells to create the front page layout
5. Arrange cells in Hex's grid layout for newspaper-style presentation

### Hex Thread Integration

The AI Editor is designed to work with Hex Thread:

```python
# The semantic model is automatically built
semantic_model = app.editor.semantic_model

# Use in Hex Thread for natural language queries
# Thread can understand: market counts, trends, movers, attention, etc.
```

## Architecture

```
MarketPress
├── kalshi_api.py          # Kalshi API client
├── data_normalization.py  # Data table schemas
├── signals.py             # Signal computation
├── visualization.py       # Sparklines and formatting
├── layout.py              # Section organization
├── editor.py              # AI Editor with semantic model
├── marketpress.py         # Main application
└── hex_app.py            # Hex notebook template
```

## Data Flow

```
Kalshi API → Raw Markets → Normalized Tables → Signal Computation
                                ↓
                         Section Organization
                                ↓
                    ┌──────────────────────┐
                    │   MarketPress App    │
                    ├──────────────────────┤
                    │ - Front Page Layout  │
                    │ - Section Tables     │
                    │ - AI Editor          │
                    │ - Sparklines         │
                    │ - Timestamps         │
                    └──────────────────────┘
```

## API Reference

### Main Classes

#### `MarketPress`
Main application class that coordinates all components.

**Methods:**
- `fetch_data(limit)`: Fetch fresh data from Kalshi
- `compute_signals()`: Calculate all trading signals
- `organize_sections()`: Organize markets into sections
- `generate_front_page()`: Create formatted front page text
- `get_section_dataframe(section_name)`: Get specific section data
- `get_editor_summary()`: Get AI editor's summary
- `ask_editor(query)`: Ask editor a question
- `refresh(limit)`: Complete refresh cycle

#### `KalshiAPI`
Client for Kalshi's public API.

**Methods:**
- `get_markets(limit, status)`: Fetch markets
- `get_orderbook(ticker)`: Get orderbook for a market
- `get_trades(ticker, limit)`: Get recent trades
- `get_events(limit, status)`: Get events

#### `MarketPressEditor`
AI-powered editor for summarization and Q&A.

**Methods:**
- `summarize_front_page()`: Generate executive summary
- `answer_query(query)`: Answer questions about markets

## Configuration

No configuration required! The app uses Kalshi's public API endpoints by default.

Optional customization:
```python
# Adjust fetch limits
app.fetch_data(limit=200)

# Adjust top stories count
from signals import rank_top_stories
top_stories = rank_top_stories(markets_df, n=20)

# Customize section categories
from layout import CATEGORY_MAPPINGS
CATEGORY_MAPPINGS['YourSection'] = ['keyword1', 'keyword2']
```

## Examples

### Display Top Movers
```python
app = create_marketpress_app(limit=100)
top_stories = app.get_section_dataframe('Top Stories')
print(top_stories[['title', 'yes_price', 'delta_24h']].head(10))
```

### Track Specific Market
```python
market = app.get_market_details('TICKER-SYMBOL')
sparkline = app.get_market_sparkline('TICKER-SYMBOL')
print(f"{market['title']}: {sparkline}")
```

### Monitor Developing Stories
```python
developing = app.get_section_dataframe('Developing')
print(developing[['title', 'volatility', 'attention_score']])
```

## Hex Deployment Guide

1. **Create Hex Project**: New Python notebook
2. **Upload Files**: All `.py` files from repo
3. **Setup Cell**: Copy Cell 1 from `hex_app.py`
4. **Layout Cells**: Copy remaining cells for each section
5. **Grid Layout**: Arrange in newspaper-style columns
6. **Schedule**: Set auto-refresh (e.g., every 15 minutes)
7. **Publish**: Share with team or make public

### Recommended Hex Layout
```
┌─────────────────┬─────────────────┐
│  Top Stories    │  AI Editor      │
│  (3 rows)       │  Summary        │
├─────────────────┼─────────────────┤
│  Politics       │  Business       │
│  (3 rows)       │  (3 rows)       │
├─────────────────┼─────────────────┤
│  Tech           │  Culture        │
│  (3 rows)       │  (3 rows)       │
├─────────────────┼─────────────────┤
│  Developing Stories (full width)  │
│  (3 rows)                         │
└───────────────────────────────────┘
```

## Performance

- Initial fetch: ~10-30 seconds for 100 markets
- Signal computation: <1 second
- Layout generation: <1 second
- Refresh cycle: ~15-45 seconds total

## Limitations

- Uses Kalshi's public API (no authentication required)
- Rate limited to avoid overloading the API
- Historical data accumulated during runtime only
- Sparklines require multiple snapshots over time

## Roadmap

- [ ] Persistent storage for historical snapshots
- [ ] More sophisticated volatility models
- [ ] User-customizable sections
- [ ] Email/Slack notifications for significant changes
- [ ] Enhanced Plotly visualizations
- [ ] Multi-exchange support (beyond Kalshi)

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

Built with:
- **Kalshi API**: Live prediction market data
- **Pandas**: Data manipulation
- **Hex**: Notebook deployment platform

Created for prediction market enthusiasts who want a clean, news-style view of market movements.

## Support

Questions? Open an issue on GitHub or contact the maintainer.

---

**MarketPress** - Turning prediction markets into news since 2026 📰📈
