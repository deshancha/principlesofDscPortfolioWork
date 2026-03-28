import os
import sys

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from di import AppContainer
from data_collection.di.container import DataCollectionContainer
from samples.messages import Messages
from samples.validators import validate_env_variables_single

def fetch_and_upload_to_s3():
        
    bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
    if not bucket_name:
        print(Messages.ERR_BUCKET_MISSING)
        sys.exit(1)

    # AppContainer Container DI
    core_container = AppContainer()
    core_container.config.aws.s3_bucket_name.from_env("AWS_S3_BUCKET_NAME", "dummy_bucket")
    core_container.config.aws.region_name.from_env("AWS_REGION_NAME", "us-east-1")
    
    logger = core_container.logger()
    s3_storage = core_container.cloud_storage()
    
    # Data Collection Container DI
    data_container = DataCollectionContainer(core=core_container)
    collect_usecase = data_container.collect_market_data_usecase()
    
    ticker = os.environ.get("YAHOO_FINANCE_TICKER", "")
    start_date = os.environ.get("START_DATE", "")
    end_date = os.environ.get("END_DATE", "")

    if not validate_env_variables_single(ticker, start_date, end_date, logger):
        sys.exit(1)
    
    logger.info(Messages.INFO_YF_ATTEMPT.format(ticker=ticker))
    
    try:
        assets = collect_usecase.fetch_daily(ticker, start_date, end_date)
        if assets:
            logger.info(f"Successfully fetched {len(assets)} records for {ticker}.")
            
            # json serialization
            if hasattr(assets[0], 'model_dump'):
                data_dicts = [asset.model_dump() for asset in assets]
            else:
                data_dicts = [asset.dict() for asset in assets]
                
            # Uplaod Key
            s3_key = f"market_data/{ticker}.json"
            
            logger.info(Messages.INFO_S3_UPLOAD_ATTEMPT.format(bucket_name=bucket_name, test_key=s3_key))
            
            upload_success = s3_storage.upload_raw_json(s3_key, data_dicts)
            if upload_success:
                logger.info(f"Successfully uploaded {ticker} data to S3 at {s3_key}")
            else:
                logger.error(f"Failed to upload {ticker} data to S3.")
                
        else:
            logger.error(Messages.ERR_YF_FAIL)
    except Exception as e:
        logger.error(f"{Messages.ERR_YF_FAIL} Error: {e}")
