from dependency_injector import containers, providers

from src import config
from src.bot import handlers
from src.di.bot_container import BotContainer
from src.di.data_container import DataContainer
from src.di.service_container import ServiceContainer


def inject():
    handlers.utils.TRUSTED_USER_ID = di.config.TRUSTED_USER_ID()

    handlers.card_group.card_group_service = di.services.card_group()


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    data: DataContainer = providers.Container(DataContainer, config=config)
    services: ServiceContainer = providers.Container(ServiceContainer, data=data)
    bot: BotContainer = providers.Container(BotContainer, config=config, services=services)


di = AppContainer()

di.config.BOT_TOKEN.from_value(config.BOT_TOKEN)
di.config.TRUSTED_USER_ID.from_value(config.TRUSTED_USER_ID)
di.config.DB_URL.from_value(config.DB_URL)

inject()
