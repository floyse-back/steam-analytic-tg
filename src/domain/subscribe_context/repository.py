from abc import ABC, abstractmethod
from typing import Union, List


class SubscribeRepository(ABC):
    @abstractmethod
    async def show_subscribe_type(self,type:int,session):
        pass

class SubscribesTypeRepository(ABC):
    @abstractmethod
    async def create_subscribe_types(self,type:Union[List[str],str],session):
        pass

    @abstractmethod
    async def get_subscribe_types(self,session):
        pass