from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class FreeGamesNowUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self):
        return await self.steam_client.free_games_now()