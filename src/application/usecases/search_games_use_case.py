from src.application.dto.steam_dto import transform_to_dto, GameShortModel
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class SearchGamesUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,name):
        data = await self.steam_client.search_games(name=name)

        new_data = [transform_to_dto(GameShortModel, i) for i in data]
        if new_data is None or len(new_data) == 0:
            return None
        return new_data