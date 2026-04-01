# Author: Chamika Deshan
# Created: 2026-03-28

class LogMessages:
   
    # S3 Msgs
    S3_UPLOAD_OK = "AWS S3 Upload OK: {path_key}"
    S3_UPLOAD_ERROR = "AWS S3 Upload Error: {error}"
    S3_DOWNLOAD_OK = "AWS S3 Download OK: {path_key}"
    S3_DOWNLOAD_ERROR = "AWS S3 Download Error: {error}"

    # RDS Msgs
    RDS_CREATE_TABLE_OK = "AWS RDS Create Table OK: {table_name}"
    RDS_CREATE_TABLE_ERROR = "AWS RDS Create Table Error: {error}"
    RDS_TABLE_EXISTS_ERROR = "AWS RDS Table Exists Check Error: {error}"
    RDS_INSERT_OK = "AWS RDS Insert OK: {table_name}"
    RDS_INSERT_ERROR = "AWS RDS Insert Error: {error}"
    RDS_QUERY_ERROR = "AWS RDS Query Error: {error}"