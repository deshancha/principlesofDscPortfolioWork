# Author: Chamika Deshan
# Created: 2026-03-28

from samples.messages import Messages

def validate_env_variables(tickers_env, start_date, end_date, logger) -> bool:
    # if tickers_env is empty, exit
    if not tickers_env:
        logger.error(Messages.ERR_TICKERS_MISSING)
        return False

    # if start_date is empty, exit
    if not start_date:
        logger.error(Messages.ERR_START_DATE_MISSING)
        return False

    # if end_date is empty, exit
    if not end_date:
        logger.error(Messages.ERR_END_DATE_MISSING)
        return False
    
    return True

def validate_env_variables_single(ticker_env, start_date, end_date, logger) -> bool:
    if not ticker_env:
        logger.error(Messages.ERR_TICKERS_MISSING)
        return False

    # if start_date is empty, exit
    if not start_date:
        logger.error(Messages.ERR_START_DATE_MISSING)
        return False

    # if end_date is empty, exit
    if not end_date:
        logger.error(Messages.ERR_END_DATE_MISSING)
        return False
    
    return True
