from typing import Optional, List

from src.application.dto.steam_dto import ChangedGamesWishlistModel
from src.domain.logger import ILogger
from src.domain.user_context.repository import IWishlistRepository


class GetChangedWishlistGamesUseCase:
    def __init__(self,wishlist_repository: IWishlistRepository,logger:ILogger):
        self.wishlist_repository = wishlist_repository
        self.logger = logger

    def execute(self,session,data:Optional[List[dict]])->Optional[dict]:
        if data is None:
            return None
        data_appids = [i.get("game_id") for i in data]
        data_changes = self.wishlist_repository.get_games_changed(session=session,data=data_appids)

        users_to_games = {}
        self.logger.info(f"GetChangedWishlistGamesUseCase game={data}\n\n data_changes={data_changes}")
        for game in data:
            for last_game in data_changes:
                if game["game_id"] == last_game[0] and (game["price"] != last_game[2] or game["discount"] != last_game[3]):
                    change_model =ChangedGamesWishlistModel(
                                steam_appid=game['game_id'],
                                name = game['name'],
                                short_description = game['short_desc'],
                                price_now = game['price'],
                                discount_now = game['discount'],
                                price_before = last_game[2],
                                discount_before = last_game[3]
                            )
                    if users_to_games.get(last_game[1]) is None:
                        users_to_games[last_game[1]] = [
                            change_model
                        ]
                    else:
                        users_to_games[last_game[1]].append(change_model)

        return users_to_games

