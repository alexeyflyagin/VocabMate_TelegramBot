from dependency_injector import containers, providers

from src.di.data_container import DataContainer
from src.services.impl.card_group import CardGroupService
from src.services.impl.card_item import CardItemService
from src.services.impl.training import TrainingService
from src.services.user_state import UserStateService


class ServiceContainer(containers.DeclarativeContainer):
    data: DataContainer = providers.DependenciesContainer()

    user_state = providers.Factory(
        UserStateService,
        session_manager=data.session_manager,
    )

    card_group = providers.Factory(
        CardGroupService,
        session_manager=data.session_manager,
    )

    card_item = providers.Factory(
        CardItemService,
        session_manager=data.session_manager,
    )

    training = providers.Factory(
        TrainingService,
        session_manager=data.session_manager,
    )
