from copy import copy
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from language.translator import Translator


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        new_data = copy(data)
        traslator: Translator = data['translator']
        new_data['translator'] = traslator(language=event.from_user.language_code)
        return await handler(event, new_data)