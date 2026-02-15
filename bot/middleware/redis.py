from aiogram import BaseMiddleware
from redis.asyncio import Redis
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

class RedisMiddleware(BaseMiddleware):
    def __init__(
        self,
        redis: Redis
    ) -> None:
        self.redis = redis

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
            data['redis'] = self.redis
            return await handler(event, data)
