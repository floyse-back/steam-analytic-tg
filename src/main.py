from src.infrastructure.db.database import get_async_db
from src.infrastructure.logging.logger import Logger
from src.infrastructure.logging.logger_conf import startup_logger_configure
from src.infrastructure.messages.consumer import consumer_news, consumer_subscribes
from src.shared.config import TELEGRAM_API_TOKEN
from aiogram import Bot, Dispatcher

from src.api.handlers.user_handlers import router as user_router
from src.api.handlers.steam_handlers import router as steam_router
from src.api.handlers.player_handlers import router as player_router
from src.api.handlers.subscribe_handler import router as subscribe_router
from src.api.handlers.main_handler import router as main_router

from src.api.handlers.callback.steam_callback import router as steam_callback_router
from src.api.handlers.callback.player_callback import router as player_callback_router
from src.api.handlers.callback.users_callback import router as user_callback_router
from src.api.handlers.callback.subscribe_callback import router as subscribe_callback_router
from src.api.handlers.callback.main_callback import router as main_callback_router

import asyncio

from src.startup import init_subscribe_types

dp = Dispatcher()

#Збирання всіх Routers
dp.include_routers(user_router,user_callback_router,
                   steam_router,steam_callback_router,
                   player_router,player_callback_router,
                   subscribe_router,subscribe_callback_router,
                   main_router,main_callback_router)


async def main():
    #Створення logger config and logger api.main
    startup_logger_configure()
    logger = Logger(name="api.main",file_path="api")
    #Створення
    async for session in get_async_db():
        await init_subscribe_types(session=session)
        break
    #Створення Слухачів
    asyncio.create_task(consumer_news())
    asyncio.create_task(consumer_subscribes())
    #
    bot = Bot(token=TELEGRAM_API_TOKEN)
    logger.info("Start Telegram Bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
