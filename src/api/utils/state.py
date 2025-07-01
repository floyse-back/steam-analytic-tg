from aiogram.fsm.state import State,StatesGroup


class SteamGamesID(StatesGroup):
    game = State()

class PlayerSteamName(StatesGroup):
    player = State()

class ProfileSteamName(StatesGroup):
    profile = State()

class RatingSteamPlayer(StatesGroup):
    user_1 = State()
    user_2 = State()

class SteamPlayerName(StatesGroup):
    player = State()