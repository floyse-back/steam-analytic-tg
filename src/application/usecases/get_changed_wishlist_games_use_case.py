from typing import Optional, List

from src.application.dto.steam_dto import ChangedGamesWishlistModel
from src.domain.logger import ILogger
from src.domain.user_context.repository import IWishlistRepository


class GetChangedWishlistGamesUseCase:
    def __init__(self,wishlist_repository: IWishlistRepository,logger:ILogger):
        self.wishlist_repository = wishlist_repository
        self.logger = logger

    def execute(self, session, data: Optional[List[dict]]) -> Optional[dict]:
        if data is None:
            return None

        data_appids = [i.get("game_id") for i in data]
        data_changes = self.wishlist_repository.get_games_changed(session=session, data=data_appids)

        users_to_games = {}
        self.logger.info(f"GetChangedWishlistGamesUseCase game={data}\n\ndata_changes={data_changes}")

        for game in data:
            for last_game in data_changes:
                # last_game — це кортеж: (game_id, user_id, price, discount)
                game_id = last_game[0]
                user_id = last_game[1]
                price_before = last_game[2]
                discount_before = last_game[3]

                if (
                    game["game_id"] == game_id
                    and (game["price"] != price_before or game["discount"] != discount_before)
                ):
                    change_model = ChangedGamesWishlistModel(
                        steam_appid=game['game_id'],
                        name=game['name'],
                        short_description=game['short_desc'],
                        price_now=game['price'],
                        discount_now=game['discount'],
                        price_before=price_before,
                        discount_before=discount_before,
                    )

                    if users_to_games.get(user_id) is None:
                        users_to_games[user_id] = [change_model]
                    else:
                        users_to_games[user_id].append(change_model)

        self.logger.info(f"users_to_games={users_to_games}")
        return users_to_games
