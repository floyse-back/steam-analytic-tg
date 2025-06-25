from typing import Optional

from src.application.dto.steam_dto import transform_to_dto, GameAchievementsModel
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class AchievementsGameUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,game:Optional[str]=None,page:int=1,offset:int=10) -> Optional[dict]:
        data = await self.steam_client.achievements_game(game=game,page=page,offset=offset)
        if data is None:
           return None
        serialize_data = transform_to_dto(GameAchievementsModel,data)
        logger.debug(serialize_data)
        return serialize_data