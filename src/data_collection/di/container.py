from dependency_injector import containers, providers
from data_collection.data.manager.yahoo_finance_client_imp import YahooFinanceClientImp
from data_collection.domain.manager.imarket_data_client import IMarketDataClient
from data_collection.domain.usecases.collect_market_data_usecase import CollectMarketDataUseCase

class DataCollectionContainer(containers.DeclarativeContainer):
    """
    DI for the Data Collection module.
    """
    # The 'core' dependencies container is provided from the root AppContainer
    core = providers.DependenciesContainer()

    market_client: providers.Provider[IMarketDataClient] = providers.Factory(
        YahooFinanceClientImp,
        logger=core.logger
    )

    collect_market_data_usecase: providers.Provider[CollectMarketDataUseCase] = providers.Factory(
        CollectMarketDataUseCase,
        market_client=market_client
    )
