from src.domain.subscribe_context.repository import ISubscribeRepository


class GetUserIDFromSubscribesTypeUseCase:
    def __init__(self,subscribes_repository:ISubscribeRepository):
        self.subscribes_repository = subscribes_repository

    def execute(self,type_id:int,session):
        data = self.subscribes_repository.get_user_id_from_subscribes_type(type_id=type_id,session=session)

        return data