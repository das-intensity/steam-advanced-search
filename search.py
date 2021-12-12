#!/usr/bin/env python

import argparse
import time

from core import *

def get_all_games_reviewed():
    all_games = get_all_games()
    all_games_reviewed = []
    for game in all_games:
        appid = game['appid']
        name = game['name']

        review = get_game_review_stats(appid, name, scrape=False)
        if review is None:
            continue

        game_review = review['query_summary']
        game_review.update(game)
        all_games_reviewed.append(game_review)

    return all_games_reviewed


def search(sort_by, min_reviews=None, min_score=None):
    res = get_all_games_reviewed()

    if min_reviews is not None:
        res = [x for x in res if x['total_reviews'] >= min_reviews]

    if min_score is not None:
        res = [x for x in res if x['review_score'] >= min_score]

    if sort_by == 'popularity':
        res.sort(key=lambda x: x['total_positive'] / (x['total_reviews']+1))
    elif sort_by == 'reviews':
        res.sort(key=lambda x: x['total_reviews'])
    else:
        raise NotImplementedError(f"sort_by={sort_by}")

    print(f"Found {len(res)} results:")
    for x in res:
        perc = x['total_positive'] * 100.0 / (x['total_reviews'] + 1)
        print(f"{perc:.0f}% ({x['total_reviews']}) - {x['name']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sort", default='popularity', help="Sort by: 'popularity' (default), 'reviews'")
    parser.add_argument("--min-reviews", type=int, help="minimum number of reviews")
    parser.add_argument("--min-score", type=int, help="minimum review score (e.g. 8 = 'Very Popular')")
    args = parser.parse_args()

    search(
            sort_by=args.sort,
            min_reviews=args.min_reviews,
            min_score=args.min_score,
            )
