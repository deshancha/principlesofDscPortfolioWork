# Author: Chamika Deshan
# Created: 2026-03-28

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IDatabase(ABC):
    """
    For SQL Database
    """

    @abstractmethod
    def insert_records(self, table_name: str, records: List[Dict[str, Any]]) -> bool:
        """
        Inserts dictionary to a table
        Retrn the status
        """
        pass
