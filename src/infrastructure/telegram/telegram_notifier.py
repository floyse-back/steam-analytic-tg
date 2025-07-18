from typing import Union, List

from aiogram import Bot
from aiogram.enums import ParseMode

from src.domain.logger import ILogger
from src.shared.config import TELEGRAM_API_TOKEN

class TelegramNotifier:
    def __init__(self,logger:ILogger):
        self.bot = Bot(token=TELEGRAM_API_TOKEN)
        self.logger = logger

    async def send_news_message(self,text:str,chat_id:Union[int,str]):
        try:
            await self.bot.send_message(chat_id=chat_id,text=text,parse_mode=ParseMode.HTML)
        except Exception as e:
            self.logger.debug(f"Error: {e}", exc_info=True)

    async def notify_users_message_sub(self,telegram_user_id:List[int],text:str):
        for index in telegram_user_id:
            try:
                self.logger.info(f"Notifying user {index}")
                await self.bot.send_message(chat_id=index,text=text,parse_mode=ParseMode.HTML)
            except Exception as e:
                self.logger.debug(f"Error: {e}",exc_info=True)