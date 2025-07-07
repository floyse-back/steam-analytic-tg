from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user_context.repository import IWishlistRepository
from src.infrastructure.db.models import Wishlist


class WishlistRepository(IWishlistRepository):
    async def update_game_wishlist(self,game_id:int,name:str,short_desc:Optional[str],price:int,session) ->None:
        pass

    async def get_game_wishlist(self,game_id:int,session:AsyncSession) ->Optional[Wishlist]:
        statement = select(Wishlist).where(Wishlist.game_id == game_id)
        result = await session.execute(statement)

        return result.scalars().first()

    async def create_wishlist(self,game_id:int,name:str,short_desc:str,discount:int,price:int,session:AsyncSession,back_response:bool=False) ->Optional[Wishlist]:
        wishlist_model = Wishlist(
            game_id=game_id,
            name=name,
            short_desc=short_desc,
            discount=discount,
            price=price
        )

        session.add(wishlist_model)
        await session.flush()
        await session.commit()
        if back_response:
            return wishlist_model



