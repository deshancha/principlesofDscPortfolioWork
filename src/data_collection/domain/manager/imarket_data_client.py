# Author: Chamika Deshan
# Created: 2026-03-28

from abc import ABC, abstractmethod
from typing import List
from ..model.asset_data import AssetData

class IMarketDataClient(ABC):
    """
    Financial Data Collection
    """
    
    @abstractmethod
    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> List[AssetData]:
        """
        Fetch daily data
        """
        pass
    
    @abstractmethod
    def get_last_fetched_raw_data(self) -> dict:
        """
        Get the last fetched raw data
        """
        pass
