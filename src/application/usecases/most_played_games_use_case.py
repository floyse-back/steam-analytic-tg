from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class MostPlayedGamesUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self):
        return await self.steam_client.most_played_games()