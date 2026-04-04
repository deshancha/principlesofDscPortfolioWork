
from dependency_injector import containers, providers
from core.util import LoggerFactory, ILogger
from core.data.manager import AwsS3StorageImp, AwsRdsDatabaseImp
from core.domain.manager import ICloudStorage, IDatabase

from data_collection.data.manager.yahoo_finance_client_imp import YahooFinanceClientImp
from data_collection.domain.manager.imarket_data_client import IMarketDataClient
from data_collection.domain.usecases.collect_market_data_usecase import CollectMarketDataUseCase
from data_collection.domain.usecases.table_cleanup_usecase import TableCleanupUseCase
from data_collection.domain.usecases.fetch_parallel_and_upload_to_s3_usecase import FetchParallelAndUploadToS3UseCase
from data_collection.domain.usecases.s3_to_rds_usecase import S3ToRDSUseCase
from data_collection.domain.usecases.rds_to_pandas_usecase import RDSToPandasUseCase
from data_collection.domain.usecases.data_cleaning_usecase import DataCleaningUseCase

class AppContainer(containers.DeclarativeContainer):
    """
    DI for the app
    """
    config = providers.Configuration()

    logger: providers.Provider[ILogger] = providers.Singleton(
        LoggerFactory.create,
        logger_type="console",  # config.logger_type
        name="App"
    )

    cloud_storage: providers.Provider[ICloudStorage] = providers.Singleton(
        AwsS3StorageImp,
        bucket_name=config.aws.s3_bucket_name,
        logger=logger,
        region_name=config.aws.region_name
    )

    database: providers.Provider[IDatabase] = providers.Singleton(
        AwsRdsDatabaseImp,
        connection_string=config.db.connection_string,
        logger=logger
    )

    # Market Client
    market_client: providers.Provider[IMarketDataClient] = providers.Singleton(
        YahooFinanceClientImp,
        logger=logger
    )

    # Use Cases
    collect_market_data_usecase = providers.Factory(
        CollectMarketDataUseCase,
        market_client=market_client
    )

    table_cleanup_usecase = providers.Factory(
        TableCleanupUseCase,
        database=database,
        logger=logger
    )

    fetch_parallel_and_upload_to_s3_usecase = providers.Factory(
        FetchParallelAndUploadToS3UseCase,
        s3_storage=cloud_storage,
        collect_usecase=collect_market_data_usecase,
        logger=logger,
        bucket_name=config.aws.s3_bucket_name
    )

    s3_to_rds_usecase = providers.Factory(
        S3ToRDSUseCase,
        s3_storage=cloud_storage,
        database=database,
        logger=logger
    )

    rds_to_pandas_usecase = providers.Factory(
        RDSToPandasUseCase,
        database=database,
        logger=logger
    )

    # EDA Use Cases
    data_cleaning_usecase = providers.Factory(
        DataCleaningUseCase,
        logger=logger
    )
