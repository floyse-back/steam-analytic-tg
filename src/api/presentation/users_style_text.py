import datetime
from typing import Optional, Union, List

from pydantic import BaseModel

from src.api.presentation.utils.shared_text import create_short_search_games_shared
from src.application.dto.player_dto import SteamPlayer
from src.application.dto.users_dto import GamesToWishlist


class UsersStyleText:
    STATUS_MAP = {
        0: "🟥 Офлайн",
        1: "🟩 Онлайн",
        2: "🔙 Відійшов",
        3: "🔘 Не турбувати",
        4: "🟨 В мережі, але не в грі",
        5: "🎮 У грі",
        6: "📱 З мобільного"
    }

    def __change_int_to_date(self,date:int):
        return datetime.date.fromtimestamp(date)

    def __format_date(self,date:Optional[Union[datetime.date,int]]) -> str:
        if isinstance(date, int):
            date = self.__change_int_to_date(date)
        return date.strftime("%Y.%m.%d") if date else "-"

    def __validator(self,data:Optional[Union[str,dict,BaseModel]] = None,text:str="🚫 Щось пішло не так. Спробуйте ще раз трохи згодом."):
        if data is None:
            return text
        return None

    def get_player_full_stats(self,data:Optional[SteamPlayer]=None) -> dict:
        if answer:=self.__validator(data):
            return answer

        player = data.user_data.player
        visibility = "Відкритий ✅" if player.communityvisibilitystate == 3 else "Закритий 🔒"
        profile_state = "Активований" if player.profilestate == 1 else "Не активований"
        new_text =(
        f"<b>🧑‍💻 Профіль гравця Steam</b>\n\n"
        f"<b>👤 Нік:</b> {player.personaname or '—'}\n"
        f"<b>🆔 SteamID:</b> <code>{player.steamid}</code>\n"
        f"<b>📅 Дата створення:</b> {self.__format_date(player.timecreated)}\n"
        f"<b>🕒 Час у Steam:</b> {player.timelive or '—'}\n"
        f"<b>📤 Востаннє онлайн:</b> {self.__format_date(player.lastlogoff)}\n"
        f"<b>🧑‍🤝‍🧑 Друзів:</b> {data.user_friends_list.friends_count}\n"
        f"<b>🎮 Грає зараз:</b> {player.gameextrainfo or 'Ні'}\n\n"
        f"<b>🛰️ Країна:</b> {player.loccountrycode or '—'}\n"
        f"<b>🔐 Видимість профілю:</b> {visibility}\n"
        f"<b>📄 Стан профілю:</b> {profile_state}\n"
        f"<b>📶 Статус:</b> {self.STATUS_MAP.get(player.personastate, 'Невідомо')}\n"
        f"<b>🏷️ Клан ID:</b> {player.primaryclanid or '—'}\n"
        f"<b>🧾 Ім’я:</b> {player.realname or '—'}\n\n"
        f"<b>🆔 SteamID першого друга:</b> <code>{data.user_friends_list.first_friend.steamid}</code>\n"
        f"👶 <b>Перший друг доданий:</b> {self.__format_date(data.user_friends_list.first_friend.friend_since)}\n"
        f"<b>🆔 SteamID останього друга:</b> <code>{data.user_friends_list.last_friend.steamid}</code>\n"
        f"🧓 <b>Останній друг доданий:</b> {self.__format_date(data.user_friends_list.last_friend.friend_since)}\n"
        f"<a href=\"{player.avatarfull}\">🖼️ Аватарка</a>"
    )
        return new_text

    def message_no_steam_id(self,username:str):
        return (f"👋 <b>Привіт, @{username}!</b>\n\n"
                f"🔒 <b>На жаль, ви не завершили реєстрацію, щоб отримати доступ до функцій бота.</b>\n"
                f"🎮 Щоб продовжити, надішліть свій Steam профіль у будь-якому з форматів:\n"
                f"• 🔢 SteamID64 (наприклад: <code>7656119...</code>)\n"
                f"• ✏️ Нік з URL (наприклад: <code>floysefake</code>)\n"
                f"• 🔗 Повне посилання на профіль\n\n"
                f"<i>Формат визначається автоматично 😉</i>")

    def message_change_steam_id(self, username: str):
        return (f"👋 <b>Привіт ще раз, @{username}!</b>\n\n"
                f"♻️ <b>Бажаєте змінити свій Steam профіль?</b>\n"
                f"🎮 Надішліть новий Steam профіль у будь-якому з форматів:\n"
                f"• 🔢 SteamID64 (наприклад: <code>7656119...</code>)\n"
                f"• ✏️ Нік з URL (наприклад: <code>floysefake</code>)\n"
                f"• 🔗 Повне посилання на профіль\n\n"
                f"<i>Ми автоматично все розпізнаємо 😉</i>")

    def message_incorrect_steam_id(self,steam_appid:str):
        return (f"❌ <b>На жаль, не вдалося знайти Steam профіль за ID <s>{steam_appid}</s></b>\n\n"
                f"🔁 <b>Будь ласка, перевірте правильність і спробуйте ще раз!</b>")

    def message_correct_change_steam_id(self, username: str, steam_appid: str):
        return (f"✅ <b>Ваш Steam профіль успішно оновлено, @{username}!</b>\n\n"
                f"🆔 Новий SteamID: <code>{steam_appid}</code>\n"
                f"🎉 Тепер ви можете користуватися всіма функціями бота без обмежень!")

    def message_post_game(self):
        return "<b>🎮 Введіть назву гри, яку хочете додати:</b>"

    def message_incorrect_game(self):
        return "<b>⚠️ Гру не знайдено. Перевірте правильність написання та спробуйте ще раз.</b>"

    def create_short_search_games(self,data,page:int=1,limit:int=5):
        return create_short_search_games_shared(data,page,limit)

    def message_correct_add_game(self):
        return "<b>✅ Гру успішно додано до вашого вішліста!</b>"

    def message_incorrect_add_game(self):
        return "<b>❌ Не вдалося додати гру до вішліста. Спробуйте пізніше або перевірте назву гри.</b>"

    from typing import List

    from typing import List

    def create_short_wishlist_message(self, data: List[GamesToWishlist]) -> str:
        if not data:
            return "📝 Вішліст порожній."

        lines = []
        for game in data:
            # Назва гри + ID
            line = f"🎮 <b>{game.name}</b> (ID: {game.steam_appid})\n"

            # Короткий опис (обрізаний до 100 символів)
            desc = game.short_description or "Без опису"
            if len(desc) > 100:
                desc = desc[:97] + "..."
            line += f"📖 {desc}\n"

            # Ціна + знижка, якщо є
            if game.price_overview:
                price = game.price_overview.final / 100  # ціна в доларах
                discount = game.price_overview.discount_percent or 0
                if discount > 0:
                    discounted_price = price * (100 - discount) / 100
                    line += (
                        f"💸 Ціна: <s>{price:.2f}$</s> → <b>{discounted_price:.2f}$</b> "
                        f"(<i>-{discount}%</i>)\n"
                    )
                else:
                    line += f"💰 Ціна: <b>{price:.2f}$</b>\n"

            else:
                line += "💰 Ціна: відсутня\n"

            lines.append(line)

        return "\n".join(lines)

    def game_correct_delete_wishlist(self, user):
        return f"✅ <b>Гру успішно видалено з вашого списку бажаного, {user}!</b>"

    def game_not_delete_wishlist(self, user):
        return f"⚠️ <b>Гру не вдалося видалити зі списку бажаного, {user}, оскільки вона вже там є.</b>"



