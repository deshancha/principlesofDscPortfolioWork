import os
import sys

# import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
from samples import s3_upload_download, fetch_yahoo_finance_data, fetch_yahoo_finance_data_parallel, fetch_and_upload_to_s3

def main():
    load_dotenv()
    
    # Run S3 test
    # s3_upload_download()
    
    # Run Yahoo Finance test
    # fetch_yahoo_finance_data()
    
    # Run Yahoo Finance parallel test
    # fetch_yahoo_finance_data_parallel()
    
    # Run fetch and upload to S3 test
    fetch_and_upload_to_s3()

if __name__ == "__main__":
    main()
