from typing import Optional
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class AchievementsGameUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,game:Optional[str]=None,page:int=1,offset:int=10) -> Optional[dict]:
        return await self.steam_client.achievements_game(game=game,page=page,offset=offset)