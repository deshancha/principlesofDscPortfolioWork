# Author: Chamika Deshan
# Created: 2026-04-01

import pandas as pd
from core.domain.manager import IDatabase
from core.util import ILogger
from core.util.messages import LogMessages

class RDSToPandasUseCase:
    def __init__(self, database: IDatabase, logger: ILogger):
        self.database = database
        self.logger = logger

    def execute(self, ticker: str, table_name: str):
        self.logger.info(LogMessages.RDS_PANDAS_START.format(ticker=ticker))
        
        try:
            filters = {"ticker": ticker}
            records = self.database.query_records(table_name, filters)
            
            if not records:
                self.logger.error(LogMessages.RDS_PANDAS_EMPTY.format(ticker=ticker))
                return None
                
            df = pd.DataFrame(records)

            if 'timestamp_utc' in df.columns:
                df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
                df = df.sort_values(by='timestamp_utc')

            self.logger.info(LogMessages.RDS_PANDAS_OK.format(count=len(df)))
            print(f"\n--- Data for {ticker} ---")
            print(df.head())
            return df
        except Exception as e:
            self.logger.error(LogMessages.RDS_PANDAS_QUERY_FAIL.format(ticker=ticker))
            raise e
