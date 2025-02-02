from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.utils import set_with_for_update_if
from src.data.models import TrainingOrm


async def get_by_id(
        s: AsyncSession,
        id_: int,
        with_for_update: bool = False
) -> TrainingOrm | None:
    query = select(TrainingOrm).filter(TrainingOrm.id == id_)
    set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def create(
        s: AsyncSession,
        card_group_id: int
) -> TrainingOrm:
    new_row = TrainingOrm(card_group_id=card_group_id)
    s.add(new_row)
    await s.flush()
    return new_row


async def delete(
        s: AsyncSession,
        row: TrainingOrm
):
    await s.delete(row)
    await s.flush()


async def delete_all(
        s: AsyncSession,
):
    query = select(TrainingOrm)
    set_with_for_update_if(query, True)
    res = await s.execute(query)
    rows = res.scalars().all()
    if not rows:
        return
    for row in rows:
        await s.delete(row)
    await s.flush()
