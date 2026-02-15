from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable

class DatabaseMiddleware(BaseMiddleware):
    def __init__(
        self,
        session: async_sessionmaker[AsyncSession]
    ) -> None:
        self.session = session

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
            async with self.session() as session:
                data['session'] = session
                return await handler(event, data)
