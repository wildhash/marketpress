"""
Kalshi API Integration Module
Fetches live public market data from Kalshi's API
"""
import requests
from typing import Dict, List, Optional

import time


class KalshiAPI:
    """Client for interacting with Kalshi's public API"""
    
    BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
        })
    
    def get_markets(self, limit: int = 200, status: str = "open") -> List[Dict]:
        """
        Fetch active markets from Kalshi
        
        Args:
            limit: Maximum number of markets to fetch
            status: Market status filter (open, closed, settled)
            
        Returns:
            List of market dictionaries
        """
        try:
            url = f"{self.BASE_URL}/markets"
            params = {
                'limit': limit,
                'status': status
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('markets', [])
        except requests.RequestException as e:
            print(f"Error fetching markets: {e}")
            return []
        except (ValueError, KeyError) as e:
            print(f"Error parsing market data: {e}")
            return []
    
    def get_market(self, ticker: str) -> Optional[Dict]:
        """
        Fetch a single market by ticker
        
        Args:
            ticker: Market ticker symbol
            
        Returns:
            Market dictionary or None
        """
        try:
            url = f"{self.BASE_URL}/markets/{ticker}"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('market')
        except Exception as e:
            print(f"Error fetching market {ticker}: {e}")
            return None
    
    def get_orderbook(self, ticker: str) -> Optional[Dict]:
        """
        Fetch orderbook for a market
        
        Args:
            ticker: Market ticker symbol
            
        Returns:
            Orderbook dictionary with yes/no bids and asks
        """
        try:
            url = f"{self.BASE_URL}/markets/{ticker}/orderbook"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('orderbook')
        except Exception as e:
            print(f"Error fetching orderbook for {ticker}: {e}")
            return None
    
    def get_series(self, series_ticker: str) -> Optional[Dict]:
        """
        Fetch series information
        
        Args:
            series_ticker: Series ticker symbol
            
        Returns:
            Series dictionary or None
        """
        try:
            url = f"{self.BASE_URL}/series/{series_ticker}"
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('series')
        except Exception as e:
            print(f"Error fetching series {series_ticker}: {e}")
            return None
    
    def get_trades(self, ticker: str, limit: int = 100) -> List[Dict]:
        """
        Fetch recent trades for a market
        
        Args:
            ticker: Market ticker symbol
            limit: Maximum number of trades to fetch
            
        Returns:
            List of trade dictionaries
        """
        try:
            url = f"{self.BASE_URL}/markets/{ticker}/trades"
            params = {'limit': limit}
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('trades', [])
        except Exception as e:
            print(f"Error fetching trades for {ticker}: {e}")
            return []
    
    def get_events(self, limit: int = 50, status: str = "open") -> List[Dict]:
        """
        Fetch events from Kalshi
        
        Args:
            limit: Maximum number of events to fetch
            status: Event status filter
            
        Returns:
            List of event dictionaries
        """
        try:
            url = f"{self.BASE_URL}/events"
            params = {
                'limit': limit,
                'status': status
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('events', [])
        except Exception as e:
            print(f"Error fetching events: {e}")
            return []


def fetch_enriched_markets(api: KalshiAPI, limit: int = 100, enrich_data: bool = True) -> List[Dict]:
    """
    Fetch markets with optional enriched data (orderbook, trades)
    
    Args:
        api: KalshiAPI instance
        limit: Number of markets to fetch (1-500)
        enrich_data: Whether to fetch orderbook and trade data (adds API calls and time)
        
    Returns:
        List of market dictionaries (enriched if enrich_data=True)
        
    Note:
        Enriching data makes additional API calls per market (orderbook + trades).
        For 100 markets, this adds ~200 API calls and ~5 seconds of rate limiting delays.
        Set enrich_data=False for faster fetching with basic market data only.
    """
    # Validate limit parameter
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be a positive integer")
    if limit > 500:
        print(f"Warning: limit of {limit} is very high. Consider using a smaller value (1-500).")
    
    markets = api.get_markets(limit=limit)
    
    if not enrich_data:
        # Return basic market data without enrichment
        return markets
    
    enriched = []
    total_markets = len(markets)
    
    for idx, market in enumerate(markets):
        ticker = market.get('ticker')
        if not ticker:
            continue
        
        # Add orderbook data
        orderbook = api.get_orderbook(ticker)
        if orderbook:
            market['orderbook'] = orderbook
        
        # Add recent trades
        trades = api.get_trades(ticker, limit=10)
        if trades:
            market['recent_trades'] = trades
        
        enriched.append(market)
        
        # Rate limiting with progress indicator for long operations
        # Kalshi API rate limits are not publicly documented, using conservative 0.05s delay
        if idx < total_markets - 1:  # Don't sleep after last market
            time.sleep(0.05)
            if (idx + 1) % 20 == 0:
                print(f"Progress: enriched {idx + 1}/{total_markets} markets...")
    
    return enriched
