# Author: Chamika Deshan
# Created: 2026-04-03

import os
import sys

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.agent.domain.components.coin_analysis import CoinAnalysisModule

class TradingAgent:
       
    def __init__(self, init_bal: float):
        self.init_bal = init_bal
        
        self.market_analyzer = CoinAnalysisModule()


if __name__ == "__main__":
    agent = TradingAgent(init_bal=1000)
