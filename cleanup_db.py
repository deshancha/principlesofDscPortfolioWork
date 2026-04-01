# Author: Chamika Deshan
# Created: 2026-03-29

import os
import sys
from sqlalchemy import text

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
from di.container import AppContainer

def cleanup():
    load_dotenv()
    container = AppContainer()
    container.config.from_dict({
        "db": {
            "connection_string": os.environ["DB_CONNECTION_STRING"],
        },
    })
    
    db = container.database()
    engine, _ = db._make_engine()
    
    table_name = "crypto_market_data"
    
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE;"))
        conn.commit()
    
    print("Table dropped!")

if __name__ == "__main__":
    cleanup()
