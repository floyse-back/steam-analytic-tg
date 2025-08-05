from datetime import datetime, date, timedelta
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
        self.category_messages = {
            "Колекційні картки Steam": "🃏 <b>Збирай та обмінюйся!</b>\nSteam-картки — не просто картинки, це стиль. Ця гра дасть тобі шанс поповнити колекцію!",
            "Кооперативна гра": "🤝 <b>Гра для команди</b>\nГрати разом завжди веселіше! Ця гра — саме те, що треба для спільного проходження!"
        }
        self.ganre_messages = {
            "Стратегії": "🧠 <b>Стратегія — сила думки!</b>\nПлануй, керуй, перемагай! Ця гра змусить тебе мислити на кілька ходів уперед.",
            "Пригоди": "🗺️ <b>Готовий до пригод?</b>\nНевідомі світи, таємниці й сюжети — ця гра захопить тебе з перших хвилин!",
            "Рольові ігри": "🧙 <b>Рольова магія!</b>\nСтвори свого героя, занурся в історію та вирішуй долю світу. Обирай мудро!"
        }

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
    def __create_data_games_list(data: List[GameFullModel],index_allowed:bool=True,shorted:bool=False,free_delete:bool=False) -> str:
        text = ""
        for index,game in enumerate(data):
            if game.discount!=100 and free_delete:
                continue
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
            if shorted:
                text +=(
                    f"<b>🎮{f'{index+1}.' if index_allowed else ""} {name}</b>\n"
                    f"{discount}{price}\n"
                    f"{metacritic} | {recommendations}\n"
                    f"{release}\n"
                    f"<a href=\"https://store.steampowered.com/app/{game.steam_appid}\">🔗 Відкрити у Steam</a>\n\n"
                )
            else:
                text += (
                f"<b>🎮{f'{index+1}.' if index_allowed else ""} {name}</b>\n"
                f"{discount}{price}\n"
                f"{metacritic} | {recommendations}\n\n"
                f"📚 <i>{description}</i>\n\n"
                f"🏷️ Жанри: {genres}\n"
                f"🎯 Категорії: {categories}\n"
                f"{f'🏢 Видавець: {publishers}\n' if publishers else ''}\n"
                f"{release}\n"
                f"<a href=\"https://store.steampowered.com/app/{game.steam_appid}\">🔗 Відкрити у Steam</a>\n"
            )
        return text

    def new_release_message(self, data: List[GameFullModel]):
        text_start = (
            "🚀 <b>Свіжачок прилетів!</b>\n"
            "Нові ігри щойно вискочили у Steam, ще гарячі 🔥\n"
            "Може знайдеш щось смачненьке 🎮👇\n"
        )
        result = self.__generate_steam_new_release(header=text_start,games=data)
        return result

    def free_games_now_message(self, data: List[GameFullModel]):
        if len(data) == 1:
            data_list = self.__create_data_games_list(data,free_delete=True,index_allowed=False)
        else:
            data_list = self.__create_data_games_list(data,shorted = True)
        if len(data_list)==0:
            return None
        text_start = (
            "🆓 <b>БЕЗКОШТОВНО?!</b>\n"
            "Так! Ці ігри зараз можна забрати за 0 гривень! 🎁\n"
            "Як каже народна мудрість: «Дарованому Steam-акаунту в метакритику не дивляться» 😅👇\n\n"
            f"{data_list}\n"
        )
        return text_start

    def event_history_steam_facts_message(self, data: List[GameFullModel]):
        text_start = (
            "📜 <b>Трохи історії, трохи ігор!</b>\n"
            "Ось добірка, присвячена легендарним подіям та моментам зі світу Steam 👴💻\n"
            "Поринь у ностальгію (або вивчи щось новеньке) 👇\n\n"
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
            "Не дякуй, просто дивись 👇\n\n"
            f"{self.__create_data_games_list(data,index_allowed=False)}\n"
        )
        return text_start

    def trailer_from_day_message(self,data:List[GameFullModel]):
        pass

    def festivale_message(self, event: CalendarEventModel) -> str:
        if isinstance(event, list):
            event = event[0]
        text = self.__check_date_steam_event_and_chose_answer(event)
        return text

    def __check_date_steam_event_and_chose_answer(self,event:GameFullModel) -> Optional[str]:
        """
        Генерує HTML-повідомлення для Telegram залежно від дати та типу події:
        1 - Початок події
        2 - Закінчення події
        3 - Завтра подія починається
        """
        today = date.today()
        tomorrow = today + timedelta(days=1)

        if today == event.date_start:
            if event.type_name == "festival":
                return (
                    f"<b>🎉 Стартував новий фестиваль у Steam!</b>\n\n"
                    f"🕹️ <i>{event.name}</i> — унікальна нагода відкрити для себе нові ігри, спробувати демо, переглянути стріми та просто кайфанути від улюбленого жанру.\n\n"
                    f"<b>📅 Тривалість:</b> з <u>{event.date_start.strftime('%d.%m')}</u> до <u>{event.date_end.strftime('%d.%m')}</u>\n\n"
                    f"🎮 Зазирни в Steam — буде гаряче!"
                )
            else:
                return (
                    f"<b>🔥 Знижки вже в Steam!</b>\n\n"
                    f"🛒 <i>{event.name}</i> — ідеальний шанс поповнити бібліотеку новими тайтлами. Ціни падають, як FPS на старому ноуті.\n\n"
                    f"<b>📅 Тривалість:</b> з <u>{event.date_start.strftime('%d.%m')}</u> до <u>{event.date_end.strftime('%d.%m')}</u>\n\n"
                    f"💸 Не пропусти шалені пропозиції — знижки до -90%!"
                )

        elif today == event.date_end:
            if event.type_name == "festival":
                return (
                    f"<b>⌛ Сьогодні останній день фестивалю!</b>\n\n"
                    f"🕹️ <i>{event.name}</i> завершується вже сьогодні. Це твій останній шанс переглянути демо, оцінити ігри та забрати те, що сподобалося.\n\n"
                    f"🎬 Не зволікай — віeventй Steam і встигни зацінити!\n\n"
                    f"<b>🗓 До:</b> <u>{event.date_end.strftime('%d.%m')}</u>"
                )
            else:
                return (
                    f"<b>🕔 Останній шанс на шалені знижки!</b>\n\n"
                    f"💰 <i>{event.name}</i> завершується вже сьогодні. Якщо ще щось залишилось у wishlist — час діяти!\n\n"
                    f"<b>📅 До:</b> <u>{event.date_end.strftime('%d.%m')}</u>\n\n"
                    f"🚨 Наступні знижки — не скоро. Не проґав!"
                )

        elif tomorrow == event.date_start:
            if event.type_name == "festival":
                return (
                    f"<b>⏳ Завтра стартує новий фестиваль у Steam!</b>\n\n"
                    f"🕹️ <i>{event.name}</i> — це буде справжнє свято для геймерів: демо, жанрові підбірки, стріми та багато всього цікавого!\n\n"
                    f"<b>📅 Початок:</b> <u>{event.date_start.strftime('%d.%m')}</u>\n\n"
                    f"🎮 Підготуй wishlist — завтра буде гаряче!"
                )
            else:
                return (
                    f"<b>💥 Завтра починається новий розпродаж у Steam!</b>\n\n"
                    f"🛒 <i>{event.name}</i> — готуй свій гаманець, бо будуть шалені знижки!\n\n"
                    f"<b>📅 Початок:</b> <u>{event.date_start.strftime('%d.%m')}</u>\n\n"
                    f"💸 Wishlist уже на поготові?"
                )

        return None


    def game_from_ganre_message(self, dict_data: dict) -> str:
        ganre_name:str = dict_data["type_ganre"]
        data:GameFullModel = dict_data["data"][0]
        description:str = f"🔍 Якщо ти фанат жанру <b><i>{ganre_name}</i></b>, ця гра точно приверне твою увагу!\n" if self.ganre_messages.get(f"{ganre_name}") is None else self.ganre_messages.get(f"{ganre_name}")

        return (
            f"{description}\n\n"
            f"{self.__generate_game_property_message(data,ganre_main=ganre_name)}\n"
        )

    def game_from_categories_message(self, dict_data: dict) -> str:
        category_name:str = dict_data["type_category"]
        data:GameFullModel = dict_data["data"][0]
        description = f"🔍 Якщо ти полюбляєш категорію <b><i>{category_name}</i></b>, ця гра тобі сподобається!\n" if self.category_messages.get(f"{category_name}") is None else self.category_messages.get(f"{category_name}")

        return (
            f"{description}\n\n"
            f"{self.__generate_game_property_message(data, category_main=category_name)}\n"
        )


    def __generate_steam_new_release(self,header:str,games: List[GameFullModel]) -> str:
        msg = header

        for game in games:
            if game.is_free:
                continue  # Пропускаємо безкоштовні (демки)

            game_line = f"🎮 <b>{game.name}</b>\n"

            if game.discount and game.final_formatted_price:
                game_line += f"🔻 -{game.discount}% → <b>{game.final_formatted_price}</b>\n"
            elif game.final_formatted_price:
                game_line += f"💰 <b>{game.final_formatted_price}</b>\n"

            release_year = game.release_data.strftime("%Y") if game.release_data else "?"
            recs = f"{game.recomendations} рекомендацій" if game.recomendations else "💬 Немає рецензій"
            game_line += f"📅 {release_year} | {recs}\n"
            game_line += f'🔗 <a href="https://store.steampowered.com/app/{game.steam_appid}">Steam</a>\n\n'

            if len(msg) + len(game_line) > 1024:
                break  # не додаємо більше, щоб не перевищити ліміт

            msg += game_line

        return msg.strip()

    def __generate_game_property_message(self, game: GameFullModel,ganre_main:Optional[str] = None,category_main:Optional[str]=None) -> str:
        game_ganre = game.game_ganre[0:5]
        game_category = game.game_categories[0:5]
        if ganre_main is not None and ganre_main not in [g.ganres_name for g in game_ganre]:
            game_ganre.insert(0, GanresOut(
                ganres_id=42,
                ganres_name=ganre_main
            ))
        if category_main is not None and category_main not in [c.category_name for c in game_category]:
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

        metacritic = f"🏆 <b>Metacritic:</b> {html.escape(game.metacritic)}" if game.metacritic !="-1" else ""
        recommendations = f"👍 <b>Рекомендацій:</b> {game.recomendations}" if game.recomendations else ""
        release = f"📅 <b>Реліз:</b> {game.release_data.strftime('%d.%m.%Y')}" if game.release_data else ""

        text = (
            f"Назва: <b>{html.escape(game.name)}</b>\n"
            f"{price_info}"
            f"{metacritic}\n"
            f"{recommendations}\n"
            f"{release}\n\n"
            f"📚 {html.escape(game.short_description or 'Опис відсутній.')}\n\n"
            f"🏷️ <b>Жанри:</b> {genre_names}\n"
            f"📂 <b>Категорії:</b> {category_names}\n"
            f"{f'📢 <b>Видавець:</b> {publisher_names}\n' if publisher_names else ''}"
            f"\n🔗 <a href=\"https://store.steampowered.com/app/{game.steam_appid}\">Сторінка в Steam</a>"
        )

        if game.trailer_url:
            text += f'\n🎬 <a href="{html.escape(game.trailer_url)}">Трейлер</a>'

        return text.strip()
