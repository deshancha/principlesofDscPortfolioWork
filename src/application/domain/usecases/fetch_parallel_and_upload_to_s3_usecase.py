# Author: Chamika Deshan
# Created: 2026-04-01

import concurrent.futures
from typing import List
from core.domain.manager import ICloudStorage
from core.util import ILogger
from core.util.messages import LogMessages
from core.util.validators import validate_env_variables
from data_collection.domain.usecases.collect_market_data_usecase import CollectMarketDataUseCase

class FetchParallelAndUploadToS3UseCase:
    def __init__(
        self, 
        s3_storage: ICloudStorage, 
        collect_usecase: CollectMarketDataUseCase,
        logger: ILogger,
        bucket_name: str
    ):
        self.s3_storage = s3_storage
        self.collect_usecase = collect_usecase
        self.logger = logger
        self.bucket_name = bucket_name

    def execute(self, tickers_env: str, start_date: str, end_date: str):
        if not validate_env_variables(tickers_env, start_date, end_date, self.logger):
            return

        tickers = [t.strip() for t in tickers_env.split(",") if t.strip()]
        self.logger.info(LogMessages.YF_PARALLEL_ATTEMPT.format(tickers=tickers_env))

        def fetch_and_upload(ticker):
            try:
                self.logger.info(LogMessages.YF_ATTEMPT.format(ticker=ticker))
                assets = self.collect_usecase.fetch_daily(ticker, start_date, end_date)

                if not assets:
                    self.logger.error(f"[{ticker}] {LogMessages.YF_FAIL}")
                    return (ticker, False)

                self.logger.info(LogMessages.YF_PARALLEL_OK.format(count=len(assets), ticker=ticker))

                # Serialize to JSON-compatible dicts
                if hasattr(assets[0], 'model_dump'):
                    data_dicts = [asset.model_dump() for asset in assets]
                else:
                    data_dicts = [asset.dict() for asset in assets]

                s3_key = f"market_data/{ticker}.json"
                self.logger.info(LogMessages.S3_UPLOAD_ATTEMPT.format(bucket_name=self.bucket_name, path_key=s3_key))
                upload_success = self.s3_storage.upload_raw_json(s3_key, data_dicts)

                if upload_success:
                    self.logger.info(f"[{ticker}] Uploaded to S3 at {s3_key}")
                    return (ticker, True)
                else:
                    self.logger.error(f"[{ticker}] S3 Upload Failed")
                    return (ticker, False)

            except Exception as e:
                self.logger.error(f"[{ticker}] Error: {e}")
                return (ticker, False)

        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(tickers), 10)) as executor:
            future_to_ticker = {executor.submit(fetch_and_upload, ticker): ticker for ticker in tickers}
            for future in concurrent.futures.as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    _, success = future.result()
                    results[ticker] = success
                except Exception as e:
                    self.logger.error(f"[{ticker}] resulted in an exception: {e}")
                    results[ticker] = False

        succeeded = [t for t, ok in results.items() if ok]
        self.logger.info(LogMessages.YF_PARALLEL_COMPLETED.format(count=len(succeeded)))
        for ticker, ok in results.items():
            status = "uploaded!" if ok else "failed!"
            self.logger.info(f"  {ticker}: {status}")
