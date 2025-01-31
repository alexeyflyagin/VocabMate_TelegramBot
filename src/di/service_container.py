from dependency_injector import containers, providers

from src.di.data_container import DataContainer
from src.services.user_state import UserStateService


class ServiceContainer(containers.DeclarativeContainer):
    data: DataContainer = providers.DependenciesContainer()

    user_state_service = providers.Factory(
        UserStateService,
        session_manager=data.session_manager,
    )
