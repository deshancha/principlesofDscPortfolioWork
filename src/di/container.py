from dependency_injector import containers, providers
from core.util import LoggerFactory, ILogger
from core.data.manager import AwsS3StorageImp, AwsRdsDatabaseImp
from core.domain.manager import ICloudStorage, IDatabase
from application.domain.usecases.table_cleanup_usecase import TableCleanupUseCase
from application.domain.usecases.fetch_parallel_and_upload_to_s3_usecase import FetchParallelAndUploadToS3UseCase
from application.domain.usecases.s3_to_rds_usecase import S3ToRDSUseCase
from application.domain.usecases.rds_to_pandas_usecase import RDSToPandasUseCase
from data_collection.di.container import DataCollectionContainer

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

    # Data Collection Sub-container
    data_collection = providers.Container(
        DataCollectionContainer,
        core=providers.DependenciesContainer(
            logger=logger
        )
    )

    # Core Use Cases
    table_cleanup_usecase = providers.Factory(
        TableCleanupUseCase,
        database=database,
        logger=logger
    )

    fetch_parallel_and_upload_to_s3_usecase = providers.Factory(
        FetchParallelAndUploadToS3UseCase,
        s3_storage=cloud_storage,
        collect_usecase=data_collection.collect_market_data_usecase,
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
