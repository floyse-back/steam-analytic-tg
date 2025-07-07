from typing import Optional


from src.application.dto.users_dto import SteamAppid, GamesToWishlist
from src.application.usecases.add_wishlist_game import AddWishlistGame
from src.application.usecases.check_user_steamid_use_case import CheckUserSteamIDUseCase
from src.application.usecases.create_user_use_case import CreateUserUseCase
from src.application.usecases.create_wishlist_use_case import CreateWishlistsUseCase
from src.application.usecases.get_games_to_wishlist import GetGamesToWishlistUseCase
from src.application.usecases.get_user_use_case import GetUserUseCase
from src.application.usecases.get_wishlist_pages_use_case import GetWishlistsPagesUseCase
from src.application.usecases.get_wishlists_use_case import GetWishlistsUseCase
from src.application.usecases.player_full_stats_use_case import PlayerFullStatsUseCase
from src.application.usecases.remove_wishlist_game import RemoveWishlistGameUseCase
from src.application.usecases.search_games_use_case import SearchGamesUseCase
from src.application.usecases.steamid_correct_use_case import SteamIDCorrectUseCase
from src.application.usecases.update_user_use_case import UpdateUserUseCase
from src.domain.user_context.repository import IUsersRepository, IWishlistRepository
from src.infrastructure.db.database import get_async_db
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import help_config


class UsersService:
    def __init__(self,users_repository:IUsersRepository,steam_client:SteamAnalyticsAPIClient,wishlist_repository:IWishlistRepository):
        self.create_user_use_case = CreateUserUseCase(
            users_repository=users_repository
        )
        self.get_player_full_stats_use_case = PlayerFullStatsUseCase(
            steam_client=steam_client
        )
        self.check_user_steam_id_use_case = CheckUserSteamIDUseCase(
            users_repository=users_repository
        )
        self.get_user_use_case = GetUserUseCase(
            users_repository=users_repository
        )
        self.update_user_use_case = UpdateUserUseCase(
            users_repository=users_repository
        )
        self.vanity_user_use_case = SteamIDCorrectUseCase(
            steam_client = steam_client
        )
        self.get_player_steam_id_use_case = GetUserUseCase(
            users_repository=users_repository
        )
        self.search_games_short_use_case = SearchGamesUseCase(
            steam_client=steam_client
        )
        self.get_wishlist_use_case = GetWishlistsUseCase(
            wishlist_repository = wishlist_repository
        )
        self.create_wishlist_use_case = CreateWishlistsUseCase(
            wishlist_repository = wishlist_repository
        )
        self.add_wishlist_game_use_case = AddWishlistGame(
            users_repository=users_repository
        )
        self.get_games_to_wishlist_use_case = GetGamesToWishlistUseCase(
            steam_client=steam_client
        )
        self.get_wishlist_pages_use_case = GetWishlistsPagesUseCase(
            users_repository=users_repository
        )
        self.remove_wishlist_game_use_case = RemoveWishlistGameUseCase(
            users_repository=users_repository
        )

    def user_help(self):
        return help_config.get("user")

    async def update_or_register_user(self,user_id,steam_user:Optional[str]=None)->Optional[bool]:
        """
        return False - Означає що не було знайдено користувача
        return True - Все пройшло успішно
        """
        async for session in get_async_db():
            if steam_user is not None:
                steam_appid:Optional[SteamAppid] = await self.vanity_user_use_case.execute(steam_user=steam_user)
                if steam_appid is None:
                    return False
            else:
                return False
            user = await self.get_user_use_case.execute(session=session,user_id=user_id,integer=False)
            if user is None:
                await self.create_user_use_case.execute(user_id=user_id,steam_id=steam_appid['steam_appid'],session=session)
            else:
                await self.update_user_use_case.execute(user=user,session=session,steam_id=steam_appid["steam_appid"])
                logger.debug("Error Update User Use Case %s,%s User:",user_id,steam_appid,user)
            return True

    async def check_register_steam_id_user(self,user_id,session):
        data = await self.check_user_steam_id_use_case.execute(user_id=user_id,session=session)
        return data

    async def get_profile_user(self,telegram_id:int,session):
        """
        Повертає False коли користувач або не зареєстрований або не ввів steam_appid
        """
        steam_appid = await self.get_player_steam_id_use_case.execute(user_id=telegram_id,session=session)
        if steam_appid is None:
            return False
        return await self.get_player_full_stats_use_case.execute(user=steam_appid)

    async def search_games_short(self,name:str,page:int=1,limit:int=5):
        data = await self.search_games_short_use_case.execute(name=name,page=page,limit=limit,share=False)
        if data is None or len(data) == 0:
            return None
        return data

    async def add_wishlist_game(self, game:int,user_id:int,session)->bool:
        user_model = await self.get_user_use_case.execute(user_id=user_id,session=session,integer=False,other_models ="wishlist")
        logger.debug("Start Find User_Model %s",user_model)
        if user_model is None:
            return False
        if wishlist_model:= await self.get_wishlist_use_case.execute(game_id=game,session=session):
            logger.debug("WishlistModel finded %s",wishlist_model)
            pass
        else:
            #Відбувається запит до SteamAnalytic для отримання гри по Appid потім відбувається серіалізація
            #І занесення до бази даних нового wishlist.
            #І вже аж тоді додання до user нового wishlist.
            logger.debug("WishlistModel don`t found %s",wishlist_model)
            data:Optional[GamesToWishlist] = await self.get_games_to_wishlist_use_case.execute(steam_appid=game)
            logger.debug("Start Find Wishlist_Model %s",data)
            if data is None:
                return False
            if data.price_overview is None:
                wishlist_model=await self.create_wishlist_use_case.execute(game_id=data.steam_appid,name=data.name,short_desc=data.short_description,discount=0,price=0,session=session,back_response=True)
            else:
                wishlist_model=await self.create_wishlist_use_case.execute(game_id=data.steam_appid,name=data.name,short_desc=data.short_description,discount=data.price_overview.discount_percent,price=data.price_overview.final,session=session,back_response=True)
        logger.debug("Wishlist Model %s",wishlist_model)
        await self.add_wishlist_game_use_case.execute(wishlist=wishlist_model,user=user_model,session=session)
        return True

    async def remove_wishlist_game(self,user_id:int,game_id:int,session)->Optional[bool]:
        return await self.remove_wishlist_game_use_case.execute(user_id=user_id,game=game_id,session=session)

    async def show_wishlist_games(self,user_id:int,session,page:int=1,limit:int=5):
        return await self.get_wishlist_pages_use_case.execute(user_id=user_id,session=session,page=page,limit=limit)