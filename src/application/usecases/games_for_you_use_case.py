from typing import Optional, Union

from src.application.dto.steam_dto import transform_to_dto, GamesForYouModel
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GamesGameForYouUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,user:Optional[str]=None,page:int=1,limit:int=5)->Optional[Union[GamesForYouModel,dict]]:
        data = await self.steam_client.games_for_you(user=user,page=page,limit=limit)
        if data is None:
            return None
        elif isinstance(data,dict) and data.get("detail"):
            return data
        else:
            logger.debug("Games_for_You_UseCase %s",data)
            answer = [transform_to_dto(GamesForYouModel,model) for model in data]
            return answer
