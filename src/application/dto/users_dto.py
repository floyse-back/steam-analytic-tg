from pydantic import BaseModel


class SteamAppid(BaseModel):
    steam_appid: int

    class Config:
        from_attributes = True

def transform_to_dto(model:BaseModel,orm:dict):
    return model.model_validate(orm).model_dump()