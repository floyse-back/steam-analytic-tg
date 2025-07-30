from typing import Optional

from src.shared.utils import escape_markdown


class EmptyMessages:
    @staticmethod
    def create_empty_message(game: Optional[str] = None):
        if game is None:
            return "🥺 Нажаль, гру не знайдено..."
        else:
            game = escape_markdown(text=game)
            return (f"🥺 Нажаль, гру за запитом: **{game}** не знайдено..."
                    f"\nМожливо, є помилка у назві? 🧐"
                    f"\n**Спробуй ще раз! 🙌🎮**")

    @staticmethod
    def create_empty_message_for_you(data:Optional[dict],player:str):
        player = f'<b><s>{player}<s></b>' if player else ''
        if data is None:
            return "На жаль, ми не змогли знайти для вас гру 😔<br>Спробуйте пізніше 🔁"
        if data.get('detail') =="Steam user not found":
            return f"<b>😔 Нажаль, гравця {player} не було знайдено</b>"
        return f"🔒 Гравець {player} закрив профіль 🙈"
