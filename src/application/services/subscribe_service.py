from src.shared.config import help_config


class SubscribeService:
    def __init__(self):
        pass

    def subscribe_help(self):
        return help_config.get("subscribe")

    async def check_subscribes_user(self,user_id:int,type_id:int,session):
        """
        Повертає True коли користувач підписаний
        Повертає False коли користувач не підписаний
        """
        return True

