import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from DB import create_session_pool
from config import load_config
from handlers import router_messages

from middlewares import ConfigDatabasePoolMiddleware
from middlewares import ConfigChatSupportIDMiddleware

logger = logging.getLogger(__name__)


def register_global_middlewares(dp: Dispatcher, session, chat_id):
    dp.update.outer_middleware.register(ConfigDatabasePoolMiddleware(session))
    dp.message.outer_middleware.register(ConfigChatSupportIDMiddleware(chat_id))


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

    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot)

    register_global_middlewares(dp, await create_session_pool(config.db), config.tg_bot.chat_id)

    router_messages(dp)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот був вимкнений!")
