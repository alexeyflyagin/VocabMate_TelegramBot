from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.resources import sres, commands
from src.bot.states import MainStates
from src.bot.utils.state_utils import cancel_current_action
from src.bot.utils.utils import check_user_id

router = Router(name=__name__)


@router.message(StateFilter(None))
async def start_command__handler(msg: Message, state: FSMContext):
    check_user_id(msg)
    await state.set_state(MainStates.Main)
    await msg.answer(text='👋')
    await msg.answer(text=sres.AUTH.WELCOME.format(first_name=msg.from_user.first_name), parse_mode=ParseMode.MARKDOWN)


@router.message(Command(commands.CANCEL))
async def cancel__handler(msg: Message, state: FSMContext):
    await cancel_current_action(msg, state)
