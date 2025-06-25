from typing import List

from src.domain.subscribe_context.repository import ISubscribeRepository
from src.infrastructure.db.models import Subscribes


class SubscribeRepository(ISubscribeRepository):
    async def get_subscribe_type(self,type:int,session)->List[Subscribes]:
        pass
