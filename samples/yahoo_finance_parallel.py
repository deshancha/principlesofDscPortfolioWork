# Author: Chamika Deshan
# Created: 2026-03-28

import os
import sys
import concurrent.futures

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from di import AppContainer
from data_collection.di.container import DataCollectionContainer
from samples.messages import Messages
from samples.validators import validate_env_variables

def fetch_yahoo_finance_data_parallel():
    """Retrieve Yahoo Finance data for multiple tickers in parallel"""

    # AppContainer DI
    core_container = AppContainer()
    core_container.config.aws.s3_bucket_name.from_env("AWS_S3_BUCKET_NAME", "dummy_bucket")
    core_container.config.aws.region_name.from_env("AWS_REGION_NAME", "us-east-1")
    
    logger = core_container.logger()
    
    # Data Collection Container DI
    data_container = DataCollectionContainer(core=core_container)
    collect_usecase = data_container.collect_market_data_usecase()
    
    # Read config from environment variable
    tickers_env = os.environ.get("YAHOO_FINANCE_TICKERS", "")
    start_date = os.environ.get("START_DATE", "")
    end_date = os.environ.get("END_DATE", "")

    if not validate_env_variables(tickers_env, start_date, end_date, logger):
        sys.exit(1)

    tickers = [t.strip() for t in tickers_env.split(",") if t.strip()]
    
    logger.info(Messages.INFO_YF_PARALLEL_ATTEMPT.format(tickers=tickers_env))
    
    def fetch_for_ticker(ticker):
        try:
            logger.info(Messages.INFO_YF_ATTEMPT.format(ticker=ticker))
            assets = collect_usecase.fetch_daily(ticker, start_date, end_date)
            if assets:
                logger.info(Messages.INFO_YF_PARALLEL_OK.format(count=len(assets), ticker=ticker))
                return (ticker, assets)
            else:
                logger.error(f"[{ticker}] {Messages.ERR_YF_FAIL}")
                return (ticker, [])
        except Exception as e:
            logger.error(f"[{ticker}] {Messages.ERR_YF_FAIL} Error: {e}")
            return (ticker, [])

    # Use ThreadPoolExecutor for parallel execution
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(tickers), 10)) as executor:
        future_to_ticker = {executor.submit(fetch_for_ticker, ticker): ticker for ticker in tickers}
        for future in concurrent.futures.as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                _, assets = future.result()
                results[ticker] = assets
            except Exception as e:
                logger.error(f"[{ticker}] resulted in an exception: {e}")

    # Summary
    logger.info(Messages.INFO_YF_PARALLEL_COMPLETED.format(count=len([k for k, v in results.items() if len(v) > 0])))
    for ticker, assets in results.items():
        if assets:
            logger.info(f"{ticker}: {len(assets)} records")
