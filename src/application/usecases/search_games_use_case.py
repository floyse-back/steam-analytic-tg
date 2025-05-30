from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class SearchGamesUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,name):
        return await self.steam_client.search_games(name)