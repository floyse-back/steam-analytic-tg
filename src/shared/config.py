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
    "🎲 Рекомендована гра": "suggest_game",
    "📋 Переглянути всі категорії": "chose_category"
}
steam_message_menu = "Привіт! Що тебе цікавить у світі Steam? 🎮"

user_commands: dict[str, str] = {
    "👤 Профіль": "profile",
    "🎯 Улюблені ігри": "wishlist",
    "✏️ Змінити мій ID": "change_my_id",
    "📋 Переглянути всі категорії": "chose_category"

}
user_message_menu = (
    "👤 *Твій ігровий кабінет Steam*\n\n"
    "Обирай, що будемо робити далі:\n"
    "— 🔍 Подивитись профіль\n"
    "— 🎮 Улюблені ігри — додати чи видалити\n"
    "— ♻️ Змінити Steam ID\n\n"
    "⬇️ Натискай кнопку нижче — усе під контролем 😉"
)

player_commands: dict[str, str] = {
    "ℹ️ Статистика за ID": "player_full_stats",
    "🏆 Рейтинг гравця": "player_rating",
    "🎖️ Досягнення": "player_badges",
    "⚖️ Порівняти з іншим": "compare_users",
    "📋 Переглянути всі категорії":"chose_category"
}
player_message_menu = "Оберіть команду, пов’язану з гравцем 🎮:"

subscribes_commands: dict[str, str] = {
    "🆕 Нові релізи": "subscribe_new_release",
    "🆓 Безкоштовні ігри": "subscribe_free_games",
    "📅 Івенти та події": "subscribe_new_events",
    "📰 Офіційні новини": "subscribe_steam_news",
    "🔔 Бажані ігри зі знижками": "subscribe_wishlist_notificate",
    "🔥 Гарячі знижки": "subscribe_hot_discount_notificate",
    "📋 Переглянути всі категорії":"chose_category"
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


