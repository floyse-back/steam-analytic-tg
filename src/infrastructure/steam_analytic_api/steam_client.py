from httpx import AsyncClient,Client
from src.shared.config import STEAM_ANALYTIC_NAME,STEAM_ANALYTIC_PASSWORD

class SteamAnalyticsAPIClient:
    API_KEY = None
    BASE_URL = "http://127.0.0.1:8000/"

    def __init__(self):
        self.__url = "http://127.0.0.1:8000/"
        if self.API_KEY is None:
            self.login_account()

    def __create_client_session(self)->AsyncClient:
        auth = {"Authorization": "{}".format(self.API_KEY)}
        return AsyncClient(base_url=self.__url,follow_redirects=True,headers=auth)

    @classmethod
    def login_account(cls):
        with Client(base_url=cls.BASE_URL) as client:
            response = client.post(f"api/v1/auth/login",params={
                "username": STEAM_ANALYTIC_NAME,
                "password": STEAM_ANALYTIC_PASSWORD
            })
        if response.status_code == 201:
            cls.API_KEY = response.json()["refresh_token"]

    async def search_games(self,name):
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/steam/search_game",params={"name":name})
        return response.json()

    async def discounts_games(self,limit=15,page=1):
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/steam/best_sallers",
                                           params={
                                               "limit":limit,
                                               "page":page
                                           }
                                           )
        return response.json()