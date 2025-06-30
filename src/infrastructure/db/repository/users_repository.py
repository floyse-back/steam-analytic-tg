from typing import Optional, List

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.user_context.repository import IUsersRepository
from src.infrastructure.db.models import Users, Wishlist
from src.infrastructure.logging.logger import logger


class UsersRepository(IUsersRepository):
    async def check_user_created(self,user_id:int,session):
        """
        Надає True тоді коли користувач вже є
        Надає False тоді коли користувач ще не створений
        """
        statement = select(Users.id).where(Users.id == user_id)
        result = await session.execute(statement)
        return True if result.scalars().first() else False

    async def check_user_steamid(self,user_id:int,session):
        """
        Видає True тоді коли користувач(user_id) зареєстрований + має steamid
        """
        statement = select(Users.steam_id).where(Users.id == user_id)
        result = await session.execute(statement)
        data = result.scalars().first()
        logger.debug(data)
        return True if data else False

    async def create_user(self,user_id:int,session,steam_id:Optional[int]=None,role:str="user")->None:
        new_model = Users(
            id=user_id,
            steam_id=steam_id,
            role=role
        )
        session.add(new_model)
        await session.commit()

    async def delete_user(self,user_id:int,session:AsyncSession)->None:
        statement = delete(Users).where(Users.id == user_id)
        await session.execute(statement)

    async def get_user(self,user_id:int,session:AsyncSession)->Optional[Users]:
        statement = select(Users).where(Users.id == user_id)
        result = await session.execute(statement)
        data = result.scalars().first()
        logger.debug("Data %d",data)
        return data

    async def update_user(self,user:Users,steam_id,session:AsyncSession)->None:
        user.steam_id = steam_id
        await session.commit()

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