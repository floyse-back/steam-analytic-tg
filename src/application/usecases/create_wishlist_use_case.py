from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user_context.repository import IWishlistRepository
from src.infrastructure.db.models import Wishlist


class CreateWishlistsUseCase:
    def __init__(self,wishlist_repository:IWishlistRepository):
        self.wishlist_repository = wishlist_repository

    async def execute(self,game_id:int,name:str,short_desc:str,discount:int,price:int,session:AsyncSession,back_response:bool=False)->Optional[Wishlist]:
        return await self.wishlist_repository.create_wishlist(game_id=game_id,name=name,short_desc=short_desc,discount=discount,price=price,session=session,back_response=back_response)