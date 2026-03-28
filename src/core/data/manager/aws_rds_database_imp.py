# Author: Chamika Deshan
# Created: 2026-03-28

from sqlalchemy import create_engine, MetaData, Table
from core.domain.manager.idatabase import IDatabase
from typing import List, Dict, Any
from core.util.logger import ILogger
from core.util.messages import LogMessages

class AwsRdsDatabaseImp(IDatabase):
    """
    AWS RDS imp
    """
    def __init__(self, connection_string: str, logger: ILogger):
        self.engine = create_engine(connection_string)
        self.metadata = MetaData()
        self.logger = logger

    def insert_records(self, table_name: str, records: List[Dict[str, Any]]) -> bool:
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            with self.engine.begin() as conn:
                conn.execute(table.insert(), records)
            return True
        except Exception as e:
            self.logger.error(LogMessages.RDS_INSERT_ERROR.format(error=str(e)))
            return False
