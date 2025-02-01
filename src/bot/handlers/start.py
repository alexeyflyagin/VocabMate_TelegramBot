from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import commands
from src.bot.resources import sres
from src.bot.handlers.utils import check_user_id
from src.bot.states import MainStates

router = Router(name=__name__)


@router.message(StateFilter(None))
async def start_command__handler(msg: Message, state: FSMContext):
    check_user_id(msg)
    await state.set_state(MainStates.Main)
    await msg.answer(text='👋')
    await msg.answer(text=sres.AUTH.WELCOME.format(first_name=msg.from_user.first_name), parse_mode=ParseMode.MARKDOWN)


@router.message(Command(commands.CANCEL))
async def cancel__handler(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state and current_state.startswith(MainStates.__name__):
        await msg.answer(text=sres.CANCEL.NO_ACTIONS)
        return
    await state.set_state(MainStates.Main)
    await msg.answer(text=sres.CANCEL.SUCCESS)
