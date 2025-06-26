from src.application.usecases.create_user_use_case import CreateUserUseCase
from src.domain.user_context.repository import IUsersRepository
from src.infrastructure.db.database import get_async_db
from src.shared.config import help_config


class UsersService:
    def __init__(self,users_repository:IUsersRepository):
        self.users_repository = users_repository
        self.create_user_use_case = CreateUserUseCase(
            users_repository=users_repository
        )

    def user_help(self):
        return help_config.get("user")

    async def start_register_user(self,user_id):
        async for session in get_async_db():
            await self.create_user_use_case.execute(user_id=user_id,session=session)


