import random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.resources import sres
from src.bot.views.base.default.callbacks.confirmation import ConfirmationCD


def confirmation_ikm(
        tag: int,
        p_arg: int | str | bool | None = None,
        s_arg: int | str | bool | None = None,
) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    confirm_data = ConfirmationCD(tag=tag, p_arg=p_arg, s_arg=s_arg, action=ConfirmationCD.Action.CONFIRM).pack()
    cancel_data = ConfirmationCD(tag=tag, p_arg=p_arg, s_arg=s_arg, action=ConfirmationCD.Action.CANCEL).pack()
    buttons = [
        InlineKeyboardButton(text=sres.BTN.CONFIRM, callback_data=confirm_data),
        InlineKeyboardButton(text=sres.BTN.CANCEL, callback_data=cancel_data),
    ]
    random.shuffle(buttons)
    ikb.add(*buttons)
    ikb.adjust(2)
    return ikb.as_markup()
