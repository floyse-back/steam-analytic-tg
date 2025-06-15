from pydantic.experimental.pipeline import transform

from src.application.dto.steam_dto import transform_to_dto, GameShortListModel
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class MostPlayedGamesUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self):
        data = await self.steam_client.most_played_games()
        if data is None or len(data) == 0 :
            return False
        new_data = [transform_to_dto(GameShortListModel,i) for i in data]
        return new_data