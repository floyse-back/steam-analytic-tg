from typing import Optional

from sqlalchemy import delete, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.user_context.repository import IUsersRepository
from src.infrastructure.db.models import Users, Wishlist, Subscribes, SubscribesType, users_to_whishlist
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
        return data

    async def get_user_and_wishlist(self,user_id:int,session) ->Optional[Users]:
        statement = select(Users).options(
            selectinload(Users.wishlist),
        ).where(Users.id == user_id)
        result = await session.execute(statement)
        data = result.scalars().first()
        return data

    async def get_wishlist_user_pages(self,user_id:int,session,page:int=1,limit:int=5):
        statement = (select(Wishlist)
                     .join(users_to_whishlist)
                     .where(users_to_whishlist.c.user_id == user_id)
                     .offset((page-1)*limit).limit(limit))
        result = await session.execute(statement)
        return result.scalars().all()

    async def update_user(self,user:Users,steam_id,session:AsyncSession)->None:
        user.steam_id = steam_id
        await session.commit()

    async def get_user_subscribes(self,user_id:int,session:AsyncSession)->Optional[Users]:
        statement = select(Users.id).options(
            selectinload(Users.wishlist),
        ).where(Users.id == user_id).limit(1)

        result = await session.execute(statement)

        return result.scalars().first()

    async def get_games_wishlist(self,user_id:int,session:AsyncSession)->Optional[Users]:
        statement = select(Users.id).options(
            selectinload(Users.wishlist),
        ).where(Users.id == user_id).limit(1)

        result = await session.execute(statement)

        return result.scalars().first()

    async def add_game_wishlist_user(self,user:Users,wishlist:Wishlist,session:AsyncSession)->bool:
        user.wishlist.append(wishlist)
        for wishlist_model in user.wishlist:
            if wishlist_model.game_id == wishlist.game_id:
                return False
        await session.commit()
        return True

    async def remove_game_wishlist_user(self,user_id,game_id,session:AsyncSession)->Optional[bool]:
        try:
             statement = delete(users_to_whishlist).filter(and_(users_to_whishlist.c.user_id == user_id,users_to_whishlist.c.game_id == game_id))
             await session.execute(statement)
             await session.commit()
             return True
        except Exception as e:
            logger.error("SQLAlchemy Error: %s",e)
            return False

    async def check_subscribes(self,user_id:int,type_id:int,session:AsyncSession)->bool:
        statement = select(Subscribes).filter(Subscribes.type_id == type_id).filter(Subscribes.user_id == user_id)
        exsisting = await session.scalar(statement)
        if exsisting:
            return True
        return False

    async def subscribe(self,type_id:int,user_id:int,session:AsyncSession)->bool:
        subscribes_type_model  = await session.get(SubscribesType,type_id)
        if subscribes_type_model is None:
            logger.debug("subscribes_type_model not found %s",type_id)
            return False
        sub_model = Subscribes(
            user_id=user_id,
            type_id=type_id
        )
        session.add(sub_model)
        await session.commit()
        return True

    async def unsubscribe(self,type_id:int,user_id:int,session:AsyncSession)->bool:
        stmt = delete(Subscribes).filter(Subscribes.type_id == type_id).filter(Subscribes.user_id == user_id)
        await session.execute(stmt)
        await session.commit()
        return True