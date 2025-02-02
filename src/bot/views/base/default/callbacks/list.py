from aiogram.filters.callback_data import CallbackData

from src.bot.views.base.constants import CallbackPrefix


class ListCD(CallbackData, prefix=CallbackPrefix.LIST):
    tag: int
    c_page: int
    action: int
    p_arg: int | str | bool | None
    s_arg: int | str | bool | None
    selected_item_id: int | None = None

    class Action:
        PREVIOUS = 0
        COUNTER = 1
        NEXT = 2
        SELECT = 3
        BACK = 4
        ADD = 5
