from typing import Optional

from src.application.dto.player_dto import SteamBadgesListModel, transform_to_dto
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GetPlayerBudgesUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self, user:str)->Optional[SteamBadgesListModel]:
        data = await self.steam_client.get_player_badges(user=user)
        if data is None:
            return None
        logger.debug("Data:%s",data)
        serialize_data = transform_to_dto(SteamBadgesListModel,data)
        logger.debug("Serialize Data",serialize_data)

        return serialize_data