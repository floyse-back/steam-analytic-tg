from abc import ABC,abstractmethod
from typing import Optional, List


class IUsersRepository(ABC):
    @abstractmethod
    async def create_user(self,steam_id:Optional[int],id:int,session)->None:
        pass

    @abstractmethod
    async def delete_user(self,user_id:int,session)->None:
        pass

    @abstractmethod
    async def get_steam_id(self,user_id:int,session)->Optional[int]:
        pass

    @abstractmethod
    async def update_user(self,user_id:int,data:dict,session)->None:
        pass

    @abstractmethod
    async def show_user_subscribes(self,session)->Optional[List["Subscribes"]]:
        pass

    @abstractmethod
    async def show_game_whishlist(self,user_id:int,session)->List["Whishlist"]:
        pass

    @abstractmethod
    async def add_game_whishlist_user(self,user_id:int,game_id:int,session)->None:
        pass

    @abstractmethod
    async def remove_game_whishlist_user(self,user_id:int,game_id:int,session)->None:
        pass

    @abstractmethod
    async def subscribe(self,type:int,user_id:int,session)->None:
        pass

    @abstractmethod
    async def unsubscribe(self,type:int,user_id:int,session)->None:
        pass


class IWhishlistRepository(ABC):
    @abstractmethod
    async def update_game_whishlist(self,game_id:int,name:str,short_desc:Optional[str],price:int,session)->None:
        pass

