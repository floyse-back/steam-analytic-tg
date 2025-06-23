from abc import ABC, abstractmethod
from typing import Union, List


class ISubscribeRepository(ABC):
    @abstractmethod
    async def show_subscribe_type(self,type:int,session):
        pass

class ISubscribesTypesRepository(ABC):
    @abstractmethod
    async def delete_subscribe_types(self,session):
        pass

    @abstractmethod
    async def check_from_type_and_id(self,id:int,session)->bool:
        pass

    @abstractmethod
    async def create_subscribe_type(self,type:int,session):
        pass

    @abstractmethod
    async def get_subscribe_types(self,session):
        pass

    @abstractmethod
    async def get_subscribe_type(self,type_id:int,session):
        pass
