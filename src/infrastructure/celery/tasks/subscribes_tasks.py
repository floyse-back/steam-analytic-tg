from src.shared.depends import get_subscribes_service
from src.shared.subscribe_types import SUBSCRIBES_TYPE_DATA_REVERSE
from ..celery_app import app
from ..db_connect import get_db
from ..subscribes_styling.subscribe_style_text import SubscribeStyleText
from ...logging.logger import Logger
from ...telegram.telegram_notifier import TelegramNotifier
import asyncio

subscribe_service = get_subscribes_service()
subscribes_style_text = SubscribeStyleText()
logger = Logger(name="infrastructure.celery.worker",file_path="infrastructure")

@app.task
def subscribe_provide_wishlist():
    pass



@app.task
def send_notification_sub(sub_type:str,data:dict):
    sub_type_int = SUBSCRIBES_TYPE_DATA_REVERSE.get(f"{sub_type}",{"type_id":-1}).get("type_id")
    if sub_type_int==-1:
        raise ValueError(f"{sub_type}")
    session = next(get_db())
    telegram_ids = subscribe_service.get_user_id_by_subscribes_type(sub_type_int,session)
    if telegram_ids is None:
        return False
    telegram_notifier = TelegramNotifier(logger=logger)
    logger.info(f"Subscribes_tasks: Data Telegram Notifier:",data)
    text = str(data)[0:1500]
    asyncio.run(telegram_notifier.notify_users_message_sub(telegram_user_id=telegram_ids,text=text))

@app.task
def send_notification_from_wishlist(sub_type:str):
    pass