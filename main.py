import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from DB import create_session_pool
from config import BOT_TOKEN
from handlers import router_messages
from middlewares.config import ConfigDatabasePoolMiddleware

from config import DatabaseConfig

logger = logging.getLogger(__name__)


def register_global_middlewares(dp: Dispatcher, session):
    dp.update.outer_middleware.register(ConfigDatabasePoolMiddleware(session))


bot_commands = (
    ('start', 'Старт'),
)
commands_for_bot = []

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    storage = MemoryStorage()
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot)

    session_pool = await create_session_pool(DatabaseConfig)
    register_global_middlewares(dp, session_pool)

    router_messages(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот був вимкнений!")
