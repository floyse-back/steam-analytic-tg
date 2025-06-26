from typing import Union

from src.application.dto.steam_dto import transform_to_dto, GameShortModel, GameListModel
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


class SearchGamesUseCase:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

    async def execute(self,name,page:int=1,limit:int=5,share:bool=True)->Union[GameShortModel,GameListModel,None]:
        """
        Функція повертає GameShortModel при share=True
        Функція повертає GameListModel при share=False
        """
        data = await self.steam_client.search_games(name=name,page=page,limit=limit,share=True)

        if share:
            new_data = [transform_to_dto(GameShortModel, i) for i in data]
        else:
            new_data = [transform_to_dto(GameListModel,i) for i in data]

        if new_data is None or len(new_data) == 0:
            return None
        return new_data