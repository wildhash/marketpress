"""
Signal Computation Module
Computes trading signals and metrics for market analysis
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta


def compute_probability_changes(current_df: pd.DataFrame, 
                                historical_snapshots: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Compute probability changes over 24h and 7d periods
    
    Args:
        current_df: Current market data with yes_price
        historical_snapshots: Historical snapshot data (if available)
        
    Returns:
        DataFrame with delta columns added
    """
    df = current_df.copy()
    
    # Initialize delta columns
    df['delta_24h'] = np.nan
    df['delta_7d'] = np.nan
    
    if historical_snapshots is None or historical_snapshots.empty:
        # Use previous_yes_price if available as a proxy for 24h change
        if 'previous_yes_price' in df.columns and 'yes_price' in df.columns:
            df['delta_24h'] = df['yes_price'] - df['previous_yes_price']
        return df
    
    # Calculate actual changes from historical data
    now = pd.Timestamp.now()
    h24_ago = now - timedelta(hours=24)
    d7_ago = now - timedelta(days=7)
    
    for ticker in df['ticker'].unique():
        ticker_snapshots = historical_snapshots[historical_snapshots['ticker'] == ticker].copy()
        
        if ticker_snapshots.empty:
            continue
        
        ticker_snapshots = ticker_snapshots.sort_values('snapshot_time')
        current_price = df.loc[df['ticker'] == ticker, 'yes_price'].iloc[0] if not df[df['ticker'] == ticker].empty else None
        
        if current_price is None:
            continue
        
        # Find 24h price
        h24_snapshots = ticker_snapshots[ticker_snapshots['snapshot_time'] <= h24_ago]
        if not h24_snapshots.empty:
            h24_price = h24_snapshots.iloc[-1]['yes_price']
            df.loc[df['ticker'] == ticker, 'delta_24h'] = current_price - h24_price
        
        # Find 7d price
        d7_snapshots = ticker_snapshots[ticker_snapshots['snapshot_time'] <= d7_ago]
        if not d7_snapshots.empty:
            d7_price = d7_snapshots.iloc[-1]['yes_price']
            df.loc[df['ticker'] == ticker, 'delta_7d'] = current_price - d7_price
    
    return df


def compute_volatility(snapshots_df: pd.DataFrame, window_hours: int = 24) -> pd.DataFrame:
    """
    Compute price volatility for each market
    
    Args:
        snapshots_df: Historical snapshot data
        window_hours: Time window for volatility calculation
        
    Returns:
        DataFrame with ticker and volatility
    """
    if snapshots_df.empty:
        return pd.DataFrame(columns=['ticker', 'volatility'])
    
    cutoff_time = pd.Timestamp.now() - timedelta(hours=window_hours)
    recent_snapshots = snapshots_df[snapshots_df['snapshot_time'] >= cutoff_time].copy()
    
    volatility_data = []
    
    for ticker in recent_snapshots['ticker'].unique():
        ticker_data = recent_snapshots[recent_snapshots['ticker'] == ticker].copy()
        
        if len(ticker_data) < 2:
            continue
        
        ticker_data = ticker_data.sort_values('snapshot_time')
        prices = ticker_data['yes_price'].dropna()
        
        if len(prices) < 2:
            continue
        
        # Calculate standard deviation of prices
        volatility = prices.std()
        
        volatility_data.append({
            'ticker': ticker,
            'volatility': volatility,
            'price_observations': len(prices)
        })
    
    return pd.DataFrame(volatility_data)


def compute_attention_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute attention metrics based on volume and open interest
    
    Args:
        df: Market data with volume and open_interest columns
        
    Returns:
        DataFrame with attention score added
    """
    df = df.copy()
    
    # Normalize volume and OI to 0-1 range
    if 'volume' in df.columns and 'open_interest' in df.columns:
        max_volume = df['volume'].max() if df['volume'].max() > 0 else 1
        max_oi = df['open_interest'].max() if df['open_interest'].max() > 0 else 1
        
        df['volume_score'] = df['volume'] / max_volume
        df['oi_score'] = df['open_interest'] / max_oi
        
        # Attention score is weighted average (60% volume, 40% OI)
        df['attention_score'] = 0.6 * df['volume_score'] + 0.4 * df['oi_score']
    else:
        df['attention_score'] = 0.0
    
    return df


def compute_confidence_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute confidence metrics based on spread
    
    Args:
        df: Market data with spread column
        
    Returns:
        DataFrame with confidence score added
    """
    df = df.copy()
    
    if 'spread' not in df.columns:
        df['confidence_score'] = 0.5  # Neutral default
        return df
    
    # Tighter spread = higher confidence
    # Normalize: spread of 0 = confidence 1.0, spread of 0.10+ = confidence 0
    df['confidence_score'] = df['spread'].apply(
        lambda x: max(0, 1.0 - (x * 10)) if pd.notna(x) else 0.5
    )
    
    return df


def compute_all_signals(markets_df: pd.DataFrame, 
                        historical_snapshots: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Compute all signals for markets
    
    Args:
        markets_df: Current market data
        historical_snapshots: Historical snapshot data
        
    Returns:
        DataFrame with all signals computed
    """
    df = markets_df.copy()
    
    # Probability changes
    df = compute_probability_changes(df, historical_snapshots)
    
    # Volatility (if we have historical data)
    if historical_snapshots is not None and not historical_snapshots.empty:
        volatility_df = compute_volatility(historical_snapshots)
        if not volatility_df.empty and 'ticker' in volatility_df.columns and 'volatility' in volatility_df.columns:
            df = df.merge(volatility_df[['ticker', 'volatility']], on='ticker', how='left')
        else:
            df['volatility'] = np.nan
    else:
        df['volatility'] = np.nan
    
    # Attention metrics
    df = compute_attention_metrics(df)
    
    # Confidence metrics
    df = compute_confidence_metrics(df)
    
    return df


def rank_top_stories(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Rank markets by "newsworthiness" for top stories
    
    Args:
        df: Markets with computed signals
        n: Number of top stories to return
        
    Returns:
        DataFrame with top n stories
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Newsworthiness score based on:
    # - Large probability changes (40%)
    # - High attention (30%)
    # - High confidence (20%)
    # - Recent volatility (10%)
    
    # Normalize delta_24h
    abs_delta = df['delta_24h'].fillna(0).abs()
    max_delta = abs_delta.max() if abs_delta.max() > 0 else 1
    delta_score = abs_delta / max_delta
    
    # Use existing normalized scores
    attention = df['attention_score'].fillna(0)
    confidence = df['confidence_score'].fillna(0.5)
    
    # Normalize volatility
    vol = df['volatility'].fillna(0)
    max_vol = vol.max() if vol.max() > 0 else 1
    vol_score = vol / max_vol
    
    df['newsworthiness'] = (
        0.4 * delta_score + 
        0.3 * attention + 
        0.2 * confidence + 
        0.1 * vol_score
    )
    
    # Sort and return top n
    top_stories = df.nlargest(n, 'newsworthiness')
    
    return top_stories
