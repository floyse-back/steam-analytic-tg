from typing import List

from src.api.presentation.subscribe_style_text import SubscribeStyleText
from src.shared.depends import get_subscribes_service
from src.shared.subscribe_types import SUBSCRIBES_TYPE_DATA_REVERSE
from ..celery_app import app
from ..db_connect import get_db
from ...logging.logger import Logger
from ...messages.provider import EventProvider
from ...telegram.telegram_notifier import TelegramNotifier
import asyncio

subscribe_service = get_subscribes_service()
subscribes_style_text = SubscribeStyleText()
logger = Logger(name="infrastructure.celery.worker",file_path="infrastructure")

@app.task
def subscribe_provide_wishlist_batches():
    session = next(get_db())
    event_provider = EventProvider()
    for data in subscribe_service.update_push_wishlist_games(session=session):
        logger.info(f"Subscribing {data}")
        asyncio.run(event_provider.send_message(data=data,queue="sub_appids"))
        logger.info(f"Send Message")


@app.task
def send_notification_sub(sub_type:str,data:dict):
    sub_type_int = SUBSCRIBES_TYPE_DATA_REVERSE.get(f"{sub_type}",{"type_id":-1}).get("type_id")
    logger.info(f"Subscribe Type: {sub_type_int}")
    if sub_type_int==-1:
        raise ValueError(f"{sub_type}")
    session = next(get_db())
    logger.info(f"Data {data}")
    telegram_ids = subscribe_service.get_user_id_by_subscribes_type(sub_type_int,session)
    if telegram_ids is None:
        return False
    logger.info("Telegram ids %s", telegram_ids)
    telegram_notifier = TelegramNotifier(logger=logger)
    logger.info(f"Data {data}")
    #Text Generator
    text = subscribes_style_text.dispatcher(f"{sub_type}",data)
    #Text Generator
    logger.info(f"Text TEXT {text}")
    asyncio.run(telegram_notifier.notify_users_message_sub(telegram_user_id=telegram_ids,text=text))

@app.task
def send_notification_from_wishlist(data):
    logger.info("UPDATE_NOTIFICATION_FROM_WISHLIST_BASE: Start task",)
    session = next(get_db())
    new_data = subscribe_service.get_changed_games(session=session,data=data)
    logger.info(f"SendNotificationFromWishlist: {new_data}")
    return data

@app.task
def update_notification_from_wishlist_base(data:List[dict]):
    logger.info(f"Data {data}")
    session = next(get_db())
    subscribe_service.upsert_games_wishlist(data=data,session=session)
