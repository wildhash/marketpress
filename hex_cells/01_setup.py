"""
MarketPress Hex Cell 1: Setup and Configuration
Imports, config, constants, API base URLs, time windows
"""

# Install dependencies (run once if needed)
# !pip install requests pandas numpy plotly python-dateutil

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time

# Configuration
KALSHI_BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"
USE_DEMO_DATA = True  # Set to False for live Kalshi data
MARKET_LIMIT = 100  # Number of markets to fetch
RATE_LIMIT_DELAY = 0.5  # Seconds between API calls

# Time windows for signal computation
TIME_WINDOW_24H = timedelta(hours=24)
TIME_WINDOW_7D = timedelta(days=7)
TIME_WINDOW_30D = timedelta(days=30)

# Section categories and keywords
CATEGORY_MAPPINGS = {
    'Politics': ['election', 'senate', 'house', 'president', 'congress', 'bill', 'vote', 
                 'democrat', 'republican', 'approval', 'policy', 'government', 'white house'],
    'Business': ['fed', 'rate', 'inflation', 'gdp', 'unemployment', 'stock', 'market cap',
                 'earnings', 'revenue', 'economy', 'trade', 'tariff', 'dollar'],
    'Tech': ['ai', 'tech', 'software', 'apple', 'google', 'microsoft', 'amazon', 'tesla',
             'meta', 'twitter', 'chip', 'semiconductor', 'robot', 'launch', 'iphone'],
    'Culture': ['movie', 'album', 'award', 'oscar', 'grammy', 'emmy', 'box office', 'streaming',
                'taylor swift', 'drake', 'beyonce', 'conference', 'attendance', 'festival'],
    'Sports': ['nfl', 'nba', 'mlb', 'nhl', 'soccer', 'football', 'basketball', 'baseball',
               'champion', 'super bowl', 'world series', 'finals', 'playoff', 'tournament']
}

# Newsworthiness weighting factors
NEWSWORTHINESS_WEIGHTS = {
    'delta_24h': 0.30,
    'volatility': 0.25,
    'attention': 0.25,
    'confidence': 0.20
}

# Display settings
MAX_STORIES_PER_SECTION = 10
TOP_STORIES_COUNT = 5
DEVELOPING_THRESHOLD = 0.15  # Volatility threshold for "Developing" section

print("✓ MarketPress configuration loaded")
print(f"  API Base: {KALSHI_BASE_URL}")
print(f"  Market Limit: {MARKET_LIMIT}")
print(f"  Demo Mode: {USE_DEMO_DATA}")
