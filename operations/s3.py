# Author: Chamika Deshan
# Created: 2026-03-28

import os
import sys

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from operations.config import get_container
from operations.messages import Messages

def s3_upload_download():
    """Amazon S3 Upload/Download Sample"""
    # AppContainer DI from shared config
    container = get_container()
    bucket_name = container.config.aws.s3_bucket_name()
    
    if not bucket_name:
        print(Messages.ERR_BUCKET_MISSING)
        sys.exit(1)
        
    print(Messages.INFO_S3_BUCKET.format(bucket_name=bucket_name))
    
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
