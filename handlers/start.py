from aiogram import types
import html

from language.translator import LocalizedTranslator


async def start(message: types.Message, translator: LocalizedTranslator):
    await message.answer(translator.get('start', user=html.escape(message.from_user.full_name)))


async def help_handler(message: types.Message, translator: LocalizedTranslator):
    await message.answer(translator.get('help'))
