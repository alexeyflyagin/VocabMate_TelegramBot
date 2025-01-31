from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.loggers import bot_logger

router = Router(name=__name__)

@router.message(CommandStart())
async def start_command__handler(msg: Message, state: FSMContext):
    bot_logger.info(msg.date)
