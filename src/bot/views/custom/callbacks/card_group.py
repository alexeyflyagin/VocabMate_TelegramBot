from enum import IntEnum

from aiogram.filters.callback_data import CallbackData

from src.bot.views.constants import CallbackPrefix


class CardGroupCD(CallbackData, prefix=CallbackPrefix.CARD_GROUP):
    card_group_id: int
    action: int

    class Action(IntEnum):
        DELETE = 0
        CARDS = 1
        BACK_TO_LIST = 2
        NEW_CARD = 3
        TO_TRAIN = 4
