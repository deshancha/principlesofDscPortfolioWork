# Author: Chamika Deshan
# Created: 2026-04-01

from core.util.messages import LogMessages

def validate_env_variables(tickers_env: str, start_date: str, end_date: str, logger) -> bool:
    if not tickers_env:
        logger.error(LogMessages.ERR_TICKERS_MISSING)
        return False

    if not start_date:
        logger.error(LogMessages.ERR_START_DATE_MISSING)
        return False

    if not end_date:
        logger.error(LogMessages.ERR_END_DATE_MISSING)
        return False
    
    return True

def validate_env_variables_single(ticker: str, start_date: str, end_date: str, logger) -> bool:
    if not ticker:
        logger.error(LogMessages.ERR_TICKER_MISSING)
        return False

    if not start_date:
        logger.error(LogMessages.ERR_START_DATE_MISSING)
        return False

    if not end_date:
        logger.error(LogMessages.ERR_END_DATE_MISSING)
        return False
    
    return True
