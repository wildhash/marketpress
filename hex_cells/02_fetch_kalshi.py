"""
MarketPress Hex Cell 2: Fetch Kalshi Data
Pull public Kalshi market data with pagination, raw JSON capture
"""

def fetch_kalshi_markets(limit: int = 100, status: str = 'open') -> List[Dict]:
    """
    Fetch markets from Kalshi API
    
    Args:
        limit: Number of markets to fetch
        status: Market status (open, closed, settled)
        
    Returns:
        List of market dictionaries
    """
    markets = []
    cursor = None
    
    while len(markets) < limit:
        try:
            url = f"{KALSHI_BASE_URL}/markets"
            params = {
                'limit': min(200, limit - len(markets)),
                'status': status
            }
            if cursor:
                params['cursor'] = cursor
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            batch = data.get('markets', [])
            if not batch:
                break
                
            markets.extend(batch)
            
            cursor = data.get('cursor')
            if not cursor:
                break
                
            time.sleep(RATE_LIMIT_DELAY)
            
        except Exception as e:
            print(f"API error: {e}")
            break
    
    return markets[:limit]


def fetch_orderbook(ticker: str) -> Optional[Dict]:
    """Fetch orderbook for a market"""
    try:
        url = f"{KALSHI_BASE_URL}/markets/{ticker}/orderbook"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None


def generate_demo_markets(limit: int = 100) -> List[Dict]:
    """Generate demo market data for testing"""
    categories = list(CATEGORY_MAPPINGS.keys())
    templates = [
        "Will {candidate} win {state} in 2024?",
        "{company} market cap above ${amount}B by {month} {year}",
        "Fed raises rates in {month}",
        "Inflation below {pct}% by {month} {year}",
        "{artist} releases album by {month} {year}",
        "{team} wins championship",
        "Conference attendance exceeds {num} by {month} {year}",
        "Presidential approval rating above {pct}% by {month} {year}",
        "{company} launches {product} by {month} {year}",
        "Infrastructure Bill passes Congress by {month} {year}"
    ]
    
    markets = []
    for i in range(limit):
        category = np.random.choice(categories)
        template = np.random.choice(templates)
        
        # Fill template
        title = template.format(
            candidate=np.random.choice(['Trump', 'Biden', 'Independent']),
            state=np.random.choice(['Texas', 'California', 'Florida', 'New York', 'Georgia', 'Wisconsin']),
            company=np.random.choice(['Apple', 'Tesla', 'Microsoft', 'Amazon', 'Google']),
            amount=np.random.randint(50, 200),
            month=np.random.choice(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
            year=np.random.choice([2026]),
            artist=np.random.choice(['Taylor Swift', 'Drake', 'Beyonce', 'Kendrick Lamar']),
            team=np.random.choice(['Lakers', 'Warriors', 'Yankees', 'Red Sox']),
            num=np.random.randint(100, 200),
            pct=np.random.randint(20, 150),
            product=np.random.choice(['AI assistant', 'new iPhone', 'electric car'])
        )
        
        yes_price = np.random.uniform(0.15, 0.85)
        volume = int(np.random.lognormal(10, 2))
        open_interest = int(volume * np.random.uniform(0.5, 2.0))
        
        market = {
            'ticker': f'DEMO-{i:03d}',
            'title': title,
            'category': category.lower(),
            'yes_bid': yes_price - 0.01,
            'yes_ask': yes_price + 0.01,
            'volume': volume,
            'open_interest': open_interest,
            'close_time': (datetime.now() + timedelta(days=np.random.randint(30, 365))).isoformat(),
            'status': 'open'
        }
        markets.append(market)
    
    return markets


# Fetch data
print("Fetching market data...")
if USE_DEMO_DATA:
    print("Using demo market data...")
    raw_markets = generate_demo_markets(MARKET_LIMIT)
    print(f"Generated {len(raw_markets)} demo markets")
else:
    print("Fetching from Kalshi API...")
    raw_markets = fetch_kalshi_markets(MARKET_LIMIT)
    print(f"Fetched {len(raw_markets)} markets from API")

print(f"✓ Data fetched: {len(raw_markets)} markets")
