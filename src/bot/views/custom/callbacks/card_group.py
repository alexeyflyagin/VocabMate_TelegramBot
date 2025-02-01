from enum import Enum

from aiogram.filters.callback_data import CallbackData

from src.bot.views.constants import CallbackPrefix


class CardGroupCD(CallbackData, prefix=CallbackPrefix.CARD_GROUP):
    card_group_id: int
    action: int

    class Action(int, Enum):
        DELETE = 0
        CARDS = 1