from dependency_injector import containers, providers

from src import config
from src.di.bot_container import BotContainer
from src.di.data_container import DataContainer
from src.di.service_container import ServiceContainer


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    data: DataContainer = providers.Container(DataContainer, config=config)
    services: ServiceContainer = providers.Container(ServiceContainer, data=data)
    bot: BotContainer = providers.Container(BotContainer, config=config, services=services)


di = AppContainer()

di.config.BOT_TOKEN.from_value(config.BOT_TOKEN)
di.config.DB_URL.from_value(config.DB_URL)
