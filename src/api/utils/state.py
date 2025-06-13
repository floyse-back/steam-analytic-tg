from aiogram.fsm.state import State,StatesGroup


class SteamGamesID(StatesGroup):
    game = State()

class PlayerSteamID(StatesGroup):
    player = State()
