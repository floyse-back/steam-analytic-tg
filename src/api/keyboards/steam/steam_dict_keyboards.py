from src.api.keyboards.steam.steam_keyboards import generate_steam_games_keyboard, create_page_swapper_inline

steam_games_keyboards_dictionary = {
    "game_price":generate_steam_games_keyboard(text="🎮🔄 — Ціна іншої гри",callback_data="game_price"),
    "achievements_game": generate_steam_games_keyboard(text="🎮🔄 — Знайти- іншу гру", callback_data="achievements_game"),
}