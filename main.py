import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllChatAdministrators, \
    BotCommandScopeAllGroupChats

from DB import create_session_pool
from config import load_config
from handlers import router_messages
from language.translator import Translator

from middlewares import ConfigDatabasePoolMiddleware,ConfigChatSupportIDMiddleware,\
    ThrottlingMiddleware
from middlewares.translator import TranslatorMiddleware

logger = logging.getLogger(__name__)


def register_global_middlewares(dp: Dispatcher, session, chat_id):
    dp.message.outer_middleware.register(ConfigDatabasePoolMiddleware(session))
    dp.update.outer_middleware.register(ConfigChatSupportIDMiddleware(chat_id))
    dp.message.middleware.register(ThrottlingMiddleware())
    dp.message.middleware.register(TranslatorMiddleware())


bot_commands = (
    ('help', 'Помощь', 'help'),
)
commands_for_bot = []

bot_commands_group = (
    ('ban', 'Блокировка (нет отвечать, параметр -m )'),
    ('unban', 'Разблокировка (нет отвечать, параметр -m )'),
)
commands_for_bot_group = []


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

    for cmd in bot_commands: commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot,scope=BotCommandScopeAllPrivateChats())

    for cmd in bot_commands_group: commands_for_bot_group.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot_group,scope=BotCommandScopeAllGroupChats())

    register_global_middlewares(dp, await create_session_pool(config.db,False), config.tg_bot.chat_id)

    router_messages(dp)

    await dp.start_polling(bot,translator=Translator())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        logger.error("Бот був вимкнений!")
