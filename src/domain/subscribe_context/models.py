from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Subscribes:
    id:int
    user_id:int
    type_id:int
    role_permitions:int

    user: "Users"
    type: SubscribeType

    subscribes_at: datetime

@dataclass
class SubscribeType:
    id:int
    name:str

    subscribes: List["Subscribes"]
