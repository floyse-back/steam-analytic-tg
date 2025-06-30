from abc import ABC,abstractmethod
from typing import Optional, List

from src.domain.user_context.models import Users, Game


class IUsersRepository(ABC):
    @abstractmethod
    async def check_user_created(self,user_id:int,session)->bool:
        pass

    @abstractmethod
    async def check_user_steamid(self,user_id:int,session)->bool:
        pass

    @abstractmethod
    async def create_user(self,user_id:int,session,steam_id:Optional[int]=None,role:str="user")->None:
        pass

    @abstractmethod
    async def delete_user(self,user_id:int,session)->None:
        pass

    @abstractmethod
    async def get_user(self,user_id:int,session)->Optional[Users]:
        pass

    @abstractmethod
    async def update_user(self,user,steam_id,session)->None:
        pass

    @abstractmethod
    async def get_user_subscribes(self,session)->Optional[List["Subscribes"]]:
        pass

    @abstractmethod
    async def get_games_wishlist(self,user_id:int,session)->List["Wishlist"]:
        pass

    @abstractmethod
    async def add_game_wishlist_user(self,user:Users,game:Game,session)->None:
        pass

    @abstractmethod
    async def remove_game_wishlist_user(self,user:Users,game:Game,session)->None:
        pass

    @abstractmethod
    async def subscribe(self,type:int,user_id:int,session)->None:
        pass

    @abstractmethod
    async def unsubscribe(self,type:int,user_id:int,session)->None:
        pass


class IWishlistRepository(ABC):
    @abstractmethod
    async def update_game_whishlist(self,game_id:int,name:str,short_desc:Optional[str],price:int,session)->None:
        pass

    @abstractmethod
    async def get_game_whishlist(self,game_id:int,session)->Optional[Game]:
        pass



