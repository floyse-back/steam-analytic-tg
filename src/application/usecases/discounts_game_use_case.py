from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class DiscountsGameUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,page:int=1,limit:int=2):
        return await self.steam_client.discounts_games(limit=limit,page=page)