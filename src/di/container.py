from dependency_injector import containers, providers
from core.util import LoggerFactory, ILogger
from core.data.manager import AwsS3StorageImp, AwsRdsDatabaseImp
from core.domain.manager import ICloudStorage, IDatabase

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
