from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from bot.core.config import config

redis_client = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    username=config.REDIS_USER,
    password=config.REDIS_USER_PASSWORD.get_secret_value() if config.REDIS_USER_PASSWORD else None
)

storage = RedisStorage(redis=redis_client)
