# MarketPress 📰

A Hex-native "prediction markets newspaper" that feels like BBC/Yahoo. MarketPress transforms live Kalshi market data into a scannable front page with raw-fact headlines, interactive filters, and an AI "Editor Desk" powered by Hex Threads.

## 🌐 Live Site

**[Visit the MarketPress Landing Page](https://wildhash.github.io/marketpress/)**

This is the judge-friendly landing page. The Hex project link is inside.

---

## Visual Preview

### Front Page
> 📸 **Screenshot Placeholder**: See [assets/frontpage_placeholder.md](assets/frontpage_placeholder.md) for what will be captured
> 
> Shows: Lead Story, Top Stories, Category Sections (Politics/Business/Tech/Culture/Sports), Developing, and Most Read

### Drill-Down View  
> 📸 **Screenshot Placeholder**: See [assets/drilldown_placeholder.md](assets/drilldown_placeholder.md) for what will be captured
>
> Shows: Detailed fact box with market statistics, 7-day timeline, and all computed signals

### Editor Desk (Threads)
> 📸 **Screenshot Placeholder**: See [assets/editor_desk_placeholder.md](assets/editor_desk_placeholder.md) for what will be captured
>
> Shows: AI-powered Q&A using Hex Threads with semantic model integration

**For now, see the live demo at the public Hex link below.**

---

## Judge Mode (5 Minutes)

**Want to see it in action?** Two options:

### Option A: Open Public Hex Project (Recommended) ⭐
1. Open the public Hex project: **[MarketPress - Prediction Markets Newspaper](https://app.hex.tech/wildhash/app/marketpress-prediction-markets-newspaper/latest)**
2. Click **"Run All"**
3. Explore the interactive front page with live prediction market data
4. Try the AI Editor Desk in Threads

### Option B: Build from Source
1. Follow the [HEX_GUIDE.md](HEX_GUIDE.md) step-by-step instructions
2. Paste 8 cells from `hex_cells/` folder
3. Click **"Run All"**
4. Total time: 5-10 minutes

---

## What You Get

A judge-proof, BBC-style prediction markets front page with:

- **Lead Story** - The most newsworthy market right now
- **Top Stories** - Highest-ranked markets across all categories
- **Section Pages** - Politics, Business, Tech, Culture, Sports
- **Developing** - High-volatility markets with accelerating attention
- **Most Read** - Highest-attention markets (volume/OI proxy)

Each headline includes:
- Implied probability
- Δ24h / Δ7d movement
- Volume / attention proxy
- Spread / confidence proxy
- Last updated timestamp

Plus:
- **Filters** - Category, time window, min liquidity
- **Drill-down** - Click headline → timeline + fact box
- **AI Editor Desk** - Hex Threads integration for natural language queries

---

## Philosophy: Raw Facts, No Spin

MarketPress presents **what the crowd believes**, not what pundits think. Every headline is a prediction market with:
- Real money on the line
- Transparent probability
- Trackable changes over time

No commentary. No hot takes. Just the wisdom (or madness) of crowds.

---

## Methodology: How Markets Become News

MarketPress transforms raw prediction market data into a scannable newspaper through computed signals:

### Newsworthiness Score
A composite metric that ranks markets by editorial importance:
- **Delta 24h** (30%): Recent probability changes signal breaking developments
- **Volatility** (25%): Standard deviation of prices indicates uncertainty and debate
- **Attention** (25%): Combined volume and open interest shows crowd engagement
- **Confidence** (20%): Inverse of spread reflects market conviction

Markets with the highest newsworthiness become "Lead Story" and "Top Stories."

### Confidence Score
How certain the market is about the outcome:
- **Tight spread (< 2%)**: High confidence—market makers agree on the price
- **Normal spread (2-5%)**: Moderate confidence—typical market conditions  
- **Wide spread (> 5%)**: Low confidence—disagreement or low liquidity

Confidence helps distinguish "serious desk" high-conviction markets from speculative noise.

### Attention Score
A proxy for "most read" (engagement and trading activity):
- **Volume**: Total contracts traded (direct activity measure)
- **Open Interest**: Outstanding positions (sustained interest)
- **Composite**: Weighted combination reflecting total market engagement

High attention markets are the "most watched" stories.

### Volatility
Price instability over rolling windows:
- **7-day standard deviation**: How much the probability bounces around
- **Developing stories**: Markets with both high volatility AND accelerating attention
- **Stable markets**: Low volatility signals consensus

Volatile markets with rising attention surface as "Developing" stories.

---

## Features

### 📰 Newspaper-Style Layout
- **Lead Story** - Single most newsworthy market
- **Top Stories** - Top 5 across all categories  
- **Category Sections** - Politics, Business, Tech, Culture, Sports
- **Developing** - High volatility + accelerating attention
- **Most Read** - Highest attention scores

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

### In Hex (Recommended)

**The Hex-first approach:** See [HEX_GUIDE.md](HEX_GUIDE.md) for complete instructions.

Quick summary:
1. Create a new Hex notebook
2. Create 8 Python cells, paste code from `hex_cells/` folder in order:
   - `01_setup.py` - Config and constants
   - `02_fetch_kalshi.py` - Data fetching  
   - `03_normalize.py` - Table normalization
   - `04_signals.py` - Signal computation
   - `05_sections.py` - Section organization
   - `06_frontpage.py` - Front page layout
   - `07_drilldown.py` - Drill-down details
   - `08_editor.py` - Editor Desk functions
3. Run All
4. Arrange in grid layout

### Hex Threads Integration (Editor Desk)

The AI Editor Desk is powered by Hex Threads with a semantic model (`semantic_model.yaml`).

#### 2-Minute Threads Demo

Once your Hex project is running, open the Threads panel and try these starter prompts:

1. **"Write today's front page in 8 headlines"** - Get a concise executive summary of top markets
2. **"What's the biggest belief shift since yesterday?"** - Find markets with the largest 24h probability changes
3. **"Show me the fun desk: weird movers with real liquidity"** - Discover unusual markets with actual trading activity
4. **"Which categories are most unstable right now?"** - Identify which sections (Politics/Business/Tech/etc.) have highest volatility

These prompts work reliably because they align with the computed signals and section organization in the data model.

**Available Functions:**
```python
summarize_front_page()      # Executive summary
biggest_belief_shifts()     # Top movers
most_unstable_markets()     # High volatility
fun_desk()                  # Weird movers with liquidity
serious_desk()              # High-stakes markets
answer_query(question)      # Natural language Q&A
```

## What's Working Today

✅ **Core Features (Production Ready)**
- Kalshi public API ingestion with pagination
- Three normalized tables (markets, snapshots, liquidity)
- Signal computation (Δ24h, Δ7d, volatility, attention, confidence, newsworthiness)
- Newspaper-style section organization
- Front page layout with Lead Story, Top Stories, and 5 category sections
- Developing stories (high volatility detection)
- Most Read proxy (attention scoring)
- Drill-down fact boxes with full market details
- AI Editor Desk with Hex Threads integration
- Semantic model for natural language queries
- Demo mode for testing without API
- Hex-first packaging (8 cells, paste and run)

✅ **Hex Integration**
- Cell-by-cell code organization (`hex_cells/` folder)
- Complete deployment guide
- Thread-ready semantic model
- Interactive filters and displays

## What's Next

🚧 **Planned Enhancements**
- **Multi-source enrichment**: News headlines, Twitter sentiment, Google Trends correlation
- **Alerting system**: Email/Slack notifications for significant market moves
- **Premium x402 paywall integration**: Monetization layer for advanced features
- **Persistent historical storage**: Database backend for long-term trend analysis
- **Advanced volatility models**: GARCH, realized volatility, implied volatility
- **Multi-exchange support**: Polymarket, PredictIt, Manifold Markets
- **User-customizable sections**: Create your own market categories
- **Real-time WebSocket updates**: Live price ticking without refresh
- **Mobile-optimized layout**: Responsive design for phones/tablets

---

## Architecture

### Hex-First Design

MarketPress is designed for **Hex Projects**, not traditional applications. The architecture reflects this:

```
User Opens Hex Project → Runs 8 Cells → Interactive Front Page
```

### Cell Flow

```
Cell 1: Setup          → Configuration, constants, category mappings
Cell 2: Fetch          → Kalshi API or demo data  
Cell 3: Normalize      → Markets, snapshots, liquidity tables
Cell 4: Signals        → Δ24h, Δ7d, volatility, attention, confidence, newsworthiness
Cell 5: Sections       → Organize into Lead, Top, Politics, Business, Tech, Culture, Sports, Developing, Most Read
Cell 6: Front Page     → Display-ready dataframes with formatting
Cell 7: Drill-Down     → Fact boxes and timeline data
Cell 8: Editor Desk    → Threads functions for Q&A
```

### Data Flow

```
Kalshi API → Raw Markets → Normalized Tables → Signal Computation
                                ↓
                         Section Organization
                                ↓
                     ┌──────────────────────┐
                     │   Front Page Layout  │
                     ├──────────────────────┤
                     │ - Lead Story         │
                     │ - Top Stories        │
                     │ - Category Sections  │
                     │ - Developing         │
                     │ - Most Read          │
                     │ - Editor Desk        │
                     └──────────────────────┘
                                ↓
                        Hex Display + Threads
```

### Traditional Python Architecture (Optional)

For standalone Python usage, the codebase includes:
```
MarketPress
├── hex_cells/             # Hex-first cell code (8 files)
├── kalshi_api.py          # Kalshi API client
├── data_normalization.py  # Data table schemas
├── signals.py             # Signal computation
├── visualization.py       # Sparklines and formatting
├── layout.py              # Section organization
├── editor.py              # AI Editor with semantic model
├── marketpress.py         # Main application orchestrator
├── demo_data.py           # Demo data generator
├── hex_app.py             # Legacy Hex template
└── semantic_model.yaml    # Threads semantic model spec
```

---

## API Reference (Python)

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

**Recommended Method**: Use the `hex_cells/` folder approach documented in [HEX_GUIDE.md](HEX_GUIDE.md).

Quick summary:
1. **Create Hex Project**: New Python notebook
2. **Create 8 Python Cells**: Paste code from `hex_cells/01_setup.py` through `hex_cells/08_editor.py`
3. **Run All**: Click "Run All" to execute all cells
4. **Grid Layout**: Arrange outputs in newspaper-style columns
5. **Schedule**: Set auto-refresh (e.g., every 15 minutes)
6. **Publish**: Share with team or make public

### Legacy Method (Not Recommended)

**⚠️ Do not use for judging or production.** The `hex_app.py` file is a legacy single-file template from earlier development. It is kept for historical reference only.

**Use the `hex_cells/` method above instead** (Option A or B in HEX_GUIDE.md).

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

## Troubleshooting

### API Connection Issues
**Problem**: Kalshi API is unavailable, rate-limited, or returns errors.

**Solution**: The application includes automatic demo fallback. When the API fails, it will:
1. Automatically load cached sample market data from `demo_data/`
2. Display a banner: `"Demo mode: using cached sample markets (Kalshi unavailable)"`
3. Continue functioning normally with realistic sample data

To manually enable demo mode, set `USE_DEMO_DATA = True` in `hex_cells/01_setup.py`.

### Missing Data or Empty Sections
**Problem**: Some sections show no markets or missing data.

**Solution**: 
- Ensure all cells run in order (1-8)
- Check for error messages in cell outputs
- Try reducing `MARKET_LIMIT` in Cell 1 (default is 100)
- Verify demo mode is working if API is unavailable

### Slow Performance
**Problem**: Data fetching or signal computation takes too long.

**Solution**:
- Reduce `MARKET_LIMIT` in Cell 1 (try 50 markets)
- Increase refresh interval in Hex schedule
- Use demo data for testing layouts before going live

### Threads Prompts Not Working
**Problem**: Editor Desk queries return unexpected results.

**Solution**:
- Verify `semantic_model.yaml` is properly loaded
- Ensure all data tables (`markets_df`, `snapshots_df`, `liquidity_df`) are populated
- Check that column names match the semantic model definitions
- Try the starter prompts listed in the Threads demo section

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
