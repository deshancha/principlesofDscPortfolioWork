# Author: Chamika Deshan
# Created: 2026-04-03

class DecisionModule:
    """
    Simulates Agentic Decisions - Get the sentiment and returns BUY or SELL decision
    """

    def decide(self, asset_profile: dict, sentiment_data: dict) -> dict:
        sentiment = sentiment_data.get('sentiment_label')
        
        if sentiment == "BULLISH":
            decision = "BUY"
            reason = "Positive -> Buy!"
        else:
            decision = "SELL"
            reason = "Negative -> Sell!"
            
        return {
            "llm_decision": decision,
            "llm_reason": reason
        }
