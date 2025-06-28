import random

from typing_extensions import Optional

from src.application.dto.steam_dto import GameShortModel, transform_to_dto, GameAchievementsModel, GameListModel
from src.application.usecases.achievements_game_use_case import AchievementsGameUseCase
from src.application.usecases.check_game_price_use_case import GetCheckGamePriceUseCase
from src.application.usecases.discount_for_you_use_case import DiscountsGameForYouUseCase
from src.application.usecases.discounts_game_use_case import DiscountsGameUseCase
from src.application.usecases.free_games_now_use_case import FreeGamesNowUseCase
from src.application.usecases.games_for_you_use_case import GamesGameForYouUseCase
from src.application.usecases.most_played_games_use_case import MostPlayedGamesUseCase
from src.application.usecases.search_games_use_case import SearchGamesUseCase
from src.application.usecases.suggest_game_use_case import GetSuggestGameUseCase
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import help_config, ganre_config
from src.shared.dispatcher import DispatcherCommands
from src.shared.utils import escape_markdown


class SteamService:
    def __init__(self,steam_client:SteamAnalyticsAPIClient):
        self.steam_client = steam_client

        self.dispatcher_command = DispatcherCommands(
            command_map={
                "search_game":self.search_games,
                "games_for_you":self.games_for_you,
                "discount_for_you":self.discount_for_you,
                "achievements_game":self.achievements_game,
                "game_price":self.check_game_price
            }
        )

        self.search_games_use_case = SearchGamesUseCase(
            steam_client = self.steam_client,
        )
        self.discount_games_use_case = DiscountsGameUseCase(
            steam_client = self.steam_client,
        )
        self.most_played_games_use_case = MostPlayedGamesUseCase(
            steam_client = self.steam_client,
        )
        self.games_for_you_use_case = GamesGameForYouUseCase(
            steam_client = self.steam_client,
        )
        self.discount_for_you_use_case = DiscountsGameForYouUseCase(
            steam_client = self.steam_client,
        )
        self.free_games_now_use_case = FreeGamesNowUseCase(
            steam_client = self.steam_client,
        )
        self.achievements_game_use_case = AchievementsGameUseCase(
            steam_client = self.steam_client,
        )
        self.suggest_game_use_case = GetSuggestGameUseCase(
            steam_client = self.steam_client
        )
        self.steam_price_game = GetCheckGamePriceUseCase(
            steam_client = self.steam_client
        )

    def steam_help(self):
        return help_config.get("games")

    def __create_empty_message(self,game:Optional[str] = None):
        if game is None:
            return "🥺 Нажаль, гру не знайдено..."
        else:
            game = escape_markdown(text=game)
            return (f"🥺 Нажаль, гру за запитом: **{game}** не знайдено..."
                    f"\nМожливо, є помилка у назві? 🧐"
                    f"\n**Спробуй ще раз! 🙌🎮**")

    def __generate_first_smile(self):
        data = ["🎮","🎪","👻"]
        return random.choice(data)

    def __create_short_desc(self,data:GameShortModel):
        ganre_string = ""
        ganres_dict = data[f"game_ganre"]
        for i in range(0,min(len(ganres_dict),5)):
            ganre_string += f"{ganre_config.get(ganres_dict[i]["ganres_name"],"🎮")}" + ganres_dict[i]["ganres_name"] + " "

        first_smile = self.__generate_first_smile()
        price_smile = "🆓" if data["final_formatted_price"] == "Free" else "💵"

        discount_string = f" - ({data["discount"]})" if data["discount"]>0 else ""

        return f"""
{first_smile} [{data["name"]}](https://store.steampowered.com/app/{data["steam_appid"]}/) - {price_smile} {data["final_formatted_price"]}{discount_string}
_{data["short_description"]}_
✅ **Ganres:** {ganre_string}
        """

    def __create_achievements_description(self,data:GameAchievementsModel,page:int=1,offset:int=10):
        achievements_description = ""
        start_number = (page-1)*offset+1
        for i,ach in enumerate(data["achievements"]["highlighted"]):
            achievements_description += f" - {start_number+i}.{ach["name"]}\n"
        if achievements_description == "":
            achievements_description = "🚫Ця гра немає досягнень 🚫"

        text = (f"🔥 *Гра*: **[{data['name']}](https://store.steampowered.com/app/{data['steam_appid']}/)**\n"
                f"📝 *Короткий опис*: {data['short_description']}\n"
                f"**🏅 Кількість досягнень: {data['achievements']['total']}**\n"
                f"🏅 *Список досягнень*:\n{achievements_description}\n"
                f"{self.__generate_first_smile()} *Ціна*: **{data['price_overview']['final_formatted'] if data.get('price_overview') is not None else 'Безкоштовно'}**")
        return text

    def __create_short_list_games(self,data,page,limit):
        new_text = ""
        start_number = (page-1)*limit+1
        for i,game in enumerate(data):
            new_text += f"{start_number+i}.[{game["name"]}](https://store.steampowered.com/app/{game["appid"]}/) |{game["price"]/100 if not game["price"]==0 else "🆓"}$ | {f'({game["discount"]}%)' if game["discount"]>0 else ""}| 👍{game["positive"]} | 👎{game["negative"]} \n"

        return f"{new_text}"

    def __create_short_search_games(self,data,page,limit):
        new_text = ""
        start_number = (page-1)*limit+1
        for i,game in enumerate(data):
            new_text += (f"\n{start_number+i}.{game['name']}"
                         f"\nЦіна гри: {game['final_formatted_price']}")
        return f"{new_text}"

    async def search_games(self,name,page:int=1,limit:int=5,share:bool=True):
        """
        Повертає при share=True Pydantic:GameShortModel
        Повертає при share=False Pydantic:GameListModel
        """
        data = await self.search_games_use_case.execute(name,page=page,limit=limit,share=share)
        if data is None or len(data) == 0:
            return None
        return data

    async def discount_games(self,page:int=1,limit:int=10):
        data = await self.discount_games_use_case.execute(page=page,limit=limit)
        new_message = f"🎮🤑 **Найкращі знижки дня** 🤑🎮\n{self.__create_short_list_games(data,page,limit)}"
        return new_message

    async def free_games_now(self):
        data = await self.free_games_now_use_case.execute()

        if data is None or len(data) == 0:
            return self.__create_empty_message()

        for model in data:
            new_data = transform_to_dto(GameShortModel,model)
            new_message=f"{self.__create_short_desc(new_data)}"

        return data

    async def most_played_games(self,page:int=1,limit:int=10):
        data = await self.most_played_games_use_case.execute(page=page,limit=limit)

        text = self.__create_short_list_games(data,page,limit)
        text = "\t🔥🎮 **Найпопулярніші ігри:** 🎮🔥\n" + text
        return text

    async def games_for_you(self,user:Optional[str]=None):
        data =  await self.games_for_you_use_case.execute(user)
        return data

    async def discount_for_you(self,user:Optional[str]=None):
        data = await self.discount_for_you_use_case.execute(user)
        return data

    async def achievements_game(self,game:Optional[str]=None,page:int=1,offset:int=10):
        data = await self.achievements_game_use_case.execute(game=game,page=page,offset=offset)

        if data is None:
            return self.__create_empty_message(game=game)

        text = self.__create_achievements_description(data,page,offset)
        return text

    async def check_game_price(self,game:str):
        data = await self.steam_price_game.execute(game)

        if data is None:
            return self.__create_empty_message(game=game)

        return data

    async def suggest_game(self):
        data = await self.suggest_game_use_case.execute()
        return data

    async def dispatcher(self,command_name,*args,**kwargs):
        return await self.dispatcher_command.dispatch(command_name, *args, **kwargs)





