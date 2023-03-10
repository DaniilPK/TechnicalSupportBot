from aiogram import types
import html


async def start(message: types.Message):
    await message.answer(f'Здравствуйте <b>{html.escape(message.from_user.full_name)}</b>.\n\n⏰ Поддержка работает с <b>12:00 до 22:00</b>'
                         '\nНапишите ваш вопрос и мы ответим '
                         'Вам в ближайшее время.')
