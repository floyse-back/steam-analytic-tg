from typing import List

from src.api.presentation.subscribe_style_text import SubscribeStyleText
from src.shared.depends import get_subscribes_service
from src.shared.static_url.images import images_urls
from src.shared.subscribe_types import SUBSCRIBES_TYPE_DATA_REVERSE
from ..celery_app import app, run_async
from ..db_connect import get_db
from ...logging.logger import Logger
from ...messages.provider import EventProvider
from ...telegram.telegram_notifier import TelegramNotifier

subscribe_service = get_subscribes_service()
subscribes_style_text = SubscribeStyleText(
    logger=Logger(name="api.subscribe_style_text", file_path="api")
)
logger = Logger(name="infrastructure.celery.worker",file_path="infrastructure")
telegram_notifier = TelegramNotifier(logger=logger)

@app.task
def subscribe_provide_wishlist_batches():
    session = next(get_db())
    event_provider = EventProvider()
    for data in subscribe_service.update_push_wishlist_games(session=session):
        logger.info(f"Subscribing {data}")
        run_async(event_provider.send_message(data=data,queue="sub_appids"))
        logger.info(f"Send Message")


@app.task
def send_notification_sub(sub_type:str,data:dict):
    sub_type_int = SUBSCRIBES_TYPE_DATA_REVERSE.get(f"{sub_type}",{"type_id":-1}).get("type_id")
    if sub_type_int==-1:
        raise ValueError(f"{sub_type}")
    session = next(get_db())
    logger.info(f"Data {data}")
    if data is None or len(data) == 0:
        logger.info(f"Data is None {data}")
        return None
    telegram_ids = subscribe_service.get_user_id_by_subscribes_type(sub_type_int,session)
    if telegram_ids is None:
        return False
    logger.info(f"Data {data}")
    text = subscribes_style_text.dispatcher(f"{sub_type}",data=data)
    run_async(telegram_notifier.notify_users_message_sub(telegram_user_id=telegram_ids,text=text,image = images_urls.get(f"{sub_type}")))

@app.task
def send_notification_from_wishlist(data:List[dict]):
    logger.info("ABOBA: Start task")
    session=next(get_db())
    new_data = subscribe_service.get_changed_games(session=session,data=data)
    users_text_dict:dict[str,List[str]] = subscribes_style_text.generate_wishlist_subscribe(data=new_data)
    logger.info(f"users_text_dict: {users_text_dict}")
    run_async(telegram_notifier.send_wishlist_messages(users=users_text_dict))
    logger.info(f"SendNotificationFromWishlist: {new_data}")


@app.task
def update_notification_from_wishlist_base(data:List[dict]):
    logger.info(f"Data {data}")
    session=next(get_db())
    subscribe_service.upsert_games_wishlist(data=data,session=session)
