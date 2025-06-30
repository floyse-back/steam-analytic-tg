from typing_extensions import Optional

from src.domain.user_context.repository import IUsersRepository
from src.infrastructure.logging.logger import logger


class CreateUserUseCase:
    def __init__(self,users_repository:IUsersRepository):
        self.users_repository = users_repository

    async def execute(self,user_id:int,session,steam_id:Optional[int]=None):
        if not await self.users_repository.check_user_created(user_id,session):
            await self.users_repository.create_user(user_id=user_id,steam_id=steam_id,session=session)
            logger.debug(f"Create user {user_id}")
