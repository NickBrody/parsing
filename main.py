import os
from bs4 import BeautifulSoup
import requests

from models import Game, session, Base, engine

prices_list = []
games_list = []
links_list = []

game_name = input("Введите название игры: ")
game_name_encode = game_name.replace(" ", "+")

URL = f"https://psprices.com/region-tr/games/?q={game_name_encode}&content_type="

print(URL)

content = requests.get(URL)
soup = BeautifulSoup(content.content, 'html.parser')
links = soup.find_all('a')
games = soup.find_all('span',
                      {'class': "leading-5 line-clamp-2 underline-offset-2 group-hover:underline"})
prices = soup.find_all('span', {'class': 'font-bold'})

Base.metadata.create_all(engine)


def get_prices():
    for price in prices:
        if 'bg-premium' not in price.get('class'):
            price_without_spaces = price.text.replace(" ", '').replace("\n", '')
            decode_price = price_without_spaces.split('\n')

            for i in decode_price:
                if i.startswith("₺"):
                    prices_list.append(i)


def get_games():
    for game in games:
        games_list.append(game.text)


def get_links():
    for link in links:
        str_link = str(link["href"])
        if str_link.startswith("/region-tr/game/"):
            links_list.append(f"https://psprices.com{str_link}")


def create_new_list():
    get_games()
    get_prices()
    get_links()
    new_list = list(zip(games_list, prices_list, links_list))
    return new_list


def generate_result_filename():
    i = 1
    while os.path.exists(f"result_{i}.txt"):
        i += 1
    return f"result_{i}.txt"


filename = generate_result_filename()


def insert_into_db():
    for i in create_new_list():
        new_games = Game(game_name=i[0],
                         price=i[1],
                         link=i[2])

        session.add(new_games)
        session.commit()
        with open(filename, "a") as file:
            file.write(f"{i[0]}, {i[1]}\n{i[2]}\n\n")


insert_into_db()
