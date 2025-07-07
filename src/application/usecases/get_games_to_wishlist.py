from typing import Optional

from src.application.dto.users_dto import transform_to_dto, GamesToWishlist
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GetGamesToWishlistUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,steam_appid)->Optional[GamesToWishlist]:
        data = await self.steam_client.get_game_stats(steam_appid)
        if data is None:
            return None

        #Серіалізація Даних
        serialize_data = transform_to_dto(model=GamesToWishlist,orm=data,model_dump=False)

        return serialize_data
