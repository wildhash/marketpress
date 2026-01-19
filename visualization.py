"""
Visualization Module
Creates sparklines and other visualizations for the MarketPress app
"""
import pandas as pd

from typing import List, Optional


# Threshold for trend arrow determination (0.5% change)
# Below this threshold, the market is considered flat (→)
TREND_ARROW_THRESHOLD = 0.005


def create_sparkline_text(prices: List[float], width: int = 10) -> str:
    """
    Create a text-based sparkline for price movements
    
    Args:
        prices: List of prices in chronological order
        width: Character width of the sparkline
        
    Returns:
        ASCII sparkline string
    """
    if not prices or len(prices) < 2:
        return "─" * width
    
    # Unicode block elements for sparklines
    blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    
    # Normalize prices to 0-7 range
    min_price = min(prices)
    max_price = max(prices)
    
    if max_price == min_price:
        return blocks[4] * width  # Middle block for flat line
    
    # Sample prices to fit width
    if len(prices) > width:
        step = len(prices) / width
        sampled = [prices[int(i * step)] for i in range(width)]
    else:
        sampled = prices + [prices[-1]] * (width - len(prices))
    
    # Convert to block characters
    normalized = [(p - min_price) / (max_price - min_price) * 7 for p in sampled]
    sparkline = ''.join([blocks[min(int(n), 7)] for n in normalized])
    
    return sparkline


def create_sparkline_svg(prices: List[float], width: int = 100, height: int = 30) -> str:
    """
    Create an SVG sparkline
    
    Args:
        prices: List of prices in chronological order
        width: SVG width in pixels
        height: SVG height in pixels
        
    Returns:
        SVG string
    """
    if not prices or len(prices) < 2:
        return f'<svg width="{width}" height="{height}"><line x1="0" y1="{height/2}" x2="{width}" y2="{height/2}" stroke="#ccc" stroke-width="1"/></svg>'
    
    min_price = min(prices)
    max_price = max(prices)
    
    if max_price == min_price:
        y = height / 2
        return f'<svg width="{width}" height="{height}"><line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="#666" stroke-width="2"/></svg>'
    
    # Create points
    points = []
    for i, price in enumerate(prices):
        x = (i / (len(prices) - 1)) * width
        y = height - ((price - min_price) / (max_price - min_price)) * height
        points.append(f"{x:.1f},{y:.1f}")
    
    points_str = " ".join(points)
    
    # Determine color based on trend
    color = "#0066cc" if prices[-1] >= prices[0] else "#cc0000"
    
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <polyline points="{points_str}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>
</svg>'''
    
    return svg


def get_trend_arrow(current: float, previous: Optional[float]) -> str:
    """
    Get a trend arrow indicator
    
    Args:
        current: Current value
        previous: Previous value
        
    Returns:
        Arrow character (↑, ↓, →)
    """
    if previous is None or pd.isna(previous) or pd.isna(current):
        return "→"
    
    diff = current - previous
    
    if abs(diff) < TREND_ARROW_THRESHOLD:
        return "→"
    elif diff > 0:
        return "↑"
    else:
        return "↓"


def get_trend_color(delta: Optional[float]) -> str:
    """
    Get color for a delta value
    
    Args:
        delta: Change in probability
        
    Returns:
        Color name or code
    """
    if delta is None or pd.isna(delta):
        return "gray"
    
    if abs(delta) < 0.01:  # Less than 1% change
        return "gray"
    elif delta > 0:
        return "green"
    else:
        return "red"


def format_probability(prob: Optional[float]) -> str:
    """
    Format probability for display
    
    Args:
        prob: Probability value (0-1)
        
    Returns:
        Formatted string (e.g., "45%")
    """
    if prob is None or pd.isna(prob):
        return "N/A"
    
    return f"{prob * 100:.0f}%"


def format_delta(delta: Optional[float]) -> str:
    """
    Format probability change for display
    
    Args:
        delta: Change in probability (0-1 scale)
        
    Returns:
        Formatted string with sign (e.g., "+5%", "-3%")
    """
    if delta is None or pd.isna(delta):
        return "—"
    
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta * 100:.0f}%"


def create_market_headline(row: pd.Series) -> str:
    """
    Create a newspaper-style headline for a market
    
    Args:
        row: Market data row
        
    Returns:
        Formatted headline string
    """
    title = row.get('title', 'Unknown Market')
    prob = row.get('yes_price', None)
    delta_24h = row.get('delta_24h', None)
    
    prob_str = format_probability(prob)
    delta_str = format_delta(delta_24h)
    arrow = get_trend_arrow(prob, prob - delta_24h if delta_24h else None)
    
    # Create headline
    headline = f"{title} {arrow} {prob_str}"
    if delta_24h and not pd.isna(delta_24h):
        headline += f" ({delta_str} 24h)"
    
    return headline


def create_sparkline_from_snapshots(ticker: str, 
                                    snapshots_df: pd.DataFrame, 
                                    hours: int = 24) -> str:
    """
    Create sparkline from historical snapshot data
    
    Args:
        ticker: Market ticker
        snapshots_df: Historical snapshots DataFrame
        hours: Hours of history to include
        
    Returns:
        Sparkline text
    """
    if snapshots_df.empty:
        return "─────"
    
    cutoff = pd.Timestamp.now() - pd.Timedelta(hours=hours)
    ticker_data = snapshots_df[
        (snapshots_df['ticker'] == ticker) & 
        (snapshots_df['snapshot_time'] >= cutoff)
    ].copy()
    
    if ticker_data.empty or len(ticker_data) < 2:
        return "─────"
    
    ticker_data = ticker_data.sort_values('snapshot_time')
    prices = ticker_data['yes_price'].dropna().tolist()
    
    return create_sparkline_text(prices, width=8)
