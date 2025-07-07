from src.domain.user_context.repository import IUsersRepository


class AddWishlistGame:
    def __init__(self,users_repository:IUsersRepository):
        self.users_repository = users_repository

    async def execute(self,wishlist,user,session):
        await self.users_repository.add_game_wishlist_user(user=user, wishlist=wishlist,session=session)