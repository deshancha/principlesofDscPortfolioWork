from abc import ABC, abstractmethod

class ICloudStorage(ABC):
    """
    Cloud upload/download
    """
    
    @abstractmethod
    def upload_raw_json(self, path_key: str, json_data: dict) -> bool:
        pass

    @abstractmethod
    def download_raw_json(self, path_key: str) -> dict:
        pass
