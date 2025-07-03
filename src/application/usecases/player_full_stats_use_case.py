from typing import Optional

from src.application.dto.player_dto import SteamPlayer,transform_to_dto
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class PlayerFullStatsUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self, user:str)->Optional[SteamPlayer]:
        data = await self.steam_client.get_full_stats_player(user=user)
        if data is None:
            return None
        #Серіалізація даних
        logger.info("Data PlayerFullStats %s",data)
        serialize_data = transform_to_dto(SteamPlayer, data)
        return serialize_data