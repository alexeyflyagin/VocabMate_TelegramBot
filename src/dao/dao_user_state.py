from aiogram.fsm.storage.base import StorageKey
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import UserStateOrm


async def get_by_key(
        s: AsyncSession,
        key: StorageKey,
        with_for_update: bool = False
) -> UserStateOrm:
    query = ((select(UserStateOrm).filter(UserStateOrm.user_id == key.user_id)
              .filter(UserStateOrm.bot_id == key.bot_id)).filter(UserStateOrm.thread_id == key.thread_id)
             .filter(UserStateOrm.destiny == key.destiny).filter(UserStateOrm.chat_id == key.chat_id)
             .filter(UserStateOrm.business_connection_id == key.business_connection_id))
    if with_for_update:
        query = query.with_for_update()
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def create(
        s: AsyncSession,
        key: StorageKey,
) -> UserStateOrm:
    user_state = UserStateOrm(bot_id=key.bot_id, chat_id=key.chat_id, user_id=key.user_id, thread_id=key.thread_id,
                              business_connection_id=key.business_connection_id, destiny=key.destiny)
    s.add(user_state)
    await s.flush()
    return user_state
