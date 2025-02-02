from datetime import datetime

from pydantic import BaseModel

from src.bot.resources import sres


class CardGroupItemData(BaseModel):
    card_group_id: int
    created_at: datetime
    title: str
    card_labels: list[str]


class CardItemData(BaseModel):
    card_item_id: int
    created_at: datetime
    term: str
    definition: str


class CardGroupPageListViewData(BaseModel):
    total_items: int
    page: int
    total_pages: int
    limit: int
    items: list[CardGroupItemData]


class CardPageListOfCardGroupViewData(BaseModel):
    total_items: int
    page: int
    total_pages: int
    limit: int
    card_group_id: int
    card_group_title: str
    items: list[CardItemData]


class CardGroupViewData(BaseModel):
    card_group_id: int
    created_at: datetime
    title: str
    card_labels: list[str]
    back_btn: str | None = sres.BTN.BACK_TO_LIST


class DeleteCardGroupViewData(BaseModel):
    card_group_id: int
    title: str
    total_cards: int


class CardGroupKeyboardData(BaseModel):
    card_group_id: int
    total_cards: int
    back_btn: str | None = None
