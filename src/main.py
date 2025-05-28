from src.shared.config import TELEGRAM_API_TOKEN
from aiogram import Bot,Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

import asyncio

dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"{message.from_user.full_name}")


async def main():
    bot = Bot(token=TELEGRAM_API_TOKEN)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
