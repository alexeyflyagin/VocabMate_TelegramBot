from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ForceReply

from src.bot.resources import sres, keyboards
from src.bot.resources.constants import TempStorageDataKeys
from src.bot.states import NewCardGroupStates, NewCardItemStates, TrainingStates
from src.bot.utils.state_utils import set_global_state, update_temp_data
from src.bot.views.base.models import View
from src.services.models.training import StartTrainingResponse


async def update_state__for__new_card_group(msg: Message, state: FSMContext):
    markup = ForceReply(input_field_placeholder=sres.NEW_CARD_GROUP.ENTER_TITLE__MP)
    view = View.for_state(text=sres.NEW_CARD_GROUP.ENTER_TITLE, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    await set_global_state(msg, state, new_state=NewCardGroupStates.Title, view=view)


async def update_state__for__new_card_item(msg: Message, state: FSMContext, card_group_id: int):
    if not isinstance(msg, Message) or not isinstance(state, FSMContext) or not isinstance(card_group_id, int):
        raise ValueError(
            f"Invalid arg types: msg={type(msg)}, state={type(state)}, card_group_id={type(card_group_id)}")

    markup = ForceReply(input_field_placeholder=sres.NEW_CARD_ITEM.ENTER_TERM__MP)
    view = View.for_state(text=sres.NEW_CARD_ITEM.ENTER_TERM, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    await set_global_state(msg, state, new_state=NewCardItemStates.Term, view=view)
    await update_temp_data(state, TempStorageDataKeys.GROUP_ID__FOR__NEW_CARD_ITEM, card_group_id)


async def update_state__for__start_training(msg: Message, state: FSMContext, training: StartTrainingResponse):
    if not isinstance(msg, Message) or not isinstance(state, FSMContext) \
            or not isinstance(training, StartTrainingResponse):
        raise ValueError(f"Invalid arg types: msg={type(msg)}, state={type(state)}, training={type(training)}")

    markup = keyboards.TRAINING_RKM
    text = sres.TRAINING.START_TEXT.format(total_levels=training.total_levels,
                                           card_group_title=training.card_group.title)
    view = View.for_state(text, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    await set_global_state(msg, state, new_state=TrainingStates.Start, view=view)
    await update_temp_data(state, TempStorageDataKeys.TRAINING_ID, training.training_id)
