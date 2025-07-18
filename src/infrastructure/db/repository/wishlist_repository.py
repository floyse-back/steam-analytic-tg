from typing import Optional, List, Tuple, Sequence

from sqlalchemy import select, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.domain.user_context.repository import IWishlistRepository
from src.infrastructure.db.models import Wishlist, users_to_whishlist, Users, Subscribes


class WishlistRepository(IWishlistRepository):
    async def get_game_wishlist(self,game_id:int,session:AsyncSession) ->Optional[Wishlist]:
        statement = select(Wishlist).where(Wishlist.game_id == game_id)
        result = await session.execute(statement)

        return result.scalars().first()

    async def create_wishlist(self,game_id:int,name:str,short_desc:str,discount:int,price:int,session:AsyncSession,back_response:bool=False) ->Optional[Wishlist]:
        wishlist_model = Wishlist(
            game_id=game_id,
            name=name,
            short_desc=short_desc,
            discount=discount,
            price=price
        )

        session.add(wishlist_model)
        await session.flush()
        await session.commit()
        if back_response:
            return wishlist_model

    def get_game_node_wishlist(self,page:int,limit:int,session:Session)->Optional[Sequence[Wishlist]]:
        statement = select(Wishlist).offset((page-1)*limit).limit(limit)
        result = session.execute(statement)

        return result.scalars().unique().all()

    def upsert_wishlist_games(self,data:Optional[dict],session:AsyncSession)->None:
        statement = insert(Wishlist).values(
            data
        )
        statement = statement.on_conflict_do_update(
            index_elements=["game_id"],
            set_={
                "name": statement.excluded.name,
                "short_desc": statement.excluded.short_desc,
                "discount": statement.excluded.discount,
                "price": statement.excluded.price,
            }
        )
        session.execute(statement)
        session.commit()

    def get_games_changed(self, session, data:List[int])->List[Tuple[int, int,int,int]]:
        statement = (select(Wishlist.game_id,Users.id,Wishlist.price,Wishlist.discount)
                     .join(users_to_whishlist,Wishlist.game_id == users_to_whishlist.c.game_id)
                     .join(Users,Users.id == users_to_whishlist.c.user_id)
                     .join(Subscribes,Users.id == Subscribes.user_id)
                     .filter(and_(Subscribes.type_id == 4,Wishlist.game_id.in_(data)))
                     ).distinct()
        result = session.execute(statement)
        return result.fetchall()


