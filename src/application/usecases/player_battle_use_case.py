from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GetPlayerBattleUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self, user1:str,user2:str):
        data = await self.steam_client.get_player_battle(user1=user1,user2=user2)
        if data is None:
            return None

        #Серіалізація
        logger.debug("Data:%s",data)
        return data