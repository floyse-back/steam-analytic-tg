from aiogram.utils.keyboard import InlineKeyboardButton,InlineKeyboardMarkup, InlineKeyboardBuilder
from src.shared.config import steam_commands

async def create_inline_steam_commands():
    steam_inline_keyboard = InlineKeyboardBuilder()

    for v,i in steam_commands.items():
        steam_inline_keyboard.add(
            InlineKeyboardButton(
                text=v,
                callback_data=i
            )
        )

    return steam_inline_keyboard.adjust(2).as_markup()

search_new_game_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎮🔄 — Знайти іншу гру",callback_data="search_game")],
        [InlineKeyboardButton(
            text="🏠 Меню",
            callback_data=f"steam_menu"
        )]
    ]
)

go_to_main_menu_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [   InlineKeyboardButton(
            text="🏠 Меню",
            callback_data=f"steam_menu"
        )]
    ]
)

async def create_player_details_inline(callback_data,text):
    inline_buttons = InlineKeyboardBuilder()
    inline_buttons.add(
        InlineKeyboardButton(
            text=f"{text}",
            callback_data=callback_data
        )
    )
    return inline_buttons.adjust(1).as_markup()

async def create_page_swapper_inline(callback_data:str,menu_callback_data:str,current_page:int):
    inline_keyboard =  InlineKeyboardBuilder()
    if current_page-1 == 0:
        inline_keyboard.add(
            InlineKeyboardButton(
                text=f"",
                callback_data=f"noop"
            )
            )
    else:
        inline_keyboard.add(
            InlineKeyboardButton(
                text=f"⬅️ {current_page-1}",
                callback_data=f"{callback_data}:{current_page-1}"
            )
            )
    inline_keyboard.add(
        InlineKeyboardButton(
            text="🏠 Меню",
            callback_data=f"{menu_callback_data}"
        )
    )
    inline_keyboard.add(
        InlineKeyboardButton(
            text=f"{current_page+1} ➡️",
            callback_data=f"{callback_data}:{current_page+1}"
        )
    )
    return inline_keyboard.adjust(3).as_markup()

suggest_game_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
         InlineKeyboardButton(
             text="🎮🔄 - Згенерувати повторно",
             callback_data=f"suggest_game"
         )
        ],
        [
        InlineKeyboardButton(
            text="🏠 Меню",
            callback_data=f"steam_menu"
        )
        ]

    ]
)