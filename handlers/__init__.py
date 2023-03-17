from aiogram import Router, F
from aiogram.filters import CommandStart, BaseFilter, IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import Message

import config
from handlers.addingNewChat import chat_add_handler
from handlers.start import start
from handlers.message import reply_messages, reply_messages_private


class ChatIdFilter(BaseFilter):
    def __init__(self,param):
        self.param = param

    async def __call__(self, event, chat_id) -> bool:
        if self.param:
            return event.chat.id == chat_id
        else:
            return event.chat.id != chat_id


class IsReplyFilter(BaseFilter):
    async def __call__(self, msg: Message):
        return True if msg.reply_to_message else False


def router_messages(router: Router):
    router.message.register(start,CommandStart(),F.chat.type == 'private')
    router.message.register(reply_messages_private,F.chat.type == 'private')
    router.message.register(reply_messages,ChatIdFilter(True),IsReplyFilter())

    router.my_chat_member.register(chat_add_handler,ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> IS_MEMBER
    ),ChatIdFilter(False))