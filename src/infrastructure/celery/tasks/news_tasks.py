from typing import List

from src.application.dto.steam_dto import transform_to_dto, GameFullModel, CalendarEventModel
from src.shared.config import CHAT_ID
from ..celery_app import app
import asyncio

from ..news_styling.news_style_text import NewsStyleText
from ...logging.logger import Logger
from ...telegram.telegram_notifier import TelegramNotifier

logger = Logger(name="api",file_path="celery_app")

@app.task
def news_send_message(type_news:str,data:List[dict]):
    telegram_notifier = TelegramNotifier(logger=logger)

    if type_news == "news_calendar_event_now":
        model = CalendarEventModel
    else:
        model = GameFullModel
    new_data = [transform_to_dto(model,i,model_dump=False) for i in data]
    if len(new_data) == 1:
        new_data = new_data[0:1]
    news_style_text = NewsStyleText()
    logger.info("New DATA: %s",new_data)
    message = news_style_text.dispatch_sync(type_news,new_data)
    logger.debug("Message: %s",message)
    asyncio.run(telegram_notifier.send_news_message(text=message,chat_id=CHAT_ID))