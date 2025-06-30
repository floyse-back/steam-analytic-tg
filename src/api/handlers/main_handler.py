from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.api.keyboards import main_keyboards as main_keyboards
from src.api.keyboards.main_keyboards import start_keyboard
from src.api.keyboards.users.users_keyboards import profile_cancel_inline_keyboard_main
from src.api.presentation.main_style_text import MainStyleText
from src.api.utils.state import ProfileSteamName
from src.application.services.users_service import UsersService
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import MainMenu, help_config

router = Router()

users_service = UsersService(
    users_repository=UsersRepository(),
    steam_client=SteamAnalyticsAPIClient(),
)

main_style_text = MainStyleText()

@router.message(CommandStart())
async def start(message: Message,state: FSMContext):
    await message.delete()
    if not await users_service.check_register_steam_id_user(message.from_user.id):
        await state.update_data()
        await state.set_state(ProfileSteamName.profile)
        await message.answer(f"{main_style_text.start_message_no_steam_id(username=message.from_user.username)}",parse_mode=ParseMode.HTML,reply_markup=profile_cancel_inline_keyboard_main)
    else:
        await message.answer(f"{main_style_text.start_message_with_steam_id(username=message.from_user.username)}",parse_mode=ParseMode.HTML,reply_markup=start_keyboard)


@router.message(lambda message: message.text == f"{MainMenu.help}")
async def help(message: Message):
    await message.delete()
    return await message.answer(help_config.get(f"help"),parse_mode=ParseMode.MARKDOWN,reply_markup=main_keyboards.help_inline_keyboard)


@router.callback_query(F.data=="help_back")
async def help_callback(callback_query: CallbackQuery):
    await callback_query.answer()
    return await callback_query.message.edit_text(help_config.get(f"help"),parse_mode=ParseMode.MARKDOWN,reply_markup=main_keyboards.help_inline_keyboard)
