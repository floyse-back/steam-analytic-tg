import random

from typing_extensions import Optional

from src.application.dto.steam_dto import GameShortModel, transform_to_dto
from src.application.usecases.achievements_game_use_case import AchievementsGameUseCase
from src.application.usecases.discount_for_you_use_case import DiscountsGameForYouUseCase
from src.application.usecases.discounts_game_use_case import DiscountsGameUseCase
from src.application.usecases.free_games_now_use_case import FreeGamesNowUseCase
from src.application.usecases.games_for_you_use_case import GamesGameForYouUseCase
from src.application.usecases.most_played_games_use_case import MostPlayedGamesUseCase
from src.application.usecases.search_games_use_case import SearchGamesUseCase
from src.application.usecases.suggest_game_use_case import GetSuggestGameUseCase
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import help_config, ganre_config
from src.shared.dispatcher import DispatcherCommands

class SteamService:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

        self.dispatcher = DispatcherCommands(
            command_map={
                "search_game":self.search_games,
                "games_for_you":self.games_for_you,
                "discount_for_you":self.discount_for_you,
                "achievements_game":self.achievements_game,
                "game_price":self.games_for_you
            }
        )

        self.search_games_use_case = SearchGamesUseCase(
            steam_client = self.steam_client,
        )
        self.discount_games_use_case = DiscountsGameUseCase(
            steam_client = self.steam_client,
        )
        self.most_played_games_use_case = MostPlayedGamesUseCase(
            steam_client = self.steam_client,
        )
        self.games_for_you_use_case = GamesGameForYouUseCase(
            steam_client = self.steam_client,
        )
        self.discount_for_you_use_case = DiscountsGameForYouUseCase(
            steam_client = self.steam_client,
        )
        self.free_games_now_use_case = FreeGamesNowUseCase(
            steam_client = self.steam_client,
        )
        self.achievements_game_use_case = AchievementsGameUseCase(
            steam_client = self.steam_client,
        )
        self.suggest_game_use_case = GetSuggestGameUseCase(
            steam_client = self.steam_client
        )

    def steam_help(self):
        return help_config.get("games")

    def __create_empty_message(self):
        return "Game Not Found"

    def __generate_first_smile(self):
        data = ["🎮","🎪","👻"]
        return random.choice(data)

    def __create_short_desc(self,data:GameShortModel):
        ganre_string = ""
        ganres_dict = data[f"game_ganre"]
        for i in range(0,min(len(ganres_dict),5)):
            ganre_string += f"{ganre_config.get(ganres_dict[i]["ganres_name"],"🎮")}" + ganres_dict[i]["ganres_name"] + " "

        first_smile = self.__generate_first_smile()
        price_smile = "🆓" if data["final_formatted_price"] == "Free" else "💵"

        discount_string = f" - ({data["discount"]})" if data["discount"]>0 else ""

        return f"""
{first_smile} [{data["name"]}](https://store.steampowered.com/app/{data["steam_appid"]}/) - {price_smile} {data["final_formatted_price"]}{discount_string}
_{data["short_description"]}_
✅ **Ganres:** {ganre_string}
        """

    def __create_short_list_games(self,data,page,limit):
        new_text = ""
        start_number = (page-1)*limit+1
        for i,game in enumerate(data):
            new_text += f"{start_number+i}.[{game["name"]}](https://store.steampowered.com/app/{game["appid"]}/) |{game["price"]/100 if not game["price"]==0 else "🆓"}$ | {f'({game["discount"]}%)' if game["discount"]>0 else ""}| 👍{game["positive"]} | 👎{game["negative"]} \n"

        return f"{new_text}"

    async def search_games(self,name):
        data = await self.search_games_use_case.execute(name)
        new_message = ""

        if data is None:
            return self.__create_empty_message()

        for model in data:
            new_message+=f"{self.__create_short_desc(model)}"
        return "Знайдені ігри за вашим запитом: \n{}".format(new_message)

    async def discount_games(self,page:int=1,limit:int=10):
        data = await self.discount_games_use_case.execute(page=page,limit=limit)
        new_message = f"🎮🤑 **Найкращі знижки дня** 🤑🎮\n{self.__create_short_list_games(data,page,limit)}"
        return new_message

    async def free_games_now(self):
        data = await self.free_games_now_use_case.execute()

        if data is None or len(data) == 0:
            return self.__create_empty_message()

        for model in data:
            new_data = transform_to_dto(GameShortModel,model)
            new_message=f"{self.__create_short_desc(new_data)}"

        return new_message

    async def most_played_games(self,page:int=1,limit:int=10):
        data = await self.most_played_games_use_case.execute(page=page,limit=limit)

        text = self.__create_short_list_games(data,page,limit)
        text = "\t🔥🎮 **Найпопулярніші ігри:** 🎮🔥\n" + text
        return text

    async def games_for_you(self,user:Optional[str]=None):
        data =  await self.games_for_you_use_case.execute(user)
        return data

    async def discount_for_you(self,user:Optional[str]=None):
        data = await self.discount_for_you_use_case.execute(user)
        return data

    async def achievements_game(self,game:Optional[str]=None):
        data = await self.achievements_game_use_case.execute(game)
        return data

    async def check_game_price(self,game_id:int):
        pass

    async def suggest_game(self):
        data = await self.suggest_game_use_case.execute()
        text =""
        for i in data:
            text+=self.__create_short_desc(i)
        return f"""Випадкова гра:\n {text}"""

    async def dispetcher(self,command_name,*args,**kwargs):
        return await self.dispatcher.dispatch(command_name,*args,**kwargs)





