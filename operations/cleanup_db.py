# Author: Chamika Deshan
# Created: 2026-03-29

import os
import sys
from sqlalchemy import text

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
from operations.config import get_container, TABLE_NAME
from operations.messages import Messages

def cleanup():
    container = get_container()
    logger = container.logger()
    db = container.database()
    engine, _ = db._make_engine()
    
    logger.info(Messages.INFO_RDS_CLEANUP_START.format(table_name=TABLE_NAME))
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {TABLE_NAME} CASCADE;"))
        conn.commit()
    
    logger.info(Messages.INFO_RDS_CLEANUP_OK.format(table_name=TABLE_NAME))
    print("Table dropped!")