from dependency_injector import containers, providers

from src.bot import handlers
from src.bot.bot import VocabMateBot
from src.bot.user_state_storage import PgSQLUserStateStorage
from src.di.service_container import ServiceContainer


class BotContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    services: ServiceContainer = providers.DependenciesContainer()

    psql_user_state_storage = providers.Factory(
        PgSQLUserStateStorage,
        user_state_service=services.user_state,
    )

    vocab_bot = providers.Factory(
        VocabMateBot,
        token=config.BOT_TOKEN,
        storage=psql_user_state_storage,
        routers=[
            handlers.start.router,
            handlers.card_group.router,
            handlers.end.router
        ],
    )
