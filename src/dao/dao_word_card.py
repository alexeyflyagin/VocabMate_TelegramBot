from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.utils import set_with_for_update_if
from src.data.models import WordCardOrm


async def get_by_id(
        s: AsyncSession,
        id_: int,
        with_for_update: bool = False
) -> WordCardOrm:
    query = select(WordCardOrm).filter(WordCardOrm.id == id_)
    set_with_for_update_if(query, with_for_update)
    res = await s.execute(query)
    return res.scalar_one_or_none()


async def create(
        s: AsyncSession,
        group_id: int,
        word: str,
        transcriptions: str,
        translations: list[str],
        pos: list[str],
) -> WordCardOrm:
    new_row = WordCardOrm(group_id=group_id, word=word, transcriptions=transcriptions, translations=translations,
                          pos=pos)
    s.add(new_row)
    await s.flush()
    return new_row


async def delete(
        s: AsyncSession,
        row: WordCardOrm
):
    await s.delete(row)
    await s.flush()
