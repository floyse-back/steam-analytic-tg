from typing_extensions import Optional

from src.application.usecases.achievements_game_use_case import AchievementsGameUseCase
from src.application.usecases.discount_for_you_use_case import DiscountsGameForYouUseCase
from src.application.usecases.discounts_game_use_case import DiscountsGameUseCase
from src.application.usecases.free_games_now_use_case import FreeGamesNowUseCase
from src.application.usecases.games_for_you_use_case import GamesGameForYouUseCase
from src.application.usecases.most_played_games_use_case import MostPlayedGamesUseCase
from src.application.usecases.search_games_use_case import SearchGamesUseCase
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import help_config
from src.shared.dispatcher import DispatcherCommands


class SteamService:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

        self.dispatcher = DispatcherCommands(
            command_map={
                "search_game":self.search_games
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

    async def search_games(self,name):
        return await self.search_games_use_case.execute(name)

    async def discount_games(self):
        return await self.discount_games_use_case.execute()

    async def free_games_now(self):
        return await self.free_games_now_use_case.execute()

    async def most_played_games(self):
        return await self.most_played_games_use_case.execute()

    async def games_for_you(self,user:Optional[str]=None):
        return await self.games_for_you_use_case.execute(user)

    async def discount_for_you(self,user:Optional[str]=None):
        return await self.discount_for_you_use_case.execute(user)

    async def achievements_game(self,game:Optional[str]=None):
        return await self.achievements_game_use_case.execute(game)

    async def check_game_price(self,game_id:int):
        pass

    async def suggest_game(self):
        pass

    async def dispetcher(self,command_name,*args,**kwargs):
        return await self.dispatcher.dispatch(command_name,*args,**kwargs)





