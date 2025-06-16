from typing import Optional, List, Dict, Union

from pydantic import BaseModel


class GameShortModel(BaseModel):
    name:str
    steam_appid:Optional[int] = None
    final_formatted_price:Optional[str]
    discount:Union[int,str]
    game_ganre:List[Dict]
    short_description:Optional[str]
    url:Optional[str] = None

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

class GameLongModel(BaseModel):
    pass



def transform_to_dto(model:BaseModel,orm:dict):
    return model.model_validate(orm).model_dump()