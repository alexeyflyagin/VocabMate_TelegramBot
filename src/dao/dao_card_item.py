from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.utils import set_with_for_update_if
from src.data.models import CardItemOrm


async def get_by_id(
        s: AsyncSession,
        id_: int,
        with_for_update: bool = False
) -> CardItemOrm:
    query = select(CardItemOrm).filter(CardItemOrm.id == id_)
    set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def get_by_group_id(
        s: AsyncSession,
        group_id: int,
        with_for_update: bool = False
) -> tuple[CardItemOrm, ...]:
    query = select(CardItemOrm).filter(CardItemOrm.group_id == group_id).order_by(CardItemOrm.created_at)
    set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return tuple(res.scalars().all())


async def create(
        s: AsyncSession,
        group_id: int,
        term: str,
        definition: str,
) -> CardItemOrm:
    new_row = CardItemOrm(group_id=group_id, term=term, definition=definition)
    s.add(new_row)
    await s.flush()
    return new_row


async def delete(
        s: AsyncSession,
        row: CardItemOrm
):
    await s.delete(row)
    await s.flush()
