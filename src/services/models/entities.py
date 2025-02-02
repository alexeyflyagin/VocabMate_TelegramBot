from datetime import datetime

from pydantic import BaseModel


class CardItemEntity(BaseModel):
    id: int
    created_at: datetime
    group_id: int
    term: str
    definition: str

    class Config:
        from_attributes = True


class CardGroupEntity(BaseModel):
    id: int
    created_at: datetime
    title: str

    cards: list[CardItemEntity] | None = None

    class Config:
        from_attributes = True
