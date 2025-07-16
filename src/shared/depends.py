from src.application.services.player_service import PlayerService
from src.application.services.steam_service import SteamService
from src.application.services.subscribe_service import SubscribeService
from src.application.services.users_service import UsersService
from src.infrastructure.db.repository.subscribe_repository import SubscribeRepository
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.infrastructure.db.repository.wishlist_repository import WishlistRepository
from src.infrastructure.logging.logger import Logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient


#Ініціалізація Services
def get_user_repository():
    return UsersRepository(
        logger = Logger(name="infrastructure.user_repository",file_path="infrastructure")
    )

def get_steam_service()->SteamService:
    return SteamService(
        steam_client=SteamAnalyticsAPIClient(),
        users_repository=get_user_repository(),
        logger = Logger(name="application.steam_service",file_path="application")
    )

def get_users_service()->UsersService:
    return UsersService(
        users_repository=get_user_repository(),
        steam_client=SteamAnalyticsAPIClient(),
        wishlist_repository=WishlistRepository(),
        logger = Logger(name="application.users_service",file_path="application")
    )

def get_player_service()->PlayerService:
    return PlayerService(
        steam_client=SteamAnalyticsAPIClient(),
        users_repository=get_user_repository(),
        logger = Logger(name="application.player_service",file_path="application")
    )

def get_subscribes_service()->SubscribeService:
    return SubscribeService(
        users_repository=get_user_repository(),
        subscribes_repository=SubscribeRepository(),
        logger = Logger(name="application.subscribes_service",file_path="application")
    )