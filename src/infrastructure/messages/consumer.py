import json

import aio_pika
import aio_pika.abc

from src.infrastructure.celery.tasks.news_tasks import news_send_message
from src.infrastructure.celery.tasks.subscribes_tasks import send_notification_sub, subscribe_provide_wishlist_batches, \
    send_notification_from_wishlist, update_notification_from_wishlist_base
from src.infrastructure.logging.logger import Logger
from src.shared.config import RABBITMQ_CONNECTION
from celery import chain

logger = Logger(name="rabbitmq.consumer",file_path="rabbitmq")

async def connect_aio():
    return await aio_pika.connect_robust(
        RABBITMQ_CONNECTION
    )

async def consumer_news():
    connection = await connect_aio()

    async with connection:
        queue_name = "news_queue"

        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                async with message.process():
                    logger.debug("Data From RABBITMQ %s",message.body)
                    body = json.loads(message.body.decode())
                    data = body.get("data")
                    type_news = body.get("type_news")
                    news_send_message.delay(type_news,data)
                    if queue.name in message.body.decode():
                        break

async def consumer_subscribes():
    connection = await connect_aio()

    async with connection:
        queue_name = "subscribe_queue"
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iterator:
            async for message in queue_iterator:
                async with message.process():
                    logger.debug("Data From RABBITMQ Channel Subscribe_queue %s",message.body)
                    body = json.loads(message.body.decode())
                    data = body.get("body")
                    if body.get("type") == "update_steam_games" and body.get("status",False):
                        logger.info("Send_and_update_wishlist_games")
                        subscribe_provide_wishlist_batches.delay()
                    elif body.get("type") == "send_and_update_wishlist_games" and body.get("status",False):
                        logger.info("Send_and_update_wishlist_games")
                        chain(
                            send_notification_from_wishlist.s(body.get("data")),
                            update_notification_from_wishlist_base.s()
                        ).delay()
                        logger.info("Send_and_update_wishlist_games %s",body.get("data"))
                    else:
                        type_sub = body.get("sub_type")
                        send_notification_sub.delay(type_sub,data)
                        if queue.name in message.body.decode():
                            break
