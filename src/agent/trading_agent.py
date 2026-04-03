# Author: Chamika Deshan
# Created: 2026-04-03

import os
import sys

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.agent.domain.components.coin_analysis import CoinAnalysisModule
from src.agent.domain.components.information_retrieval import MockNewsItemModule
from src.agent.domain.components.decision_module import DecisionModule
class TradingAgent:
       
    def __init__(self, init_bal: float):
        self.init_bal = init_bal
        # analysis module
        self.market_analyzer = CoinAnalysisModule()
        # rag module
        self.rag_module = MockNewsItemModule()
        # decision module
        self.decision_engine = DecisionModule()

    def analyze_and_trade(self, ticker: str):
        print(f"Trading - [{ticker}]")
        
        # 1. Analyze
        profile = self.market_analyzer.get_coin_details(ticker)
        
        # 2. RAG - Get Info
        sentiment = self.rag_module.fetch_market_sentiment(ticker)
        
        # 3. Decide
        decision = self.decision_engine.decide(profile, sentiment)

if __name__ == "__main__":
    agent = TradingAgent(init_bal=1000)
    
    test_tickers = ["BTC-USD", "DOGE-USD", "SOL-USD"]
    for coin in test_tickers:
        try:
            agent.analyze_and_trade(coin)
        except Exception as e:
            print(f"Error - {coin}: {e}")
