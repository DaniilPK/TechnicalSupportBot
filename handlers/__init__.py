from aiogram import Router, F
from aiogram.filters import CommandStart, BaseFilter, IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, Command
from aiogram.types import Message

from handlers.addingNewChat import chat_add_handler
from handlers.message import reply_messages, reply_messages_private, ban_user, unban_user
from handlers.start import start, help_handler


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
    router.message.register(help_handler, Command(commands=['help']), F.chat.type == 'private')
    router.message.register(ban_user,Command(commands=['ban']),ChatIdFilter(True),IsReplyFilter())
    router.message.register(unban_user,Command(commands=['unban']),ChatIdFilter(True),IsReplyFilter())

    router.message.register(reply_messages_private,F.chat.type == 'private')
    router.message.register(reply_messages,ChatIdFilter(True),IsReplyFilter())

    router.my_chat_member.register(chat_add_handler,ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> IS_MEMBER
    ),ChatIdFilter(False),F.chat_type.in_({"group", "supergroup"}))