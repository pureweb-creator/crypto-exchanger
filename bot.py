import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.core import config, redis_loader
from bot.handlers import start, exchange
from bot.tasks.exchange import udpate_data

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.config.BOT_TOKEN.get_secret_value())

    dp = Dispatcher(storage = redis_loader.storage)

    dp.include_routers(start.router, exchange.router)

    @dp.startup()
    async def on_startup(bot: Bot):
        asyncio.create_task(udpate_data())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
