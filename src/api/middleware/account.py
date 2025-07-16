from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.api.keyboards.users.users_keyboards import profile_cancel_inline_keyboard_main
from src.api.presentation.users_style_text import UsersStyleText
from src.api.utils.state import ProfileSteamName
from src.application.services.users_service import UsersService
from src.infrastructure.db.database import get_async_db


async def user_get_or_none(state:FSMContext,telegram_id,message:Message,users_service:UsersService,style_text=UsersStyleText()):
    async for session in get_async_db():
        answer = await users_service.get_profile_user(telegram_id=telegram_id,session=session,account=False)
    if answer is None or answer is False:
        await state.update_data()
        await state.set_state(ProfileSteamName.profile)
        await message.delete()
        await message.answer(f"{style_text.message_no_steam_id(username=message.from_user.username)}",
                             parse_mode=ParseMode.HTML, reply_markup=profile_cancel_inline_keyboard_main)
        return None
    return True
