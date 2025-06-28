import random
from typing import Optional, List, Union

from src.api.presentation.empty_messages import EmptyMessages
from src.application.dto.steam_dto import GameShortModel, GameAchievementsModel
from src.shared.config import ganre_config

class SteamStyleText:
    def __init__(self):
        self.first_smile = ["🎮","🎪","👻"]

    def __generate_first_smile(self, game: Optional[str] = None):
        return random.choice(self.first_smile)

    def validator(self,data:Union[Optional[dict],List],game:Optional[str]=None):
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
            answer+= f"""
    {self.__generate_first_smile()} <b><a href='https://store.steampowered.com/app/{model["steam_appid"]}/'>{model["name"]}</a></b> - {price_smile} {model["final_formatted_price"]}{discount_string}\n
    <b><i>{model["short_description"]}</i></b>\n
    ✅ <b>Ganres: {ganre_string}</b>
            """
        return answer

    def create_achievements_description(self,data:GameAchievementsModel,page:int=1,offset:int=10):
        achievements_description = ""
        start_number = (page-1)*offset+1
        for i,ach in enumerate(data["achievements"]["highlighted"]):
            achievements_description += f" - {start_number+i}.{ach["name"]}\n"
        if achievements_description == "":
            achievements_description = "🚫Ця гра немає досягнень 🚫"

        text = (f"🔥 *Гра*: **[{data['name']}](https://store.steampowered.com/app/{data['steam_appid']}/)**\n"
                f"📝 *Короткий опис*: {data['short_description']}\n"
                f"**🏅 Кількість досягнень: {data['achievements']['total']}**\n"
                f"🏅 *Список досягнень*:\n{achievements_description}\n"
                f"{self.__generate_first_smile()} *Ціна*: **{data['price_overview']['final_formatted'] if data.get('price_overview') is not None else 'Безкоштовно'}**")
        return text

    def create_short_list_games(self,data,page,limit):
        new_text = ""
        start_number = (page-1)*limit+1
        for i,game in enumerate(data):
            new_text += f"{start_number+i}.[{game["name"]}](https://store.steampowered.com/app/{game["appid"]}/) |{game["price"]/100 if not game["price"]==0 else "🆓"}$ | {f'({game["discount"]}%)' if game["discount"]>0 else ""}| 👍{game["positive"]} | 👎{game["negative"]} \n"

        return f"{new_text}"

    def create_short_search_games(self,data,page,limit):
        new_text = ""
        start_number = (page-1)*limit+1
        for i,game in enumerate(data):
            new_text += (f"\n{start_number+i}.{game['name']}"
                         f"\nЦіна гри: {game['final_formatted_price']}")
        return f"{new_text}"