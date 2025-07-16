from datetime import date
from typing import Optional, List, Dict, Union

from pydantic import BaseModel, field_validator

class CalendarEventModel(BaseModel):
    name: Optional[str]
    date_start: date
    date_end: date
    type_name: Optional[str] = 'festival'

    class Config:
        from_attributes = True

class GameShortModel(BaseModel):
    name:str
    steam_appid:Optional[int] = None
    final_formatted_price:Optional[str]
    discount:Union[int,str]
    game_ganre:List[Dict]
    short_description:Optional[str]
    img_url:Optional[str] = None

    class Config:
        from_attributes = True

class GameListModel(BaseModel):
    name:str
    steam_appid:Optional[int] = None
    final_formatted_price:Optional[str]
    discount:Union[int] = None

    class Config:
        from_attributes = True

class GameShortListModel(BaseModel):
    name:str
    appid:Union[int,str]
    price:Union[int,str]
    discount:Union[int,str]
    positive:Optional[int]
    negative:Optional[int]
    average_forever:Optional[int]
    img_url:Optional[str]

class CategoryOut(BaseModel):
    category_id: int
    category_name: str

    class Config:
        from_attributes = True

class GanresOut(BaseModel):
    ganres_id: int
    ganres_name: str

    class Config:
        from_attributes = True

class PublisherOut(BaseModel):
    publisher_id: int
    publisher_name: str

    class Config:
        from_attributes = True

class GameFullModel(BaseModel):
    steam_appid: int
    name: str
    is_free: Optional[bool] = None
    short_description: Optional[str] = None
    final_price: Optional[int] = None
    final_formatted_price: Optional[str] = None
    metacritic: Optional[str] = None
    discount: Optional[int] = None
    recomendations: Optional[int] = None
    release_data: Optional[date] = None

    game_ganre: List[GanresOut]
    game_publisher: List[PublisherOut]
    game_categories: List[CategoryOut]

    class Config:
        from_attributes = True

class GameForYouModel(BaseModel):
    appid:Union[int]
    name:Optional[str]
    img: Optional[str]
    rating:Optional[int] = None

class AchivementModel(BaseModel):
    name:str

    class Config:
        from_attributes = True

class AchievementsModel(BaseModel):
    total:Optional[int] = None
    highlighted:List[AchivementModel]

    class Config:
        from_attributes = True

class PriceOverviewModel(BaseModel):
    initial:Optional[int] = None
    final:Optional[int] = None
    discount_percent:Optional[int] = None
    initial_formatted:Optional[str] = None
    final_formatted:Optional[str] = None


class GameAchievementsModel(BaseModel):
    name:str
    steam_appid:Optional[int]
    achievements:AchievementsModel
    price_overview:Optional[PriceOverviewModel] = None
    short_description:Optional[str]

    class Config:
        from_attributes = True

class GamePriceModel(BaseModel):
    name:str
    steam_appid:Optional[int]
    short_description:Optional[str]
    price_overview:Optional[PriceOverviewModel] = None

    class Config:
        from_attributes = True

class GamesForYouModel(BaseModel):
    steam_appid:Optional[int]
    name:Optional[str]
    final_formatted_price:Optional[str]
    total:Optional[int]
    discount:Union[int]
    short_description:Optional[str]
    recomendations:Optional[int]
    metacritic:Optional[str]


class GameAppidValidatedModel(BaseModel):
    steam_appid:Optional[str]

    @field_validator("steam_appid",mode='before')
    def validate_steam_appid(cls, v:str):
        if isinstance(v,str) and v.strip().startswith("https://store.steampowered.com/app/"):
            v = v.replace("https://store.steampowered.com/app/","").split("/")[0]
        elif isinstance(v,str) and v.strip().startswith("https://steamcommunity.com/app/"):
            v = v.replace("https://steamcommunity.com/app/","").split("/")[0]
        elif isinstance(v,str):
            pass
        else:
            raise ValueError(f"steam_appid must be an integer, not {v}")
        return v

def transform_to_dto(model:BaseModel,orm:dict,model_dump=True):
    if model_dump:
        return model.model_validate(orm).model_dump()
    else:
        return model.model_validate(orm)