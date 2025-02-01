from aiogram.types import BotCommand

MY_CARD_GROUP = BotCommand(command='mycardgroups', description="Get the list of my card groups.")
NEW_CARD_GROUP = BotCommand(command='newcardgroup', description="Create the new card group.")

CANCEL = BotCommand(command='cancel', description="Cancel current action.")
