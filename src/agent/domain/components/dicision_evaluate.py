from src.agent.domain.model.action import Action

class DecisionEvaluateModule:
    """
    Trade Based on Cluster
    """
    
    def __init__(self):
        pass

    def evaluate_decision(self, decision: Action, coin_details: dict, balance: float) -> dict:
        # Sell
        if decision == Action.SELL:
            return {
                "action": Action.SELL,
                "buy_amount": 0.0,
                "reason": "Just Sell"
            }

        cluster_id = coin_details.get("cluster_id")

        buy_percentage = 0.0
        rationale = ""
        
        # Based on cluster we decide the buy percentage
        if cluster_id == 2:
            # Rise low - BTC
            buy_percentage = 20
            rationale = "Low Risk -> 20%"
        elif cluster_id == 0:
            # Risk medium - ETH, SOL
            buy_percentage = 10
            rationale = "Mid Risk -> 10%"
        elif cluster_id == 1:
            # Risk high - BNB, DOGE
            buy_percentage = 1
            rationale = "High Risk -> 1%"
            
        buy_amount = balance * (buy_percentage/100)

        return {
            "action": Action.BUY,
            "buy_amount": buy_amount,
            "reason": rationale
        }
