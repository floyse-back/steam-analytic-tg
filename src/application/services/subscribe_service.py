from src.shared.config import help_config


class SubscribeService:
    def __init__(self):
        pass

    def subscribe_help(self):
        return help_config.get("subscribe")