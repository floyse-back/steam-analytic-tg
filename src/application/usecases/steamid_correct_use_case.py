from typing import Optional

from src.application.dto.users_dto import SteamAppid, transform_to_dto
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class SteamIDCorrectUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,steam_user)->Optional[SteamAppid]:
        data = await self.steam_client.vanity_user_find(steam_user=steam_user)
        if data is None:
            return None
        return transform_to_dto(SteamAppid,data)