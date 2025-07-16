from typing import List

from src.application.dto.steam_dto import GameFullModel, CalendarEventModel


class SubscribeStyleText:
    def new_release_message(self,data:List[GameFullModel]):
        pass

    def free_games_message(self,data:List[GameFullModel]):
        pass

    def hot_discount_message(self,data:List[GameFullModel]):
        pass

    def steam_event_message(self,data:CalendarEventModel):
        pass

    def steam_wishlist_message(self,data:List[GameFullModel]):
        pass