from aiogram import Dispatcher, Bot, Router
from aiogram.fsm.storage.base import BaseStorage

from src.loggers import bot_logger


class VocabMateBot:

    def __init__(
            self,
            token: str,
            storage: BaseStorage | None = None,
            routers: list[Router] | None = None,
    ):
        self.bot = Bot(token)
        self.dp = Dispatcher(storage=storage)
        self._register_routers(routers)

        self.dp.startup.register(self._startup)
        self.dp.shutdown.register(self._shutdown)

    def _register_routers(self, routers: list[Router] | None):
        if not routers:
            return
        self.dp.include_routers(*routers)

    async def _startup(self):
        bot_name = await self.bot.get_my_name()
        bot_logger.info(f'{bot_name.name} bot is started.')

    async def _shutdown(self):
        bot_name = await self.bot.get_my_name()
        bot_logger.info(f'{bot_name.name} bot is ended.')

    async def run(self):
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)
