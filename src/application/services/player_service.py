from src.application.usecases.get_user_use_case import GetUserUseCase
from src.application.usecases.player_battle_use_case import GetPlayerBattleUseCase
from src.application.usecases.player_full_stats_use_case import PlayerFullStatsUseCase
from src.application.usecases.player_get_budges import GetPlayerBudgesUseCase
from src.application.usecases.player_player_rating_use_case import GetPlayerRatingUseCase
from src.application.usecases.steamid_correct_use_case import SteamIDCorrectUseCase
from src.domain.user_context.repository import IUsersRepository
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import help_config
from src.shared.dispatcher import DispatcherCommands


class PlayerService:
    def __init__(self,steam_client:SteamAnalyticsAPIClient,users_repository:IUsersRepository):
        self.get_player_full_stats_use_case = PlayerFullStatsUseCase(
            steam_client=steam_client
        )
        self.get_player_budges_use_case = GetPlayerBudgesUseCase(
            steam_client=steam_client
        )
        self.get_player_battle_use_case = GetPlayerBattleUseCase(
            steam_client=steam_client
        )
        self.get_player_rating_use_case = GetPlayerRatingUseCase(
            steam_client=steam_client
        )
        self.get_vanity_use_case = SteamIDCorrectUseCase(
            steam_client = steam_client
        )
        self.dispatcher_command = DispatcherCommands(
            command_map={
                "player_full_stats": self.get_player_full_stats,
                "player_rating": self.get_player_rating,
                "player_badges":self.get_player_badges,
                "player_play":self.get_player_play
            }
        )
        self.get_player_steam_id_use_case = GetUserUseCase(
            users_repository=users_repository
        )

    def player_help(self):
        return help_config.get("player")

    async def get_player_badges(self,user):
        return await self.get_player_budges_use_case.execute(user=user)

    async def get_player_full_stats(self,user):
        return await self.get_player_full_stats_use_case.execute(user=user)

    async def get_player_rating(self,user):
        return await self.get_player_rating_use_case.execute(user=user)

    async def get_player_battle(self,user1:str,user2:str):
        return await self.get_player_battle_use_case.execute(user1=user1,user2=user2)

    async def get_player_play(self,user:str):
        return None

    async def get_vanity_user(self,user:str):
        return await self.get_vanity_use_case.execute(user)

    async def get_user_steam_id(self,telegram_id:int,session):
        data = await self.get_player_steam_id_use_case.execute(user_id=telegram_id,session=session)
        if data is None:
            return None
        return data

    async def dispatcher(self,command_name,*args,**kwargs):
        return await self.dispatcher_command.dispatch(command_name, *args, **kwargs)