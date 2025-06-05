from typing import Optional

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



