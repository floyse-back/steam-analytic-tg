from typing import Optional

from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv

load_dotenv()

ASYNC_DATABASE_URL = getenv("ASYNC_DATABASE_URL")

TELEGRAM_API_TOKEN = getenv('TELEGRAM_API_TOKEN')

STEAM_ANALYTIC_NAME = getenv('STEAM_ANALYTIC_NAME')
STEAM_ANALYTIC_PASSWORD = getenv('STEAM_ANALYTIC_PASSWORD')

@dataclass(frozen=True)
class MainMenu:
    steam: str = "🧩 Steam"
    player: str = "🎮 Гравець"
    subscribes: str = "📬 Підписки"
    help: str = "❓ Допомога"
    profile: str = "👤 Профіль"
    subtitle: str = "📋 Головне меню"

steam_commands: dict[str, str] = {
    "🔍 Знайти гру": "search_game",
    "🎁 100% знижки!": "free_now",
    "💸 Знижки": "discount_games",
    "🏆 Найкращі ігри": "most_played_games",
    "🎮 Ігри для тебе": "games_for_you",
    "💰 Знижки для тебе": "discount_for_you",
    "📜 Досягнення гри": "achievements_game",
    "💵 Ціна гри зараз": "game_price",
    "🎲 Рекомендована гра": "suggest_game"
}
steam_message_menu = "Привіт! Що тебе цікавить у світі Steam? 🎮"

user_commands: dict[str, str] = {
    "👤 Профіль": "profile",
    "🎯 Улюблені ігри": "whishlist",
    "🆔 Перевірка по ID": "user_steam_info",
    "✏️ Змінити мій ID": "change_my_id"
}
user_message_menu = (
    "👤 *Твій кабінет Steam*\n\n"
    "Оберіть, що хочеш зробити:\n"
    "— Переглянути профіль\n"
    "— Керувати улюбленими іграми\n"
    "— Перевірити Steam-інформацію по ID\n"
    "— Змінити свій Steam ID\n\n"
    "⬇️ Обери дію з меню нижче:"
)

player_commands: dict[str, str] = {
    "ℹ️ Статистика за ID": "player_full_stats",
    "🏆 Рейтинг гравця": "player_rating",
    "🎖️ Досягнення": "player_badges",
    "🟢 Онлайн статус": "player_play",
    "⚖️ Порівняти з іншим": "compare_users",
}
player_message_menu = "Оберіть команду, пов’язану з гравцем 🎮:"

subscribes_commands: dict[str, str] = {
    "🆕 Нові релізи": "subscribe_new_release",
    "🆓 Безкоштовні ігри": "subscribe_free_games",
    "📅 Івенти та події": "subscribe_new_event",
    "📰 Офіційні новини": "subscribe_steam_news",
    "⚙️ Оновлення Steam": "subscribe_steam_update",
    "🔔 Бажані ігри зі знижками": "subscribe_whishlist_notificate",
    "🔥 Гарячі знижки": "subscribe_hot_discount_notificate"
}
subscribes_message_menu = "Підписки на оновлення 🗞️ – оберіть категорію:"




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


help_config:Optional[dict] = {
    "help": """
*👋 Вітаємо у SteamHandler*  
Твій простий помічник у світі ігор.

*🔍 Основні розділи:*  
• */games* — Ігри, ціни, поради  
• */user* — Профіль, wishlist  
• */subscribe* — Підписки на знижки та новини  
• */player* — Статистика, досягнення

_📌 Використай /help, щоби побачити це знову._
    """,

    "user": """
*👤 /user — Профіль та wishlist*  

• */wishlist* — Показати свій список бажаного  
• */add_wishlist <game_id>* — Додати гру до списку  
• */delete_game <game_id>* — Видалити гру зі списку  
• */user_player <user_id>* — Переглянути інфо про іншого користувача
    """,

    "subscribe": """
*🔔 /subscribe — Підписки*  

Отримуй автоматичні оновлення про важливе:  

• */subscribe_new_release <True/False>* — Нові релізи ігор  
• */subscribe_free_games <True/False>* — Безкоштовні ігри  
• */subscribe_new_event <True/False>* — Події у Steam  
• */subscribe_steam_news <True/False>* — Офіційні новини  
• */subscribe_steam_update <True/False>* — Оновлення клієнта  
• */subscribe_whishlist_notificate <True/False>* — Знижки на бажане  
• */subscribe_hot_discount_notificate <True/False>* — Гарячі знижки
    """,

    "games": """
*🎮 /games — Ігри, ціни, рекомендації*  

• */search_game <назва>* — Пошук гри за назвою  
• */free_games_now* — Актуальні безкоштовні ігри (Steam + Epic)  
• */discounts_game* — Поточні знижки  
• */most_played_games* — Популярні ігри  
• */games_for_you <user_id>* — Персональні поради  
• */discount_for_you <user_id>* — Персональні знижки  
• */achievements_game <gameID>* — Досягнення гри  
• */check_game_price <назва гри>* — Перевірити ціну  
• */suggest_game <жанр/настрій>* — AI-поради за жанром/настроєм
    """,

    "player": """
*🧩 /player — Статистика гравця*  

• */user_full_stats <user_id>* — Загальна статистика  
• */user_rating <user_id>* — Рейтинг гравця  
• */achievements_user <user_id>* — Його досягнення  
• */user_stalkering <user_id>* — Стежити за профілем  
• */user_play* — У що граєш зараз  
• */my_wishlist_deals* — Знижки на твоє бажане  
• */compare_users <user1> <user2>* — Порівняння профілів  
• */friend_activity* — Активність друзів
    """
}

ganre_config = {
    "Action": "⚡",
    "Adventure": "🌐",
    "RPG": "🛡️",
    "Strategy": "♟️",
    "Simulation": "🖥️",
    "Sports": "⚽",
    "Racing": "🏎️",
    "Puzzle": "🧩",
    "Horror": "🕯️",
    "Platformer": "👟",
    "Fighting": "🥋",
    "Sandbox": "🗃️",
    "Shooter": "🎯",
    "Survival": "⚒️",
    "Battle Royale": "🏹",
    "Stealth": "👤",
    "Visual Novel": "📖",
    "Rhythm": "🎵",
    "Educational": "📚",
    "Card Game": "🃏",
    "Board Game": "♟️",

    "Free to Play": "🆓",
    "Paid": "💰",
    "DLC": "📦",
    "Expansion": "➕",
}


