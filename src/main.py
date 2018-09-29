#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import animelist
import anime


def parse_args():
    parser = argparse.ArgumentParser(description="Get the list of"
                                     " anime OP and ED from"
                                     " exported XML extracted from MAL.")

    parser.add_argument("--xml",
                        required=True,
                        help="Get data from XML exported MyAnimeList list")
    parser.add_argument("--include-ptw",
                        action="store_true",
                        help="Include Plan To Watch animes")
    args = parser.parse_args()

    return args


def main(username=None):
    args = parse_args()
    user_animelist = animelist.AnimeList(args.xml)
    print("Getting animes from MAL anime list...")
    user_animes = user_animelist.get_list_of_animes(args.include_ptw)
    print("Animes processed: {0}".format(len(user_animes)))
    anime.dump_to_tsv('anisongs.tsv', user_animes)


if __name__ == '__main__':
    main()
