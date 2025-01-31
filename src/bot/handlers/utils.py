from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.bot import sres
from src.bot.exceptions import InvalidTrustedUserId
from src.loggers import bot_logger

TRUSTED_USER_ID: int | None = None


def check_user_id(msg: Message):
    if TRUSTED_USER_ID is None:
        bot_logger.critical('The TRUSTED_USER_ID was not found.')
    if TRUSTED_USER_ID != msg.from_user.id:
        raise InvalidTrustedUserId(msg.from_user.id)
    return


async def unknown_error(msg: Message, state: FSMContext):
    # Probably `state` will be useful in the future
    await msg.answer(sres.ERRORS.UNEXPECTED)


async def unknown_error_for_callback(callback: CallbackQuery, state: FSMContext):
    # Probably `state` will be useful in the future
    await callback.answer(sres.ERRORS.UNEXPECTED)
