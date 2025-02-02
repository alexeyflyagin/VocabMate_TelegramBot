from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ForceReply

from src.bot.checks import check_content_type, MsgCheckError
from src.bot.resources import sres, commands
from src.bot.states import NewCardGroupStates, MainStates
from src.bot.utils.update_state_utils import update_state__for__new_card_group, \
    update_state__for__new_card_item, update_state__for__start_training
from src.bot.utils.utils import show_card_list_of_card_group, show_card_group_list
from src.bot.views.base.default.callbacks.confirmation import ConfirmationCD
from src.bot.views.base.default.callbacks.list import ListCD
from src.bot.views.constants import Tag
from src.bot.views.custom.callbacks.card_group import CardGroupCD
from src.bot.views.custom.mappers.card_group import vd__card_group__from__entity, vd__delete_card_group__from__entity
from src.bot.views.custom.view.card_group import view__card_group, view__delete_card_group
from src.loggers import bot_logger
from src.services.exceptions import VocabMateNotFoundError
from src.services.impl.card_group import CardGroupService
from src.services.impl.card_item import CardItemService
from src.services.impl.training import TrainingService
from src.services.models.card_group import CreateCardGroupRequest, GetCardGroupsRequest
from src.services.models.card_item import GetCardsOfCardGroupRequest
from src.services.models.training import StartTrainingRequest

router = Router(name=__name__)
training_service: TrainingService
card_group_service: CardGroupService
card_item_service: CardItemService


@router.message(MainStates(), Command(commands.NEW_CARD_GROUP))
async def new_card_group__handler(msg: Message, state: FSMContext):
    await update_state__for__new_card_group(msg, state)


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
        await msg.answer(text=e.e_msg,
                         reply_markup=ForceReply(input_field_placeholder=sres.NEW_CARD_GROUP.ENTER_TITLE__MP))


@router.callback_query(CardGroupCD.filter())
async def card_group__callback(callback: CallbackQuery, state: FSMContext):
    data = CardGroupCD.unpack(callback.data)
    try:
        card_group = await card_group_service.get_card_group(data.card_group_id)
        if data.action == data.Action.DELETE:
            vd = vd__delete_card_group__from__entity(card_group)
            await view__delete_card_group(vd).edit_view(callback.message)
        elif data.action == data.Action.CARDS:
            request_data = GetCardsOfCardGroupRequest(card_group_id=data.card_group_id, limit=8)
            response = await card_item_service.get_cards_of_card_group(request_data)
            await show_card_list_of_card_group(callback.message, response, is_update=True)
        elif data.action == data.Action.BACK_TO_LIST:
            groups_data = await card_group_service.get_groups(GetCardGroupsRequest(limit=6))
            await show_card_group_list(callback.message, groups_data, is_update=True)
        elif data.action == data.Action.NEW_CARD:
            await update_state__for__new_card_item(callback.message, state, card_group.id)
            await callback.answer()
        elif data.action == data.Action.TO_TRAIN:
            request_data = StartTrainingRequest(card_group_id=card_group.id)
            response = await training_service.start_training(request_data)
            await update_state__for__start_training(callback.message, state, response)
            await callback.answer(sres.TRAINING.TRAINING_IS_STARTED)
        else:
            await callback.answer(sres.DEFAULT.UNEXPECTED_ACTION)
    except VocabMateNotFoundError as e:
        bot_logger.debug(e)
        groups_data = await card_group_service.get_groups(GetCardGroupsRequest(limit=6))
        await show_card_group_list(callback.message, groups_data, is_update=True)
        await callback.answer(sres.CARD_GROUP.NOT_FOUND_ERROR.format(id=data.card_group_id))


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
            groups_data = await card_group_service.get_groups(GetCardGroupsRequest(limit=6))
            await show_card_group_list(callback.message, groups_data)
        elif data.action == data.Action.CANCEL:
            vd = vd__card_group__from__entity(card_group)
            await view__card_group(vd).edit_view(callback.message)
            await callback.answer()
        else:
            await callback.answer(sres.DEFAULT.UNEXPECTED_ACTION)
    except VocabMateNotFoundError as e:
        bot_logger.debug(e)
        groups_data = await card_group_service.get_groups(GetCardGroupsRequest(limit=6))
        await show_card_group_list(callback.message, groups_data, is_update=True)
        await callback.answer(sres.CARD_GROUP.NOT_FOUND_ERROR.format(id=card_group_id))


