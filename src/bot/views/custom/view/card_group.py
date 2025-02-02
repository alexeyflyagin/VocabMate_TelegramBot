from aiogram.enums import ParseMode

from src.bot.resources import sres
from src.bot.resources.datetime_formatter import date_format
from src.bot.resources.utils import shorten, esc_md
from src.bot.views.base.default.keyboards.confirmation import confirmation_ikm
from src.bot.views.base.default.keyboards.list import list_ikm
from src.bot.views.base.default.models.list import ListItem, ListKeyboardData
from src.bot.views.base.models import View, ViewType
from src.bot.views.constants import Tag
from src.bot.views.custom.keyboards.card_group import card_group_ikm
from src.bot.views.custom.models.card_group import CardGroupViewData, CardGroupKeyboardData, DeleteCardGroupViewData, \
    CardGroupPageOfListViewData

MAX_ITEMS_IN_SHORT_LIST = 5


def view__card_group(data: CardGroupViewData) -> View:
    if not isinstance(data, CardGroupViewData):
        raise ValueError("Invalid type of data view. Required: `CardGroupViewData`")

    items = []
    total_cards = len(data.card_labels)
    for i in range(min(total_cards, MAX_ITEMS_IN_SHORT_LIST)):
        item = sres.CARD_GROUP.SHORT_LIST__ITEM.format(card_content=shorten(data.card_labels[i]))
        item = esc_md(item)
        items.append(item)

    if total_cards > MAX_ITEMS_IN_SHORT_LIST:
        more_items_counter = total_cards - MAX_ITEMS_IN_SHORT_LIST
        items.append(sres.CARD_GROUP.SHORT_LIST__MORE.format(more_counter=more_items_counter))

    text = sres.CARD_GROUP.VIEW.format(
        id=data.card_group_id,
        title=esc_md(data.title),
        created_at=date_format(data.created_at),
        items_short_list='\n'.join(items) if items else sres.CARD_GROUP.SHORT_LIST__NO_ITEM_PLACEHOLDER
    )

    markup = card_group_ikm(CardGroupKeyboardData(card_group_id=data.card_group_id, total_cards=total_cards))

    return View(view_type=ViewType.TEXT, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)


def view__delete_card_group(data: DeleteCardGroupViewData) -> View:
    if not isinstance(data, DeleteCardGroupViewData):
        raise ValueError("Invalid type of data view. Required: `DeleteCardGroupViewData`")

    text = sres.CARD_GROUP.DELETE.DELETE_CONFIRMATION_VIEW.format(title=esc_md(data.title))
    if data.total_cards:
        text = sres.CARD_GROUP.DELETE.DELETE_CONFIRMATION_WITH_CARDS_VIEW.format(
            title=esc_md(data.title),
            cards_counter=data.total_cards,
        )

    markup = confirmation_ikm(tag=Tag.DELETE_CARD_GROUP_CONFIRMATION, p_arg=data.card_group_id)

    return View(view_type=ViewType.TEXT, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)


def view__card_group_list(data: CardGroupPageOfListViewData) -> View:
    if not isinstance(data, CardGroupPageOfListViewData):
        raise ValueError("Invalid type of data view. Required: `CardGroupPageOfListViewData`")

    list_items: list[ListItem] = []
    items: list[str] = []

    start_index = data.page * data.limit + 1
    for i in range(len(data.items)):
        item = data.items[i]
        list_item = ListItem(btn_label=str(start_index + i), item_id=item.card_group_id)
        list_items.append(list_item)
        item_text = sres.CARD_GROUP_LIST.ITEM.format(
            btn_label=list_item.btn_label,
            title=esc_md(shorten(item.title, width=30))
        )
        items.append(item_text)

    text = sres.CARD_GROUP_LIST.VIEW__NO_ITEMS
    if items:
        text = sres.CARD_GROUP_LIST.VIEW.format(items='\n'.join(items))

    markup_data = ListKeyboardData(
        tag=Tag.CARD_GROUP_LIST,
        add_btn=sres.DEFAULT.BTN.ADD,
        items=list_items,
        c_page=data.page,
        total_pages=data.total_pages,
        total_items=data.total_items,
    )
    markup = list_ikm(markup_data)

    return View(view_type=ViewType.TEXT, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
