from src.application.dto.steam_dto import transform_to_dto, GameShortListModel
from src.domain.logger import ILogger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class DiscountsGameUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient,logger:ILogger):
        self.steam_client = steam_client
        self.logger = logger

    async def execute(self,page:int=1,limit:int=2):
        data =  await self.steam_client.discounts_games(limit=limit,page=page)
        self.logger.debug(f"DiscountsGamesUseCase: page=%s limit=%s",page,limit)
        data = [transform_to_dto(GameShortListModel,i) for i in data]
        return data