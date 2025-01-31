from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.utils import set_with_for_update_if
from src.data.models import CardGroupOrm


async def get_by_id(
        s: AsyncSession,
        id_: int,
        with_for_update: bool = False
) -> CardGroupOrm:
    query = select(CardGroupOrm).filter(CardGroupOrm.id == id_)
    set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def create(
        s: AsyncSession,
        title: str
) -> CardGroupOrm:
    new_row = CardGroupOrm(title=title)
    s.add(new_row)
    await s.flush()
    return new_row


async def delete(
        s: AsyncSession,
        row: CardGroupOrm
):
    await s.delete(row)
    await s.flush()
