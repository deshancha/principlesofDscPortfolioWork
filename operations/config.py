# Author: Chamika Deshan
# Created: 2026-04-01

import os
import sys
from dotenv import load_dotenv

# Ensure 'src' is in the python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(BASE_DIR, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from di.container import AppContainer

def get_container() -> AppContainer:
    """
    Returns a fully configured AppContainer.
    Loads .env and wires configuration from environment variables.
    """
    load_dotenv()
    
    container = AppContainer()
    container.config.from_dict({
        "aws": {
            "s3_bucket_name": os.environ.get("AWS_S3_BUCKET_NAME"),
            "region_name": os.environ.get("AWS_REGION_NAME", "us-east-1"),
        },
        "db": {
            "connection_string": os.environ.get("DB_CONNECTION_STRING"),
        },
    })
    return container

# Common constants
TABLE_NAME = os.environ.get("AWS_RDS_TABLE_NAME", "crypto_market_data")
