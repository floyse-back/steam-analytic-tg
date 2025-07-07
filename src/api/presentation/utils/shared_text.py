from src.api.presentation.empty_messages import EmptyMessages


def create_short_search_games_shared(data ,page :int =1 ,limit :int =10):
    if data is None:
        return EmptyMessages.create_empty_message()
    new_text = ""
    start_number = (page -1 ) *limit +1

    for i ,game in enumerate(data):
        new_text += \
            (f"\n{start_number + i}.<b><a href='https://store.steampowered.com/app/{game["steam_appid"]}/'>{game['name']}</a></b>"
            f"\nЦіна гри: {game['final_formatted_price']}")
    return f"{new_text}"