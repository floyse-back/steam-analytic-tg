from typing import Union

from pydantic import BaseModel,field_validator
from typing_extensions import Optional

from src.application.dto.steam_dto import PriceOverviewModel


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

class GamesToWishlist(BaseModel):
    steam_appid: int
    name:str
    short_description:str
    price_overview:Optional[PriceOverviewModel] = None

def transform_to_dto(model:BaseModel,orm:dict,model_dump=True):
    if model_dump:
        return model.model_validate(orm).model_dump()
    else:
        return model.model_validate(orm)