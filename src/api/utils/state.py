from aiogram.fsm.state import State,StatesGroup


class SteamGamesID(StatesGroup):
    game = State()

class PlayerSteamName(StatesGroup):
    player = State()

class ProfileSteamName(StatesGroup):
    profile = State()

class ChangeSteamName(StatesGroup):
    steam_appid_new = State()

class BattleSteamPlayer(StatesGroup):
    user_1 = State()
    user_2 = State()

class SteamPlayerName(StatesGroup):
    player = State()

class WishlistGame(StatesGroup):
    game = State()