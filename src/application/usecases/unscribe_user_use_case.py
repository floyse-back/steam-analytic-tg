from src.domain.user_context.repository import IUsersRepository


class UnsubscribeUserUseCase:
    def __init__(self,users_repositoty:IUsersRepository):
        self.users_repositoty=users_repositoty

    async def execute(self,user_id:int,type_id:int,session):
        return await self.users_repositoty.unsubscribe(user_id=user_id,type_id=type_id,session=session)
