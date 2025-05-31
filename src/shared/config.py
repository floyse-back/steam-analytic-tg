from dotenv import load_dotenv
from os import getenv

load_dotenv()


TELEGRAM_API_TOKEN = getenv('TELEGRAM_API_TOKEN')

STEAM_ANALYTIC_NAME = getenv('STEAM_ANALYTIC_NAME')
STEAM_ANALYTIC_PASSWORD = getenv('STEAM_ANALYTIC_PASSWORD')

start_message = """
🎮 *Ласкаво просимо до SteamHandler!*  
Твій персональний асистент у світі ігор Steam та Epic Games.

Ось що я вмію:

🔍 *Ігри*
/games — Пошук, ціни, знижки, рекомендації

👤 *Профіль*
/user — Перегляд свого профілю, wishlist, інформація про інших користувачів

🔔 *Підписки*
/subscribe — Автоматичні сповіщення про новинки, знижки, події

📊 *Аналітика*
/player — Статистика, досягнення, активність друзів

💬 Напиши /help, щоб дізнатися більше про кожен розділ!

_Бот працює 24/7, готовий допомогти у будь-який час._
"""


help_config = {
    "help": """
        Ласкаво просимо до SteamHandler — твого особистого помічника у світі ігор!
        Ось список доступних розділів допомоги:
        
        /games — Пошук, ціни, рекомендації
        /user — Профіль, wishlist, інфо про користувача
        /subscribe — Підписки на новини, знижки, релізи
        /player — Аналіз профілю, статистика, досягнення
    """,
    "user": """
    👤 /user — Профіль та wishlist
    /wishlist — Показати свій список бажаного

    /add_wishlist <game_id> — Додати гру до wishlist

    /delete_game <game_id> — Видалити гру з wishlist

    /user_player <user_id> — Переглянути інфо про іншого користувача
    """,
    "subscribe": """
    🔔 /subscribe — Підписки
    Отримуй автоматичні оновлення про важливі події:

    /subscribe_new_release <True/False> — Нові релізи ігор

    /subscribe_free_games <True/False> — Нові безкоштовні ігри

    /subscribe_new_event <True/False> — Ігрові події Steam

    /subscribe_steam_news <True/False> — Офіційні новини Steam

    /subscribe_steam_update <True/False> — Оновлення клієнта Steam

    /subscribe_whishlist_notificate <True/False> — Знижки у твоєму wishlist

    /subscribe_hot_discount_notificate <True/False> — Гарячі знижки на ігри
    """,
    "games": """
        🎮 /games — Ігри, ціни, рекомендації
        /search_game <назва> — Знайди гру за її назвою

        /free_games_now — Поточні безкоштовні ігри (Steam + Epic)

        /discounts_game — Актуальні знижки на ігри

        /most_played_games — Топ найпопулярніших ігор

        /games_for_you <user_id> — Індивідуальні рекомендації ігор

        /discount_for_you <user_id> — Персональні знижки

        /achievements_game <gameID> — Досягнення конкретної гри

        /check_game_price <назва гри> — Перевірити поточну ціну гри

        /suggest_game <жанр/настрій> — AI-поради щодо ігор за жанром або настроєм
    """,
    "player": """
        🧩/player — Статистика та аналітика гравця

        /user_full_stats <user_id> — Повна статистика гравця

        /user_rating <user_id> — Рейтинг користувача

        /achievements_user <user_id> — Досягнення користувача

        /user_stalkering <user_id> — Стежити за активністю профілю

        /user_play — Дізнайся, в яку гру зараз граєш

        /my_wishlist_deals — Перевір знижки на ігри з твого wishlist

        /compare_users <user1> <user2> — Порівняння двох профілів

        /friend_activity — Огляд активності друзів (опційно)
    """
}
