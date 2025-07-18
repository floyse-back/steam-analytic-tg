from src.application.dto.steam_dto import PriceOverviewModel
from src.application.dto.users_dto import GamesToWishlist
from src.domain.user_context.repository import IWishlistRepository


class GetWishlistGamesNodesUseCase:
    def __init__(self, wishlist_repository:IWishlistRepository):
        self.wishlist_repository = wishlist_repository

    def execute(self,session,page:int=1,limit:int=200):
        data_list = self.wishlist_repository.get_game_node_wishlist(page=page,limit=limit,session = session)
        if data_list is None or len(data_list) == 0:
            return None

        #Серіалізація
        serialize_data = [GamesToWishlist(
            steam_appid=data.game_id,
            name=data.name,
            short_description=data.short_desc,
            price_overview=PriceOverviewModel(
                final=data.price,
                discount_percent=data.discount
            )
        ).model_dump() for data in data_list]

        return serialize_data