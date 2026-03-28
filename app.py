import os
import sys
import logging

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
from di import AppContainer

class Messages:
    ERR_BUCKET_MISSING = "Error: AWS_S3_BUCKET_NAME is missing in .env file"
    INFO_S3_BUCKET = "S3 Bucket: '{bucket_name}'..."
    INFO_S3_UPLOAD_ATTEMPT = "S3 Upload data to Bucket:{bucket_name} -> Key:{test_key}"
    INFO_S3_UPLOAD_OK = "S3 Upload OK"
    INFO_S3_DOWNLOAD_ATTEMPT = "S3 Start Download Bucket:{bucket_name} -> Key:{test_key}"
    INFO_S3_DOWNLOAD_OK = "S3 Download OK -> {data}"
    ERR_S3_DOWNLOAD_FAIL = "S3 Download Failed"
    ERR_S3_UPLOAD_FAIL = "Upload Failed"


def main():
    load_dotenv()
    
    bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
    if not bucket_name:
        print(Messages.ERR_BUCKET_MISSING)
        sys.exit(1)
        
    print(Messages.INFO_S3_BUCKET.format(bucket_name=bucket_name))
    
    container = AppContainer()
    container.config.aws.s3_bucket_name.from_env("AWS_S3_BUCKET_NAME")
    container.config.aws.region_name.from_env("AWS_REGION_NAME", "us-east-1")
    container.config.db.connection_string.from_value("sqlite:///:memory:") # dummy db string just to bypass any validation
    
    # allows use @Inject without supply manually
    container.wire(modules=[__name__])
    
    s3_storage = container.cloud_storage()
    logger = container.logger()
    
    # S3 upload
    test_key = "test_uploads/sample.json"
    test_data = {
        "event": "s3_upload",
        "description": "Test S3 Upload"
    }
    
    logger.info(Messages.INFO_S3_UPLOAD_ATTEMPT.format(bucket_name=bucket_name, test_key=test_key))
    upload_success = s3_storage.upload_raw_json(test_key, test_data)
    
    if upload_success:
        logger.info(Messages.INFO_S3_UPLOAD_OK)
        
        # S3 Download
        logger.info(Messages.INFO_S3_DOWNLOAD_ATTEMPT.format(bucket_name=bucket_name, test_key=test_key))
        downloaded_data = s3_storage.download_raw_json(test_key)
        
        if downloaded_data:
            logger.info(Messages.INFO_S3_DOWNLOAD_OK.format(data=downloaded_data))
        else:
            logger.error(Messages.ERR_S3_DOWNLOAD_FAIL)
    else:
        logger.error(Messages.ERR_S3_UPLOAD_FAIL)


if __name__ == "__main__":
    main()
