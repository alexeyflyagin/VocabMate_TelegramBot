from datetime import datetime

from pydantic import BaseModel


class CardGroupViewData(BaseModel):
    card_group_id: int
    date_create: datetime
    title: str
    card_labels: list[str]


class DeleteCardGroupViewData(BaseModel):
    card_group_id: int
    title: str
    total_cards: int


class CardGroupKeyboardData(BaseModel):
    card_group_id: int
    total_cards: int
