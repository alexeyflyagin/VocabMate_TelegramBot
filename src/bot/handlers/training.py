import math

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from src.bot.resources import sres, commands
from src.bot.resources.constants import TempStorageDataKeys
from src.bot.resources.keyboards import TRAINING_TERM_RKM, TRAINING_DEFINITION_RKM
from src.bot.resources.utils import progress_bar, esc_md
from src.bot.states import TrainingStates
from src.bot.utils.state_utils import set_global_state, get_temp_data
from src.bot.views.base.models import View
from src.services.impl.training import TrainingService
from src.services.models.training import AnswerLevelRequest

router = Router(name=__name__)
training_service: TrainingService


@router.message(TrainingStates(), Command(commands.CANCEL))
async def cancel__handler(msg: Message, state: FSMContext):
    training_id = await get_temp_data(state, TempStorageDataKeys.TRAINING_ID)
    try:
        response = await training_service.finish_training(training_id)
        await View.for_state(text=sres.TRAINING.FINISH_TEXT.format(
            card_group_title=esc_md(response.card_group.title),
            total_answered=response.total_answered,
            total_levels=response.total_levels,
            total_wrong=response.total_answered_wrong,
        ), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove()).answer_view(msg)
        await set_global_state(msg, state)
    except TelegramBadRequest:
        pass


@router.message(TrainingStates.Start, F.text == sres.TRAINING.BTN.LETS_GO)
async def start__handler(msg: Message, state: FSMContext):
    training_id = await get_temp_data(state, TempStorageDataKeys.TRAINING_ID)
    level_data = await training_service.get_current_level(training_id)
    percentage = level_data.total_answered / level_data.total_levels
    await View.for_state(text=sres.TRAINING.CARD__TERM__VIEW.format(
        progress_bar=esc_md(progress_bar(percentage)),
        percentage=f'{math.ceil(percentage * 100)}',
        total_answered=level_data.total_answered,
        total_levels=level_data.total_levels,
        term=esc_md(level_data.card_item.term),
    ), parse_mode=ParseMode.MARKDOWN, reply_markup=TRAINING_TERM_RKM).answer_view(msg)
    await state.set_state(TrainingStates.Term)


@router.message(TrainingStates.Term, F.text == sres.TRAINING.BTN.FORGOT)
@router.message(TrainingStates.Term, F.text == sres.TRAINING.BTN.REMEMBER)
async def term__handler(msg: Message, state: FSMContext):
    training_id = await get_temp_data(state, TempStorageDataKeys.TRAINING_ID)
    is_right = msg.text == sres.TRAINING.BTN.REMEMBER
    level_data = await training_service.get_current_level(training_id)
    answer_response = await training_service.answer_level(
        AnswerLevelRequest(training_id=training_id, is_right=is_right))
    if is_right:
        level_data = await training_service.get_current_level(training_id)
        if level_data.is_completed:
            await View.for_state(text=sres.TRAINING.FINISH_TEXT.format(
                card_group_title=esc_md(level_data.card_group.title),
                total_answered=level_data.total_answered,
                total_levels=level_data.total_levels,
                total_wrong=level_data.total_answered_wrong,
            ), parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardRemove()).answer_view(msg)
            await set_global_state(msg, state)
        else:
            percentage = level_data.total_answered / level_data.total_levels
            await View.for_state(text=sres.TRAINING.CARD__TERM__VIEW.format(
                progress_bar=esc_md(progress_bar(percentage)),
                percentage=f'{math.ceil(percentage * 100)}',
                total_answered=level_data.total_answered,
                total_levels=level_data.total_levels,
                term=esc_md(level_data.card_item.term),
            ), parse_mode=ParseMode.MARKDOWN, reply_markup=TRAINING_TERM_RKM).answer_view(msg)
    else:
        level_data.total_answered += 1
        percentage = level_data.total_answered / level_data.total_levels
        await View.for_state(text=sres.TRAINING.CARD__TERM__WITH_DEFINITION__VIEW.format(
            progress_bar=esc_md(progress_bar(percentage)),
            percentage=f'{math.ceil(percentage * 100)}',
            total_added=answer_response.total_added,
            total_answered=level_data.total_answered,
            total_levels=level_data.total_levels,
            term=esc_md(level_data.card_item.term),
            definition=esc_md(level_data.card_item.definition),
        ), parse_mode=ParseMode.MARKDOWN, reply_markup=TRAINING_DEFINITION_RKM).answer_view(msg)


@router.message(TrainingStates.Start)
async def other_start__handler(msg: Message):
    try:
        await msg.delete()
    except TelegramBadRequest:
        pass


@router.message(TrainingStates.Term)
@router.message(TrainingStates.Definition)
async def other_term__handler(msg: Message, state: FSMContext):
    training_id = await get_temp_data(state, TempStorageDataKeys.TRAINING_ID)
    level_data = await training_service.get_current_level(training_id)
    percentage = level_data.total_answered / level_data.total_levels
    await View.for_state(text=sres.TRAINING.CARD__TERM__VIEW.format(
        progress_bar=esc_md(progress_bar(percentage)),
        percentage=f'{math.ceil(percentage * 100)}',
        total_answered=level_data.total_answered,
        total_levels=level_data.total_levels,
        term=esc_md(level_data.card_item.term),
    ), parse_mode=ParseMode.MARKDOWN, reply_markup=TRAINING_TERM_RKM).answer_view(msg)
