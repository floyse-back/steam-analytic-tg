from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user_context.repository import IWishlistRepository
from src.infrastructure.db.models import Wishlist


class GetWishlistsUseCase:
    def __init__(self,wishlist_repository:IWishlistRepository):
        self.wishlist_repository = wishlist_repository

    async def execute(self,game_id:int,session:AsyncSession)->Optional[Wishlist]:
        return await self.wishlist_repository.get_game_wishlist(game_id=game_id,session=session)