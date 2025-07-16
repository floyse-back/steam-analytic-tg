from typing import Optional, Union

from src.application.dto.steam_dto import transform_to_dto, GamesForYouModel
from src.domain.logger import ILogger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GamesGameForYouUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient,logger:ILogger):
        self.steam_client = steam_client
        self.logger = logger

    async def execute(self,user:Optional[str]=None,page:int=1,limit:int=5)->Optional[Union[GamesForYouModel,dict]]:
        data = await self.steam_client.games_for_you(user=user,page=page,limit=limit)
        if data is None:
            return None
        elif isinstance(data,dict) and data.get("detail"):
            return data
        else:
            answer = [transform_to_dto(GamesForYouModel,model) for model in data]
            self.logger.info("GamesGameForYouUseCase Success user = %s",user)
            return answer
