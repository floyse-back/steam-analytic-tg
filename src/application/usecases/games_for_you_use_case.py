from typing import Optional

from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GamesGameForYouUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,user:Optional[str]=None):
        return await self.steam_client.games_for_you(user=user)