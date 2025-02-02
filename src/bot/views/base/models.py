from enum import StrEnum

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, ForceReply, Message
from pydantic import BaseModel, Field

from src.loggers import bot_logger


class ViewType(StrEnum):
    TEXT = "text"


class View(BaseModel):
    view_type: ViewType = Field(default=ViewType.TEXT)
    text: str | None = Field(default=None)
    parse_mode: ParseMode | None = Field(default=None)
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = Field(
        default=None)

    @staticmethod
    def for_state(
            text: str,
            parse_mode: ParseMode | None = None,
            reply_markup: ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
    ) -> "View":
        return View(view_type=ViewType.TEXT, text=text, parse_mode=parse_mode, reply_markup=reply_markup)

    async def answer_view(
            self,
            msg: Message,
    ) -> Message:
        return await self.show_view(msg.bot, msg.chat.id)

    async def edit_view(
            self,
            msg: Message,
    ) -> Message:
        return await self.show_view(msg.bot, msg.chat.id, update_msg_id=msg.message_id)

    async def update_view(
            self,
            bot: Bot,
            chat_id: int,
            updated_msg_id: int,
    ) -> Message:
        return await self.show_view(bot, chat_id, update_msg_id=updated_msg_id)

    async def show_view(
            self,
            bot: Bot,
            chat_id: int,
            update_msg_id: int | None = None,
    ) -> Message:
        try:
            if self.view_type == ViewType.TEXT and update_msg_id:
                new_msg = await bot.edit_message_text(chat_id=chat_id, text=self.text, parse_mode=self.parse_mode,
                                                      reply_markup=self.reply_markup, message_id=update_msg_id)
                if isinstance(new_msg, bool) and new_msg == True:
                    new_msg = await bot.send_message(chat_id=chat_id, text=self.text, parse_mode=self.parse_mode,
                                                     reply_markup=self.reply_markup)
                    bot_logger.debug("The message cannot be edited. A new message has been sent.")

            elif self.view_type == ViewType.TEXT:
                new_msg = await bot.send_message(chat_id=chat_id, text=self.text, parse_mode=self.parse_mode,
                                                 reply_markup=self.reply_markup)

            else:
                raise ValueError(f"The view cannot be displayed. Incorrect view type ({self.view_type}).")

            return new_msg
        except TelegramAPIError as e:
            bot_logger.error(e)
            raise
