from typing import Dict, Any

from aiogram.filters.state import StateType
from aiogram.fsm.storage.base import StorageKey

from src.dao import dao_user_state
from src.data.session_manager import SessionManager


class UserStateService:

    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        async with self._session_manager.session as s:
            user_state = await dao_user_state.get_by_key(s, key)
            if user_state is None:
                user_state = await dao_user_state.create(s, key)
            user_state.state = state.state
            await s.commit()

    async def get_state(self, key: StorageKey) -> str | None:
        async with self._session_manager.session as s:
            user_state = await dao_user_state.get_by_key(s, key)
            if user_state is None:
                user_state = await dao_user_state.create(s, key)
            return user_state.state

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        async with self._session_manager.session as s:
            user_state = await dao_user_state.get_by_key(s, key)
            if user_state is None:
                user_state = await dao_user_state.create(s, key)
            user_state.data = data
            await s.commit()

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        async with self._session_manager.session as s:
            user_state = await dao_user_state.get_by_key(s, key)
            if user_state is None:
                user_state = await dao_user_state.create(s, key)
            return user_state.data
