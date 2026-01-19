"""
MarketPress Smoke Test
Minimal test to ensure basic functionality works
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        import pandas as pd
        import numpy as np
        import requests
        print("  ✓ Dependencies imported")
    except ImportError as e:
        print(f"  ✗ Dependency import failed: {e}")
        return False
    
    try:
        from kalshi_api import KalshiAPI
        from data_normalization import normalize_markets, normalize_snapshots, normalize_liquidity_spread
        from signals import compute_all_signals, rank_top_stories
        from layout import organize_into_sections, identify_developing_stories
        from visualization import format_probability, format_delta
        from editor import MarketPressEditor
        from marketpress import MarketPress, create_marketpress_app
        print("  ✓ MarketPress modules imported")
    except ImportError as e:
        print(f"  ✗ Module import failed: {e}")
        return False
    
    return True


def test_demo_data_generation():
    """Test that demo data can be generated"""
    print("\nTesting demo data generation...")
    
    try:
        from demo_data import generate_demo_markets
        markets = generate_demo_markets(10)
        
        assert len(markets) == 10, f"Expected 10 markets, got {len(markets)}"
        assert all('ticker' in m for m in markets), "Missing ticker field"
        assert all('title' in m for m in markets), "Missing title field"
        # Demo data may have bid/ask or just price fields
        
        print("  ✓ Demo data generated successfully")
        return True
    except Exception as e:
        print(f"  ✗ Demo data generation failed: {e}")
        return False


def test_data_normalization():
    """Test that data can be normalized into tables"""
    print("\nTesting data normalization...")
    
    try:
        from demo_data import generate_demo_markets
        from data_normalization import normalize_markets, normalize_snapshots, normalize_liquidity_spread
        import pandas as pd
        
        raw_markets = generate_demo_markets(10)
        
        # Normalize
        markets_df = normalize_markets(raw_markets)
        snapshots_df = normalize_snapshots(raw_markets)
        liquidity_df = normalize_liquidity_spread(raw_markets)
        
        assert isinstance(markets_df, pd.DataFrame), "markets_df is not a DataFrame"
        assert len(markets_df) == 10, f"Expected 10 markets, got {len(markets_df)}"
        assert 'ticker' in markets_df.columns, "Missing ticker column"
        assert 'yes_price' in markets_df.columns, "Missing yes_price column"
        
        assert isinstance(snapshots_df, pd.DataFrame), "snapshots_df is not a DataFrame"
        assert isinstance(liquidity_df, pd.DataFrame), "liquidity_df is not a DataFrame"
        
        print("  ✓ Data normalized successfully")
        return True
    except Exception as e:
        print(f"  ✗ Data normalization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_signal_computation():
    """Test that signals can be computed"""
    print("\nTesting signal computation...")
    
    try:
        from demo_data import generate_demo_markets
        from data_normalization import normalize_markets, normalize_snapshots, normalize_liquidity_spread
        from signals import compute_all_signals
        
        raw_markets = generate_demo_markets(10)
        markets_df = normalize_markets(raw_markets)
        snapshots_df = normalize_snapshots(raw_markets)
        liquidity_df = normalize_liquidity_spread(raw_markets)
        
        # Compute signals - compute_all_signals takes markets_df and optional historical_snapshots
        markets_df = compute_all_signals(markets_df, snapshots_df)
        
        assert 'attention_score' in markets_df.columns, "Missing attention_score"
        assert 'volatility' in markets_df.columns, "Missing volatility"
        assert 'confidence_score' in markets_df.columns, "Missing confidence_score"
        # newsworthiness is computed separately in rank_top_stories
        
        print("  ✓ Signals computed successfully")
        return True
    except Exception as e:
        print(f"  ✗ Signal computation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_marketpress_app():
    """Test that MarketPress app can be created and used"""
    print("\nTesting MarketPress app...")
    
    try:
        from marketpress import create_marketpress_app
        
        # Create app with demo data
        app = create_marketpress_app(limit=10, use_demo=True)
        
        assert app is not None, "App creation failed"
        assert hasattr(app, 'markets_df'), "App missing markets_df"
        assert len(app.markets_df) > 0, "No markets in app"
        
        # Test section access
        sections = ['Top Stories', 'Politics', 'Business', 'Tech', 'Culture']
        for section in sections:
            df = app.get_section_dataframe(section)
            assert df is not None, f"Failed to get {section} section"
        
        print("  ✓ MarketPress app works")
        return True
    except Exception as e:
        print(f"  ✗ MarketPress app failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_hex_cells():
    """Test that hex cell code can be executed"""
    print("\nTesting hex cells...")
    
    try:
        # This is a basic test - in a full test we'd execute each cell
        import os
        hex_cells_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hex_cells')
        
        expected_cells = [
            '01_setup.py',
            '02_fetch_kalshi.py',
            '03_normalize.py',
            '04_signals.py',
            '05_sections.py',
            '06_frontpage.py',
            '07_drilldown.py',
            '08_editor.py'
        ]
        
        for cell in expected_cells:
            cell_path = os.path.join(hex_cells_dir, cell)
            assert os.path.exists(cell_path), f"Missing hex cell: {cell}"
        
        print("  ✓ All hex cells present")
        return True
    except Exception as e:
        print(f"  ✗ Hex cells check failed: {e}")
        return False


def run_smoke_tests():
    """Run all smoke tests"""
    print("="*60)
    print("MARKETPRESS SMOKE TESTS")
    print("="*60)
    
    tests = [
        test_imports,
        test_demo_data_generation,
        test_data_normalization,
        test_signal_computation,
        test_marketpress_app,
        test_hex_cells
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n  ✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✓ All smoke tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(run_smoke_tests())
