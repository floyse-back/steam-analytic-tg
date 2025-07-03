from __future__ import annotations
import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, field_validator
import heapq

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

class SteamRatingModel(BaseModel):
    steam_appid:Optional[int]
    user_rating:int = 0
    personaname:Optional[str]
    player_level:Optional[int]
    player_xp:Optional[int]
    player_xp_needed_to_level_up:Optional[int]
    timecreated:Optional[datetime.date]
    timelive:Union[int,str]
    friends_count:Optional[int]
    badges_count:Optional[int]
    lastlogoff:Optional[datetime.date]
    playtime:Union[int,str]

    allow_games:bool = True
    allow_friends:bool = True
    allow_badges:bool = True

    @field_validator("lastlogoff","timecreated",mode="before")
    def change_unix_time_from_date(cls, v):
        if isinstance(v, int):
            return datetime.date.fromtimestamp(v)

    @field_validator("playtime", mode="before")
    def change_unix_time_playtime(cls, v):
        if isinstance(v, int):
            total_minutes = v  # наприклад, 120985 хв
            days = total_minutes // (24 * 60)
            hours = (total_minutes % (24 * 60)) // 60
            minutes = total_minutes % 60
            return "{:02}д. {:02}г. {:02}хв.".format(days, hours, minutes)
        return v

    @field_validator("timelive",mode="before")
    def change_unix_time(cls,v):
        if isinstance(v,(int,float)):
            delta = datetime.timedelta(seconds=v)
            total_days = delta.days
            years = total_days // 365
            days = total_days % 365
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60

            return f"{years:01}р. {days:02}д. {hours:02}г. {minutes:02}хв."
        return v

class SteamPlayer(BaseModel):
    user_data: Optional[PlayersLists] = None
    user_friends_list: Optional[FriendsListModel] = None
    user_badges: Optional[SteamBadgesListModel] = None
    user_games: Optional[GamesList] = None

    class Config:
        from_attributes = True

class PlayersLists(BaseModel):
    player:PlayerModel

    class Config:
        from_attributes = True

class PlayerModel(BaseModel):
    steamid:int
    personaname:Optional[str]
    avatarfull:Optional[str]
    personastate:Optional[int]
    communityvisibilitystate:Optional[int]
    profilestate:Optional[int]
    lastlogoff:Optional[datetime.date]
    #PrivateData
    realname:Optional[str] = None
    primaryclanid:Optional[int] = None
    timecreated:Optional[datetime.date] = None
    timelive:Union[int,str] = None
    gameid:Optional[int] = None
    gameextrainfo:Optional[str] = None
    loccountrycode:Optional[str] = None

    @field_validator("lastlogoff","timecreated",mode="before")
    def change_unix_time_from_date(cls, v):
        if isinstance(v, int):
            return datetime.date.fromtimestamp(v)
        return v

    @field_validator("timelive",mode="before")
    def change_unix_time(cls,v):
        if isinstance(v,(int,float)):
            delta = datetime.timedelta(seconds=v)
            total_days = delta.days
            years = total_days // 365
            days = total_days % 365
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60

            return f"{years:01}р. {days:02}д. {hours:02}г. {minutes:02}хв."
        return v



    class Config:
        from_attributes = True

class FriendsListModel(BaseModel):
    friends_count: Optional[int] = None
    first_friend: Optional[FriendsShortModel] = None
    last_friend: Optional[FriendsShortModel] = None
    friends: List[FriendsShortModel]

    class Config:
        from_attributes = True

class FriendsShortModel(BaseModel):
    steamid:str
    relationship:str
    friend_since:int

    class Config:
        from_attributes = True

class SteamUser(BaseModel):
    user_data: Optional[PlayersLists] = None
    user_friends_list: Optional[FriendsListModel] = None
    user_badges: Optional[SteamBadgesListModel] = None
    user_games: Optional[GamesList] = None

    class Config:
        from_attributes = True

class SteamOwnedGame(BaseModel):
    appid:Optional[int]
    name:Optional[str]
    playtime_forever:Optional[int]
    playtime_2weeks:Optional[int] = None
    rtime_last_played:Optional[int] = None

    class Config:
        from_attributes = True

class GamesList(BaseModel):
    game_count:int
    games:List[SteamOwnedGame]

    class Config:
        from_attributes = True

class ComparisonModel(BaseModel):
    user_1:Optional[Union[int,float,str]]
    user_2:Optional[Union[int,float,str]]
    difference:Optional[Union[int,float,str]]
    winner : Optional[str]

class PlayerComparison(BaseModel):
    user_1:str
    user_2:str
    player_level: Optional[ComparisonModel] = None
    player_xp: Optional[ComparisonModel] = None
    badge_count: Optional[ComparisonModel] = None
    total_badges_xp: Optional[ComparisonModel] = None
    game_count: Optional[ComparisonModel] = None
    total_playtime: Optional[ComparisonModel] = None
    total_rating: Optional[ComparisonModel] = None

def transform_to_dto(model:BaseModel,orm:dict):
    return model.model_validate(orm)