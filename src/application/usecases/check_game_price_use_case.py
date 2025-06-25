from src.application.dto.steam_dto import transform_to_dto, GamePriceModel
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class GetCheckGamePriceUseCase(SteamAnalyticsAPIClient):
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,app:str):
        data = await self.steam_client.check_game_price(app)
        if data is None:
            return None

        serialize_data = transform_to_dto(GamePriceModel,data)
        return serialize_data