@router.message(MainStates(), Command(commands.MY_CARD_GROUP))
async def my_card_groups__handler(msg: Message):
    groups_data = await card_group_service.get_groups(GetCardGroupsRequest(limit=6))
    await show_card_group_list(msg, groups_data)


@router.callback_query(ListCD.filter(F.tag == Tag.CARD_GROUP_LIST))
async def card_group_list__callback(callback: CallbackQuery, state: FSMContext):
    data = ListCD.unpack(callback.data)
    if data.action == data.Action.ADD:
        await update_state__for__new_card_group(callback.message, state)
        await callback.answer()
    elif data.action == data.Action.COUNTER:
        groups_data = await card_group_service.get_groups(GetCardGroupsRequest(page=data.c_page, limit=6))
        await show_card_group_list(callback.message, groups_data, is_update=True)
        await callback.answer()
    elif data.action == data.Action.NEXT:
        groups_data = await card_group_service.get_groups(GetCardGroupsRequest(page=data.c_page + 1, limit=6))
        await show_card_group_list(callback.message, groups_data, is_update=True)
        await callback.answer()
    elif data.action == data.Action.PREVIOUS:
        groups_data = await card_group_service.get_groups(GetCardGroupsRequest(page=data.c_page - 1, limit=6))
        await show_card_group_list(callback.message, groups_data, is_update=True)
        await callback.answer()
    elif data.action == data.Action.SELECT:
        try:
            card_group = await card_group_service.get_card_group(id_=data.selected_item_id)
            vd = vd__card_group__from__entity(card_group)
            await view__card_group(vd).edit_view(callback.message)
        except VocabMateNotFoundError as e:
            bot_logger.debug(e)
            groups_data = await card_group_service.get_groups(GetCardGroupsRequest(limit=6))
            await show_card_group_list(callback.message, groups_data, is_update=True)
            await callback.answer(sres.CARD_GROUP.NOT_FOUND_ERROR.format(id=data.selected_item_id))
    else:
        await callback.answer(sres.DEFAULT.UNEXPECTED_ACTION)


@router.callback_query(ListCD.filter(F.tag == Tag.CARD_LIST_OF_CARD_GROUP))
async def card_list_of_card_group__callback(callback: CallbackQuery, state: FSMContext):
    data = ListCD.unpack(callback.data)
    card_group_id = int(data.p_arg)
    try:
        card_group = await card_group_service.get_card_group(card_group_id)
        if data.action == data.Action.ADD:
            await update_state__for__new_card_item(callback.message, state, card_group.id)
            await callback.answer()
        elif data.action == data.Action.COUNTER:
            request_data = GetCardsOfCardGroupRequest(card_group_id=card_group_id, page=data.c_page, limit=8)
            response = await card_item_service.get_cards_of_card_group(request_data)
            await show_card_list_of_card_group(callback.message, response, is_update=True)
            await callback.answer()
        elif data.action == data.Action.NEXT:
            request_data = GetCardsOfCardGroupRequest(card_group_id=card_group_id, page=data.c_page + 1, limit=8)
            response = await card_item_service.get_cards_of_card_group(request_data)
            await show_card_list_of_card_group(callback.message, response, is_update=True)
            await callback.answer()
        elif data.action == data.Action.PREVIOUS:
            request_data = GetCardsOfCardGroupRequest(card_group_id=card_group_id, page=data.c_page - 1, limit=8)
            response = await card_item_service.get_cards_of_card_group(request_data)
            await show_card_list_of_card_group(callback.message, response, is_update=True)
            await callback.answer()
        elif data.action == data.Action.SELECT:
            await callback.answer(sres.DEFAULT.TEMPORARILY_UNAVAILABLE)
        elif data.action == data.Action.BACK:
            vd = vd__card_group__from__entity(card_group)
            await view__card_group(vd).edit_view(callback.message)
            await callback.answer()
        else:
            await callback.answer(sres.DEFAULT.UNEXPECTED_ACTION)
    except VocabMateNotFoundError as e:
        bot_logger.debug(e)
        groups_data = await card_group_service.get_groups(GetCardGroupsRequest(limit=6))
        await show_card_group_list(callback.message, groups_data, is_update=True)
        await callback.answer(sres.CARD_GROUP.NOT_FOUND_ERROR.format(id=card_group_id))
