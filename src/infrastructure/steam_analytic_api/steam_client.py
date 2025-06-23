from typing import Optional, Union, List

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
        else:
            raise Exception(response.text)

    async def search_games(self,name)->Optional[List[dict]]:
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/steam/search_game",params={"name":name})
        return response.json()

    async def discounts_games(self,limit=10,page=1)->Optional[List[dict]]:
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/steam/best_sallers",
                                           params={
                                               "limit":limit,
                                               "page":page
                                           }
                                           )
        return response.json()

    async def free_games_now(self)->Optional[List[dict]]:
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/analytics/free_games")

        if response.status_code == 200:
            return response.json()

    async def most_played_games(self,page=1,limit=5) -> Optional[List[dict]]:
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/steam/get_top_games/",params={
                "page":page,
                "limit":limit,
            })

        if response.status_code == 200:
            return response.json()

    async def games_for_you(self,user:Optional[str]=None) -> Optional[dict]:
        if user is None:
            raise Exception("User is required")
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/analytics/games_for_you",params={
                "user":user
            })

        if response.status_code == 200:
            return response.json()
        return None

    async def discount_for_you(self, user: Optional[str] = None)-> Optional[dict]:
        if user is None:
            raise Exception("User is required")
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/analytics/salling_for_you", params={
                "user": user
            })

        if response.status_code == 200:
            return response.json()
        return None

    async def achievements_game(self, game: str,page:int=1,offset:int=10) -> Optional[dict]:
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/steam/game_achivements", params={
                "game": game,
                "page":page,
                "offset":offset
            })
        if response.status_code == 200:
            return response.json()

    async def check_game_price(self, game_id: int):
        pass

    async def suggest_game(self) -> Optional[List]:
        async with self.__create_client_session() as client:
            response = await client.get(f"api/v1/analytics/random_games")

        if response.status_code == 200:
            return response.json()
        return None