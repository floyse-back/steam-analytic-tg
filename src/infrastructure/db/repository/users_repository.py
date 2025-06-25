from typing import Optional, List

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.user_context.repository import IUsersRepository
from src.infrastructure.db.models import Users, Wishlist


class UsersRepository(IUsersRepository):
    async def create_user(self,steam_id:Optional[int],id:int,role:str,session:AsyncSession)->None:
        new_model = Users(
            id=id,
            steam_id=steam_id,
            role=role
        )
        session.add(new_model)
        await session.commit()

    async def delete_user(self,user_id:int,session:AsyncSession)->None:
        statement = delete(Users).where(Users.id == user_id)
        await session.execute(statement)

    async def get_steam_id(self,user_id:int,session:AsyncSession)->Optional[int]:
        statement = select(Users.steam_id).where(Users.id == user_id)
        result = await session.execute(statement)

        return result.scalars().first()

    async def update_user(self,user_id:int,steam_id:int,role:str,session:AsyncSession)->None:
        pass

    async def get_user_subscribes(self,session:AsyncSession)->Optional[List["Subscribes"]]:
        pass

    async def get_games_wishlist(self,user_id:int,session:AsyncSession)->Optional[Users]:
        statement = select(Users.id).options(
            selectinload(Wishlist),
        ).where(Users.id == user_id).limit(1)

        result = await session.execute(statement)

        return result.scalars().all()

    async def add_game_wishlist_user(self,user_id:int,game_id:int,session:AsyncSession)->None:
        pass

    async def remove_game_wishlist_user(self,user_id:int,session:AsyncSession)->None:
        pass

    async def subscribe(self,type:int,user_id:int,session)->None:
        pass

    async def unsubscribe(self,type:int,user_id:int,session:AsyncSession)->None:
        pass