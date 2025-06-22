from typing import Optional

from src.application.dto.steam_dto import transform_to_dto, GameShortModel
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GetSuggestGameUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self):
        response:Optional[list]= await self.steam_client.suggest_game()

        if response:
            data = [transform_to_dto(GameShortModel,i) for i in response]

            return data
        return None