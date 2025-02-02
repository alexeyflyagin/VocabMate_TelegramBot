from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from src.bot.exceptions import InvalidTrustedUserId
from src.bot.views.custom.mappers.card_group import vd__card_group_page_list__from__get_card_groups_response, \
    vd__card_page_list_of_card_group__from__get_cards_of_card_group_response
from src.bot.views.custom.view.card_group import view__card_group_list, view__card_list_of_card_group
from src.loggers import bot_logger
from src.services.models.card_group import GetCardGroupsResponse
from src.services.models.card_item import GetCardsOfCardGroupResponse

TRUSTED_USER_ID: int | None = None


def check_user_id(msg: Message):
    if TRUSTED_USER_ID is None:
        bot_logger.critical('The TRUSTED_USER_ID was not found.')
    if TRUSTED_USER_ID != msg.from_user.id:
        raise InvalidTrustedUserId(msg.from_user.id)
    return


async def show_card_group_list(msg: Message, groups_data: GetCardGroupsResponse, is_update: bool = False):
    if not isinstance(msg, Message) or not isinstance(groups_data, GetCardGroupsResponse) \
            or not isinstance(is_update, int):
        raise ValueError(
            f"Invalid arg types: msg={type(msg)}, groups_data={type(groups_data)}, is_update={type(is_update)}")

    vd = vd__card_group_page_list__from__get_card_groups_response(groups_data)
    update_msg_id = msg.message_id if is_update else None
    try:
        await view__card_group_list(vd).show_view(bot=msg.bot, chat_id=msg.chat.id, update_msg_id=update_msg_id)
    except TelegramBadRequest as e:
        if "message is not modified" not in e.message:
            raise
        pass


async def show_card_list_of_card_group(msg: Message, groups_data: GetCardsOfCardGroupResponse, is_update: bool = False):
    if not isinstance(msg, Message) or not isinstance(groups_data, GetCardsOfCardGroupResponse) \
            or not isinstance(is_update, int):
        raise ValueError(
            f"Invalid arg types: msg={type(msg)}, groups_data={type(groups_data)}, is_update={type(is_update)}")

    vd = vd__card_page_list_of_card_group__from__get_cards_of_card_group_response(groups_data)
    update_msg_id = msg.message_id if is_update else None
    try:
        await view__card_list_of_card_group(vd).show_view(bot=msg.bot, chat_id=msg.chat.id, update_msg_id=update_msg_id)
    except TelegramBadRequest as e:
        if "message is not modified" not in e.message:
            raise
        pass
