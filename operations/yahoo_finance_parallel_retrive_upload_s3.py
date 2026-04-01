# Author: Chamika Deshan
# Created: 2026-03-28

import os
import sys
import concurrent.futures

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from operations.config import get_container
from operations.messages import Messages
from operations.validators import validate_env_variables


def fetch_parallel_and_upload_to_s3():
    """Fetch Yahoo Finance data for multiple tickers in parallel and upload each to S3"""

    # AppContainer DI from shared config
    core_container = get_container()
    bucket_name = core_container.config.aws.s3_bucket_name()
    
    if not bucket_name:
        print(Messages.ERR_BUCKET_MISSING)
        sys.exit(1)

    logger = core_container.logger()
    s3_storage = core_container.cloud_storage()
    
    # Data Collection Container DI
    from data_collection.di.container import DataCollectionContainer
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

    def fetch_and_upload(ticker):
        try:
            logger.info(Messages.INFO_YF_ATTEMPT.format(ticker=ticker))
            assets = collect_usecase.fetch_daily(ticker, start_date, end_date)

            if not assets:
                logger.error(f"[{ticker}] {Messages.ERR_YF_FAIL}")
                return (ticker, False)

            logger.info(Messages.INFO_YF_PARALLEL_OK.format(count=len(assets), ticker=ticker))

            # Serialize to JSON-compatible dicts
            if hasattr(assets[0], 'model_dump'):
                data_dicts = [asset.model_dump() for asset in assets]
            else:
                data_dicts = [asset.dict() for asset in assets]

            # Upload to S3 with ticker name
            s3_key = f"market_data/{ticker}.json"
            logger.info(Messages.INFO_S3_UPLOAD_ATTEMPT.format(bucket_name=bucket_name, test_key=s3_key))
            upload_success = s3_storage.upload_raw_json(s3_key, data_dicts)

            if upload_success:
                logger.info(f"[{ticker}] Uploaded to S3 at {s3_key}")
                return (ticker, True)
            else:
                logger.error(f"[{ticker}] {Messages.ERR_S3_UPLOAD_FAIL}")
                return (ticker, False)

        except Exception as e:
            logger.error(f"[{ticker}] Error: {e}")
            return (ticker, False)

    # Goes Parallel
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(tickers), 10)) as executor:
        future_to_ticker = {executor.submit(fetch_and_upload, ticker): ticker for ticker in tickers}
        for future in concurrent.futures.as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                _, success = future.result()
                results[ticker] = success
            except Exception as e:
                logger.error(f"[{ticker}] resulted in an exception: {e}")
                results[ticker] = False

    # Summary
    succeeded = [t for t, ok in results.items() if ok]
    logger.info(Messages.INFO_YF_PARALLEL_COMPLETED.format(count=len(succeeded)))
    for ticker, ok in results.items():
        status = "uploaded!" if ok else "failed!"
        logger.info(f"  {ticker}: {status}")
