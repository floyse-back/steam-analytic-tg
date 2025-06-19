from aiogram.fsm.state import State,StatesGroup


class SteamGamesID(StatesGroup):
    game = State()

class PlayerSteamName(StatesGroup):
    player = State()

class PageNumberSwapper(StatesGroup):
    current_page = State()
