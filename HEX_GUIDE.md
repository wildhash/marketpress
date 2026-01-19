# MarketPress Hex Deployment Guide

## Judge Mode (5 minutes)

### Option A: Public Hex Project (Recommended) ⭐
Open the public Hex project and click "Run All" to see the live front page.
- **Public Project**: [MarketPress - Prediction Markets Newspaper](https://app.hex.tech/wildhash/app/marketpress-prediction-markets-newspaper/latest)
- Simply click **"Run All"** and explore the interactive newspaper layout
- Try the AI Editor Desk prompts in Threads

### Option B: Build from Source (5-10 minutes)
Follow the step-by-step instructions below to create your own Hex project.

---

## Building from Source

### 1. Create a New Hex Project
1. Log in to Hex (hex.tech)
2. Click "Create Project" → "Blank Notebook"
3. Name it "MarketPress"

### 2. Create Cells in Order
**Do NOT upload files**. Instead, create Python cells and paste the contents of each file from the `hex_cells/` folder in numeric order.

### 3. Cell-by-Cell Instructions

#### Cell 1: Setup and Configuration
1. Create a new **Python cell** in Hex
2. Paste the entire contents of `hex_cells/01_setup.py`
3. Run the cell
4. Expected output: "✓ MarketPress configuration loaded"

#### Cell 2: Fetch Kalshi Data
1. Create a new **Python cell**
2. Paste the entire contents of `hex_cells/02_fetch_kalshi.py`
3. Run the cell
4. Expected output: "✓ Data fetched: N markets"

#### Cell 3: Normalize Data
1. Create a new **Python cell**
2. Paste the entire contents of `hex_cells/03_normalize.py`
3. Run the cell
4. Expected output: "✓ Normalized N markets into tables"

#### Cell 4: Compute Signals
1. Create a new **Python cell**
2. Paste the entire contents of `hex_cells/04_signals.py`
3. Run the cell
4. Expected output: "✓ Computed signals for N markets"

#### Cell 5: Section Organization
1. Create a new **Python cell**
2. Paste the entire contents of `hex_cells/05_sections.py`
3. Run the cell
4. Expected output: "✓ Organized into sections" with section counts

#### Cell 6: Front Page Layout
1. Create a new **Python cell**
2. Paste the entire contents of `hex_cells/06_frontpage.py`
3. Run the cell
4. Expected output: Formatted front page with Top Stories

#### Cell 7: Drill-Down Details
1. Create a new **Python cell**
2. Paste the entire contents of `hex_cells/07_drilldown.py`
3. Run the cell
4. Expected output: Example fact box for lead story

#### Cell 8: Editor Desk (Threads)
1. Create a new **Python cell**
2. Paste the entire contents of `hex_cells/08_editor.py`
3. Run the cell
4. Expected output: Editor's summary and available functions

### 4. Run All
After creating all 8 cells, click **"Run All"** in Hex. The notebook will:
1. Configure the application
2. Fetch market data (or use demo data)
3. Normalize into tables
4. Compute signals
5. Organize into sections
6. Display front page
7. Show drill-down example
8. Initialize Editor Desk

### 5. Expected Outputs
After running all cells, you should see:
- **Cell 1**: Configuration confirmation
- **Cell 2**: Market count
- **Cell 3**: Normalized tables info
- **Cell 4**: Signal computation results
- **Cell 5**: Section organization counts
- **Cell 6**: Front page layout with top stories
- **Cell 7**: Fact box for lead story
- **Cell 8**: Editor's summary and available functions

### 6. Accessing Data
All data is now available as DataFrame variables:
- `markets_df` - All markets with signals
- `snapshots_df` - Time-series data
- `liquidity_df` - Spread and confidence metrics
- `top_stories_display` - Top stories formatted
- `politics_display`, `business_display`, etc. - Section tables
- `lead_fact_box` - Lead story details

### 7. Styling Tips

Add markdown cells for headers:
```markdown
# 📰 MARKETPRESS

*Live prediction market news - Updated every 15 minutes*

---

## Top Stories
```

### 8. Schedule Auto-Refresh

1. Click "Schedule" in Hex
2. Set refresh interval (e.g., every 15 minutes)
3. Configure to run during market hours
4. Enable email/Slack notifications for significant changes

### 9. Advanced Features

#### Add Filters with Hex Inputs
Create additional cells for filtering:
```python
# Cell: Filter by Category
# Create a dropdown input widget named 'selected_category'
filtered_df = markets_df[markets_df['section'] == selected_category]
section_to_display_df(filtered_df)
```

#### Display Individual Sections
Create separate cells for each section:
```python
# Cell: Politics Section
politics_display[['title', 'probability', 'delta_24h', 'attention']]
```

```python
# Cell: Business Section
business_display[['title', 'probability', 'delta_24h', 'attention']]
```

### 10. Hex Thread Integration

Hex Threads can interact with your data using the Editor Desk functions. Try these prompts:

**Starter Prompts for Hex Threads:**
1. "Write today's front page in 8 headlines"
2. "What's the biggest belief shift since yesterday?"
3. "Show me the fun desk: weird movers with real liquidity"
4. "Which categories are most unstable right now?"
5. "Summarize the political markets"
6. "What's the most watched market today?"

**Use Editor Functions:**
```python
# In a new cell, call Editor Desk functions:
biggest_belief_shifts()  # Top movers
most_unstable_markets()  # High volatility
fun_desk()  # Weird movers
serious_desk()  # High-stakes markets
answer_query("How many markets are tracked?")
```

The semantic model is automatically built from the data and includes:
- All market details
- Sections and categories
- Signals (attention, volatility, newsworthiness)
- Time-series snapshots

### 11. Publishing

1. Click "Publish" in Hex
2. Set permissions (private, organization, public)
3. Share the link with your team
4. Embed in dashboards or websites

### 12. Troubleshooting

**API Connection Issues:**
- Set `USE_DEMO_DATA = True` in Cell 1 to test with demo data
- Check if Kalshi API is accessible from Hex
- Verify no rate limiting issues

**Missing Data:**
- Ensure all cells run in order (1-8)
- Check for error messages in output
- Try reducing `MARKET_LIMIT` in Cell 1

**Slow Performance:**
- Reduce `MARKET_LIMIT` in Cell 1
- Increase refresh interval in schedule
- Use demo data for testing

**Cells Won't Run:**
- Make sure you run cells in order (dependencies)
- Check that all dependencies are installed
- Restart kernel and run all cells

## Best Practices

1. **Always run cells in order** (1-8) when starting fresh
2. **Use demo data first** (`USE_DEMO_DATA = True`) to test the layout
3. **Set appropriate refresh intervals** (15-30 minutes recommended)
4. **Monitor API usage** to avoid rate limits
5. **Use Hex's built-in formatting** for tables
6. **Test Threads prompts** to get familiar with the Editor Desk

## File Reference

All Hex cell files are in the `hex_cells/` folder:
- `01_setup.py` - Configuration and constants
- `02_fetch_kalshi.py` - Data fetching
- `03_normalize.py` - Data normalization
- `04_signals.py` - Signal computation
- `05_sections.py` - Section organization
- `06_frontpage.py` - Front page layout
- `07_drilldown.py` - Drill-down details
- `08_editor.py` - Editor Desk functions

## Support

For issues or questions:
- Check the main README.md
- Review the hex_cells/ folder for cell code
- Open an issue on GitHub

---

**Happy Market Watching! 📈📰**
