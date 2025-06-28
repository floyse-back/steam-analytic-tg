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