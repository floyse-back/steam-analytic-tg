from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Users:
    id:int
    steam_id:int
    role:int

    subscribes: List["Subscribes"]
    whishlist: List["Whishlist"]

@dataclass(frozen=True)
class Whishlist:
    game_id: int
    name:str
    short_desc:str
    price:int
    users: List["Users"]