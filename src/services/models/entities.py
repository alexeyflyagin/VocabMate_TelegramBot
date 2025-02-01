from datetime import datetime

from pydantic import BaseModel


class WordCardEntity(BaseModel):
    id: int
    date_create: datetime
    group_id: int
    word: str
    transcription: str
    translations: list[str]
    pos: list[str]

    class Config:
        from_attributes = True


class CardGroupEntity(BaseModel):
    id: int
    date_create: datetime
    title: str

    cards: list[WordCardEntity] | None = None

    class Config:
        from_attributes = True
