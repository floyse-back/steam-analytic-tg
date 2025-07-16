from src.application.usecases.check_subscribes_user_use_case import CheckSubscribesUserUseCase
from src.application.usecases.get_user_id_from_subscribes_type import GetUserIDFromSubscribesTypeUseCase
from src.application.usecases.subscribe_user_use_case import SubscribeUserUseCase
from src.application.usecases.unscribe_user_use_case import UnsubscribeUserUseCase
from src.domain.logger import ILogger
from src.domain.subscribe_context.repository import ISubscribeRepository
from src.domain.user_context.repository import IUsersRepository


class SubscribeService:
    def __init__(self,users_repository:IUsersRepository,subscribes_repository:ISubscribeRepository,logger:ILogger):
        self.logger = logger
        self.subscribe_user_use_case = SubscribeUserUseCase(
            users_repository
        )
        self.unsubscribe_user_use_case = UnsubscribeUserUseCase(
            users_repository
        )
        self.check_subscribes_user_use_case = CheckSubscribesUserUseCase(
            users_repository=users_repository
        )
        self.get_user_id_by_sub_type_use_case = GetUserIDFromSubscribesTypeUseCase(
            subscribes_repository=subscribes_repository
        )

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

    def get_user_id_by_subscribes_type(self,subscribes_type:int,session):
        return self.get_user_id_by_sub_type_use_case.execute(type_id=subscribes_type,session=session)