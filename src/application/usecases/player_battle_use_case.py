from src.application.dto.player_dto import transform_to_dto, PlayerComparison
from src.domain.logger import ILogger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GetPlayerBattleUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient,logger:ILogger):
        self.steam_client = steam_client
        self.logger = logger

    async def execute(self, user1:str,user2:str):
        self.logger.info("GetPlayerBattleUseCase: user1=%s user2=%s",user1,user2)
        data = await self.steam_client.get_player_battle(user1=user1,user2=user2)
        if data is None:
            return None

        #Серіалізація
        serialize_data = transform_to_dto(PlayerComparison, data)
        self.logger.debug("GetPlayerBattleUseCase: user1=%s, user2=%s, data=%s",user1,user2,serialize_data)
        return serialize_data