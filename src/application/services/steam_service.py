from typing import List

from typing_extensions import Optional, Union

from src.application.dto.steam_dto import GameShortModel, GameListModel
from src.application.usecases.achievements_game_use_case import AchievementsGameUseCase
from src.application.usecases.check_game_price_use_case import GetCheckGamePriceUseCase
from src.application.usecases.discount_for_you_use_case import DiscountsGameForYouUseCase
from src.application.usecases.discounts_game_use_case import DiscountsGameUseCase
from src.application.usecases.free_games_now_use_case import FreeGamesNowUseCase
from src.application.usecases.games_for_you_use_case import GamesGameForYouUseCase
from src.application.usecases.get_user_use_case import GetUserUseCase
from src.application.usecases.most_played_games_use_case import MostPlayedGamesUseCase
from src.application.usecases.search_games_use_case import SearchGamesUseCase
from src.application.usecases.suggest_game_use_case import GetSuggestGameUseCase
from src.domain.logger import ILogger
from src.domain.user_context.repository import IUsersRepository
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.dispatcher import DispatcherCommands


class SteamService:
    def __init__(self,steam_client:SteamAnalyticsAPIClient,users_repository:IUsersRepository,logger:ILogger):
        self.steam_client = steam_client
        self.logger = logger
        self.dispatcher_command = DispatcherCommands(
            command_map={
                "search_game":self.search_games,
                "games_for_you":self.games_for_you,
                "discount_for_you":self.discount_for_you,
                "achievements_game":self.achievements_game,
                "game_price":self.check_game_price
            }
        )

        self.search_games_use_case = SearchGamesUseCase(
            steam_client = self.steam_client,
        )
        self.discount_games_use_case = DiscountsGameUseCase(
            steam_client = self.steam_client,
            logger = logger
        )
        self.most_played_games_use_case = MostPlayedGamesUseCase(
            steam_client = self.steam_client,
        )
        self.games_for_you_use_case = GamesGameForYouUseCase(
            steam_client = self.steam_client,
            logger = logger
        )
        self.discount_for_you_use_case = DiscountsGameForYouUseCase(
            steam_client = self.steam_client,
        )
        self.free_games_now_use_case = FreeGamesNowUseCase(
            steam_client = self.steam_client,
        )
        self.achievements_game_use_case = AchievementsGameUseCase(
            steam_client = self.steam_client,
            logger = logger
        )
        self.suggest_game_use_case = GetSuggestGameUseCase(
            steam_client = self.steam_client
        )
        self.steam_price_game = GetCheckGamePriceUseCase(
            steam_client = self.steam_client
        )
        self.get_user_use_case = GetUserUseCase(
            users_repository=users_repository,
            logger=logger
        )

    async def search_games(self,name,page:int=1,limit:int=5,share:bool=True)->List[Optional[Union[GameShortModel,GameListModel]]]:
        """
        Повертає при share=True Pydantic:GameShortModel
        Повертає при share=False Pydantic:GameListModel
        """
        data = await self.search_games_use_case.execute(name,page=page,limit=limit,share=share)
        if data is None or len(data) == 0:
            return None
        return data

    async def discount_games(self,page:int=1,limit:int=10):
        data = await self.discount_games_use_case.execute(page=page,limit=limit)
        return data

    async def free_games_now(self):
        data = await self.free_games_now_use_case.execute()
        return data

    async def most_played_games(self,page:int=1,limit:int=10):
        data = await self.most_played_games_use_case.execute(page=page,limit=limit)
        return data

    async def games_for_you(self,user:Optional[str]=None,page:int=1,limit:int=5):
        data =  await self.games_for_you_use_case.execute(user,page,limit)
        return data

    async def discount_for_you(self,user:Optional[str]=None,page:int=1,limit:int=5):
        data = await self.discount_for_you_use_case.execute(user,page=page,limit=limit)
        return data

    async def achievements_game(self,game:Optional[str]=None,page:int=1,offset:int=10):
        data = await self.achievements_game_use_case.execute(game=game,page=page,offset=offset)
        return data

    async def check_game_price(self,game:str):
        data = await self.steam_price_game.execute(game)
        return data

    async def suggest_game(self):
        data = await self.suggest_game_use_case.execute()
        return data

    async def get_player(self,telegram_appid:int,session):
        data:Optional[int] = await self.get_user_use_case.execute(user_id=telegram_appid,session=session)
        self.logger.info("Steam Appid From Steam Service,%s",data)
        if data is None:
            return None
        self.logger.info("Steam Appid From Steam Service,%s",data)
        return data

    async def dispatcher(self,command_name,*args,**kwargs):
        return await self.dispatcher_command.dispatch(command_name, *args, **kwargs)





