import os
import sys

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
from di.container import AppContainer
from agent.trading_agent import TradingAgent

def _app_container() -> AppContainer:
    load_dotenv()
    container = AppContainer()
    container.config.from_dict({
        "aws": {
            "s3_bucket_name": os.environ["AWS_S3_BUCKET_NAME"],
            "region_name": os.environ.get("AWS_REGION_NAME", "us-east-1"),
        },
        "db": {
            "connection_string": os.environ["DB_CONNECTION_STRING"],
        },
    })
    return container

def main():
    container = _app_container()
    table_name = os.environ.get("AWS_RDS_TABLE_NAME", "crypto_market_data")
    tickers_env = os.environ.get("YAHOO_FINANCE_TICKERS", "")
    start_date = os.environ.get("START_DATE", "")
    end_date = os.environ.get("END_DATE", "")

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        # -1: Dump RDS table
        if arg == "-1":
            usecase = container.table_cleanup_usecase()
            usecase.execute(table_name)
            return
            
        # 1: Fetch from YF and upload to S3
        elif arg == "1":
            usecase = container.fetch_parallel_and_upload_to_s3_usecase()
            usecase.execute(tickers_env, start_date, end_date)
            return
            
        # 2: Fetch from S3 and upload to RDS
        elif arg == "2":
            usecase = container.s3_to_rds_usecase()
            usecase.execute([t.strip() for t in tickers_env.split(",") if t.strip()], table_name)
            return
            
        # 3: Fetch from RDS and load to Pandas
        elif arg == "3":
            usecase = container.rds_to_pandas_usecase()
            usecase.execute(ticker="BTC-USD", table_name=table_name)
            return

        # 4: Trading Agent
        elif arg == "4":
            agent = TradingAgent(init_bal=1000)
            
            test_tickers = ["BTC-USD", "DOGE-USD", "SOL-USD", "ETH-USD", "BNB-USD"]
            for coin in test_tickers:
                try:
                    agent.analyze_and_trade(coin)
                except Exception as e:
                    print(f"Error : {coin}: {e}")
            return

if __name__ == "__main__":
    main()
