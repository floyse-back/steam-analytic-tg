from src.domain.user_context.models import Users
from src.domain.user_context.repository import IUsersRepository
from src.infrastructure.logging.logger import logger


class GetUserUseCase:
    def __init__(self,users_repository:IUsersRepository):
        self.users_repository=users_repository

    async def execute(self,user_id:int,session):
        user:Users= await self.users_repository.get_user(user_id=user_id,session=session)
        logger.debug("Steam Appid From Use Case,%s",user)
        return user.steam_id