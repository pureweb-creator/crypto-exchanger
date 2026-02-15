import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from bot.core.config import Settings
from bot.handlers import start, exchange
from bot.tasks.exchange import udpate_data
from bot.middleware.database import DatabaseMiddleware
from bot.middleware.redis import RedisMiddleware

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from redis.asyncio import Redis

async def main():
    logging.basicConfig(level=logging.INFO)

    settings = Settings()

    engine = create_async_engine(url=settings.POSTGRES_DB_URL, echo=True)

    session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    r = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        username=settings.REDIS_USER,
        password=settings.REDIS_USER_PASSWORD.get_secret_value() if settings.REDIS_USER_PASSWORD else None
    )

    storage = RedisStorage(r)

    bot = Bot(token=settings.BOT_TOKEN.get_secret_value())
    dp = Dispatcher(storage=storage)
    dp.update.middleware(DatabaseMiddleware(session=session))
    dp.update.middleware(RedisMiddleware(redis=r))
    dp.include_routers(start.router, exchange.router)

    @dp.startup()
    async def on_startup():
        asyncio.create_task(udpate_data(r))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
