from aiogram.fsm.state import State,StatesGroup


class SteamGamesID(StatesGroup):
    game_id = State()

class PlayerSteamID(StatesGroup):
    game_id = State()
