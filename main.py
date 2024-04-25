from typing import List

import requests
from bs4 import BeautifulSoup

from models import Base, Game, engine, session

game_name = input("Введите название игры: ")
game_name_encode = game_name.replace(" ", "+")
game_name_for_txt = game_name.replace(" ", "_")

URL = f"https://psprices.com/region-tr/games/?q={game_name_encode}&content_type="

content = requests.get(URL)
soup = BeautifulSoup(content.content, "html.parser")
links = soup.find_all("a")
games = soup.find_all(
    "span", {"class": "line-clamp-2 h-10 underline-offset-2 group-hover:underline"}
)
prices = soup.find_all("span", {"class": "font-bold"})

platforms = soup.find_all("img", {"class": "rounded-b aspect-square object-contain w-full"})

Base.metadata.create_all(engine)


def get_platforms():
    platforms_list = []
    for p in platforms:
        if "api.playstation" in p["data-src"]:
            platforms_list.append("PlayStation")
        elif "s-microsoft" in p["data-src"]:
            platforms_list.append("XBox")
    return platforms_list


def get_prices() -> List:
    prices_list = []
    for price in prices:
        if "bg-premium" not in price.get("class"):
            price_without_spaces = price.text.replace(" ", "").replace("\n", "")
            decode_price = price_without_spaces.split("\n")

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


def get_links_to_store():
    print(f"\nНайдено {len(get_links())} ссылок/ки\n")
    print("Программа проходит по ссылкам, пожалуйста, ожидайте...\n")

    links_to_store = []
    count = 0
    for i in get_links():
        result = requests.get(i)
        count += 1
        print(f"Пройдено ссылок: {count}")
        links_soup = BeautifulSoup(result.content, "html.parser")
        game_links = links_soup.find_all("a")
        for link in game_links:
            store_link = str(link.get("href"))
            if store_link.startswith("/game/buy/"):
                links_to_store.append(f"https://psprices.com{store_link}")
    return links_to_store


def create_new_list():
    print(get_games())
    new_list = list(
        zip(get_games(), get_platforms(), get_prices(), get_links_to_store())
    )
    print("\nИдёт запись в документ и базу данных, пожалуйста, ожидайте...")
    print(f"\nПройдено и выведено ссылок в документ: {len(new_list)}")
    return new_list


def insert_into_db():
    for i in create_new_list():
        new_games = Game(game_name=i[0], platform=i[1], price=i[2], link=i[3])

        session.add(new_games)
        session.commit()
        with open(f"result_{game_name_for_txt}", "a") as file:
            file.write(f"{i[0]}, {i[1]}, {i[2]}\n{i[3]}\n\n")


insert_into_db()
