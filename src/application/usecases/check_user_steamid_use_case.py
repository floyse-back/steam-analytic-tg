from src.domain.user_context.repository import IUsersRepository


class CheckUserSteamIDUseCase:
    def __init__(self,users_repository:IUsersRepository):
        self.users_repository = users_repository

    async def execute(self,user_id:int,session)->bool:
        data = await self.users_repository.check_user_steamid(user_id=user_id,session=session)
        return data