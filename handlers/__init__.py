from aiogram import Router
from aiogram.filters import CommandStart

from handlers.start import start
from handlers.message import messageReplyes


def router_messages(router: Router):
    router.message.register(start,CommandStart())
    router.message.register(messageReplyes)