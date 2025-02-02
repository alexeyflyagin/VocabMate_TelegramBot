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
    adjust = []
    new_card_data = CardGroupCD(card_group_id=data.card_group_id, action=CardGroupCD.Action.NEW_CARD).pack()
    cards_data = CardGroupCD(card_group_id=data.card_group_id, action=CardGroupCD.Action.CARDS).pack()
    delete_data = CardGroupCD(card_group_id=data.card_group_id, action=CardGroupCD.Action.DELETE).pack()
    ikb.add(InlineKeyboardButton(text=sres.BTN.ADD_NEW_CARD, callback_data=new_card_data))
    ikb.add(InlineKeyboardButton(text=add_counter(sres.BTN.CARDS, count=data.total_cards), callback_data=cards_data))
    ikb.add(InlineKeyboardButton(text=sres.BTN.DELETE, callback_data=delete_data))
    adjust += [2, 1]

    if data.back_btn:
        back_to_list_data = CardGroupCD(card_group_id=data.card_group_id, action=CardGroupCD.Action.BACK_TO_LIST).pack()
        ikb.add(InlineKeyboardButton(text=data.back_btn, callback_data=back_to_list_data))
        adjust.append(1)

    ikb.adjust(*adjust)
    return ikb.as_markup()
