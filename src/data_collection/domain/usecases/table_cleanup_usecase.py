# Author: Chamika Deshan
# Created: 2026-04-01

from sqlalchemy import text
from core.domain.manager import IDatabase
from core.util import ILogger
from core.util.messages import LogMessages

class TableCleanupUseCase:
    def __init__(self, database: IDatabase, logger: ILogger):
        self.database = database
        self.logger = logger

    def execute(self, table_name: str):
        self.logger.info(LogMessages.RDS_CLEANUP_START.format(table_name=table_name))
        
        try:
            engine, _ = self.database._make_engine()
            with engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
                conn.commit()
            
            self.logger.info(LogMessages.RDS_CLEANUP_OK.format(table_name=table_name))
        except Exception as e:
            self.logger.error(LogMessages.RDS_CREATE_TABLE_ERROR.format(error=str(e)))
            raise e
