from aiogram.enums import ParseMode

from src.bot.resources import sres
from src.bot.resources.datetime_formatter import date_format
from src.bot.resources.utils import shorten, esc_md
from src.bot.views.base.default.keyboards.confirmation import confirmation_ikm
from src.bot.views.base.models import View, ViewType
from src.bot.views.constants import Tag
from src.bot.views.custom.keyboards.card_group import card_group_ikm
from src.bot.views.custom.models.card_group import CardGroupViewData, CardGroupKeyboardData, DeleteCardGroupViewData

MAX_ITEMS_IN_SHORT_LIST = 5


def view__card_group(data: CardGroupViewData):
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
        date_create=date_format(data.date_create),
        items_short_list='\n'.join(items) if items else sres.CARD_GROUP.SHORT_LIST__NO_ITEM_PLACEHOLDER
    )

    markup = card_group_ikm(CardGroupKeyboardData(card_group_id=data.card_group_id, total_cards=total_cards))

    return View(view_type=ViewType.TEXT, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)


def view__delete_card_group(data: DeleteCardGroupViewData):
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
