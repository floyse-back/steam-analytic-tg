import random
from typing import Optional, List, Union

from src.api.presentation.empty_messages import EmptyMessages
from src.application.dto.steam_dto import GameShortModel, GameAchievementsModel, GamePriceModel, GamesForYouModel
from src.shared.config import ganre_config
from src.shared.dispatcher import DispatcherCommands


class SteamStyleText:
    def __init__(self):
        self.first_smile = ["🎮","🎪","👻"]

        self.dispatcher_command = DispatcherCommands(
            command_map={
                "games_for_you":self.create_for_you,
                "discount_for_you":self.create_for_you,
                "achievements_game":self.create_achievements_description,
                "game_price":self.create_game_price,
                "search_game":self.create_short_search_games
            }
        )

        self.emojis = [
            "🎮", "🕹️", "🔥", "💥", "🧠", "🗡️", "🛡️", "👾",
            "💸", "🤑", "🎯", "🚀", "🌌", "🧊", "⛓️", "👑",
            "🧙‍♂️", "🐉", "🧛‍♂️", "⚔️", "🏆", "🕰️"
        ]

    def __generate_first_smile(self):
        return random.choice(self.first_smile)

    @staticmethod
    def __generate_stars_from_total(total):
        if total >= 700:
            return "⭐⭐⭐⭐⭐"
        elif total >= 400:
            return "⭐⭐⭐⭐"
        elif total >= 300:
            return "⭐⭐⭐"
        elif total >= 100:
            return "⭐⭐"
        elif total >= 25:
            return "⭐"
        else:
            return "—"


    @staticmethod
    def __generate_smile_discount(percent:int)->str:
        if percent == 0:
            return "🧊"
        elif percent < 10:
            return "😕"
        elif percent < 30:
            return "🤨"
        elif percent < 50:
            return "😉"
        elif percent < 70:
            return "🔥"
        elif percent < 90:
            return "🚨"
        else:
            return "💯"

    def __generate_emojis(self,count:int=4):
        return random.sample(self.emojis,count)

    def validator(self,data:Union[Optional[dict],List,GameAchievementsModel],game:Optional[str]=None):
        if data is None:
            return EmptyMessages.create_empty_message(game=game)
        return False

    def create_short_desc(self,data:Union[GameShortModel,List[GameShortModel]]) -> str:
        if (answer:=self.validator(data=data)):return answer
        if isinstance(data, GameShortModel):
            data = [data]
        answer = ""
        for model in data:
            ganre_string = ""
            ganres_dict = model[f"game_ganre"]
            for i in range(0,min(len(ganres_dict),5)):
                ganre_string += f"{ganre_config.get(ganres_dict[i]["ganres_name"],"🎮")}" + ganres_dict[i]["ganres_name"] + " "
            price_smile = "🆓" if model["final_formatted_price"] == "Free" else "💵"
            discount_string = f" - ({model["discount"]})" if model["discount"]>0 else ""
            answer+= (f"{self.__generate_first_smile()} <b><a href='https://store.steampowered.com/app/{model["steam_appid"]}/'>{model["name"]}</a></b> - {price_smile} {model["final_formatted_price"]}{discount_string}\n"
                      f"<b><i>{model["short_description"]}</i></b>\n"
                      f"✅ <b>Ganres: {ganre_string}</b>\n\n")
        return answer

    def create_achievements_description(self,data:GameAchievementsModel,game:Optional[str]=None,page:int=1,offset:int=10):
        if (answer:=self.validator(data=data,game=game)):return answer
        achievements_description = ""
        start_number = (page-1)*offset+1
        for i,ach in enumerate(data["achievements"]["highlighted"]):
            achievements_description += f" - {start_number+i}.{ach["name"]}\n"
        if achievements_description == "":
            achievements_description = "🚫Ця гра немає досягнень 🚫"

        text = (f"🔥 <b>Гра</b>: <b><i><a href='https://store.steampowered.com/app/{data['steam_appid']}/'>{data['name']}</a></i></b>\n"
                f"📝 <b>Короткий опис</b>: <i>{data['short_description']}</i>\n"
                f"<b>🏅 Кількість досягнень: {data['achievements']['total']}</b>\n"
                f"🏅 <b>Список досягнень</b>:\n<i>{achievements_description}</i>\n"
                f"{self.__generate_first_smile()} <b>Ціна</b>: <i><b>{data['price_overview']['final_formatted'] if data.get('price_overview') is not None else 'Безкоштовно'}</b></i>")
        return text

    def create_short_list_games(self,data,page,limit):
        new_text = ""
        start_number = (page-1)*limit+1
        for i,game in enumerate(data):
            new_text += f"<b>{start_number+i}.<a href='https://store.steampowered.com/app/{game["appid"]}/'>{game["name"]}</a></b> |<i>{f'{game["price"]/100}$' if not game["price"]==0 else "🆓"}</i> | {f'<b>{game["discount"]}%</b>' if game["discount"]>0 else ""}| <b>👍{game["positive"]}</b> | <b>👎{game["negative"]}</b>\n"

        return f"{new_text}"

    def create_short_search_games(self,data,page,limit):
        if data is None:
            return EmptyMessages.create_empty_message()
        new_text = ""
        start_number = (page-1)*limit+1


        for i,game in enumerate(data):
            new_text += (f"\n{start_number+i}.<b><a href='https://store.steampowered.com/app/{game["steam_appid"]}/'>{game['name']}</a></b>"
                         f"\nЦіна гри: {game['final_formatted_price']}")
        return f"{new_text}"

    def create_game_price(self,data:GamePriceModel)->str:
        emojis = self.__generate_emojis(count=2)
        new_text = (f"<b>{emojis[0]} <a href='https://store.steampowered.com/app/{data['steam_appid']}/'>{data['name']}</a></b>\n\n"
                    f"<i><b>{data["short_description"]}</b></i>\n\n")
        if data["price_overview"]:
            price_overview = data["price_overview"]
            if price_overview['final_formatted'] == price_overview['initial_formatted']:
                price_line = data['initial_formatted']
            else:
                price_line = f"<s>{price_overview['initial_formatted']}</s> ➡️ {price_overview['final_formatted']}"
            discount = price_overview['discount_percent']
            new_text+=(f"<b>💸 Ціна: {price_line}</b>\n"
                    f"{self.__generate_smile_discount(percent=discount)} <b>Знижка:</b> <b><i>{discount}%</i></b>")
        else:
            new_text += f"<b>🎁 Гра безкоштовна!! 🎁</b>"
        new_text +=f"\n<b>{emojis[1]} Steam AppID {data['steam_appid']}</b>"
        return new_text

    def create_for_you(self,data:List[GamesForYouModel],player:Optional['str']=None,page:int=1,limit:int=5):
        if isinstance(data,dict) and data.get('detail'):
            return EmptyMessages.create_empty_message_for_you(data=data,player=player)

        emojis = self.__generate_emojis(count=len(data))
        new_text=""
        start_number = (page-1)*limit+1
        for i,model in enumerate(data):
            new_text +=(
                f"{start_number+i}.{emojis[i]} <b><a href='https://store.steampowered.com/app/{model['steam_appid']}/'>{model['name']}</a></b>\n"
                f"💡 <i>{model['short_description']}</i>\n"
                f"{self.__generate_smile_discount(percent=model['discount'])}| {model['final_formatted_price'] if model['final_formatted_price']!="Free" else "Безкоштовно"}\n"
                f"<b>📊 Відгуків: {model['recomendations']} | 🎯 Metacritic: {model['metacritic'] if model['metacritic']!="-1" else "Даних немає"}</b>\n"
                f"<b>⭐ Рейтинг: {self.__generate_stars_from_total(total=model['total'])} ({model['total']} балів)</b>\n\n"
            )
        return new_text

    def dispatcher(self,command_name,*args,**kwargs):
        return self.dispatcher_command.dispatch_sync(command_name,*args,**kwargs)

