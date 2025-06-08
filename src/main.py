from aiogram.enums import ParseMode

import src.api.keyboards.main_keyboards as main_keyboards
from src.infrastructure.logging.logger import logger
from src.shared.config import TELEGRAM_API_TOKEN,help_config,start_message
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from src.api.handlers.user_handlers import router as user_router
from src.api.handlers.steam_handlers import router as steam_router
from src.api.handlers.player_handlers import router as player_router
from src.api.handlers.subscribe_handler import router as subscribe_router

import asyncio

dp = Dispatcher()

#Збирання всіх Routers
dp.include_routers(user_router,steam_router,player_router,subscribe_router)

@dp.message(CommandStart())
async def start(message: Message):
    await message.delete()
    return await message.answer(f"{start_message}", parse_mode=ParseMode.MARKDOWN,reply_markup=main_keyboards.start_keyboard)



@dp.message(lambda message: message.text == "Help")
async def help(message: Message):
    await message.delete()
    return await message.answer(help_config.get(f"help"),parse_mode=ParseMode.MARKDOWN,reply_markup=main_keyboards.help_inline_keyboard)

@dp.callback_query(F.data=="help_back")
async def help_callback(callback_query: CallbackQuery):
    await callback_query.answer()
    return await callback_query.message.edit_text(help_config.get(f"help"),parse_mode=ParseMode.MARKDOWN,reply_markup=main_keyboards.help_inline_keyboard)



async def main():
    bot = Bot(token=TELEGRAM_API_TOKEN)
    logger.info("Start Telegram Bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
