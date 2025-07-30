from typing import Optional, List

from src.domain.logger import ILogger
from src.domain.user_context.repository import IWishlistRepository


class UpsertWishlistGamesUseCase:
    def __init__(self, wishlist_repository:IWishlistRepository,logger:ILogger):
        self.wishlist_repository = wishlist_repository
        self.logger = logger

    def execute(self,data:Optional[List[dict]],session):
        if data is None or len(data) == 0:
            return None
        self.logger.info("UpsertWishlistGamesUseCase execute data = %s",data)
        self.wishlist_repository.upsert_wishlist_games(data = data, session = session)

