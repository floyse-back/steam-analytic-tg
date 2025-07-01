from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class PlayerFullStatsUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self, user:str):
        data = await self.steam_client.get_full_stats_player(user=user)
        if data is None:
            return None
        #Серіалізація даних
        logger.debug("Data:%s",data)
        return data