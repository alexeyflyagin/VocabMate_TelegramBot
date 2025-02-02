from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent

from src.bot.exceptions import InvalidTrustedUserId
from src.bot.handlers.utils import unknown_error, unknown_error_for_callback
from src.bot.resources import sres
from src.loggers import bot_logger

router = Router(name=__name__)


@router.error()
async def error__handler(event: ErrorEvent, state: FSMContext):
    if isinstance(event.exception, InvalidTrustedUserId):
        bot_logger.info(event.exception)
        await event.update.message.answer(text=sres.ERRORS.ACCESS_ERROR, parse_mode=ParseMode.MARKDOWN)
    else:
        bot_logger.exception(event.exception)
        if event.update.message:
            await unknown_error(event.update.message, state)
        elif event.update.callback_query:
            await unknown_error_for_callback(event.update.callback_query, state)
