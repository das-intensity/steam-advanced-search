#!/usr/bin/env python

import argparse
import time

from core import *



def scrape():
    all_games = get_all_games()

    for game in all_games:
        appid = game['appid']
        name = game['name']

        get_game_review_stats(appid, name)

    raise NotImplementedError



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("--initial", help="initial run, so create fresh stats files")
    parser.parse_args()

    scrape()
