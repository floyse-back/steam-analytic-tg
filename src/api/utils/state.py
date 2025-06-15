from aiogram.fsm.state import State,StatesGroup


class SteamGamesID(StatesGroup):
    game = State()

class PlayerSteamName(StatesGroup):
    player = State()
