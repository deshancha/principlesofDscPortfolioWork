# Author: Chamika Deshan
# Created: 2026-03-29

import os
import sys
import concurrent.futures

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from di import AppContainer
from samples.messages import Messages

TABLE_NAME = os.environ.get("AWS_RDS_TABLE_NAME", "crypto_market_data")

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

def _app_container() -> AppContainer:
    container = AppContainer()
    container.config.from_dict({
        "aws": {
            "s3_bucket_name": os.environ["AWS_S3_BUCKET_NAME"],
            "region_name": os.environ.get("AWS_REGION_NAME", "us-east-1"),
        },
        "db": {
            "connection_string": os.environ["DB_CONNECTION_STRING"],
        },
    })
    return container


def _process_ticker(ticker: str, s3_storage, database, logger) -> tuple:
    """Get Json Ticker from S3 and add to AWS table"""
    try:
        s3_key = f"market_data/{ticker}.json"
        logger.info(Messages.INFO_S3_RDS_DOWNLOAD_ATTEMPT.format(ticker=ticker, s3_key=s3_key))

        records = s3_storage.download_raw_json(s3_key)
        if not records:
            logger.error(Messages.ERR_S3_RDS_EMPTY.format(ticker=ticker))
            return (ticker, False)

        logger.info(Messages.INFO_S3_RDS_DOWNLOAD_OK.format(ticker=ticker, count=len(records)))

        database.create_table(TABLE_NAME, TABLE_COLUMNS)

        # add the ticker into every record
        for record in records:
            record.setdefault("ticker", ticker)

        # insert records for the current ticker
        success = database.insert_records(TABLE_NAME, records)
        if success:
            logger.info(Messages.INFO_S3_RDS_INSERT_OK.format(ticker=ticker, count=len(records)))
        else:
            logger.error(Messages.ERR_S3_RDS_INSERT_FAIL.format(ticker=ticker))

        return (ticker, success)

    except Exception as e:
        logger.error(f"[{ticker}] S3 -> RDS error: {e}")
        return (ticker, False)


def fetch_from_s3_and_store_in_rds():
    """
    S3 Yfinance Json -> AWS RDS
    """
    tickers_env = os.environ.get("YAHOO_FINANCE_TICKERS", "")
    if not tickers_env:
        print(Messages.ERR_TICKERS_MISSING)
        sys.exit(1)

    tickers = [t.strip() for t in tickers_env.split(",") if t.strip()]

    container = _app_container()
    logger = container.logger()
    s3_storage = container.cloud_storage()
    database = container.database()

    logger.info(Messages.INFO_S3_RDS_START.format(tickers=tickers_env))

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(tickers), 5)) as executor:
        future_to_ticker = {
            executor.submit(_process_ticker, ticker, s3_storage, database, logger): ticker
            for ticker in tickers
        }
        for future in concurrent.futures.as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                _, success = future.result()
                results[ticker] = success
            except Exception as e:
                logger.error(f"[{ticker}] thread error: {e}")
                results[ticker] = False

    # Summary
    succeeded = [t for t, ok in results.items() if ok]
    failed = [t for t, ok in results.items() if not ok]
    logger.info(Messages.INFO_S3_RDS_COMPLETED.format(ok=len(succeeded), fail=len(failed)))
    for ticker, ok in results.items():
        status = "inserted!" if ok else "failed!"
        logger.info(f"  {ticker}: {status}")
