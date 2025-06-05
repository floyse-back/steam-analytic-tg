from src.shared.config import help_config


class PlayerService:
    def __init__(self):
        pass

    def player_help(self):
        return help_config.get("player")

