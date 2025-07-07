
from src.domain.user_context.repository import IUsersRepository


class RemoveWishlistGameUseCase:
    def __init__(self, users_repository:IUsersRepository):
        self.users_repository = users_repository

    async def execute(self,user_id:int,game:int,session):
        return await self.users_repository.remove_game_wishlist_user(user_id=user_id,game_id=game,session=session)
