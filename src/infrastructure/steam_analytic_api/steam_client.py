from httpx import AsyncClient


class SteamAnalyticsAPIClient:
    def __init__(self):
        self.__url = "http://127.0.0.1:8000/"
        self.__client = AsyncClient(base_url=self.__url,follow_redirects=True)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__client.aclose()

    async def search_games(self,name):
            response = await self.__client.get(f"api/v1/steam/search_game",params={"name":name})
            return response.json()

    async def discounts_games(self,limit=15,page=1):
        response = await self.__client.get(f"api/v1/steam/best_sallers",
                                           params={
                                               "limit":limit,
                                               "page":page
                                           }
                                           )
        return response.json()
