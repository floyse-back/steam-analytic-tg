from typing import List

from sqlalchemy import select

from src.domain.subscribe_context.repository import ISubscribeRepository
from src.infrastructure.db.models import Subscribes, SubscribesType


class SubscribeRepository(ISubscribeRepository):
    async def get_subscribe_type(self,type:int,session)->List[Subscribes]:
        pass

    def get_user_id_from_subscribes_type(self,type_id:int,session)->List[int]:
        statement = (select(Subscribes.user_id).where(Subscribes.type_id == type_id))
        result = session.execute(statement)

        return result.scalars().all()
