from src.domain.user_context.repository import IUsersRepository


class CheckSubscribesUserUseCase:
    def __init__(self, users_repository:IUsersRepository):
        self.users_repository = users_repository

    async def execute(self,user_id:int,type_id:int,session):
        return True