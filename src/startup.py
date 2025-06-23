from src.infrastructure.db.repository.subscribe_types_repository import SubscribeTypesRepository
from src.infrastructure.logging.logger import logger
from src.shared.subscribe_types import SUBSCRIBES_TYPE_DATA


async def init_subscribe_types(session):
    logger.info("Init subscribe types")
    subscribe_types_repository = SubscribeTypesRepository()
    #Оновлення всіх типів subscribes
    for k,v in SUBSCRIBES_TYPE_DATA.items():
        if await subscribe_types_repository.check_from_type_and_id(type_id=k,session=session):
            await subscribe_types_repository.create_subscribe_type(sub_id=k,name=v,session=session)
    logger.info("Init subscribe types done")