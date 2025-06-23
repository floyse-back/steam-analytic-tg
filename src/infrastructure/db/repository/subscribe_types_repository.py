from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.subscribe_context.repository import ISubscribesTypesRepository
from src.infrastructure.db.models import SubscribesType


class SubscribeTypesRepository(ISubscribesTypesRepository):
    async def delete_subscribe_types(self,session):
        pass

    async def check_from_type_and_id(self,type_id:int,session:AsyncSession)->bool:
        statement = select(SubscribesType.id).where(SubscribesType.id == type_id)
        result = await session.execute(statement)
        result = result.scalars().all()
        if result:
            return False
        return True

    async def create_subscribe_type(self,sub_id:int,name:str,session:AsyncSession):
        model = SubscribesType(
            id=sub_id,
            name=name
        )
        session.add(model)
        await session.commit()

    async def get_subscribe_types(self,session:AsyncSession)->List[SubscribesType]:
        statement = select(SubscribesType)
        result = await session.execute(statement)

        return result.scalars().all()

    async def get_subscribe_type(self,session:AsyncSession,type_id:Optional[int]=None,type_name:Optional[str]=None)->List[SubscribesType]:
        statement = select(SubscribesType)
        if type_id is not None:
            statement = statement.filter(SubscribesType.id == type_id)
        elif type_name is not None:
            statement = statement.filter(SubscribesType.name == type_name)

        result = await session.execute(statement)

        return result.scalars().first()