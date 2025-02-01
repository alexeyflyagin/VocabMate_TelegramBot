from sqlalchemy import select, func
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


async def get_page(
        s: AsyncSession,
        limit: int,
        page: int,
        block_row: bool = False,
) -> tuple[CardGroupOrm, ...] | None:
    query = select(CardGroupOrm).order_by(CardGroupOrm.date_create.desc())
    offset = page * limit
    query = query.offset(offset).limit(limit)
    query = set_with_for_update_if(query, block_row)
    r = await s.execute(query)
    return tuple(r.scalars().all())


async def get_total_count(
        s: AsyncSession,
) -> int | None:
    query = select(func.count()).select_from(CardGroupOrm)
    r = await s.execute(query)
    return r.scalar()


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
