from typing import Optional, List, Dict, Union

from pydantic import BaseModel


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

    class Config:
        from_attributes = True

def transform_to_dto(model:BaseModel,orm:dict):
    return model.model_validate(orm).model_dump()