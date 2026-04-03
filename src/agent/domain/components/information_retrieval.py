# Author: Chamika Deshan
# Created: 2026-04-03

import random

class MockNewsItemModule:
    """
    Mock News Item from Api
    """
    
    def __init__(self):
        self.mock_sentiments = {
            "BTC-USD": "BEARISH",
            "ETH-USD": "BULLISH",
            "SOL-USD": "BEARISH",
            "BNB-USD": "BULLISH",
            "DOGE-USD": "BULLISH"
        }

    def fetch_market_sentiment(self, ticker: str) -> dict:
        sentiment = self.mock_sentiments.get(ticker)
            
        return {
            "ticker": ticker,
            "sentiment_label": sentiment
        }
