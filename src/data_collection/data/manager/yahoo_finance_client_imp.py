import yfinance as yf
from datetime import datetime
from typing import List
from data_collection.domain.manager.imarket_data_client import IMarketDataClient
from data_collection.domain.model.asset_data import AssetData
from core.util.logger import ILogger

class _Messages:
    """Private message constants for YahooFinanceClientImp logging."""
    FETCH_START = "Fetching daily data for {ticker} from {start_date} to {end_date} via Yahoo Finance..."
    FETCH_EMPTY = "No data found for {ticker} between {start_date} and {end_date}."
    FETCH_SUCCESS = "Successfully fetched {record_count} records for {ticker}."
    FETCH_ERROR = "Failed to fetch data for {ticker} from Yahoo Finance: {error}"

class YahooFinanceClientImp(IMarketDataClient):
    """
    Imp of Fetch Market Data with Yahoo Finance.
    """
    def __init__(self, logger: ILogger):
        self._last_fetched_data = {}
        self.logger = logger
        
    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> List[AssetData]:
        self.logger.info(_Messages.FETCH_START.format(ticker=ticker, start_date=start_date, end_date=end_date))
        try:
            ticker_obj = yf.Ticker(ticker)
            # Download
            df = ticker_obj.history(start=start_date, end=end_date, interval="1d")
            
            if df.empty:
                self.logger.warning(_Messages.FETCH_EMPTY.format(ticker=ticker, start_date=start_date, end_date=end_date))
                return []
                
            self.logger.info(_Messages.FETCH_SUCCESS.format(record_count=len(df), ticker=ticker))
            
            # Temp save last fetched raw data for access
            self._last_fetched_data = {
                "meta": {
                    "source": "yahoo_finance",
                    "ticker": ticker,
                    "start_date": start_date,
                    "end_date": end_date,
                    "fetched_at": datetime.utcnow().isoformat()
                },
                # Pandas serialization trick for raw dumps
                "data": df.reset_index().to_dict(orient="records")
            }
            
            assets = []
            for index, row in df.iterrows():
                assets.append(
                    AssetData(
                        ticker=ticker,
                        timestamp_utc=str(index.date()), # Convert pandas timestamp to string
                        open_price=float(row['Open']),
                        high_price=float(row['High']),
                        low_price=float(row['Low']),
                        close_price=float(row['Close']),
                        volume=int(row['Volume']),
                        source="yahoo_finance"
                    )
                )
            return assets
            
        except Exception as e:
            self.logger.error(_Messages.FETCH_ERROR.format(ticker=ticker, error=str(e)))
            raise e
        
    def get_last_fetched_raw_data(self) -> dict:
        return self._last_fetched_data
