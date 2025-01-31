import asyncio
from asyncio import CancelledError

from src.di.app_container import di
from src.loggers import bot_logger


async def main():
    bot = di.bot.vocab_bot()
    session_manager = di.data.session_manager()
    try:
        await session_manager.test_connection()
        await bot.run()
    except CancelledError:
        pass
    except Exception as e:
        bot_logger.exception(e)
    finally:
        await session_manager.disconnect()



if __name__ == '__main__':
    asyncio.run(main())
