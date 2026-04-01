# Author: Chamika Deshan
# Created: 2026-03-28

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, Date, inspect
from sqlalchemy.pool import NullPool
from core.domain.manager.idatabase import IDatabase
from typing import List, Dict, Any, Optional
from core.util.logger import ILogger
from core.util.messages import LogMessages


_TYPE_MAP = {
    "INT": Integer,
    "INTEGER": Integer,
    "FLOAT": Float,
    "DATE": Date,
}

def _resolve_type(type_str: str):
    upper = type_str.upper().strip()
    if upper in _TYPE_MAP:
        return _TYPE_MAP[upper]()
    if upper.startswith("VARCHAR"):
        try:
            length = int(upper.replace("VARCHAR", "").strip("()"))
        except ValueError:
            length = 255
        return String(length)
    return String(255)


class AwsRdsDatabaseImp(IDatabase):
    """
    AWS RDS implementation with connection string, TODO: Token
    """

    def __init__(self, connection_string: str, logger: ILogger):
        self.connection_string = connection_string
        self.logger = logger

    def _make_engine(self):
        engine = create_engine(self.connection_string, poolclass=NullPool)
        return engine, MetaData()

    def table_exists(self, table_name: str) -> bool:
        try:
            engine, _ = self._make_engine()
            return table_name in inspect(engine).get_table_names()
        except Exception as e:
            self.logger.error(LogMessages.RDS_TABLE_EXISTS_ERROR.format(error=str(e)))
            return False

    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        try:
            engine, metadata = self._make_engine()
            if table_name in inspect(engine).get_table_names():
                return True
            cols = [Column("id", Integer, primary_key=True, autoincrement=True)]
            for col_name, col_type in columns.items():
                cols.append(Column(col_name, _resolve_type(col_type)))
            Table(table_name, metadata, *cols)
            metadata.create_all(engine)
            self.logger.info(LogMessages.RDS_CREATE_TABLE_OK.format(table_name=table_name))
            return True
        except Exception as e:
            self.logger.error(LogMessages.RDS_CREATE_TABLE_ERROR.format(error=str(e)))
            return False

    def insert_records(self, table_name: str, records: List[Dict[str, Any]]) -> bool:
        try:
            if not records:
                return True
            engine, metadata = self._make_engine()
            table = Table(table_name, metadata, autoload_with=engine)
            with engine.begin() as conn:
                conn.execute(table.insert(), records)
            self.logger.info(LogMessages.RDS_INSERT_OK.format(table_name=table_name))
            return True
        except Exception as e:
            self.logger.error(LogMessages.RDS_INSERT_ERROR.format(error=str(e)))
            return False

    def query_records(self, table_name: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        try:
            engine, metadata = self._make_engine()
            table = Table(table_name, metadata, autoload_with=engine)
            with engine.connect() as conn:
                query = table.select()
                if filters:
                    for col, val in filters.items():
                        query = query.where(table.c[col] == val)
                result = conn.execute(query)
                return [dict(row._mapping) for row in result]
        except Exception as e:
            self.logger.error(LogMessages.RDS_QUERY_ERROR.format(error=str(e)))
            return []
