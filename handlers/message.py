import logging

from aiogram import types, Bot
from sqlalchemy.ext.asyncio import AsyncSession

from DB.Users import newMessage, SearchMessage
from config import chatID


async def messageReplyes(message: types.Message, bot: Bot, session: AsyncSession):
    logging.info(message)
    if message.chat.id == chatID:
        userID = await SearchMessage(session, message.reply_to_message.message_id)
        if message.text:
            await bot.send_message(userID, message.text)
        elif message.photo:
            await bot.send_photo(userID, message.photo[-1].file_id, caption=message.caption)
        elif message.sticker:
            await bot.send_sticker(userID, message.sticker.file_id)
        elif message.animation:
            await bot.send_animation(userID, message.animation.file_id)
    else:
        mes = await bot.forward_message(chatID, message.from_user.id, message.message_id)
        await newMessage(session, message.from_user.id, message.message_id, mes.message_id)

    await session.close()
