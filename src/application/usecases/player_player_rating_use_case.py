from src.application.dto.player_dto import transform_to_dto, SteamRatingModel
from src.domain.logger import ILogger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GetPlayerRatingUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient,logger:ILogger):
        self.steam_client = steam_client
        self.logger = logger

    async def execute(self, user:str):
        data = await self.steam_client.get_player_rating(user=user)
        self.logger.info("GetPlayerRatingUseCase: user=%s",user)
        if data is None:
            return None

        #Серіалізація
        serialize_data = transform_to_dto(SteamRatingModel,data)
        self.logger.debug("GetPlayerRatingUseCase: user=%s, Data:%s",user,serialize_data)

        return serialize_data