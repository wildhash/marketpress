"""
Data Normalization Module
Normalizes Kalshi market data into structured tables
"""
import pandas as pd
from typing import Dict, List
from datetime import datetime
import numpy as np


def normalize_markets(raw_markets: List[Dict]) -> pd.DataFrame:
    """
    Normalize raw market data into a structured DataFrame
    
    Args:
        raw_markets: List of raw market dictionaries from Kalshi API
        
    Returns:
        DataFrame with normalized market data
    """
    markets_data = []
    
    for market in raw_markets:
        try:
            market_row = {
                'ticker': market.get('ticker'),
                'title': market.get('title', ''),
                'subtitle': market.get('subtitle', ''),
                'event_ticker': market.get('event_ticker', ''),
                'series_ticker': market.get('series_ticker', ''),
                'category': market.get('category', 'Other'),
                'status': market.get('status', 'unknown'),
                'yes_price': market.get('yes_price', 0) / 100.0 if market.get('yes_price') else None,  # Convert cents to probability
                'no_price': market.get('no_price', 0) / 100.0 if market.get('no_price') else None,
                'last_price': market.get('last_price', 0) / 100.0 if market.get('last_price') else None,
                'open_time': pd.to_datetime(market.get('open_time')) if market.get('open_time') else None,
                'close_time': pd.to_datetime(market.get('close_time')) if market.get('close_time') else None,
                'expiration_time': pd.to_datetime(market.get('expiration_time')) if market.get('expiration_time') else None,
                'volume': market.get('volume', 0),
                'open_interest': market.get('open_interest', 0),
                'liquidity': market.get('liquidity', 0),
                'previous_yes_price': market.get('previous_yes_price', 0) / 100.0 if market.get('previous_yes_price') else None,
                'result': market.get('result', ''),
            }
            markets_data.append(market_row)
        except Exception as e:
            print(f"Error normalizing market {market.get('ticker', 'unknown')}: {e}")
            continue
    
    df = pd.DataFrame(markets_data)
    
    # Add derived fields
    if not df.empty:
        df['fetch_time'] = pd.Timestamp.now()
        
    return df


def normalize_snapshots(raw_markets: List[Dict]) -> pd.DataFrame:
    """
    Create snapshot records for time-series analysis
    
    Args:
        raw_markets: List of raw market dictionaries
        
    Returns:
        DataFrame with market snapshots
    """
    snapshots = []
    snapshot_time = pd.Timestamp.now()
    
    for market in raw_markets:
        try:
            snapshot = {
                'ticker': market.get('ticker'),
                'snapshot_time': snapshot_time,
                'yes_price': market.get('yes_price', 0) / 100.0 if market.get('yes_price') else None,
                'no_price': market.get('no_price', 0) / 100.0 if market.get('no_price') else None,
                'last_price': market.get('last_price', 0) / 100.0 if market.get('last_price') else None,
                'volume': market.get('volume', 0),
                'open_interest': market.get('open_interest', 0),
            }
            snapshots.append(snapshot)
        except Exception as e:
            print(f"Error creating snapshot for {market.get('ticker', 'unknown')}: {e}")
            continue
    
    return pd.DataFrame(snapshots)


def normalize_liquidity_spread(raw_markets: List[Dict]) -> pd.DataFrame:
    """
    Extract liquidity and spread metrics from orderbook data
    
    Args:
        raw_markets: List of raw market dictionaries with orderbook data
        
    Returns:
        DataFrame with liquidity and spread metrics
    """
    liquidity_data = []
    
    for market in raw_markets:
        try:
            ticker = market.get('ticker')
            orderbook = market.get('orderbook', {})
            
            # Extract yes side
            yes_bids = orderbook.get('yes', [])
            yes_best_bid = None
            yes_best_ask = None
            yes_bid_volume = 0
            yes_ask_volume = 0
            
            if yes_bids:
                for level in yes_bids:
                    price = level.get('price', 0) / 100.0
                    quantity = level.get('quantity', 0)
                    
                    if level.get('type') == 'bid':
                        yes_bid_volume += quantity
                        if yes_best_bid is None or price > yes_best_bid:
                            yes_best_bid = price
                    elif level.get('type') == 'ask':
                        yes_ask_volume += quantity
                        if yes_best_ask is None or price < yes_best_ask:
                            yes_best_ask = price
            
            # Extract no side
            no_bids = orderbook.get('no', [])
            no_best_bid = None
            no_best_ask = None
            no_bid_volume = 0
            no_ask_volume = 0
            
            if no_bids:
                for level in no_bids:
                    price = level.get('price', 0) / 100.0
                    quantity = level.get('quantity', 0)
                    
                    if level.get('type') == 'bid':
                        no_bid_volume += quantity
                        if no_best_bid is None or price > no_best_bid:
                            no_best_bid = price
                    elif level.get('type') == 'ask':
                        no_ask_volume += quantity
                        if no_best_ask is None or price < no_best_ask:
                            no_best_ask = price
            
            # Calculate spread (using yes side as primary)
            spread = None
            if yes_best_bid is not None and yes_best_ask is not None:
                spread = yes_best_ask - yes_best_bid
            
            # Calculate mid price
            mid_price = None
            if yes_best_bid is not None and yes_best_ask is not None:
                mid_price = (yes_best_bid + yes_best_ask) / 2
            
            liquidity_row = {
                'ticker': ticker,
                'timestamp': pd.Timestamp.now(),
                'yes_best_bid': yes_best_bid,
                'yes_best_ask': yes_best_ask,
                'yes_bid_volume': yes_bid_volume,
                'yes_ask_volume': yes_ask_volume,
                'no_best_bid': no_best_bid,
                'no_best_ask': no_best_ask,
                'no_bid_volume': no_bid_volume,
                'no_ask_volume': no_ask_volume,
                'spread': spread,
                'mid_price': mid_price,
                'total_liquidity': yes_bid_volume + yes_ask_volume + no_bid_volume + no_ask_volume,
            }
            liquidity_data.append(liquidity_row)
        except Exception as e:
            print(f"Error extracting liquidity for {market.get('ticker', 'unknown')}: {e}")
            continue
    
    return pd.DataFrame(liquidity_data)


def merge_normalized_data(markets_df: pd.DataFrame, 
                          liquidity_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge markets and liquidity data
    
    Args:
        markets_df: Normalized markets DataFrame
        liquidity_df: Liquidity and spread DataFrame
        
    Returns:
        Merged DataFrame
    """
    if markets_df.empty or liquidity_df.empty:
        return markets_df
    
    merged = markets_df.merge(
        liquidity_df[['ticker', 'spread', 'mid_price', 'total_liquidity', 
                      'yes_best_bid', 'yes_best_ask']],
        on='ticker',
        how='left'
    )
    
    return merged
