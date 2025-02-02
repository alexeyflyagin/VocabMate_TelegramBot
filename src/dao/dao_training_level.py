from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.utils import set_with_for_update_if
from src.data.models import TrainingLevelOrm


async def get_by_id(
        s: AsyncSession,
        id_: int,
        with_for_update: bool = False,
) -> TrainingLevelOrm | None:
    query = select(TrainingLevelOrm).filter(TrainingLevelOrm.id == id_)
    set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def create(
        s: AsyncSession,
        training_id: int,
        card_item_id: int,
) -> TrainingLevelOrm:
    new_row = TrainingLevelOrm(training_id=training_id, card_item_id=card_item_id)
    s.add(new_row)
    await s.flush()
    return new_row


async def get_total_count_by_training_id(
        s: AsyncSession,
        training_id: int,
) -> int | None:
    query = select(func.count()).select_from(TrainingLevelOrm).filter(TrainingLevelOrm.training_id == training_id)
    r = await s.execute(query)
    return r.scalar()


async def get_total_answered_by_training_id(
        s: AsyncSession,
        training_id: int,
        answered_is_right: bool | None = None
) -> int | None:
    query = select(func.count()).select_from(TrainingLevelOrm).filter(TrainingLevelOrm.training_id == training_id)
    query = query.filter(TrainingLevelOrm.answered_at.is_not(None))
    if answered_is_right is not None:
        query = query.filter(TrainingLevelOrm.answer_is_right == answered_is_right)
    r = await s.execute(query)
    return r.scalar()


async def get_total_not_answered_by_training_id(
        s: AsyncSession,
        training_id: int,
) -> int | None:
    query = select(func.count()).select_from(TrainingLevelOrm).filter(TrainingLevelOrm.training_id == training_id)
    query = query.filter(TrainingLevelOrm.answered_at.is_(None))
    r = await s.execute(query)
    return r.scalar()


async def get_random_not_answered_by_training_id(
        s: AsyncSession,
        training_id: int,
        with_for_update: bool = False
) -> TrainingLevelOrm | None:
    query = select(TrainingLevelOrm).filter(TrainingLevelOrm.training_id == training_id)
    query = query.filter(TrainingLevelOrm.answered_at.is_(None))
    query = query.order_by(func.random())
    set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalars().first()


async def delete(
        s: AsyncSession,
        row: TrainingLevelOrm
):
    await s.delete(row)
    await s.flush()
