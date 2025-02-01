from aiogram import Router, F
from aiogram.enums import ParseMode, ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.bot.checks import check_content_type, MsgCheckError
from src.bot.resources import sres, commands
from src.bot.states import NewCardGroupStates, MainStates
from src.bot.views.base.default.callbacks.confirmation import ConfirmationCD
from src.bot.views.base.default.callbacks.list import ListCD
from src.bot.views.constants import Tag
from src.bot.views.custom.callbacks.card_group import CardGroupCD
from src.bot.views.custom.mappers.card_group import vd__card_group__from__entity, vd__delete_card_group__from__entity, \
    vd__card_group_page_of_list__from__get_card_groups_response
from src.bot.views.custom.view.card_group import view__card_group, view__delete_card_group, view__card_group_list
from src.loggers import bot_logger
from src.services.exceptions import VocabMateNotFoundError
from src.services.impl.card_group import CardGroupService
from src.services.models.card_group import CreateCardGroupRequest, GetCardGroupsRequest

router = Router(name=__name__)
card_group_service: CardGroupService


@router.message(MainStates(), Command(commands.NEW_CARD_GROUP))
async def new_card_group__handler(msg: Message, state: FSMContext):
    await state.set_state(NewCardGroupStates.Title)
    await msg.answer(text=sres.NEW_CARD_GROUP.ENTER_TITLE, parse_mode=ParseMode.MARKDOWN)


@router.message(NewCardGroupStates.Title)
async def new_card_group__title__handler(msg: Message, state: FSMContext):
    try:
        check_content_type(msg, ContentType.TEXT)

        request_data = CreateCardGroupRequest(title=msg.text)
        card_group = await card_group_service.create_card_group(request_data)
        vd = vd__card_group__from__entity(card_group)

        await msg.answer(text=sres.NEW_CARD_GROUP.SUCCESS)
        await view__card_group(vd).answer_view(msg)

        await state.set_state(MainStates.Main)
    except MsgCheckError as e:
        await msg.answer(text=e.e_msg)


@router.callback_query(CardGroupCD.filter())
async def card_group__callback(callback: CallbackQuery):
    data = CardGroupCD.unpack(callback.data)
    try:
        card_group = await card_group_service.get_card_group(data.card_group_id)
        if data.action == data.Action.DELETE:
            vd = vd__delete_card_group__from__entity(card_group)
            await view__delete_card_group(vd).edit_view(callback.message)
    except VocabMateNotFoundError as e:
        bot_logger.debug(e)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer(text=sres.CARD_GROUP.NOT_FOUND_ERROR.format(id=data.card_group_id))


@router.callback_query(ConfirmationCD.filter(F.tag == Tag.DELETE_CARD_GROUP_CONFIRMATION))
async def delete__card_group__callback(callback: CallbackQuery):
    data = ConfirmationCD.unpack(callback.data)
    card_group_id = int(data.p_arg)
    try:
        card_group = await card_group_service.get_card_group(card_group_id)
        if data.action == data.Action.CONFIRM:
            await card_group_service.delete_card_group(card_group_id)
            deleted_text = sres.CARD_GROUP.DELETE.SUCCESS.format(id=card_group_id)
            await callback.message.edit_text(text=deleted_text)
            await callback.answer(deleted_text)
        elif data.action == data.Action.CANCEL:
            vd = vd__card_group__from__entity(card_group)
            await view__card_group(vd).edit_view(callback.message)
            await callback.answer()
    except VocabMateNotFoundError as e:
        bot_logger.debug(e)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer(text=sres.CARD_GROUP.NOT_FOUND_ERROR.format(id=data.card_group_id))


@router.message(MainStates(), Command(commands.MY_CARD_GROUP))
async def my_card_groups__handler(msg: Message):
    groups_data = await card_group_service.get_groups(GetCardGroupsRequest(limit=6))
    vd = vd__card_group_page_of_list__from__get_card_groups_response(groups_data)
    await view__card_group_list(vd).answer_view(msg)


@router.callback_query(ListCD.filter(F.tag == Tag.CARD_GROUP_LIST))
async def new_card_group__handler(callback: CallbackQuery, state: FSMContext):
    data = ListCD.unpack(callback.data)
    if data.action == data.Action.ADD:
        await state.set_state(NewCardGroupStates.Title)
        await callback.message.answer(text=sres.NEW_CARD_GROUP.ENTER_TITLE, parse_mode=ParseMode.MARKDOWN)
        await callback.answer()
    elif data.action == data.Action.COUNTER:
        groups_data = await card_group_service.get_groups(GetCardGroupsRequest(limit=6))
        vd = vd__card_group_page_of_list__from__get_card_groups_response(groups_data)
        await view__card_group_list(vd).edit_view(callback.message)
        await callback.answer()
    elif data.action == data.Action.NEXT:
        groups_data = await card_group_service.get_groups(GetCardGroupsRequest(page=data.c_page + 1, limit=6))
        vd = vd__card_group_page_of_list__from__get_card_groups_response(groups_data)
        await view__card_group_list(vd).edit_view(callback.message)
        await callback.answer()
    elif data.action == data.Action.PREVIOUS:
        groups_data = await card_group_service.get_groups(GetCardGroupsRequest(page=data.c_page - 1, limit=6))
        vd = vd__card_group_page_of_list__from__get_card_groups_response(groups_data)
        await view__card_group_list(vd).edit_view(callback.message)
        await callback.answer()
    elif data.action == data.Action.SELECT:
        await callback.answer(text=sres.DEFAULT.TEMPORARILY_UNAVAILABLE)
