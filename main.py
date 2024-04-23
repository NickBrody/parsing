from typing import List

from bs4 import BeautifulSoup
import requests

from models import Game, session, Base, engine

game_name = input("Введите название игры: ")
game_name_encode = game_name.replace(" ", "+")

URL = f"https://psprices.com/region-tr/games/?q={game_name_encode}&content_type="

content = requests.get(URL)
soup = BeautifulSoup(content.content, 'html.parser')
links = soup.find_all('a')
games = soup.find_all('span',
                      {'class': "leading-5 line-clamp-2 underline-offset-2 group-hover:underline"})
prices = soup.find_all('span', {'class': 'font-bold'})

platforms = soup.find_all('span', {'class': "flex items-center gap-1"})


def get_platforms():
    platforms_list = []
    for i in platforms:
        platform_arrays = f"{str(i.text)}\n"
        sorted_list = []
        split_list = platform_arrays.split(" ")

        for element in split_list:
            new_element = (element.replace('\n\n', '').
                           replace('\n', ' ').replace('+E', ''))
            sorted_list.append(new_element)
        platforms_list.append(sorted_list)

    cleaned_list = [[element.strip() for element in sublist] for sublist in platforms_list]
    result_list = [' '.join(inner_list) for inner_list in cleaned_list]

    return result_list


Base.metadata.create_all(engine)


def get_prices() -> List:
    prices_list = []
    for price in prices:
        if 'bg-premium' not in price.get('class'):
            price_without_spaces = price.text.replace(" ", '').replace("\n", '')
            decode_price = price_without_spaces.split('\n')

            for i in decode_price:
                if i.startswith("₺"):
                    prices_list.append(i)
    return prices_list


def get_games():
    games_list = []
    for game in games:
        games_list.append(game.text)
    return games_list


def get_links():
    links_list = []
    for link in links:
        str_link = str(link["href"])
        if str_link.startswith("/region-tr/game/"):
            links_list.append(f"https://psprices.com{str_link}")
    return links_list


def create_new_list():
    new_list = list(zip(get_games(), get_platforms(),
                        get_prices(), get_links()))
    return new_list


def insert_into_db():
    for i in create_new_list():
        new_games = Game(game_name=i[0],
                         platform=i[1],
                         price=i[2],
                         link=i[3])

        session.add(new_games)
        session.commit()
        with open(f"result_{game_name}", "a") as file:
            file.write(f"{i[0]}, {i[1]}, {i[2]}\n{i[3]}\n\n")


insert_into_db()
