import html

from aiogram import types, Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import CommandObject
from sqlalchemy.ext.asyncio import AsyncSession

from DB.Message import newMessage, SearchMessage
from DB.Users import update_status


async def reply_messages(message: types.Message, bot: Bot, session: AsyncSession):
    userID = await SearchMessage(session, message.reply_to_message.message_id)
    if userID is None: return await message.reply('Пользователь не найден')
    try:
        if message.text:
            await bot.send_message(userID, message.text)
        elif message.photo:
            await bot.send_photo(userID, message.photo[-1].file_id, caption=message.caption)
        elif message.sticker:
            await bot.send_sticker(userID, message.sticker.file_id)
        elif message.animation:
            await bot.send_animation(userID, message.animation.file_id)
    except TelegramForbiddenError:
        await message.reply('Пользователь заблокировал бота')


async def reply_messages_private(message: types.Message, bot: Bot,chat_id, session: AsyncSession):
    mes = await bot.forward_message(chat_id, message.from_user.id, message.message_id)
    await newMessage(session, message.from_user.id, mes.message_id)


async def ban_user(message: types.Message, bot: Bot, session: AsyncSession,command: CommandObject):
    userID = await SearchMessage(session, message.reply_to_message.message_id)
    if userID is None:
        await message.reply('Пользователь не найден')
    await update_status(session,userID,'ban',True)

    try:
        us = await bot.get_chat_member(userID,userID)
        if command.args is not None:
            if command.args.find('-m'):
                await message.reply(f'OK. User <b>{html.escape(us.user.full_name)}</b> was banned')
        else:
            await message.reply(f'OK. User <b>{html.escape(us.user.full_name)}</b> was banned')
    except Exception as ex:
        print(ex)

async def unban_user(message: types.Message, bot: Bot, session: AsyncSession,command: CommandObject):
    userID = await SearchMessage(session, message.reply_to_message.message_id)
    if userID is None:
        await message.reply('Пользователь не найден')
    await update_status(session,userID,'ban',False)

    try:
        us = await bot.get_chat_member(userID,userID)
        if command.args is not None:
            if command.args.find('-m'):
                await message.reply(f'OK. User <b>{html.escape(us.user.full_name)}</b> was unbanned')
        else:
            await message.reply(f'OK. User <b>{html.escape(us.user.full_name)}</b> was unbanned')
    except Exception as ex:
        print(ex)

