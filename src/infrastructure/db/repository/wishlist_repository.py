from typing import Optional

from src.domain.user_context.models import Game
from src.domain.user_context.repository import IWishlistRepository


class WishlistRepository(IWishlistRepository):
    async def update_game_whishlist(self,game_id:int,name:str,short_desc:Optional[str],price:int,session) ->None:
        pass

    async def get_game_whishlist(self,game_id:int,session) ->Optional[Game]:
        pass


