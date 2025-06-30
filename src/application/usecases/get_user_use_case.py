from src.domain.user_context.repository import IUsersRepository


class GetUserUseCase:
    def __init__(self,users_repository:IUsersRepository):
        self.users_repository=users_repository

    async def execute(self,user_id:int,session):
        user= await self.users_repository.get_user(user_id=user_id,session=session)
        return user