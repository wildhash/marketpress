"""
Demo Data Generator
Provides sample market data for testing when API is unavailable
"""
from datetime import datetime, timedelta
import random


def generate_demo_markets(count: int = 50):
    """
    Generate demo market data for testing
    
    Args:
        count: Number of markets to generate
        
    Returns:
        List of market dictionaries
    """
    categories = ['Politics', 'Business', 'Tech', 'Sports', 'Culture']
    
    # Sample market templates
    templates = {
        'Politics': [
            "Will {party} win {state} in 2024?",
            "Will {candidate} lead in {state} polls by {date}?",
            "{bill} passes Congress by {date}",
            "Presidential approval rating above {num}% by {date}",
        ],
        'Business': [
            "S&P 500 above {num} by {date}",
            "{company} stock reaches ${num} by {date}",
            "Fed raises rates in {month}",
            "Inflation below {num}% by {date}",
        ],
        'Tech': [
            "{company} launches {product} by {date}",
            "AI model exceeds {num} parameters by {date}",
            "{tech} adoption reaches {num}% by {date}",
            "{company} market cap above ${num}B by {date}",
        ],
        'Sports': [
            "{team} wins {championship}",
            "{player} MVP by {date}",
            "{team} makes playoffs in {year}",
            "{sport} season starts by {date}",
        ],
        'Culture': [
            "{movie} wins Oscar for {category}",
            "{artist} releases album by {date}",
            "{show} renewed for season {num}",
            "{event} attendance exceeds {num} by {date}",
        ]
    }
    
    replacements = {
        'party': ['Democratic', 'Republican', 'Independent'],
        'state': ['Pennsylvania', 'Georgia', 'Arizona', 'Wisconsin', 'Nevada'],
        'candidate': ['Biden', 'Trump', 'Harris', 'DeSantis', 'Newsom'],
        'bill': ['Infrastructure Bill', 'Healthcare Reform', 'Tax Reform'],
        'company': ['Apple', 'Microsoft', 'Google', 'Amazon', 'Tesla', 'Meta'],
        'product': ['new iPhone', 'AI assistant', 'electric vehicle', 'VR headset'],
        'tech': ['5G', 'AI', 'Blockchain', 'Quantum Computing'],
        'team': ['Lakers', 'Yankees', 'Patriots', 'Cowboys', 'Warriors'],
        'championship': ['NBA Finals', 'World Series', 'Super Bowl'],
        'player': ['LeBron James', 'Aaron Judge', 'Patrick Mahomes'],
        'sport': ['NFL', 'NBA', 'MLB', 'NHL'],
        'movie': ['The Sequel', 'New Blockbuster', 'Indie Film'],
        'category': ['Best Picture', 'Best Director', 'Best Actor'],
        'artist': ['Taylor Swift', 'Drake', 'The Weeknd'],
        'show': ['Hit Series', 'Popular Drama', 'Comedy Show'],
        'event': ['Music Festival', 'Conference', 'Convention'],
        'month': ['March', 'June', 'September', 'December'],
        'year': ['2024', '2025'],
    }
    
    markets = []
    now = datetime.now()
    
    for i in range(count):
        category = random.choice(categories)
        template = random.choice(templates[category])
        
        # Replace placeholders
        title = template
        for key, values in replacements.items():
            if f'{{{key}}}' in title:
                title = title.replace(f'{{{key}}}', random.choice(values))
        
        # Replace {num} and {date}
        title = title.replace('{num}', str(random.randint(50, 150)))
        future_date = now + timedelta(days=random.randint(30, 365))
        title = title.replace('{date}', future_date.strftime('%b %Y'))
        
        # Generate market data
        base_price = random.randint(20, 80)
        delta = random.randint(-15, 15)
        
        ticker = f"DEMO-{i+1:03d}"
        
        market = {
            'ticker': ticker,
            'title': title,
            'subtitle': f"Market closes {future_date.strftime('%B %d, %Y')}",
            'event_ticker': f"EVENT-{random.randint(1, 20)}",
            'series_ticker': f"SERIES-{category.upper()}",
            'category': category,
            'status': 'open',
            'yes_price': base_price,
            'no_price': 100 - base_price,
            'last_price': base_price,
            'previous_yes_price': max(0, min(100, base_price - delta)),
            'open_time': (now - timedelta(days=random.randint(1, 90))).isoformat(),
            'close_time': future_date.isoformat(),
            'expiration_time': (future_date + timedelta(days=1)).isoformat(),
            'volume': random.randint(100, 50000),
            'open_interest': random.randint(50, 10000),
            'liquidity': random.randint(100, 5000),
            'result': '',
        }
        
        # Add orderbook data
        spread = random.uniform(0.01, 0.10)
        mid = base_price / 100.0
        
        market['orderbook'] = {
            'yes': [
                {'type': 'bid', 'price': int((mid - spread/2) * 100), 'quantity': random.randint(10, 500)},
                {'type': 'ask', 'price': int((mid + spread/2) * 100), 'quantity': random.randint(10, 500)},
            ],
            'no': [
                {'type': 'bid', 'price': int((1 - mid - spread/2) * 100), 'quantity': random.randint(10, 500)},
                {'type': 'ask', 'price': int((1 - mid + spread/2) * 100), 'quantity': random.randint(10, 500)},
            ]
        }
        
        # Add recent trades
        market['recent_trades'] = [
            {
                'price': base_price + random.randint(-5, 5),
                'quantity': random.randint(1, 100),
                'side': random.choice(['yes', 'no']),
                'created_time': (now - timedelta(minutes=random.randint(1, 120))).isoformat()
            }
            for _ in range(random.randint(3, 10))
        ]
        
        markets.append(market)
    
    return markets
