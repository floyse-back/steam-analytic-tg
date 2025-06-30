from typing import Union

from pydantic import BaseModel,field_validator
from typing_extensions import Optional


class SteamAppid(BaseModel):
    steam_appid: int

    class Config:
        from_attributes = True

class SteamVanityNameCorrection(BaseModel):
    steam_appid: str

    @field_validator("steam_appid",mode='before')
    def format_steam_appid(cls, v:str):
        if isinstance(v, str) and v.strip().startswith("https://"):
            v = v.rstrip("/").split("/")[-1]
        return v

def transform_to_dto(model:BaseModel,orm:dict):
    return model.model_validate(orm).model_dump()