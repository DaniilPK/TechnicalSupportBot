from aiogram import Bot
from aiogram.types import ChatMemberUpdated


async def chat_add_handler(event: ChatMemberUpdated, bot: Bot):
    await bot.leave_chat(event.chat.id)
    # Выход при давлении в чат айди которого не совпадает с config.TgBot.chat_id
