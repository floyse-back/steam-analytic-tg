import asyncio
from typing import Union, List, Optional

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest
from aiogram.types import ChatMemberLeft, ChatMemberBanned

from src.api.keyboards.main_keyboards import start_keyboard
from src.domain.logger import ILogger
from src.shared.config import TELEGRAM_API_TOKEN, CHAT_ID


class TelegramNotifier:
    def __init__(self,logger:ILogger):
        self.bot = Bot(token=TELEGRAM_API_TOKEN)
        self.logger = logger

    async def check_user_leave_group(self,user_id:int):
        checker = await self.bot.get_chat_member(chat_id=CHAT_ID, user_id=user_id)
        if isinstance(checker, (ChatMemberLeft, ChatMemberBanned)):
            return False
        await asyncio.sleep(0.25)
        return True

    async def __send_message_retry(self,func,counter:int,*args,**kwargs):
        if counter % 30 == 0:
            self.logger.debug("NotifyUsersMessageSub: Rate limit reached, sleeping for 1s...")
            await asyncio.sleep(1)
        retry = 0
        while retry < 3:
            try:
                self.logger.info(f"NotifyUsersMessageSub: Notifying user")
                await func(*args,**kwargs)
                return True
            except TelegramRetryAfter as RateLimit:
                await asyncio.sleep(2)
                self.logger.warning("RateLimit WARNING %s",RateLimit)
            except TelegramBadRequest as BadRequest:
                self.logger.warning("BadRequest WARNING %s",BadRequest.message)
                if BadRequest.message.find("failed to get HTTP URL content"):
                    return "Bad Request"
                return None
            except Exception as e:
                retry += 1
                await asyncio.sleep(0.25)
                self.logger.warning(f"Retry {retry}/3 failed: {e}", exc_info=True)

        return False



    async def send_news_message(self,text:str,chat_id:Union[int,str],video_format:bool=False,video_url:Optional[str]=None,img_url:Optional[str]=None):
        if video_format:
            data = await self.__send_message_retry(func=self.bot.send_video,counter=1,chat_id=chat_id,caption=text,video=video_url,parse_mode=ParseMode.HTML)
            if data == "Bad Request":
                await self.send_news_message(text,chat_id=chat_id,img_url=img_url)
        elif img_url:
            data = await self.__send_message_retry(func=self.bot.send_photo,counter=1,chat_id=chat_id,caption=text,photo=img_url,parse_mode=ParseMode.HTML)
            if data == "Bad Request":
                await self.send_news_message(text, chat_id=chat_id)
        else:
            await self.__send_message_retry(func=self.bot.send_message,counter=1,chat_id=chat_id,text=text,parse_mode=ParseMode.HTML)

    async def notify_users_message_sub(self,telegram_user_id:List[int],text:str,image:Optional[str]=None):
        counter = 1
        reply_board = start_keyboard
        for user_id in telegram_user_id:
            try:
                checker = await self.bot.get_chat_member(chat_id=CHAT_ID, user_id=user_id)
            except Exception as e:
                await asyncio.sleep(2)
                checker = None
                self.logger.warning("CheckUserSubscribe: WARNING %s",e)

            if isinstance(checker, (ChatMemberLeft, ChatMemberBanned)):
                continue
            elif image:
                success = await self.__send_message_retry(self.bot.send_photo,counter=counter,chat_id=user_id,caption=text,photo=image,parse_mode=ParseMode.HTML,reply_markup=reply_board)
            else:
                success = await self.__send_message_retry(self.bot.send_message,counter=counter,chat_id=user_id,text=text,parse_mode=ParseMode.HTML,reply_markup=reply_board)
            counter += 1
            if not success:
                self.logger.error(f"NotifyUsersMessageSub: Failed to notify user {user_id} after 3 retries.")

    async def send_wishlist_messages(self, users:dict[str,List[str]]):
        counter = 1
        for user_id, messages in users.items():
            for message in messages:
                await self.__send_message_retry(self.bot.send_message,chat_id=user_id,counter=counter,text=message,parse_mode=ParseMode.HTML)
                counter += 1