from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from DB import search_or_create_user


class ConfigDatabasePoolMiddleware(BaseMiddleware):
    def __init__(self, session_pool) -> None:
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        async with self.session_pool() as session:
            if not await search_or_create_user(session, event.from_user.id):
                data['session'] = session
                return await handler(event, data)
            else:
                return

