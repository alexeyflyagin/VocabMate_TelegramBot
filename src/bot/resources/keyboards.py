from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.resources import sres

TRAINING_RKM = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=sres.TRAINING.BTN.LETS_GO)]],
    is_persistent=True, resize_keyboard=True,
)

TRAINING_TERM_RKM = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=sres.TRAINING.BTN.FORGOT), KeyboardButton(text=sres.TRAINING.BTN.REMEMBER)]],
    is_persistent=True, resize_keyboard=True,
)

TRAINING_DEFINITION_RKM = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=sres.TRAINING.BTN.OK)]],
    is_persistent=True, resize_keyboard=True,
)

