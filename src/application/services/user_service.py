from src.shared.config import help_config


class UserService:
    def __init__(self):
        pass

    def user_help(self):
        return help_config.get("user")

