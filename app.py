import os
import sys

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
from di.container import AppContainer
from operations import s3_upload_download, fetch_yahoo_finance_data, fetch_yahoo_finance_data_parallel, fetch_and_upload_to_s3, fetch_parallel_and_upload_to_s3, fetch_from_s3_and_store_in_rds, fetch_from_rds_to_pandas, cleanup

def main():
    # Check for command-line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        # Dump RDS table
        if arg == "-1":
            cleanup()
            return
        # Fetch from Yfinance and upload to S3
        elif arg == "1":
            fetch_parallel_and_upload_to_s3()
            return
        # Fetch from S3 and upload to RDS
        elif arg == "2":
            fetch_from_s3_and_store_in_rds()
            return
        # Fetch from RDS and load to Pandas
        elif arg == "3":
            fetch_from_rds_to_pandas(ticker="BTC-USD")
            return

if __name__ == "__main__":
    main()
