"""
MarketPress Main Application
BBC/Yahoo-style newspaper front page for prediction markets
"""
import pandas as pd
from typing import Optional

from kalshi_api import KalshiAPI, fetch_enriched_markets
from data_normalization import normalize_markets, normalize_snapshots, normalize_liquidity_spread, merge_normalized_data
from signals import compute_all_signals, rank_top_stories
from layout import organize_into_sections, identify_developing_stories, create_section_layout
from visualization import format_probability, format_delta, create_sparkline_from_snapshots
from editor import MarketPressEditor

try:
    from demo_data import generate_demo_markets
    DEMO_AVAILABLE = True
except ImportError:
    DEMO_AVAILABLE = False


class MarketPress:
    """
    Main MarketPress application class
    """
    
    def __init__(self, use_demo: bool = False):
        """
        Initialize MarketPress application
        
        Args:
            use_demo: If True, use demo data instead of live API
        """
        self.api = KalshiAPI()
        self.markets_df = pd.DataFrame()
        self.snapshots_df = pd.DataFrame()
        self.liquidity_df = pd.DataFrame()
        self.sections = {}
        self.editor = None
        self.use_demo = use_demo
    
    def fetch_data(self, limit: int = 100) -> bool:
        """
        Fetch fresh data from Kalshi API or use demo data
        
        Args:
            limit: Number of markets to fetch
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.use_demo:
                print("Using demo market data...")
                if not DEMO_AVAILABLE:
                    print("Demo data module not available")
                    return False
                raw_markets = generate_demo_markets(limit)
                print(f"Generated {len(raw_markets)} demo markets")
            else:
                print("Fetching market data from Kalshi...")
                # Fetch enriched market data
                raw_markets = fetch_enriched_markets(self.api, limit=limit)
                
                # If no markets fetched, try demo mode
                if not raw_markets:
                    print("No markets fetched from API, falling back to demo data...")
                    self.use_demo = True
                    return self.fetch_data(limit=limit)
            
            if not raw_markets:
                print("Warning: No markets available")
                return False
            
            print(f"Processing {len(raw_markets)} markets")
            
            # Normalize data into tables
            self.markets_df = normalize_markets(raw_markets)
            self.liquidity_df = normalize_liquidity_spread(raw_markets)
            
            # Create snapshot
            snapshot = normalize_snapshots(raw_markets)
            self.snapshots_df = pd.concat([self.snapshots_df, snapshot], ignore_index=True)
            
            # Merge liquidity data into markets
            self.markets_df = merge_normalized_data(self.markets_df, self.liquidity_df)
            
            print(f"Normalized {len(self.markets_df)} markets into tables")
            return True
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            if not self.use_demo:
                print("Falling back to demo data...")
                self.use_demo = True
                return self.fetch_data(limit=limit)
            return False
    
    def compute_signals(self):
        """Compute all trading signals"""
        print("Computing signals...")
        
        if self.markets_df.empty:
            print("No markets to compute signals for")
            return
        
        # Compute all signals using historical snapshots if available
        self.markets_df = compute_all_signals(self.markets_df, self.snapshots_df)
        
        print(f"Computed signals for {len(self.markets_df)} markets")
    
    def organize_sections(self):
        """Organize markets into sections"""
        print("Organizing into sections...")
        
        if self.markets_df.empty:
            print("No markets to organize")
            return
        
        # Rank top stories
        top_stories = rank_top_stories(self.markets_df, n=15)
        
        # Organize into category sections
        self.sections = organize_into_sections(self.markets_df)
        
        # Override top stories with ranked version
        self.sections['Top Stories'] = top_stories
        
        # Add developing stories section
        developing = identify_developing_stories(self.markets_df)
        self.sections['Developing'] = developing
        
        print(f"Organized into {len(self.sections)} sections")
    
    def initialize_editor(self):
        """Initialize the AI editor"""
        print("Initializing AI Editor...")
        
        if self.markets_df.empty:
            print("No data for editor")
            return
        
        self.editor = MarketPressEditor(self.markets_df, self.sections)
        print("Editor ready")
    
    def generate_front_page(self) -> str:
        """
        Generate the complete front page
        
        Returns:
            Formatted front page text
        """
        if self.markets_df.empty:
            return "No market data available. Please fetch data first."
        
        # Create the layout
        layout = create_section_layout(self.sections)
        
        return layout
    
    def get_section_dataframe(self, section_name: str) -> pd.DataFrame:
        """
        Get DataFrame for a specific section
        
        Args:
            section_name: Name of the section
            
        Returns:
            DataFrame for the section
        """
        return self.sections.get(section_name, pd.DataFrame())
    
    def get_market_details(self, ticker: str) -> Optional[pd.Series]:
        """
        Get details for a specific market
        
        Args:
            ticker: Market ticker
            
        Returns:
            Series with market details or None
        """
        if self.markets_df.empty:
            return None
        
        market_data = self.markets_df[self.markets_df['ticker'] == ticker]
        if market_data.empty:
            return None
        
        return market_data.iloc[0]
    
    def get_market_sparkline(self, ticker: str) -> str:
        """
        Get sparkline for a market
        
        Args:
            ticker: Market ticker
            
        Returns:
            Sparkline text
        """
        return create_sparkline_from_snapshots(ticker, self.snapshots_df, hours=24)
    
    def get_editor_summary(self) -> str:
        """
        Get AI editor's summary of the front page
        
        Returns:
            Editor summary text
        """
        if self.editor is None:
            self.initialize_editor()
        
        if self.editor is None:
            return "Editor not available"
        
        return self.editor.summarize_front_page()
    
    def ask_editor(self, query: str) -> str:
        """
        Ask the editor a question
        
        Args:
            query: Question to ask
            
        Returns:
            Editor's answer
        """
        if self.editor is None:
            self.initialize_editor()
        
        if self.editor is None:
            return "Editor not available"
        
        return self.editor.answer_query(query)
    
    def refresh(self, limit: int = 100):
        """
        Refresh all data and regenerate the front page
        
        Args:
            limit: Number of markets to fetch
        """
        print("\n" + "="*60)
        print("REFRESHING MARKETPRESS")
        print("="*60 + "\n")
        
        # Fetch fresh data
        if not self.fetch_data(limit=limit):
            print("Failed to fetch data")
            return
        
        # Compute signals
        self.compute_signals()
        
        # Organize sections
        self.organize_sections()
        
        # Initialize editor
        self.initialize_editor()
        
        print("\n✓ MarketPress refreshed successfully\n")


# Convenience functions for Hex integration

def create_marketpress_app(limit: int = 100, use_demo: bool = False) -> MarketPress:
    """
    Create and initialize a MarketPress application
    
    Args:
        limit: Number of markets to fetch
        use_demo: If True, use demo data instead of live API
        
    Returns:
        Initialized MarketPress instance
    """
    app = MarketPress(use_demo=use_demo)
    app.refresh(limit=limit)
    return app


def get_front_page_text(app: MarketPress) -> str:
    """
    Get the front page as text
    
    Args:
        app: MarketPress instance
        
    Returns:
        Front page text
    """
    return app.generate_front_page()


def get_section_table(app: MarketPress, section_name: str) -> pd.DataFrame:
    """
    Get a section as a formatted DataFrame for display
    
    Args:
        app: MarketPress instance
        section_name: Section name
        
    Returns:
        Formatted DataFrame
    """
    df = app.get_section_dataframe(section_name)
    
    if df.empty:
        return df
    
    # Select and format columns for display
    display_cols = ['title', 'yes_price', 'delta_24h', 'volume', 'attention_score']
    available_cols = [col for col in display_cols if col in df.columns]
    
    display_df = df[available_cols].copy()
    
    # Format percentages
    if 'yes_price' in display_df.columns:
        display_df['probability'] = display_df['yes_price'].apply(format_probability)
    
    if 'delta_24h' in display_df.columns:
        display_df['24h_change'] = display_df['delta_24h'].apply(format_delta)
    
    return display_df


def get_editor_summary(app: MarketPress) -> str:
    """
    Get editor summary
    
    Args:
        app: MarketPress instance
        
    Returns:
        Summary text
    """
    return app.get_editor_summary()


def ask_editor_question(app: MarketPress, question: str) -> str:
    """
    Ask the editor a question
    
    Args:
        app: MarketPress instance
        question: Question string
        
    Returns:
        Answer text
    """
    return app.ask_editor(question)


# Main execution example
if __name__ == "__main__":
    print("Starting MarketPress...")
    
    # Try live API first, fall back to demo
    # Create and initialize the app
    app = create_marketpress_app(limit=50, use_demo=False)
    
    # Display front page
    print("\n" + get_front_page_text(app))
    
    # Display editor summary
    print("\n" + get_editor_summary(app))
    
    # Example queries
    print("\n" + "="*60)
    print("EDITOR Q&A")
    print("="*60)
    
    questions = [
        "What are the top headlines?",
        "What's the biggest mover today?",
        "How many political markets are active?",
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: {ask_editor_question(app, q)}")
