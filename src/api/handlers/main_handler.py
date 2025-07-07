from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.api.handlers.callback.message_utils import user_register_utils
from src.api.keyboards.main_keyboards import start_keyboard
from src.api.keyboards.users.users_keyboards import profile_cancel_inline_keyboard_main
from src.api.presentation.main_style_text import MainStyleText
from src.application.services.users_service import UsersService
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.infrastructure.db.repository.wishlist_repository import WishlistRepository
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient

router = Router()

users_service = UsersService(
    users_repository=UsersRepository(),
    steam_client=SteamAnalyticsAPIClient(),
    wishlist_repository=WishlistRepository(),
)

main_style_text = MainStyleText()

@router.message(CommandStart())
async def start(message: Message,state: FSMContext):
    if await user_register_utils(message=message,state=state,users_service=users_service,main_style_text=main_style_text,reply_markup=profile_cancel_inline_keyboard_main):
        return None
    else:
        logger.debug("Steam Appid From Steam Service,%s",message.from_user.id)
        logger.debug("Chat ID %s",message.chat.id)
        await message.answer(f"{main_style_text.start_message_with_steam_id(username=message.from_user.username)}",parse_mode=ParseMode.HTML,reply_markup=start_keyboard)