import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.resources import sres
from src.bot.views.base.default.callbacks.list import ListCD
from src.bot.views.base.default.models.list import ListKeyboardData


def list_ikm(
        data: ListKeyboardData
) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    adjust: list[int] = []
    items_count = len(data.items)
    for element in data.position:

        if element == element.ADD_BTN and data.add_btn:
            add_btn_data = ListCD(tag=data.tag, c_page=data.c_page, p_arg=data.p_arg, s_arg=data.s_arg,
                                  action=ListCD.Action.ADD).pack()
            ikb.add(InlineKeyboardButton(text=data.add_btn, callback_data=add_btn_data))
            adjust.append(1)

        elif element == element.BACK_BTN and data.back_btn:
            back_btn_data = ListCD(tag=data.tag, c_page=data.c_page, p_arg=data.p_arg, s_arg=data.s_arg,
                                   action=ListCD.Action.BACK).pack()
            ikb.add(InlineKeyboardButton(text=data.back_btn, callback_data=back_btn_data))
            adjust.append(1)

        elif element == element.SCROLL:
            if (not data.is_always_scrollable and data.total_pages > 1) or data.is_always_scrollable:
                previous_btn_data = ListCD(tag=data.tag, c_page=data.c_page, p_arg=data.p_arg, s_arg=data.s_arg,
                                           action=ListCD.Action.PREVIOUS).pack()
                counter_btn_data = ListCD(tag=data.tag, c_page=data.c_page, p_arg=data.p_arg, s_arg=data.s_arg,
                                          action=ListCD.Action.COUNTER).pack()
                next_btn_data = ListCD(tag=data.tag, c_page=data.c_page, p_arg=data.p_arg, s_arg=data.s_arg,
                                       action=ListCD.Action.NEXT).pack()
                page_counter = sres.DEFAULT.BTN.PAGE_COUNTER.format(current=data.c_page + 1, total=data.total_pages)
                ikb.add(InlineKeyboardButton(text=sres.DEFAULT.BTN.PREVIOUS_SYM, callback_data=previous_btn_data))
                ikb.add(InlineKeyboardButton(text=page_counter, callback_data=counter_btn_data))
                ikb.add(InlineKeyboardButton(text=sres.DEFAULT.BTN.NEXT_SYM, callback_data=next_btn_data))
                adjust.append(3)

        elif element == element.ITEMS:
            rows = math.ceil(items_count / data.max_item_in_row)
            for i in range(rows):
                items = data.items[i * data.max_item_in_row:(i + 1) * data.max_item_in_row]
                for item in items:
                    item_data = ListCD(tag=data.tag, c_page=data.c_page, p_arg=data.p_arg, s_arg=data.s_arg,
                                       action=ListCD.Action.SELECT,
                                       selected_item_id=item.item_id).pack()
                    ikb.add(InlineKeyboardButton(text=item.btn_label, callback_data=item_data))
                adjust.append(len(items))

    ikb.adjust(*adjust)
    return ikb.as_markup()
