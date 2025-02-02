from aiogram import Router
from aiogram.enums import ContentType, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ForceReply, ReplyKeyboardRemove

from src.bot.checks import check_content_type, MsgCheckError
from src.bot.resources import sres
from src.bot.resources.constants import TempStorageDataKeys
from src.bot.states import NewCardItemStates
from src.bot.utils.state_utils import update_temp_data, get_temp_data, set_global_state, unknown_error, \
    cancel_current_action
from src.bot.utils.utils import show_card_list_of_card_group, show_card_group_list
from src.bot.views.base.models import View
from src.bot.views.custom.mappers.card_group import vd__card_group__from__entity
from src.bot.views.custom.view.card_group import view__card_group
from src.loggers import bot_logger
from src.services.exceptions import VocabMateNotFoundError
from src.services.impl.card_group import CardGroupService
from src.services.impl.card_item import CardItemService
from src.services.models.card_group import GetCardGroupsRequest
from src.services.models.card_item import AddCardItemRequest, GetCardsOfCardGroupRequest

router = Router(name=__name__)
card_item_service: CardItemService
card_group_service: CardGroupService


@router.message(NewCardItemStates.Term)
async def new_card_item__term__handler(msg: Message, state: FSMContext):
    try:
        check_content_type(msg, ContentType.TEXT)
        await update_temp_data(state, TempStorageDataKeys.TERM__FOR__NEW_CARD_ITEM, msg.text)

        await state.set_state(NewCardItemStates.Definition)
        markup = ForceReply(input_field_placeholder=sres.NEW_CARD_ITEM.ENTER_DEFINITION__MP)
        await View.for_state(text=sres.NEW_CARD_ITEM.ENTER_DEFINITION, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=markup).answer_view(msg)
    except MsgCheckError as e:
        await msg.answer(text=e.e_msg,
                         reply_markup=ForceReply(input_field_placeholder=sres.NEW_CARD_ITEM.ENTER_TERM__MP))


@router.message(NewCardItemStates.Definition)
async def new_card_item__definition__handler(msg: Message, state: FSMContext):
    group_id = await get_temp_data(state, TempStorageDataKeys.GROUP_ID__FOR__NEW_CARD_ITEM)
    term = await get_temp_data(state, TempStorageDataKeys.TERM__FOR__NEW_CARD_ITEM)
    try:
        check_content_type(msg, ContentType.TEXT)
        request_data = AddCardItemRequest(group_id=group_id, term=term, definition=msg.text)
        await card_item_service.add_card_item(request_data)
        card_group = await card_group_service.get_card_group(group_id)

        success_msg_text = sres.NEW_CARD_ITEM.SUCCESS.format(title=card_group.title)
        view = View.for_state(text=success_msg_text, parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove())
        await set_global_state(msg, state, view=view)

        request_data = GetCardsOfCardGroupRequest(card_group_id=card_group.id, limit=8)
        response = await card_item_service.get_cards_of_card_group(request_data)
        await show_card_list_of_card_group(msg, response)
    except MsgCheckError as e:
        await msg.answer(text=e.e_msg,
                         reply_markup=ForceReply(input_field_placeholder=sres.NEW_CARD_ITEM.ENTER_TERM__MP))
    except VocabMateNotFoundError as e:
        bot_logger.debug(e)
        await msg.answer(sres.CARD_GROUP.NOT_FOUND_ERROR.format(id=group_id))
        groups_data = await card_group_service.get_groups(GetCardGroupsRequest(limit=6))
        await show_card_group_list(msg, groups_data)

