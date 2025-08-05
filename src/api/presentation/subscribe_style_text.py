import html
from datetime import datetime, date
from typing import Optional, List

from src.application.dto.steam_dto import ChangedGamesWishlistModel
from src.domain.logger import ILogger
from src.shared.dispatcher import DispatcherCommands


class SubscribeStyleText:
    def __init__(self,logger:ILogger):
        self.dispatcher_command = DispatcherCommands(
            command_map={
                "subscribe_steam_news":self.generate_steam_event_messages,
                "subscribe_hot_discount_notificate":self.generate_hot_discount_notificate,
                "subscribe_free_games":self.generate_free_games,
                "subscribe_new_release":self.generate_new_release,
                "subscribe_wishlist_notificate":self.generate_wishlist_notificate,
            }
        )
        self.logger = logger

    @staticmethod
    def user_have_subscribe(description: str):
        return (
            f"{description}\n\n"
            f"✅ <b>Ви вже підписані на цю категорію.</b>"
        )

    @staticmethod
    def user_dont_have_subscribe(description: str):
        return (
            f"{description}\n\n"
            f"❗️ <b>Ви ще не підписані.</b>\n"
            f"Не зволікайте — підпишіться та отримуйте сповіщення першими! 😉"
        )

    @staticmethod
    def after_subscribes():
        return (
            "<b>✔️ Успішно:</b> <i>підписку активовано.</i>"
        )

    @staticmethod
    def after_unsubscribe():
        return (
            "<b>🛑 Підписку скасовано.</b> <i>Ви більше не отримуватимете оновлення з цієї категорії.</i>"
        )

    @staticmethod
    def after_bad_subscribe():
        return (
            "<b>⚠️ Неможливо оформити підписку.</b> <i>Ймовірно, вона вже активна або виникла помилка.</i>"
        )

    @staticmethod
    def after_bad_unsubscribe():
        return (
            "<b>⚠️ Скасування не виконано.</b> <i>Підписка, можливо, вже була скасована або не існувала.</i>"
        )

    def __check_date_steam_event_and_chose_answer(self, event: dict) -> Optional[str]:
        today = date.today()
        if today == event["date_start"]:
            if event["type_name"] == "festival":
                return (
                    f"<b>🎉 Стартував новий фестиваль у Steam!</b>\n\n"
                    f"🕹️ <i>{event['name']}</i> — унікальна нагода відкрити для себе нові ігри, спробувати демо, переглянути стріми та просто кайфанути від улюбленого жанру.\n\n"
                    f"<b>📅 Тривалість:</b> з <u>{event['date_start'].strftime('%d.%m')}</u> до <u>{event['date_end'].strftime('%d.%m')}</u>\n\n"
                    f"🎮 Зазирни в Steam — буде гаряче!"
                )
            else:  # sale
                return (
                    f"<b>🔥 Знижки вже в Steam!</b>\n\n"
                    f"🛒 <i>{event['name']}</i> — ідеальний шанс поповнити бібліотеку новими тайтлами. Ціни падають, як FPS на старому ноуті.\n\n"
                    f"<b>📅 Тривалість:</b> з <u>{event['date_start'].strftime('%d.%m')}</u> до <u>{event['date_end'].strftime('%d.%m')}</u>\n\n"
                    f"💸 Не пропусти шалені пропозиції — знижки до -90%!"
                )

        elif today == event["date_end"]:
            if event["type_name"] == "festival":
                return (
                    f"<b>⌛ Сьогодні останній день фестивалю!</b>\n\n"
                    f"🕹️ <i>{event['name']}</i> завершується вже сьогодні. Це твій останній шанс переглянути демо, оцінити ігри та забрати те, що сподобалося.\n\n"
                    f"🎬 Не зволікай — відкрий Steam і встигни зацінити!\n\n"
                    f"<b>🗓 До:</b> <u>{event['date_end'].strftime('%d.%m')}</u>"
                )
            else:  # sale
                return (
                    f"<b>🕔 Останній шанс на шалені знижки!</b>\n\n"
                    f"💰 <i>{event['name']}</i> завершується вже сьогодні. Якщо ще щось залишилось у wishlist — час діяти!\n\n"
                    f"<b>📅 До:</b> <u>{event['date_end'].strftime('%d.%m')}</u>\n\n"
                    f"🚨 Наступні знижки — не скоро. Не проґав!"
                )

        return None

    def generate_steam_event_messages(self,data: List[dict]) -> str:
        if data is None or len(data) == 0:
            return None

        event = data[0]
        event['date_start'] = datetime.strptime(event['date_start'], '%Y-%m-%d').date()
        event['date_end'] = datetime.strptime(event['date_end'], '%Y-%m-%d').date()
        text = self.__check_date_steam_event_and_chose_answer(event=event)
        return text

    @staticmethod
    def __generate_full_game_model(game: dict) -> str:
        return (
            f"<b>🎮 {game['name']}</b>\n"
            f"<b>🗓 Дата виходу:</b> {game['release_data']}\n"
            f"{f"<b>📈 Metacritic:</b> {game['metacritic']}\n" if game['metacritic']=="-1" else '—'}"
            f"<b>🆓 Ціна:</b> {'Безкоштовно' if game['is_free'] else game['final_formatted_price']}\n"
            f"<a href='https://store.steampowered.com/app/{game['steam_appid']}'>🛒 Відкрити в Steam</a>"
        )

    @staticmethod
    def __generate_game_accent_discount(game: dict) -> str:
        status = (
            "<b>🆓 Безкоштовно</b>"
            if game['is_free'] or game['discount'] == 100
            else f"<b>💸 Знижка: -{game['discount']}%</b>\n💰 <i>{game['final_formatted_price']}</i>"
        )
        return (
            f"<b>🎮 {game['name']}</b>\n"
            f"{status}\n"
            f"<a href='https://store.steampowered.com/app/{game['steam_appid']}'>🛒 Переглянути в Steam</a>\n"
        )

    @staticmethod
    def __generate_wishlist_changes(game: ChangedGamesWishlistModel) -> str:
        """
        Генерація HTML caption для телеграм
        """
        name = html.escape(game.name)
        price_now = f"{game.price_now}₴" if game.price_now > 0 else "Безкоштовно"
        price_before = f"{game.price_before}₴"
        discount_now = f"-{game.discount_now}%"
        discount_before = f"-{game.discount_before}%" if game.discount_before > 0 else "без знижки"

        if game.discount_now == 100 and game.price_now == 0:
            text = (
                f"<b>🎉 <a href='https://store.steampowered.com/app/{game.steam_appid}'>{name}</a></b>\n"
                f"Гра стала <u>безкоштовною</u>!\n"
                f"Ціна була: <s>{price_before}</s>\n"
                f"Тепер: <b>{price_now}</b> 🆓"
            )

        elif game.discount_now < game.discount_before and game.price_now > game.price_before:
            text = (
                f"<b>📈 {name}</b>\n"
                f"Ціна зросла: <s>{price_before}</s> → <b>{price_now}</b>\n"
                f"Знижка зменшена: {discount_before} → {discount_now}"
            )

        elif game.discount_now > game.discount_before and game.price_now < game.price_before:
            text = (
                f"<b>🔥 {name}</b>\n"
                f"Знижка зросла: {discount_before} → {discount_now}\n"
                f"Ціна зменшилась: <s>{price_before}</s> → <b>{price_now}</b>"
            )

        elif game.discount_now == game.discount_before and game.price_now > game.price_before:
            text = (
                f"<b>💰 {name}</b>\n"
                f"Ціна зросла: <s>{price_before}</s> → <b>{price_now}</b>\n"
                f"Знижка не змінилась: {discount_now}"
            )

        elif game.discount_now == game.discount_before and game.price_now < game.price_before:
            text = (
                f"<b>🔻 {name}</b>\n"
                f"Ціна зменшилась: <s>{price_before}</s> → <b>{price_now}</b>\n"
                f"Знижка не змінилась: {discount_now}"
            )

        elif game.discount_now > game.discount_before and game.price_now == game.price_before:
            text = (
                f"<b>📉 {name}</b>\n"
                f"Знижка зросла: {discount_before} → {discount_now}\n"
                f"Ціна залишилась: <b>{price_now}</b>"
            )

        elif game.discount_now < game.discount_before and game.price_now == game.price_before:
            text = (
                f"<b>⚠️ {name}</b>\n"
                f"Знижка зменшилась: {discount_before} → {discount_now}\n"
                f"Ціна не змінилась: <b>{price_now}</b>"
            )

        else:
            text = f"<b>{name}</b>\nЦіна: {price_now}, Знижка: {discount_now}"

        return text

    def generate_hot_discount_notificate(self, data) -> str:
        text = (
            "<b>🔥 Гарячі знижки в Steam!</b>\n"
            "Не пропусти найвигідніші пропозиції — ігри зі знижками до 99%! Пора поповнити свою бібліотеку 🎮💥\n\n"
        )
        self.logger.info("Execute GenerateHotDiscountNotificate")
        self.logger.debug(f"Data: {data}")
        for ind,game in enumerate(data):
            text += self.__generate_game_accent_discount(game)
            if ind != len(data)-1:
                text += "\n"
        return text

    def generate_free_games(self, data) -> str:
        text = (
            "<b>🎁 Безкоштовні ігри в Steam!</b>\n"
            "Скористайся шансом отримати круті ігри абсолютно безкоштовно. Не проґав свою можливість! 🕹️\n\n"
        )
        for ind,game in enumerate(data):
            text += self.__generate_full_game_model(game)
            if ind != len(data)-1:
                text += "\n\n"
        return text

    def generate_new_release(self, data) -> str:
        text = (
            "<b>🆕 Нові релізи на Steam!</b>\n"
            "Ось найсвіжіші ігри, що з'явилися у магазині. Перевір, можливо серед них є твій новий фаворит 🎮\n\n"
        )
        self.logger.info("Execute GenerateHotDiscountNotificate")
        self.logger.debug(f"Data: {data}")
        for ind,game in enumerate(data):
            text += self.__generate_full_game_model(game)
            if ind != len(data)-1:
                text += "\n\n"
        return text

    def generate_wishlist_notificate(self, data: List[dict]) -> str:
        return (
            "<b>🔔 Оновлення у твоєму списку бажаного!</b>\n"
            "Є нові новини про ігри, які ти додав до вішлиста. Не пропусти вигідні пропозиції та свіжі релізи! 🎮\n\n"
        )

    def generate_wishlist_subscribe(self, data: dict) -> dict[str, list[str]]:
        new_data = {}
        for k, v in data.items():
            texts = []
            text_batch = '<b>Зміни в улюблених іграх:</b> 🔥🎮✨'
            for i, game in enumerate(v, 1):  # нумерація з 1 для зручності
                text_batch += "\n\n"+self.__generate_wishlist_changes(game=game)
                if i % 5 == 0:
                    texts.append(text_batch)
                    text_batch = ""
            if text_batch:
                texts.append(text_batch)
            new_data[k] = texts
        return new_data


    def dispatcher(self,func_name,*args,**kwargs)->Optional[str]:
        return self.dispatcher_command.dispatch_sync(func_name,*args,**kwargs)


