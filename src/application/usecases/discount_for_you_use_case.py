from typing import Optional
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class DiscountsGameForYouUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,user:Optional[str]=None):
        data = await self.steam_client.discount_for_you(user)
        if data is None:
            return {"Try Later"}
        else:
            #Логіка сериалізації
            return data