from typing import List, Union, Optional

from aiogram.utils.keyboard import InlineKeyboardButton,InlineKeyboardMarkup, InlineKeyboardBuilder

from src.application.dto.steam_dto import GameListModel
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

achievements_new_game_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎮🔄 — Знайти іншу гру",callback_data="achievements_game")],
        [InlineKeyboardButton(
            text="🏠 Меню",
            callback_data=f"steam_menu"
        )]
    ]
)
game_price_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎮🔄 — Ціна іншої гри",callback_data="game_price")],
        [InlineKeyboardButton(
            text="🏠 Меню",
            callback_data=f"steam_menu"
        )]
    ]
)

def generate_steam_games_keyboard(text:str,callback_data:str,menu_callback_data:str="steam_menu",menu_text:str="🏠 Меню")->InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f"{text}",callback_data=f"{callback_data}")],
        [InlineKeyboardButton(
            text=f"{menu_text}",
            callback_data=f"{menu_callback_data}"
        )]
    ]
    )

    return inline_keyboard


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

def create_page_swapper_inline(callback_data:str,menu_callback_data:str,current_page:int,count=5,limit=5,mark_up=True,next_page:Optional[bool] = None)->Union[InlineKeyboardMarkup,InlineKeyboardBuilder]:
    """
    Про next_page
    if next_page is None тоді наступна сторінка заблокована
    if next_page == True тоді вона не заблокована і може бути при деяких умовах
    """

    inline_keyboard =  InlineKeyboardBuilder()
    if current_page-1 == 0:
        behind_button=InlineKeyboardButton(text=f"-",callback_data=f"noop")
    else:
        behind_button = InlineKeyboardButton( text=f"⬅️ {current_page-1}",callback_data=f"{callback_data}:{current_page-1}")
    menu_button=InlineKeyboardButton(text="🏠 Меню",callback_data=f"{menu_callback_data}")
    """
    В майбутньому можливо буде накинуто ліміт...
    """
    if count>=limit and next_page is None:
        next_button = InlineKeyboardButton(text=f"{current_page+1} ➡️",callback_data=f"{callback_data}:{current_page+1}"
            )
    else:
        next_button=InlineKeyboardButton(text=f"-",callback_data=f"noop")

    inline_keyboard.row(behind_button,menu_button,next_button)
    if mark_up:
        return inline_keyboard.as_markup()
    return inline_keyboard

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

def create_search_share_keyboards(callback_data:str,value:str,data:List[GameListModel],menu_callback_data:str="steam_menu",page:int=1,limit:int=5):
    inline_keyboard = create_page_swapper_inline(
        callback_data=f"search_short_games:{value}:{callback_data}",
        menu_callback_data=menu_callback_data,
        current_page=page,
        limit = 5,
        count=len(data),
        mark_up=False
    )
    start_value = (page-1)*limit+1
    for i,model in enumerate(data):
        inline_keyboard.add(
            InlineKeyboardButton(
                text=f"{start_value+i}",
                callback_data=f"{callback_data}:{model['steam_appid']}"
            )
        )
    return inline_keyboard.adjust(3).as_markup()

def create_player_steam_id(callback_data:str,steam_appid:Optional[int],page:Union[int,str]=1,menu_name_data:str="steam_menu")->Optional[InlineKeyboardMarkup]:
    if steam_appid is None:
        return None

    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(
                text=f"{steam_appid} - Ваш",
                callback_data =f"{callback_data}:{steam_appid}:{page}"
            )],
            [InlineKeyboardButton(
            text="🏠 Меню",
            callback_data=f"{menu_name_data}"
            )
            ]
        ]
    )
    return inline_keyboard

def try_now_keyboard_inline(callback_data:str)->Optional[InlineKeyboardMarkup]:
    try_now_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
            InlineKeyboardButton(
                text="Ввести іншого користувача",
                callback_data=f"{callback_data}"
            ),
            InlineKeyboardButton(
                text="🏠 Меню",
                callback_data=f"steam_menu"
            )
        ]
        ]
    )
    return try_now_keyboard