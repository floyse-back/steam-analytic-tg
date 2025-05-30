from httpx import AsyncClient
import asyncio


class SteamAnalyticsAPIClient:
    def __init__(self):
        self.__url = "http://127.0.0.1:8000/"

    async def search_games(self,name):
        async with AsyncClient(base_url=self.__url,follow_redirects=True) as client:
            response = await client.get(f"api/v1/steam/search_game",params={"name":name})
            return response.json()

st = SteamAnalyticsAPIClient()
async def main():
    data = await st.search_games("C")
    data_2 = await st.free_games_now()
    return data, data_2

print(asyncio.run(main()))
