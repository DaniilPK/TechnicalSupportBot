from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update


class ConfigChatSupportIDMiddleware(BaseMiddleware):
    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        data['chat_id'] = self.chat_id
        return await handler(event, data)