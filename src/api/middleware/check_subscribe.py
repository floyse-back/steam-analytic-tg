from typing import Dict, Any, Callable

from aiogram import BaseMiddleware
from aiogram.enums import ParseMode
from aiogram.types import TelegramObject, ChatMemberLeft, ChatMemberBanned, Message

from src.api.middleware.keyboards import check_subscribe
from src.api.presentation.main_style_text import MainStyleText
from src.shared.config import CHAT_ID, CHANNEL_URL


class CheckSubscribeMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject,Dict[str,Any]], bool],
                       event: Message,
                       data: Dict[str,Any]
                       ):
        checker = await event.bot.get_chat_member(chat_id=CHAT_ID, user_id=event.from_user.id)
        if isinstance(checker, (ChatMemberLeft, ChatMemberBanned)):
            response = MainStyleText().subscribe_channel(channel_url=CHANNEL_URL)
            result = await event.bot.send_message(chat_id=event.chat.id, text=response,parse_mode=ParseMode.HTML,reply_markup=check_subscribe)
        else:
            result = await handler(event, data)

        return result