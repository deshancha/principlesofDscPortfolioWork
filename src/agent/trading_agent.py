# Author: Chamika Deshan
# Created: 2026-04-03

import os
import sys

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.agent.domain.components.coin_analysis import CoinAnalysisModule
from src.agent.domain.components.information_retrieval import MockNewsItemModule
from src.agent.domain.components.decision_module import DecisionModule
from src.agent.domain.components.dicision_evaluate import DecisionEvaluateModule
from src.agent.domain.model.action import Action

class TradingAgent:
       
    def __init__(self, init_bal: float):
        self.init_bal = init_bal
        
        # analysis module
        self.market_analyzer = CoinAnalysisModule()

        # rag module
        self.rag_module = MockNewsItemModule()

        # decision module
        self.decision_engine = DecisionModule()
        self.risk_manager = DecisionEvaluateModule()

    def analyze_and_trade(self, ticker: str):
        print(f"------------------ Trading - [{ticker}] ------------------")
        
        # 1. Analyze
        coin_details = self.market_analyzer.get_coin_details(ticker)
        # 2. RAG - Get Info
        sentiment = self.rag_module.fetch_market_sentiment(ticker)
        # 3. Decide
        decision = self.decision_engine.decide(coin_details, sentiment)
        # 4. Evaluate decision
        final_decision = self.risk_manager.evaluate_decision(
            decision=decision['llm_decision'],
            coin_details=coin_details,
            balance=self.init_bal
        )

        buy_amount = final_decision['buy_amount']
        print(f"Decision: {final_decision['action'].value}")
        print(f"Buy Amount: ${buy_amount}")
        print(f"Reason: {final_decision['reason']}")

        if final_decision['action'] == Action.BUY:
            self.init_bal -= buy_amount
            print(f"Balance : {self.init_bal}")

        return final_decision


if __name__ == "__main__":
    agent = TradingAgent(init_bal=1000)
    
    test_tickers = ["BTC-USD", "DOGE-USD", "SOL-USD", "ETH-USD", "BNB-USD"]
    for coin in test_tickers:
        try:
            agent.analyze_and_trade(coin)
        except Exception as e:
            print(f"Error processing {coin}: {e}")
