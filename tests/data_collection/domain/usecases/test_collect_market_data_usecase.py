import pytest
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../src')))

from data_collection.domain.usecases.collect_market_data_usecase import CollectMarketDataUseCase
from data_collection.domain.model.asset_data import AssetData

class TestCollectMarketDataUseCase:
    
    def setup_method(self):
        self.mock_market_client = MagicMock()
        self.usecase = CollectMarketDataUseCase(market_client=self.mock_market_client)
        
    def test_fetch_daily_forwards_to_client(self):
        # provide mock data
        mock_assets = [
            AssetData(
                ticker="AAPL", timestamp_utc="2023-01-01", open_price=150.0,
                high_price=155.0, low_price=149.0, close_price=153.0, volume=1000000, source="yahoo_finance"
            )
        ]
        self.mock_market_client.fetch_daily.return_value = mock_assets
        
        # Fetch
        result = self.usecase.fetch_daily(ticker="AAPL", start_date="2023-01-01", end_date="2023-01-02")
        
        # Assert
        assert result == mock_assets
        self.mock_market_client.fetch_daily.assert_called_once_with("AAPL", "2023-01-01", "2023-01-02")

    def test_get_last_fetched_raw_data_forwards_to_client(self):
        # provide mock data
        mock_raw = {"meta": "data", "data": []}
        self.mock_market_client.get_last_fetched_raw_data.return_value = mock_raw
        
        # Fetch
        result = self.usecase.get_last_fetched_raw_data()
        
        # Assert
        assert result == mock_raw
        self.mock_market_client.get_last_fetched_raw_data.assert_called_once()

