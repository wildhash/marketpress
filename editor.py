"""
Hex Thread Editor Module
Provides AI-powered summarization and query answering for the MarketPress front page
"""
import pandas as pd
from typing import Dict, List, Optional


class MarketPressEditor:
    """
    AI Editor for MarketPress - provides summaries and answers queries about market data
    """
    
    def __init__(self, markets_df: pd.DataFrame, sections: Dict[str, pd.DataFrame]):
        """
        Initialize the editor with market data
        
        Args:
            markets_df: Complete markets DataFrame
            sections: Dictionary of section DataFrames
        """
        self.markets_df = markets_df
        self.sections = sections
        self.semantic_model = self._build_semantic_model()
    
    def _build_semantic_model(self) -> Dict:
        """
        Build a semantic model of the current market state
        
        Returns:
            Dictionary with key statistics and trends
        """
        if self.markets_df.empty:
            return {}
        
        model = {
            'total_markets': len(self.markets_df),
            'active_categories': self.markets_df['section'].nunique() if 'section' in self.markets_df.columns else 0,
            'total_volume': self.markets_df['volume'].sum() if 'volume' in self.markets_df.columns else 0,
            'total_open_interest': self.markets_df['open_interest'].sum() if 'open_interest' in self.markets_df.columns else 0,
            'avg_probability': self.markets_df['yes_price'].mean() if 'yes_price' in self.markets_df.columns else 0,
            'markets_up': len(self.markets_df[self.markets_df['delta_24h'] > 0]) if 'delta_24h' in self.markets_df.columns else 0,
            'markets_down': len(self.markets_df[self.markets_df['delta_24h'] < 0]) if 'delta_24h' in self.markets_df.columns else 0,
            'highest_confidence': None,
            'highest_attention': None,
            'biggest_mover_up': None,
            'biggest_mover_down': None,
        }
        
        # Find highest confidence market
        if 'confidence_score' in self.markets_df.columns:
            conf_idx = self.markets_df['confidence_score'].idxmax()
            if pd.notna(conf_idx):
                model['highest_confidence'] = {
                    'title': self.markets_df.loc[conf_idx, 'title'],
                    'probability': self.markets_df.loc[conf_idx, 'yes_price'],
                    'score': self.markets_df.loc[conf_idx, 'confidence_score']
                }
        
        # Find highest attention market
        if 'attention_score' in self.markets_df.columns:
            att_idx = self.markets_df['attention_score'].idxmax()
            if pd.notna(att_idx):
                model['highest_attention'] = {
                    'title': self.markets_df.loc[att_idx, 'title'],
                    'probability': self.markets_df.loc[att_idx, 'yes_price'],
                    'score': self.markets_df.loc[att_idx, 'attention_score']
                }
        
        # Find biggest movers
        if 'delta_24h' in self.markets_df.columns:
            up_markets = self.markets_df[self.markets_df['delta_24h'] > 0]
            if not up_markets.empty:
                up_idx = up_markets['delta_24h'].idxmax()
                model['biggest_mover_up'] = {
                    'title': self.markets_df.loc[up_idx, 'title'],
                    'probability': self.markets_df.loc[up_idx, 'yes_price'],
                    'delta': self.markets_df.loc[up_idx, 'delta_24h']
                }
            
            down_markets = self.markets_df[self.markets_df['delta_24h'] < 0]
            if not down_markets.empty:
                down_idx = down_markets['delta_24h'].idxmin()
                model['biggest_mover_down'] = {
                    'title': self.markets_df.loc[down_idx, 'title'],
                    'probability': self.markets_df.loc[down_idx, 'yes_price'],
                    'delta': self.markets_df.loc[down_idx, 'delta_24h']
                }
        
        return model
    
    def summarize_front_page(self) -> str:
        """
        Generate an executive summary of the front page
        
        Returns:
            Summary text
        """
        summary_parts = []
        
        summary_parts.append("📰 MARKETPRESS EDITOR'S SUMMARY")
        summary_parts.append("=" * 60)
        summary_parts.append("")
        
        # Overall market state
        total = self.semantic_model.get('total_markets', 0)
        up = self.semantic_model.get('markets_up', 0)
        down = self.semantic_model.get('markets_down', 0)
        
        summary_parts.append(f"Tracking {total} active prediction markets today.")
        
        if up > 0 or down > 0:
            up_pct = (up / total * 100) if total > 0 else 0
            down_pct = (down / total * 100) if total > 0 else 0
            summary_parts.append(f"Market sentiment: {up} markets up ({up_pct:.0f}%), {down} down ({down_pct:.0f}%).")
        
        summary_parts.append("")
        
        # Top stories overview
        if 'Top Stories' in self.sections and not self.sections['Top Stories'].empty:
            top_section = self.sections['Top Stories']
            summary_parts.append("TOP HEADLINES:")
            
            for idx, row in top_section.head(3).iterrows():
                title = row.get('title', 'Unknown')
                prob = row.get('yes_price', 0)
                delta = row.get('delta_24h', 0)
                
                prob_str = f"{prob * 100:.0f}%" if prob else "N/A"
                
                if delta and pd.notna(delta):
                    sign = "up" if delta > 0 else "down"
                    delta_str = f"{abs(delta) * 100:.0f}%"
                    summary_parts.append(f"  • {title}: {prob_str} ({sign} {delta_str})")
                else:
                    summary_parts.append(f"  • {title}: {prob_str}")
            
            summary_parts.append("")
        
        # Biggest movers
        up_mover = self.semantic_model.get('biggest_mover_up')
        down_mover = self.semantic_model.get('biggest_mover_down')
        
        if up_mover or down_mover:
            summary_parts.append("NOTABLE MOVEMENTS:")
            
            if up_mover:
                title = up_mover['title']
                delta = up_mover['delta'] * 100
                prob = up_mover['probability'] * 100 if up_mover['probability'] else 0
                summary_parts.append(f"  ↑ Biggest gain: {title} (+{delta:.0f}% to {prob:.0f}%)")
            
            if down_mover:
                title = down_mover['title']
                delta = abs(down_mover['delta']) * 100
                prob = down_mover['probability'] * 100 if down_mover['probability'] else 0
                summary_parts.append(f"  ↓ Biggest drop: {title} (-{delta:.0f}% to {prob:.0f}%)")
            
            summary_parts.append("")
        
        # Attention and confidence highlights
        attention = self.semantic_model.get('highest_attention')
        if attention:
            title = attention['title']
            summary_parts.append(f"MOST WATCHED: {title}")
            summary_parts.append("")
        
        # Section summaries
        summary_parts.append("SECTION HIGHLIGHTS:")
        for section_name in ['Politics', 'Business', 'Tech', 'Culture', 'Sports']:
            if section_name in self.sections and not self.sections[section_name].empty:
                count = len(self.sections[section_name])
                summary_parts.append(f"  {section_name}: {count} active markets")
        
        summary_parts.append("")
        summary_parts.append("=" * 60)
        
        return "\n".join(summary_parts)
    
    def answer_query(self, query: str) -> str:
        """
        Answer a query about the markets
        
        Args:
            query: User query string
            
        Returns:
            Answer text
        """
        query_lower = query.lower()
        
        # Handle different types of queries
        if 'how many' in query_lower or 'count' in query_lower:
            return self._answer_count_query(query_lower)
        elif 'biggest' in query_lower or 'largest' in query_lower or 'top' in query_lower:
            return self._answer_biggest_query(query_lower)
        elif 'what' in query_lower or 'which' in query_lower:
            return self._answer_what_query(query_lower)
        elif 'average' in query_lower or 'mean' in query_lower:
            return self._answer_average_query(query_lower)
        else:
            return self._answer_general_query(query_lower)
    
    def _answer_count_query(self, query: str) -> str:
        """Answer counting queries"""
        total = self.semantic_model.get('total_markets', 0)
        
        if 'politics' in query or 'political' in query:
            if 'Politics' in self.sections:
                count = len(self.sections['Politics'])
                return f"There are {count} political markets currently active."
        elif 'business' in query or 'economic' in query:
            if 'Business' in self.sections:
                count = len(self.sections['Business'])
                return f"There are {count} business/economic markets currently active."
        elif 'tech' in query:
            if 'Tech' in self.sections:
                count = len(self.sections['Tech'])
                return f"There are {count} technology markets currently active."
        
        return f"There are {total} total markets currently active across all categories."
    
    def _answer_biggest_query(self, query: str) -> str:
        """Answer queries about biggest/largest/top items"""
        if 'mover' in query or 'change' in query:
            up_mover = self.semantic_model.get('biggest_mover_up')
            down_mover = self.semantic_model.get('biggest_mover_down')
            
            if 'up' in query and up_mover:
                title = up_mover['title']
                delta = up_mover['delta'] * 100
                return f"The biggest gainer is '{title}', up {delta:.1f}% in 24 hours."
            elif 'down' in query and down_mover:
                title = down_mover['title']
                delta = abs(down_mover['delta']) * 100
                return f"The biggest decliner is '{title}', down {delta:.1f}% in 24 hours."
            
            if up_mover and down_mover:
                return f"Biggest gain: '{up_mover['title']}' (+{up_mover['delta']*100:.1f}%). Biggest drop: '{down_mover['title']}' ({down_mover['delta']*100:.1f}%)."
        
        if 'attention' in query or 'watched' in query or 'popular' in query:
            attention = self.semantic_model.get('highest_attention')
            if attention:
                title = attention['title']
                return f"The most watched market is '{title}' with the highest trading activity."
        
        return "I can tell you about the biggest movers, most watched markets, or highest confidence predictions. What would you like to know?"
    
    def _answer_what_query(self, query: str) -> str:
        """Answer what/which queries"""
        if 'top' in query or 'headline' in query or 'main' in query:
            if 'Top Stories' in self.sections and not self.sections['Top Stories'].empty:
                top_story = self.sections['Top Stories'].iloc[0]
                title = top_story.get('title', 'Unknown')
                prob = top_story.get('yes_price', 0) * 100
                return f"The top headline is: '{title}' at {prob:.0f}%."
        
        return self.summarize_front_page()
    
    def _answer_average_query(self, query: str) -> str:
        """Answer queries about averages"""
        avg_prob = self.semantic_model.get('avg_probability', 0)
        return f"The average market probability across all markets is {avg_prob * 100:.0f}%."
    
    def _answer_general_query(self, query: str) -> str:
        """Handle general queries"""
        return "I can help you understand the market data. Try asking about: the biggest movers, most watched markets, top headlines, or market counts by category."
