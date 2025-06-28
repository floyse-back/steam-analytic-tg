from src.application.dto.steam_dto import transform_to_dto, GameShortModel
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class FreeGamesNowUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self):
        data =  await self.steam_client.free_games_now()
        if data is None or len(data) == 0:
            return None
        return [transform_to_dto(GameShortModel,model) for model in data]