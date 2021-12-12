import datetime
import json
import os
import time

import requests

DATA_PATH='steam-advanced-search-data'

ALL_GAMES_PATH=os.path.join(DATA_PATH, 'all_games.json')
ALL_GAMES=None

def get_all_games(fresh=False, max_age=None):
    global ALL_GAMES

    assert max_age is None, 'max_age not implemented'

    if ALL_GAMES is None and os.path.isfile(ALL_GAMES_PATH):
        ALL_GAMES = json.load(open(ALL_GAMES_PATH))

    if ALL_GAMES is None or fresh == True:
        print("SCRAPING ALL_GAMES FROM WEB")
        stamp = datetime.datetime.now().strftime('%Y%m%d')
        ALL_GAMES = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json').json()
        ALL_GAMES['stamp'] = stamp
        json.dump(ALL_GAMES, open(ALL_GAMES_PATH, 'w+'))

    return ALL_GAMES['applist']['apps']


def get_game_review_stats(appid, name='unspecified', max_age=None, scrape=None):
    print(f"Getting {appid} - {name}")
    assert max_age is None, 'max_age not implemented'

    path = os.path.join(DATA_PATH, 'games', f"{appid}.json")

    if os.path.isfile(path):
        print("exists")
        data = json.load(open(path))
    elif scrape is not False:
        stamp = datetime.datetime.now().strftime('%Y%m%d')
        data = requests.get(f"http://store.steampowered.com/appreviews/{appid}?json=1").json()
        #print(data)
        print("fresh")
        data['stamp'] = stamp
        json.dump(data, open(path, 'w+'))
        time.sleep(2)
    else:
        print("missing")
        return None

    return data

#STATS_PATH=os.path.join(DATA_PATH, 'stats.json')
