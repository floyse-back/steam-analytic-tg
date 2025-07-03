import datetime
from typing import Optional, Union

from pydantic import BaseModel

from src.api.presentation.empty_messages import EmptyMessages
from src.application.dto.player_dto import SteamPlayer, SteamRatingModel, SteamBadgesListModel, PlayerComparison, \
    ComparisonModel
from src.shared.dispatcher import DispatcherCommands


class PlayerStyleText:
    STATUS_MAP = {
        0: "🟥 Офлайн",
        1: "🟩 Онлайн",
        2: "🔙 Відійшов",
        3: "🔘 Не турбувати",
        4: "🟨 В мережі, але не в грі",
        5: "🎮 У грі",
        6: "📱 З мобільного"
    }
    def __init__(self):
        self.empty_messages = EmptyMessages()
        self.dispatcher_commands = DispatcherCommands(
            command_map={
                "player_full_stats": self.get_player_full_stats,
                "player_rating": self.get_player_rating_text,
                "player_badges": self.get_player_badges_text,
                "player_play": self.get_player_play_text
            }
        )

    def __validator(self,data:Optional[Union[str,dict,BaseModel]] = None,text:str="🚫 Щось пішло не так. Спробуйте ще раз трохи згодом."):
        if data is None:
            return text
        return None

    def __access_note(self,allow_games: bool, allow_friends: bool, allow_badges: bool) -> str:
        messages = []
        if not allow_games:
            messages.append("⚠️ Доступ до ігор було не отримано.")
        if not allow_friends:
            messages.append("⚠️ Доступ до друзів було не отримано.")
        if not allow_badges:
            messages.append("⚠️ Доступ до значків не було отримано.")
        if not messages:
            return "✅ Усі необхідні дані доступні."
        return "<s><b>Примітка:</b></s>\n" + "\n".join(messages)

    def __format_date(self,date:Optional[Union[datetime.date,int]]) -> str:
        if isinstance(date, int):
            date = self.__change_int_to_date(date)
        return date.strftime("%Y.%m.%d") if date else "-"

    def __change_int_to_date(self,date:int):
        return datetime.date.fromtimestamp(date)

    def get_player_full_stats(self,data:SteamPlayer):
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

    def __user_rating_stars(self,total:int):
        if total >= 8000:
            return "⭐⭐⭐⭐⭐"
        elif total >= 6000:
            return "⭐⭐⭐⭐"
        elif total >= 4000:
            return "⭐⭐⭐"
        elif total >= 2000:
            return "⭐⭐"
        elif total >= 0:
            return "⭐"
        else:
            return "—"

    def get_player_rating_text(self,data:SteamRatingModel):
        if answer:=self.__validator(data):
            return answer
        text = (
            f"<b>🧾 Статистика профілю Steam</b>\n"
            f"<b>👤 Нік:</b> {data.personaname}\n"
            f"<b>🆔 AppID:</b> {data.steam_appid}\n"
            f"<b>📈 Рейтинг:</b>{self.__user_rating_stars(data.user_rating)} ({data.user_rating})\n"
            f"<b>🏅 Рівень профілю:</b> {data.player_level}\n"
            f"<b>🔸 Досвід:</b> {data.player_xp} XP\n"
            f"<b>🆙 До наступного рівня:</b> {data.player_xp_needed_to_level_up} XP\n"
            f"<b>📅 Дата створення:</b> {self.__format_date(data.timecreated)}\n"
            f"<b>🕰️ Час у Steam:</b> {data.timelive}\n"
            f"<b>🧑‍🤝‍🧑 Друзів:</b> {data.friends_count}\n"
            f"<b>🎖️ Бейджів:</b> {data.badges_count}\n"
            f"<b>📤 Востаннє онлайн:</b> {self.__format_date(data.lastlogoff)}\n"
            f"<b>🎮 Загальний час у грі:</b> {data.playtime}\n\n"
            f"{self.__access_note(data.allow_games,data.allow_friends,data.allow_badges)}"
        )
        return text

    def get_player_badges_text(self,data:SteamBadgesListModel):
        if answer:=self.__validator(data):
            return answer
        text = (
            f"<b>🎖️ Бейджі профілю Steam</b>\n\n"
            f"<b>🏅 Рівень профілю:</b> {data.player_level}\n"
            f"<b>🔸 Поточний XP:</b> {data.player_xp}\n"
            f"<b>📈 До наступного рівня:</b> {data.player_xp_needed_to_level_up} XP\n"
            f"<b>⬅️ Поточний рівень починається з:</b> {data.player_xp_needed_current_level} XP\n\n"
        )

        for i, badge in enumerate(data.badges, 1):
            text += (
                f"<b>🏷️ Бейдж #{i}</b>\n"
                f"🆔 ID: {badge.badgeid}\n"
                f"🎚️ Рівень: {badge.level}\n"
                f"✨ XP: {badge.xp}\n"
                f"📉 Рідкість: {badge.scarcity:,} гравців мають цей бейдж\n"
                f"🗓️ Отримано: <code>{datetime.datetime.fromtimestamp(badge.completion_time).strftime('%d.%m.%Y')}</code>\n\n"
            )
        return text

    def get_player_play_text(self,data):
        pass

    def get_player_compare(self,data:PlayerComparison):
        if answer:=self.__validator(data):
            return answer
        output = "<b>🔎 Порівняння гравців</b>\n\n"

        user1 = data.user_1
        user2 = data.user_2

        output += f"<u>{user1}</u> vs <u>{user2}</u>\n\n"

        display_names = {
            "player_level": "🏅 Рівень профілю",
            "player_xp": "✨ Загальний XP",
            "badge_count": "🎖️ Кількість бейджів",
            "total_badges_xp": "💠 Загальний XP з бейджів",
            "game_count": "🎮 Кількість ігор",
            "total_playtime": "🕒 Загальний ігровий час (у хв)",
            "total_rating": "📊 Загальний рейтинг",
        }

        for field, label in display_names.items():
            field_data: ComparisonModel = getattr(data, field)
            if field_data is None:
                continue

            val1 = field_data.user_1 if field_data.user_1 is not None else "—"
            val2 = field_data.user_2 if field_data.user_2 is not None else "—"
            diff = field_data.difference if field_data.difference is not None else "—"

            winner = field_data.winner
            if winner == "user_1":
                win_note = f"(перемагає: {user1})"
            elif winner == "user_2":
                win_note = f"(перемагає: {user2})"
            else:
                win_note = "(нічия)"

            output += (
                f"{label}:\n"
                f"• {user1}: {val1}\n"
                f"• {user2}: {val2}\n"
                f"➖ Різниця: {diff} {win_note}\n\n"
            )

        return output

    def incorrect_steamname(self,username):
        return f"🚫 Користувача з <b><s>{username}</s></b> не знайдено. 🤔 Перевірте, чи все введено правильно."

    def create_message_from_get_user(self,users:int=1):
        """
        if users == 1 Повертаємо про 1 юзера
        """
        if users == 1:
            return "<b>💡 Вкажіть нік, ID або посилання на профіль гравця у Steam.</b>"
        elif users == 2:
            return "<b>💡 Тепер введіть інформацію про другого гравця (нік, ID або URL профілю).</b>"

    def create_incorrect_message_from_get_user(self,user:Optional[str]=None):
        if user is None:
            return "❌ <b>Користувача не знайдено!</b>\n🔎 Перевірте правильність введеного імені, ID або посилання."
        return f"<b>⚠️ Гравця <code><s>{user}</s></code> не знайдено.</b>\n❗<i>Можливо, допущено помилку при введенні. Введіть дані ще раз.</i>"

    def dispatcher(self,cammand_name,*args,**kwargs):
        return self.dispatcher_commands.dispatch_sync(cammand_name,*args,**kwargs)