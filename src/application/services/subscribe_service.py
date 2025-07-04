from src.application.usecases.check_subscribes_user_use_case import CheckSubscribesUserUseCase
from src.application.usecases.subscribe_user_use_case import SubscribeUserUseCase
from src.application.usecases.unscribe_user_use_case import UnsubscribeUserUseCase
from src.domain.user_context.repository import IUsersRepository
from src.shared.config import help_config


class SubscribeService:
    def __init__(self,users_repository:IUsersRepository):
        self.subscribe_user_use_case = SubscribeUserUseCase(
            users_repository
        )
        self.unsubscribe_user_use_case = UnsubscribeUserUseCase(
            users_repository
        )
        self.check_subscribes_user_use_case = CheckSubscribesUserUseCase(
            users_repository=users_repository
        )

    def subscribe_help(self):
        return help_config.get("subscribe")

    async def check_subscribes_user(self,user_id:int,type_id:int,session):
        """
        Повертає True коли користувач підписаний
        Повертає False коли користувач не підписаний
        """
        return await self.check_subscribes_user_use_case.execute(user_id=user_id,type_id=type_id,session=session)

    async def subscribe(self,user_id:int,type_id:int,session):
        """
        True - успішно
        False - невдало
        """
        if await self.check_subscribes_user_use_case.execute(user_id=user_id,type_id=type_id,session=session):
            return False # Якщо знайдемо підписку то сенс нам від неї бо вона вже є
        return await self.subscribe_user_use_case.execute(user_id=user_id,type_id=type_id,session=session)

    async def unsubscribe(self,user_id:int,type_id:int,session):
        """
        True - успішно
        False - невдало
        """
        return await self.unsubscribe_user_use_case.execute(user_id=user_id,type_id=type_id,session=session)

