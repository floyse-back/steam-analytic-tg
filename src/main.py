from src.infrastructure.logging.logger import logger
from src.shared.config import TELEGRAM_API_TOKEN
from aiogram import Bot, Dispatcher

from src.api.handlers.user_handlers import router as user_router
from src.api.handlers.steam_handlers import router as steam_router
from src.api.handlers.player_handlers import router as player_router
from src.api.handlers.subscribe_handler import router as subscribe_router
from src.api.handlers.main_handler import router as main_router
from src.api.handlers.callback.steam_callback import router as steam_callback_router

import asyncio

dp = Dispatcher()

#Збирання всіх Routers
dp.include_routers(user_router,
                   steam_router,steam_callback_router,
                   player_router,
                   subscribe_router,
                   main_router)


async def main():
    bot = Bot(token=TELEGRAM_API_TOKEN)
    logger.info("Start Telegram Bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
