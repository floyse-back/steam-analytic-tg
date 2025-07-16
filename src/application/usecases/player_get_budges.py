from typing import Optional

from src.application.dto.player_dto import SteamBadgesListModel, transform_to_dto
from src.domain.logger import ILogger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GetPlayerBudgesUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient,logger:ILogger):
        self.steam_client = steam_client
        self.logger = logger

    async def execute(self, user:str)->Optional[SteamBadgesListModel]:
        self.logger.info("GetPlayerBudgesUseCase: user=%s",user)
        data = await self.steam_client.get_player_badges(user=user)
        if data is None:
            return None
        self.logger.debug("GetPlayerBudgesUseCase data:%s user=%s",data)
        serialize_data = transform_to_dto(SteamBadgesListModel,data)

        return serialize_data