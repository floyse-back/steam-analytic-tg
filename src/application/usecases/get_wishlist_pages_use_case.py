from src.application.dto.steam_dto import PriceOverviewModel
from src.application.dto.users_dto import GamesToWishlist
from src.domain.user_context.repository import IUsersRepository


class GetWishlistsPagesUseCase:
    def __init__(self,users_repository:IUsersRepository):
        self.users_repository = users_repository

    async def execute(self,user_id:int,session,page:int=1,limit:int=5):
        data_list =  await self.users_repository.get_wishlist_user_pages(user_id,session,page,limit)
        if data_list is None or len(data_list) == 0:
            return None

        serialize_data = [GamesToWishlist(
            steam_appid=data.game_id,
            name=data.name,
            short_description=data.short_desc,
            price_overview=PriceOverviewModel(
                final=data.price,
                discount_percent=data.discount
            )
        ) for data in data_list]
        return serialize_data