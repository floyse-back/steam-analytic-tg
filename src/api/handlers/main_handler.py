from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from src.api.keyboards import main_keyboards as main_keyboards
from src.application.services.users_service import UsersService
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.shared.config import start_message, MainMenu, help_config

router = Router()

users_service = UsersService(
    users_repository=UsersRepository(),
)

@router.message(CommandStart())
async def start(message: Message):
    await message.delete()
    await users_service.start_register_user(message.from_user.id)
    return await message.answer(f"{start_message}", parse_mode=ParseMode.MARKDOWN,reply_markup=main_keyboards.start_keyboard)


@router.message(lambda message: message.text == f"{MainMenu.help}")
async def help(message: Message):
    await message.delete()
    return await message.answer(help_config.get(f"help"),parse_mode=ParseMode.MARKDOWN,reply_markup=main_keyboards.help_inline_keyboard)


@router.callback_query(F.data=="help_back")
async def help_callback(callback_query: CallbackQuery):
    await callback_query.answer()
    return await callback_query.message.edit_text(help_config.get(f"help"),parse_mode=ParseMode.MARKDOWN,reply_markup=main_keyboards.help_inline_keyboard)
