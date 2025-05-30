from src.application.usecases.search_games_use_case import SearchGamesUseCase
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class SteamService:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

        self.search_games_use_case = SearchGamesUseCase(
            steam_client = self.steam_client,
        )

    async def search_games(self,name):
        return await self.search_games_use_case.execute(name)




