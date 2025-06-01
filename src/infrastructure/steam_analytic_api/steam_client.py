from typing import Optional

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

    async def discounts_games(self,limit=2,page=1):
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/steam/best_sallers",
                                           params={
                                               "limit":limit,
                                               "page":page
                                           }
                                           )
        return response.json()

    async def free_games_now(self):
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/analytics/free_games")

        if response.status_code == 200:
            return response.json()

    async def most_played_games(self,page=1,limit=5):
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/steam/get_top_games/",params={
                "page":page,
                "limit":limit,
            })

        if response.status_code == 200:
            return response.json()

    async def games_for_you(self,user:Optional[str]=None):
        if user is None:
            raise Exception("user is required")
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/analytics/games_for_you",params={
                "user":user
            })

        if response.status_code == 200:
            return response.json()

    async def discount_for_you(self, user: Optional[str] = None):
        if user is None:
            raise Exception("user is required")
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/analytics/salling_for_you", params={
                "user": user
            })

        if response.status_code == 200:
            return response.json()

    async def achievements_game(self, game: str):
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/analytics/game_achivements", params={
                "game_id": game
            })

        if response.status_code == 200:
            return response.json()

    async def check_game_price(self, game_id: int):
        pass

    async def suggest_game(self):
        pass