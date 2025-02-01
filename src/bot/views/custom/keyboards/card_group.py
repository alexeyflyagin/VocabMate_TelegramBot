from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.resources import sres
from src.bot.resources.utils import add_counter
from src.bot.views.custom.callbacks.card_group import CardGroupCD
from src.bot.views.custom.models.card_group import CardGroupKeyboardData


def card_group_ikm(data: CardGroupKeyboardData) -> InlineKeyboardMarkup:
    if not isinstance(data, CardGroupKeyboardData):
        raise ValueError("Invalid type of data view. Required: `CardGroupKeyboardData`")

    ikb = InlineKeyboardBuilder()
    cards_data = CardGroupCD(card_group_id=data.card_group_id, action=CardGroupCD.Action.CARDS).pack()
    delete_data = CardGroupCD(card_group_id=data.card_group_id, action=CardGroupCD.Action.DELETE).pack()
    ikb.add(InlineKeyboardButton(text=add_counter(sres.BTN.CARDS, count=data.total_cards), callback_data=cards_data))
    ikb.add(InlineKeyboardButton(text=sres.BTN.DELETE, callback_data=delete_data))
    ikb.adjust(1)
    return ikb.as_markup()
