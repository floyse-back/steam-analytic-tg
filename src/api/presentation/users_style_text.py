import datetime
from typing import Optional, Union

from pydantic import BaseModel

from src.application.dto.player_dto import SteamPlayer


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