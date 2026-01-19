# MarketPress Hex Deployment Guide

## Quick Start

### 1. Create a New Hex Project
1. Log in to Hex (hex.tech)
2. Click "Create Project" → "Blank Notebook"
3. Name it "MarketPress"

### 2. Upload Files
Upload these Python files to your Hex project:
- `kalshi_api.py`
- `data_normalization.py`
- `signals.py`
- `visualization.py`
- `layout.py`
- `editor.py`
- `marketpress.py`
- `demo_data.py`

### 3. Create Cells

#### Cell 1: Setup and Initialization
```python
# Install dependencies (run once)
!pip install requests pandas numpy plotly python-dateutil

# Import the MarketPress application
from marketpress import create_marketpress_app

# Initialize the application
# Set use_demo=True for testing, False for live Kalshi data
app = create_marketpress_app(limit=100, use_demo=False)

print("✓ MarketPress initialized")
```

#### Cell 2: Top Stories
```python
from visualization import format_probability, format_delta

top_stories = app.get_section_dataframe('Top Stories')

# Format for display
display_df = top_stories[['title', 'yes_price', 'delta_24h', 'volume']].head(10).copy()
display_df.columns = ['Market', 'Probability', '24h Change', 'Volume']

# Format percentages
display_df['Probability'] = display_df['Probability'].apply(format_probability)
display_df['24h Change'] = display_df['24h Change'].apply(format_delta)

display_df
```

#### Cell 3: AI Editor Summary
```python
print(app.get_editor_summary())
```

#### Cell 4: Politics Section
```python
politics = app.get_section_dataframe('Politics')
politics[['title', 'yes_price', 'delta_24h']].head(10)
```

#### Cell 5: Business Section
```python
business = app.get_section_dataframe('Business')
business[['title', 'yes_price', 'delta_24h']].head(10)
```

#### Cell 6: Tech Section
```python
tech = app.get_section_dataframe('Tech')
tech[['title', 'yes_price', 'delta_24h']].head(10)
```

#### Cell 7: Culture Section
```python
culture = app.get_section_dataframe('Culture')
culture[['title', 'yes_price', 'delta_24h']].head(10)
```

#### Cell 8: Sports Section
```python
sports = app.get_section_dataframe('Sports')
sports[['title', 'yes_price', 'delta_24h']].head(10)
```

#### Cell 9: Developing Stories
```python
developing = app.get_section_dataframe('Developing')
developing[['title', 'yes_price', 'delta_24h', 'volatility']].head(10)
```

#### Cell 10: Interactive Q&A
```python
# Add a Hex text input widget named 'question'
# Then use this code:
answer = app.ask_editor(question)
print(answer)
```

### 4. Layout Configuration

Use Hex's grid layout to arrange cells:

```
┌──────────────┬──────────────┬──────────────┐
│ Cell 1       │ Cell 3       │              │
│ (Setup)      │ (AI Editor)  │              │
├──────────────┼──────────────┤              │
│ Cell 2       │ Cell 9       │  Cell 10     │
│ (Top Stories)│ (Developing) │  (Q&A)       │
├──────────────┼──────────────┤              │
│ Cell 4       │ Cell 5       │              │
│ (Politics)   │ (Business)   │              │
├──────────────┼──────────────┤              │
│ Cell 6       │ Cell 7       │              │
│ (Tech)       │ (Culture)    │              │
└──────────────┴──────────────┘              │
│ Cell 8 (Sports)              │              │
└──────────────────────────────┴──────────────┘
```

### 5. Styling Tips

Add markdown cells for headers:
```markdown
# 📰 MARKETPRESS

*Live prediction market news - Updated every 15 minutes*

---

## Top Stories
```

### 6. Schedule Auto-Refresh

1. Click "Schedule" in Hex
2. Set refresh interval (e.g., every 15 minutes)
3. Configure to run during market hours
4. Enable email/Slack notifications for significant changes

### 7. Advanced Features

#### Add Plotly Sparklines
```python
import plotly.graph_objects as go

def create_plotly_sparkline(ticker):
    snapshots = app.snapshots_df[app.snapshots_df['ticker'] == ticker]
    prices = snapshots['yes_price'].tolist()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=prices, mode='lines', line=dict(color='blue', width=2)))
    fig.update_layout(
        height=50,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    )
    return fig

# Use in a cell
create_plotly_sparkline('DEMO-001')
```

#### Add Filters with Hex Inputs
```python
# Create a dropdown input named 'category_filter'
filtered_df = app.markets_df[app.markets_df['category'] == category_filter]
filtered_df[['title', 'yes_price', 'delta_24h']]
```

#### Add Threshold Alerts
```python
# Alert on big movers
big_movers = app.markets_df[abs(app.markets_df['delta_24h']) > 0.10]
if not big_movers.empty:
    print(f"⚠️ {len(big_movers)} markets moved >10% in 24h!")
    print(big_movers[['title', 'yes_price', 'delta_24h']])
```

### 8. Hex Thread Integration

For Hex Thread, expose the semantic model:

```python
# Make data available to Thread
semantic_model = {
    'markets': app.markets_df.to_dict('records'),
    'sections': {name: df.to_dict('records') for name, df in app.sections.items()},
    'summary': app.editor.semantic_model
}

# Thread can now answer questions like:
# - "What are the biggest movers today?"
# - "Show me all tech markets above 70%"
# - "What's the average probability in politics?"
```

### 9. Publishing

1. Click "Publish" in Hex
2. Set permissions (private, organization, public)
3. Share the link with your team
4. Embed in dashboards or websites

### 10. Troubleshooting

**API Connection Issues:**
- Set `use_demo=True` in Cell 1 to test with demo data
- Check if Kalshi API is accessible from Hex
- Verify no rate limiting issues

**Missing Data:**
- Ensure Cell 1 runs successfully
- Check for error messages in output
- Try reducing the `limit` parameter

**Slow Performance:**
- Reduce the number of markets fetched
- Increase refresh interval
- Cache results between runs

**Styling Issues:**
- Use Hex's built-in table formatting
- Add custom CSS if needed
- Use markdown for headers

## Best Practices

1. **Run Cell 1 first** every time you open the notebook
2. **Set appropriate refresh intervals** (15-30 minutes recommended)
3. **Monitor API usage** to avoid rate limits
4. **Use filters** to focus on specific categories
5. **Archive historical data** for long-term analysis
6. **Test with demo data** before going live
7. **Add error handling** for production use

## Support

For issues or questions:
- Check the main README.md
- Review example.py for usage examples
- Open an issue on GitHub

---

**Happy Market Watching! 📈📰**
