from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.api.handlers.callback.message_utils import user_register_utils
from src.api.keyboards.main_keyboards import start_keyboard
from src.api.keyboards.users.users_keyboards import profile_cancel_inline_keyboard_main
from src.api.presentation.main_style_text import MainStyleText
from src.infrastructure.logging.logger import Logger
from src.shared.depends import get_users_service

router = Router()

users_service = get_users_service()

main_style_text = MainStyleText()
logger = Logger(name = "api.main_handler",file_path="api")

@router.message(CommandStart())
async def start(message: Message,state: FSMContext):
    if await user_register_utils(message=message,state=state,users_service=users_service,main_style_text=main_style_text,reply_markup=profile_cancel_inline_keyboard_main):
        return None
    else:
        logger.debug("Start_handler: Steam Appid From Steam Service,%s",message.from_user.id)
        logger.debug("Start_handler: Chat ID %s",message.chat.id)
        logger.info("Start_handler: Chat ID %s",message.chat.id)
        await message.answer(f"{main_style_text.start_message_with_steam_id(username=message.from_user.username)}",parse_mode=ParseMode.HTML,reply_markup=start_keyboard)