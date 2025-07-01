from typing import List, Optional

from pydantic import BaseModel


class SteamBadgeModel(BaseModel):
    badgeid:int
    level:int
    completion_time:int
    xp:int
    scarcity:int

    class Config:
        from_attributes = True

class SteamBadgesListModel(BaseModel):
    badges:List[SteamBadgeModel]
    player_xp: int
    player_level: int
    player_xp_needed_to_level_up: int
    player_xp_needed_current_level:int

    class Config:
        from_attributes = True

def transform_to_dto(model:BaseModel,orm:dict):
    return model.model_validate(orm).model_dump()