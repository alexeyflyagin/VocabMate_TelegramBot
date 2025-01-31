from dependency_injector import containers, providers

from src.data.session_manager import SessionManager


class DataContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    session_manager = providers.Singleton(
        SessionManager,
        db_url=config.DB_URL
    )
