# Author: Chamika Deshan
# Created: 2026-03-28

class Messages:
    # S3
    ERR_BUCKET_MISSING = "Error: AWS_S3_BUCKET_NAME is missing in .env file"
    INFO_S3_BUCKET = "S3 Bucket: '{bucket_name}'..."
    INFO_S3_UPLOAD_ATTEMPT = "S3 Upload data to Bucket:{bucket_name} -> Key:{test_key}"
    INFO_S3_UPLOAD_OK = "S3 Upload OK"
    INFO_S3_DOWNLOAD_ATTEMPT = "S3 Start Download Bucket:{bucket_name} -> Key:{test_key}"
    INFO_S3_DOWNLOAD_OK = "S3 Download OK -> {data}"
    ERR_S3_DOWNLOAD_FAIL = "S3 Download Failed"
    ERR_S3_UPLOAD_FAIL = "Upload Failed"

    # Yahoo Finance
    INFO_YF_ATTEMPT = "-Fetching YahooFinance data for {ticker}-"
    ERR_YF_FAIL = "Yahoo Finance Data Fetch Failed"

    # Yahoo Finance Parallel
    INFO_YF_PARALLEL_ATTEMPT = "Fetching data parallel for tickers: {tickers}"
    INFO_YF_PARALLEL_OK = "Successfuly fetched {count} records for {ticker}"
    INFO_YF_PARALLEL_COMPLETED = "Parallel Fetch completed. Tickers Count: {count}"
    ERR_END_DATE_MISSING = "Error: END_DATE is missing in .env file"
    ERR_START_DATE_MISSING = "Error: START_DATE is missing in .env file"
    ERR_TICKER_MISSING = "Error: Ticker is missing in .env file"
    ERR_TICKERS_MISSING = "Error: YAHOO_FINANCE_TICKERS is missing in .env file"

    # S3 → RDS
    INFO_S3_RDS_START = "Starting S3 → RDS pipeline for tickers: {tickers}"
    INFO_S3_RDS_DOWNLOAD_ATTEMPT = "[{ticker}] Downloading s3://market_data/{s3_key}"
    INFO_S3_RDS_DOWNLOAD_OK = "[{ticker}] Downloaded {count} records from S3"
    INFO_S3_RDS_INSERT_OK = "[{ticker}] Inserted {count} records into RDS"
    INFO_S3_RDS_COMPLETED = "S3 → RDS pipeline complete. OK: {ok}, Failed: {fail}"
    ERR_S3_RDS_EMPTY = "[{ticker}] No data found in S3, skipping"
    ERR_S3_RDS_INSERT_FAIL = "[{ticker}] RDS insert failed"

    # RDS → Pandas
    INFO_RDS_PANDAS_START = "Starting RDS → Pandas retrieval for ticker: {ticker}"
    INFO_RDS_PANDAS_OK = "Successfully loaded {count} records into Pandas DataFrame"
    ERR_RDS_PANDAS_QUERY_FAIL = "RDS query failed for ticker: {ticker}"
    ERR_RDS_PANDAS_EMPTY = "No data found in RDS for ticker: {ticker}"
