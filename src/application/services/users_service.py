from typing import Optional

from src.application.dto.users_dto import SteamAppid
from src.application.usecases.check_user_steamid_use_case import CheckUserSteamIDUseCase
from src.application.usecases.create_user_use_case import CreateUserUseCase
from src.application.usecases.get_user_use_case import GetUserUseCase
from src.application.usecases.player_full_stats_use_case import PlayerFullStatsUseCase
from src.application.usecases.steamid_correct_use_case import SteamIDCorrectUseCase
from src.application.usecases.update_user_use_case import UpdateUserUseCase
from src.domain.user_context.repository import IUsersRepository
from src.infrastructure.db.database import get_async_db
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import help_config


class UsersService:
    def __init__(self,users_repository:IUsersRepository,steam_client:SteamAnalyticsAPIClient):
        self.create_user_use_case = CreateUserUseCase(
            users_repository=users_repository
        )
        self.get_player_full_stats_use_case = PlayerFullStatsUseCase(
            steam_client=steam_client
        )
        self.check_user_steam_id_use_case = CheckUserSteamIDUseCase(
            users_repository=users_repository
        )
        self.get_user_use_case = GetUserUseCase(
            users_repository=users_repository
        )
        self.update_user_use_case = UpdateUserUseCase(
            users_repository=users_repository
        )
        self.vanity_user_use_case = SteamIDCorrectUseCase(
            steam_client = steam_client
        )
        self.get_player_steam_id_use_case = GetUserUseCase(
            users_repository=users_repository
        )

    def user_help(self):
        return help_config.get("user")

    async def update_or_register_user(self,user_id,steam_user:Optional[str]=None)->Optional[bool]:
        """
        return False - Означає що не було знайдено користувача
        return True - Все пройшло успішно
        """
        async for session in get_async_db():
            if steam_user is not None:
                steam_appid:Optional[SteamAppid] = await self.vanity_user_use_case.execute(steam_user=steam_user)
                if steam_appid is None:
                    return False
            else:
                return False
            user = await self.get_user_use_case.execute(session=session,user_id=user_id,integer=False)
            if user is None:
                await self.create_user_use_case.execute(user_id=user_id,steam_id=steam_appid['steam_appid'],session=session)
            else:
                await self.update_user_use_case.execute(user=user,session=session,steam_id=steam_appid["steam_appid"])
                logger.debug("Error Update User Use Case %s,%s User:",user_id,steam_appid,user)
            return True

    async def check_register_steam_id_user(self,user_id,session):
        data = await self.check_user_steam_id_use_case.execute(user_id=user_id,session=session)
        return data

    async def get_profile_user(self,telegram_id:int,session):
        """
        Повертає False коли користувач або не зареєстрований або не ввів steam_appid
        """
        steam_appid = await self.get_player_steam_id_use_case.execute(user_id=telegram_id,session=session)
        if steam_appid is None:
            return False
        return await self.get_player_full_stats_use_case.execute(user=steam_appid)
