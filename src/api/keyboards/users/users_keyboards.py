from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.api.keyboards.steam.steam_keyboards import create_page_swapper_inline
from src.application.dto.users_dto import GamesToWishlist
from src.shared.config import user_commands

async def create_user_inline_keyboard():
    user_inline_keyboard = InlineKeyboardBuilder()

    for v,i in user_commands.items():
        user_inline_keyboard.add(InlineKeyboardButton(text=v, callback_data=i))

    return user_inline_keyboard.adjust(2).as_markup()

def create_wishlist_inline_keyboard(callback_data:str,current_page:int=1,count:int=5,limit:int=5,next_page:Optional[bool]=None):
    inline_keyboard:InlineKeyboardBuilder = create_page_swapper_inline(
        callback_data=callback_data,
        menu_callback_data="user_main",
        current_page=current_page,
        count=count,
        limit=limit,
        mark_up=False,
        next_page=next_page,
    )
    inline_keyboard.row(
            InlineKeyboardButton(text="➕ Додати гру до списку бажаного", callback_data="add_wishlist_game"),
            InlineKeyboardButton(text="🗑️ Видалити гру зі списку", callback_data=f"remove_wishlist_game:{current_page}")
        ),
    return inline_keyboard.adjust(3).as_markup()

def create_remove_wishlist_inline_keyboard(data:list[GamesToWishlist],callback_data:Optional[str],delete_call_start_data:str,user_id:int,current_page:int=1,count:int=5,limit:int=5,next_page:Optional[bool]=None):
    if data is None:
        return None
    inline_keyboard:InlineKeyboardBuilder = create_page_swapper_inline(
        callback_data=callback_data,
        menu_callback_data="user_main",
        current_page=current_page,
        count=count,
        limit=limit,
        mark_up=False,
        next_page=next_page,
    )
    start_page = (current_page - 1)*limit
    for i,model in enumerate(data):
        inline_keyboard.add(
            InlineKeyboardButton(
                text=f"{start_page+i}",
                callback_data=f"{delete_call_start_data}:{model.steam_appid}:{user_id}"
            )
        )
    return inline_keyboard.adjust(3).as_markup()


wishlist_inline_keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Додати гру до списку бажаного", callback_data="add_wishlist_game"),
            InlineKeyboardButton(text="🗑️ Видалити гру зі списку", callback_data="remove_wishlist_game")
        ],
        [
            InlineKeyboardButton(text="👤 Перейти до профілю", callback_data="user_main")
        ]
    ]
)
go_to_wishlist_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎯 Улюблені ігри",
                callback_data="wishlist"
            ),
        ]
    ]
)
find_or_back = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="🎯 Улюблені ігри",
                callback_data="wishlist"
            ),
            InlineKeyboardButton(
                text="➕ Знайти іншу гру",
                callback_data="add_wishlist_game"
            ),

        ]
    ]
)

back_to_profile_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад до меню", callback_data="user_main")
        ]
    ]
)

profile_cancel_inline_keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Скасувати", callback_data="profile_cancel_state")
        ]
    ]
)
