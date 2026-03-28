from typing import List
from data_collection.domain.manager.imarket_data_client import IMarketDataClient
from data_collection.domain.model.asset_data import AssetData

class CollectMarketDataUseCase:
    def __init__(self, market_client: IMarketDataClient):
        self.market_client = market_client
        
    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> List[AssetData]:
        return self.market_client.fetch_daily(ticker, start_date, end_date)
        
    def get_last_fetched_raw_data(self) -> dict:
        return self.market_client.get_last_fetched_raw_data()

