from src.shared.config import TELEGRAM_API_TOKEN,help_config,start_message
from aiogram import Bot,Dispatcher
from aiogram.filters import CommandStart,Command
from aiogram.types import Message


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
    await message.answer(f"{start_message}", parse_mode="Markdown")



@dp.message(Command(commands=["help"]))
async def help(message: Message):
    await message.answer(help_config.get(f"help"))
    await message.delete()


async def main():
    bot = Bot(token=TELEGRAM_API_TOKEN)
    print("StartUp")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
