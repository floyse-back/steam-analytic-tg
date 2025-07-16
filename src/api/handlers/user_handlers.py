from typing import Optional

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.api.handlers.callback.users_callback import users_style_text
from src.api.keyboards.main_keyboards import start_keyboard
from src.api.keyboards.steam.steam_keyboards import create_search_share_keyboards
from src.api.keyboards.users.users_keyboards import create_user_inline_keyboard, profile_cancel_inline_keyboard_main, \
    back_to_profile_main
from src.api.middleware.account import user_get_or_none
from src.api.utils.state import ProfileSteamName, ChangeSteamName, WishlistGame
from src.infrastructure.logging.logger import Logger
from src.shared.config import MainMenu, user_message_menu
from src.shared.depends import get_users_service

router = Router(name=__name__)

logger = Logger(name="api.user_handler",file_path="api")
users_service = get_users_service()


@router.message(lambda message: message.text == f"{MainMenu.profile}")
async def user_reply(message: Message,state: FSMContext):
    if await user_get_or_none(state=state,telegram_id=message.from_user.id,users_service=users_service,message=message,style_text=users_style_text) is None:
        return None

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

@router.message(WishlistGame.game)
async def get_wishlist_game(message: Message, state:FSMContext):
    await state.update_data(game=message.text)
    state_data = await state.get_data()
    await state.clear()
    page,limit=1,5
    logger.debug(f"User wishlist game %s",state_data)
    if state_data.get("game") is not None:
        data = await users_service.search_games_short(name=state_data["game"],page=page,limit=limit)

        if data is None:
            await state.clear()
            await state.update_data(command="add_wishlist_game")
            await state.set_state(WishlistGame.game)
            await message.delete()
            await message.answer(f"{users_style_text.message_incorrect_game()}",parse_mode=ParseMode.HTML)
            return None
        else:
            reply_command = create_search_share_keyboards(callback_data=state_data["command"],value=state_data["game"],data=data,page=page,limit=limit)
        response = users_style_text.create_short_search_games(data,page=page,limit=limit)
        await message.delete()
        await message.answer(f"{response}", parse_mode=ParseMode.HTML, reply_markup=reply_command)
