from src.domain.user_context.models import Users
from src.domain.user_context.repository import IUsersRepository
from src.infrastructure.logging.logger import logger


class GetUserUseCase:
    def __init__(self,users_repository:IUsersRepository):
        self.users_repository=users_repository

    async def execute(self,user_id:int,session,integer:bool=True):
        """
        Integer Вказує на те що ми отримаємо у відповідь загалом це steam_appid integer:bool
        Якщо integer False то весь об'єкт отримаємо
        """
        user:Users= await self.users_repository.get_user(user_id=user_id,session=session)
        logger.debug("Steam Appid From Use Case,%s",user)
        if user is None:
            return None
        if integer:
            return user.steam_id
        return user