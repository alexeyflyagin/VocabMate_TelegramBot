from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.loggers import service_logger


class SessionManager:

    def __init__(self, db_url: str):
        self._engine = create_async_engine(db_url)
        self._session_maker = async_sessionmaker(self._engine)

    @property
    def session(self) -> AsyncSession:
        return self._session_maker()

    async def test_connection(self):
        try:
            async with self.session as s:
                expected = 1
                result = await s.execute(text(f"SELECT {expected}"))
                if result.scalar() != expected:
                    raise ConnectionError('The connection to the database is established incorrectly.')
                service_logger.info('The connection to the database is established.')
        except Exception as e:
            service_logger.critical(e)
            raise

    async def disconnect(self):
        try:
            await self._engine.dispose()
        except Exception as e:
            service_logger.warn(e)
        service_logger.info('The connection to the database is closed.')
