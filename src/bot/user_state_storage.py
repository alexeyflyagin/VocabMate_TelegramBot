from typing import Dict, Any, Optional

from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType

from src.loggers import bot_logger
from src.services.user_state import UserStateService


class PgSQLUserStateStorage(BaseStorage):

    def __init__(self, user_state_service: UserStateService):
        self.user_state_service = user_state_service

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        try:
            await self.user_state_service.set_state(key, state)
        except Exception as e:
            bot_logger.critical(e)
            raise

    async def get_state(self, key: StorageKey) -> Optional[str]:
        try:
            return await self.user_state_service.get_state(key)
        except Exception as e:
            bot_logger.critical(e)
            raise

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        try:
            await self.user_state_service.set_data(key, data)
        except Exception as e:
            bot_logger.critical(e)
            raise

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        try:
            return await self.user_state_service.get_data(key)
        except Exception as e:
            bot_logger.critical(e)
            raise

    async def close(self) -> None:
        pass
