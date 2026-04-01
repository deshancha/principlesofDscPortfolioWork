# Author: Chamika Deshan
# Created: 2026-03-28

import os
import sys

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from operations.config import get_container
from operations.messages import Messages
from operations.validators import validate_env_variables_single

def fetch_yahoo_finance_data():
    """Retrieve Yahoo Finance data"""

    # AppContainer DI from shared config
    core_container = get_container()
    logger = core_container.logger()
    
    # Data Collection Container DI
    from data_collection.di.container import DataCollectionContainer
    data_container = DataCollectionContainer(core=core_container)
    collect_usecase = data_container.collect_market_data_usecase()
    
    # Read config from environment variable
    ticker = os.environ.get("YAHOO_FINANCE_TICKER", "")
    start_date = os.environ.get("START_DATE", "")
    end_date = os.environ.get("END_DATE", "")

    if not validate_env_variables_single(ticker, start_date, end_date, logger):
        sys.exit(1)
    
    logger.info(Messages.INFO_YF_ATTEMPT.format(ticker=ticker))
    
    try:
        assets = collect_usecase.fetch_daily(ticker, start_date, end_date)
        if assets:
            # Display first 5 rows
            for index, asset in enumerate(assets[:5], start=1):
                logger.info(f"{index}. Date: {asset.timestamp_utc} | Open: {asset.open_price:.2f} | Close: {asset.close_price:.2f} | Volume: {asset.volume}")
        else:
            logger.error(Messages.ERR_YF_FAIL)
    except Exception as e:
        logger.error(f"{Messages.ERR_YF_FAIL} Error: {e}")
