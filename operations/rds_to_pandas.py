# Author: Chamika Deshan
# Created: 2026-03-29

import os
import sys
import pandas as pd

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from operations.config import get_container, TABLE_NAME
from operations.messages import Messages

def fetch_from_rds_to_pandas(ticker: str = "BTC-USD"):
    """
    AWS RDS -> Pandas
    """
    container = get_container()
    logger = container.logger()
    database = container.database()

    logger.info(Messages.INFO_RDS_PANDAS_START.format(ticker=ticker))

    try:
        # query records of ticker
        filters = {"ticker": ticker}
        records = database.query_records(TABLE_NAME, filters)

        if not records:
            logger.error(Messages.ERR_RDS_PANDAS_EMPTY.format(ticker=ticker))
            return None

        df = pd.DataFrame(records)

        # sort and cleanup
        if 'timestamp_utc' in df.columns:
            df['timestamp_utc'] = pd.to_datetime(df['timestamp_utc'])
            df = df.sort_values(by='timestamp_utc')

        logger.info(Messages.INFO_RDS_PANDAS_OK.format(count=len(df)))

        logger.info(f"\n--- Ticker {ticker} ---")
        logger.info(df.head(10).to_string(index=False))
        logger.info(f"\nShape: {df.shape}")
        
        return df

    except Exception as e:
        logger.error(f"[{ticker}] RDS -> Pandas error: {e}")
        return None
