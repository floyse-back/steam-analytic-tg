from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Users:
    id:int
    steam_id:int
    role:int

    subscribes: List["Subscribes"]
    whishlist: List["Wishlist"]

@dataclass(frozen=True)
class Wishlist:
    game_id: int
    name:str
    short_desc:str
    discount:int
    price:int
    users: List["Users"]

@dataclass(frozen=True)
class Game:
    game_id: int
    name:str
    short_description:str