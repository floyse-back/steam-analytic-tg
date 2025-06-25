from src.api.keyboards.steam.steam_keyboards import generate_steam_games_keyboard

steam_games_keyboards_dictionary = {
    "game_price":generate_steam_games_keyboard(text="🎮🔄 — Ціна іншої гри",callback_data="game_price"),
    "search_game":generate_steam_games_keyboard(text="🎮🔄 — Знайти іншу гру",callback_data="search_game"),
    "achievements_game":generate_steam_games_keyboard(text="🎮🔄 — Знайти іншу гру",callback_data="achievements_game"),
}