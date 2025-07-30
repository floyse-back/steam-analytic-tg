from datetime import datetime
from typing import List, Optional

import html
from src.application.dto.steam_dto import GameFullModel, CalendarEventModel, GanresOut, CategoryOut
from src.shared.dispatcher import DispatcherCommands
from html import escape

class NewsStyleText(DispatcherCommands):
    def __init__(self):
        super().__init__(
            command_map={
                "news_new_release": self.new_release_message,
                "news_free_games_now": self.free_games_now_message,
                "news_event_history": self.event_history_steam_facts_message,
                "news_discounts_steam_now": self.news_discounts_steam_message,
                "news_top_for_a_coins": self.news_top_for_a_coins_message,
                "news_random_game": self.random_game_message,
                "news_calendar_event_now": self.festivale_message,
                "news_game_from_ganre": self.game_from_ganre_message,
                "news_game_from_categories": self.game_from_categories_message
            }
        )

    @staticmethod
    def __create_game_from_history_news(data: List['GameFullModel']) -> str:
        now = datetime.now().date()
        result = []

        for game in data:
            # Реліз
            release_str = game.release_data.strftime("%d.%m.%Y") if game.release_data else "?"
            years_passed = now.year - game.release_data.year if game.release_data else "?"

            # Відгуки
            if game.recomendations:
                reviews = f"{round(game.recomendations / 1000)}K+" if game.recomendations >= 1000 else str(
                    game.recomendations)
            else:
                reviews = "Немає"

            # Metacritic
            metacritic_block = f"🏆 <b>Metacritic:</b> <i>{game.metacritic}</i>" if game.metacritic and game.metacritic != "-1" else ""

            # Знижка
            if game.discount and game.discount > 0:
                price_block = f"💰 <b>-{game.discount}%</b> → <b>{game.final_formatted_price}</b>"
            else:
                price_block = f"💰 <b>{game.final_formatted_price or '—'}</b>"

            # Формування повідомлення
            game_text = (
                f"🎮 <a href='https://store.steampowered.com/app/{game.steam_appid}'>{game.name}</a>\n"
                f"📅 <b>Реліз:</b> {release_str} — <i>{years_passed} років тому</i>\n"
                f"{price_block}\n"
                f"👍 <b>Відгуків:</b> {reviews}\n"
                f"{metacritic_block}\n"
            )

            result.append(game_text.strip())

        return "\n\n".join(result)

    @staticmethod
    def __create_game_from_steam_news(data: List['GameFullModel']) -> str:
        result = []
        for game in data:
            name = game.name
            discount = f"-{game.discount}%" if game.discount else "—"
            price = game.final_formatted_price or "Безкоштовно"
            recs = f"{game.recomendations // 1000}K+" if game.recomendations and game.recomendations >= 1000 else str(
                game.recomendations or "—")
            release = game.release_data.year if game.release_data else "N/A"
            link = f"https://store.steampowered.com/app/{game.steam_appid}"

            block = (
                f"\n🎮 <b>{name}</b>\n"
                f"🔻 {discount} → {price}\n"
                f"💬 {recs} рецензій\n"
                f"📅 Реліз: {release}\n"
                f"🔗 <a href=\"{link}\">У Steam</a>"
            )

            result.append(block)

        return "\n\n".join(result)

    @staticmethod
    def __create_data_games_list(data: List[GameFullModel],index_allowed:bool=True) -> str:
        text = ""
        for index,game in enumerate(data):
            # Назва гри
            name = escape(game.name)
            # Ціна
            price = "🆓 Безкоштовно" if game.is_free or (game.final_price == 0) else f"💰 {game.final_formatted_price}"

            # Знижка
            discount = f"🔻 -{game.discount}% " if game.discount and game.discount > 0 else ""

            # Метакритик
            metacritic = f"🏆 Metacritic: {game.metacritic}" if game.metacritic != '-1' and game.metacritic else "🏆 Metacritic: N/A"

            # Рекомендації
            recommendations = f"👍 Рецензій: {game.recomendations}" if game.recomendations else ""

            # Жанри
            genres = ", ".join([escape(g.ganres_name) for g in game.game_ganre[0:5]]) or "Без жанру"

            # Категорії
            categories = ", ".join([escape(c.category_name) for c in game.game_categories[0:5]]) or "Без категорій"

            # Видавці
            publishers = ", ".join([escape(p.publisher_name) for p in game.game_publisher[0:5]]) or None

            # Опис
            description = escape(game.short_description or "Опису немає")

            # Дата релізу
            release = f"📅 Реліз: {game.release_data.strftime('%d.%m.%Y')}" if game.release_data else ""

            # Форматування HTML
            text += (
                f"<b>🎮{f'{index+1}.' if index_allowed else ""} {name}</b>\n"
                f"{discount}{price}\n"
                f"{metacritic} | {recommendations}\n"
                f"📚 <i>{description}</i>\n"
                f"🏷️ Жанри: {genres}\n"
                f"🎯 Категорії: {categories}\n"
                f"{f'🏢 Видавець: {publishers}\n' if publishers else ''}\n"
                f"{release}\n"
                f"<a href=\"https://store.steampowered.com/app/{game.steam_appid}\">🔗 Відкрити у Steam</a>\n"
                f"────────────────────────────────────────\n"
            )
        return text

    def new_release_message(self, data: List[GameFullModel]):
        text_start = (
            "🚀 <b>Свіжачок прилетів!</b>\n"
            "Нові ігри щойно вискочили у Steam, ще гарячі 🔥\n"
            "Може знайдеш щось смачненьке 🎮👇\n"
            f"{self.__create_game_from_steam_news(data)}\n"
        )
        return text_start

    def free_games_now_message(self, data: List[GameFullModel]):
        text_start = (
            "🆓 <b>БЕЗКОШТОВНО?!</b>\n"
            "Так! Ці ігри зараз можна забрати за 0 гривень! 🎁\n"
            "Як каже народна мудрість: «Дарованому Steam-акаунту в метакритику не дивляться» 😅👇\n"
            f"{self.__create_data_games_list(data)}\n"
        )
        return text_start

    def event_history_steam_facts_message(self, data: List[GameFullModel]):
        text_start = (
            "📜 <b>Трохи історії, трохи ігор!</b>\n"
            "Ось добірка, присвячена легендарним подіям та моментам зі світу Steam 👴💻\n"
            "Поринь у ностальгію (або вивчи щось новеньке) 👇\n"
            f"{self.__create_game_from_history_news(data)}\n"
        )
        return text_start

    def news_discounts_steam_message(self, data: List[GameFullModel]):
        text_start = (
            "💸 <b>Знижки летять, гаманці тремтять!</b>\n"
            "Ці ігри зараз зі знижками, а отже: саме час зробити вигляд, що тобі вони життєво необхідні 🛒🤣👇\n"
            f"{self.__create_game_from_steam_news(data)}\n"
        )
        return text_start

    def news_top_for_a_coins_message(self, data: List[GameFullModel]):
        text_start = (
            "🪙 <b>Максимум кайфу — мінімум витрат!</b>\n"
            "Ось топ ігор, які дають більше, ніж коштують.\n"
            "Бо навіщо платити 1000 грн, якщо за 200 можна залипнути на тиждень? 😎👇\n"
            f"{self.__create_game_from_steam_news(data)}\n"
        )
        return text_start

    def random_game_message(self, data: List[GameFullModel]):
        text_start = (
            "🎲 <b>Рулетка часу!</b>\n"
            "Я вибрав гру випадково — а раптом це твоє нове геймерське кохання? 💘🎮\n"
            "Не дякуй, просто дивись 👇\n"
            f"{self.__create_data_games_list(data,index_allowed=False)}\n"
        )
        return text_start

    def trailer_from_day_message(self,data:List[GameFullModel]):
        pass

    def festivale_message(self, event: CalendarEventModel) -> str:
        if isinstance(event, list):
            event = event[0]

        name = event.name or "без назви"
        start = event.date_start.strftime('%d.%m.%Y')
        end = event.date_end.strftime('%d.%m.%Y')

        if event.type_name == "sale":
            return (
                f"<b>🔥 Глобальний розпродаж в Steam вже почався!</b>\n\n"
                f"🛒 <i>{name}</i> — це твоя можливість поповнити бібліотеку ігор за вигідними цінами. "
                f"Знижки на тисячі тайтлів, від інді-проєктів до легендарних AAA-хітів!\n\n"
                f"<b>📅 Акція діє з</b> <u>{start}</u> <b>до</b> <u>{end}</u>\n\n"
                f"💡 Не зволікай — найкращі пропозиції можуть зникнути швидше, ніж ти думаєш.\n\n"
                f"💸 Час економити з розумом і грати в кайф!"
            )
        else:
            return (
                f"<b>🎉 Steam знову тішить нас фестивалем!</b>\n\n"
                f"🕹️ <i>{name}</i> — це чудова нагода відкрити нові ігри, зануритись у жанри, які ти міг оминати, "
                f"та спробувати демо найочікуваніших тайтлів майбутнього.\n\n"
                f"<b>📅 Тривалість:</b> з <u>{start}</u> до <u>{end}</u>\n\n"
                f"👀 Слідкуй за оновленнями, адже під час фестивалів часто з’являються спеціальні покази, "
                f"стріми від розробників та унікальні активності.\n\n"
                f"🎮 Час досліджувати нове!"
            )

    def game_from_ganre_message(self, dict_data: dict) -> str:
        ganre_name:str = dict_data["type_ganre"]
        data:GameFullModel = dict_data["data"][0]
        return (
            f"🎮 <b>Гра за жанром — {ganre_name}</b>\n"
            f"🔍 Якщо ти фанат жанру <b><i>{ganre_name}</i></b>, ця гра точно приверне твою увагу!\n"
            f"Ось що ми для тебе знайшли:\n"
            f"{self.__generate_game_property_message(data,ganre_main=ganre_name)}\n"
        )

    def game_from_categories_message(self, dict_data: dict) -> str:
        category_name:str = dict_data["type_category"]
        data:GameFullModel = dict_data["data"][0]

        return (
            f"🎮 <b>Гра за категорією — {category_name}</b>\n"
            f"🔍 Якщо ти полюбляєш категорію <b><i>{category_name}</i></b>, ця гра тобі сподобається!\n"
            f"Ось що ми для тебе знайшли:\n"
            f"{self.__generate_game_property_message(data, category_main=category_name)}\n"
        )

    def __generate_game_property_message(self, game: GameFullModel,ganre_main:Optional[str] = None,category_main:Optional[str]=None) -> str:
        game_ganre = game.game_ganre[0:5]
        game_category = game.game_categories[0:5]
        if not ganre_main is None and ganre_main not in game_ganre:
            game_ganre.insert(0, GanresOut(
                ganres_id=42,
                ganres_name=ganre_main
            ))
        if not category_main is None and category_main not in game_ganre:
            game_category.insert(0, CategoryOut(
                category_id = 42,
                category_name=category_main
            ))

        genre_names = ", ".join(html.escape(g.ganres_name) for g in game_ganre)
        category_names = ", ".join(html.escape(c.category_name) for c in game.game_categories[0:5]) or "Немає"
        publisher_names = ", ".join(html.escape(p.publisher_name) for p in game.game_publisher[0:5]) or None

        price_info = (
            f"💰 <b>Ціна:</b> {html.escape(game.final_formatted_price)} {f'(-{game.discount}%)' if game.discount != 0 else ''}"
            if not game.is_free and game.final_formatted_price
            else "🆓 <b>Безкоштовно</b>"
        )

        metacritic = f"🏆 <b>Metacritic:</b> {html.escape(game.metacritic)}" if game.metacritic !=-1 else ""
        recommendations = f"👍 <b>Рекомендацій:</b> {game.recomendations}" if game.recomendations else ""
        release = f"📅 <b>Реліз:</b> {game.release_data.strftime('%d.%m.%Y')}" if game.release_data else ""


        text = f"""
    <b>{html.escape(game.name)}</b>
    {html.escape(game.short_description or "Опис відсутній.")}

    {price_info}
    {metacritic}
    {recommendations}
    {release}

    🏷️ <b>Жанри:</b> {genre_names}
    {f'📢 <b>Видавець:</b> {publisher_names}' if publisher_names else ''}
    📂 <b>Категорії:</b> {category_names}

    🔗 <a href="https://store.steampowered.com/app/{game.steam_appid}">Сторінка в Steam</a>"""

        if game.trailer_url:
            text += f'\n🎬 <a href="{html.escape(game.trailer_url)}">Трейлер</a>'

        return text.strip()
