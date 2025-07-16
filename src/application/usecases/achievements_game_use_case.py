from typing import Optional

from src.application.dto.steam_dto import transform_to_dto, GameAchievementsModel
from src.domain.logger import ILogger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class AchievementsGameUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient,logger:ILogger):
        self.steam_client = steam_client
        self.logger = logger

    async def execute(self,game:Optional[str]=None,page:int=1,offset:int=10) -> Optional[dict]:
        data = await self.steam_client.achievements_game(game=game,page=page,offset=offset)
        if data is None:
           return None
        serialize_data = transform_to_dto(GameAchievementsModel,data)
        self.logger.debug("AchievementsGameUseCase Confirm %s",serialize_data)
        return serialize_data