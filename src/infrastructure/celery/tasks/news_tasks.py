from typing import List, Union

from src.application.dto.steam_dto import transform_to_dto, GameFullModel, CalendarEventModel
from src.shared.config import CHAT_ID
from ..celery_app import app, run_async

from ..news_styling.news_style_text import NewsStyleText
from ...logging.logger import Logger
from ...telegram.telegram_notifier import TelegramNotifier

logger = Logger(name="api",file_path="celery_app")

@app.task
def news_send_message(type_news:str,data:List[dict]):
    telegram_notifier = TelegramNotifier(logger=logger)
    video_url=None
    video_format=None
    if type_news == "news_calendar_event_now":
        model = CalendarEventModel
    else:
        model = GameFullModel
    logger.debug("Last Data %s",data)
    new_data:List[Union[GameFullModel,CalendarEventModel]] = [transform_to_dto(model,i,model_dump=False) for i in data]
    if len(new_data) == 1:
        new_data:List[Union[GameFullModel,CalendarEventModel]] = new_data[0:1]
    if type_news.startswith("news_game_from_ganre"):
        video_url = f"{new_data[0].trailer_url}"
        new_data:dict = {
            "type_ganre":type_news.replace("news_game_from_ganre",""),
            "data":new_data
        }
        video_format = True if video_url else False
        type_news = "news_game_from_ganre"
    news_style_text = NewsStyleText()
    logger.info("New DATA: %s",new_data)
    message = news_style_text.dispatch_sync(type_news,new_data)
    logger.debug("Message: %s",message)
    run_async(telegram_notifier.send_news_message(text=message,chat_id=CHAT_ID,video_format=video_format,video_url=video_url))