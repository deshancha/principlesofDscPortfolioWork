# Author: Chamika Deshan
# Created: 2026-03-28

class LogMessages:
    # S3 Msgs
    S3_BUCKET = "S3 Bucket: '{bucket_name}'..."
    S3_UPLOAD_ATTEMPT = "S3 Upload data to Bucket:{bucket_name} -> Key:{path_key}"
    S3_UPLOAD_OK = "AWS S3 Upload OK: {path_key}"
    S3_UPLOAD_ERROR = "AWS S3 Upload Error: {error}"
    S3_DOWNLOAD_ATTEMPT = "S3 Start Download Bucket:{bucket_name} -> Key:{path_key}"
    S3_DOWNLOAD_OK = "AWS S3 Download OK: {path_key}"
    S3_DOWNLOAD_ERROR = "AWS S3 Download Error: {error}"

    # RDS Msgs
    RDS_CREATE_TABLE_OK = "AWS RDS Create Table OK: {table_name}"
    RDS_CREATE_TABLE_ERROR = "AWS RDS Create Table Error: {error}"
    RDS_TABLE_EXISTS_ERROR = "AWS RDS Table Exists Check Error: {error}"
    RDS_INSERT_OK = "AWS RDS Insert OK: {table_name}"
    RDS_INSERT_ERROR = "AWS RDS Insert Error: {error}"
    RDS_QUERY_ERROR = "AWS RDS Query Error: {error}"
    RDS_CLEANUP_START = "Starting RDS cleanup for table: {table_name}"
    RDS_CLEANUP_OK = "RDS cleanup completed for table: {table_name}"

    # Yahoo Finance
    YF_ATTEMPT = "-Fetching YahooFinance data for {ticker}-"
    YF_FAIL = "Yahoo Finance Data Fetch Failed"
    
    # Yahoo Finance Parallel
    YF_PARALLEL_ATTEMPT = "Fetching data parallel for tickers: {tickers}"
    YF_PARALLEL_OK = "Successfuly fetched {count} records for {ticker}"
    YF_PARALLEL_COMPLETED = "Parallel Fetch completed. Tickers Count: {count}"

    # S3 -> RDS Pipeline
    S3_RDS_START = "Starting S3 -> RDS pipeline for tickers: {tickers}"
    S3_RDS_DOWNLOAD_ATTEMPT = "[{ticker}] Downloading s3://market_data/{s3_key}"
    S3_RDS_DOWNLOAD_OK = "[{ticker}] Downloaded {count} records from S3"
    S3_RDS_INSERT_OK = "[{ticker}] Inserted {count} records into RDS"
    S3_RDS_COMPLETED = "S3 -> RDS pipeline complete. OK: {ok}, Failed: {fail}"
    S3_RDS_EMPTY = "[{ticker}] No data found in S3, skipping"
    S3_RDS_INSERT_FAIL = "[{ticker}] RDS insert failed"

    # RDS -> Pandas
    RDS_PANDAS_START = "Starting RDS -> Pandas retrieval for ticker: {ticker}"
    RDS_PANDAS_OK = "Successfully loaded {count} records into Pandas DataFrame"
    RDS_PANDAS_QUERY_FAIL = "RDS query failed for ticker: {ticker}"
    RDS_PANDAS_EMPTY = "No data found in RDS for ticker: {ticker}"

    # Validation Errors
    ERR_BUCKET_MISSING = "Error: AWS_S3_BUCKET_NAME is missing in .env file"
    ERR_END_DATE_MISSING = "Error: END_DATE is missing in .env file"
    ERR_START_DATE_MISSING = "Error: START_DATE is missing in .env file"
    ERR_TICKER_MISSING = "Error: Ticker is missing in .env file"
    ERR_TICKERS_MISSING = "Error: YAHOO_FINANCE_TICKERS is missing in .env file"