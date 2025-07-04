from typing import Optional, Union

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from pydantic import BaseModel

from src.api.keyboards.steam.steam_keyboards import create_page_swapper_inline
from src.api.presentation.main_style_text import MainStyleText
from src.api.utils.state import ProfileSteamName
from src.application.services.users_service import UsersService
from src.infrastructure.db.database import get_async_db
from src.infrastructure.logging.logger import logger


async def create_page_message(callback_query:CallbackQuery,callback_data:str,page,data:Optional[Union[BaseModel,dict]],response:str,limit:int=5):
    if data is not None:
        await callback_query.message.edit_text(f"{response}",parse_mode=ParseMode.HTML,reply_markup=create_page_swapper_inline(callback_data=f"{callback_data}",current_page=page,menu_callback_data=f"steam_menu",limit=limit,count=len(data)))
    else:
        await callback_query.message.edit_reply_markup(reply_markup=create_page_swapper_inline(callback_data=f"{callback_data}",current_page=page,menu_callback_data=f"steam_menu",next_page=False))
    await callback_query.answer()

async def user_register_utils(message:Message,state:FSMContext,users_service:UsersService,main_style_text:MainStyleText,reply_markup:InlineKeyboardMarkup):
    await message.delete()
    async for session in get_async_db():
        if not await users_service.check_register_steam_id_user(message.from_user.id,session=session):
            await state.update_data()
            await state.set_state(ProfileSteamName.profile)
            await message.answer(f"{main_style_text.start_message_no_steam_id(username=message.from_user.username)}",parse_mode=ParseMode.HTML,reply_markup=reply_markup)
            return True
        return False
