# Author: Chamika Deshan
# Created: 2026-03-28

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IDatabase(ABC):
    """
    RDS SQL operations
    """

    @abstractmethod
    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        pass

    @abstractmethod
    def table_exists(self, table_name: str) -> bool:
        pass            

    @abstractmethod
    def insert_records(self, table_name: str, records: List[Dict[str, Any]]) -> bool:
        pass

    @abstractmethod
    def query_records(self, table_name: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        pass
