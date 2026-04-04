# Author: Chamika Deshan
# Created: 2026-04-03

import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class CoinAnalysisModule:
    """
    Analyzes market data with clustering
    """
    
    def __init__(self):
        # From EDA Clustering we found this values, ref - eda_coin_clustering.ipynb
        # Volatality - STD of Daily Growth
        # Mean Return - Mean of Daily Close
        self.cluster_mapping = {
            "BTC-USD": {
                "cluster": 2,
                "volatility": 0.025,
                "mean_return": 0.0008,
            },
            "BNB-USD": {
                "cluster": 2,
                "volatility": 0.028,
                "mean_return": 0.0012,
            },
            "ETH-USD": {
                "cluster": 0,
                "volatility": 0.037,
                "mean_return": 0.0005,
            },
            "SOL-USD": {
                "cluster": 0,
                "volatility": 0.043,
                "mean_return": 0.0006,
            },
            
            "DOGE-USD": {
                "cluster": 1,
                "volatility": 0.050,
                "mean_return": 0.0013,
            }
        }

    def get_coin_details(self, ticker: str) -> dict:
        """
        Returns details [ticker, cluster_id, risk_cluster, daily_volatility, mean_daily_return]
        """
        if ticker not in self.cluster_mapping:
            raise ValueError(f"Ticker {ticker} not found!")
            
        profile = self.cluster_mapping[ticker]
        cluster = profile['cluster']
        
        # We use pre calcualted cluster values
        # BTC, BNB - Low | ETH, SOL - Medium | DOGE - High
        if profile['volatility'] >= 0.045:
            # Speculative
            risk_cluster = "High"
        elif profile['volatility'] >= 0.035:
            # Has Growth
            risk_cluster = "Medium"
        else:
            # Stable
            risk_cluster = "Low"
            
        return {
            "ticker": ticker,
            "cluster_id": cluster,
            "risk_cluster": risk_cluster,
            "daily_volatility": profile['volatility'],
            "mean_daily_return": profile['mean_return']
        }
