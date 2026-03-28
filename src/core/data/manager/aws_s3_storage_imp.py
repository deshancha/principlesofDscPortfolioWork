# Author: Chamika Deshan
# Created: 2026-03-28

import boto3
import json
from core.domain.manager.icloud_storage import ICloudStorage
from core.util.logger import ILogger
from core.util.messages import LogMessages

class AwsS3StorageImp(ICloudStorage):
    """
    AWS S3 imp
    """
    def __init__(self, bucket_name: str, logger: ILogger, region_name: str = "us-east-1"):
        self.bucket_name = bucket_name
        self.logger = logger
        # env -> AWS_ACCESS_KEY_ID would need here
        self.s3_client = boto3.client('s3', region_name=region_name)

    def upload_raw_json(self, path_key: str, json_data: dict) -> bool:
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=path_key,
                Body=json.dumps(json_data),
                ContentType="application/json"
            )
            self.logger.info(LogMessages.S3_UPLOAD_OK.format(path_key=path_key))
            return True
        except Exception as e:
            self.logger.error(LogMessages.S3_UPLOAD_ERROR.format(error=str(e)))
            return False

    def download_raw_json(self, path_key: str) -> dict:
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=path_key
            )
            self.logger.info(LogMessages.S3_DOWNLOAD_OK.format(path_key=path_key))
            return json.loads(response['Body'].read().decode('utf-8'))
        except Exception as e:
            self.logger.error(LogMessages.S3_DOWNLOAD_ERROR.format(error=str(e)))
            return {}
