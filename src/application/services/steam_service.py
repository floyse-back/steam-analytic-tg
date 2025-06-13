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

    async def search_games(self,name):
        data = await self.search_games_use_case.execute(name)
        new_message = ""

        if data is None or len(data) == 0:
            return self.__create_empty_message()

        for model in data:
            new_data=transform_to_dto(GameShortModel,model)
            new_message+=f"{self.__create_short_desc(new_data)}"

        return new_message

    async def discount_games(self):
        data = await self.discount_games_use_case.execute()

    async def free_games_now(self):
        data = await self.free_games_now_use_case.execute()
        return data

    async def most_played_games(self):
        data = await self.most_played_games_use_case.execute()

    async def games_for_you(self,user:Optional[str]=None):
        data =  await self.games_for_you_use_case.execute(user)

    async def discount_for_you(self,user:Optional[str]=None):
        data = await self.discount_for_you_use_case.execute(user)

    async def achievements_game(self,game:Optional[str]=None):
        data = await self.achievements_game_use_case.execute(game)

    async def check_game_price(self,game_id:int):
        pass

    async def suggest_game(self):
        pass

    async def dispetcher(self,command_name,*args,**kwargs):
        return await self.dispatcher.dispatch(command_name,*args,**kwargs)





