from typing import Optional

from src.application.dto.player_dto import SteamPlayer,transform_to_dto
from src.domain.logger import ILogger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class PlayerFullStatsUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient,logger:ILogger):
        self.steam_client = steam_client
        self.logger = logger

    async def execute(self, user:str)->Optional[SteamPlayer]:
        self.logger.info("PlayerFullStatsUseCase: user=%s",user)
        data = await self.steam_client.get_full_stats_player(user=user)
        if data is None:
            return None
        #Серіалізація даних
        self.logger.debug("PlayerFullStatsUseCase: user=%s data=%s",user,data)
        serialize_data = transform_to_dto(SteamPlayer, data)
        return serialize_data