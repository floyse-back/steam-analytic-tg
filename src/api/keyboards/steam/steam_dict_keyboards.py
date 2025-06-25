from src.api.keyboards.steam.steam_keyboards import achievements_new_game_inline_keyboard, \
    search_new_game_inline_keyboard, game_price_inline_keyboard

steam_games_keyboards_dictionary = {
    "game_price":game_price_inline_keyboard,
    "search_game":search_new_game_inline_keyboard,
    "achievements_game":achievements_new_game_inline_keyboard,
}