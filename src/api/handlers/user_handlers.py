from typing import Optional

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from src.api.handlers.callback.users_callback import users_style_text
from src.api.keyboards.main_keyboards import start_keyboard
from src.api.keyboards.users.users_keyboards import create_user_inline_keyboard, profile_cancel_inline_keyboard_main, \
    back_to_profile_main
from src.api.utils.state import ProfileSteamName, ChangeSteamName
from src.application.services.users_service import UsersService
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import MainMenu, user_message_menu

router = Router(name=__name__)

users_service = UsersService(
    users_repository=UsersRepository(),
    steam_client=SteamAnalyticsAPIClient(),
)


@router.message(Command("user"))
async def user_help(message: Message):
    await message.delete()
    return await message.answer(users_service.user_help(),parse_mode=ParseMode.MARKDOWN)

@router.message(lambda message: message.text == f"{MainMenu.profile}")
async def user_reply(message: Message):
    await message.delete()
    await message.answer(text=f"{user_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_user_inline_keyboard())

@router.message(ProfileSteamName.profile)
async def user_profile(message:Message, state: FSMContext):
    steam_appid:Optional[str] = message.text
    logger.debug(f"User profile %s",steam_appid)
    bool_answer:bool = await users_service.update_or_register_user(user_id=message.from_user.id,steam_user=steam_appid)
    await state.clear()
    if bool_answer:
        await message.answer(f"<b>Ви успішно зберегли SteamAppid:</b><code>{steam_appid}</code>!!",parse_mode=ParseMode.HTML,reply_markup=start_keyboard)
    else:
        await state.set_state(ProfileSteamName.profile)
        await message.answer(f"<b>Нажаль мені не вдалося знайти ваш SteamAppid <s>{steam_appid}</s></b>\n"
                             f"Спробуйте ще раз!!",parse_mode=ParseMode.HTML)

@router.message(ChangeSteamName.steam_appid_new)
async def user_profile_change(message:Message, state:FSMContext):
    steam_appid:Optional[str] = message.text
    logger.debug(f"User profile %s",steam_appid)
    steam_appid_complete = await users_service.update_or_register_user(user_id=message.from_user.id,steam_user=steam_appid)
    state_data = await state.get_data()
    if state_data.get("last_bot_message_id") is not None:
        try:
            await message.bot.delete_message(message_id=state_data["last_bot_message_id"],chat_id=message.chat.id)
        except Exception as ex:
            logger.critical("Exception: %s",ex)
    await state.clear()
    if not steam_appid_complete:
        await message.answer(f"{users_style_text.message_incorrect_steam_id(steam_appid=steam_appid)}",parse_mode=ParseMode.HTML,reply_markup=profile_cancel_inline_keyboard_main)
        await state.clear()
        await state.update_data(last_bot_message_id=message.message_id)
        await state.set_state(ChangeSteamName.steam_appid_new)
    else:
        await message.answer(f"{users_style_text.message_correct_change_steam_id(username=message.from_user.username,steam_appid=steam_appid)}",parse_mode=ParseMode.HTML,reply_markup=back_to_profile_main)
        await state.clear()