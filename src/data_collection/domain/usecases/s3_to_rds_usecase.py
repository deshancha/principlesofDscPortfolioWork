# Author: Chamika Deshan
# Created: 2026-04-01

import concurrent.futures
from typing import List
from core.domain.manager import ICloudStorage, IDatabase
from core.util import ILogger
from core.util.messages import LogMessages

# AssetData -> TABLE_NAME Columns
TABLE_COLUMNS = {
    "ticker":        "VARCHAR(20)",
    "timestamp_utc": "VARCHAR(30)",
    "open_price":    "FLOAT",
    "high_price":    "FLOAT",
    "low_price":    "FLOAT",
    "close_price":   "FLOAT",
    "volume":        "BIGINT",
    "source":        "VARCHAR(50)",
}

class S3ToRDSUseCase:
    def __init__(self, s3_storage: ICloudStorage, database: IDatabase, logger: ILogger):
        self.s3_storage = s3_storage
        self.database = database
        self.logger = logger

    def execute(self, tickers: List[str], table_name: str):
        self.logger.info(LogMessages.S3_RDS_START.format(tickers=",".join(tickers)))

        # Create table once before starting threads
        self.database.create_table(table_name, TABLE_COLUMNS)

        def process_ticker(ticker):
            try:
                s3_key = f"market_data/{ticker}.json"
                self.logger.info(LogMessages.S3_RDS_DOWNLOAD_ATTEMPT.format(ticker=ticker, s3_key=s3_key))

                records = self.s3_storage.download_raw_json(s3_key)
                if not records:
                    self.logger.error(LogMessages.S3_RDS_EMPTY.format(ticker=ticker))
                    return (ticker, False)

                self.logger.info(LogMessages.S3_RDS_DOWNLOAD_OK.format(ticker=ticker, count=len(records)))

                for record in records:
                    record.setdefault("ticker", ticker)

                success = self.database.insert_records(table_name, records)
                if success:
                    self.logger.info(LogMessages.S3_RDS_INSERT_OK.format(ticker=ticker, count=len(records)))
                else:
                    self.logger.error(LogMessages.S3_RDS_INSERT_FAIL.format(ticker=ticker))

                return (ticker, success)

            except Exception as e:
                self.logger.error(f"[{ticker}] S3 -> RDS error: {e}")
                return (ticker, False)

        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(tickers), 5)) as executor:
            future_to_ticker = {executor.submit(process_ticker, ticker): ticker for ticker in tickers}
            for future in concurrent.futures.as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    _, success = future.result()
                    results[ticker] = success
                except Exception as e:
                    self.logger.error(f"[{ticker}] thread error: {e}")
                    results[ticker] = False

        succeeded = [t for t, ok in results.items() if ok]
        failed = [t for t, ok in results.items() if not ok]
        self.logger.info(LogMessages.S3_RDS_COMPLETED.format(ok=len(succeeded), fail=len(failed)))
