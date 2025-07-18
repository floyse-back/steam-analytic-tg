from typing import Optional, List

from src.application.usecases.check_subscribes_user_use_case import CheckSubscribesUserUseCase
from src.application.usecases.get_changed_wishlist_games_use_case import GetChangedWishlistGamesUseCase
from src.application.usecases.get_user_id_from_subscribes_type import GetUserIDFromSubscribesTypeUseCase
from src.application.usecases.get_wishlist_games_nodes_use_case import GetWishlistGamesNodesUseCase
from src.application.usecases.subscribe_user_use_case import SubscribeUserUseCase
from src.application.usecases.unscribe_user_use_case import UnsubscribeUserUseCase
from src.application.usecases.upsert_wishlist_games_use_case import UpsertWishlistGamesUseCase
from src.domain.logger import ILogger
from src.domain.subscribe_context.repository import ISubscribeRepository
from src.domain.user_context.repository import IUsersRepository, IWishlistRepository


class SubscribeService:
    def __init__(self,users_repository:IUsersRepository,subscribes_repository:ISubscribeRepository,logger:ILogger,wishlist_repository:IWishlistRepository):
        self.logger = logger
        self.subscribe_user_use_case = SubscribeUserUseCase(
            users_repository
        )
        self.unsubscribe_user_use_case = UnsubscribeUserUseCase(
            users_repository
        )
        self.check_subscribes_user_use_case = CheckSubscribesUserUseCase(
            users_repository=users_repository
        )
        self.get_user_id_by_sub_type_use_case = GetUserIDFromSubscribesTypeUseCase(
            subscribes_repository=subscribes_repository
        )
        self.get_wishlist_games_nodes_use_case = GetWishlistGamesNodesUseCase(
            wishlist_repository=wishlist_repository
        )
        self.upsert_wishlist_games_use_case = UpsertWishlistGamesUseCase(
            wishlist_repository=wishlist_repository,
            logger=logger
        )
        self.get_changed_games_use_case = GetChangedWishlistGamesUseCase(
            wishlist_repository=wishlist_repository
        )

    async def check_subscribes_user(self,user_id:int,type_id:int,session):
        """
        Повертає True коли користувач підписаний
        Повертає False коли користувач не підписаний
        """
        return await self.check_subscribes_user_use_case.execute(user_id=user_id,type_id=type_id,session=session)

    async def subscribe(self,user_id:int,type_id:int,session):
        """
        True - успішно
        False - невдало
        """
        if await self.check_subscribes_user_use_case.execute(user_id=user_id,type_id=type_id,session=session):
            return False # Якщо знайдемо підписку то сенс нам від неї бо вона вже є
        return await self.subscribe_user_use_case.execute(user_id=user_id,type_id=type_id,session=session)

    async def unsubscribe(self,user_id:int,type_id:int,session):
        """
        True - успішно
        False - невдало
        """
        return await self.unsubscribe_user_use_case.execute(user_id=user_id,type_id=type_id,session=session)

    def get_user_id_by_subscribes_type(self,subscribes_type:int,session):
        return self.get_user_id_by_sub_type_use_case.execute(type_id=subscribes_type,session=session)

    def update_push_wishlist_games(self,session,page:int=1,limit:int=250):
        data = [52]
        while True:
            data = self.get_wishlist_games_nodes_use_case.execute(page=page,limit=limit,session=session)
            if not data:
                break
            yield data
            page += 1

    def upsert_games_wishlist(self,session,data:Optional[List[dict]]):
        self.logger.info("UPSERT_GAMES_WISHLIST EXECUTED len(data) = %s",len(data))
        self.upsert_wishlist_games_use_case.execute(session=session,data=data)

    def get_updated_wishlists(self,session,data:Optional[List[dict]]):
        """
        Повертає dict який містить в собі
        Game Data та telegram_id user який підписаний на розсилку по wishlist
        """
        self.logger.info("get_updated_wishlists EXECUTED len(data) = %s",len(data))

    def get_changed_games(self,session,data:Optional[List[dict]]):
        self.logger.info("get_changed_games EXECUTED len(data) = %s",len(data))
        return self.get_changed_games_use_case.execute(session=session,data=data)
