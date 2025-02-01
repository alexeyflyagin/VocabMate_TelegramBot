from aiogram.filters.callback_data import CallbackData

from src.bot.views.base.constants import CallbackPrefix


class ConfirmationCD(CallbackData, prefix=CallbackPrefix.CONFIRMATION):
    tag: int
    p_arg: int | str | bool | None
    s_arg: int | str | bool | None
    action: int

    class Action:
        CANCEL = 0
        CONFIRM = 1
