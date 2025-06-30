from src.domain.user_context.repository import IUsersRepository


class UpdateUserUseCase:
    def __init__(self, users_repository:IUsersRepository):
        self.users_repository = users_repository

    async def execute(self,user,steam_id:int,session)->None:
        await self.users_repository.update_user(user=user,steam_id=steam_id,session=session)