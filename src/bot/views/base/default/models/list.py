from enum import Enum

from pydantic import BaseModel, Field


class ListItem(BaseModel):
    btn_label: str
    item_id: int


class Elements(str, Enum):
    BACK_BTN = 'back_btn'
    ADD_BTN = 'add_btn'
    ITEMS = 'items'
    SCROLL = 'scroll'


class Position(list[Elements], Enum):
    CLASSIC = [Elements.SCROLL, Elements.ITEMS, Elements.ADD_BTN, Elements.BACK_BTN]
    LOWER = [Elements.ITEMS, Elements.ADD_BTN, Elements.SCROLL, Elements.BACK_BTN]
    UPPER = [Elements.BACK_BTN, Elements.SCROLL, Elements.ITEMS, Elements.ADD_BTN]


class ListKeyboardData(BaseModel):
    tag: int
    items: list[ListItem]
    c_page: int
    total_items: int
    total_pages: int
    add_btn: str | None = None
    back_btn: str | None = None
    p_arg: int | str | bool | None = None
    s_arg: int | str | bool | None = None
    is_always_scrollable: bool = False
    max_item_in_row: int = Field(default=6, ge=1, le=8)
    position: list[Elements] = Position.CLASSIC
